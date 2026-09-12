"""
Performance Debugging Masterclass

Learning Objectives:
1. Understand how to measure code execution time.
2. Use built-in modules like `timeit`, `cProfile`, and `pstats`.
3. Identify bottlenecks in code and apply optimization strategies.

Concept Explanation:
Performance debugging (profiling) is the process of determining where a program spends its time.
- `timeit`: Good for micro-benchmarking small snippets of code.
- `cProfile`: A deterministic profiler for analyzing entire programs and function calls.
- Algorithmic optimization: Replacing O(N^2) algorithms with O(N log N) or O(N) using appropriate data structures.
"""

import time
import timeit
import cProfile
import pstats
import io
import unittest
from typing import List, Set

# --- Basic Implementation ---
def measure_time_decorator(func):
    """A basic decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        # In a real scenario, we might log this
        wrapper.last_execution_time = end - start
        return result
    return wrapper

@measure_time_decorator
def slow_sum(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total

# --- Intermediate Implementation ---
def compare_list_vs_set(items: List[int], targets: List[int]) -> tuple:
    """Demonstrates performance difference between list and set lookups (timeit)."""
    
    # List lookup O(N)
    def list_lookup():
        return [t for t in targets if t in items]
        
    # Set lookup O(1) avg
    item_set = set(items)
    def set_lookup():
        return [t for t in targets if t in item_set]
        
    # Microbenchmark
    list_time = timeit.timeit(list_lookup, number=10)
    set_time = timeit.timeit(set_lookup, number=10)
    
    return list_time, set_time

# --- Advanced Implementation ---
def computationally_heavy_task(data: List[int]) -> List[int]:
    """A task with multiple steps to profile."""
    def step1(d): return [x * 2 for x in d]
    def step2(d): return sorted(d, reverse=True)
    def step3(d): return [x for x in d if x % 3 == 0]
    
    d1 = step1(data)
    d2 = step2(d1)
    d3 = step3(d2)
    return d3

def profile_heavy_task(data: List[int]) -> str:
    """Uses cProfile to profile the heavy task and returns the stats report."""
    pr = cProfile.Profile()
    pr.enable()
    
    computationally_heavy_task(data)
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats(10) # Print top 10 functions
    return s.getvalue()

# --- Performance Analysis ---
"""
Performance Analysis:
- `timeit` temporarily disables garbage collection to provide consistent micro-benchmarks.
- `cProfile` introduces a slight overhead but is highly accurate for relative function call timings.
- Replacing lists with sets for membership testing changes lookup complexity from O(N) to O(1),
  significantly reducing overall execution time for large datasets.
"""

# --- Edge Cases ---
"""
Edge Cases Handled:
- Empty data sets handled efficiently.
- Using `time.perf_counter()` over `time.time()` for accurate, high-resolution duration measurement
  independent of system clock updates.
"""

# --- Interview Challenge ---
"""
Interview Challenge:
Question: When would you use `timeit` versus `cProfile`?
Answer: Use `timeit` for micro-benchmarking small snippets or single expressions to compare 
specific operations. Use `cProfile` to analyze an entire application or complex function 
to identify bottlenecks and view the call graph.
"""

# --- Tests ---
class TestPerformanceDebugging(unittest.TestCase):
    def test_measure_time_decorator(self):
        res = slow_sum(1000)
        self.assertEqual(res, sum(range(1000)))
        self.assertTrue(hasattr(slow_sum, 'last_execution_time'))
        self.assertGreater(slow_sum.last_execution_time, 0)

    def test_compare_list_vs_set(self):
        items = list(range(1000))
        targets = [999, 500, -1]
        l_time, s_time = compare_list_vs_set(items, targets)
        # Set lookup should be significantly faster or comparable for small test
        self.assertGreaterEqual(l_time, 0)
        self.assertGreaterEqual(s_time, 0)

    def test_profiling(self):
        data = list(range(1000))
        report = profile_heavy_task(data)
        self.assertIn('function calls', report)
        self.assertIn('computationally_heavy_task', report)

if __name__ == "__main__":
    print("Running Performance Debugging Masterclass Tests...")
    unittest.main()
