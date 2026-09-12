"""
## A. Concept Name
Context Managers

## B. One-Sentence Definition
A context manager is a Python object that defines a temporary runtime context for a block of code, automatically handling setup and teardown operations.

## C. Why Does This Exist?
To guarantee the clean-up of resources (like files, network connections, and locks) even if an exception occurs during execution, eliminating repetitive `try...finally` boilerplate.

## D. Intuition
Imagine renting a car. You pick it up (setup), drive it (execution), and return it (teardown). The context manager ensures the car is returned no matter what happened during the drive.

## E. Real-Life Analogy
Entering a secure building. 
Setup: Swiping your ID card to unlock the door. 
Execution: Doing your work inside. 
Teardown: The door automatically locking behind you when you leave. You don't have to manually lock it.

## F. Mental Model
Think of the `with` statement as a sandwich. 
- Top bread: `__enter__()` (Resource Acquisition)
- Meat: The block of code inside the `with` statement.
- Bottom bread: `__exit__()` (Resource Release)

## G. Visual Explanation
```python
with context_manager() as cm:
    # 1. __enter__() is called.
    # 2. Return value of __enter__() is assigned to `cm`.
    do_something(cm) 
    # 3. Code block executes.
# 4. __exit__() is guaranteed to be called, regardless of exceptions.
```

## H. Formal Explanation
A context manager is an object that implements the context management protocol, consisting of two methods: `__enter__(self)` and `__exit__(self, exc_type, exc_value, traceback)`. When a `with` statement is evaluated, `__enter__` is called. Its return value is bound to the target(s) specified in the `as` clause. When the block inside the `with` statement completes (normally or via exception), `__exit__` is invoked. If an exception occurred, `__exit__` can suppress it by returning `True`.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
See the `Timer` class implementation below for a from-scratch class-based context manager.

## K. Library / Production Implementation (if applicable)
Python's built-in `open()` function is the most common example. The `contextlib` module provides utilities like `@contextmanager` to create context managers from generator functions, and `contextlib.suppress` (similar to our interview question below).

## L. Trace (walk through example)
For the `Timer` context manager:
1. `with Timer() as t:` is encountered.
2. `Timer.__init__()` initializes state.
3. `Timer.__enter__()` records `start_time` and returns `self`.
4. The block of code runs (e.g., `time.sleep(1)`).
5. The block exits. `Timer.__exit__()` is called.
6. `Timer.__exit__()` calculates duration, prints it, and returns `True` or `False` depending on if exceptions should be suppressed.

## M. Complexity
- Time Complexity: O(1) overhead for entering and exiting the context.
- Space Complexity: O(1) overhead. The context manager holds references to the resource and exception info, but doesn't inherently allocate significant space.

## N. Common Mistakes
- Exception Swallowing: Returning `True` from `__exit__` unintentionally, suppressing errors that should propagate.
- Generator Yield: Forgetting to yield exactly once in a `@contextmanager` decorated function.
- Generator Cleanup: Forgetting the `try...finally` block in a generator context manager, which causes resource leaks if an exception is raised at the `yield`.

## O. Common Confusions
- `__enter__` vs `__init__`: `__init__` creates the object, `__enter__` acquires the resource for the `with` block. They serve different lifecycle phases.
- The `as` keyword: The variable after `as` receives what `__enter__` returns, NOT the context manager object itself (unless `__enter__` returns `self`).

## P. When To Use
- File I/O operations.
- Acquiring and releasing locks in multithreading.
- Opening and closing database connections.
- Temporarily patching/mocking objects in tests.
- Measuring execution time of a specific block.

## Q. When NOT To Use
- For logic that doesn't require setup and teardown.
- When the resource needs to remain open indefinitely across multiple disparate scopes.

## R. Trade-offs
- Slight microsecond overhead due to function calls (`__enter__`/`__exit__`).
- Highly readable and safe, eliminating manual cleanup bugs.

## S. Debugging
- Use print statements in `__enter__` and `__exit__` to ensure they are being hit.
- Inspect the `exc_type`, `exc_value`, and `traceback` arguments in `__exit__` to understand what exception occurred inside the block.

## T. Memory Hook
"Enter, Execute, Exit (even if Error)" - The 4 E's of Context Managers.

## U. Active Recall
1. What two magic methods define the context management protocol?
2. What does returning `True` from `__exit__` do?
3. In a `@contextmanager` generator, what ensures cleanup if an error happens?

## V. Practice
Write a context manager `WorkingDir(path)` that temporarily changes the current working directory, and switches back to the original directory when exiting.

## W. Interview Question
Create a context manager `Suppress` that suppresses specified exceptions but lets others propagate (Implemented below).

## X. Project Connection
Used heavily in database connection pools to ensure connections are returned to the pool after a request is handled.
"""

import time
import os
from contextlib import contextmanager
from typing import Any, Generator, Optional, Type


# --- Basic Implementation: Built-in Context Manager ---
def read_file_basic(filepath: str) -> str:
    """Uses the built-in open() context manager."""
    # Create a dummy file for testing
    with open(filepath, 'w') as f:
        f.write("Hello Context Manager!")
    
    # Read using context manager
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Cleanup dummy file
    os.remove(filepath)
    return content


# --- Intermediate Implementation: Class-based Context Manager ---
class Timer:
    """A context manager that measures the execution time of a block of code."""
    def __init__(self, description: str = "Execution") -> None:
        self.description = description
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def __enter__(self) -> 'Timer':
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], 
                 exc_value: Optional[BaseException], 
                 traceback: Optional[Any]) -> bool:
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"{self.description} took {duration:.4f} seconds")
        
        # If an exception occurred, we can swallow it by returning True
        # Returning False (or None) propagates the exception.
        if exc_type is not None:
            print(f"An exception of type {exc_type.__name__} occurred: {exc_value}")
            return False  # Propagate exception
        return True


# --- Advanced Implementation: Generator-based Context Manager ---
@contextmanager
def temporary_environment_variable(key: str, value: str) -> Generator[None, None, None]:
    """
    A context manager to temporarily set an environment variable.
    Restores the original value (or unsets it) when exiting.
    """
    original_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if original_value is None:
            del os.environ[key]
        else:
            os.environ[key] = original_value


# --- Interview Challenge ---
class Suppress:
    """Context manager to suppress specified exceptions."""
    def __init__(self, *exceptions: Type[BaseException]) -> None:
        self.exceptions = exceptions

    def __enter__(self) -> None:
        pass

    def __exit__(self, exc_type: Optional[Type[BaseException]], 
                 exc_value: Optional[BaseException], 
                 traceback: Optional[Any]) -> bool:
        # Return True if the exception type is a subclass of any of the specified exceptions
        return exc_type is not None and issubclass(exc_type, self.exceptions)


# --- Tests ---
def run_tests() -> None:
    print("Testing Context Managers...")

    # Test basic file read
    test_file = "test_file_cm.txt"
    content = read_file_basic(test_file)
    assert content == "Hello Context Manager!"

    # Test Timer
    with Timer("Sleep Test"):
        time.sleep(0.01)

    # Test Generator Context Manager
    assert "TEST_ENV_VAR" not in os.environ
    with temporary_environment_variable("TEST_ENV_VAR", "my_value"):
        assert os.environ["TEST_ENV_VAR"] == "my_value"
    assert "TEST_ENV_VAR" not in os.environ

    # Test Suppress Context Manager
    with Suppress(ValueError):
        raise ValueError("This should be suppressed")
    
    try:
        with Suppress(ValueError):
            raise TypeError("This should NOT be suppressed")
        assert False, "TypeError should have propagated"
    except TypeError:
        pass

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
