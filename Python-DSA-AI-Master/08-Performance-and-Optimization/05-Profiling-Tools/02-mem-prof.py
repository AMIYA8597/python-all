"""
Profiling Tools: Memory Profiler

Learning Objectives:
1. Understand line-by-line memory profiling.
2. Use the external `memory_profiler` library.
3. Visualize memory consumption over the lifespan of a function.
4. Identify which specific line causes memory spikes.

Concept Explanation:
While `tracemalloc` tracks block allocations, `memory_profiler` tracks the OS 
RSS (Resident Set Size) memory line-by-line. It is slower than normal execution 
but provides an incredibly detailed view of where RAM is consumed and released 
within a single function.

Requires: `pip install memory_profiler`
"""

# Try to import the profiler. If not installed, we'll mock it so the script runs.
try:
    from memory_profiler import profile
except ImportError:
    print("Warning: memory_profiler not installed. Profiling will be mocked.")
    def profile(func):
        return func

import time
from typing import List

# --- Basic Implementation ---
@profile
def create_large_lists() -> List[int]:
    """Function demonstrating memory growth and shrinkage."""
    print("Step 1: Creating array 1")
    arr1 = [1] * (10 ** 6)  # Approx 8MB
    time.sleep(0.1)
    
    print("Step 2: Creating array 2")
    arr2 = [2] * (2 * 10 ** 6) # Approx 16MB
    time.sleep(0.1)
    
    print("Step 3: Deleting array 1")
    del arr1
    time.sleep(0.1)
    
    return arr2

# --- Intermediate Implementation ---
# To run memory_profiler from the command line on this file:
# python -m memory_profiler 02-mem-prof.py

@profile
def memory_leak_simulation() -> None:
    """Simulate a subtle memory leak."""
    cache = []
    for i in range(5):
        # Local data that should be garbage collected
        local_data = [i] * 100_000
        # Oops, we append it to an external cache! Memory leak!
        cache.append(local_data)
        
# --- Advanced Implementation / Performance Analysis ---
"""
Output of memory_profiler looks like this:
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    28     40.0 MiB     40.0 MiB           1   @profile
    29                                         def create_large_lists():
    ...
    31     47.6 MiB      7.6 MiB           1       arr1 = [1] * (10 ** 6)
    ...
    35     62.9 MiB     15.3 MiB           1       arr2 = [2] * (2 * 10 ** 6)
    ...
    38     55.3 MiB     -7.6 MiB           1       del arr1
    
Increment column is the most important: it shows how much memory that specific 
line ADDED (+) or FREED (-).
"""

# --- Edge Cases ---
def garbage_collection_delay():
    """
    Python's Garbage Collector doesn't immediately return memory to the OS.
    If you `del` a list, `memory_profiler` might not show an immediate drop 
    in RSS memory because Python keeps the arena allocated for future use.
    Forcing `gc.collect()` sometimes clarifies the profiling output.
    """
    import gc
    gc.collect()

# --- Interview Challenge ---
"""
Challenge: What is the difference between `tracemalloc` and `memory_profiler`?
Answer: `tracemalloc` tracks Python's internal memory allocations (mallocs).
`memory_profiler` queries the Operating System for the process's total RSS memory 
usage at each line. Therefore, `memory_profiler` includes overhead from C extensions 
and the Python interpreter itself.
"""

# --- Tests ---
def run_tests():
    res = create_large_lists()
    assert len(res) == 2000000
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: memory_profiler ---")
    create_large_lists()
    memory_leak_simulation()
    run_tests()
    
    print("\nTip: To see the actual line-by-line profile, run:")
    print("pip install memory_profiler")
    print("python -m memory_profiler 02-mem-prof.py")
