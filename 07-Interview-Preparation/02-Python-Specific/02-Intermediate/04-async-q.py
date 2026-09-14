"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - ASYNC & GIL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a Python script that downloads 1,000 images from S3. 
# It takes 100 seconds. I added `threading.Thread(target=download)` and spawned 
# 1,000 threads. It now takes 2 seconds. Doesn't the GIL prevent Python from 
# running threads in parallel? Why did it get 50x faster?"
#
# If you don't understand the exact C-level mechanism of the Global Interpreter 
# Lock (GIL), you will fail. The GIL only locks Python bytecode execution. The 
# moment a thread makes an I/O system call (like `requests.get()`), CPython 
# physically DROPS the GIL, allowing other threads to run freely while the first 
# thread waits for the network!
#
# Interviewer: "Okay, so Threading works for I/O. Why should I ever use `asyncio`?"
# If you spawn 10,000 Threads, the Operating System will allocate 10,000 Memory 
# Stacks (8MB each = 80 Gigabytes of RAM!) and the CPU will violently stutter 
# doing Context Switches. `asyncio` uses exactly ONE Thread and 10,000 State 
# Machines, consuming almost zero RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Global Interpreter Lock (GIL).
# - Understand why the GIL drops during I/O wait times.
# - Differentiate OS Threading vs Event Loop Asyncio.
#
# ==============================================================================
"""

import time
import threading
import asyncio
import multiprocessing

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GIL AND I/O BOUND PERFORMANCE
# ==============================================================================
def mock_network_download(thread_id: int):
    """
    Simulates downloading a file.
    CRITICAL: time.sleep() drops the GIL!
    When this executes, CPython says: "Ah, this thread is just waiting for a 
    C-level system timer. It doesn't need to execute Python bytecode. I will 
    DROP THE GIL and give it to another thread!"
    """
    time.sleep(0.5) # Simulates network latency

def demonstrate_gil_drop():
    section_header("The GIL & I/O Bound Tasks (Threading)")
    
    print("Task: Download 10 files (0.5 seconds each).")
    
    # 1. Synchronous
    start = time.perf_counter()
    for i in range(10):
        mock_network_download(i)
    end = time.perf_counter()
    print(f"  -> Synchronous Time: {end - start:.2f} seconds (Expected ~5s)")
    
    # 2. Multi-Threading
    start = time.perf_counter()
    threads = []
    for i in range(10):
        t = threading.Thread(target=mock_network_download, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    end = time.perf_counter()
    print(f"  -> Multi-Thread Time: {end - start:.2f} seconds (Expected ~0.5s)")
    
    print("\nConclusion: The GIL does NOT prevent Threading from speeding up I/O!")
    print("The GIL is dropped the moment the OS handles the network request.")


# ==============================================================================
# 4. THE GIL AND CPU BOUND DISASTER
# ==============================================================================
def heavy_cpu_math():
    """
    A pure CPU-Bound task. No waiting. Just pure Python bytecode execution.
    Because it is constantly executing bytecode, it NEVER drops the GIL!
    """
    total = 0
    for i in range(5_000_000):
        total += i
    return total

def demonstrate_gil_block():
    section_header("The GIL & CPU Bound Tasks (Disaster)")
    
    print("Task: Run massive mathematical calculations 4 times.")
    
    # 1. Synchronous
    start = time.perf_counter()
    for _ in range(4):
        heavy_cpu_math()
    end = time.perf_counter()
    sync_time = end - start
    print(f"  -> Synchronous Time: {sync_time:.2f} seconds")
    
    # 2. Multi-Threading
    start = time.perf_counter()
    threads = []
    for _ in range(4):
        t = threading.Thread(target=heavy_cpu_math)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    end = time.perf_counter()
    thread_time = end - start
    print(f"  -> Multi-Thread Time: {thread_time:.2f} seconds")
    
    print("\nConclusion: Threading was NOT faster! In fact, it's often SLOWER!")
    print("Because only 1 thread can hold the GIL at a time, the 4 threads just ")
    print("fought each other violently for the lock, executing sequentially anyway, ")
    print("while adding massive Context-Switching overhead!")


def run_all_labs():
    demonstrate_gil_drop()
    demonstrate_gil_block()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What exactly is the GIL, and why does Python have it?"
   Senior Answer: "The Global Interpreter Lock (GIL) is a physical C-level Mutex lock that protects CPython's internal memory state. CPython's primary Garbage Collector relies on Reference Counting. If two Threads simultaneously incremented the reference count of the exact same object without a lock, a Race Condition would occur, and the count would be incorrect, leading to a fatal memory leak or a segfault. Instead of putting a heavy lock on every single one of the 10 Million objects in RAM (which would crash single-threaded performance), Python puts ONE massive lock on the entire interpreter itself. Only one thread can execute Python bytecode at any given microsecond."

2. Interviewer: "If Threading speeds up I/O bounds, why was Asyncio invented?"
   Senior Answer: "Threading is managed by the Operating System (OS). When you spawn 10,000 threads, the OS must allocate a massive 8MB memory stack for each thread (80 GB of RAM!). Furthermore, the OS scheduler must preemptively pause and resume 10,000 threads, destroying the CPU with Context-Switching latency. `asyncio` completely bypasses the OS. It uses exactly ONE physical thread. When a coroutine hits `await`, it mathematically pauses its state machine and hands control back to a central Event Loop in software. Because the Context-Switch happens in pure Python logic rather than hardware interrupts, `asyncio` can effortlessly juggle 100,000 concurrent network requests using almost zero RAM."

3. Interviewer: "How do you bypass the GIL for CPU-bound tasks in Python?"
   Senior Answer: "You cannot bypass the GIL using Threads or Asyncio, because both run inside the exact same CPython Process, bounded by the exact same GIL. To bypass it, you must use the `multiprocessing` module to spawn completely independent OS Processes. Each Process has its own physical memory space, its own Python Interpreter, and crucially, its own completely isolated GIL! If you spawn 8 Processes on an 8-Core CPU, they will run in perfect mathematical parallel, utilizing 100% of the hardware. The tradeoff is that sharing data between Processes requires heavy serialization (Pickling) over IPC (Inter-Process Communication) pipes."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Async & GIL) Completed.")
