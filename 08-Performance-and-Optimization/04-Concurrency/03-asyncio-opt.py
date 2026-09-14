"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (CONCURRENCY - ASYNCIO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Threading is excellent for I/O operations, but OS Threads are mathematically 
# heavy. Each thread consumes ~8 MB of RAM for its execution stack. If a web 
# scraper attempts to open 10,000 concurrent network sockets using 10,000 threads, 
# it requires 80 Gigabytes of RAM, instantly crashing the server.
#
# A senior engineer uses `asyncio`. Instead of relying on the OS to schedule 
# heavy hardware threads, they deploy an "Event Loop" running on a single CPU core. 
# They use Coroutines (`async/await`) to mathematically suspend execution at the 
# application level whenever a socket blocks. 10,000 concurrent sockets consume 
# 0 threads and just a few Megabytes of RAM, executing with flawless efficiency.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Asyncio Event Loop architecture.
# - Prove the extreme memory efficiency of Coroutines vs OS Threads.
# - Master `asyncio.gather` for concurrent execution.
#
# ==============================================================================
"""

import time
import timeit
import asyncio
import threading

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. OS THREADING VS ASYNC COROUTINES
# ==============================================================================

# --- A. The Heavy Thread ---
def blocking_network_call(thread_id: int):
    """Simulates a blocking network I/O request (e.g., HTTP GET)."""
    # time.sleep() blocks the ENTIRE OS thread!
    time.sleep(1.0) 

def demonstrate_heavy_threads(concurrent_requests: int):
    print(f"\n  [SCENARIO A: OS THREADING ({concurrent_requests} Concurrent Requests)]")
    start = timeit.default_timer()
    
    threads = []
    for i in range(concurrent_requests):
        t = threading.Thread(target=blocking_network_call, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    end = timeit.default_timer()
    print(f"    -> Expected Time: ~1.0 seconds")
    print(f"    -> Actual Time:   {end - start:.4f} seconds")
    print("    -> OS Overhead: MASSIVE. The OS just allocated and destroyed")
    print(f"       {concurrent_requests} heavy execution stacks in RAM.")


# --- B. The Lightweight Coroutine ---
async def non_blocking_network_call(coro_id: int):
    """Simulates a non-blocking asyncio network request."""
    # asyncio.sleep() mathematically yields control back to the Event Loop!
    # The OS thread is NEVER blocked!
    await asyncio.sleep(1.0)

async def run_async_workload(concurrent_requests: int):
    print(f"\n  [SCENARIO B: ASYNCIO COROUTINES ({concurrent_requests} Concurrent Requests)]")
    start = timeit.default_timer()
    
    # We dynamically construct thousands of Coroutine tasks in microseconds!
    tasks = [non_blocking_network_call(i) for i in range(concurrent_requests)]
    
    # asyncio.gather() commands the Event Loop to execute them all concurrently.
    await asyncio.gather(*tasks)
    
    end = timeit.default_timer()
    print(f"    -> Expected Time: ~1.0 seconds")
    print(f"    -> Actual Time:   {end - start:.4f} seconds")
    print("    -> OS Overhead: ZERO. Only 1 OS Thread was ever used.")
    print("       The Event Loop mathematically juggled thousands of lightweight states.")

def demonstrate_asyncio():
    section_header("Performance Proof: The Event Loop vs OS Threads")
    
    REQUESTS = 1000 # 1,000 Concurrent Network Connections!
    
    # Note: 1,000 threads might trigger warnings or slight slowdowns on weak CPUs.
    demonstrate_heavy_threads(REQUESTS)
    
    # We must explicitly boot up the Event Loop to run the Coroutines!
    asyncio.run(run_async_workload(REQUESTS))
    
    print("\n  [MATHEMATICAL CONCLUSION]")
    print("    Both approaches achieved near-perfect concurrency.")
    print("    However, if we increased the load to 50,000 connections, the OS")
    print("    Threading approach would violently crash the Operating System (OOM).")
    print("    The Asyncio approach would gracefully scale using just Megabytes of RAM.")


# ==============================================================================
# 4. THE DANGER OF BLOCKING THE EVENT LOOP
# ==============================================================================
async def bad_coroutine():
    """A mathematically catastrophic coroutine."""
    # A junior engineer forgets to use an 'async' compatible library, and 
    # accidentally calls a standard blocking function (like `time.sleep` or 
    # `requests.get`) inside an async definition!
    print("    [BAD COROUTINE] Initiating a 2-second blocking halt...")
    time.sleep(2.0) # THIS FREEZES THE ENTIRE EVENT LOOP!
    print("    [BAD COROUTINE] Unblocked.")

async def good_coroutine(id: int):
    print(f"    [GOOD CORO {id}] Requesting data...")
    await asyncio.sleep(0.5)
    print(f"    [GOOD CORO {id}] Received data!")

async def run_catastrophe_simulation():
    section_header("The Danger: Blocking the Event Loop")
    
    print("  [SCENARIO] We launch 3 fast requests, but one bad coroutine slips in.")
    
    start = timeit.default_timer()
    
    # The Event Loop starts juggling...
    await asyncio.gather(
        good_coroutine(1),
        good_coroutine(2),
        bad_coroutine(), # BOOM.
        good_coroutine(3)
    )
    
    end = timeit.default_timer()
    print(f"\n  [RESULT] Total Time: {end - start:.4f} seconds")
    print("  [CONCLUSION] The entire application halted for 2 seconds. Because Asyncio")
    print("  runs on a SINGLE OS THREAD, a single blocking call completely disables")
    print("  concurrency for every single coroutine currently loaded in the Event Loop.")

def run_all_labs():
    demonstrate_asyncio()
    asyncio.run(run_catastrophe_simulation())


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Asyncio runs on a single CPU core, how is it capable of processing 10,000 network requests concurrently without blocking?"
   Senior Answer: "Asyncio leverages the OS Kernel's high-performance I/O multiplexing architectures (like `epoll` on Linux or `kqueue` on macOS). When an `await` command is encountered (e.g., waiting for an HTTP response), the Event Loop does not pause. It mathematically registers the File Descriptor (Socket) with the OS kernel and instantly yields control to another coroutine. The single CPU core rapidly rotates through the active coroutines in microseconds. When the OS kernel detects that network packets have finally arrived for a specific socket, it flags the Event Loop, which immediately resumes execution of that specific coroutine. It is Cooperative Multitasking at the highest mathematical efficiency."

2. Interviewer: "What is the architectural difference in memory consumption between Threading and Asyncio?"
   Senior Answer: "When you spawn an OS Thread, the kernel physically allocates a dedicated Execution Stack (typically 8 Megabytes on Linux) to track variables, function calls, and registers. 1,000 threads instantly consume 8 Gigabytes of pure RAM overhead before executing a single line of business logic. Asyncio operates entirely in User Space. A Coroutine is merely a Python Generator object that mathematically tracks its own state in a few hundred bytes. The OS is completely unaware of coroutines. Therefore, you can launch 1,000,000 coroutines on a standard laptop with only a few hundred Megabytes of RAM, fundamentally solving the 'C10k Problem' (handling 10,000 concurrent connections)."

3. Interviewer: "A Junior Developer is using `asyncio`, but they import the standard `requests` library to make HTTP calls. They report that their web scraper is running sequentially, taking 500 seconds for 500 requests. What went wrong?"
   Senior Answer: "They catastrophically 'Blocked the Event Loop'. The standard `requests` library is architecturally synchronous; it executes a blocking C-level socket call. Because the Asyncio Event Loop runs on a single physical OS thread, invoking a blocking call physically freezes the entire thread! The Event Loop cannot yield execution to other coroutines because it is violently trapped by the OS kernel waiting for the network timeout. To resolve this, they must swap `requests` for an asynchronous library (like `aiohttp` or `httpx`), which utilizes non-blocking sockets and properly yields `await` control back to the central Event Loop."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Concurrency (Asyncio) Completed.")
