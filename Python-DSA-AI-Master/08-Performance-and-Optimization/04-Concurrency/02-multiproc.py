"""
Concurrency: Multiprocessing

Learning Objectives:
1. Understand the `multiprocessing` module as a workaround for the GIL.
2. Create separate processes that run in parallel on multiple CPU cores.
3. Compare Inter-Process Communication (IPC) overhead to threading.
4. Use Pool for mapping functions across datasets.

Concept Explanation:
To truly utilize multiple CPU cores for CPU-bound tasks in Python, you must use
`multiprocessing`. This spawns entirely separate Python interpreter processes, each 
with its own memory space and its own GIL. Because memory is not shared, processes 
don't step on each other's toes, but passing data between them (IPC) requires 
serialization (pickling), which incurs an overhead cost.
"""

import multiprocessing
import time
import math
from typing import List

# --- Basic Implementation ---
def cpu_bound_task(n: int) -> int:
    """A heavy mathematical task."""
    count = 0
    for i in range(n):
        count += math.isqrt(i)
    return count

# --- Intermediate Implementation ---
def sequential_execution(data: List[int]) -> List[int]:
    """Process data one item at a time."""
    start = time.perf_counter()
    results = [cpu_bound_task(n) for n in data]
    elapsed = time.perf_counter() - start
    return results, elapsed

# --- Advanced Implementation / Performance Analysis ---
def parallel_execution_pool(data: List[int]) -> List[int]:
    """Process data in parallel using a Process Pool."""
    start = time.perf_counter()
    # Create a pool of workers matching the number of logical CPU cores
    with multiprocessing.Pool() as pool:
        # Map blocks until all processes finish
        results = pool.map(cpu_bound_task, data)
    elapsed = time.perf_counter() - start
    return results, elapsed

def compare_performance():
    # 4 tasks of 10 million iterations
    dataset = [10_000_000] * 4 
    
    print("Comparing CPU-bound workload...")
    
    _, t_seq = sequential_execution(dataset)
    print(f"Sequential Time:      {t_seq:.2f}s")
    
    # Protect entry point for multiprocessing in Windows
    _, t_par = parallel_execution_pool(dataset)
    print(f"Multiprocessing Time: {t_par:.2f}s")
    print(f"Speedup:              {t_seq/t_par:.2f}x")

# --- Edge Cases ---
def overhead_edge_case():
    """If the task is too small, IPC overhead makes multiprocessing slower!"""
    small_data = [10] * 1000
    _, t_seq = sequential_execution(small_data)
    _, t_par = parallel_execution_pool(small_data)
    
    print("\n[Overhead Edge Case: Small Tasks]")
    print(f"Sequential: {t_seq:.4f}s")
    print(f"Parallel:   {t_par:.4f}s")
    print("Parallel is slower because the cost of spawning processes and copying data exceeds the computation time!")

# --- Interview Challenge ---
"""
Challenge: How do you share state (like a counter) between Processes?
Answer: You cannot use normal variables. You must use multiprocessing.Value, 
multiprocessing.Array, or a Manager(), which handle the IPC locking under the hood.
"""
def shared_state_example():
    def increment(shared_counter, lock):
        with lock:
            shared_counter.value += 1

    counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    processes = [multiprocessing.Process(target=increment, args=(counter, lock)) for _ in range(5)]
    
    for p in processes: p.start()
    for p in processes: p.join()
    assert counter.value == 5

# --- Tests ---
def run_tests():
    assert cpu_bound_task(5) == 4 # isqrt(0)+isqrt(1)+isqrt(2)+isqrt(3)+isqrt(4) = 0+1+1+1+2 = 5
    shared_state_example()
    print("\nAll tests passed.")

if __name__ == '__main__':
    # Required for Windows compatibility with multiprocessing
    multiprocessing.freeze_support() 
    print("--- Performance Analysis: Multiprocessing ---")
    compare_performance()
    overhead_edge_case()
    run_tests()
