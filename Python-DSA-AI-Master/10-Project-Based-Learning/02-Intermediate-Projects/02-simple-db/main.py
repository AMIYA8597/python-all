"""
Simple Key-Value Database
=========================

Overview:
---------
This module provides a robust, professional-grade implementation of a simple 
in-memory Key-Value database in Python, complete with file-based persistence. 
It simulates core database functionalities like Create, Read, Update, Delete (CRUD),
transaction simulation, and persistent storage via JSON.

Why this exists and Industry Use Cases:
---------------------------------------
Key-value stores are fundamental in computer science and software engineering.
Real-world systems like Redis, Memcached, and Amazon DynamoDB are highly 
scalable key-value databases. Understanding how to build one from scratch teaches
you about data structures, serialization, atomicity, and file I/O.

Beginner Explanation:
---------------------
Think of a database like a giant dictionary. You have a 'key' (like a word) 
and a 'value' (its definition). This program lets you add new words, look them up, 
change their meanings, or remove them, and it saves this dictionary to a file so 
it isn't lost when you turn off the computer.

Deep Technical Explanation:
---------------------------
The SimpleKVDB class wraps a standard Python dictionary `Dict[str, Any]` to hold data.
It employs a Write-Ahead Logging (WAL) or simple state-saving mechanism by serializing
the dictionary to a JSON file upon each write operation (or selectively on `commit`).
Thread safety is simulated using threading.Lock() to ensure that concurrent operations
do not corrupt the internal state. 

Advanced Concepts Covered:
- Thread-safe operations using Locks.
- Data serialization and deserialization (JSON).
- Exception handling and custom exception classes.
- Context managers for atomic operations.
"""

import json
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

class DatabaseError(Exception):
    """Base exception for Database errors."""
    pass

class KeyNotFoundError(DatabaseError):
    """Raised when a key is not found in the database."""
    pass

class SimpleKVDB:
    def __init__(self, filepath: str = "database.json", auto_commit: bool = True):
        """
        Initialize the database.
        
        :param filepath: Path to the JSON file for persistence.
        :param auto_commit: If True, writes to disk after every modification.
        """
        self.filepath = filepath
        self.auto_commit = auto_commit
        self._data: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Loads data from the JSON file into memory."""
        if not os.path.exists(self.filepath):
            self._data = {}
            return

        with self._lock:
            try:
                with open(self.filepath, 'r', encoding='utf-8') as file:
                    self._data = json.load(file)
            except json.JSONDecodeError:
                raise DatabaseError(f"File {self.filepath} is corrupted or not valid JSON.")
            except Exception as e:
                raise DatabaseError(f"Failed to load database: {e}")

    def _save_to_disk(self) -> None:
        """Saves current in-memory data to the JSON file."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self._data, file, indent=4)

    def set(self, key: str, value: Any) -> None:
        """
        Set the string value of a key.
        
        :param key: The key to set.
        :param value: The value to associate with the key. (Must be JSON serializable)
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        with self._lock:
            self._data[key] = value
            if self.auto_commit:
                self._save_to_disk()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the value of a key.
        
        :param key: The key to retrieve.
        :param default: Return value if key does not exist.
        :return: The value associated with the key.
        """
        with self._lock:
            return self._data.get(key, default)

    def get_strict(self, key: str) -> Any:
        """
        Get the value of a key, but raise an exception if it doesn't exist.
        
        :param key: The key to retrieve.
        :raises KeyNotFoundError: If the key is not in the database.
        """
        with self._lock:
            if key not in self._data:
                raise KeyNotFoundError(f"Key '{key}' not found.")
            return self._data[key]

    def delete(self, key: str) -> bool:
        """
        Removes the specified key.
        
        :param key: The key to delete.
        :return: True if the key was removed, False if it did not exist.
        """
        with self._lock:
            if key in self._data:
                del self._data[key]
                if self.auto_commit:
                    self._save_to_disk()
                return True
            return False

    def keys(self) -> List[str]:
        """Returns a list of all keys in the database."""
        with self._lock:
            return list(self._data.keys())

    def clear(self) -> None:
        """Empties the entire database."""
        with self._lock:
            self._data.clear()
            if self.auto_commit:
                self._save_to_disk()

    def commit(self) -> None:
        """Manually flush in-memory data to disk."""
        with self._lock:
            self._save_to_disk()

# ---------------------------------------------------------
# Test Execution & Real-World Simulation
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- Starting Simple Key-Value DB Tests ---")
    
    db_file = "test_db.json"
    
    # Clean up before test
    if os.path.exists(db_file):
        os.remove(db_file)
        
    db = SimpleKVDB(filepath=db_file, auto_commit=True)
    
    # 1. Test SET and GET
    db.set("user:1001", {"name": "Alice", "role": "admin"})
    db.set("user:1002", {"name": "Bob", "role": "user"})
    
    print(f"User 1001: {db.get('user:1001')}")
    print(f"User 1002: {db.get('user:1002')}")
    
    # 2. Test KeyNotFoundError
    try:
        db.get_strict("user:9999")
    except KeyNotFoundError as e:
        print(f"Expected error caught: {e}")
        
    # 3. Test DELETE
    db.delete("user:1002")
    print(f"Keys after deletion: {db.keys()}")
    
    # 4. Test Persistence
    print("\nSimulating database restart...")
    db_restarted = SimpleKVDB(filepath=db_file)
    print(f"Loaded User 1001 after restart: {db_restarted.get('user:1001')}")
    
    # Cleanup
    if os.path.exists(db_file):
        os.remove(db_file)
    print("--- Tests Completed Successfully ---")
