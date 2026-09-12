"""
Module: Distributed Computing with Dask Simulation
==================================================

Learning Objectives:
1. Understand lazy evaluation and task graphs.
2. Learn how Dask scales operations beyond RAM limits.
3. Handle chunked computation.

Concept Explanation:
Dask is a flexible parallel computing library in Python. It provides parallelized
versions of NumPy arrays and Pandas dataframes by breaking them down into smaller
chunks and building a task graph for lazy execution.

(Note: This module simulates Dask concepts using generators or standard libraries
in case dask is not installed, but outlines standard dask patterns.)

Type Hints & Edge Cases:
- Large out-of-memory structures.
"""

from typing import List, Iterator

# Basic Concept: Lazy Evaluation via Generators
def lazy_range(n: int) -> Iterator[int]:
    """Generates numbers lazily (simulating dask delayed)."""
    for i in range(n):
        yield i

def lazy_square(nums: Iterator[int]) -> Iterator[int]:
    for num in nums:
        yield num * num

# Advanced Concept: Simulated Dask Array Chunking
class SimDaskArray:
    def __init__(self, data: List[int], chunk_size: int):
        self.data = data
        self.chunk_size = chunk_size
        self.chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
    def sum(self) -> int:
        """Simulates computing sum of chunks lazily/parallelly."""
        # In real Dask, this builds a computation graph and `.compute()` executes it.
        chunk_sums = [sum(chunk) for chunk in self.chunks]
        return sum(chunk_sums)

# Interview Challenge
def challenge_moving_average(arr: SimDaskArray, window: int) -> List[float]:
    """Challenge: Calculate moving average over a chunked array."""
    data = arr.data
    res = []
    for i in range(len(data) - window + 1):
        res.append(sum(data[i:i+window]) / window)
    return res

def test_dask_sim():
    # Test Lazy Evaluation
    nums = lazy_range(5)
    squares = list(lazy_square(nums))
    assert squares == [0, 1, 4, 9, 16], "Lazy evaluation failed"
    
    # Test Chunked Array
    arr = SimDaskArray(list(range(100)), chunk_size=10)
    assert arr.sum() == sum(range(100)), "Simulated Dask sum failed"
    
    # Test Moving Average
    ma_arr = SimDaskArray([1, 2, 3, 4, 5], chunk_size=2)
    assert challenge_moving_average(ma_arr, 3) == [2.0, 3.0, 4.0], "Moving average failed"
    
    print("All tests passed.")

if __name__ == "__main__":
    print("Dask Algorithms Execution\\n" + "-"*30)
    test_dask_sim()
