"""
## A. Concept Name
SQL Basics in Python using sqlite3

## B. Core Explanation
This module provides a comprehensive, production-ready implementation of basic SQL operations (CRUD - Create, Read, Update, Delete) using Python's built-in `sqlite3` library.

## C. Best Practices & Design Patterns
It demonstrates best practices including:
- Type hinting
- Context managers for robust resource handling (connections and cursors)
- Parameterized queries to prevent SQL injection
- Proper error handling and logging
- Object-Oriented design

## D. Industry Use Cases
- Local application data storage (desktop apps, mobile apps).
- Caching layer for web applications.
- Embedded databases for IoT devices.
- Automated testing (using in-memory SQLite databases) before deploying to Postgres/MySQL.

## X. Project Connection
This file serves as a foundational step for implementing databases in complex AI and DSA projects, demonstrating how to securely and efficiently persist application state.
"""

import sqlite3
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class User:
    """Data class representing a User entity."""
    user_id: Optional[int]
    username: str
    email: str
    age: int

class DatabaseManager:
    """
    Manages database connections and operations.
    """
    def __init__(self, db_path: str = ":memory:"):
        """
        Initializes the DatabaseManager.
        
        Args:
            db_path: Path to the SQLite database file. Defaults to ":memory:" for testing.
        """
        self.db_path = db_path
        # Enforce foreign key constraints in SQLite
        self._execute_pragma("PRAGMA foreign_keys = ON;")

    @contextmanager
    def get_connection(self):
        """
        Context manager that yields a database connection and ensures it is closed.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            # Use Row factory to access columns by name
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def _execute_pragma(self, pragma_query: str) -> None:
        """Executes a PRAGMA statement to configure SQLite."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(pragma_query)
            conn.commit()

    def create_tables(self) -> None:
        """
        Creates the necessary tables if they do not exist.
        """
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL CHECK(age >= 0)
        );
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
            logger.info("Tables ensured successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def insert_user(self, user: User) -> int:
        """
        Inserts a new user into the database using parameterized queries to prevent SQL injection.
        
        Args:
            user: The User object to insert.
            
        Returns:
            The auto-generated user ID.
        """
        query = """
        INSERT INTO users (username, email, age)
        VALUES (?, ?, ?);
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user.username, user.email, user.age))
                conn.commit()
                last_id = cursor.lastrowid
                logger.info(f"Inserted user {user.username} with ID {last_id}.")
                return last_id
        except sqlite3.IntegrityError as e:
            logger.warning(f"Integrity Error (e.g., duplicate username/email): {e}")
            raise
        except sqlite3.Error as e:
            logger.error(f"Failed to insert user: {e}")
            raise

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.
        """
        query = "SELECT id, username, email, age FROM users WHERE id = ?;"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return User(user_id=row['id'], username=row['username'], email=row['email'], age=row['age'])
                return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            raise

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.
        """
        query = "SELECT id, username, email, age FROM users ORDER BY id ASC;"
        users = []
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    users.append(User(user_id=row['id'], username=row['username'], email=row['email'], age=row['age']))
            return users
        except sqlite3.Error as e:
            logger.error(f"Error fetching all users: {e}")
            raise

    def update_user_email(self, user_id: int, new_email: str) -> bool:
        """
        Updates the email address of a specific user.
        
        Args:
            user_id: ID of the user.
            new_email: The new email address.
            
        Returns:
            True if the update was successful, False otherwise.
        """
        query = "UPDATE users SET email = ? WHERE id = ?;"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (new_email, user_id))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Updated email for user ID {user_id}.")
                else:
                    logger.warning(f"User ID {user_id} not found for update.")
                return success
        except sqlite3.Error as e:
            logger.error(f"Error updating user ID {user_id}: {e}")
            raise

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user from the database.
        """
        query = "DELETE FROM users WHERE id = ?;"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (user_id,))
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    logger.info(f"Deleted user ID {user_id}.")
                return success
        except sqlite3.Error as e:
            logger.error(f"Error deleting user ID {user_id}: {e}")
            raise

    def bulk_insert_users(self, users: List[User]) -> None:
        """
        Inserts multiple users efficiently using executemany.
        """
        query = "INSERT INTO users (username, email, age) VALUES (?, ?, ?);"
        # Extract tuple data for executemany
        user_data = [(u.username, u.email, u.age) for u in users]
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # executemany is significantly faster than executing single inserts in a loop
                cursor.executemany(query, user_data)
                conn.commit()
                logger.info(f"Bulk inserted {cursor.rowcount} users.")
        except sqlite3.Error as e:
            logger.error(f"Bulk insert failed: {e}")
            raise


# ==========================================
# Tests / Execution Block
# ==========================================
if __name__ == "__main__":
    print("--- Starting SQL Basics Demonstration ---")
    
    # 1. Initialize DB Manager (using in-memory DB for this demonstration)
    db = DatabaseManager(":memory:")
    
    # 2. Create tables
    db.create_tables()
    
    # 3. Insert a user
    user1 = User(user_id=None, username="alice_smith", email="alice@example.com", age=28)
    user1_id = db.insert_user(user1)
    
    # 4. Fetch the user
    fetched_user = db.get_user_by_id(user1_id)
    print(f"Fetched User: {fetched_user}")
    
    # 5. Bulk insert
    users_to_add = [
        User(None, "bob_jones", "bob@example.com", 35),
        User(None, "charlie_brown", "charlie@example.com", 22),
        User(None, "diana_prince", "diana@example.com", 30)
    ]
    db.bulk_insert_users(users_to_add)
    
    # 6. Fetch all users
    all_users = db.get_all_users()
    print(f"\nAll Users ({len(all_users)} total):")
    for u in all_users:
        print(f"  - {u.username} ({u.email}), Age {u.age}")
        
    # 7. Update a user
    print("\nUpdating Bob's email...")
    bob_db_id = next(u.user_id for u in all_users if u.username == "bob_jones")
    db.update_user_email(bob_db_id, "bob_new@example.com")
    
    # Verify update
    updated_bob = db.get_user_by_id(bob_db_id)
    print(f"Bob after update: {updated_bob.email}")
    
    # 8. Delete a user
    print("\nDeleting Charlie...")
    charlie_db_id = next(u.user_id for u in all_users if u.username == "charlie_brown")
    db.delete_user(charlie_db_id)
    
    # 9. Verify deletion
    final_users = db.get_all_users()
    print(f"\nFinal Users ({len(final_users)} total):")
    for u in final_users:
        print(f"  - {u.username}")

    print("\n--- Demonstration Complete ---")
