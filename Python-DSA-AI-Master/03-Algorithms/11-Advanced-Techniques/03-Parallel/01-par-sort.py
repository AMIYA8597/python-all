"""
Module: Parallel Sorting Algorithms
===================================

Learning Objectives:
1. Understand the concept of divide and conquer in parallel computing.
2. Implement a parallel version of merge sort using Python's multiprocessing.
3. Compare the performance of sequential and parallel sorting.

Concept Explanation:
Parallel sorting divides a large dataset into smaller chunks, sorts these chunks
independently on different CPU cores, and then merges the sorted chunks back together.
This reduces the time complexity theoretically by a factor of the number of processors.

Type Hints & Edge Cases:
- Empty arrays or single-element arrays are handled efficiently.
- Array sizes not divisible by number of processors are managed appropriately.
"""

import multiprocessing
import random
import time
from typing import List

# Basic Implementation: Sequential Merge Sort
def merge(left: List[int], right: List[int]) -> List[int]:
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

def sequential_merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    return merge(left, right)

# Intermediate/Advanced Implementation: Parallel Merge Sort
def parallel_merge_sort(arr: List[int], processes: int = multiprocessing.cpu_count()) -> List[int]:
    """Sorts an array using multiprocessing."""
    if len(arr) <= 1:
        return arr
        
    chunk_size = max(1, len(arr) // processes)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    with multiprocessing.Pool(processes) as pool:
        sorted_chunks = pool.map(sequential_merge_sort, chunks)
        
    while len(sorted_chunks) > 1:
        merged_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged_chunks.append(merge(sorted_chunks[i], sorted_chunks[i+1]))
            else:
                merged_chunks.append(sorted_chunks[i])
        sorted_chunks = merged_chunks
        
    return sorted_chunks[0]

# Interview Challenge
def challenge_k_way_merge(lists: List[List[int]]) -> List[int]:
    """
    Challenge: Merge k sorted lists efficiently.
    Hint: Can use parallel reduction or min-heap.
    """
    if not lists:
        return []
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                merged.append(merge(lists[i], lists[i+1]))
            else:
                merged.append(lists[i])
        lists = merged
    return lists[0]

def test_sorts():
    arr = [random.randint(0, 1000) for _ in range(100)]
    assert sequential_merge_sort(arr) == sorted(arr), "Sequential sort failed"
    assert parallel_merge_sort(arr) == sorted(arr), "Parallel sort failed"
    assert challenge_k_way_merge([[1, 4, 7], [2, 5, 8], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "K-way merge failed"
    print("All tests passed.")

def performance_analysis():
    # Performance Analysis
    arr = [random.randint(0, 100000) for _ in range(200000)] # Keep size manageable for tests
    
    start = time.time()
    sequential_merge_sort(arr)
    seq_time = time.time() - start
    print(f"Sequential Time: {seq_time:.4f}s")
    
    start = time.time()
    parallel_merge_sort(arr)
    par_time = time.time() - start
    print(f"Parallel Time: {par_time:.4f}s")
    print(f"Speedup: {seq_time / par_time:.2f}x (Note: Speedup varies due to overhead on smaller arrays)")

if __name__ == "__main__":
    print("Parallel Sorting Execution\\n" + "-"*30)
    test_sorts()
    # To run performance analysis, uncomment the next line. Multiprocessing in tests can be slow.
    # performance_analysis()
