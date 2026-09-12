\"\"\"
Module: 05-perf-web.py
Topic: Web Performance Optimization in Python

This module covers essential techniques for optimizing web applications in Python.
We will explore caching strategies, asynchronous I/O, and basic profiling.

Why it matters:
In real-world web development, responding to requests quickly is critical for user 
experience and SEO. Handling high traffic efficiently saves server costs and prevents 
downtime. Python, being an interpreted language, requires careful optimization, 
especially when dealing with I/O bound tasks like database queries or external API calls.

Learning Objectives:
1. Understand the difference between I/O bound and CPU bound bottlenecks.
2. Implement caching mechanisms to store frequently accessed data.
3. Utilize asynchronous programming (asyncio) to handle concurrent requests.
4. Profile code to identify performance bottlenecks.

Beginner Explanation:
Imagine a restaurant. If the chef (CPU) has to wait for ingredients to be delivered 
(I/O) before starting to cook the next meal, the restaurant will be slow. 
Asynchronous programming is like having the chef work on another dish while waiting 
for ingredients. Caching is like keeping a stock of pre-chopped vegetables ready to use.

Advanced Explanation:
Web performance optimization in Python typically revolves around mitigating the Global 
Interpreter Lock (GIL) for CPU-bound tasks using multiprocessing, and leveraging the 
Event Loop for I/O-bound tasks using asynchronous frameworks (like FastAPI or aiohttp).
Caching strategies (e.g., LRU Cache, Redis) reduce latency by storing serialized 
computations or database results in fast memory. Profiling tools (cProfile, line_profiler) 
provide deterministic metrics on function call frequencies and execution times.
\"\"\"

import time
import asyncio
from functools import lru_cache
from typing import Dict, Any, List
import cProfile
import pstats
import io

# ==========================================
# 1. Basic Caching Implementation
# ==========================================

# Using built-in LRU (Least Recently Used) cache for simple memoization.
@lru_cache(maxsize=128)
def fetch_user_data_simulated(user_id: int) -> Dict[str, Any]:
    \"\"\"
    Simulates a slow database call to fetch user data.
    The lru_cache decorator caches the results for recent user_ids.
    \"\"\"
    time.sleep(1) # Simulate slow I/O
    return {\"id\": user_id, \"name\": f\"User_{user_id}\", \"status\": \"active\"}


# ==========================================
# 2. Professional Implementation: Async I/O
# ==========================================

async def async_fetch_data(resource_id: int) -> str:
    \"\"\"
    Simulates an asynchronous HTTP request or DB call.
    \"\"\"
    await asyncio.sleep(0.5) # Non-blocking sleep
    return f\"Data for resource {resource_id}\"

async def process_multiple_requests(resource_ids: List[int]) -> List[str]:
    \"\"\"
    Concurrently processes multiple I/O bound requests using asyncio.gather.
    This drastically reduces overall execution time compared to sequential execution.
    \"\"\"
    tasks = [async_fetch_data(rid) for rid in resource_ids]
    # Run all tasks concurrently and wait for all to finish
    results = await asyncio.gather(*tasks)
    return results

# ==========================================
# 3. Profiling Example
# ==========================================

def cpu_bound_task() -> int:
    \"\"\"A poorly optimized CPU bound task for profiling.\"\"\"
    total = 0
    for i in range(1000000):
        total += i * i
    return total

def profile_code(func, *args, **kwargs):
    \"\"\"Utility function to profile another function.\"\"\"
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args, **kwargs)
    pr.disable()
    
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(10) # Print top 10 lines
    print(s.getvalue())
    return result


# ==========================================
# Complexity Analysis
# ==========================================
# Async I/O:
# Time Complexity: O(max(T1, T2, ... Tn)) where Ti is the time of the i-th task.
#   (Assuming no CPU blocking and infinite concurrency limits).
# Space Complexity: O(N) to store the tasks and results.

# LRU Cache:
# Time Complexity: O(1) for lookup, insertion, and deletion.
# Space Complexity: O(K) where K is the maxsize of the cache.


# ==========================================
# Interview Challenge
# ==========================================
# Challenge: You are building a rate limiter for an API endpoint.
# Implement a simple Token Bucket rate limiter algorithm in Python.
# Considerations: Concurrency issues if used in a multi-threaded WSGI environment.


if __name__ == \"__main__\":
    print(\"--- Demonstrating Caching ---\")
    start = time.time()
    fetch_user_data_simulated(1) # Slow
    print(f\"First call took: {time.time() - start:.4f}s\")
    
    start = time.time()
    fetch_user_data_simulated(1) # Fast (Cached)
    print(f\"Second call took: {time.time() - start:.4f}s\")
    
    assert fetch_user_data_simulated.cache_info().hits == 1

    print(\"\\n--- Demonstrating Async I/O ---\")
    start = time.time()
    # Running the async loop
    results = asyncio.run(process_multiple_requests([1, 2, 3, 4, 5]))
    duration = time.time() - start
    print(f\"Async processing of 5 tasks took: {duration:.4f}s\")
    print(f\"Results: {results}\")
    # 5 tasks of 0.5s each should take roughly 0.5s concurrently, not 2.5s
    assert duration < 1.0 

    print(\"\\n--- Demonstrating Profiling ---\")
    profile_code(cpu_bound_task)
    print(\"All tests passed successfully.\")
