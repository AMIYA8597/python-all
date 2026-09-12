"""
## A. Concept Name
Advanced Concurrency in Python

## B. One-Sentence Definition
Concurrency in Python involves executing multiple tasks simultaneously or seemingly simultaneously using threads, processes, or asynchronous event loops to optimize I/O or CPU-bound operations.

## C. Why Does This Exist?
To maximize resource utilization. Programs often wait for external resources (I/O, like networks or disks) or need to perform heavy computations. Concurrency models allow the program to do other work while waiting or to utilize multiple CPU cores for parallel processing.

## D. Intuition
Imagine a chef in a kitchen.
- **Sequential**: The chef chops onions, waits for water to boil, then cooks pasta. (Inefficient)
- **Multithreading**: The chef chops onions while occasionally checking the boiling water. (Good for waiting/I/O)
- **Multiprocessing**: Multiple chefs work in separate kitchens simultaneously. (Good for heavy work/CPU)
- **Asyncio**: A highly organized single chef who starts boiling water, immediately moves to chopping onions, and gets alerted exactly when the water boils. (Massive concurrent waiting)

## E. Real-Life Analogy
- Multithreading: A call center agent handling multiple chat windows, switching between customers while waiting for them to type.
- Multiprocessing: Multiple separate call center agents, each handling their own customer simultaneously.
- Asyncio: A single ultra-efficient agent using an automated ticket system that notifies them exactly when a customer has replied, allowing them to handle thousands of chats without sitting idle.

## F. Mental Model
- **Process**: A heavy, isolated box with its own Python interpreter and memory. Bypasses the GIL.
- **Thread**: A lighter worker inside a single process box. Shares memory but is restricted by the GIL (only one thread runs Python code at a time).
- **Asyncio Event Loop**: A single worker inside a single thread that juggles multiple tasks by actively yielding control when waiting for I/O.

## G. Visual Explanation
CPU Bound Task:
Process 1 [========================]
Process 2 [========================]  -> True parallelism

I/O Bound Task (Asyncio):
Task 1: [Req]->(wait)...............->[Resp]
Task 2:        [Req]->(wait)........->[Resp]
Task 3:               [Req]->(wait).->[Resp]
Loop  : [Work][Work]  (Idle)        [W][W][W] -> Cooperative multitasking

## H. Formal Explanation
Python provides three primary paradigms for concurrency:
1. `multiprocessing`: Spawns OS processes. Circumvents the Global Interpreter Lock (GIL) enabling true parallelism on multicore CPUs. High overhead for creation and IPC (Inter-Process Communication).
2. `threading`: Uses OS threads. Limited by the GIL, meaning it provides concurrency but not true parallelism for Python bytecodes. However, the GIL is released during I/O operations (like network or disk reads), making it useful for I/O-bound tasks.
3. `asyncio`: Provides single-threaded, single-process concurrent code using coroutines, multiplexing I/O access over sockets and other resources, running an event loop.

## I. Mathematical Foundation (if applicable)
Amdahl's Law applies to multiprocessing:
Speedup = 1 / ( (1 - P) + P/N )
Where P is the proportion of the program that can be made parallel, and N is the number of processors. The GIL makes P near 0 for multithreading on CPU-bound Python tasks.

## J. From-Scratch Implementation (if applicable)
(See code section below for manual thread/process pool implementations)

## K. Library / Production Implementation (if applicable)
(See code section below for `concurrent.futures` and `asyncio` usage)

## L. Trace (walk through example)
For Asyncio tasks:
1. `fetch_data(1)` starts, hits `await asyncio.sleep(0.2)`. It yields control back to the event loop.
2. The event loop immediately starts `fetch_data(2)`, which hits `await asyncio.sleep(0.3)` and yields.
3. The event loop immediately starts `fetch_data(3)`, which hits `await asyncio.sleep(0.1)` and yields.
4. At t=0.1s, `fetch_data(3)` wakes up and finishes.
5. At t=0.2s, `fetch_data(1)` wakes up and finishes.
6. At t=0.3s, `fetch_data(2)` wakes up and finishes.
Total time is ~0.3s, not 0.6s.

## M. Complexity
- Time Complexity: Multiprocessing divides time by N cores for highly parallel tasks. Asyncio processes concurrent I/O in O(max(I/O times)).
- Space Complexity: Multiprocessing requires O(N) memory overhead (copies the interpreter). Threading is lighter. Asyncio has the lowest overhead (just small state machines per task).

## N. Common Mistakes
- Using multithreading for CPU-bound tasks (makes it slower due to GIL contention).
- Calling a blocking synchronous function (like `time.sleep` or `requests.get`) inside an `async def` function, which completely blocks the asyncio event loop.
- Passing non-picklable objects to a `ProcessPoolExecutor`.

## O. Common Confusions
- "Why does Python have a GIL?" It simplifies CPython's memory management (reference counting) by making it thread-safe.
- "Is Asyncio faster than Threading?" Not in raw speed, but it uses much less memory, allowing you to have 10,000+ concurrent connections instead of just a few hundred threads.

## P. When To Use
- `multiprocessing`: Number crunching, image processing, heavy data analysis (CPU-bound).
- `threading`: Legacy I/O bound tasks, GUI applications, calling blocking C extensions.
- `asyncio`: Massive I/O (web servers like FastAPI, websockets, web scraping thousands of pages).

## Q. When NOT To Use
- Don't use `multiprocessing` for simple I/O tasks; the IPC overhead outweighs the benefits.
- Don't use `asyncio` for CPU-bound tasks without delegating to a `ProcessPoolExecutor`.

## R. Trade-offs
- Multiprocessing: True parallelism vs High memory and IPC overhead.
- Threading: Easy to implement vs GIL limitations and thread-safety bugs (race conditions).
- Asyncio: Extremely lightweight and no race conditions vs "Infectious" (requires changing all code to async/await syntax) and hard to debug.

## S. Debugging
- Use `asyncio.run(main(), debug=True)` to catch coroutines that were never awaited or blocking calls that stall the event loop.
- Watch out for deadlocks in threading/multiprocessing when acquiring multiple locks or joining cyclically.

## T. Memory Hook (a short memorable principle)
- CPU bound? Use Processes.
- I/O bound and existing sync code? Use Threads.
- I/O bound and massive scale? Use Asyncio.

## U. Active Recall (questions before answers)
1. What does the GIL prevent? (Multiple threads executing Python bytecode at once).
2. What happens if you use `time.sleep()` inside `asyncio`? (The entire event loop freezes).

## V. Practice (exercises)
1. Modify the hybrid example to run a CPU-bound task in a `ProcessPoolExecutor` from within an asyncio event loop.
2. Write a script that downloads 5 webpages using `threading` vs `asyncio` and compare the syntax and speed.

## W. Interview Question
"Explain the difference between concurrent.futures.ThreadPoolExecutor and asyncio. When would you choose one over the other?"
(Answer: ThreadPool uses OS threads and is good for wrapping existing blocking libraries. Asyncio uses a single thread with cooperative multitasking, which is more scalable for high concurrency but requires async-compatible libraries like `aiohttp`).

## X. Project Connection
Used in web scrapers to download pages quickly, in web frameworks (FastAPI) to handle thousands of concurrent users, and in data engineering pipelines to process large chunks of data in parallel.
"""

