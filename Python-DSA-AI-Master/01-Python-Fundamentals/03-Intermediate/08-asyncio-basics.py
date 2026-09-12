"""
## A. Concept Name
Asyncio (Asynchronous I/O)

## B. One-Sentence Definition
Asyncio is a library to write concurrent code using the async/await syntax, enabling cooperative multitasking in a single thread.

## C. Why Does This Exist?
Threading introduces significant overhead when managing thousands of I/O-bound tasks (like network requests). Asyncio allows a single thread to handle massive concurrency without the overhead of OS thread context switching, by yielding control while waiting for I/O operations.

## D. Intuition
Instead of halting the entire program while waiting for a slow operation (like a web request) to finish, the program says "I'm going to wait here; let me know when you're done, and in the meantime, someone else can use the CPU."

## E. Real-Life Analogy
Imagine a chef in a kitchen (the CPU thread).
- **Synchronous:** The chef puts a pizza in the oven and stands there staring at it for 15 minutes doing nothing until it's done.
- **Threading:** You hire 10 chefs to cook 10 pizzas, but they bump into each other and you have to pay them all.
- **Asyncio:** One chef puts a pizza in the oven, sets a timer, and immediately goes to chop vegetables for a salad. When the timer goes off, the chef takes the pizza out. One chef (thread) handles multiple tasks efficiently!

## F. Mental Model
Think of an Event Loop as a central manager. Tasks are submitted to the manager. The manager runs a task until it hits an `await` keyword. At that point, the task is suspended, and the manager switches to another task that is ready to run.

## G. Visual Explanation
Event Loop Execution:
Task 1: [Starts] -----> [await I/O] (Yields control)
Task 2:                 [Starts] -----> [await I/O] (Yields control)
Task 1:                                 <I/O Done> [Resumes & Finishes]
Task 2:                                             <I/O Done> [Resumes & Finishes]

## H. Formal Explanation
Asyncio is a single-threaded, single-process concurrent programming model based on cooperative multitasking. Coroutines (declared with `async def`) can pause their execution at `await` expressions, returning control to the event loop. The event loop monitors these suspended coroutines (often via non-blocking I/O multiplexing like `select` or `epoll`) and resumes them when their awaited operation completes.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
N/A

## K. Library / Production Implementation (if applicable)
Under the hood, `asyncio` in Python uses `epoll` (Linux), `kqueue` (macOS), or `IOCP` (Windows) to wait for file descriptors to become readable or writable without blocking the CPU thread.

## L. Trace (walk through example)
1. `asyncio.run(main())` starts the event loop.
2. `main()` calls `await basic_async()`.
3. `basic_async()` calls `await fetch_data(1, 1.0)`.
4. `fetch_data` hits `await asyncio.sleep(1.0)`. Control goes back to the event loop.
5. The event loop checks for other ready tasks (none at this instant).
6. 1 second later, the sleep completes. The event loop wakes up `fetch_data`.
7. `fetch_data` finishes and returns to `basic_async()`.

## M. Complexity
- **Time Complexity:** O(N / concurrency_level). Concurrency allows tasks that wait on I/O to overlap perfectly in time.
- **Space Complexity:** O(T) where T is the number of concurrent tasks (coroutine objects and event loop tracking).

## N. Common Mistakes
1. **Blocking the Event Loop:** Using synchronous blocking calls like `time.sleep()` or `requests.get()` inside an `async def`. This freezes the entire thread, defeating the purpose of asyncio.
2. **Forgetting `await`:** Calling an async function without `await` returns a coroutine object, but doesn't actually execute it.

## O. Common Confusions
**Asyncio vs Threading:** Threading is preemptive (OS decides when to switch threads). Asyncio is cooperative (you decide when to switch using `await`). Use multiprocessing for CPU-bound tasks, asyncio for I/O-bound tasks.

## P. When To Use
- High-concurrency I/O-bound applications (e.g., WebSockets, chat servers, web scrapers).
- Microservices making many API calls.

## Q. When NOT To Use
- CPU-bound tasks (image processing, heavy math). Asyncio won't speed these up; you need `multiprocessing`.
- When your ecosystem is mostly synchronous libraries (like `requests` or `SQLAlchemy`'s sync mode), as wrapping everything in executors can be cumbersome.

## R. Trade-offs
- **Pros:** Massive scalability, low memory overhead compared to threads, no complex thread locking/race conditions.
- **Cons:** "Viral" nature (async functions must be awaited by other async functions), steep learning curve, hard to debug.

## S. Debugging
- Set `PYTHONASYNCIODEBUG=1` environment variable.
- Use `loop.set_debug(True)` to print warnings about coroutines taking too long or not being awaited.

## T. Memory Hook (a short memorable principle)
"Yield to the Loop" - `await` means "I'm pausing; event loop, take the wheel!"

## U. Active Recall (questions before answers)
1. What does `await` do? (It yields control back to the event loop while waiting for an operation).
2. What happens if you run `time.sleep(10)` in an async function? (The entire event loop hangs for 10 seconds).

## V. Practice (exercises)
- Modify `intermediate_async` to fetch 10 URLs concurrently using `aiohttp`.
- Write an async generator that yields a number every second.

## W. Interview Question
"What is the difference between asyncio, threading, and multiprocessing in Python?"
*Answer:* Multiprocessing uses multiple CPU cores for CPU-bound tasks. Threading uses OS threads for I/O bound tasks but has context-switching overhead. Asyncio uses a single thread and cooperative multitasking for highly efficient, massive I/O bound concurrency.

## X. Project Connection
Can be used to build a concurrent web scraper that fetches 1,000 pages simultaneously in seconds instead of minutes.
"""

