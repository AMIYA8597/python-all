"""
# ==============================================================================
# LABORATORY: CONCURRENCY MODELS (MULTIPROCESSING VS THREADING VS ASYNCIO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have reached the absolute peak of the Python curriculum. 
# You understand $O(N \log N)$ sorts, Graph traversals, Dynamic Programming, 
# and Computational Geometry.
#
# But when you deploy your algorithms in a production environment (like Google 
# or Amazon servers), the absolute bottleneck is no longer Time Complexity. 
# It is Concurrency.
#
# Python provides three entirely different mathematical paradigms for running 
# code "at the same time". Choosing the wrong one will cause your $O(N)$ algorithm 
# to run 100x slower.
#
# 1. MULTIPROCESSING (`multiprocessing` library)
#    - Spawns completely separate Operating System `.exe` processes.
#    - Completely bypasses the Python GIL (Global Interpreter Lock).
#    - True mathematical parallelism across multiple physical CPU cores!
#    - BEST FOR: CPU-Bound Algorithms (Matrix Multiplication, Parallel Sorting).
#
# 2. MULTITHREADING (`threading` library)
#    - Spawns multiple threads INSIDE a single process.
#    - Locked by the GIL! Only one thread can execute Python bytecode at a time.
#    - FAKE parallelism. It uses rapid context-switching.
#    - BEST FOR: I/O-Bound Tasks (Reading gigabytes from a Hard Drive). While 
#      one thread waits for the physical spinning disk, the GIL unlocks and lets 
#      another thread run!
#
# 3. ASYNCHRONOUS I/O (`asyncio` library)
#    - A single thread running an Event Loop.
#    - FAKE parallelism, but extremely lightweight. No OS context-switching overhead!
#    - BEST FOR: Massive Network Concurrency. (Scraping 10,000 algorithmic datasets 
#      from an API simultaneously).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Prove the CPU-bound GIL bottleneck in multithreading.
# - Prove the true parallelism of multiprocessing.
# - Master the architectural decision tree for production deployment.
#
# ==============================================================================
"""

import time
import math
import threading
import multiprocessing
import asyncio

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CPU-BOUND WORKLOAD (MATRIX / MATH HEAVY)
# ==============================================================================
def cpu_bound_task(task_id: int, iterations: int):
    """
    A purely mathematical task. No hard drive, no network. 100% CPU usage.
    """
    result = 0
    for i in range(iterations):
        result += math.sin(i) * math.cos(i)
    return result


def benchmark_single_core(iterations: int, tasks: int):
    start = time.time()
    for i in range(tasks):
        cpu_bound_task(i, iterations)
    return time.time() - start


def benchmark_threading(iterations: int, tasks: int):
    """
    Attempts to run the CPU task using Python Threads.
    SPOILER: The GIL will absolutely destroy performance.
    """
    start = time.time()
    threads = []
    
    for i in range(tasks):
        t = threading.Thread(target=cpu_bound_task, args=(i, iterations))
        threads.append(t)
        t.start()
        
    # Wait for all threads to finish
    for t in threads:
        t.join()
        
    return time.time() - start


def benchmark_multiprocessing(iterations: int, tasks: int):
    """
    Runs the CPU task using true OS-level processes, bypassing the GIL.
    """
    start = time.time()
    processes = []
    
    for i in range(tasks):
        p = multiprocessing.Process(target=cpu_bound_task, args=(i, iterations))
        processes.append(p)
        p.start()
        
    # Wait for all processes to finish
    for p in processes:
        p.join()
        
    return time.time() - start


# ==============================================================================
# 4. THE I/O-BOUND WORKLOAD (NETWORK / SLEEP HEAVY)
# ==============================================================================
def io_bound_task(task_id: int, delay: float):
    """
    Simulates a network request or hard drive read.
    0% CPU usage, 100% waiting time.
    """
    time.sleep(delay)


async def async_io_task(task_id: int, delay: float):
    """
    The AsyncIO version of the I/O task.
    """
    await asyncio.sleep(delay)


def benchmark_io_threading(tasks: int, delay: float):
    start = time.time()
    threads = []
    for i in range(tasks):
        t = threading.Thread(target=io_bound_task, args=(i, delay))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start


