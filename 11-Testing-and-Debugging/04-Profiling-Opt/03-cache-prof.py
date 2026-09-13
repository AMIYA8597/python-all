"""
Caching and Profiling in Python

Learning Objectives:
1. Understand the concept of memoization and caching.
2. Use `functools.lru_cache` to cache function results.
3. Profile cache performance (hits, misses, maxsize).
4. Implement a custom cache decorator.

Concept Explanation:
Caching stores the results of expensive function calls and returns the cached result when
the same inputs occur again. `functools.lru_cache` provides a Least Recently Used cache.
Profiling the cache helps determine if caching is effective (high hit rate) or if the cache
size needs tuning.

Imports:
- functools: For lru_cache.
- time: For measuring execution time.
"""

from functools import lru_cache
import time
from typing import Callable, Any, Dict, Tuple

# ==========================================
# Basic Implementation: Uncached vs. lru_cache
# ==========================================

def fibonacci_uncached(n: int) -> int:
    """Calculates Fibonacci numbers without caching."""
    if n < 2:
        return n
    return fibonacci_uncached(n - 1) + fibonacci_uncached(n - 2)

@lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    """Calculates Fibonacci numbers with LRU caching."""
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

# ==========================================
# Intermediate Implementation: Profiling lru_cache
# ==========================================

def profile_lru_cache() -> None:
    """Profiles the built-in lru_cache performance."""
    print("Calculating fibonacci(35) uncached...")
    start = time.perf_counter()
    # Uncached takes a long time, we do 30 to keep it reasonable
    fibonacci_uncached(30) 
    print(f"Uncached time: {time.perf_counter() - start:.4f}s")
    
    print("Calculating fibonacci(30) cached (first run)...")
    start = time.perf_counter()
    fibonacci_cached(30)
    print(f"Cached time (misses): {time.perf_counter() - start:.6f}s")
    
    print("Calculating fibonacci(30) cached (second run)...")
    start = time.perf_counter()
    fibonacci_cached(30)
    print(f"Cached time (hits): {time.perf_counter() - start:.6f}s")
    
    # View cache statistics
    print(f"Cache Info: {fibonacci_cached.cache_info()}")

# ==========================================
# Advanced Implementation: Custom Cache with Stats
# ==========================================

def custom_cache_with_stats(func: Callable) -> Callable:
    """A custom cache decorator that tracks hits and misses."""
    cache: Dict[Tuple[Any, ...], Any] = {}
    stats = {"hits": 0, "misses": 0}
    
    def wrapper(*args: Any) -> Any:
        if args in cache:
            stats["hits"] += 1
            return cache[args]
        
        stats["misses"] += 1
        result = func(*args)
        cache[args] = result
        return result
        
    wrapper.cache_stats = stats # type: ignore
    return wrapper

@custom_cache_with_stats
def expensive_computation(x: int, y: int) -> int:
    """Simulates an expensive computation."""
    time.sleep(0.1) # Simulate work
    return x * y

# ==========================================
# Edge Cases & Interview Challenge
# ==========================================

"""
Edge Cases:
1. Unhashable arguments: lru_cache requires arguments to be hashable (e.g., lists/dicts fail).
2. Memory constraints: An unbounded cache (maxsize=None) can consume all memory.

Interview Challenge:
Question: Implement an LRU Cache class from scratch without using functools.
Hint: Use a combination of a hash map (dict) and a doubly linked list, or take advantage
of Python 3.7+ dicts which maintain insertion order.
"""

def test_cache() -> None:
    """Tests the custom cache decorator."""
    assert expensive_computation(2, 3) == 6
    assert expensive_computation.cache_stats["misses"] == 1 # type: ignore
    assert expensive_computation(2, 3) == 6
    assert expensive_computation.cache_stats["hits"] == 1 # type: ignore
    print("Cache tests passed.")

if __name__ == "__main__":
    print("--- Caching and Profiling ---")
    print("1. Profiling built-in lru_cache:")
    profile_lru_cache()
    
    print("\n2. Custom Cache with Stats:")
    expensive_computation(5, 5)
    expensive_computation(5, 5) # Hit
    expensive_computation(10, 10) # Miss
    print(f"Custom cache stats: {expensive_computation.cache_stats}") # type: ignore
    
    print("\n3. Running Tests:")
    test_cache()
