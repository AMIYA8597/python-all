"""
## A. Concept Name
Exception Handling

## B. One-Sentence Definition
Exception handling is a mechanism to gracefully intercept, manage, and recover from runtime errors that would otherwise crash a program.

## C. Why Does This Exist?
Software interacts with unpredictable environments (networks, file systems, users). Exception handling exists so that when these inevitable failures occur, the program can fail safely, log the issue, and optionally recover, rather than abruptly terminating.

## D. Intuition
Imagine you are driving a car and get a flat tire. Instead of the car exploding (a crash), you have a spare tire and a process to fix it (exception handling). You pull over (catch the error), change the tire (handle it), and resume driving.

## E. Real-Life Analogy
A restaurant kitchen. The chef (program) tries to cook a dish. If they run out of salt (error), they don't burn down the kitchen (crash). Instead, they ask a waiter to buy more salt (catch and recover), or inform the customer (graceful failure).

## F. Mental Model
Think of exception handling as a safety net placed under a tightrope walker. The walker (code) walks normally (try block). If they slip (raise exception), the net catches them (except block), and someone checks if they are okay (finally block).

## G. Visual Explanation
Normal Flow: Code -> Code -> Code
Error Flow: Code -> Exception Thrown -> Exception Caught -> Fallback Code -> Continue

## H. Formal Explanation
In Python, exception handling utilizes try, except, else, and finally blocks. Code that might raise an exception goes in the try block. Handlers for specific exception types go in except blocks. The else block executes if no exceptions were raised. The finally block executes invariably, making it ideal for resource cleanup.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
N/A (Built into the language).

## K. Library / Production Implementation (if applicable)
Standard library modules heavily use exceptions (e.g., `json.loads` raises `json.JSONDecodeError`, HTTP libraries raise `requests.exceptions.ConnectionError`). Context managers (`with` statements) often encapsulate exception handling for resource acquisition and release.

## L. Trace (walk through example)
1. Enter `try` block: `result = 10 / 0`
2. `ZeroDivisionError` is raised.
3. Python looks for a matching `except ZeroDivisionError`.
4. It finds it, executes the `except` block.
5. The `else` block is skipped.
6. The `finally` block executes.

## M. Complexity
Time Complexity: Virtually free (O(1)) if no exception is raised. If raised, there is a small overhead for stack unwinding.
Space Complexity: O(1) overhead.

## N. Common Mistakes
- Catching broad `Exception` or bare `except:` which masks bugs (like syntax errors or keyboard interrupts).
- Putting too much code inside a single `try` block.
- Forgetting to clean up resources (use `finally` or context managers).

## O. Common Confusions
- `except Exception:` vs bare `except:`: The former catches all standard runtime errors. The latter also catches `SystemExit` and `KeyboardInterrupt`, making it impossible to terminate the program safely.
- `else` block: It runs only if the `try` block finishes without raising an exception, and before the `finally` block.

## P. When To Use
- When dealing with I/O (files, network, databases).
- When parsing user input.
- Implementing "Easier to Ask for Forgiveness than Permission" (EAFP) design patterns.

## Q. When NOT To Use
- For normal control flow (like loops).
- To ignore all errors (`except: pass`).

## R. Trade-offs
EAFP vs LBYL ("Look Before You Leap"): EAFP is generally faster in Python when exceptions are rare, but slower when they are frequent due to the overhead of stack unwinding.

## S. Debugging
- Read the traceback from bottom (where error occurred) to top (where it originated).
- Use exception chaining (`raise ... from ...`) to keep track of the original cause of an error.

## T. Memory Hook (a short memorable principle)
Try, Catch, Else, Finally: Try it, Catch it if it breaks, Else celebrate, Finally clean up.

## U. Active Recall (questions before answers)
1. What does the `else` block do in a try-except structure?
2. Why is catching bare `except:` dangerous?
3. How do you preserve the original exception when raising a new one?

## V. Practice (exercises)
1. Write a function that reads a file and safely handles `FileNotFoundError` and `PermissionError`.
2. Create a custom exception class `InsufficientFundsError` for a bank account simulation.

## W. Interview Question
What is the difference between EAFP and LBYL in Python, and which is more "Pythonic"? Give an example.

## X. Project Connection
Exception handling is crucial in any robust application. In a web server, handling exceptions prevents the entire server from crashing when a single request fails, allowing it to return a 500 error and continue serving other users.
"""

