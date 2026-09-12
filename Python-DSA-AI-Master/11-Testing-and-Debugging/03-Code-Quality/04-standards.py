"""
Module Docstring: Coding Standards and PEP 8

Learning Objectives:
1. Understand PEP 8 standards for Python code formatting.
2. Learn correct naming conventions (variables, functions, classes).
3. Apply standard type hinting.
4. Understand how code formatting impacts readability.

Concept Explanation:
PEP 8 is the Style Guide for Python Code. It provides conventions for writing 
clear, readable Python code. Adhering to standard formatting makes code easier 
to read and maintain, especially in collaborative environments.
"""

from typing import List, Optional, Callable
import unittest

# Basic Implementation: Proper vs Improper Naming and Formatting
# BAD STYLE (Do not do this)
def cAlc_Area(r):
  PI=3.14159
  return PI*(r**2)

# GOOD STYLE (PEP 8 Compliant)
PI: float = 3.14159

def calculate_area(radius: float) -> float:
    """
    Calculates the area of a circle given its radius.
    """
    return PI * (radius ** 2)

# Intermediate Implementation: Proper Class Structuring
class user_account: # Bad: Should be PascalCase
    pass

class UserAccount: # Good
    """
    Represents a user account in the system.
    """
    def __init__(self, username: str, email: str, is_active: bool = True) -> None:
        self.username = username
        self.email = email
        # Protected attribute starts with single underscore
        self._is_active = is_active
        # Private attribute starts with double underscore
        self.__password_hash = ""

    def activate_account(self) -> None:
        """Activates the user account."""
        self._is_active = True

    @property
    def is_active(self) -> bool:
        """Returns the active status of the account."""
        return self._is_active

# Advanced Implementation: Advanced Type Hinting Standards (PEP 484)
# Using generic types, callables, and optional types
def process_user_data(
    users: List[UserAccount], 
    filter_func: Optional[Callable[[UserAccount], bool]] = None
) -> List[str]:
    """
    Processes a list of user accounts and returns usernames based on a filter.
    
    Args:
        users: A list of UserAccount objects.
        filter_func: An optional function that takes a UserAccount and returns a bool.
        
    Returns:
        A list of active usernames or filtered usernames.
    """
    if filter_func is None:
        # Default filter: only active users
        filter_func = lambda user: user.is_active
        
    return [user.username for user in users if filter_func(user)]

# Performance Analysis
def performance_analysis() -> None:
    """
    Type hints and styling have NO runtime performance overhead.
    Python completely ignores type hints at runtime (except for evaluating annotations 
    and storing them in __annotations__). Code readability scales significantly with good style.
    """
    pass

# Edge Cases
# - Line length limit (PEP 8 suggests 79 characters, but modern tools like Black use 88).
# - Resolving type hints with circular imports using `from __future__ import annotations`.
# - Name clashing with Python built-ins (use trailing underscore e.g. `class_`).

# Interview Challenge
"""
Challenge: Correct the PEP 8 violations in the following snippet:
class myClass:
  def DoSomething(self,A,B):
    return A+B
"""
# Solution:
class MyClass:
    """A PEP 8 compliant class."""
    
    def do_something(self, a: int, b: int) -> int:
        """Adds two integers and returns the result."""
        return a + b

# Tests
class TestCodingStandards(unittest.TestCase):
    def test_calculate_area(self):
        self.assertAlmostEqual(calculate_area(2.0), 12.56636)
        
    def test_user_account(self):
        user = UserAccount("alice", "alice@example.com", False)
        self.assertFalse(user.is_active)
        user.activate_account()
        self.assertTrue(user.is_active)
        
    def test_process_user_data(self):
        users = [
            UserAccount("bob", "bob@example.com", True),
            UserAccount("eve", "eve@example.com", False)
        ]
        active_users = process_user_data(users)
        self.assertEqual(active_users, ["bob"])
        
    def test_my_class_solution(self):
        obj = MyClass()
        self.assertEqual(obj.do_something(3, 4), 7)

if __name__ == "__main__":
    print("Running tests...")
    unittest.main(exit=False)
    print("\nRunning performance analysis...")
    performance_analysis()