import asyncio
import time
from typing import List


# Basic Implementation: async / await
async def fetch_data(id: int, delay: float) -> dict:
    """Simulates an asynchronous network fetch."""
    print(f"Task {id}: Starting fetch...")
    await asyncio.sleep(delay) # Non-blocking sleep yields control to event loop
    print(f"Task {id}: Finished fetch.")
    return {"id": id, "data": f"content-{id}"}

async def basic_async() -> None:
    print("\n--- Basic Asyncio ---")
    start = time.time()
    
    # Await them sequentially (slow)
    res1 = await fetch_data(1, 1.0)
    res2 = await fetch_data(2, 1.0)
    
    print(f"Sequential async took {time.time() - start:.4f}s")


# Intermediate Implementation: asyncio.gather for Concurrency
async def intermediate_async() -> None:
    print("\n--- Concurrent Asyncio (gather) ---")
    start = time.time()
    
    # Run tasks concurrently
    # The event loop runs them together, switching context on `await`
    results = await asyncio.gather(
        fetch_data(1, 1.0),
        fetch_data(2, 1.0),
        fetch_data(3, 1.0)
    )
    
    print(f"Results: {results}")
    print(f"Concurrent async took {time.time() - start:.4f}s")


# Advanced Implementation: Background Tasks and Blocking Code
def blocking_io() -> str:
    """A synchronous, blocking function (e.g., requests.get)."""
    time.sleep(1.0)
    return "Blocking IO done"

async def advanced_async() -> None:
    print("\n--- Advanced Asyncio ---")
    
    # 1. Background Tasks (Fire and forget)
    task = asyncio.create_task(fetch_data(99, 0.5))
    print("Background task created, doing other things...")
    await asyncio.sleep(0.1)
    
    # Wait for the background task to finish before proceeding
    res = await task
    print(f"Background task result: {res}")
    
    # 2. Running blocking code in an executor
    loop = asyncio.get_running_loop()
    print("Running blocking function in ThreadPoolExecutor...")
    start = time.time()
    blocking_result = await loop.run_in_executor(None, blocking_io)
    print(f"Result: {blocking_result}, took {time.time() - start:.4f}s")


# Performance Analysis
def analyze_performance() -> None:
    print("\n--- Performance Analysis ---")
    print("Asyncio vs Threading:")
    print("- Asyncio can handle tens of thousands of connections (e.g., WebSockets).")
    print("- Threading overhead becomes huge past a few hundred threads.")
    print("- Asyncio requires an 'async to the core' ecosystem (e.g., aiohttp, asyncpg).")

# Edge Cases
def handle_edge_cases() -> None:
    print("\n--- Edge Cases ---")
    async def bad_async():
        # NEVER do this in an async function!
        time.sleep(0.1) # Blocks the ENTIRE event loop
        return True
        
    print("Warning: time.sleep() inside async blocks the entire event loop.")
    print("Always use await asyncio.sleep().")


# Interview Challenge
"""
Challenge: Write an async function that times out if a task takes too long.
"""
async def timeout_challenge() -> None:
    print("\n--- Timeout Challenge ---")
    try:
        # Require task to finish in 0.5s, but it takes 1.0s
        result = await asyncio.wait_for(fetch_data(100, 1.0), timeout=0.5)
        print(result)
    except asyncio.TimeoutError:
        print("Task 100 timed out successfully!")


# Tests
def run_tests() -> None:
    print("\nAll async examples will be executed by asyncio.run() in the main block.")

async def main() -> None:
    await basic_async()
    await intermediate_async()
    await advanced_async()
    await timeout_challenge()

if __name__ == "__main__":
    print("--- Running Asyncio Examples ---")
    # Python 3.7+ standard way to start an asyncio program
    asyncio.run(main())
    analyze_performance()
    handle_edge_cases()
    run_tests()
