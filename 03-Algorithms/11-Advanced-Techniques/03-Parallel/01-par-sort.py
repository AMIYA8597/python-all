"""
# ==============================================================================
# LABORATORY: PARALLEL ALGORITHMS (MULTI-CORE MERGE SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Moore's Law (the doubling of CPU clock speeds every two years) mathematically 
# died around 2005 due to quantum tunneling and thermal limits. A modern CPU core 
# runs at roughly the exact same 3.5 GHz as a CPU from 15 years ago.
#
# How did computers keep getting faster? MULTI-CORE PROCESSING.
# A modern CPU doesn't have one 10 GHz core; it has sixteen 3 GHz cores!
#
# Standard Merge Sort is $O(N \log N)$. If you have 16 CPU cores, standard Merge 
# Sort only uses ONE core. The other 15 cores sit idle at 0% utilization.
#
# The Solution: Parallel Merge Sort.
# Merge Sort is a Divide and Conquer algorithm. The left half of the array has 
# absolutely NO mathematical dependency on the right half of the array!
# We can send the Left Half to CPU Core 1, and the Right Half to CPU Core 2. 
# They sort them simultaneously in strict parallel! We then take the results and 
# run a standard $O(N)$ merge.
# 
# Python Warning: The Global Interpreter Lock (GIL).
# If you try to use the `threading` library in Python for CPU-bound tasks, it 
# will run SLOWER. The GIL physically prevents multiple Python threads from 
# executing bytecodes simultaneously to protect memory integrity. 
# To achieve true parallelism in Python, you MUST use the `multiprocessing` library, 
# which bypasses the GIL by spawning entirely separate Operating System processes!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the death of Moore's law and the necessity of multi-core logic.
# - Understand why Python `threading` fails for CPU-bound tasks (The GIL).
# - Implement true Parallel Merge Sort using `multiprocessing.Pool`.
#
# ==============================================================================
"""

import time
import random
import multiprocessing
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD (SINGLE-CORE) MERGE SORT
# ==============================================================================
def standard_merge(left: List[int], right: List[int]) -> List[int]:
    """
    Standard O(N) array merge.
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # Append the remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def standard_merge_sort(arr: List[int]) -> List[int]:
    """
    Standard O(N log N) Merge Sort. Runs entirely on a single CPU core.
    """
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = standard_merge_sort(arr[:mid])
    right = standard_merge_sort(arr[mid:])
    
    return standard_merge(left, right)


# ==============================================================================
# 4. PARALLEL (MULTI-CORE) MERGE SORT
# ==============================================================================
def parallel_merge_sort(arr: List[int], num_processes: int = None) -> List[int]:
    """
    True Parallel Merge Sort bypassing the Python GIL.
    Chunks the array into pieces based on the number of CPU cores available.
    Sorts the chunks simultaneously across different OS processes.
    Merges the chunks back together sequentially.
    """
    if len(arr) <= 1:
        return arr
        
    # Auto-detect available CPU cores if not provided
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    # If the array is too small, the overhead of spinning up OS processes will 
    # actually make it run slower! Fall back to single-core.
    if len(arr) < 10000 or num_processes <= 1:
        return standard_merge_sort(arr)
        
    # 1. DIVIDE THE DATA (Chunking)
    # Break the massive array into chunks, one for each CPU core.
    chunk_size = math.ceil(len(arr) / num_processes)
    chunks = [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    # 2. PARALLEL PROCESSING (Bypassing the GIL)
    # `multiprocessing.Pool` creates entirely separate Python processes!
    # `pool.map` automatically distributes the chunks to the different cores, 
    # runs `standard_merge_sort` on them simultaneously, and waits for all of 
    # them to finish!
    with multiprocessing.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(standard_merge_sort, chunks)
        
    # 3. SEQUENTIAL MERGE
    # The cores have finished sorting their independent chunks!
    # Now we must physically merge them back together.
    # (Since we have K chunks, we iteratively merge them).
    while len(sorted_chunks) > 1:
        next_level = []
        
        # Merge pairs of chunks
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged = standard_merge(sorted_chunks[i], sorted_chunks[i + 1])
                next_level.append(merged)
            else:
                # Odd chunk out, just carry it over
                next_level.append(sorted_chunks[i])
                
        sorted_chunks = next_level
        
    return sorted_chunks[0]


import math # Required for chunk ceiling calculation

def demonstrate_parallel_sort():
    section_header("Algorithm: Multi-Core Parallel Merge Sort")
    
    # Generate a massive array of random integers
    n_elements = 1_000_000
    print(f"Generating {n_elements:,} random elements...")
    arr = [random.randint(0, 10_000_000) for _ in range(n_elements)]
    
    print(f"Detected CPU Cores: {multiprocessing.cpu_count()}")
    
    # 1. Single Core Benchmark
    print("\nExecuting Single-Core Merge Sort...")
    start_time = time.time()
    arr_sorted_single = standard_merge_sort(arr)
    single_duration = time.time() - start_time
    print(f"Time: {single_duration:.4f} seconds")
    
    # 2. Multi-Core Benchmark
    print("\nExecuting Multi-Core Parallel Merge Sort (Bypassing GIL)...")
    start_time = time.time()
    arr_sorted_multi = parallel_merge_sort(arr)
    multi_duration = time.time() - start_time
    print(f"Time: {multi_duration:.4f} seconds")
    
    # Verify correctness
    print("\nVerification:")
    print(f"Arrays mathematically match? {arr_sorted_single == arr_sorted_multi}")
    
    if multi_duration < single_duration:
        speedup = single_duration / multi_duration
        print(f"Multi-Core was {speedup:.2f}x faster!")
    else:
        print("Note: If Multi-Core was slower, it's due to the massive overhead of ")
        print("Python spinning up OS processes and serializing data across memory ")
        print("boundaries (Pickling). In lower-level languages like C++ or Rust, ")
        print("parallelism has almost zero overhead!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Global Interpreter Lock (GIL) in Python?
   Answer: The GIL is a mutex (lock) embedded deep inside the CPython interpreter. It physically guarantees that ONLY ONE Python thread can execute Python bytecodes at any given moment. This was designed in the 1990s to prevent memory corruption and race conditions with Python's Reference Counting garbage collector. Because of the GIL, if you create 16 `threading.Thread` objects to do heavy CPU math, they will NOT run on 16 cores. They will line up on ONE core and take turns executing, actually running SLOWER than a single thread due to context-switching overhead!

2. How does `multiprocessing` bypass the GIL?
   Answer: The `multiprocessing` library does not use threads. It literally asks the Operating System to boot up completely separate Python.exe instances! Because they are entirely separate programs, each process has its own independent memory space, its own garbage collector, and its own GIL! The OS seamlessly schedules these different processes across all 16 physical CPU cores, achieving true mathematical parallelism.

3. Why is there a performance penalty (overhead) for `multiprocessing`?
   Answer: Because the processes have separate memory spaces, they cannot directly access the massive unsorted array in RAM! The master process must physically copy (Serialize / Pickle) the chunk of data, pipe it through the OS to the worker process, wait for it to sort, and then physical copy (Unpickle) the sorted data back! This Inter-Process Communication (IPC) is extremely slow. If the array is too small, the time spent serializing the data will completely destroy the time saved by sorting in parallel!
"""

if __name__ == "__main__":
    # In Windows, multiprocessing MUST be wrapped in this check to prevent 
    # recursive infinite fork bombs!
    demonstrate_parallel_sort()
    print("\n[SUCCESS] Laboratory: Parallel Merge Sort Completed.")
