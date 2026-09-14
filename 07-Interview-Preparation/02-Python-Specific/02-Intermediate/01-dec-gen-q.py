"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - DECORATORS & GENERATORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Write a `@retry` decorator that automatically retries a failed 
# database query 3 times before finally crashing."
#
# If you don't understand that a Decorator is just a High-Order Function that 
# returns a Closure, you will fail. If you forget to use `@functools.wraps`, 
# you will destroy the original function's metadata and break the logging system.
#
# Interviewer: "I have a 50 GB log file. I need to parse it line by line. Write 
# the code."
# If you write `lines = file.readlines()`, you instantly fail the interview 
# with an Out-Of-Memory (OOM) error. You MUST understand that `file` is a 
# Generator that mathematically yields one line at a time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the anatomy of a Decorator (Closures).
# - Master `@functools.wraps` (Metadata preservation).
# - Understand Generators as mathematically paused State Machines.
#
# ==============================================================================
"""

import time
import functools

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DECORATORS (CLOSURES UNDER THE HOOD)
# ==============================================================================
def retry_decorator(max_retries: int):
    """
    A Decorator with Arguments!
    This requires a 3-level deep nested closure.
    1. Outer: Receives the decorator arguments (max_retries).
    2. Middle: Receives the actual function being decorated.
    3. Inner: The physical wrapper that executes when the function is called.
    """
    def decorator(func):
        # CRITICAL: Preserves the __name__ and __doc__ of the original function!
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    print(f"  [Attempt {attempts + 1}] Executing {func.__name__}...")
                    # We execute the actual function!
                    result = func(*args, **kwargs)
                    print(f"  [SUCCESS] {func.__name__} succeeded!")
                    return result
                except Exception as e:
                    attempts += 1
                    print(f"  [FAILED] Error: {e}. Retrying...")
                    time.sleep(0.1) # Backoff
            
            # If we break the while loop, we exhausted all retries!
            print("  [FATAL] All retries exhausted. Crashing.")
            raise Exception("Max retries exceeded.")
            
        return wrapper
    return decorator

# Applying the decorator!
@retry_decorator(max_retries=3)
def unstable_database_query(fail_count: int):
    """Simulates a database that fails a specific number of times before succeeding."""
    # We cheat by using an attribute on the function object to track state for the demo
    if not hasattr(unstable_database_query, "current_fails"):
        unstable_database_query.current_fails = 0
        
    if unstable_database_query.current_fails < fail_count:
        unstable_database_query.current_fails += 1
        raise ConnectionError("Database timed out!")
        
    return "DB_DATA_123"

def demonstrate_decorators():
    section_header("Decorators & Closures")
    
    print("Testing a function that fails 2 times, then succeeds on the 3rd attempt.")
    print("The `@retry(max_retries=3)` decorator should catch and handle it automatically!")
    
    # Reset state
    unstable_database_query.current_fails = 0
    result = unstable_database_query(fail_count=2)
    print(f"\nFinal Result: {result}")
    
    print(f"\nFunction Metadata preserved by @functools.wraps:")
    print(f"__name__: {unstable_database_query.__name__}")
    print(f"__doc__: {unstable_database_query.__doc__.strip()}")


# ==============================================================================
# 4. GENERATORS (STATE MACHINES)
# ==============================================================================
def infinite_fibonacci_generator():
    """
    A Generator. It does NOT return an array. 
    It yields ONE number, and physically FREEZES its execution state in RAM.
    When called again, it THAWS and resumes from the exact line after the yield.
    """
    a, b = 0, 1
    while True: # Infinite loop! If this was a List, it would crash instantly.
        yield a
        a, b = b, a + b

def demonstrate_generators():
    section_header("Generators (Paused State Machines)")
    
    print("Creating an INFINITE sequence of Fibonacci numbers...")
    fib_gen = infinite_fibonacci_generator()
    
    print(f"Generator Object: {fib_gen}")
    print("Notice it did NOT execute the function. It created a State Machine.\n")
    
    print("Extracting exactly 7 numbers from the infinite sequence:")
    for _ in range(7):
        # `next()` mathematically commands the generator to unfreeze, calculate ONE 
        # number, yield it, and instantly freeze again.
        print(f"  Yielded: {next(fib_gen)}")
        
    print("\nThe Generator is perfectly paused, consuming O(1) memory.")
    print("We can resume it whenever we want!")
    print(f"  Yielded: {next(fib_gen)}")


def run_all_labs():
    demonstrate_decorators()
    demonstrate_generators()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Without using the `@` syntactic sugar, how do you mathematically apply a Decorator to a function?"
   Senior Answer: "The `@` symbol is just syntactic sugar. A Decorator is fundamentally a High-Order Function that accepts a function as an argument and returns a new wrapper function. If I have `def my_decorator(func): ...`, and I want to decorate `def original_func(): ...`, the mathematical equivalent under the hood is: `original_func = my_decorator(original_func)`. I am physically overwriting the variable name `original_func` with the new Closure returned by the decorator."

2. Interviewer: "Why MUST you use `@functools.wraps(func)` when writing a custom decorator?"
   Senior Answer: "When you return the `wrapper` function from a decorator, you are physically replacing the original function with the wrapper. The `wrapper` function has its own `__name__` (which is literally the string 'wrapper') and its own `__doc__` string. If you don't use `@wraps`, any code that tries to print the function's name (like a Logging system or a metric tracer) will print 'wrapper' instead of 'calculate_taxes'. You completely blind the debugging system. `@functools.wraps` physically copies the `__name__`, `__doc__`, and `__module__` from the original function and glues it onto the wrapper, flawlessly preserving introspection."

3. Interviewer: "How does the `yield` keyword convert a standard function into a Generator State Machine?"
   Senior Answer: "When the Python Compiler reads a function and detects the physical word `yield` anywhere inside it, it violently alters the compilation of that function. It no longer compiles it as a standard subroutine that pushes a frame onto the C stack. Instead, it compiles it as a Generator Object. When the function is called, it does NOT execute the code; it instantly returns the Generator Object. This object contains the exact state of all local variables and an Instruction Pointer. When you call `next()`, it executes until it hits `yield`, hands you the value, and suspends the Instruction Pointer. It mathematically trades CPU stack execution for explicit Heap-based state tracking, allowing it to pause and resume infinitely."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Decorators & Generators) Completed.")
