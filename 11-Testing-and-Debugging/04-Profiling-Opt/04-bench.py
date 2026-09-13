"""
Benchmarking in Python

Learning Objectives:
1. Distinguish between profiling (finding bottlenecks) and benchmarking (comparing implementations).
2. Set up fair benchmarking tests.
3. Use multiple iterations to get statistically significant results.
4. Compare different data structures and algorithms.

Concept Explanation:
Benchmarking is the practice of comparing the performance of different systems, algorithms,
or implementations under specific workloads. While profiling tells you *where* your code is
slow, benchmarking tells you *which* approach is faster overall.

Imports:
- timeit: For accurate, isolated timing.
- random: For generating test data.
- statistics: For calculating mean and variance of benchmark runs.
"""

import timeit
import random
import statistics
from typing import List, Callable, Any

# ==========================================
# Basic Implementation: Simple Comparison
# ==========================================

def generate_data(size: int = 10000) -> List[int]:
    """Generates a random list of integers."""
    return [random.randint(1, 1000) for _ in range(size)]

def search_list(data: List[int], target: int) -> bool:
    """Searches for an item in a list (O(n))."""
    return target in data

def search_set(data: set, target: int) -> bool:
    """Searches for an item in a set (O(1))."""
    return target in data

# ==========================================
# Intermediate Implementation: Benchmark Runner
# ==========================================

def run_benchmark(func: Callable, *args: Any, iterations: int = 1000) -> float:
    """Runs a function multiple times and returns the average execution time."""
    # We use a lambda to pass arguments to the function within timeit
    timer = timeit.Timer(lambda: func(*args))
    # Execute the benchmark
    times = timer.repeat(repeat=5, number=iterations)
    # Return the minimum time to filter out OS noise
    return min(times) / iterations

def compare_search_structures() -> None:
    """Benchmarks searching in a List vs. a Set."""
    data_list = generate_data(10000)
    data_set = set(data_list)
    target = -1 # Worst-case scenario: target not in collection
    
    list_time = run_benchmark(search_list, data_list, target)
    set_time = run_benchmark(search_set, data_set, target)
    
    print(f"List Search Time (per operation): {list_time:.8f}s")
    print(f"Set Search Time  (per operation): {set_time:.8f}s")
    print(f"Set is {list_time / set_time:.2f}x faster!")

# ==========================================
# Advanced Implementation: Statistical Benchmarking
# ==========================================

def benchmark_with_stats(name: str, stmt: str, setup: str, repeat: int = 10, number: int = 1000) -> None:
    """Runs a benchmark and prints statistical data (mean, median, stdev)."""
    times = timeit.repeat(stmt=stmt, setup=setup, repeat=repeat, number=number)
    
    # Normalize times per operation
    times_per_op = [t / number for t in times]
    
    mean = statistics.mean(times_per_op)
    stdev = statistics.stdev(times_per_op)
    
    print(f"--- Benchmark: {name} ---")
    print(f"Mean execution time: {mean:.8f}s ± {stdev:.8f}s")
    print(f"Min: {min(times_per_op):.8f}s | Max: {max(times_per_op):.8f}s")

# ==========================================
# Edge Cases & Interview Challenge
# ==========================================

"""
Edge Cases:
1. Garbage Collection: timeit disables GC during runs to prevent it from skewing results.
   If your code relies heavily on GC, you might need to enable it in the setup.
2. Warm-up phase: JIT compilers (like PyPy) need a warm-up phase to optimize code.

Interview Challenge:
Question: Why is finding an element in a Set generally O(1) in Python, but finding it
in a List is O(n)? What happens if there are many hash collisions in the Set?
Hint: Sets are implemented as hash tables. Hash collisions degrade performance to O(n)
in the worst case.
"""

def test_benchmark() -> None:
    """Tests the data generation."""
    data = generate_data(10)
    assert len(data) == 10
    print("Tests passed.")

if __name__ == "__main__":
    print("--- Benchmarking ---")
    print("1. Data Structure Comparison:")
    compare_search_structures()
    
    print("\n2. Statistical Benchmarking:")
    setup_str = "data = list(range(1000))"
    stmt_map = "list(map(str, data))"
    stmt_comp = "[str(x) for x in data]"
    
    benchmark_with_stats("map() vs string conversion", stmt_map, setup_str)
    benchmark_with_stats("List comprehension string conversion", stmt_comp, setup_str)
    
    print("\n3. Running Tests:")
    test_benchmark()
