"""
# ==============================================================================
# LABORATORY: THREADING, MULTIPROCESSING, AND THE GIL
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You cannot scale a Python application without understanding its concurrency model.
# The Global Interpreter Lock (GIL) fundamentally changes how Python handles threads
# compared to Java or C++. If you use threads for CPU-bound tasks (like matrix 
# multiplication), your program will actually run SLOWER due to context-switching overhead.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Concurrency (interleaving) vs Parallelism (simultaneous execution).
# - Understand the CPython Global Interpreter Lock (GIL).
# - Use the `threading` module for I/O-bound tasks (network, disk).
# - Use the `multiprocessing` module for CPU-bound tasks (math, data processing).
# - Prevent race conditions using Locks (`threading.Lock()`).
# - Master `concurrent.futures.ThreadPoolExecutor` and `ProcessPoolExecutor`.
#
# ==============================================================================
"""

import time
import threading
import multiprocessing
import concurrent.futures

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GIL AND CPU-BOUND TASKS (MULTIPROCESSING)
# ==============================================================================

def cpu_bound_task(n: int) -> int:
    """A heavy mathematical task."""
    count = 0
    for i in range(n):
        count += i
    return count

def demonstrate_cpu_bound():
    """
    Because of the GIL, only ONE thread can execute Python bytecodes at a time.
    For CPU-heavy tasks, threading provides ZERO benefit and adds overhead.
    We MUST use multiprocessing to bypass the GIL and utilize multiple CPU cores.
    """
    section_header("CPU-Bound Execution: Threading vs Multiprocessing")
    
    n = 20_000_000
    tasks = [n, n]
    
    # 1. SYNCHRONOUS
    start = time.perf_counter()
    [cpu_bound_task(t) for t in tasks]
    print(f"Synchronous time:    {time.perf_counter() - start:.3f}s")
    
    # 2. THREADING (Usually SLOWER than synchronous due to GIL contention!)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(cpu_bound_task, tasks)
    print(f"Threading time:      {time.perf_counter() - start:.3f}s (GIL blocked!)")
    
    # 3. MULTIPROCESSING (Spawns entirely new Python processes with their own memory and GIL)
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(cpu_bound_task, tasks)
    print(f"Multiprocessing time:{time.perf_counter() - start:.3f}s (True Parallelism!)")


# ==============================================================================
# 4. I/O-BOUND TASKS (THREADING)
# ==============================================================================

def io_bound_task(task_id: int) -> None:
    """Simulates a network request or database query."""
    # time.sleep RELEASES the GIL, allowing other threads to run!
    time.sleep(1)
    
def demonstrate_io_bound():
    """
    For I/O tasks, the GIL is released while Python waits for the OS/Network.
    Threading is PERFECT here.
    """
    section_header("I/O-Bound Execution: Threading shines")
    
    tasks = range(5)
    
    # 1. SYNCHRONOUS (Will take ~5 seconds)
    start = time.perf_counter()
    for t in tasks:
        io_bound_task(t)
    print(f"Synchronous I/O: {time.perf_counter() - start:.3f}s")
    
    # 2. THREADING (Will take ~1 second because they sleep concurrently)
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(io_bound_task, tasks)
    print(f"Threaded I/O:    {time.perf_counter() - start:.3f}s (Massive Speedup!)")


# ==============================================================================
# 5. RACE CONDITIONS & LOCKS
# ==============================================================================

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()
        
    def deposit_dangerous(self, amount: int):
        # A race condition occurs here. Reading, adding, and writing 
        # are NOT atomic operations in Python bytecodes!
        temp = self.balance
        temp += amount
        self.balance = temp
        
    def deposit_safe(self, amount: int):
        # The lock ensures only ONE thread can execute this block at a time.
        with self.lock:
            temp = self.balance
            temp += amount
            self.balance = temp

def run_race_condition(account: BankAccount, method_name: str, workers: int, operations: int):
    method = getattr(account, method_name)
    
    def worker():
        for _ in range(operations):
            method(1)
            
    threads = []
    for _ in range(workers):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

def demonstrate_locks():
    section_header("Race Conditions and Locks")
    
    workers = 5
    operations = 100_000
    expected = workers * operations
    
    # Dangerous Bank
    dangerous_bank = BankAccount()
    run_race_condition(dangerous_bank, "deposit_dangerous", workers, operations)
    print(f"Dangerous Bank Balance: {dangerous_bank.balance:,} (Expected: {expected:,})")
    print(" ^ Notice the missing funds due to thread race conditions!")
    
    # Safe Bank
    safe_bank = BankAccount()
    run_race_condition(safe_bank, "deposit_safe", workers, operations)
    print(f"Safe Bank Balance:      {safe_bank.balance:,} (Expected: {expected:,})")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Global Interpreter Lock (GIL)?
   Answer: A mutex built into CPython that prevents multiple native threads from executing Python bytecodes simultaneously. It makes CPython thread-safe internally but prevents true multicore parallelism for CPU-bound code.

2. When should you use Threading in Python?
   Answer: For I/O-bound tasks (network requests, API calls, file reads, database queries) because the GIL is released while waiting for the OS to perform the I/O.

3. When should you use Multiprocessing in Python?
   Answer: For CPU-bound tasks (image processing, data crunching, heavy math). Multiprocessing spawns entirely new OS processes, each with its own memory space and its own GIL, allowing true parallel execution on multiple cores.

4. What is a Race Condition?
   Answer: When multiple threads access and mutate shared data concurrently, causing unpredictable results because the exact order of operation execution depends on OS scheduling. Fixed using a `Lock`.
"""

if __name__ == "__main__":
    # Note: On Windows, multiprocessing MUST be protected by __main__ block
    demonstrate_cpu_bound()
    demonstrate_io_bound()
    demonstrate_locks()
    print("\n[SUCCESS] Laboratory: Concurrency & Parallelism Completed.")
