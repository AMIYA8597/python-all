"""
Profiling Tools: Built-in cProfile

Learning Objectives:
1. Understand the difference between macro and micro profiling.
2. Use Python's built-in `cProfile` module.
3. Use the `pstats` module to format and sort profiling output.
4. Identify bottlenecks by analyzing `tottime` vs `cumtime`.

Concept Explanation:
Before optimizing code, you must measure it. Blind optimization wastes time.
`cProfile` is a C-extension that hooks into Python to measure how often and 
for how long various parts of the program are executed.
- `tottime`: Total time spent IN the function alone.
- `cumtime`: Total time spent IN the function AND all functions it called.
"""

import cProfile
import pstats
import io
import math
import time

# --- Basic Implementation ---
def slow_string_concat() -> str:
    """Inefficient string building."""
    s = ""
    for i in range(10000):
        s += str(i)
    return s

def fast_string_join() -> str:
    """Efficient string building."""
    return "".join(str(i) for i in range(10000))

def compute_heavy_math():
    """A CPU intensive function."""
    res = []
    for i in range(5000):
        res.append(math.factorial(500))
    return res

# --- Intermediate Implementation ---
def main_application():
    """A simulated app with multiple bottlenecks."""
    slow_string_concat()
    fast_string_join()
    compute_heavy_math()
    # Simulate waiting on IO
    time.sleep(0.5)

# --- Advanced Implementation / Performance Analysis ---
def profile_function(func):
    """A decorator to profile a single function."""
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        result = func(*args, **kwargs)
        
        pr.disable()
        s = io.StringIO()
        # Sort by cumulative time
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # Print only top 10 lines
        ps.print_stats(10)
        print(s.getvalue())
        return result
    return wrapper

@profile_function
def run_app_with_decorator():
    main_application()

# --- Edge Cases ---
def overhead_edge_case():
    """
    cProfile introduces overhead! Functions that are extremely fast but called 
    millions of times will appear artificially slow because the profiling hook 
    takes longer than the function itself.
    """
    pass

# --- Interview Challenge ---
"""
Challenge: Looking at a cProfile output, a function `foo` has high `cumtime` 
but very low `tottime`. A function `bar` has high `tottime`. 
Which should you optimize to improve performance?

Answer: `bar`. `foo`'s high cumtime means it's calling other things that take 
time, but `foo` itself isn't doing the heavy lifting. `bar` is actually doing 
work, so optimizing `bar` will yield the best results.
"""

# --- Tests ---
def run_tests():
    assert len(slow_string_concat()) == len(fast_string_join())
    print("Tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: cProfile ---")
    print("Profiling the main_application:\n")
    
    # We can also profile a block of code directly
    pr = cProfile.Profile()
    pr.enable()
    main_application()
    pr.disable()
    
    # Format the stats
    ps = pstats.Stats(pr)
    
    print("\n--- Sorted by Total Time (Where CPU spends most effort) ---")
    ps.sort_stats('tottime').print_stats(5)
    
    print("\n--- Sorted by Cumulative Time (The call chain) ---")
    ps.sort_stats('cumtime').print_stats(5)
    
    run_tests()
