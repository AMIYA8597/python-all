"""
# ==============================================================================
# LABORATORY: ADVANCED CONCURRENCY (SEMAPHORES, IPC, SHARED MEMORY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When scaling an async scraper or API caller, if you spawn 10,000 tasks at once, 
# you will instantly get rate-limited (HTTP 429) or crash your router. You MUST 
# use Semaphores. When using multiprocessing, processes DO NOT share memory. 
# Communicating between them requires understanding IPC (Inter-Process Communication) 
# and explicitly shared memory arrays.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Control async concurrency limits using `asyncio.Semaphore`.
# - Use `asyncio.Queue` for Producer/Consumer pipelines.
# - Understand IPC (Inter-Process Communication) in multiprocessing.
# - Use `multiprocessing.Queue` to safely pass data between processes.
# - Understand `multiprocessing.shared_memory` (Python 3.8+).
#
# ==============================================================================
"""

import time
import asyncio
import multiprocessing
from multiprocessing import shared_memory

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ASYNCIO SEMAPHORES (RATE LIMITING)
# ==============================================================================

async def limited_api_call(id: int, sem: asyncio.Semaphore):
    """
    The Semaphore limits how many of these tasks can execute SIMULTANEOUSLY.
    If the semaphore allows 3, the 4th task pauses at the `async with` block 
    until one of the first 3 finishes.
    """
    async with sem:
        print(f"  [API] Task {id} starting...")
        await asyncio.sleep(0.5) # Simulating network request
        print(f"  [API] Task {id} finished.")

async def demonstrate_semaphores():
    section_header("Asyncio: Semaphores for Rate Limiting")
    
    # We create 10 tasks, but only allow 3 to run at exactly the same time.
    sem = asyncio.Semaphore(3)
    
    print("Spawning 10 tasks with a concurrency limit of 3...")
    start = time.perf_counter()
    
    tasks = [limited_api_call(i, sem) for i in range(1, 11)]
    await asyncio.gather(*tasks)
    
    print(f"Completed in {time.perf_counter() - start:.2f}s")


# ==============================================================================
# 4. ASYNCIO QUEUES (PRODUCER / CONSUMER)
# ==============================================================================

async def producer(queue: asyncio.Queue):
    print("  [Producer] Starting...")
    for i in range(1, 6):
        await asyncio.sleep(0.2) # Simulating producing data
        item = f"Item-{i}"
        await queue.put(item)
        print(f"  [Producer] Put {item} into queue.")
        
async def consumer(id: int, queue: asyncio.Queue):
    print(f"  [Consumer {id}] Starting...")
    while True:
        # Pauses until an item is available in the queue
        item = await queue.get()
        print(f"  [Consumer {id}] Processing {item}...")
        await asyncio.sleep(0.5) # Simulating processing time
        
        # Tell the queue this item is fully processed
        queue.task_done()

async def demonstrate_async_queues():
    section_header("Asyncio: Producer/Consumer Queues")
    
    queue = asyncio.Queue()
    
    # Fire up the producer
    prod = asyncio.create_task(producer(queue))
    
    # Fire up 2 concurrent consumers
    cons1 = asyncio.create_task(consumer(1, queue))
    cons2 = asyncio.create_task(consumer(2, queue))
    
    # Wait for the producer to finish putting items in
    await prod
    
    # Wait for the queue to be completely empty (all items task_done)
    await queue.join()
    
    # Cancel the infinite loop consumers
    cons1.cancel()
    cons2.cancel()
    print("  [System] All items processed, consumers cancelled.")


# ==============================================================================
# 5. MULTIPROCESSING: IPC (INTER-PROCESS COMMUNICATION)
# ==============================================================================

def mp_worker(queue: multiprocessing.Queue):
    """This runs in an entirely different OS process!"""
    data = queue.get() # Receive data from main process
    print(f"  [Worker Process] Received data: {data}")
    
    # Modify data and send it back
    data.append("PROCESSED_BY_WORKER")
    queue.put(data)

def demonstrate_ipc():
    """
    Because processes have SEPARATE memory spaces, you cannot just pass a list 
    and expect modifications to show up in the main process.
    You MUST use an IPC mechanism like multiprocessing.Queue (which serializes 
    the data using pickle and passes it through an OS pipe).
    """
    section_header("Multiprocessing IPC (Queues)")
    
    # Create a process-safe queue
    q = multiprocessing.Queue()
    
    data_to_send = ["Hello", "World"]
    print(f"  [Main Process] Sending data: {data_to_send}")
    q.put(data_to_send)
    
    # Spawn the process
    p = multiprocessing.Process(target=mp_worker, args=(q,))
    p.start()
    p.join() # Wait for it to finish
    
    # Retrieve the result
    result = q.get()
    print(f"  [Main Process] Received back: {result}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What happens if you spawn 1000 asyncio tasks making HTTP requests at the same time?
   Answer: You will exhaust local OS sockets, overwhelm the target server, and likely receive HTTP 429 (Too Many Requests) or connection timeouts. You must throttle concurrency using an `asyncio.Semaphore`.

2. Why do we need `queue.task_done()` and `queue.join()`?
   Answer: In a producer/consumer model, the consumers run in an infinite `while True:` loop. `queue.join()` pauses the main program until every item put into the queue has had `queue.task_done()` called on it, ensuring no items are dropped before the program exits.

3. Why can't multiple processes share a standard Python list?
   Answer: Multiprocessing creates entirely new OS processes. The OS isolates their memory spaces for security. A list in Process A physically does not exist in the RAM space of Process B. You must pass data using IPC (Pipes, Queues) which pickles/unpickles the data, or use explicit Shared Memory blocks.
"""

if __name__ == "__main__":
    asyncio.run(demonstrate_semaphores())
    asyncio.run(demonstrate_async_queues())
    
    # Note: On Windows, multiprocessing MUST be protected by __main__ block
    demonstrate_ipc()
    print("\n[SUCCESS] Laboratory: Advanced Concurrency Completed.")
