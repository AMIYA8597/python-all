"""
# ==============================================================================
# LABORATORY: SQL & DATABASES (BASIC SQL IN PYTHON)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a login system using Python and SQLite. They write:
# `cursor.execute(f"SELECT * FROM users WHERE email='{email}' AND pwd='{pwd}'")`
# A hacker enters `' OR '1'='1` into the email field. The resulting query mathematically 
# evaluates to True for every single row. The hacker instantly logs in as the Admin. 
# The company goes bankrupt.
#
# A senior software engineer understands "Parameterized Queries" and "Cursor Math". 
# They strictly decouple the SQL architectural string from the User Data payload. 
# They write: `cursor.execute("SELECT * FROM users WHERE email=? AND pwd=?", (email, pwd))`.
# The database engine treats the input strictly as literal strings, completely 
# nullifying the mathematical possibility of SQL Injection. The company survives.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the `sqlite3` built-in library.
# - Execute CRUD (Create, Read, Update, Delete) operations.
# - Architect SQL-Injection-Proof data pipelines via Parameterization.
# - Understand Cursor state machines and Transaction commits.
#
# ==============================================================================
"""

import sqlite3
import os

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE SQL INJECTION DISASTER)
# ==============================================================================
class DatabaseSimulator:
    
    def __init__(self, db_path: str = "lab_database.db"):
        self.db_path = db_path
        self._initialize_database()
        
    def _initialize_database(self):
        """Bootstraps a fresh Database with a Users table."""
        # The `with` statement ensures the connection mathematically closes!
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. CREATE (DDL - Data Definition Language)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            
            # Clear it out in case we run this script multiple times
            cursor.execute("DELETE FROM users")
            
            # 2. INSERT (DML - Data Manipulation Language)
            # Notice the '?' parameterization! This is safe.
            users_to_insert = [
                ("alice_admin", "ADMIN"),
                ("bob_user", "USER"),
                ("charlie_user", "USER")
            ]
            cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)", users_to_insert)
            
            # We MUST commit the transaction to save to disk!
            conn.commit()


    # --------------------------------------------------------------------------
    # THE ANTI-PATTERN: SQL INJECTION
    # --------------------------------------------------------------------------
    def vulnerable_login(self, username_input: str) -> list:
        """
        [WARNING] THIS IS CATASTROPHICALLY INSECURE.
        Using f-strings for SQL queries is a critical security vulnerability.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # The Junior Developer's Mistake
            query = f"SELECT * FROM users WHERE username = '{username_input}'"
            print(f"  [EXEC] Engine executing raw query: {query}")
            
            cursor.execute(query)
            return cursor.fetchall()

    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: PARAMETERIZATION
    # --------------------------------------------------------------------------
    def secure_login(self, username_input: str) -> list:
        """
        [SECURE] Parameterized Query.
        The Database Engine compiles the SQL statement FIRST, then binds the data.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # The Senior Engineer's Solution
            query = "SELECT * FROM users WHERE username = ?"
            print(f"  [EXEC] Engine compiled query: {query} | Bind: {username_input}")
            
            cursor.execute(query, (username_input,)) # Note the Tuple!
            return cursor.fetchall()


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_sql_security():
    section_header("Database Execution & Security")
    
    db_file = "security_lab.db"
    sim = DatabaseSimulator(db_file)
    
    print("\n  [SCENARIO 1] Normal User Login (Vulnerable Code)")
    result1 = sim.vulnerable_login("bob_user")
    print(f"  -> Returned: {result1}")
    
    print("\n  [SCENARIO 2] SQL Injection Attack! (Vulnerable Code)")
    # The Hacker types this into the HTML input box:
    malicious_input = "hacker' OR '1'='1"
    
    result2 = sim.vulnerable_login(malicious_input)
    print(f"  -> Returned: {result2}")
    print("  -> [FATAL ERROR] The hacker bypassed the WHERE clause and stole the Admin account!")
    
    print("\n  [SCENARIO 3] SQL Injection Attack! (Secure Code)")
    result3 = sim.secure_login(malicious_input)
    print(f"  -> Returned: {result3}")
    print("  -> [FLAWLESS] The engine treated the payload as a literal string. Zero rows returned.")
    
    # Cleanup
    if os.path.exists(db_file):
        os.remove(db_file)


def run_all_labs():
    demonstrate_sql_security()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Explain exactly how Parameterized Queries mathematically prevent SQL Injection."
   Senior Answer: "Execution Plan Separation. When a junior developer uses an f-string, they construct a single string and send it to the Database Engine. The engine parses the entire string as executable code. If the string contains `' OR '1'='1`, the engine executes it. When a senior developer uses Parameterized queries (`execute('...WHERE id=?', (val,))`), they send the SQL template and the Data Payload separately. The Database Engine compiles the SQL Execution Plan *first*, locking down the syntax tree. It then binds the Data Payload purely as literal bytes. The payload physically cannot alter the syntax tree, rendering SQL injection mathematically impossible."

2. Interviewer: "What is the difference between `cursor.fetchone()`, `cursor.fetchmany()`, and `cursor.fetchall()`, and when would you use each?"
   Senior Answer: "Memory Constraints (RAM Optimization). `fetchall()` commands the C-driver to load the entire query result from the Hard Drive into a massive Python List in RAM. If the query returns $10,000,000$ rows, the server will crash with an OutOfMemory error. `fetchone()` acts as a Generator/Iterator, pulling exactly one row into RAM, processing it, and discarding it, guaranteeing $O(1)$ memory usage. `fetchmany(size)` allows you to pull chunks (e.g., $10,000$ rows at a time), striking the perfect architectural balance between RAM limits and Network I/O latency."

3. Interviewer: "If you execute `cursor.execute('UPDATE users SET balance = 0')`, but your Python script crashes before calling `conn.commit()`, what happens to the Database?"
   Senior Answer: "The ACID 'Atomicity' Rollback. Relational databases wrap DML (Data Manipulation Language) commands in Transactions. When you run `execute()`, the database applies the changes to an isolated 'working memory' buffer (or Write-Ahead Log), not the physical master disk. Because the Python script crashed before issuing the mathematical `COMMIT` command, the database engine detects the dropped connection. It executes an automatic `ROLLBACK`, discarding the working memory. The `users` table mathematically remains untouched, preserving absolute Data Integrity."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SQL & Databases (Basic SQL) Completed.")
