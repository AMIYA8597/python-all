"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (ASYNCHRONOUS PROGRAMMING & EVENT LOOPS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You want to fetch data from 10,000 different websites.
# 
# Synchronous (Blocking): You fetch Website 1. You WAIT 1 second for the network. 
# Then Website 2. Total time: 10,000 seconds (3 hours).
#
# Multi-Threading: You spawn 10,000 threads. The OS tries to manage 10,000 
# independent CPU execution contexts. The overhead of context-switching completely 
# crashes the CPU. Memory blows up (each thread needs a stack). Total failure.
#
# Asynchronous (Asyncio / NodeJS): You use exactly ONE thread. You start fetching 
# Website 1. The moment the network starts waiting, your code says "await" and 
# YIELDS control back to the Event Loop. The Event Loop instantly starts fetching 
# Website 2. And 3. And 10,000. 
#
# All 10,000 network requests are flying through the fiber-optic cables 
# simultaneously! When a response comes back, the Event Loop wakes up the 
# specific function. Total time: ~2 seconds. Total Threads: 1.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of the Event Loop.
# - Understand Coroutines and `await` yielding.
# - Differentiate I/O-Bound (Async) vs CPU-Bound (Multiprocessing).
#
# ==============================================================================
"""

import asyncio
import time
import multiprocessing

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ASYNCIO (I/O BOUND EFFICIENCY)
# ==============================================================================
async def fetch_website_mock(site_id: int) -> str:
    """
    A Coroutine!
    When this function hits `await`, it mathematically pauses execution and 
    returns control to the central Event Loop, allowing other code to run!
    """
    print(f"[Async] Requesting Site {site_id}... (Pausing function, yielding to Event Loop)")
    
    # Simulate network latency. NOT time.sleep()!
    # time.sleep() would physically freeze the entire thread, breaking Asyncio.
    # asyncio.sleep() tells the Event Loop "wake me up in 1 second, go do other stuff!"
    await asyncio.sleep(1.0)
    
    print(f"[Async] Downloaded Site {site_id}!")
    return f"Data_{site_id}"

async def run_async_engine():
    start = time.time()
    
    # We create 5 coroutines. They do NOT execute yet!
    tasks = [fetch_website_mock(i) for i in range(1, 6)]
    
    print("Firing all 5 network requests SIMULTANEOUSLY on a SINGLE thread...")
    # asyncio.gather fires them all concurrently into the Event Loop
    results = await asyncio.gather(*tasks)
    
    end = time.time()
    print(f"\nAll 5 requests completed in: {end - start:.2f} seconds!")
    print(f"Results: {results}")

def demonstrate_asyncio():
    section_header("Asynchronous I/O (The Event Loop)")
    # The Event Loop is the beating heart of Async Python and NodeJS.
    asyncio.run(run_async_engine())


# ==============================================================================
# 4. MULTIPROCESSING (CPU BOUND EFFICIENCY)
# ==============================================================================
def heavy_cpu_math(worker_id: int):
    """
    A function that does NOT wait for network/disk. It violently crunches math.
    Asyncio is USELESS here, because the CPU never pauses. If the CPU never pauses, 
    the Event Loop never gets control back!
    """
    print(f"[Worker {worker_id}] Starting 20 Million operations...")
    total = 0
    for i in range(20_000_000):
        total += i
    return total

def demonstrate_multiprocessing():
    section_header("Multiprocessing (Bypassing the GIL)")
    
    print("Asyncio cannot solve CPU-Bound tasks because of the Global Interpreter Lock (GIL).")
    print("To utilize all 8 cores of a modern CPU for raw math, we must spawn independent Processes!")
    
    start = time.time()
    
    # We spawn a Pool of independent Python processes.
    # Each Process has its own Memory, its own GIL, and runs on a different physical CPU core!
    with multiprocessing.Pool(processes=4) as pool:
        # Map fires the function 4 times concurrently across the 4 cores
        results = pool.map(heavy_cpu_math, range(4))
        
    end = time.time()
    print(f"\nAll 4 massive CPU tasks completed in: {end - start:.2f} seconds!")


def run_all_labs():
    demonstrate_asyncio()
    
    # Multiprocessing requires safe main-guarding in Python (Windows specifically)
    demonstrate_multiprocessing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the architectural difference between Multi-Threading and Asynchronous Programming.
   Answer: Multi-Threading relies on the Operating System (OS). The OS spawns multiple physical threads, and preemptively interrupts them (Context Switching) thousands of times a second to fake concurrency. This costs massive memory and CPU overhead. Asynchronous Programming relies entirely on the Application Code. It uses exactly ONE thread. The Application uses a central "Event Loop". Functions explicitly say "I am waiting for the network, you can take over" (`await`). Because the yielding is cooperative and managed purely in software, the overhead is near zero. A single thread can manage 100,000 async connections flawlessly!

2. If Asyncio is so fast, why does `time.sleep()` completely destroy it?
   Answer: `time.sleep()` is a blocking, synchronous OS command. When you call it, you command the OS to physically freeze the actual CPU thread! Because Asyncio runs entirely on that *single* thread, freezing the thread freezes the central Event Loop! All 10,000 concurrent network connections instantly halt. You MUST use `await asyncio.sleep()`, which doesn't freeze the thread; it simply registers a timer with the Event Loop, allowing the Event Loop to continue processing other coroutines while waiting.

3. When building a system, how do you mathematically decide between Asyncio and Multiprocessing?
   Answer: You look at the bottleneck!
   - Is it "I/O-Bound"? (Waiting for Database, Network, Disk, third-party APIs). Use Asyncio! The CPU is sitting idle 99% of the time waiting for electrons to travel through cables. Asyncio perfectly utilizes that idle time.
   - Is it "CPU-Bound"? (Video Encoding, Machine Learning, Cryptography, massive `for` loops). Use Multiprocessing! The CPU is running at 100% capacity. An Event Loop cannot help if there is no idle time to yield. You must bypass Python's GIL and physically turn on the other 7 cores of your processor by spawning independent OS Processes.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Async Programming) Completed.")
