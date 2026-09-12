"""
Parallel Algorithm Design

1. Module Description:
   This module demonstrates the principles of Parallel Algorithm Design, specifically 
   focusing on the MapReduce paradigm and parallel sorting (Divide and Conquer). 
   Designing parallel algorithms requires identifying independent tasks that can be 
   executed concurrently without race conditions.

2. Learning Objectives:
   - Understand Data Parallelism vs Task Parallelism.
   - Implement the MapReduce paradigm in pure Python.
   - Learn how to implement parallel divide-and-conquer algorithms like Merge Sort.
   - Master Python's `concurrent.futures` for thread/process synchronization.

3. Concept Explanation:
   - Data Parallelism: The same operation is applied concurrently to different pieces of data.
   - Amdahl's Law: The theoretical maximum speedup of a program using multiple processors 
     is limited by the sequential fraction of the program.
   - MapReduce: A programming model that maps data to key-value pairs (Map phase), 
     shuffles them (often implicit or handled by framework), and then reduces the values 
     associated with the same key (Reduce phase).

4. Industry Use Cases:
   - Big Data analytics (Hadoop, Apache Spark).
   - Text processing (word counts, inverted indices).
   - Parallel database queries.
"""

import time
import math
import string
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple


# ---------------------------------------------------------------------------
# Basic Implementation: Sequential Word Count
# ---------------------------------------------------------------------------
def sequential_word_count(documents: List[str]) -> Dict[str, int]:
    """
    Basic sequential approach to counting words in a list of documents.
    """
    counts = defaultdict(int)
    for doc in documents:
        # Clean and split
        words = doc.translate(str.maketrans('', '', string.punctuation)).lower().split()
        for word in words:
            counts[word] += 1
    return dict(counts)


# ---------------------------------------------------------------------------
# Professional Implementation: Parallel MapReduce Word Count
# ---------------------------------------------------------------------------
def _mapper(document: str) -> Dict[str, int]:
    """
    Map function: takes a document and returns a local word count.
    Designed to run in isolation on a separate process.
    """
    local_counts = defaultdict(int)
    words = document.translate(str.maketrans('', '', string.punctuation)).lower().split()
    for word in words:
        local_counts[word] += 1
    return dict(local_counts)


def _reducer(map_results: List[Dict[str, int]]) -> Dict[str, int]:
    """
    Reduce function: aggregates multiple local counts into a global count.
    """
    global_counts = defaultdict(int)
    for local_count in map_results:
        for word, count in local_count.items():
            global_counts[word] += count
    return dict(global_counts)


def parallel_mapreduce_word_count(documents: List[str], num_workers: int = 4) -> Dict[str, int]:
    """
    Implements a MapReduce architecture for counting words using multiprocessing.
    
    Args:
        documents: A list of text blocks to process.
        num_workers: Number of parallel processes to use.
        
    Returns:
        A dictionary containing the global word frequency count.
    """
    # 1. Map Phase (Parallel)
    map_results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Distribute the mapping tasks
        futures = [executor.submit(_mapper, doc) for doc in documents]
        for future in as_completed(futures):
            map_results.append(future.result())
            
    # 2. Reduce Phase (Sequential or Hierarchical Parallel)
    # For simplicity, we reduce sequentially here, but large-scale systems 
    # parallelize the reduce phase by partitioning keys.
    return _reducer(map_results)


# ---------------------------------------------------------------------------
# Bonus: Parallel Merge Sort (Divide and Conquer)
# ---------------------------------------------------------------------------
def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sequential_merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    return _merge(left, right)

def parallel_merge_sort(arr: List[int], depth: int = 0, max_depth: int = 2) -> List[int]:
    """
    Parallel merge sort using ThreadPoolExecutor. Threads are fine here if we just want 
    to demonstrate concurrency structure, though CPU-bound tasks in Python prefer Processes.
    """
    if len(arr) <= 1:
        return arr
        
    # Fallback to sequential if we reach maximum recursion depth for parallelism
    # to avoid thread overhead dominating runtime.
    if depth >= max_depth:
        return sequential_merge_sort(arr)
        
    mid = len(arr) // 2
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_left = executor.submit(parallel_merge_sort, arr[:mid], depth + 1, max_depth)
        future_right = executor.submit(parallel_merge_sort, arr[mid:], depth + 1, max_depth)
        
        left_sorted = future_left.result()
        right_sorted = future_right.result()
        
    return _merge(left_sorted, right_sorted)


# ---------------------------------------------------------------------------
# Complexity Analysis & Interview Challenge
# ---------------------------------------------------------------------------
"""
Complexity Analysis:
- MapReduce Word Count: Time O(N / P) for map phase, where N is total words and P is processes.
- Parallel Merge Sort: Time O(N log N) work, O(N) span. Memory O(N).

Interview Challenge:
1. How does the choice between Processes and Threads affect parallel merge sort in Python?
   Answer: In Python, due to the GIL, ThreadPoolExecutor will not provide actual CPU speedup 
   for pure sorting (CPU bound). To get real speedup, ProcessPoolExecutor is needed, but 
   IPC serialization costs (pickling the array parts back and forth) can destroy the gains 
   unless the dataset is massively large and chunking is optimized.
"""


# ---------------------------------------------------------------------------
# Example Usage & Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- Parallel Algorithm Design ---")
    
    # Test 1: MapReduce
    sample_docs = [
        "Hello world! Welcome to parallel programming.",
        "Parallel programming is fun but challenging.",
        "Hello again. World of parallel computation."
    ] * 10  # Multiply to simulate more data
    
    seq_res = sequential_word_count(sample_docs)
    par_res = parallel_mapreduce_word_count(sample_docs)
    
    assert seq_res == par_res, "MapReduce results do not match sequential counts!"
    print(f"MapReduce Output Snippet: {list(par_res.items())[:5]}")
    
    # Test 2: Parallel Merge Sort
    data = [i for i in range(10000, 0, -1)]
    sorted_data = parallel_merge_sort(data)
    
    assert sorted_data == sorted(data), "Parallel merge sort failed!"
    print("Parallel merge sort passed successfully!")
    print("All parallel algorithm tests passed!")
