"""
Concurrency and Asyncio in Python

Learning Objectives:
1. Understand the difference between threads, processes, and async tasks.
2. Master the basics of the `asyncio` library (event loops, coroutines, tasks).
3. Identify scenarios where `asyncio` outperforms threading/multiprocessing.
4. Implement concurrent execution of tasks using `asyncio.gather` and `asyncio.as_completed`.

Concept Explanation:
- Threads (via `threading`) are good for I/O-bound tasks but limited by the GIL (Global Interpreter Lock) for CPU-bound tasks.
- Processes (via `multiprocessing`) bypass the GIL by using separate memory spaces, suitable for CPU-bound tasks.
- `asyncio` provides cooperative multitasking using an event loop and coroutines. It is excellent for high-concurrency I/O-bound operations (e.g., network requests, database queries) in a single thread without the overhead of context switching.

Interview Focus:
- How does the GIL affect multithreading in Python?
- Write a simple asyncio program that fetches data from multiple URLs concurrently.
- What is the difference between `asyncio.sleep()` and `time.sleep()`?
"""
import asyncio
import time
from typing import List

# ==========================================
# 1. Basic Asyncio Usage
# ==========================================

async def fetch_data(id: int, delay: float) -> str:
    """Simulates an asynchronous network request or database query."""
    print(f"Task {id}: Starting fetch with delay {delay}s...")
    # asyncio.sleep is non-blocking; it yields control back to the event loop.
    await asyncio.sleep(delay)
    print(f"Task {id}: Finished fetch.")
    return f"Data from task {id}"

async def main_basic():
    """Run tasks sequentially vs concurrently."""
    start_time = time.time()
    
    # Sequential execution (anti-pattern for asyncio)
    # res1 = await fetch_data(1, 1.0)
    # res2 = await fetch_data(2, 2.0)
    
    # Concurrent execution
    # create_task schedules the coroutine on the event loop
    task1 = asyncio.create_task(fetch_data(1, 1.0))
    task2 = asyncio.create_task(fetch_data(2, 2.0))
    
    res1 = await task1
    res2 = await task2
    
    duration = time.time() - start_time
    print(f"Basic execution took {duration:.2f} seconds")
    return [res1, res2]

# ==========================================
# 2. Gathering Multiple Tasks
# ==========================================

async def fetch_batch(ids: List[int]) -> List[str]:
    """Runs a batch of tasks concurrently and returns results in order."""
    tasks = [fetch_data(id, 0.5) for id in ids]
    
    # asyncio.gather runs awaitables concurrently and returns their results.
    # If one task fails, gather will raise the exception immediately (unless return_exceptions=True).
    results = await asyncio.gather(*tasks)
    return results

# ==========================================
# Interview Challenge: Rate Limiting
# ==========================================
# Implement an async function that processes a list of items but limits
# the maximum number of concurrent tasks.

async def process_item(item: int) -> int:
    await asyncio.sleep(0.1) # Simulate work
    return item * 2

async def process_with_limit(items: List[int], limit: int) -> List[int]:
    """Process items with a concurrency limit using asyncio.Semaphore."""
    semaphore = asyncio.Semaphore(limit)
    
    async def sem_task(item: int) -> int:
        async with semaphore:
            return await process_item(item)
            
    tasks = [sem_task(item) for item in items]
    return await asyncio.gather(*tasks)

def test_concurrency():
    print("Testing basic asyncio...")
    # asyncio.run is the main entry point to execute an async function
    results = asyncio.run(main_basic())
    assert results == ["Data from task 1", "Data from task 2"]
    
    print("\nTesting asyncio.gather...")
    batch_results = asyncio.run(fetch_batch([3, 4, 5]))
    assert batch_results == ["Data from task 3", "Data from task 4", "Data from task 5"]
    
    print("\nTesting concurrency limit...")
    start_time = time.time()
    items = list(range(10))
    # 10 items, 0.1s each, limit of 5. Should take ~0.2s total.
    limited_results = asyncio.run(process_with_limit(items, limit=5))
    duration = time.time() - start_time
    assert limited_results == [i * 2 for i in range(10)]
    assert 0.2 <= duration < 0.35 # Rough timing check
    
    print("\nAll concurrency tests passed!")

if __name__ == "__main__":
    test_concurrency()
