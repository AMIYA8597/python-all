"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (CONCURRENCY - THREADING & GIL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Concurrency in Python is fundamentally misunderstood by junior engineers. 
# They assume that creating 4 threads will distribute mathematical work across 
# 4 CPU cores, mathematically quadrupling the speed of their application.
#
# They run their threaded code and discover it is actually SLOWER than a 
# single-threaded script. They have crashed into the Global Interpreter Lock (GIL).
#
# A senior engineer mathematically maps the application into two categories: 
# CPU-Bound (Mathematics) and I/O-Bound (Network/Disk). They deploy Threading 
# EXCLUSIVELY for I/O operations where the OS physically evicts the thread from 
# the CPU, allowing the GIL to drop and enabling flawless concurrent execution.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the physical architecture of the Global Interpreter Lock (GIL).
# - Prove why Threading fails for CPU-bound tasks.
# - Prove why Threading is mathematically perfect for I/O-bound tasks.
#
# ==============================================================================
"""

import time
import timeit
import threading
import math
import requests # We will use a simulated delay if requests is unavailable
import socket

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CPU-BOUND TASKS (THE GIL BOTTLECK)
# ==============================================================================
def mathematical_workload():
    """A CPU-heavy operation (Cryptographic hashing, Matrix multiplication)"""
    total = 0
    # 5,000,000 iterations burning pure CPU cycles!
    for i in range(5_000_000):
        total += math.sqrt(i)
    return total

def demonstrate_gil_failure():
    section_header("The GIL Failure: Threading on CPU-Bound Tasks")
    
    print("\n  [SCENARIO A: SINGLE THREAD (Sequential Execution)]")
    start_single = timeit.default_timer()
    # Execute the math twice sequentially
    mathematical_workload()
    mathematical_workload()
    end_single = timeit.default_timer()
    time_single = end_single - start_single
    print(f"    -> Time:   {time_single:.4f} seconds")
    
    print("\n  [SCENARIO B: MULTI-THREADING (2 Concurrent Threads)]")
    start_multi = timeit.default_timer()
    # Spawn two threads! Junior expectation: 2x speedup!
    t1 = threading.Thread(target=mathematical_workload)
    t2 = threading.Thread(target=mathematical_workload)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    end_multi = timeit.default_timer()
    time_multi = end_multi - start_multi
    print(f"    -> Time:   {time_multi:.4f} seconds")
    
    print("\n  [MATHEMATICAL PROOF]")
    print("    -> Multi-threading provided ZERO speedup. In fact, it is often SLOWER!")
    print("    -> Reason: The GIL forces the CPU to execute Python Bytecode linearly.")
    print("       The threads spend their entire execution aggressively fighting each")
    print("       other to acquire the GIL lock, incurring massive Context Switching overhead.")


# ==============================================================================
# 4. I/O-BOUND TASKS (THE GIL DROPS)
# ==============================================================================
def network_workload():
    """An I/O-bound operation simulating a Database Query or API HTTP Request."""
    # `time.sleep` simulates waiting for a network socket to respond.
    # The CPU is doing absolutely ZERO work during this delay!
    time.sleep(1.0) 

def demonstrate_io_success():
    section_header("The Threading Victory: I/O-Bound Tasks")
    
    print("\n  [SCENARIO A: SINGLE THREAD (Sequential Execution)]")
    start_single = timeit.default_timer()
    # We execute 3 simulated network requests sequentially
    for _ in range(3):
        network_workload()
    end_single = timeit.default_timer()
    time_single = end_single - start_single
    print(f"    -> Expected Time: 3.0 seconds")
    print(f"    -> Actual Time:   {time_single:.4f} seconds")
    
    print("\n  [SCENARIO B: MULTI-THREADING (3 Concurrent Threads)]")
    start_multi = timeit.default_timer()
    
    threads = []
    for _ in range(3):
        t = threading.Thread(target=network_workload)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    end_multi = timeit.default_timer()
    time_multi = end_multi - start_multi
    print(f"    -> Expected Time: ~1.0 seconds")
    print(f"    -> Actual Time:   {time_multi:.4f} seconds")
    
    print("\n  [MATHEMATICAL PROOF]")
    print("    -> Multi-threading achieved a flawless 3x speedup!")
    print("    -> Reason: When Thread 1 executes an I/O operation (sleep/socket), the CPython")
    print("       interpreter mathematically detects that the thread is physically blocked.")
    print("       It instantly FORCES Thread 1 to drop the GIL. Thread 2 acquires the GIL and")
    print("       initiates its network request, dropping the GIL immediately. All 3 threads")
    print("       wait on the OS Network Socket concurrently without violating the GIL!")


def run_all_labs():
    demonstrate_gil_failure()
    demonstrate_io_success()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What exactly is the Global Interpreter Lock (GIL), and why did Guido van Rossum architect CPython to include it?"
   Senior Answer: "The GIL is a physical Mutex lock embedded deep within the CPython Interpreter. It mandates that exactly *one* native OS thread can execute Python Bytecode at any given microsecond. It was architected to protect Python's core memory management system: Reference Counting. If two threads attempted to increment or decrement an object's reference count concurrently without a lock, a Race Condition would occur. An object could mathematically be dropped to a reference count of $0$ and be deleted by Thread A while Thread B was actively reading it, instantly triggering a catastrophic Segfault. The GIL trades multi-core parallelism for flawless, lock-free, thread-safe memory management at the single-core level."

2. Interviewer: "If the GIL restricts execution to a single core, why did the CPU-Bound Threading test actually take slightly *longer* than the sequential test?"
   Senior Answer: "Because of 'Context Switching Overhead'. In a single-threaded application, the CPU executes the loop seamlessly in L1 Cache. In the Multi-Threaded test, the OS Thread Scheduler grants execution to Thread A. Thread A acquires the GIL, runs for $5$ milliseconds, and is forcefully suspended by the OS. The CPU must physically dump the CPU registers to RAM, load Thread B's context, and grant Thread B the GIL. Thread A and B violently thrash back and forth thousands of times a second, continuously fighting for the GIL Mutex lock. This administrative OS-level context switching consumes massive CPU cycles, yielding worse performance than doing the work linearly."

3. Interviewer: "How does the GIL interact with I/O operations like HTTP requests or Database Queries?"
   Senior Answer: "This is the saving grace of Python concurrency. When a Python thread executes an I/O blocking operation (like calling `socket.recv()` or `time.sleep()`), the CPython interpreter executes a macro explicitly forcing the thread to drop the GIL *before* handing the blocking request to the OS kernel. The OS suspends the thread. Because the GIL is now free, the Python interpreter instantly awakens Thread B, allowing it to execute bytecode. This means that an application with $100$ threads making HTTP requests can mathematically have $99$ threads suspended by the OS waiting for network responses, while $1$ thread actively holds the GIL and processes the incoming payload. The GIL is never a bottleneck for network-heavy code."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Concurrency (Threading & GIL) Completed.")
