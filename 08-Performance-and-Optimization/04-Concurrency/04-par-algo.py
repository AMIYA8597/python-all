"""
Concurrency: Parallel Algorithms (Divide and Conquer)

Learning Objectives:
1. Understand how to break an algorithm down into parallelizable chunks.
2. Implement a parallel Merge Sort using `multiprocessing`.
3. Understand Amdahl's Law (theoretical limit of parallel speedup).
4. Identify thresholding (when to stop splitting and compute sequentially).

Concept Explanation:
Some algorithms are inherently sequential (like calculating Fibonacci recursively). 
Others, like Merge Sort, can be split into independent sub-problems (Divide and 
Conquer), making them candidates for parallelization. However, inter-process 
communication has overhead. If we parallelize down to arrays of size 1, the overhead 
dominates. We must establish a "chunk size threshold" where we fallback to sequential sorting.
"""

import multiprocessing
import random
import time
from typing import List

# --- Basic Implementation ---
def merge(left: List[int], right: List[int]) -> List[int]:
    """Standard merge function for two sorted arrays."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sequential_mergesort(arr: List[int]) -> List[int]:
    """Standard sequential merge sort."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequential_mergesort(arr[:mid])
    right = sequential_mergesort(arr[mid:])
    return merge(left, right)

# --- Intermediate Implementation ---
# Threshold: below this array size, fallback to sequential to avoid process overhead
THRESHOLD = 100_000

def parallel_mergesort(arr: List[int]) -> List[int]:
    """Parallel merge sort using multiprocessing pool."""
    if len(arr) <= THRESHOLD:
        return sequential_mergesort(arr)
        
    mid = len(arr) // 2
    left_part = arr[:mid]
    right_part = arr[mid:]
    
    # Spawn processes for the two halves
    with multiprocessing.Pool(processes=2) as pool:
        # map handles the pickling and distributing
        sorted_halves = pool.map(parallel_mergesort, [left_part, right_part])
        
    return merge(sorted_halves[0], sorted_halves[1])

# --- Advanced Implementation / Performance Analysis ---
def compare_performance():
    # Note: Sorting integers in Python is heavily optimized via Timsort (list.sort()).
    # A pure Python mergesort is naturally slow, but this demonstrates the parallel concept.
    size = 400_000
    print(f"Generating {size} random integers...")
    data = [random.randint(0, 1000) for _ in range(size)]
    
    print("Sorting sequentially...")
    start = time.perf_counter()
    _ = sequential_mergesort(data)
    t_seq = time.perf_counter() - start
    
    print("Sorting in parallel...")
    start = time.perf_counter()
    _ = parallel_mergesort(data)
    t_par = time.perf_counter() - start
    
    print(f"\nSequential Time: {t_seq:.4f}s")
    print(f"Parallel Time:   {t_par:.4f}s")
    print(f"Speedup:         {t_seq/t_par:.2f}x")

# --- Edge Cases ---
def amdahls_law_explanation():
    """
    Amdahl's Law states: Speedup = 1 / ((1 - P) + P/N)
    where P is the parallelizable portion, and N is the number of processors.
    
    In Parallel Merge Sort, the `merge()` step cannot be parallelized easily.
    Therefore, the `merge()` step is the sequential bottleneck (1 - P).
    No matter how many CPUs you have, you can never be faster than the final merge.
    """
    pass

# --- Tests ---
def run_tests():
    arr = [38, 27, 43, 3, 9, 82, 10]
    assert sequential_mergesort(arr) == [3, 9, 10, 27, 38, 43, 82]
    assert parallel_mergesort(arr) == [3, 9, 10, 27, 38, 43, 82]
    print("\nAll tests passed.")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("--- Performance Analysis: Parallel Algorithms ---")
    compare_performance()
    run_tests()
