"""
# ==============================================================================
# LABORATORY: ASYNCIO AND THE EVENT LOOP
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# `asyncio` is the foundation of modern high-performance Python web frameworks 
# (FastAPI, AIOHTTP) and AI Agents that need to make thousands of concurrent API 
# calls (e.g. hitting the OpenAI API). Unlike threading (which the OS manages), 
# asyncio is cooperative multitasking managed entirely within a single Python thread.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Event Loop.
# - Differentiate Coroutines (`async def`) from normal functions.
# - Understand the `await` keyword (yielding control back to the loop).
# - Master `asyncio.create_task` and `asyncio.gather` for concurrency.
# - Identify and avoid the "Blocking the Event Loop" trap.
#
# ==============================================================================
"""

import time
import asyncio
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COROUTINES AND THE EVENT LOOP
# ==============================================================================

# `async def` defines a Coroutine, not a function.
# Calling it does NOT execute the code; it returns a coroutine object.
async def fetch_data(id: int, delay: float) -> str:
    print(f"  [Task {id}] Starting fetch...")
    
    # await asyncio.sleep() simulates non-blocking I/O (like a network request)
    # It tells the Event Loop: "I am waiting for this. Go run other tasks!"
    await asyncio.sleep(delay)
    
    print(f"  [Task {id}] Finished fetch.")
    return f"Data {id}"

def demonstrate_basics():
    """
    You cannot call a coroutine directly. You must run it in an Event Loop.
    """
    section_header("Coroutines & The Event Loop")
    
    coro = fetch_data(1, 0.5)
    print(f"Calling fetch_data returns: {coro}")
    
    print("Executing it via asyncio.run()...")
    # asyncio.run() creates an Event Loop, runs the coroutine, and closes the loop.
    result = asyncio.run(coro)
    print(f"Result: {result}")


# ==============================================================================
# 4. CONCURRENCY: TASKS AND GATHER
# ==============================================================================

async def main_concurrent():
    """
    If we just `await` one after another, it runs sequentially.
    To run concurrently, we wrap them in Tasks and use `asyncio.gather`.
    """
    start = time.perf_counter()
    
    # 1. SEQUENTIAL (Takes 3 seconds)
    print("\n--- Sequential Awaits ---")
    await fetch_data(1, 1.0)
    await fetch_data(2, 1.0)
    await fetch_data(3, 1.0)
    print(f"Sequential Time: {time.perf_counter() - start:.2f}s")
    
    # 2. CONCURRENT (Takes 1 second)
    print("\n--- Concurrent Execution (asyncio.gather) ---")
    start = time.perf_counter()
    
    # .gather() schedules all coroutines to run concurrently on the event loop.
    results = await asyncio.gather(
        fetch_data(4, 1.0),
        fetch_data(5, 1.0),
        fetch_data(6, 1.0)
    )
    
    print(f"Gather Results: {results}")
    print(f"Concurrent Time: {time.perf_counter() - start:.2f}s (Massive Speedup!)")

def demonstrate_concurrency():
    section_header("Tasks and asyncio.gather")
    asyncio.run(main_concurrent())


# ==============================================================================
# 5. THE DEADLY TRAP: BLOCKING THE EVENT LOOP
# ==============================================================================

def blocking_io():
    """A synchronous function (like time.sleep or requests.get)"""
    time.sleep(1.0)

async def bad_task(id: int):
    print(f"  [Bad {id}] Starting...")
    blocking_io() # TRAP! This freezes the ENTIRE event loop.
    print(f"  [Bad {id}] Done.")

async def good_task(id: int):
    print(f"  [Good {id}] Starting...")
    await asyncio.sleep(1.0) # Yields control correctly
    print(f"  [Good {id}] Done.")

async def main_blocking_trap():
    print("\n--- The Blocking Trap (Using synchronous sleep) ---")
    start = time.perf_counter()
    # Even though we use gather, they run sequentially because blocking_io() 
    # freezes the thread. No other task can run!
    await asyncio.gather(bad_task(1), bad_task(2), bad_task(3))
    print(f"Blocked Time: {time.perf_counter() - start:.2f}s (Expected 1s, took 3s!)")
    
    print("\n--- The Proper Way (Using await) ---")
    start = time.perf_counter()
    await asyncio.gather(good_task(1), good_task(2), good_task(3))
    print(f"Async Time:   {time.perf_counter() - start:.2f}s (Took 1s as expected!)")

def demonstrate_blocking_trap():
    section_header("TRAP: Blocking the Event Loop")
    asyncio.run(main_blocking_trap())


# ==============================================================================
# 6. BRIDGING SYNC AND ASYNC (TO THREADS)
# ==============================================================================

async def main_bridge():
    """
    If you MUST run a synchronous blocking function (like 'requests' or heavy math) 
    inside an async application (like FastAPI), you must offload it to a thread 
    so it doesn't block the event loop.
    """
    section_header("Bridging Sync and Async (to_thread)")
    
    start = time.perf_counter()
    
    print("Offloading blocking tasks to background threads...")
    # asyncio.to_thread runs the synchronous function in a separate thread 
    # but returns an awaitable coroutine so the Event Loop keeps running!
    await asyncio.gather(
        asyncio.to_thread(blocking_io),
        asyncio.to_thread(blocking_io),
        asyncio.to_thread(blocking_io)
    )
    
    print(f"Threaded Async Time: {time.perf_counter() - start:.2f}s")

def demonstrate_bridge():
    asyncio.run(main_bridge())


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Threading and Asyncio?
   Answer: Threading is Preemptive Multitasking managed by the OS (the OS pauses and resumes threads arbitrarily). Asyncio is Cooperative Multitasking managed in a single Python thread (tasks explicitly yield control using `await`).

2. What happens if you call `requests.get()` inside an `async def` function?
   Answer: You BLOCK the Event Loop. Because `requests` is synchronous, it does not yield control. The entire async application (e.g. FastAPI server) will freeze and accept no new requests until the network call finishes. You must use an async client (like `httpx` or `aiohttp`), or offload to a thread via `asyncio.to_thread()`.

3. What does `asyncio.gather` do?
   Answer: It takes multiple awaitables, schedules them to run concurrently on the event loop, and waits for all of them to finish, returning an ordered list of their results.
"""

if __name__ == "__main__":
    demonstrate_basics()
    demonstrate_concurrency()
    demonstrate_blocking_trap()
    demonstrate_bridge()
    print("\n[SUCCESS] Laboratory: Asyncio Completed.")
