"""
# 03 - Advanced SQL: Joins, CTEs, Window Functions, and Query Plans

## A. Concept Name
Advanced SQL Data Manipulation

## B. One-Sentence Definition
Advanced SQL enables complex analytical reasoning directly inside the database engine—using CTEs to structure logic, Window Functions to analyze sequences without squashing rows, and Query Execution Plans to ensure performance.

## C. Why Does This Exist?
A beginner downloads all tables into Python as Pandas DataFrames and uses Python to merge, filter, and calculate moving averages. This is an anti-pattern called "Data Swamp."
When dealing with 500 million rows, Python will run out of RAM and crash. 
The database engine is highly optimized in C/C++ to do these operations hundreds of times faster without sending gigabytes over the network. Push the compute to the data!

## D. Intuition & Real-World Analogy
- **A Simple Query**: Asking the librarian for a book.
- **A JOIN**: Asking the librarian to find a book, check the author's biography in a separate room, and staple them together for you.
- **A CTE (Common Table Expression)**: Giving the librarian a temporary scratchpad. "First, list all authors from Europe. Call this list X. Now, from list X, find who sold the most books."
- **A Window Function**: Looking at a bank statement. You see each individual transaction (row), but you also see a "Running Balance" next to it (a window function).

## E. Core Mathematical Concepts

### 1. JOIN Types
- `INNER JOIN`: Only keep rows where the condition matches in BOTH tables. (Set Intersection).
- `LEFT JOIN`: Keep ALL rows from the left table. If there is no match in the right table, fill with `NULL`.
- `FULL OUTER JOIN`: Keep everything from both tables, fill missing matches with `NULL`. (Set Union).

### 2. Window Functions (OVER / PARTITION BY)
Unlike `GROUP BY`, which squashes 100 rows into 1 summary row, a Window Function calculates a summary value but keeps all 100 rows intact.
- `ROW_NUMBER()`: 1, 2, 3, 4 (Strictly sequential)
- `RANK()`: 1, 2, 2, 4 (Skips ranks if there's a tie)
- `DENSE_RANK()`: 1, 2, 2, 3 (Never skips ranks)

### 3. EXPLAIN QUERY PLAN
Before running a query, the SQL engine compiles it. `EXPLAIN` tells you if the engine is doing a "Full Table Scan" (O(N)) or an "Index Lookup" (O(log N)).

## F. Common Mistakes & Anti-Patterns
1. **Accidental Cartesian Products (Cross Joins)**: Forgetting the `ON` clause in a JOIN. If Table A has 1,000 rows and Table B has 1,000 rows, the result will have 1,000,000 rows, crashing your server.
2. **Filtering a LEFT JOIN in the WHERE clause**: If you do a `LEFT JOIN` and then put a condition on the right table in the `WHERE` clause (e.g., `WHERE right_table.status = 'active'`), you accidentally convert it into an `INNER JOIN` because `NULL != 'active'`.

## G. Interview Connection
**Q: "What is the difference between WHERE and HAVING?"**
A: "`WHERE` filters rows BEFORE they are aggregated by `GROUP BY`. `HAVING` filters the aggregated results AFTER the `GROUP BY` has happened."

**Q: "What is the difference between RANK() and DENSE_RANK()?"**
A: "If two employees tie for the top salary, both get rank 1. `RANK()` will assign the next employee rank 3. `DENSE_RANK()` will assign the next employee rank 2."

## H. Implementation & Guided Practice
"""

import sqlite3
import pandas as pd # Used purely for pretty printing tables

def print_query(cursor, query: str, title: str):
    print(f"\n--- {title} ---")
    cursor.execute(query)
    # Fetch column names
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    # Use Pandas purely for pretty CLI formatting
    df = pd.DataFrame(rows, columns=columns)
    print(df.to_string(index=False))

