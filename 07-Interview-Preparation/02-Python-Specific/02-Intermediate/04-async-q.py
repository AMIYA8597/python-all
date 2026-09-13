"""
Module: Asynchronous Programming

Learning Objectives:
1. Understand the core concepts of asynchronous programming in Python (`asyncio`).
2. Learn how to define and run coroutines using `async` and `await`.
3. Understand concurrency vs. parallelism.
4. Execute multiple asynchronous tasks concurrently using `asyncio.gather`.

Interview Questions Covered:
- What is the difference between synchronous, multithreading, multiprocessing, and asynchronous programming in Python?
- How do you run multiple asynchronous tasks at the same time?
- Explain the Global Interpreter Lock (GIL) and how async relates to it.
"""

import asyncio
import time
from typing import List, Any

# ---------------------------------------------------------
# Concept 1: Basic Coroutines
# ---------------------------------------------------------
async def fetch_data(id: int, delay: float) -> dict:
    """Simulates an asynchronous I/O operation (e.g., network request)."""
    print(f"Task {id}: Starting fetch (delay {delay}s)...")
    await asyncio.sleep(delay)  # Yields control back to the event loop
    print(f"Task {id}: Finished fetch!")
    return {"id": id, "data": f"Sample data {id}"}

# ---------------------------------------------------------
# Concept 2: Concurrent Execution
# ---------------------------------------------------------
async def main_async() -> List[dict]:
    """Runs multiple fetch operations concurrently."""
    start_time = time.time()
    
    # Create a list of coroutines
    tasks = [
        fetch_data(1, 1.5),
        fetch_data(2, 0.5),
        fetch_data(3, 1.0)
    ]
    
    # Run them concurrently and wait for all to complete
    print("Running tasks concurrently...")
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"All tasks completed in {end_time - start_time:.2f} seconds.")
    return results

# ---------------------------------------------------------
# Tests and Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    # In Python 3.7+, asyncio.run is the preferred way to execute the main coroutine
    print("--- Asyncio Example ---")
    results = asyncio.run(main_async())
    print("\nResults collected:")
    for res in results:
        print(res)
