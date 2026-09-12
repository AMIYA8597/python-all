"""
Parallel Sort Implementation and Analysis.

Learning Objectives:
1. Understand how sorting can be parallelized.
2. Use Python's multiprocessing module for parallel sorting.
3. Recognize the overhead of parallelization in Python.

Concept Explanation:
Parallel sorting aims to speed up the sorting process by utilizing multiple CPU cores.
A common approach is parallel merge sort: the array is divided into sub-arrays,
each sub-array is sorted in a separate process, and then the sorted sub-arrays are merged.
In Python, due to the Global Interpreter Lock (GIL), threading is not effective for CPU-bound
tasks like sorting, so multiprocessing is preferred.

Performance Analysis:
- Time Complexity: Ideally O((N/P) log(N/P)) where P is number of processors, plus merge time.
- Space Complexity: O(N) for merging.
- Note: Inter-process communication overhead can make this slower than sequential sort for small N.

Edge Cases:
- Small arrays where IPC overhead dominates.
- Single-core machines (will not provide speedup).

Interview Challenge:
Why use multiprocessing over multithreading for parallel sorting in Python?
Answer: Because of the Global Interpreter Lock (GIL) in CPython, multiple threads cannot execute Python bytecodes simultaneously. Thus, for CPU-bound tasks like sorting, multiprocessing is required to achieve true parallelism.
"""

import multiprocessing
from typing import List

def merge(left: List[int], right: List[int]) -> List[int]:
    """Merges two sorted lists."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def parallel_merge_sort(arr: List[int]) -> List[int]:
    """Parallel implementation of merge sort."""
    if len(arr) <= 1:
        return arr
        
    num_processes = multiprocessing.cpu_count()
    
    # If the array is too small, fallback to standard sort to avoid overhead
    if len(arr) < 1000:
         return sorted(arr)
         
    # Split the array into chunks
    chunk_size = max(1, len(arr) // num_processes)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(sorted, chunks)
        
    # Merge sorted chunks
    while len(sorted_chunks) > 1:
        merged_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged_chunks.append(merge(sorted_chunks[i], sorted_chunks[i+1]))
            else:
                merged_chunks.append(sorted_chunks[i])
        sorted_chunks = merged_chunks
        
    return sorted_chunks[0] if sorted_chunks else []

def test_parallel_sort() -> None:
    """Tests for parallel sort."""
    import random
    arr = [random.randint(0, 10000) for _ in range(5000)]
    sorted_arr = parallel_merge_sort(arr)
    assert sorted_arr == sorted(arr), "Parallel sort failed"
    
    empty: List[int] = []
    assert parallel_merge_sort(empty) == [], "Empty test failed"
    
    single = [1]
    assert parallel_merge_sort(single) == [1], "Single element test failed"
    
    print("All Parallel Sort tests passed!")

if __name__ == "__main__":
    test_parallel_sort()
