"""
Module: Data Science Optimization Techniques

Learning Objectives:
1. Identify performance bottlenecks in Python code using algorithmic analysis.
2. Replace slow Python loops with optimized algorithmic approaches and vectorization concepts.
3. Understand the importance of caching and memoization in data pipelines.
4. Learn how to optimize time and space complexity for technical interviews.

Concept Explanation:
Python is an interpreted language, which means native `for` loops can be slow when processing 
millions of items. In Data Science, optimization is crucial. Optimization falls into three tiers:
1. Algorithmic Optimization: Changing the data structures (e.g., using Sets instead of Lists for O(1) lookups).
2. Caching/Memoization: Preventing the re-calculation of expensive, repeated operations.
3. Vectorization (Simulated here): Processing entire arrays of data simultaneously in C/C++ backends 
   (typically done using NumPy or Pandas).

===========================================================================
Basic Implementation
===========================================================================
A classic slow algorithm: Finding common elements between two large lists using nested loops,
and an unoptimized recursive function mimicking an expensive data calculation.
"""

import time
from typing import List, Set, Callable, Any
from functools import lru_cache

# ---------------------------------------------------------------------------
# Basic Approach: O(N * M) Time Complexity
# ---------------------------------------------------------------------------
def find_common_elements_basic(list_a: List[int], list_b: List[int]) -> List[int]:
    """
    Basic approach to finding common elements.
    Highly inefficient because the `in` operator on a list takes O(M) time, 
    making the total time O(N * M).
    """
    common = []
    for item in list_a:
        if item in list_b:  # O(M) search inside an O(N) loop
            if item not in common:
                common.append(item)
    return common

def expensive_computation_basic(n: int) -> int:
    """
    Simulates an expensive recursive calculation (like Fibonacci).
    Time Complexity is O(2^N) due to redundant calculations.
    """
    if n <= 1:
        return n
    return expensive_computation_basic(n-1) + expensive_computation_basic(n-2)


# ===========================================================================
# Professional Implementation
# ===========================================================================

class DataOptimizer:
    """
    Professional implementation showcasing various Data Science optimization techniques.
    """

    @staticmethod
    def find_common_elements_optimized(list_a: List[int], list_b: List[int]) -> List[int]:
        """
        Algorithmic Optimization: Uses Sets for O(1) lookups.
        Time Complexity: O(N + M) - drastically faster than basic.
        Space Complexity: O(M) to store the set.
        """
        # Convert list_b to a set for O(1) lookups
        set_b = set(list_b)
        
        # Use list comprehension for speed, filtering through the set
        # We also use a set to ensure unique results, then convert back to list
        common_set = {item for item in list_a if item in set_b}
        return list(common_set)

    @staticmethod
    @lru_cache(maxsize=128)
    def expensive_computation_optimized(n: int) -> int:
        """
        Caching Optimization: Uses functools.lru_cache to memoize results.
        If a result for 'n' was already calculated, it returns in O(1) time.
        Time Complexity drops from O(2^N) to O(N).
        """
        if n <= 1:
            return n
        return DataOptimizer.expensive_computation_optimized(n-1) + DataOptimizer.expensive_computation_optimized(n-2)
        
    @staticmethod
    def simulate_vectorized_operation(data: List[float], scalar: float) -> List[float]:
        """
        Vectorization Concept: In pure Python, list comprehensions or map() 
        are the closest we get to "vectorized" speeds without NumPy. They are 
        implemented in C under the hood of the Python interpreter, making them 
        faster than standard append() loops.
        """
        # Standard loop would use data.append(val * scalar)
        # List comprehension is highly optimized in CPython
        return [val * scalar for val in data]


# ===========================================================================
# Complexity Analysis & Interview Challenge
# ===========================================================================
"""
Complexity Analysis Highlights:
1. Data Structures Matter: Changing a List to a Set changed our search algorithm 
   from O(N^2) to O(N). This is the most common optimization in technical interviews.
2. Memoization: Trading Space for Time. By storing previous answers in a cache 
   (Space O(N)), we eliminated redundant tree branches, reducing time from O(2^N) to O(N).

Interview Challenge:
Question: You have a DataFrame with 10 million rows, and you need to apply a complex 
          mathematical transformation to a specific column. `df.apply(my_func)` is taking 
          too long. How do you optimize it?
Answer:
1. Vectorization: Rewrite the mathematical transformation using native NumPy/Pandas operations 
   instead of applying a custom Python function row-by-row.
2. Cython/Numba: If the logic cannot be vectorized (e.g., it contains complex stateful loops), 
   compile the function using Numba (`@jit`) or Cython to run at C-speeds.
3. Parallelization: Split the DataFrame into chunks and use `multiprocessing` or tools 
   like Dask to process chunks across multiple CPU cores.
"""

# ===========================================================================
# Example Usage & Tests
# ===========================================================================
def time_execution(func: Callable, *args: Any) -> float:
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start

if __name__ == "__main__":
    print("Testing Data Science Optimization Techniques...")
    
    # 1. Test Algorithmic Optimization (Sets vs Lists)
    a = list(range(10000))
    b = list(range(5000, 15000))
    
    # Warm up caches
    basic_res = find_common_elements_basic(a[:100], b[:100])
    opt_res = DataOptimizer.find_common_elements_optimized(a[:100], b[:100])
    
    time_basic = time_execution(find_common_elements_basic, a, b)
    time_opt = time_execution(DataOptimizer.find_common_elements_optimized, a, b)
    
    print(f"List Lookup Time: {time_basic:.4f}s")
    print(f"Set Lookup Time:  {time_opt:.4f}s")
    print(f"Speedup: {time_basic / time_opt:.1f}x")
    
    # Assertions
    assert sorted(find_common_elements_basic([1, 2, 3], [2, 3, 4])) == [2, 3]
    assert sorted(DataOptimizer.find_common_elements_optimized([1, 2, 3], [2, 3, 4])) == [2, 3]

    # 2. Test Memoization / Caching
    # We use a small N for basic so it doesn't hang forever, but a larger N for optimized
    val_basic = expensive_computation_basic(30)
    val_opt = DataOptimizer.expensive_computation_optimized(30)
    assert val_basic == val_opt
    
    # Optimized can easily handle large N instantly
    val_large = DataOptimizer.expensive_computation_optimized(100)
    assert val_large > 0 # Just verify it computed
    
    print("All optimization tests passed successfully!")
