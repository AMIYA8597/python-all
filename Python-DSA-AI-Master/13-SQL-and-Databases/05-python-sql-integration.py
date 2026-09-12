"""
## A. Concept Name
Python SQL Integration & Database Management

## B. Motivation
Databases are essential for persistent storage. Python provides a standard API (PEP 249) for interacting with relational databases, allowing AI engineers to store, retrieve, and manipulate data seamlessly.

## C. Core Mechanics
Python uses the `sqlite3` module (for SQLite) or third-party drivers (like `psycopg2` for PostgreSQL) to connect to databases. The core workflow involves creating a connection, obtaining a cursor, executing SQL queries, and committing or rolling back transactions.

## D. Key Syntax
```python
import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM table_name')
results = cursor.fetchall()
conn.close()
```

## E. Common Patterns
- Context Managers: Using `with` statements to ensure connections are closed or transactions are automatically committed or rolled back.
- Parameterized Queries: Using `?` placeholders (or `%s` in other DBs) to prevent SQL injection.
- Fetching: Utilizing `fetchone()`, `fetchmany()`, or `fetchall()` effectively based on expected data size.

## F. Error Handling
Always catch exceptions like `sqlite3.Error` to gracefully handle database connectivity issues, constraint violations, missing tables, or syntax errors in queries.

## G. Best Practices
- Never use f-strings or string concatenation for SQL queries; always use parameterized queries to prevent SQL injection attacks.
- Keep transactions short to prevent locking issues.
- Set `row_factory` (e.g., `sqlite3.Row`) to access columns by name instead of index.

## H. AI & ML Integration
In AI pipelines, SQL databases are often used to store raw training data, feature stores, experiment metadata, and inference results. Libraries like Pandas integrate deeply via `read_sql` and `to_sql`.

## X. Project Connection
This integration acts as the foundational persistence layer of our AI projects. It will be used to store user configurations, application state, parsed datasets, and evaluation metrics for AI models.
"""

import sqlite3
import contextlib
import os

def run_python_sql_integration():
    db_file = 'example.db'
    
    # 1. Using context managers for connections and transactions
    print("--- 1. Context Managers & Parameterized Queries ---")
    with contextlib.closing(sqlite3.connect(db_file)) as conn:
        # Enable returning rows as dictionaries
        conn.row_factory = sqlite3.Row
        
        with conn: # This acts as a transaction manager (auto-commits or rolls back)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)')
            cursor.execute('DELETE FROM users') # Clear existing data
            
            # 2. Parameterized queries to prevent SQL Injection
            user_data = [
                ('admin', 'admin@example.com'),
                ('jdoe', 'jdoe@example.com'),
                ('smi', 'smith@example.com')
            ]
            cursor.executemany('INSERT INTO users (username, email) VALUES (?, ?)', user_data)
            print(f"Inserted {cursor.rowcount} users.")

    # 3. Fetching Data
    print("\n--- 2. Fetching Data (fetchone, fetchall, fetchmany) ---")
    with contextlib.closing(sqlite3.connect(db_file)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        
        # fetchone()
        first_user = cursor.fetchone()
        print(f"First User: {first_user['username']} ({first_user['email']})")
        
        # fetchmany()
        next_two = cursor.fetchmany(2)
        print("Next two users:")
        for u in next_two:
            print(f" - {u['username']}")
            
    print("\n--- 3. Handling Exceptions ---")
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            # This will fail because the table doesn't have a column 'age'
            cursor.execute('INSERT INTO users (username, age) VALUES (?, ?)', ('test', 25))
    except sqlite3.Error as e:
        print(f"Database error caught: {e}")

    # Cleanup
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("\nCleanup: Removed temporary database file.")
        except OSError:
            pass

if __name__ == "__main__":
    run_python_sql_integration()
