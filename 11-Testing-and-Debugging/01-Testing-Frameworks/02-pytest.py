"""
Pytest Framework - Educational Script

Learning Objectives:
1. Understand the advantages of pytest over unittest.
2. Learn how to write simple assertions using the standard `assert` statement.
3. Master pytest fixtures for setup and teardown.
4. Learn how to parameterize tests for multiple inputs.
5. Understand pytest markers for categorizing or skipping tests.

Concept Explanation:
`pytest` is a mature full-featured Python testing tool that helps you write better programs.
Unlike `unittest`, it doesn't require boilerplate code (like inheriting from TestCase).
It uses plain `assert` statements and provides detailed introspection on failure.

Key Features:
- Fixtures: Modular, scalable ways to manage test state and dependencies.
- Parameterization: Run the same test with different inputs.
- Markers: Categorize tests (e.g., slow, integration) or control execution (skip, xfail).
"""

import pytest
from typing import List, Dict, Set, Any
import time

# --- Basic Implementation: Simple Tests with Assertions ---

def reverse_string(s: str) -> str:
    """Reverses a given string."""
    return s[::-1]

def test_reverse_string() -> None:
    """Basic test using simple assert."""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"

def test_exception_handling() -> None:
    """Test that an exception is raised using pytest.raises."""
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0

# --- Intermediate Implementation: Fixtures ---

class Database:
    """A mock database connection."""
    def __init__(self) -> None:
        self.connected = False
        self.data: Dict[str, str] = {}
        
    def connect(self) -> None:
        self.connected = True
        
    def disconnect(self) -> None:
        self.connected = False
        
    def insert(self, key: str, value: str) -> None:
        if not self.connected:
            raise ConnectionError("Not connected")
        self.data[key] = value

# A pytest fixture
@pytest.fixture
def db_connection() -> Database:
    """Fixture that provides a connected database, and cleans up afterwards."""
    db = Database()
    db.connect()
    yield db # Execution pauses here, provides db to the test
    # Teardown happens after the test
    db.disconnect()

def test_database_insert(db_connection: Database) -> None:
    """Test using the database fixture."""
    assert db_connection.connected is True
    db_connection.insert("user1", "Alice")
    assert db_connection.data["user1"] == "Alice"

# --- Advanced Implementation: Parameterization and Markers ---

def is_palindrome(s: str) -> bool:
    """Checks if a string is a palindrome."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

@pytest.mark.parametrize("test_input,expected", [
    ("racecar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
])
def test_is_palindrome(test_input: str, expected: bool) -> None:
    """Test multiple inputs concisely."""
    assert is_palindrome(test_input) == expected

@pytest.mark.slow
def test_slow_operation() -> None:
    """A test marked as slow. Can be filtered out during test runs."""
    time.sleep(0.1) # Simulating slow operation
    assert True

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature() -> None:
    """A test that is intentionally skipped."""
    assert False

# --- Performance Analysis ---
# Pytest can be faster than unittest due to test collection mechanisms.
# Using `--numprocesses` (from pytest-xdist) allows parallel test execution.
# Fixture scope (function, class, module, session) is critical for performance;
# use module or session scope for expensive setups like DB connections.

# --- Edge Cases ---
# Using mutable default arguments in fixtures can lead to state leakage between tests.
# Assertions on floating point numbers should use `pytest.approx()`.

def test_float_comparison() -> None:
    """Demonstrate safe floating point comparison."""
    result = 0.1 + 0.2
    assert result == pytest.approx(0.3)

# --- Interview Challenge ---
# Challenge: Write a pytest fixture that captures standard output and tests a print function.
# (Hint: Pytest provides a built-in `capsys` fixture).

def greet(name: str) -> None:
    print(f"Hello, {name}!")

def test_greet(capsys: pytest.CaptureFixture[str]) -> None:
    greet("World")
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"

if __name__ == "__main__":
    # To run this script as a pytest test module directly:
    print("Run this file using: pytest 02-pytest.py -v")
    # For educational execution within the script:
    pytest.main([__file__, "-v"])