import sys
from typing import Any, Optional


# Basic Implementation: Try/Except/Else/Finally
def safe_divide(a: float, b: float) -> Optional[float]:
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return None
    except TypeError as e:
        print(f"Error: Invalid types for division - {e}")
        return None
    else:
        print("Division successful.")
        return result
    finally:
        print("Execution of safe_divide completed.")


# Intermediate Implementation: Custom Exceptions
class CustomValidationError(Exception):
    """Raised when data fails a custom validation check."""
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code

def validate_age(age: int) -> None:
    if age < 0:
        raise CustomValidationError("Age cannot be negative.", code=400)
    if age > 150:
        raise CustomValidationError("Age is suspiciously high.", code=401)
    print(f"Age {age} is valid.")


# Advanced Implementation: Exception Chaining and Context Managers
class DatabaseConnectionError(Exception):
    pass

def connect_to_database() -> None:
    try:
        # Simulate network error
        raise ConnectionError("Network unreachable")
    except ConnectionError as e:
        # Exception chaining: keeping track of the root cause
        raise DatabaseConnectionError("Failed to connect to DB") from e

class ManagedFile:
    """A custom context manager for file handling."""
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        print(f"Opening file {self.filename}")
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            print(f"Closing file {self.filename}")
            self.file.close()
        if exc_type is not None:
            print(f"Exception occurred: {exc_type}, {exc_val}")
        return True # Suppress the exception


# Performance Analysis
def analyze_performance() -> None:
    print("--- Performance Analysis ---")
    import timeit
    
    # Try/except is virtually free if no exception is raised
    # "Look Before You Leap" (LBYL) vs "Easier to Ask for Forgiveness than Permission" (EAFP)
    
    setup = "d = {'key': 'value'}"
    lbyl = "if 'key' in d: val = d['key']"
    eafp = "try:\n    val = d['key']\nexcept KeyError:\n    pass"
    
    t_lbyl = timeit.timeit(lbyl, setup=setup, number=1000000)
    t_eafp = timeit.timeit(eafp, setup=setup, number=1000000)
    
    print(f"LBYL time: {t_lbyl:.4f}s")
    print(f"EAFP time: {t_eafp:.4f}s")
    print("EAFP is often faster when the happy path is common.")

# Edge Cases
def handle_edge_cases() -> None:
    print("\n--- Edge Cases ---")
    try:
        try:
            1 / 0
        finally:
            print("Finally block executes even if we re-raise implicitly!")
    except ZeroDivisionError:
        print("Caught the division by zero from inner try.")

# Interview Challenge
"""
Challenge: Write a retry context manager that retries a block of code if a specific exception is raised.
"""
from contextlib import contextmanager

@contextmanager
def retry_block(exceptions: tuple, retries: int = 3):
    class RetryControl:
        def __init__(self):
            self.attempts = 0
            self.success = False

    control = RetryControl()
    while control.attempts < retries and not control.success:
        try:
            yield control
            control.success = True
        except exceptions as e:
            control.attempts += 1
            if control.attempts >= retries:
                raise e
            print(f"Retry {control.attempts}/{retries} after catching {type(e).__name__}")


# Tests
def run_tests() -> None:
    # Test safe_divide
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) is None
    
    # Test custom exception
    try:
        validate_age(-5)
    except CustomValidationError as e:
        assert e.code == 400
        
    # Test exception chaining
    try:
        connect_to_database()
    except DatabaseConnectionError as e:
        assert isinstance(e.__cause__, ConnectionError)
        
    # Test Context Manager
    with ManagedFile('test.txt') as f:
        f.write('hello')
        raise ValueError("Simulated error") # Should be suppressed
        
    import os
    if os.path.exists('test.txt'):
        os.remove('test.txt')
    
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Running Exception Handling Examples ---")
    analyze_performance()
    handle_edge_cases()
    run_tests()
