"""
System Design: Performance Profiling in Python
==============================================

Learning Objectives:
1. Understand why "guessing" performance bottlenecks is an anti-pattern.
2. Master `cProfile` and `pstats` for algorithmic and time profiling.
3. Learn how to use `tracemalloc` to identify memory leaks and spikes.
4. Learn how to write micro-benchmarks with the `timeit` module.

Concept Explanation:
--------------------
Performance optimization without profiling is premature optimization. In a complex system, the bottleneck might be I/O (network/disk) or CPU (calculations). 
- `cProfile`: A built-in C-extension module that tracks how often and for how long various parts of the program were executed.
- `tracemalloc`: A built-in library to trace memory blocks allocated by Python. Highly useful to find memory leaks.
- `timeit`: Used for micro-benchmarking small snippets of code to avoid caching/OS scheduling anomalies.

Industry Use Cases:
-------------------
- Reducing API response times in Django/FastAPI by profiling endpoints.
- Identifying memory leaks in long-running Celery workers or daemon processes.
- Optimizing scientific computing scripts.

Basic Implementation:
---------------------
"""
import cProfile
import pstats
import io
import time
import tracemalloc
import timeit

def slow_function():
    """A CPU intensive function."""
    total = 0
    for i in range(1_000_000):
        total += i
    return total

def fast_function():
    """Optimized version using built-ins."""
    return sum(range(1_000_000))

def run_basic_profiler():
    """Using cProfile directly in code."""
    pr = cProfile.Profile()
    pr.enable()
    
    slow_function()
    fast_function()
    
    pr.disable()
    s = io.StringIO()
    # Sort by cumulative time
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    return s.getvalue()


# Professional Implementation
# ---------------------------
# Creating decorators for profiling memory and time for continuous monitoring.

from functools import wraps
from typing import Callable, Any

def time_profiler(func: Callable) -> Callable:
    """Decorator to profile the execution time of a specific function using cProfile."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler).sort_stats('tottime')
        print(f"\n--- Performance Profile for {func.__name__} ---")
        stats.print_stats(5)  # Print top 5 rows
        return result
    return wrapper

def memory_profiler(func: Callable) -> Callable:
    """Decorator to trace memory allocation spikes using tracemalloc."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\n--- Memory Profile for {func.__name__} ---")
        print(f"Current Memory Usage: {current / 10**6:.3f} MB")
        print(f"Peak Memory Usage:    {peak / 10**6:.3f} MB")
        return result
    return wrapper


@time_profiler
@memory_profiler
def memory_hungry_task():
    """Simulate a task that loads a lot of data in memory."""
    # Creates a massive list
    large_list = [x * 2 for x in range(1_000_000)]
    return len(large_list)

# Complexity Analysis:
# Profiling inherently introduces overhead. `cProfile` introduces some overhead but is fast enough for development.
# `tracemalloc` can slow down execution significantly and should NOT be running continuously in production.
# Instead, in production, use APM tools (Datadog, New Relic) or sampling profilers (like PySpy).

# Common Mistakes:
# 1. Profiling I/O bound tasks and mistaking waiting for disk/network as CPU inefficiency.
# 2. Running micro-benchmarks without `timeit`, failing to account for GC pauses or CPU frequency scaling.
# 3. Leaving profiling decorators attached in production code, causing severe performance degradation.

# Interview Challenge:
# Q: You notice a memory leak in a long-running Python worker. How do you find it?
# A: First, I would take memory snapshots at different times using `tracemalloc`. 
# By comparing two snapshots (`snapshot2.compare_to(snapshot1, 'lineno')`), I can see exactly which line of code is allocating memory that isn't being freed. Also, I would check for unclosed files/connections, or objects appending to global lists.

if __name__ == "__main__":
    print("Running Profiling Examples...")
    
    # 1. Run timeit microbenchmarks
    print("\n--- Microbenchmarking with timeit ---")
    slow_time = timeit.timeit("slow_function()", globals=globals(), number=5)
    fast_time = timeit.timeit("fast_function()", globals=globals(), number=5)
    print(f"slow_function (5 runs): {slow_time:.4f} seconds")
    print(f"fast_function (5 runs): {fast_time:.4f} seconds")
    
    # 2. Run decorated profiler
    print("\n--- Running Decorated Profilers ---")
    memory_hungry_task()
    
    print("\nAll tests passed successfully.")