async def benchmark_io_asyncio(tasks: int, delay: float):
    start = time.time()
    # Schedule all tasks simultaneously on the single-thread event loop!
    coroutines = [async_io_task(i, delay) for i in range(tasks)]
    await asyncio.gather(*coroutines)
    return time.time() - start


def demonstrate_concurrency():
    section_header("Algorithm: CPU-Bound Execution (Math Heavy)")
    
    iterations = 5_000_000
    tasks = 4
    
    print(f"Executing {tasks} massive mathematical tasks...")
    
    single_time = benchmark_single_core(iterations, tasks)
    print(f"1. Single Core (Sequential)  : {single_time:.4f} seconds")
    
    thread_time = benchmark_threading(iterations, tasks)
    print(f"2. Threading (GIL Blocked)   : {thread_time:.4f} seconds")
    
    multi_time = benchmark_multiprocessing(iterations, tasks)
    print(f"3. Multiprocessing (True)    : {multi_time:.4f} seconds")
    
    print("\nObservation:")
    print("Threading was SLOWER than running sequentially! The GIL forced the threads")
    print("to wait in line, and the context-switching overhead ruined the CPU caches.")
    print("Multiprocessing bypassed the GIL and achieved true parallel speedup!")
    
    section_header("Algorithm: I/O-Bound Execution (Network Heavy)")
    
    io_tasks = 100
    delay = 0.1 # 100ms ping delay
    
    print(f"Executing {io_tasks} network requests with 100ms delay...")
    print(f"Sequential time would be: {io_tasks * delay:.1f} seconds")
    
    io_thread = benchmark_io_threading(io_tasks, delay)
    print(f"\n1. Threading   : {io_thread:.4f} seconds")
    
    io_async = asyncio.run(benchmark_io_asyncio(io_tasks, delay))
    print(f"2. AsyncIO     : {io_async:.4f} seconds")
    
    print("\nObservation:")
    print("Threading is incredibly fast for I/O! The GIL unlocks instantly when ")
    print("a thread hits `time.sleep()` or a network socket.")
    print("AsyncIO is mathematically the fastest because it avoids the RAM overhead ")
    print("of spawning 100 physical OS threads, multiplexing everything instantly ")
    print("on a single core's event loop!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. If AsyncIO is so fast, why don't we use it for Parallel Merge Sort?
   Answer: AsyncIO runs on a SINGLE thread. It is completely fake concurrency! It only switches tasks when a task hits an `await` keyword (which implies waiting for an external I/O blocker like a network). A Merge Sort algorithm is 100% CPU-bound. It never hits an `await`! If you try to run Merge Sort in AsyncIO, the first task will completely lock up the single thread, preventing any other tasks from running until it finishes. It will run perfectly sequentially and provide 0% speedup.

2. Why did Threading run SLOWER than Single-Core for the CPU task?
   Answer: The Global Interpreter Lock (GIL). Only one thread can execute Python code at a time. The Operating System tries to be fair, so it pauses Thread A (Context Switch), gives the GIL to Thread B, pauses Thread B, gives the GIL to Thread C... 
   This constant pausing and swapping flushes the physical L1/L2 caches on the CPU hardware, destroying performance. Since they aren't running in parallel anyway, running them sequentially is mathematically superior because it avoids the cache-flush overhead!

3. Final Capstone Summary: When to use which?
   Answer: 
   - Rule 1: Are you sorting arrays, doing matrix math, or running AI Neural Networks? (CPU-Bound). USE MULTIPROCESSING.
   - Rule 2: Are you scraping 10,000 URLs, querying APIs, or writing to disk? (I/O-Bound). USE ASYNCIO (or Threading if the library doesn't support async).
   - Rule 3: Python is fundamentally designed as a high-level orchestration language. Let Python handle the AsyncIO, and offload the intense CPU math to C++ bindings (like NumPy/Pandas), which drop the GIL automatically!
"""

if __name__ == "__main__":
    # In Windows, multiprocessing MUST be wrapped in this check
    demonstrate_concurrency()
    print("\n[SUCCESS] Laboratory: Concurrency Models Completed.")
    print("\n[CAPSTONE] THE PYTHON CURRICULUM IS FULLY COMPLETED.")
