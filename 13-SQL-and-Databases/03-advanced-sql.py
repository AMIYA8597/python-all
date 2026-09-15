"""
# ==============================================================================
# LABORATORY: SQL & DATABASES (ADVANCED SQL / JOINS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer needs to find the names of all Users who bought an Item 
# over $100. They write a `SELECT * FROM users` query, pull 1,000,000 rows into 
# Python RAM, then write a `SELECT * FROM orders` query, pull 5,000,000 rows 
# into RAM, and use a Python `for` loop to match the IDs. The server crashes 
# with an OutOfMemory error after 45 seconds of O(N^2) looping.
#
# A senior database architect knows that Relational Databases are mathematically 
# optimized in C++ to perform Set Theory operations. They write an `INNER JOIN`. 
# The Database Engine mathematically hashes the primary keys and intersects the 
# tables on the Hard Drive, returning exactly the 5 rows needed across the 
# network in 0.002 seconds. The Python server uses 10 KB of RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Relational Set Theory (INNER, LEFT, CROSS JOINS).
# - Execute Data Aggregation (`GROUP BY`, `HAVING`).
# - Architect computational offloading (Window Functions & Subqueries).
#
# ==============================================================================
"""

import sqlite3
import os

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE SCHEMA & AGGREGATION)
# ==============================================================================
class AdvancedSQLSimulator:
    
    def __init__(self, db_path: str = "advanced_lab.db"):
        self.db_path = db_path
        self._initialize_database()
        
    def _initialize_database(self):
        """Bootstraps a Relational Schema (Users -> Orders)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users Table (The One)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            
            # Orders Table (The Many) - Foreign Key Relationship
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    amount DECIMAL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM orders")
            
            # Insert Users
            cursor.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [
                (1, "Alice"),
                (2, "Bob"),
                (3, "Charlie")  # Charlie has NO orders!
            ])
            
            # Insert Orders
            cursor.executemany("INSERT INTO orders (user_id, amount) VALUES (?, ?)", [
                (1, 150.0),
                (1, 200.0),
                (2, 50.0)
            ])
            conn.commit()


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL QUERIES
    # --------------------------------------------------------------------------
    def run_inner_join(self):
        """INNER JOIN: Mathematical Intersection (A ∩ B)."""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT users.name, orders.amount 
                FROM users 
                INNER JOIN orders ON users.id = orders.user_id
            """
            print("  [INNER JOIN] Returns ONLY users who actually have orders:")
            for row in conn.cursor().execute(query):
                print(f"    -> {row[0]} spent ${row[1]}")

    def run_left_join(self):
        """LEFT JOIN: Everything in A, plus matches in B (NULL if no match)."""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT users.name, orders.amount 
                FROM users 
                LEFT JOIN orders ON users.id = orders.user_id
            """
            print("\n  [LEFT JOIN] Returns ALL users. Missing orders are NULL:")
            for row in conn.cursor().execute(query):
                amount = row[1] if row[1] is not None else "NULL (No Orders)"
                print(f"    -> {row[0]} spent ${amount}")

    def run_aggregation(self):
        """GROUP BY / HAVING: Computational Offloading."""
        with sqlite3.connect(self.db_path) as conn:
            query = """
                SELECT users.name, SUM(orders.amount) as total_spent
                FROM users
                INNER JOIN orders ON users.id = orders.user_id
                GROUP BY users.id
                HAVING total_spent > 100
            """
            print("\n  [GROUP BY + HAVING] Calculates total per user, filters where Total > $100:")
            for row in conn.cursor().execute(query):
                print(f"    -> {row[0]} is a VIP! Total spent: ${row[1]}")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_advanced_sql():
    section_header("Database Execution: Advanced SQL")
    
    db_file = "advanced_lab.db"
    sim = AdvancedSQLSimulator(db_file)
    
    sim.run_inner_join()
    sim.run_left_join()
    sim.run_aggregation()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing JOINS and GROUP BY, we commanded the C++ Database Engine ")
    print("  to execute the heavy lifting on the Hard Drive, sending only the final ")
    print("  calculated 3 rows across the network to Python.")
    
    if os.path.exists(db_file):
        os.remove(db_file)


def run_all_labs():
    demonstrate_advanced_sql()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical and architectural difference between the `WHERE` clause and the `HAVING` clause?"
   Senior Answer: "The Order of Execution in the Database Engine. The `WHERE` clause executes *before* data is aggregated; it filters individual rows as they are read from the Hard Drive. The `GROUP BY` clause then mathematically aggregates the surviving rows into buckets (e.g., calculating `SUM(amount)` per user). The `HAVING` clause executes *after* the aggregation. You physically cannot write `WHERE SUM(amount) > 100` because the SUM has not been calculated yet. You must use `HAVING SUM(amount) > 100` to filter the aggregated buckets."

2. Interviewer: "If Table A has $1,000$ rows and Table B has $1,000$ rows, what happens if you write a `CROSS JOIN` (or a `SELECT * FROM A, B` without a WHERE clause)?"
   Senior Answer: "The Cartesian Product Disaster. An Inner Join uses a Hash map or B-Tree to match Primary Keys to Foreign Keys. A Cross Join mathematically forces every single row in Table A to combine with every single row in Table B. The Database Engine executes $1,000 \times 1,000 = 1,000,000$ row computations. If the tables are large (e.g., $100,000$ rows), this results in $10,000,000,000$ rows, immediately crashing the database server's RAM and CPU. This is why explicit `INNER JOIN ... ON ...` syntax is strictly enforced over legacy comma-separated queries."

3. Interviewer: "Explain what a Window Function (`OVER()`) is and how it replaces complex Python logic."
   Senior Answer: "Non-Collapsing Aggregation. If you use a `GROUP BY` to find the average salary of a department, the engine collapses all employee rows into a single 'Department' row. You lose the individual employee data. A Window Function (e.g., `AVG(salary) OVER (PARTITION BY department)`) calculates the aggregation *without* collapsing the rows. The Database Engine returns every single employee, but appends a new column containing the average salary of their specific department. This allows the architect to perform complex mathematical ranking (e.g., 'Top 3 highest paid per department') entirely in the Database Engine without writing O(N^2) sorting logic in Python."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SQL & Databases (Advanced SQL) Completed.")
