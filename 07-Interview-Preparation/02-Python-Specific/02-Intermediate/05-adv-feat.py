"""
Module: Advanced Features

Learning Objectives:
1. Understand Context Managers and the `with` statement (`__enter__` and `__exit__`).
2. Learn about Metaclasses and how they control class creation.
3. Understand Descriptors and the descriptor protocol (`__get__`, `__set__`, `__delete__`).
4. Learn how these features are used in popular libraries (e.g., ORMs, web frameworks).

Interview Questions Covered:
- How do you create a custom context manager?
- What is a metaclass and when would you use one?
- How do properties work under the hood in Python (Descriptors)?
"""

import time
from typing import Any, Type

# ---------------------------------------------------------
# Concept 1: Context Managers
# ---------------------------------------------------------
class TimerContextManager:
    """A context manager to measure the execution time of a block of code."""
    def __enter__(self) -> 'TimerContextManager':
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        self.end_time = time.time()
        print(f"Block executed in {self.end_time - self.start_time:.4f} seconds.")
        # Return False to propagate exceptions, True to suppress them
        return False

# ---------------------------------------------------------
# Concept 2: Descriptors
# ---------------------------------------------------------
class ValidatedString:
    """A descriptor that ensures an attribute is always a string and not empty."""
    def __init__(self, min_length: int = 1):
        self.min_length = min_length
        self.name = ""
        
    def __set_name__(self, owner: Type, name: str):
        self.name = name
        
    def __get__(self, instance: Any, owner: Type) -> str:
        if instance is None:
            return self
        return instance.__dict__.get(self.name, "")
        
    def __set__(self, instance: Any, value: Any):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be a string.")
        if len(value) < self.min_length:
            raise ValueError(f"{self.name} must be at least {self.min_length} characters long.")
        instance.__dict__[self.name] = value

class UserProfile:
    # Using the descriptor
    username = ValidatedString(min_length=3)
    
    def __init__(self, username: str):
        self.username = username

# ---------------------------------------------------------
# Tests and Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- Context Manager Example ---")
    with TimerContextManager():
        # Simulate some work
        time.sleep(0.3)
        print("Work completed inside context manager.")
        
    print("\n--- Descriptor Example ---")
    try:
        user1 = UserProfile("alice")
        print(f"Created user with username: {user1.username}")
        
        # This will raise a ValueError
        user2 = UserProfile("bo")
    except ValueError as e:
        print(f"Validation Error: {e}")
