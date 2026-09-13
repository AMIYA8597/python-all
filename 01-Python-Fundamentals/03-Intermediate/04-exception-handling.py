"""
# ==============================================================================
# LABORATORY: EXCEPTION HANDLING & EAFP
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Unhandled exceptions crash programs. Poorly handled exceptions (e.g., bare 
# `except:`) hide bugs and make distributed ML or backend systems impossible 
# to debug. Mastering custom exception hierarchies and the full `try/except/else/finally`
# block is a hallmark of professional Python engineering.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Python's core philosophy: EAFP vs LBYL.
# - Master the full execution flow: try, except, else, finally.
# - Understand why catching bare `Exception` is dangerous.
# - Design Custom Exception hierarchies for large projects.
# - Use `raise ... from` for exception chaining.
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. EAFP VS LBYL
# ==============================================================================
def demonstrate_eafp():
    """
    LBYL: Look Before You Leap (C/Java style). Check everything before acting.
    EAFP: Easier to Ask Forgiveness than Permission (Python style). Just do it,
          and catch the exception if it fails. EAFP is often faster because 
          you avoid checking conditions on the "happy path".
    """
    section_header("EAFP vs LBYL")
    
    my_dict = {"a": 1, "b": 2}
    
    print("--- LBYL (Look Before You Leap) ---")
    if "c" in my_dict:
        print(my_dict["c"])
    else:
        print("Key 'c' not found!")
        
    print("\n--- EAFP (Easier to Ask Forgiveness) ---")
    try:
        # We just try it. If it succeeds, it's very fast.
        print(my_dict["c"])
    except KeyError:
        # If it fails, we handle it.
        print("Key 'c' not found (caught KeyError)!")


# ==============================================================================
# 4. FULL TRY / EXCEPT / ELSE / FINALLY
# ==============================================================================
def safe_divide(x: float, y: float) -> None:
    print(f"\nAttempting {x} / {y}")
    try:
        # 1. The dangerous code goes here.
        result = x / y
        
    except ZeroDivisionError as e:
        # 2. Runs ONLY if a ZeroDivisionError occurs.
        print(f"  [ERROR] Cannot divide by zero: {e}")
        
    except TypeError as e:
        # Multiple except blocks are allowed.
        print(f"  [ERROR] Invalid types: {e}")
        
    else:
        # 3. Runs ONLY if NO exceptions occurred in the try block!
        # This is where you put code that relies on the try block succeeding,
        # but which shouldn't catch exceptions itself.
        print(f"  [SUCCESS] Result is {result}")
        
    finally:
        # 4. Runs ALWAYS. Even if we hit a return or a crash.
        # Used for releasing resources (closing files, DB connections).
        print("  [CLEANUP] Closing resources...")

def demonstrate_full_flow():
    section_header("try / except / else / finally")
    safe_divide(10, 2)
    safe_divide(10, 0)
    safe_divide(10, "two") # type: ignore


# ==============================================================================
# 5. THE DANGER OF BARE EXCEPTIONS
# ==============================================================================
def demonstrate_bare_except():
    """
    Catching `except Exception:` catches EVERYTHING, including MemoryErrors, 
    assertion failures, and typos in your code.
    Catching a bare `except:` is even worse—it catches SystemExit and 
    KeyboardInterrupt, meaning you can't even CTRL+C to stop the program!
    """
    section_header("The Danger of Bare Exceptions")
    
    try:
        # A typo in the variable name
        my_var = 10
        print(my_vrr) # NameError
    except Exception as e:
        print("Caught an error, but it hid my typo!")
        print(f"The hidden error was: {e}")
        
    print("\nAlways catch SPECIFIC exceptions (e.g., ValueError, KeyError).")


# ==============================================================================
# 6. CUSTOM EXCEPTION HIERARCHIES
# ==============================================================================

# 1. Define a Base exception for your specific project/module
class DatabaseError(Exception):
    """Base class for all database-related errors in our app."""
    pass

# 2. Inherit from the base to create specific scenarios
class ConnectionTimeoutError(DatabaseError):
    def __init__(self, host: str, timeout: int):
        self.host = host
        self.timeout = timeout
        super().__init__(f"Connection to {host} timed out after {timeout}s.")

class InvalidQueryError(DatabaseError):
    pass

def connect_to_db():
    raise ConnectionTimeoutError("db.prod.internal", 30)

def demonstrate_custom_exceptions():
    section_header("Custom Exception Hierarchies")
    
    try:
        connect_to_db()
    except ConnectionTimeoutError as e:
        print(f"Caught specific timeout: {e}")
        print(f"Host that failed: {e.host}")
    except DatabaseError as e:
        print("Caught a generic database error.")


# ==============================================================================
# 7. EXCEPTION CHAINING (raise ... from)
# ==============================================================================
def demonstrate_chaining():
    """
    Sometimes you catch a low-level error (like KeyError) and want to raise a 
    high-level semantic error (like ConfigurationError).
    Using `raise NewError from old_error` preserves the original traceback!
    """
    section_header("Exception Chaining")
    
    config = {}
    print("If we run this code, we get a beautiful chained traceback:")
    print('''
    try:
        port = config["PORT"]
    except KeyError as e:
        raise ValueError("Missing 'PORT' in configuration!") from e
    ''')


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the `else` block do in exception handling?
   Answer: It executes only if the `try` block completes successfully without raising any exceptions.

2. What is EAFP?
   Answer: Easier to Ask Forgiveness than Permission. It is the Pythonic design pattern of attempting an operation (like reading a dict key) and catching the exception, rather than checking if it's safe beforehand (LBYL).

3. Why shouldn't you use `except:` or `except Exception:`?
   Answer: It swallows all errors indiscriminately. It hides bugs (like NameErrors from typos) and makes debugging impossible. Bare `except:` also blocks KeyboardInterrupt (CTRL+C).

4. How do you create a custom exception?
   Answer: Define a new class that inherits from Python's built-in `Exception` class.
"""

if __name__ == "__main__":
    demonstrate_eafp()
    demonstrate_full_flow()
    demonstrate_bare_except()
    demonstrate_custom_exceptions()
    demonstrate_chaining()
    print("\n[SUCCESS] Laboratory: Exception Handling Completed.")