import time
import asyncio
import concurrent.futures
from typing import List, AsyncGenerator


# --- Basic Implementation: ThreadPool vs ProcessPool ---
def cpu_bound_task(n: int) -> int:
    """A CPU intensive task."""
    count = 0
    for i in range(n):
        count += i
    return count

def run_multiprocessing(task_sizes: List[int]) -> List[int]:
    """Uses separate processes to bypass the GIL."""
    # Using max_workers=2 to prevent overloading testing environments
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(cpu_bound_task, task_sizes))
    return results

def run_multithreading(task_sizes: List[int]) -> List[int]:
    """
    Uses threads. For CPU bound tasks in Python, this is often SLOWER 
    than sequential execution due to GIL contention overhead.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(cpu_bound_task, task_sizes))
    return results


# --- Intermediate Implementation: Asyncio Basics ---
async def fetch_data(id: int, delay: float) -> str:
    """Simulates an asynchronous I/O operation (like an HTTP request)."""
    # print(f"Task {id}: Starting fetch")
    await asyncio.sleep(delay)  # Yields control back to the event loop
    # print(f"Task {id}: Finished fetch")
    return f"Data {id}"

async def run_asyncio_tasks() -> List[str]:
    """Runs multiple async tasks concurrently."""
    # Create a list of tasks
    tasks = [
        fetch_data(1, 0.2),
        fetch_data(2, 0.3),
        fetch_data(3, 0.1)
    ]
    # Gather runs them concurrently and waits for all to finish
    results = await asyncio.gather(*tasks)
    return results


# --- Advanced Implementation: Combining Asyncio with ThreadPools ---
def blocking_io_task() -> str:
    """A synchronous, blocking I/O task (e.g., requests.get)."""
    time.sleep(0.2)
    return "Blocking result"

async def run_hybrid_async() -> str:
    """
    Runs a synchronous blocking function inside an asyncio event loop 
    by delegating it to a background thread pool.
    """
    loop = asyncio.get_running_loop()
    # Run the blocking task in the default ThreadPoolExecutor
    result = await loop.run_in_executor(None, blocking_io_task)
    return result


# --- Interview Challenge ---
async def async_number_generator(n: int) -> AsyncGenerator[int, None]:
    """An async generator that yields numbers with a small delay."""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async def test_generator() -> List[int]:
    """Consumes the async generator."""
    results = []
    async for num in async_number_generator(3):
        results.append(num)
    return results


# --- Tests ---
def run_tests() -> None:
    print("Testing Advanced Concurrency...")

    # CPU Bound Tests
    task_sizes = [5000000, 5000000]
    
    start = time.time()
    res_seq = [cpu_bound_task(n) for n in task_sizes]
    time_seq = time.time() - start

    start = time.time()
    res_mp = run_multiprocessing(task_sizes)
    time_mp = time.time() - start

    assert res_seq == res_mp
    print(f"Sequential CPU Time: {time_seq:.4f}s")
    print(f"Multiprocessing CPU Time: {time_mp:.4f}s")

    # Asyncio Tests
    start = time.time()
    async_res = asyncio.run(run_asyncio_tasks())
    time_async = time.time() - start
    
    assert async_res == ["Data 1", "Data 2", "Data 3"]
    # Total time should be approx max(delay) which is 0.3, not sum(0.2+0.3+0.1)=0.6
    assert 0.3 <= time_async < 0.4
    print(f"Asyncio Execution Time: {time_async:.4f}s")

    # Hybrid Test
    hybrid_res = asyncio.run(run_hybrid_async())
    assert hybrid_res == "Blocking result"

    # Async Generator Test
    gen_res = asyncio.run(test_generator())
    assert gen_res == [0, 1, 2]

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
