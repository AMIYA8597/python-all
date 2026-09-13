"""
# ==============================================================================
# LABORATORY: CONTEXT MANAGERS AND RESOURCES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Managing external resources (file descriptors, database connections, locks) 
# is dangerous because an unhandled exception can bypass cleanup code. 
# Context managers (the `with` statement) guarantee cleanup by providing a 
# protocol that Python strictly enforces at the bytecode level.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the `__enter__` and `__exit__` dunder methods.
# - Build a class-based context manager for database connections.
# - Understand how `__exit__` intercepts exceptions.
# - Master `@contextmanager` and `yield` for functional context managers.
#
# ==============================================================================
"""

import time
from contextlib import contextmanager

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CLASS-BASED CONTEXT MANAGERS (__ENTER__ / __EXIT__)
# ==============================================================================

class DatabaseConnection:
    """
    A custom context manager simulating a database connection.
    Any object that implements __enter__ and __exit__ can be used with `with`.
    """
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connected = False

    def __enter__(self):
        """
        Executed IMMEDIATELY when the `with` block begins.
        The return value is assigned to the variable after the `as` keyword.
        """
        print(f"  [DB] Connecting to {self.db_url}...")
        self.connected = True
        return self  # Return the instance itself to be bound to `as db`

    def query(self, sql: str) -> str:
        if not self.connected:
            raise ConnectionError("Not connected!")
        print(f"  [DB] Executing: {sql}")
        return "Query Results"

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Executed ALWAYS when the block exits, whether normally or via exception.
        - exc_type: The exception class (e.g. ValueError)
        - exc_val: The exception instance
        - exc_tb: The traceback
        If no exception occurred, all three are None.
        """
        print("  [DB] Closing connection securely.")
        self.connected = False
        
        # If we return True here, it SWALLOWS the exception.
        # If we return False (or None), the exception propagates up.
        if exc_type is not None:
            print(f"  [DB ERROR INTERCEPTED] Exception occurred: {exc_val}")
            # We return True to swallow it for demonstration purposes.
            # Usually, you return False to let the app crash or handle it higher up.
            return True 
        return False

def demonstrate_class_cm():
    section_header("Class-Based Context Manager")
    
    print("--- 1. Normal Execution ---")
    with DatabaseConnection("postgresql://localhost") as db:
        db.query("SELECT * FROM users")
        
    print("\n--- 2. Exception Execution (Intercepted and Swallowed) ---")
    with DatabaseConnection("mysql://remote") as db:
        db.query("SELECT * FROM orders")
        # Simulate a crash
        raise ValueError("Something went terribly wrong in the business logic!")
        
    print("App continues running because the DB manager swallowed the error.")


# ==============================================================================
# 4. FUNCTIONAL CONTEXT MANAGERS (@contextmanager)
# ==============================================================================

@contextmanager
def timer(name: str):
    """
    The @contextmanager decorator allows you to write a context manager using 
    a generator function instead of a class.
    
    Everything BEFORE the `yield` acts as `__enter__`.
    Everything AFTER the `yield` acts as `__exit__`.
    """
    start = time.perf_counter()
    print(f"  [TIMER] Starting timer for '{name}'")
    
    try:
        # We yield control to the inner block of the 'with' statement
        # If we wanted to bind a variable (with timer() as t:), we would yield it here.
        yield 
    finally:
        # The finally block guarantees execution even if the inner block raises an error
        end = time.perf_counter()
        print(f"  [TIMER] '{name}' completed in {end - start:.4f}s")

def demonstrate_functional_cm():
    section_header("@contextmanager (Generator-based)")
    
    with timer("Complex Math"):
        # Simulate work
        time.sleep(0.5)
        _ = sum(i * i for i in range(10000))
        
    try:
        with timer("Failing Process"):
            time.sleep(0.2)
            raise RuntimeError("Crashed!")
    except RuntimeError:
        print("Caught the crash outside the context manager.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What methods must an object implement to be used in a `with` statement?
   Answer: It must implement the Context Manager protocol: `__enter__()` and `__exit__()`.

2. How do you return a value to the `as` variable in a `with` statement?
   Answer: You return the value from the `__enter__()` method.

3. What happens if you return `True` from the `__exit__` method?
   Answer: Python assumes the exception was handled internally and suppresses (swallows) it, allowing the program to continue executing the code after the `with` block.

4. How does `@contextmanager` work?
   Answer: It wraps a generator function. The code before the `yield` acts as `__enter__`, the `yield` itself passes control (and optionally a value) to the block, and the code after the `yield` (usually inside a `finally` block) acts as `__exit__`.
"""

if __name__ == "__main__":
    demonstrate_class_cm()
    demonstrate_functional_cm()
    print("\n[SUCCESS] Laboratory: Context Managers Completed.")
