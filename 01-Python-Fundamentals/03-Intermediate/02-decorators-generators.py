"""
# ==============================================================================
# LABORATORY: DECORATORS AND GENERATORS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Decorators allow you to cleanly modify the behavior of functions (e.g., adding 
# logging, authentication, or retry logic in MLOps pipelines).
# Generators allow you to process massive datasets (e.g., terabytes of CSV data 
# or token streams in LLMs) without running out of RAM by yielding one item at a time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the functional mechanics of a Decorator.
# - Master `@functools.wraps` to preserve function metadata.
# - Write decorators that accept arguments.
# - Master the `yield` keyword and the Generator protocol.
# - Compare memory usage between lists and generators.
# - Understand advanced generators (send, throw).
#
# ==============================================================================
"""

import sys
import time
from functools import wraps
from typing import Callable, Any, Generator

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DECORATORS: THE FUNDAMENTALS
# ==============================================================================

def my_timer(func: Callable) -> Callable:
    """
    A decorator is simply a function that takes another function, 
    wraps it in an inner function, and returns the inner function.
    """
    # @wraps preserves the original function's name and docstring.
    # Without it, wrapped_function.__name__ would be "wrapper".
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        
        # Execute the actual function
        result = func(*args, **kwargs)
        
        end = time.perf_counter()
        print(f"  [TIMER] {func.__name__} took {end - start:.6f} seconds.")
        return result
        
    return wrapper

@my_timer
def slow_function(delay: float) -> str:
    """This function simulates a slow API call."""
    time.sleep(delay)
    return "Data Fetched!"

def demonstrate_decorators():
    """
    Syntactic Sugar:
    @my_timer
    def slow_function(): ...
    
    Is identical to:
    slow_function = my_timer(slow_function)
    """
    section_header("Decorators and @wraps")
    
    print(f"Function Name: {slow_function.__name__}")
    print(f"Function Doc:  {slow_function.__doc__}")
    
    # Call the decorated function
    result = slow_function(0.2)
    print(f"Result: {result}")


# ==============================================================================
# 4. DECORATORS WITH ARGUMENTS
# ==============================================================================

def retry(max_attempts: int):
    """
    To pass arguments to a decorator, you need THREE layers of functions.
    Layer 1: Accepts the decorator arguments.
    Layer 2: Accepts the function being decorated.
    Layer 3: The actual wrapper.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"  [RETRY] Attempt {attempts}/{max_attempts} failed: {e}")
            raise RuntimeError("Max retries exceeded.")
        return wrapper
    return decorator

fail_count = 0

@retry(max_attempts=3)
def unstable_network_call():
    global fail_count
    fail_count += 1
    if fail_count < 3:
        raise ConnectionError("Network timeout.")
    return "Success!"

def demonstrate_advanced_decorators():
    section_header("Decorators with Arguments")
    print("Calling unstable function (configured for 3 max retries)...")
    res = unstable_network_call()
    print(f"Final Result: {res}")


# ==============================================================================
# 5. GENERATORS: THE YIELD KEYWORD
# ==============================================================================

def infinite_sequence() -> Generator[int, None, None]:
    """
    The `yield` keyword turns a function into a Generator.
    When Python sees `yield`, it pauses execution, saves the local variables, 
    returns the value, and waits for the next `next()` call.
    """
    num = 0
    while True:
        yield num
        num += 1

def demonstrate_generators():
    section_header("Generators & Yield")
    
    gen = infinite_sequence()
    
    print(f"Generator type: {type(gen)}")
    
    print(f"1st call: {next(gen)}")
    print(f"2nd call: {next(gen)}")
    print(f"3rd call: {next(gen)}")
    
    # We can also use it in a for loop (but we must break since it's infinite!)
    for val in gen:
        print(f"Loop call: {val}")
        if val >= 5:
            break


# ==============================================================================
# 6. MEMORY OPTIMIZATION: GENERATORS VS LISTS
# ==============================================================================

def demonstrate_generator_memory():
    """
    Generators compute values lazily (on the fly). 
    Lists compute all values upfront and store them in RAM.
    """
    section_header("Memory: Generators vs Lists")
    
    # Generate 1 million numbers
    # A list comprehension allocates RAM for all 1 million items
    list_comp = [x ** 2 for x in range(1_000_000)]
    
    # A generator expression (using parentheses) allocates almost NO RAM
    gen_comp = (x ** 2 for x in range(1_000_000))
    
    print(f"RAM used by List:      {sys.getsizeof(list_comp):>10} bytes")
    print(f"RAM used by Generator: {sys.getsizeof(gen_comp):>10} bytes")


# ==============================================================================
# 7. ADVANCED GENERATORS: STATE MACHINES (SEND)
# ==============================================================================

def accumulator() -> Generator[int, int, None]:
    """
    Generators can also RECEIVE data using the `send()` method.
    This makes them primitive coroutines (the foundation of async/await).
    """
    total = 0
    while True:
        # 1. We yield the current total.
        # 2. We PAUSE.
        # 3. When the user calls gen.send(value), it resumes and assigns value to `received`.
        received = yield total
        
        if received is None:
            break
            
        total += received

def demonstrate_coroutines():
    section_header("Advanced Generators: send()")
    
    acc = accumulator()
    
    # We MUST call next() first to prime the generator (execute up to the first yield)
    print(f"Primed total: {next(acc)}")
    
    print(f"Sent 10. New total: {acc.send(10)}")
    print(f"Sent 20. New total: {acc.send(20)}")
    print(f"Sent 5.  New total: {acc.send(5)}")
    
    acc.close() # Safely terminates the generator


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the `@wraps(func)` decorator do?
   Answer: It copies the metadata (`__name__`, `__doc__`, etc.) from the original function to the wrapper function. Without it, debugging becomes difficult because all wrapped functions will be named "wrapper".

2. Why do decorators with arguments require three nested functions?
   Answer: The outermost function receives the decorator arguments. It must return a decorator function. That middle function receives the target function and returns the innermost wrapper function.

3. Explain the difference between `return` and `yield`.
   Answer: `return` terminates the function entirely and destroys its local state. `yield` pauses the function, saves its local state (variables and instruction pointer), returns a value, and allows the function to resume exactly where it left off on the next call.

4. When should you use a generator instead of a list?
   Answer: Whenever you are processing a massive sequence of data (e.g., reading a 50GB file, streaming LLM tokens, or infinite sequences) where you only need one item at a time, to avoid OOM (Out Of Memory) errors.
"""

if __name__ == "__main__":
    demonstrate_decorators()
    demonstrate_advanced_decorators()
    demonstrate_generators()
    demonstrate_generator_memory()
    demonstrate_coroutines()
    print("\n[SUCCESS] Laboratory: Decorators and Generators Completed.")
