"""
Module: Parallel Search Algorithms
==================================

Learning Objectives:
1. Implement parallel search techniques over large datasets.
2. Handle early exits and shared state in parallel processing.
3. Understand overhead vs. benefit in multiprocessing.

Concept Explanation:
Parallel searching involves dividing an array into segments and searching each
segment on a separate core. This is useful for unsorted arrays where binary
search isn't applicable. For sorted arrays, parallel binary search or 
interpolation search can be utilized.

Type Hints & Edge Cases:
- Target not found.
- Empty arrays.
"""

import multiprocessing
import random
import time
from typing import List, Optional, Tuple

# Basic Implementation: Sequential Search
def sequential_search(arr: List[int], target: int) -> int:
    """Returns the index of the target or -1."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Helper for parallel search
def _search_chunk(args: Tuple[List[int], int, int]) -> Optional[int]:
    chunk, target, offset = args
    for i, val in enumerate(chunk):
        if val == target:
            return offset + i
    return None

# Advanced Implementation: Parallel Search
def parallel_search(arr: List[int], target: int, processes: int = multiprocessing.cpu_count()) -> int:
    """Searches an array using multiprocessing."""
    if not arr:
        return -1
        
    chunk_size = max(1, len(arr) // processes)
    chunks = [
        (arr[i:i + chunk_size], target, i)
        for i in range(0, len(arr), chunk_size)
    ]
    
    # We use map_async or imap_unordered for potential early exits, 
    # but for simplicity, we use Pool.map
    with multiprocessing.Pool(processes) as pool:
        results = pool.map(_search_chunk, chunks)
        
    for res in results:
        if res is not None:
            return res
            
    return -1

# Interview Challenge
def challenge_parallel_count(arr: List[int], target: int) -> int:
    """Challenge: Count occurrences of a target in parallel."""
    processes = multiprocessing.cpu_count()
    chunk_size = max(1, len(arr) // processes)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    def count_chunk(chunk: List[int]) -> int:
        return chunk.count(target)
        
    with multiprocessing.Pool(processes) as pool:
        counts = pool.map(count_chunk, chunks)
        
    return sum(counts)

def test_searches():
    arr = [random.randint(0, 100) for _ in range(1000)]
    arr.append(999) # ensure target exists
    target = 999
    seq_idx = sequential_search(arr, target)
    par_idx = parallel_search(arr, target)
    assert arr[seq_idx] == target, "Sequential search failed"
    assert arr[par_idx] == target, "Parallel search failed"
    assert challenge_parallel_count([1, 2, 2, 3, 2], 2) == 3, "Parallel count failed"
    print("All tests passed.")

if __name__ == "__main__":
    print("Parallel Search Execution\\n" + "-"*30)
    test_searches()
