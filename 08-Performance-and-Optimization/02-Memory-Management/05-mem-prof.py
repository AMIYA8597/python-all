"""
Memory Management: Memory Profiling

Learning Objectives:
1. Learn how to track memory allocations in Python.
2. Understand the built-in `tracemalloc` module.
3. Identify memory leaks and memory hogs in a Python script.
4. Compare snapshots to find where memory grew.

Concept Explanation:
Unlike time profiling, memory profiling helps you find *where* your program is 
consuming RAM. The `tracemalloc` module, built into Python 3.4+, traces memory 
blocks allocated by Python. By taking snapshots before and after an operation, 
you can pinpoint exactly which file and line of code allocated the most memory.
"""

import tracemalloc
import time
from typing import List

# --- Basic Implementation ---
def create_memory_hog(size: int) -> List[str]:
    """Function that consumes a lot of memory."""
    # A list of large strings
    return ["A" * 1000 for _ in range(size)]

# --- Intermediate Implementation ---
def track_memory(func, *args, **kwargs):
    """Wrapper to track memory used by a function."""
    tracemalloc.start()
    
    snapshot1 = tracemalloc.take_snapshot()
    result = func(*args, **kwargs)
    snapshot2 = tracemalloc.take_snapshot()
    
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print(f"\n[Memory Profile for {func.__name__}]")
    for stat in top_stats[:3]:
        print(stat)
        
    tracemalloc.stop()
    return result

# --- Advanced Implementation / Performance Analysis ---
class LeakyClass:
    _cache = []
    
    @classmethod
    def leak_memory(cls, data: str):
        """Intentionally leaks memory into a class variable."""
        cls._cache.append(data * 1000)

def simulate_application_loop():
    """Simulate a loop where memory leaks over time."""
    tracemalloc.start()
    
    # Base snapshot
    snap1 = tracemalloc.take_snapshot()
    
    for i in range(10):
        LeakyClass.leak_memory(f"Leak{i}")
        
    # Final snapshot
    snap2 = tracemalloc.take_snapshot()
    
    print("\n[Application Loop Memory Leak Analysis]")
    stats = snap2.compare_to(snap1, 'lineno')
    for stat in stats[:3]:
        print(stat)
        
    tracemalloc.stop()

# --- Edge Cases ---
def memory_fragmentation_example():
    """Demonstrate how allocating and deleting still leaves fragmentation."""
    tracemalloc.start()
    s1 = tracemalloc.take_snapshot()
    
    data = [create_memory_hog(100) for _ in range(10)]
    del data[::2]  # Delete half the objects, leaving holes
    
    s2 = tracemalloc.take_snapshot()
    diff = s2.compare_to(s1, 'lineno')
    print("\n[Fragmentation Example]")
    print(diff[0])
    tracemalloc.stop()

# --- Interview Challenge ---
"""
Challenge: Write a decorator that logs the peak memory usage of a function.
"""
def memory_profiler(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        res = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Function {func.__name__} peak memory: {peak / 10**6:.3f} MB")
        tracemalloc.stop()
        return res
    return wrapper

@memory_profiler
def example_func():
    return create_memory_hog(10000)

# --- Tests ---
def run_tests():
    # Mostly ensuring functions run without error
    _ = track_memory(create_memory_hog, 100)
    simulate_application_loop()
    example_func()
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: tracemalloc ---")
    run_tests()
