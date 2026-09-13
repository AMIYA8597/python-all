"""
Performance Profiling in Python

Learning Objectives:
1. Understand how to measure execution time of Python code.
2. Learn to use the built-in `cProfile` module for detailed performance analysis.
3. Learn to use the `timeit` module for micro-benchmarking.
4. Identify bottlenecks in code using profiling data.

Concept Explanation:
Performance profiling is the process of measuring the execution time of different parts
of a program to identify bottlenecks. Python provides built-in tools like `cProfile` 
(a C-extension with reasonable overhead suitable for most profiling) and `timeit` 
(for measuring small snippets of code accurately).

Imports:
- cProfile: For profiling the execution of entire functions or scripts.
- pstats: For formatting and analyzing profiling results.
- timeit: For accurate timing of small code blocks.
- time: For basic manual timing.
"""

import cProfile
import pstats
import time
import timeit
import io
from typing import List, Callable, Any

# ==========================================
# Basic Implementation: Manual Timing
# ==========================================

def basic_manual_timing(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """Measures execution time using the time module."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds.")
    return result

# ==========================================
# Intermediate Implementation: Using cProfile
# ==========================================

def profile_function(func: Callable) -> Callable:
    """A decorator that uses cProfile to profile a function."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
        ps.print_stats(10) # Print top 10 lines
        print(s.getvalue())
        
        return result
    return wrapper

# Sample functions to profile
def slow_function(n: int) -> List[int]:
    """A deliberately slow function to demonstrate profiling."""
    result = []
    for i in range(n):
        # Inefficient way to build a list
        result.insert(0, i)
    return result

def fast_function(n: int) -> List[int]:
    """A faster alternative to slow_function."""
    return [i for i in range(n - 1, -1, -1)]

@profile_function
def run_workload() -> None:
    """Runs workloads to be profiled."""
    slow_function(10000)
    fast_function(10000)

# ==========================================
# Advanced Implementation: Micro-benchmarking with timeit
# ==========================================

def micro_benchmark() -> None:
    """Uses timeit to compare two small code snippets."""
    setup_code = ""
    stmt_slow = "[i for i in range(1000)]"
    stmt_fast = "list(range(1000))"
    
    time_slow = timeit.timeit(stmt=stmt_slow, setup=setup_code, number=10000)
    time_fast = timeit.timeit(stmt=stmt_fast, setup=setup_code, number=10000)
    
    print(f"List comprehension time: {time_slow:.4f}s")
    print(f"list() constructor time: {time_fast:.4f}s")

# ==========================================
# Edge Cases & Interview Challenge
# ==========================================

"""
Edge Cases:
1. Profiling very fast functions: Overhead of cProfile might dominate. Use timeit instead.
2. Multi-threaded code: cProfile tracks time per thread; can be tricky to analyze overall performance.

Interview Challenge:
Question: Given a function that processes a large dataset, how would you determine if the bottleneck is CPU bound or I/O bound using Python tools?
Hint: Compare time.perf_counter() (wall-clock time) and time.process_time() (CPU time).
"""

def test_performance_profiling() -> None:
    """Tests the profiling functions."""
    result = basic_manual_timing(fast_function, 1000)
    assert len(result) == 1000
    print("All tests passed!")

if __name__ == "__main__":
    print("--- Performance Profiling ---")
    print("1. Manual Timing:")
    basic_manual_timing(slow_function, 5000)
    
    print("\n2. cProfile Decorator:")
    run_workload()
    
    print("\n3. timeit Micro-benchmarking:")
    micro_benchmark()
    
    print("\n4. Running Tests:")
    test_performance_profiling()
