"""
Automation Script Optimization

===============================================================================
Learning Objectives:
1. Understand the importance of optimizing automation scripts in Python.
2. Identify common bottlenecks in file I/O, data processing, and network requests.
3. Apply multiprocessing, multithreading, and asyncio for concurrent execution.
4. Utilize profiling tools (`cProfile`, `timeit`) to measure and improve performance.
5. Implement memory-efficient data structures and generators.

Concept Explanation:
Automation scripts often start as simple sequential tasks but can quickly become 
slow and resource-intensive as the scale of data or the number of operations increases.
Script optimization involves improving execution time (CPU optimization) and 
reducing resource usage (Memory optimization).

Common Optimization Techniques:
- **I/O Bound Tasks**: Network requests, reading/writing files, database queries. 
  Best optimized using `asyncio` or `threading` (Multithreading).
- **CPU Bound Tasks**: Heavy computations, image processing, complex algorithms. 
  Best optimized using `multiprocessing` to bypass the Global Interpreter Lock (GIL).
- **Algorithmic Optimization**: Using more efficient data structures (e.g., sets 
  for lookups instead of lists) and better algorithms (e.g., O(1) vs O(N)).
- **Memory Optimization**: Using generators (`yield`) instead of lists to handle 
  large datasets lazily.

Industry Use Cases:
- Large-scale log parsing and log aggregation.
- High-throughput web scraping and data extraction pipelines.
- Automating infrastructure deployments where concurrent API calls are needed.
===============================================================================
"""

import time
import timeit
import cProfile
from typing import List, Iterator, Callable, Any
import concurrent.futures
import threading

# =============================================================================
# 1. Basic vs. Optimized Approach (Algorithmic & Data Structure Optimization)
# =============================================================================

def find_duplicates_unoptimized(items: List[int]) -> List[int]:
    """
    Find duplicates in a list using an unoptimized O(N^2) approach.
    """
    duplicates = []
    for i in range(len(items)):
        if items[i] in items[i+1:] and items[i] not in duplicates:
            duplicates.append(items[i])
    return duplicates

def find_duplicates_optimized(items: List[int]) -> List[int]:
    """
    Find duplicates in a list using a set. O(N) time complexity.
    """
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


# =============================================================================
# 2. Memory Optimization with Generators
# =============================================================================

def process_large_file_unoptimized(file_path: str) -> List[str]:
    """Reads the entire file into memory at once."""
    with open(file_path, 'r') as f:
        # If file is huge, this list will consume massive RAM.
        lines = f.readlines()
        return [line.strip().upper() for line in lines]

def process_large_file_optimized(file_path: str) -> Iterator[str]:
    """Reads the file line-by-line lazily using a generator."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip().upper()


# =============================================================================
# 3. Concurrent Execution (I/O Bound and CPU Bound)
# =============================================================================

def io_bound_task(task_id: int) -> str:
    """Simulates an I/O bound task like a network request."""
    time.sleep(0.5) # Simulate latency
    return f"Task {task_id} completed."

def run_sequential() -> None:
    """Runs I/O bound tasks sequentially."""
    for i in range(5):
        io_bound_task(i)

def run_threaded() -> None:
    """Runs I/O bound tasks using ThreadPoolExecutor."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(io_bound_task, range(5))


# =============================================================================
# 4. Profiling Tools
# =============================================================================

def profile_execution(func: Callable, *args: Any, **kwargs: Any) -> None:
    """Profiles a function using cProfile."""
    profiler = cProfile.Profile()
    profiler.enable()
    func(*args, **kwargs)
    profiler.disable()
    profiler.print_stats(sort='cumulative')


# =============================================================================
# Main Execution and Tests
# =============================================================================

if __name__ == "__main__":
    print("--- 1. Algorithmic Optimization ---")
    data = [1, 2, 3, 4, 5, 2, 6, 7, 3] * 1000
    
    # Measure unoptimized
    start_time = time.time()
    find_duplicates_unoptimized(data)
    print(f"Unoptimized time: {time.time() - start_time:.4f} seconds")
    
    # Measure optimized
    start_time = time.time()
    find_duplicates_optimized(data)
    print(f"Optimized time: {time.time() - start_time:.4f} seconds")
    
    # Verify correctness
    assert set(find_duplicates_unoptimized([1, 2, 3, 2, 4, 3])) == {2, 3}
    assert set(find_duplicates_optimized([1, 2, 3, 2, 4, 3])) == {2, 3}
    print("Optimization assertions passed.\n")

    print("--- 2. Concurrency Optimization (I/O Bound) ---")
    print("Running sequential...")
    start_time = time.time()
    run_sequential()
    print(f"Sequential time: {time.time() - start_time:.4f} seconds")
    
    print("Running threaded...")
    start_time = time.time()
    run_threaded()
    print(f"Threaded time: {time.time() - start_time:.4f} seconds")
    print("Notice the significant speedup when using threads for I/O tasks.\n")
    
    print("--- 3. Profiling Example ---")
    print("Profiling the optimized duplicate finder (first 5 stats):")
    # Only printing the first few lines of profile normally, but cProfile prints to stdout
    profile_execution(find_duplicates_optimized, data)

"""
===============================================================================
Interview Challenge:
You are given a script that reads 1 million log entries from a file, parses
the timestamps, and calculates the number of requests per second. The script is
currently taking 5 minutes to run and using 4GB of RAM. 

How would you optimize this script? Provide pseudo-code or Python code demonstrating
your approach.

Hint: Consider generators for reading the file, `collections.Counter` for counting,
and potentially multiprocessing if parsing is CPU-heavy.
===============================================================================
"""
