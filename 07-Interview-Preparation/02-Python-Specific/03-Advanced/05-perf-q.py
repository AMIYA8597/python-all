"""
Performance Optimization and Profiling in Python

Learning Objectives:
1. Identify common performance bottlenecks in Python (list comprehensions vs loops, generator expressions).
2. Utilize built-in profiling tools (`timeit`, `cProfile`).
3. Optimize code using proper data structures (e.g., `set` for lookups, `collections.deque`).
4. Understand memory efficiency techniques like `__slots__`.

Concept Explanation:
- Profiling is measuring where a program spends its time or memory. Optimize only after profiling ("Premature optimization is the root of all evil").
- Python list lookups are O(N), set lookups are O(1).
- List comprehensions and generator expressions are faster than standard `for` loops due to underlying C-level optimizations.
- The `__slots__` attribute reduces memory overhead for classes with many instances by preventing the creation of a `__dict__`.

Interview Focus:
- How would you optimize a Python script that is running slowly?
- When should you use a generator instead of a list?
- What are `__slots__` and how do they save memory?
"""
import timeit
import cProfile
import pstats
import io
from typing import List

# ==========================================
# 1. Data Structure Selection
# ==========================================

def find_common_elements_slow(list1: List[int], list2: List[int]) -> List[int]:
    """O(N * M) complexity due to list lookup inside a loop."""
    common = []
    for item in list1:
        if item in list2: # O(M) operation
            common.append(item)
    return common

def find_common_elements_fast(list1: List[int], list2: List[int]) -> List[int]:
    """O(N + M) complexity by converting one list to a set for O(1) lookups."""
    set2 = set(list2) # O(M)
    # List comprehension + O(1) lookup
    return [item for item in list1 if item in set2]

# ==========================================
# 2. Memory Optimization with __slots__
# ==========================================

class PointSlow:
    """Standard class, uses a __dict__ for attributes."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class PointFast:
    """Optimized class, prevents __dict__ creation, saving memory."""
    __slots__ = ['x', 'y']
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# ==========================================
# 3. Profiling Utility (Decorator)
# ==========================================

def profile(fnc):
    """A decorator that uses cProfile to profile a function."""
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(10) # Print top 10 rows
        print(s.getvalue())
        return retval
    return inner

@profile
def simulated_workload():
    """Simulates a workload to demonstrate profiling."""
    l1 = list(range(10000))
    l2 = list(range(5000, 15000))
    
    # Intentionally call the slow version to see it in profiling output
    find_common_elements_slow(l1, l2)
    # Then the fast version
    find_common_elements_fast(l1, l2)

def test_performance():
    l1 = list(range(1000))
    l2 = list(range(500, 1500))
    
    assert find_common_elements_slow(l1, l2) == find_common_elements_fast(l1, l2)
    
    # Timing with timeit
    slow_time = timeit.timeit(lambda: find_common_elements_slow(l1, l2), number=100)
    fast_time = timeit.timeit(lambda: find_common_elements_fast(l1, l2), number=100)
    
    print(f"Slow function time: {slow_time:.4f}s")
    print(f"Fast function time: {fast_time:.4f}s")
    print(f"Speedup: {slow_time / fast_time:.2f}x")
    
    print("\nRunning simulated workload to show cProfile output...")
    simulated_workload()
    
    print("Performance tests passed!")

if __name__ == "__main__":
    test_performance()
