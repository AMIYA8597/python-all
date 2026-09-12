"""
Performance Testing and Profiling - Educational Script

Learning Objectives:
1. Understand how to measure execution time of Python code.
2. Learn how to use the `timeit` module for micro-benchmarking.
3. Discover profiling tools like `cProfile` and `pstats` to identify bottlenecks.
4. Learn how to write performance regression tests.
5. Understand time complexity implications in real code.

Concept Explanation:
Performance testing ensures your code runs within acceptable time limits and
uses resources efficiently. Profiling is the process of analyzing a program
to determine which parts are consuming the most time or memory.

Key Tools:
- timeit: Accurate timing for small snippets of code.
- cProfile: A deterministic profiler for analyzing function calls.
- time: Simple wall-clock time measurement.
"""

import time
import timeit
import cProfile
import pstats
import io
from typing import List
import random

# --- Basic Implementation: Measuring Execution Time ---

def inefficient_sum(n: int) -> int:
    """A slow way to calculate sum."""
    total = 0
    for i in range(n):
        total += i
    return total

def efficient_sum(n: int) -> int:
    """A fast way using math formula."""
    return (n * (n - 1)) // 2

def basic_timing() -> None:
    """Using time module for simple wall-clock timing."""
    print("--- Basic Timing (time module) ---")
    n = 10_000_000
    
    start_time = time.time()
    inefficient_sum(n)
    end_time = time.time()
    print(f"Inefficient sum took: {end_time - start_time:.4f} seconds")
    
    start_time = time.time()
    efficient_sum(n)
    end_time = time.time()
    print(f"Efficient sum took:   {end_time - start_time:.4f} seconds\\n")

# --- Intermediate Implementation: Micro-benchmarking with timeit ---

def micro_benchmarking() -> None:
    """Using timeit for accurate measurement of small snippets."""
    print("--- Micro-benchmarking (timeit module) ---")
    
    # Setup code is run once, stmt is run 'number' times
    setup = "data = list(range(1000))"
    stmt1 = "sum(data)"
    stmt2 = \"\"\"
total = 0
for x in data:
    total += x
    \"\"\"
    
    # timeit.timeit returns total time for 'number' executions
    time1 = timeit.timeit(stmt=stmt1, setup=setup, number=10000)
    time2 = timeit.timeit(stmt=stmt2, setup=setup, number=10000)
    
    print(f"Built-in sum() took: {time1:.4f} seconds")
    print(f"For-loop sum took:   {time2:.4f} seconds")
    print(f"Built-in is {time2/time1:.2f}x faster\\n")

# --- Advanced Implementation: Profiling with cProfile ---

def complex_operation() -> None:
    """A function that calls other functions, useful for profiling."""
    data = [random.randint(1, 100) for _ in range(10000)]
    _ = sorted(data) # Built-in sort (fast, C implementation)
    
    # Inefficient manual operation
    res = []
    for d in data:
        if d not in res: # O(n) check inside a loop -> O(n^2) overall
            res.append(d)

def profile_code() -> None:
    """Using cProfile to find bottlenecks."""
    print("--- Profiling (cProfile module) ---")
    
    pr = cProfile.Profile()
    pr.enable()
    complex_operation()
    pr.disable()
    
    # Capture and format stats
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(10) # Print top 10 time-consuming calls
    
    print(s.getvalue())

# --- Performance Regression Tests ---
# You can use standard testing frameworks to fail if code is too slow.

def test_performance_regression() -> None:
    """A test that ensures a function runs under a specific time limit."""
    n = 1_000_000
    start = time.time()
    efficient_sum(n)
    duration = time.time() - start
    
    # Fail the test if duration exceeds threshold
    assert duration < 0.1, f"Performance regression: took {duration}s, expected <0.1s"
    print("Performance regression test passed.\\n")

# --- Edge Cases ---
# Timing can be affected by background processes on your machine.
# Garbage collection can pause your program unpredictably.
# Always run performance tests multiple times and take the average or minimum.

# --- Interview Challenge ---
# Challenge: Why is `[x for x in lst]` faster than `res = []; for x in lst: res.append(x)`?
# Answer: List comprehensions are optimized in C within the Python interpreter.
# The append method lookup and function call overhead in the Python loop are avoided.

if __name__ == "__main__":
    basic_timing()
    micro_benchmarking()
    profile_code()
    test_performance_regression()
