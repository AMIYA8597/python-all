"""
Algorithm Optimization: Caching and Memoization

Learning Objectives:
1. Understand the concept of Memoization (caching function results).
2. Learn to implement custom caching dictionaries.
3. Utilize Python's built-in `functools.lru_cache` and `cache`.
4. Analyze the time-space tradeoff of caching.

Concept Explanation:
Caching (specifically memoization) is an optimization technique that speeds up 
programs by storing the results of expensive function calls and returning the 
cached result when the same inputs occur again. It trades memory space for 
execution speed.
"""

import timeit
from functools import lru_cache, cache
from typing import Dict, Any

# --- Basic Implementation ---
def fibonacci_naive(n: int) -> int:
    """Naive recursive Fibonacci (Exponential time)."""
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)

# --- Intermediate Implementation ---
class CustomCache:
    """A custom dictionary-based cache."""
    def __init__(self):
        self.cache: Dict[int, int] = {}
        
    def fibonacci_custom(self, n: int) -> int:
        if n in self.cache:
            return self.cache[n]
        if n <= 1:
            return n
        result = self.fibonacci_custom(n-1) + self.fibonacci_custom(n-2)
        self.cache[n] = result
        return result

# --- Advanced Implementation / Performance Analysis ---
@lru_cache(maxsize=128)
def fibonacci_lru(n: int) -> int:
    """LRU Cache evicts least recently used items when maxsize is hit."""
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

@cache
def fibonacci_unbounded(n: int) -> int:
    """Python 3.9+ unbounded cache (faster but consumes more memory)."""
    if n <= 1:
        return n
    return fibonacci_unbounded(n-1) + fibonacci_unbounded(n-2)

def compare_performance():
    setup = "from __main__ import fibonacci_naive, CustomCache, fibonacci_lru, fibonacci_unbounded; cc = CustomCache()"
    n = 30 # Small enough for naive to finish, big enough to show diff
    
    t_naive = timeit.timeit(f"fibonacci_naive({n})", setup=setup, number=1)
    t_custom = timeit.timeit(f"cc.fibonacci_custom({n})", setup=setup, number=1)
    t_lru = timeit.timeit(f"fibonacci_lru({n})", setup=setup, number=1)
    t_cache = timeit.timeit(f"fibonacci_unbounded({n})", setup=setup, number=1)
    
    print(f"Naive Time:    {t_naive:.6f}s")
    print(f"Custom Cache:  {t_custom:.6f}s")
    print(f"LRU Cache:     {t_lru:.6f}s")
    print(f"Unbounded:     {t_cache:.6f}s")

# --- Edge Cases ---
def demonstrate_edge_cases():
    """Cache functions must have hashable arguments!"""
    @lru_cache()
    def process_list(lst: list) -> int:
        return sum(lst)
        
    try:
        process_list([1, 2, 3]) # Lists are unhashable
    except TypeError as e:
        print(f"Expected TypeError: {e}")
        
    # Fix: use tuples
    @lru_cache()
    def process_tuple(tup: tuple) -> int:
        return sum(tup)
    assert process_tuple((1, 2, 3)) == 6

# --- Interview Challenge ---
"""
Challenge: Implement your own simple LRU Cache using an OrderedDict.
"""
from collections import OrderedDict

class SimpleLRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return -1
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False) # Remove from beginning (LRU)

# --- Tests ---
def run_tests():
    assert fibonacci_lru(10) == 55
    assert fibonacci_unbounded(10) == 55
    
    lru = SimpleLRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3) # evicts key 2
    assert lru.get(2) == -1
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Caching ---")
    compare_performance()
    demonstrate_edge_cases()
    run_tests()
