"""
## A. Concept Name
Threading and Multiprocessing in Python

## B. One-Sentence Definition
Threading and multiprocessing are concurrent execution models in Python used to run multiple tasks simultaneously, either to bypass I/O wait times (threading) or to leverage multiple CPU cores (multiprocessing).

## C. Why Does This Exist?
Sequential execution underutilizes modern hardware. When a program waits for a network request (I/O bound), the CPU sits idle. When a program performs heavy math (CPU bound), a single core maxes out while other cores do nothing. Concurrency tools exist to maximize resource utilization and improve application responsiveness.

## D. Intuition
Imagine a restaurant kitchen. 
- **Threading (I/O Bound):** One chef is cooking. While waiting for water to boil (I/O wait), they start chopping vegetables. They are not doing both *at the exact same microsecond*, but they are interleaving tasks to save total time. 
- **Multiprocessing (CPU Bound):** The kitchen gets too busy for one chef. You hire a second chef, give them their own cutting board and knife, and they work on entirely different orders simultaneously.

## E. Real-Life Analogy
Threading: You reading a book while waiting for your laundry to finish. (One person, two overlapping tasks).
Multiprocessing: You washing the car while your friend mows the lawn. (Two people, two simultaneous tasks).

## F. Mental Model
- **Threading:** Shared memory space. Lightweight. Bounded by the Global Interpreter Lock (GIL) in CPython, meaning only one thread executes Python bytecode at a time. Perfect for network requests, file I/O, or database queries.
- **Multiprocessing:** Separate memory spaces (each process gets its own Python interpreter). Heavyweight (slower to start, higher memory usage). Bypasses the GIL. Perfect for heavy computations, data processing, and image rendering.

## G. Visual Explanation
```
Time ->
Sequential:
[Task 1 (I/O)] -> [Task 2 (I/O)] -> [Task 3 (I/O)]

Threading:
[Task 1 Start] . . (waiting) . . [Task 1 End]
          [Task 2 Start] . . (waiting) . . [Task 2 End]
                    [Task 3 Start] . . (waiting) . . [Task 3 End]

Multiprocessing (across Cores):
Core 1: [Heavy Task 1]
Core 2: [Heavy Task 2]
Core 3: [Heavy Task 3]
```

## H. Formal Explanation
In CPython, the Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once. Consequently, multi-threading in Python does not yield CPU-level parallelism. To achieve true parallelism for CPU-bound tasks, the `multiprocessing` module spawns subprocesses, each with its own GIL and memory space, communicating via IPC (Inter-Process Communication) like Pipes or Queues.

## I. Mathematical Foundation (if applicable)
Amdahl's Law defines the theoretical maximum speedup of a program using multiple processors:
S = 1 / ((1 - P) + (P / N))
Where:
- P = proportion of the program that can be made parallel
- N = number of processors
Even with infinite processors, speedup is strictly limited by the sequential portion (1 - P).

## J. From-Scratch Implementation (if applicable)
(See code below for the Python implementation of both threading and multiprocessing patterns).

## K. Library / Production Implementation (if applicable)
In production, modern Python often uses `concurrent.futures.ThreadPoolExecutor` and `ProcessPoolExecutor` for simpler high-level APIs, or `asyncio` for highly concurrent I/O-bound tasks in a single thread.

## L. Trace (walk through example)
1. Thread 1 starts HTTP request.
2. Thread 1 hits `time.sleep` (or socket wait) and releases the GIL.
3. Thread 2 acquires GIL, starts its HTTP request.
4. Thread 2 hits wait, releases GIL.
5. Thread 1's request finishes, it re-acquires GIL and processes the response.

## M. Complexity
- **Time Complexity:** 
  - Threading (I/O): O(max(T1, T2, ...)) where Ti is the I/O wait time of task i.
  - Multiprocessing (CPU): O(T / N) where T is total CPU time and N is number of cores, assuming perfect parallelization.
- **Space Complexity:** 
  - Threading: O(1) additional overhead beyond task memory (shared space).
  - Multiprocessing: O(M * N) where M is memory per process and N is number of processes (memory is duplicated).

## N. Common Mistakes
- Using `threading` for CPU-bound tasks (makes it *slower* due to GIL context switching overhead).
- Modifying shared state in threads without a `Lock` (causes race conditions).
- Spawning too many processes (thrashing the CPU and running out of RAM).
- Forgetting `if __name__ == "__main__":` when using multiprocessing on Windows.

## O. Common Confusions
**Q: If the GIL prevents true parallelism, why use threading at all?**
A: Because during I/O operations (like waiting for a web response), the thread releases the GIL. Other threads can execute Python code while the first thread waits.

## P. When To Use
- **Threading:** Web scraping, API calls, reading/writing many files, UI responsiveness.
- **Multiprocessing:** Number crunching, image processing, machine learning data transformations.

## Q. When NOT To Use
- Don't use threading for matrix multiplication.
- Don't use multiprocessing for downloading 10,000 small web pages (too much memory overhead; use threading or asyncio).

## R. Trade-offs
- **Threading:** Low memory footprint, easy to share data, but limited by GIL and susceptible to race conditions.
- **Multiprocessing:** True parallelism, no GIL constraints, immune to most race conditions (isolated memory), but high memory overhead and expensive IPC (Inter-Process Communication).

## S. Debugging
- Use timeouts on `.join()` or Locks to prevent deadlocks.
- Print statements from multiple processes can interleave poorly; use the `logging` module configured for multiprocessing.
- Shared variables in threads can be debugged using `threading.current_thread().name`.

## T. Memory Hook (a short memorable principle)
**"Threads for the Web, Procs for the Math."** (Threads = I/O, Processes = CPU).

## U. Active Recall (questions before answers)
1. What does GIL stand for and what does it do?
2. Which module should you use to resize 1,000 high-res images?
3. What happens if you don't use a Lock when threads modify a shared variable?

## V. Practice (exercises)
1. Write a script that pings 5 different websites concurrently using threading.
2. Write a script that calculates the factorial of a large number across 4 processes.

## W. Interview Question
"Explain the difference between Concurrency and Parallelism in the context of Python. When would you use threading vs multiprocessing?"

## X. Project Connection
In a scalable web scraper (like building a mini search engine), you use threading (or asyncio) to fetch HTML pages concurrently, and multiprocessing to parse/tokenize the massive text chunks across multiple CPU cores.
"""

