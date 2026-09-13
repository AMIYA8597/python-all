"""
Concurrency: Asyncio Optimization

Learning Objectives:
1. Understand the concept of Asynchronous I/O and the Event Loop.
2. Implement basic async/await functions (coroutines).
3. Compare `asyncio.gather` vs sequential awaits for concurrent execution.
4. Recognize when asyncio is better than threading (high concurrency I/O).

Concept Explanation:
`asyncio` provides cooperative multitasking using a single thread and an Event Loop. 
Unlike threading, where the OS decides when to switch contexts (preemptive), 
asyncio switches contexts explicitly when it encounters an `await` on an I/O operation. 
This is incredibly lightweight, allowing thousands of concurrent connections on a 
single thread, avoiding the memory overhead of OS threads.
"""

import asyncio
import time
from typing import List

# --- Basic Implementation ---
async def fetch_data(task_id: int, delay: float) -> str:
    """Simulate an asynchronous network request."""
    # await gives control back to the Event Loop while waiting
    await asyncio.sleep(delay)
    return f"Result {task_id}"

# --- Intermediate Implementation ---
async def sequential_execution(n_tasks: int) -> List[str]:
    """Awaits tasks one by one. Defeats the purpose of asyncio!"""
    results = []
    for i in range(n_tasks):
        res = await fetch_data(i, 0.5)
        results.append(res)
    return results

async def concurrent_execution(n_tasks: int) -> List[str]:
    """Uses asyncio.gather to run tasks concurrently."""
    # Create a list of coroutine objects
    coroutines = [fetch_data(i, 0.5) for i in range(n_tasks)]
    # Wait for all of them to finish concurrently
    results = await asyncio.gather(*coroutines)
    return results

# --- Advanced Implementation / Performance Analysis ---
def compare_performance():
    n_tasks = 10
    
    print(f"Executing {n_tasks} tasks (each takes 0.5s)...\n")
    
    # 1. Sequential
    start = time.perf_counter()
    asyncio.run(sequential_execution(n_tasks))
    t_seq = time.perf_counter() - start
    print(f"Sequential Await Time: {t_seq:.2f}s")
    
    # 2. Concurrent
    start = time.perf_counter()
    asyncio.run(concurrent_execution(n_tasks))
    t_conc = time.perf_counter() - start
    print(f"Concurrent Gather Time: {t_conc:.2f}s")
    
    print(f"\nSpeedup: {t_seq/t_conc:.1f}x")

# --- Edge Cases ---
async def blocking_code_edge_case():
    """Blocking CPU operations freeze the entire Event Loop!"""
    import math
    print("\n[Edge Case: Blocking the Loop]")
    
    async def bad_task():
        # Pure CPU task blocks the loop! No other coroutines can run.
        count = 0
        for i in range(10_000_000):
            count += math.isqrt(i)
        return count
        
    async def good_task():
        await asyncio.sleep(0.1)
        print("Good task finished!")
        
    # Because bad_task never awaits, good_task cannot execute until bad_task is done
    await asyncio.gather(bad_task(), good_task())

# --- Interview Challenge ---
"""
Challenge: If you MUST run a blocking CPU-bound function inside an asyncio 
application, how do you prevent it from blocking the event loop?

Answer: Use run_in_executor to offload it to a thread or process pool!
"""
async def offload_blocking_task():
    import math
    loop = asyncio.get_running_loop()
    
    def blocking_math():
        return sum(math.isqrt(i) for i in range(5_000_000))
        
    # Runs in default ThreadPoolExecutor without blocking the event loop
    result = await loop.run_in_executor(None, blocking_math)
    return result

# --- Tests ---
def run_tests():
    # To test async code synchronously, wrap in asyncio.run
    res = asyncio.run(fetch_data(99, 0.01))
    assert res == "Result 99"
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Asyncio ---")
    compare_performance()
    asyncio.run(blocking_code_edge_case())
    run_tests()
