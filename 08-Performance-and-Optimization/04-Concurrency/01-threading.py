"""
Concurrency: Threading and the GIL

Learning Objectives:
1. Understand the difference between IO-bound and CPU-bound tasks.
2. Learn how to use Python's `threading` module.
3. Understand the Global Interpreter Lock (GIL) and its limitations.
4. Measure the effect of threading on different workloads.

Concept Explanation:
Concurrency is dealing with multiple things at once. The `threading` module allows 
multiple threads of execution within a single process. However, CPython uses a 
Global Interpreter Lock (GIL) which prevents multiple native threads from executing 
Python bytecodes simultaneously. Therefore, threading in Python is excellent for 
I/O-bound tasks (network requests, file reading) where threads wait, but it provides 
NO speedup (and can actually be slower) for pure CPU-bound math operations.
"""

import threading
import time
from typing import List

# --- Basic Implementation ---
def io_bound_task(task_id: int):
    """Simulate downloading a file or waiting for network."""
    # time.sleep releases the GIL!
    time.sleep(1)
    return task_id

def cpu_bound_task(n: int):
    """Simulate heavy computation."""
    count = 0
    for i in range(n):
        count += i
    return count

# --- Intermediate Implementation ---
def run_sequential_io(n_tasks: int) -> float:
    start = time.perf_counter()
    for i in range(n_tasks):
        io_bound_task(i)
    return time.perf_counter() - start

def run_threaded_io(n_tasks: int) -> float:
    start = time.perf_counter()
    threads = []
    for i in range(n_tasks):
        t = threading.Thread(target=io_bound_task, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join() # Wait for all threads to finish
        
    return time.perf_counter() - start

# --- Advanced Implementation / Performance Analysis ---
def run_sequential_cpu(n: int, loops: int) -> float:
    start = time.perf_counter()
    for _ in range(loops):
        cpu_bound_task(n)
    return time.perf_counter() - start

def run_threaded_cpu(n: int, loops: int) -> float:
    start = time.perf_counter()
    threads = []
    for _ in range(loops):
        t = threading.Thread(target=cpu_bound_task, args=(n,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    return time.perf_counter() - start

def compare_performance():
    print("1. I/O-Bound Workload (Waiting/Sleeping)")
    n_io = 4
    t_seq_io = run_sequential_io(n_io)
    t_thr_io = run_threaded_io(n_io)
    print(f"  Sequential: {t_seq_io:.2f}s")
    print(f"  Threaded:   {t_thr_io:.2f}s (Speedup! Threads wait concurrently)")
    
    print("\n2. CPU-Bound Workload (Math/Loops)")
    n_cpu = 5_000_000
    loops = 4
    t_seq_cpu = run_sequential_cpu(n_cpu, loops)
    t_thr_cpu = run_threaded_cpu(n_cpu, loops)
    print(f"  Sequential: {t_seq_cpu:.2f}s")
    print(f"  Threaded:   {t_thr_cpu:.2f}s (NO Speedup! GIL limits to 1 CPU core)")

# --- Edge Cases ---
def race_condition_example():
    """Demonstrate why shared state in threads is dangerous."""
    counter = 0
    def increment():
        nonlocal counter
        for _ in range(100_000):
            # Not an atomic operation!
            counter += 1
            
    threads = [threading.Thread(target=increment) for _ in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"\n[Race Condition] Expected 400000, got: {counter}")

# --- Interview Challenge ---
"""
Challenge: How do you fix the race condition above?
Answer: Use a threading.Lock() to ensure only one thread modifies the counter at a time.
"""
def locked_increment_example():
    counter = 0
    lock = threading.Lock()
    def increment():
        nonlocal counter
        for _ in range(100_000):
            with lock:
                counter += 1
    # Note: Locks make threads much slower due to context switching overhead!

# --- Tests ---
def run_tests():
    assert cpu_bound_task(5) == 10
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Threading & GIL ---")
    compare_performance()
    race_condition_example()
    run_tests()
