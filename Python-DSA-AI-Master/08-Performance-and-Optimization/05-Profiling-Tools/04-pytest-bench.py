"""
Profiling Tools: Pytest-Benchmark

Learning Objectives:
1. Understand the importance of statistically valid microbenchmarks.
2. Use the `pytest-benchmark` plugin.
3. Compare different algorithms objectively within a test suite.
4. Prevent regression by setting benchmark limits.

Concept Explanation:
Using `time.time()` or even `timeit` manually can be noisy due to background OS tasks.
`pytest-benchmark` integrates with the `pytest` testing framework to run your code
multiple times, throw out outliers, and provide statistically significant metrics 
(Mean, Min, Max, Standard Deviation). This ensures that optimizations are actually 
faster and aren't just getting lucky on a single run.

Requires: `pip install pytest pytest-benchmark`
"""

# Note: This script is meant to be run with `pytest 04-pytest-bench.py`

import pytest
from typing import List

# --- Target Functions to Benchmark ---

def sort_builtin(data: List[int]) -> List[int]:
    """Python's highly optimized Timsort (written in C)."""
    return sorted(data)

def sort_bubble(data: List[int]) -> List[int]:
    """Naive bubble sort (written in pure Python)."""
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# --- Benchmark Tests ---
# The 'benchmark' fixture is provided automatically by pytest-benchmark

def test_builtin_sort(benchmark):
    """Benchmark Python's sorted() function."""
    import random
    data = [random.randint(0, 1000) for _ in range(1000)]
    
    # benchmark() runs the function multiple times to gather statistics
    result = benchmark(sort_builtin, data)
    assert result == sorted(data)

def test_bubble_sort(benchmark):
    """Benchmark custom bubble sort function."""
    import random
    # Using a smaller dataset because bubble sort is O(N^2)
    # Using 1000 here would make the test extremely slow
    data = [random.randint(0, 1000) for _ in range(100)]
    
    result = benchmark(sort_bubble, data)
    assert result == sorted(data)

# --- Advanced Usage ---

def test_sort_with_setup(benchmark):
    """Use setup function to avoid measuring data generation time."""
    import random
    
    def generate_data():
        # Setup returns the positional and keyword arguments for the target
        args = ([random.randint(0, 100) for _ in range(500)], )
        kwargs = {}
        return args, kwargs
        
    # The benchmark will call generate_data() before each run
    result = benchmark.pedantic(sort_builtin, setup=generate_data, rounds=100)
    assert len(result) == 500

# --- Interview Challenge ---
"""
Challenge: Why is the Minimum time often considered a better metric than the 
Mean time in microbenchmarking?

Answer: An OS can arbitrarily pause your process to run background tasks, 
inflating the execution time. However, the OS cannot make your code run *faster* 
than its physical limit. The minimum time represents the execution where the OS 
interfered the least.
"""

# --- Execution Block ---
if __name__ == '__main__':
    print("--- Performance Analysis: pytest-benchmark ---")
    print("This file contains pytest tests.")
    print("To run the benchmarks, open your terminal and execute:")
    print("pip install pytest pytest-benchmark")
    print("pytest 04-pytest-bench.py")
    
    """
    Example Output:
    ----------------------------------------------------------------------------------
    Name (time in us)           Min         Max        Mean      StdDev       Median
    ----------------------------------------------------------------------------------
    test_builtin_sort       41.4000    133.5000     45.6811      7.8920      43.5000
    test_bubble_sort       615.1000  1,423.8000    668.7521     76.1132     643.2000
    ----------------------------------------------------------------------------------
    """