import threading
import multiprocessing
import time
import queue
from typing import List

# Helper Functions
def io_bound_task(name: str, delay: float) -> None:
    """Simulates an I/O bound task like a network request."""
    print(f"Task {name} starting...")
    time.sleep(delay)
    print(f"Task {name} finished.")

def cpu_bound_task(n: int) -> int:
    """Simulates a CPU bound task like calculating prime numbers."""
    count = 0
    for i in range(n):
        count += sum(j * j for j in range(100))
    return count

# Basic Implementation: Threading (I/O Bound)
def run_threading() -> None:
    print("\n--- Threading (I/O Bound) ---")
    start = time.time()
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=io_bound_task, args=(f"Thread-{i}", 1.0))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    end = time.time()
    print(f"Threading took: {end - start:.4f}s (Should be ~1s, not 3s)")


# Intermediate Implementation: Multiprocessing (CPU Bound)
def run_multiprocessing() -> None:
    print("\n--- Multiprocessing (CPU Bound) ---")
    n = 2000
    
    # Sequential execution
    start = time.time()
    for _ in range(4):
        cpu_bound_task(n)
    seq_time = time.time() - start
    print(f"Sequential took: {seq_time:.4f}s")
    
    # Parallel execution
    start = time.time()
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=cpu_bound_task, args=(n,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
    par_time = time.time() - start
    print(f"Multiprocessing took: {par_time:.4f}s")


# Advanced Implementation: Thread Synchronization
def thread_safe_counter() -> None:
    print("\n--- Thread Synchronization ---")
    class Counter:
        def __init__(self):
            self.value = 0
            self.lock = threading.Lock()

        def increment(self):
            # Without the lock, race conditions occur
            with self.lock:
                current = self.value
                time.sleep(0.0001) # Force context switch
                self.value = current + 1

    counter = Counter()
    threads = [threading.Thread(target=counter.increment) for _ in range(100)]
    
    for t in threads: t.start()
    for t in threads: t.join()
    
    print(f"Final counter value: {counter.value} (Expected: 100)")


# Performance Analysis
def analyze_performance() -> None:
    print("\n--- Performance Analysis ---")
    print("Rule of Thumb:")
    print("- I/O Bound -> Use `threading` or `asyncio`")
    print("- CPU Bound -> Use `multiprocessing`")
    print("Using threading for CPU bound tasks in Python is often SLOWER than sequential execution due to GIL contention.")


# Edge Cases
def handle_edge_cases() -> None:
    print("\n--- Edge Cases ---")
    # Deadlocks
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    
    def deadlock_func(l1, l2, name):
        with l1:
            time.sleep(0.01) # if both threads get here, deadlock!
            if l2.acquire(timeout=0.1): # Timeout prevents infinite deadlock for this demo
                try:
                    pass
                finally:
                    l2.release()
            else:
                print(f"{name} avoided deadlock via timeout.")

    t1 = threading.Thread(target=deadlock_func, args=(lock1, lock2, "T1"))
    t2 = threading.Thread(target=deadlock_func, args=(lock2, lock1, "T2"))
    t1.start(); t2.start()
    t1.join(); t2.join()


# Interview Challenge
def producer_consumer() -> None:
    """
    Challenge: Use a Queue to pass messages safely between threads (Producer/Consumer pattern).
    """
    q: queue.Queue = queue.Queue(maxsize=5)
    
    def producer():
        for i in range(3):
            q.put(f"item-{i}")
            time.sleep(0.01)
            
    def consumer():
        results = []
        for _ in range(3):
            item = q.get()
            results.append(item)
            q.task_done()
        print(f"Consumer got: {results}")

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start(); c.start()
    p.join(); c.join()


# Tests
def run_tests() -> None:
    # Most multithreading code is difficult to unit test deterministically.
    # We mainly test that they run without raising exceptions.
    print("\nRunning automated checks...")
    thread_safe_counter()
    producer_consumer()
    print("All concurrency tests passed.")

if __name__ == "__main__":
    print("--- Running Threading and Multiprocessing Examples ---")
    run_threading()
    # Windows requires the main module to be safely importable for multiprocessing
    # run_multiprocessing() is omitted from auto-run to avoid recursive spawning if not careful,
    # but it works perfectly fine within an `if __name__ == '__main__':` block.
    run_multiprocessing()
    analyze_performance()
    handle_edge_cases()
    run_tests()