def run_advanced_sql_masterclass():
    # 1. Setup in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 2. Create Schema
    cursor.execute('CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT)')
    cursor.execute('''
        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            dept_id INTEGER,
            salary REAL,
            hire_date TEXT,
            FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
        )
    ''')

    # 3. Insert Data
    cursor.executemany('INSERT INTO departments (dept_name) VALUES (?)', [
        ('Engineering',), ('Sales',), ('Marketing',), ('HR',) # HR has no employees yet
    ])
    cursor.executemany('INSERT INTO employees (name, dept_id, salary, hire_date) VALUES (?, ?, ?, ?)', [
        ('Alice', 1, 120000, '2020-01-15'),
        ('Bob', 1, 120000, '2021-03-10'), # Tied salary with Alice
        ('Charlie', 1, 95000, '2022-07-01'),
        ('Diana', 2, 110000, '2019-11-20'),
        ('Eve', 2, 70000, '2023-01-05'),
        ('Frank', None, 50000, '2023-06-15') # Contractor, no department
    ])
    conn.commit()

    # ==========================================
    # 1. ADVANCED JOINS
    # ==========================================
    print_query(cursor, '''
        SELECT e.name, e.salary, d.dept_name
        FROM employees e
        INNER JOIN departments d ON e.dept_id = d.dept_id
    ''', "1A. INNER JOIN (Only matches)")

    print_query(cursor, '''
        SELECT e.name, e.salary, d.dept_name
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
    ''', "1B. LEFT JOIN (Includes Frank with NULL dept)")

    # SQLite doesn't natively support RIGHT or FULL OUTER JOIN perfectly, 
    # but we can simulate FULL OUTER JOIN using UNION.
    
    # ==========================================
    # 2. COMMON TABLE EXPRESSIONS (CTEs)
    # ==========================================
    # Goal: Find all employees who earn MORE than their department's average.
    print_query(cursor, '''
        WITH DeptAverages AS (
            SELECT dept_id, AVG(salary) as avg_salary
            FROM employees
            WHERE dept_id IS NOT NULL
            GROUP BY dept_id
        )
        SELECT e.name, e.salary, d.dept_name, da.avg_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        JOIN DeptAverages da ON e.dept_id = da.dept_id
        WHERE e.salary > da.avg_salary
    ''', "2. CTEs: Employees earning > Dept Average")

    # ==========================================
    # 3. WINDOW FUNCTIONS
    # ==========================================
    # Goal: Rank employees by salary WITHIN their departments, and show running total.
    print_query(cursor, '''
        SELECT 
            name, 
            d.dept_name,
            salary,
            RANK() OVER(PARTITION BY e.dept_id ORDER BY salary DESC) as rank,
            DENSE_RANK() OVER(PARTITION BY e.dept_id ORDER BY salary DESC) as dense_rank,
            SUM(salary) OVER(PARTITION BY e.dept_id ORDER BY hire_date) as running_total_cost
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.dept_id
    ''', "3. WINDOW FUNCTIONS (Partition, Rank, Running Total)")
    
    # Notice how Alice and Bob both have 120k in Engineering. 
    # RANK and DENSE_RANK both give them '1'.
    # But Charlie gets '3' in RANK, and '2' in DENSE_RANK.

    # ==========================================
    # 4. EXPLAIN QUERY PLAN (Performance)
    # ==========================================
    print("\n--- 4. EXPLAIN QUERY PLAN ---")
    cursor.execute('''
        EXPLAIN QUERY PLAN
        SELECT * FROM employees WHERE salary = 95000
    ''')
    for row in cursor.fetchall():
        print(row)
        
    print("\nNotice it says 'SCAN TABLE employees'. This means O(N) full table scan!")
    print("Let's add an index and see what happens...")
    
    cursor.execute('CREATE INDEX idx_salary ON employees(salary)')
    cursor.execute('''
        EXPLAIN QUERY PLAN
        SELECT * FROM employees WHERE salary = 95000
    ''')
    for row in cursor.fetchall():
        print(row)
    print("Notice it now says 'SEARCH TABLE employees USING INDEX idx_salary'. This is O(log N) B-Tree lookup!")

    conn.close()

## I. Active Recall Questions
"""
1. You want to see ALL departments, even if they have no employees. Which JOIN do you use?
   *Answer: A RIGHT JOIN (or a LEFT JOIN if departments is the left table). INNER JOIN would exclude empty departments.*
2. How does a CTE improve readability over nested subqueries?
   *Answer: A subquery forces you to read inside-out. A CTE allows you to define the logic top-to-bottom sequentially, acting like a named variable.*
3. What is the difference between GROUP BY and OVER (PARTITION BY)?
   *Answer: GROUP BY collapses the rows into a single summary row. OVER calculates the summary but attaches it to every original individual row.*
"""

if __name__ == "__main__":
    print("========== ADVANCED SQL MASTERCLASS ==========")
    run_advanced_sql_masterclass()
    print("\n========== MASTERCLASS COMPLETE ==========")
