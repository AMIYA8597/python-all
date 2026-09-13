"""
Concurrency: Thread Pools and Futures

Learning Objectives:
1. Simplify threading using `concurrent.futures.ThreadPoolExecutor`.
2. Understand the concept of a `Future` object.
3. Learn how to map functions to iterables concurrently.
4. Handle exceptions across thread boundaries gracefully.

Concept Explanation:
Manually managing `threading.Thread` objects, starting them, and joining them 
is tedious and prone to resource exhaustion (spawning 1000 threads will crash your OS).
A ThreadPool limits the maximum number of concurrent threads. The `concurrent.futures` 
module provides a high-level API for this. It returns `Future` objects, which are 
promises that a result will eventually be available.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

# --- Basic Implementation ---
def download_image_mock(img_id: int) -> str:
    """Mock an I/O bound task (like downloading an image)."""
    # Simulate variable latency
    time.sleep(0.1 + (img_id % 3) * 0.1) 
    return f"Image_{img_id}_Data"

# --- Intermediate Implementation ---
def execute_with_map(image_ids: List[int], max_workers: int = 4) -> List[str]:
    """Use executor.map to process iterables concurrently.
    Note: map() returns results in the EXACT order of the input iterable!"""
    results = []
    # The context manager automatically waits for all threads to finish on exit
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Blocks until all are done, yields in original order
        for result in executor.map(download_image_mock, image_ids):
            results.append(result)
    return results

# --- Advanced Implementation / Performance Analysis ---
def execute_with_submit(image_ids: List[int], max_workers: int = 4) -> List[str]:
    """Use executor.submit and as_completed.
    Note: Yields results AS SOON AS THEY FINISH, regardless of input order!"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit returns a Future object immediately
        futures = [executor.submit(download_image_mock, i) for i in image_ids]
        
        # as_completed yields futures as they complete
        for future in as_completed(futures):
            # .result() gets the return value of the function
            results.append(future.result())
    return results

def compare_performance():
    ids = list(range(10))
    
    print("Using executor.map (Preserves Order):")
    start = time.perf_counter()
    res_map = execute_with_map(ids)
    print(f"  Time: {time.perf_counter() - start:.2f}s")
    print(f"  Order: {[r.split('_')[1] for r in res_map]}")
    
    print("\nUsing executor.submit + as_completed (First-finished, First-yielded):")
    start = time.perf_counter()
    res_sub = execute_with_submit(ids)
    print(f"  Time: {time.perf_counter() - start:.2f}s")
    print(f"  Order: {[r.split('_')[1] for r in res_sub]}")

# --- Edge Cases ---
def exception_handling_edge_case():
    """Exceptions inside threads are silent until you call future.result()!"""
    def crashy_task(x: int):
        if x == 2:
            raise ValueError("Task 2 Crashed!")
        return x * 2
        
    print("\n[Exception Handling]")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(crashy_task, i): i for i in range(4)}
        
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                res = future.result() # Exception is raised HERE!
                print(f"Task {task_id} success: {res}")
            except Exception as e:
                print(f"Task {task_id} failed: {repr(e)}")

# --- Interview Challenge ---
"""
Challenge: If you submit 100 tasks to a ThreadPoolExecutor with max_workers=5,
how many threads are created?
Answer: Only 5 threads are created. The remaining 95 tasks wait in an internal 
queue until a worker thread becomes available.
"""

# --- Tests ---
def run_tests():
    ids = [1, 2, 3]
    assert len(execute_with_map(ids)) == 3
    print("\nAll tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Thread Pools ---")
    compare_performance()
    exception_handling_edge_case()
    run_tests()
