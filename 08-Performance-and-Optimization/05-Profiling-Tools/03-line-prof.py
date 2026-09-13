"""
Profiling Tools: Line Profiler

Learning Objectives:
1. Understand line-by-line time profiling.
2. Use the external `line_profiler` library.
3. Identify precisely which line of a function is the performance bottleneck.
4. Compare `line_profiler` with `cProfile`.

Concept Explanation:
`cProfile` tells you *which function* is slow. `line_profiler` tells you 
*which line within that function* is slow. It evaluates the execution time of 
each individual line of code. This is invaluable for complex mathematical 
functions or large loops where cProfile's function-level view is too broad.

Requires: `pip install line_profiler`
"""

try:
    from line_profiler import LineProfiler
    has_lp = True
except ImportError:
    has_lp = False
    print("Warning: line_profiler not installed. Profiling will be mocked.")

import time
import math
from typing import List

# --- Basic Implementation ---
def slow_math_function(data: List[int]) -> List[float]:
    """A function with multiple distinct steps, some slow, some fast."""
    results = []
    
    # Step 1: Fast iteration, slow math
    for x in data:
        results.append(math.sqrt(x) ** 2.5)
        
    # Step 2: Slow I/O simulation
    time.sleep(0.2)
    
    # Step 3: Fast list comprehension
    filtered = [x for x in results if x > 100]
    
    return filtered

# --- Intermediate Implementation ---
def run_profiler():
    """Programmatically run line_profiler without command line tools."""
    if not has_lp:
        print("Cannot run profiler without line_profiler installed.")
        return
        
    data = list(range(100_000))
    
    # Initialize the profiler
    lp = LineProfiler()
    
    # Add the function you want to profile
    lp.add_function(slow_math_function)
    
    # Wrap the function execution
    lp_wrapper = lp(slow_math_function)
    lp_wrapper(data)
    
    # Print the stats
    print("\n[Line Profiler Results]")
    lp.print_stats()

# --- Advanced Implementation / Performance Analysis ---
"""
Output of line_profiler looks like this:
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    26                                           def slow_math_function(data):
    27         1          2.0      2.0      0.0      results = []
    28    100001      18564.0      0.2      9.1      for x in data:
    29    100000     162354.0      1.6     79.6          results.append(math.sqrt(x) ** 2.5)
    30         1      20015.0  20015.0      9.8      time.sleep(0.2)
    31         1       3102.0   3102.0      1.5      filtered = [x for x in results if x > 100]

This clearly shows that Line 29 takes almost 80% of the function's execution time!
"""

# --- Edge Cases ---
def overhead_warning():
    """
    Line profiler has immense overhead (can slow your code down by 10x or more).
    Do NOT leave `@profile` decorators in production code.
    Only profile small, representative datasets, not massive production datasets.
    """
    pass

# --- Interview Challenge ---
"""
Challenge: Why not just use `time.time()` around blocks of code instead of `line_profiler`?
Answer: Manual timing requires modifying the code, adding clutter, and is error-prone. 
`line_profiler` does it automatically, aggregates the data cleanly, and handles 
loops seamlessly without polluting the source code logic.
"""

# --- Tests ---
def run_tests():
    res = slow_math_function([1, 10, 100])
    assert isinstance(res, list)
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: line_profiler ---")
    run_profiler()
    run_tests()
    
    print("\nTip: To use via command line (kernprof):")
    print("1. Add @profile decorator to the function")
    print("2. Run: kernprof -l -v 03-line-prof.py")
