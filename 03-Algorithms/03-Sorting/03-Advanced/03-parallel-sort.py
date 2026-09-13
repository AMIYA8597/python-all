"""
# ==============================================================================
# LABORATORY: PARALLEL SORTING (MULTIPROCESSING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Modern CPUs have 8, 16, or even 64 cores. If you run a standard O(N log N) 
# Merge Sort, it will only use ONE core, leaving 99% of your CPU completely idle.
#
# How do we harness the full power of the hardware? We use Parallel Sorting.
#
# Merge Sort and Quick Sort are "Divide and Conquer" algorithms. When Merge Sort 
# splits the array into a Left half and a Right half, sorting the Left half has 
# absolutely nothing to do with the Right half. They are mathematically independent!
#
# This means we can hand the Left half to CPU Core 1, and the Right half to 
# CPU Core 2. They will sort them simultaneously, cutting the time in half!
#
# WARNING: Python has a Global Interpreter Lock (GIL) which prevents true 
# CPU parallelism in `threading`. To actually use multiple CPU cores in Python 
# for math-heavy tasks, we must use `multiprocessing`.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how Divide & Conquer maps perfectly to Parallel computing.
# - Understand why the GIL ruins standard Python Threading.
# - Implement a parallelized Merge Sort using `ProcessPoolExecutor`.
# - Understand the overhead of inter-process communication.
#
# ==============================================================================
"""

import math
import concurrent.futures
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE STANDARD MERGE SUBROUTINE
# ==============================================================================
def merge(left: List[int], right: List[int]) -> List[int]:
    """Standard sequential merge of two sorted arrays."""
    merged = []
    i = 0
    j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    while i < len(left):
        merged.append(left[i])
        i += 1
        
    while j < len(right):
        merged.append(right[j])
        j += 1
        
    return merged

def standard_merge_sort(arr: List[int]) -> List[int]:
    """Standard recursive merge sort."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = standard_merge_sort(arr[:mid])
    right = standard_merge_sort(arr[mid:])
    return merge(left, right)


# ==============================================================================
# 4. PARALLEL MERGE SORT IMPLEMENTATION
# ==============================================================================
def parallel_merge_sort(arr: List[int], depth: int = 0, max_depth: int = 2) -> List[int]:
    """
    Sorts an array using multiple CPU cores.
    
    `max_depth` controls how many times we split into a new Process.
    If we have an 8-core CPU, we want to split 3 times (2^3 = 8 processes).
    If we keep creating processes all the way down to arrays of size 1, 
    the OS will crash trying to manage 1 Million processes!
    """
    # 1. Base Cases
    if len(arr) <= 1:
        return arr
        
    # 2. Parallelism Limiter (The "Granularity" Check)
    # If we have reached our max depth (all CPU cores are currently busy),
    # just fall back to standard, single-core Merge Sort to finish the job locally.
    if depth >= max_depth:
        return standard_merge_sort(arr)
        
    # 3. Parallel Split
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Use ProcessPoolExecutor to spawn completely separate Python processes,
    # bypassing the Global Interpreter Lock (GIL).
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # We submit both halves to the CPU cores simultaneously
        future_left = executor.submit(parallel_merge_sort, left_half, depth + 1, max_depth)
        future_right = executor.submit(parallel_merge_sort, right_half, depth + 1, max_depth)
        
        # We wait for both CPU cores to finish their work
        sorted_left = future_left.result()
        sorted_right = future_right.result()
        
    # 4. Sequential Merge
    # Once the two cores hand us back their sorted halves, we must merge them.
    # Note: The merge step itself is usually done sequentially on the main core.
    return merge(sorted_left, sorted_right)


def demonstrate_parallel_sort():
    section_header("Algorithm: Parallel Merge Sort")
    
    # Generate a moderately sized array (16 elements for console output clarity)
    # In reality, Parallel Sort is only used for arrays of 10,000,000+ elements.
    import random
    arr = [random.randint(1, 100) for _ in range(16)]
    
    print(f"Initial Unsorted Array:\n{arr}\n")
    
    print("Executing Parallel Merge Sort...")
    print("Spawning ProcessPools to handle independent halves...")
    
    sorted_arr = parallel_merge_sort(arr)
    
    print(f"\nFinal Sorted Array:\n{sorted_arr}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we implement a `max_depth` to stop parallelism? Why not parallelize everything?
   Answer: Spawning an OS Process is incredibly expensive (it takes milliseconds and megabytes of RAM). If you spawn 100,000 processes to sort tiny arrays of size 2, the overhead of creating the processes will be 1000x slower than just sorting them on a single core. You only spawn processes equal to the number of physical cores you have on the CPU (e.g., 8 processes for an 8-core CPU), and let them handle massive chunks sequentially.

2. Why must we use `multiprocessing` instead of `threading` in Python for sorting?
   Answer: The Global Interpreter Lock (GIL). CPython has a mutex lock that prevents multiple native threads from executing Python bytecodes at once. Even if you spawn 100 threads, only 1 thread can run at a time, resulting in zero performance gain for CPU-bound tasks like sorting. `multiprocessing` bypasses this by spinning up entirely separate Python interpreters with their own memory spaces and their own GILs.

3. Does Parallelizing a sort change its Big-O Time Complexity?
   Answer: Theoretically, yes! In the PRAM (Parallel Random Access Machine) model, algorithms are evaluated on Time $O(T)$ and Work $O(W)$. If you have $N$ processors, a Parallel Merge Sort can complete in $O(\\log^2 N)$ time! However, because you are physically limited by your hardware (e.g. exactly 8 cores), the Big-O for a fixed number of cores $P$ remains $O((N \\log N) / P)$, which is mathematically still $O(N \\log N)$.
"""

if __name__ == "__main__":
    # In Windows, multiprocessing MUST be protected by __main__ block
    demonstrate_parallel_sort()
    print("\n[SUCCESS] Laboratory: Parallel Sorting Completed.")
