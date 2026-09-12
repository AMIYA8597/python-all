"""
Module: Multiprocessing Algorithms (Map-Reduce)
===============================================

Learning Objectives:
1. Implement the Map-Reduce paradigm using Python multiprocessing.
2. Understand mapping and reducing phases.
3. Solve complex data processing problems in parallel.

Concept Explanation:
Map-Reduce divides a task into two parts:
- Map: Applies a function to each element (e.g., word tokenization).
- Reduce: Combines the mapped results (e.g., word counting).

Type Hints & Edge Cases:
- Large strings or data lists.
- Aggregation of complex objects like dictionaries.
"""

import multiprocessing
from collections import defaultdict
from typing import List, Dict, Tuple

# Basic Implementation: Sequential Word Count
def sequential_word_count(text: str) -> Dict[str, int]:
    counts = defaultdict(int)
    for word in text.split():
        counts[word.lower()] += 1
    return dict(counts)

# Advanced Implementation: Parallel Map-Reduce Word Count
def map_func(chunk: str) -> Dict[str, int]:
    counts = defaultdict(int)
    for word in chunk.split():
        counts[word.lower()] += 1
    return dict(counts)

def reduce_func(dicts: List[Dict[str, int]]) -> Dict[str, int]:
    merged = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            merged[k] += v
    return dict(merged)

def parallel_word_count(text: str, processes: int = multiprocessing.cpu_count()) -> Dict[str, int]:
    """Parallel map-reduce for word counting."""
    if not text:
        return {}
        
    # Split text roughly into chunks by lines or length
    words = text.split()
    chunk_size = max(1, len(words) // processes)
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    with multiprocessing.Pool(processes) as pool:
        mapped = pool.map(map_func, chunks)
        
    reduced = reduce_func(mapped)
    return reduced

# Interview Challenge
def challenge_parallel_primes(n: int) -> int:
    """Challenge: Count primes up to n using parallel processing."""
    def is_prime(num: int) -> int:
        if num < 2: return 0
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0: return 0
        return 1

    with multiprocessing.Pool() as pool:
        # map over range, return 1 if prime else 0
        counts = pool.map(is_prime, range(2, n + 1))
    return sum(counts)

def test_map_reduce():
    text = "hello world hello python multiprocessing world parallel"
    seq = sequential_word_count(text)
    par = parallel_word_count(text)
    assert seq == par, "Map-Reduce outputs do not match"
    assert challenge_parallel_primes(20) == 8, "Prime counting failed"
    print("All tests passed.")

if __name__ == "__main__":
    print("Multiprocessing Execution\\n" + "-"*30)
    test_map_reduce()
