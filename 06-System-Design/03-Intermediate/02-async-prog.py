"""
## A. Concept Name
Asynchronous Programming in Python

## B. Learning Objectives
1. Understand the Event Loop and cooperative multitasking.
2. Differentiate between I/O-bound and CPU-bound tasks.
3. Use async/await syntax to write non-blocking code.
4. Manage concurrent tasks using asyncio.gather and asyncio.create_task.

## C. Concept Explanation
Asynchronous programming allows a single thread to handle multiple operations concurrently.
Instead of blocking the thread while waiting for I/O (like network requests or file reads),
the control is yielded back to the Event Loop, which can start or resume other tasks.
This is highly efficient for I/O-bound workloads but does not speed up CPU-bound workloads 
due to the Global Interpreter Lock (GIL) and single-threaded nature of asyncio.

## D. Industry Use Cases
- High-concurrency web frameworks (FastAPI, AIOHTTP).
- Web scraping multiple pages simultaneously.
- Chat servers and WebSocket implementations.
- Microservice orchestration requiring multiple downstream API calls.

## X. Project Connection
This concept is foundational for building scalable, high-throughput applications, such as real-time chat servers or web scrapers, where minimizing I/O wait times is critical for overall performance.
"""

import asyncio
import time
from typing import List, Dict, Any

# ==========================================
# 1. Synchronous vs Asynchronous I/O
# ==========================================
def sync_fetch(task_id: int) -> str:
    """Simulates a blocking I/O call."""
    time.sleep(1) # Blocks the entire thread
    return f"Result {task_id}"

async def async_fetch(task_id: int) -> str:
    """Simulates a non-blocking I/O call."""
    await asyncio.sleep(1) # Yields control to the event loop
    return f"Result {task_id}"

# ==========================================
# 2. Basic Async Execution
# ==========================================
async def run_basic_async():
    start = time.time()
    # Running sequentially (bad practice for async)
    res1 = await async_fetch(1)
    res2 = await async_fetch(2)
    duration = time.time() - start
    print(f"Sequential async took {duration:.2f}s") # ~2 seconds
    return [res1, res2]

# ==========================================
# 3. Professional Implementation: Concurrent Task Gathering
# ==========================================
async def fetch_user_data(user_id: int) -> Dict[str, Any]:
    await asyncio.sleep(0.5)
    return {"id": user_id, "data": "profile_info"}

async def fetch_user_orders(user_id: int) -> List[str]:
    await asyncio.sleep(0.8)
    return ["order_1", "order_2"]

async def fetch_user_dashboard(user_id: int) -> Dict[str, Any]:
    """
    Fetches user data and orders concurrently.
    The total time will be roughly the max of the individual times (~0.8s),
    rather than the sum (~1.3s).
    """
    start = time.time()
    
    # asyncio.gather runs awaitables concurrently
    profile, orders = await asyncio.gather(
        fetch_user_data(user_id),
        fetch_user_orders(user_id)
    )
    
    duration = time.time() - start
    
    return {
        "profile": profile,
        "orders": orders,
        "fetch_time_seconds": round(duration, 2)
    }

# ==========================================
# 4. Handling Timeouts and Exceptions
# ==========================================
async def unreliable_fetch():
    await asyncio.sleep(2)
    return "Success"

async def safe_fetch():
    try:
        # Wrap the coroutine in wait_for to enforce a timeout
        result = await asyncio.wait_for(unreliable_fetch(), timeout=1.0)
        return result
    except asyncio.TimeoutError:
        return "Fallback Data"
    except Exception as e:
        return f"Error: {e}"

# ==========================================
# 5. Complexity Analysis & Interview Challenge
# ==========================================
"""
Complexity:
- Time: Asyncio drastically reduces wait times for I/O bound tasks by overlapping waiting periods.
  Time(Total) = max(Time(Task1), Time(Task2)...) instead of sum().
- Space: Minimal overhead per coroutine compared to OS Threads.

# Interview Challenge
Q: How would you handle CPU-bound work in an asyncio application?
A: Asyncio runs on a single thread. A CPU-bound task (like heavy math or image processing) 
   will block the event loop, freezing all other async tasks. 
   To solve this, offload the CPU-bound task to a separate process using 
   `loop.run_in_executor(ProcessPoolExecutor(), heavy_function)`.
"""

def main():
    print("Running Async Programming Tests...")
    
    # Ensure a fresh event loop
    loop = asyncio.get_event_loop()
    
    # Test basic async
    basic_res = loop.run_until_complete(run_basic_async())
    assert basic_res == ["Result 1", "Result 2"]
    
    # Test concurrent dashboard fetch
    dashboard = loop.run_until_complete(fetch_user_dashboard(101))
    assert dashboard["profile"]["id"] == 101
    assert len(dashboard["orders"]) == 2
    assert dashboard["fetch_time_seconds"] < 1.0 # Proves concurrency
    
    # Test timeout handling
    safe_res = loop.run_until_complete(safe_fetch())
    assert safe_res == "Fallback Data"
    
    print("All async tests passed!")

if __name__ == "__main__":
    main()
