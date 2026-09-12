"""
## A. Concept Name
Advanced SQL Operations (Joins, CTEs, Window Functions)

## B. Analogy
Think of a database like an organized corporate filing system. 
- A simple query pulls a single folder.
- A JOIN is cross-referencing folders from two different departments.
- A CTE (Common Table Expression) is a temporary scratchpad summarizing data before the final report.
- A Window Function is like a running total on a bank statement—showing individual transactions alongside cumulative insights.

## C. Explanation
This module demonstrates advanced SQL queries using `sqlite3`:
1. **JOINS (INNER, LEFT):** Merge data from multiple tables based on relations.
2. **CTEs (WITH clause):** Define temporary result sets to simplify complex queries.
3. **Window Functions:** Compute aggregations and rankings over a specific "window" of rows without squashing the output like a standard GROUP BY.

## X. Project Connection
In AI and Data Science workflows, preprocessing relational data is critical. Advanced SQL allows you to push heavy data manipulation (ranking, aggregating, cross-referencing) down to the database engine, ensuring your Python AI models ingest clean, pre-computed features efficiently.
"""
import sqlite3

def run_advanced_sql():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Setup Tables
    cursor.execute('CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT)')
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            dept_id INTEGER,
            salary REAL,
            FOREIGN KEY (dept_id) REFERENCES departments (id)
        )
    ''')

    cursor.executemany('INSERT INTO departments (name) VALUES (?)', [('Engineering',), ('Sales',), ('Marketing',)])
    cursor.executemany('INSERT INTO employees (name, dept_id, salary) VALUES (?, ?, ?)', [
        ('Alice', 1, 95000),
        ('Bob', 1, 80000),
        ('Charlie', 2, 60000),
        ('David', 2, 70000),
        ('Eve', None, 50000) # Unassigned department
    ])

    print("--- 1. JOINS ---")
    print("INNER JOIN:")
    cursor.execute('''
        SELECT e.name, d.name 
        FROM employees e 
        INNER JOIN departments d ON e.dept_id = d.id
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nLEFT JOIN (includes employees without a department):")
    cursor.execute('''
        SELECT e.name, d.name 
        FROM employees e 
        LEFT JOIN departments d ON e.dept_id = d.id
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\n--- 2. Common Table Expressions (CTEs) ---")
    cursor.execute('''
        WITH DeptAvg AS (
            SELECT dept_id, AVG(salary) as avg_salary
            FROM employees
            WHERE dept_id IS NOT NULL
            GROUP BY dept_id
        )
        SELECT e.name, e.salary, d.avg_salary
        FROM employees e
        JOIN DeptAvg d ON e.dept_id = d.dept_id
        WHERE e.salary > d.avg_salary
    ''')
    print("Employees earning more than their department average:")
    for row in cursor.fetchall():
        print(row)

    print("\n--- 3. Window Functions ---")
    cursor.execute('''
        SELECT 
            name, 
            salary,
            RANK() OVER (ORDER BY salary DESC) as salary_rank,
            SUM(salary) OVER (PARTITION BY dept_id) as dept_total_salary
        FROM employees
    ''')
    print("Salary Ranking and Department Totals:")
    for row in cursor.fetchall():
        print(row)

    conn.close()

if __name__ == "__main__":
    run_advanced_sql()
