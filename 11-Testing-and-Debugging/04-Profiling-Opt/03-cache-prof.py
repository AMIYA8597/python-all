"""
# ==============================================================================
# LABORATORY: PROFILING & OPTIMIZATION (MEMOIZATION & CACHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a recursive function to calculate the Fibonacci 
# sequence. To calculate `fib(40)`, the function mathematically branches into 
# 331,160,281 separate function calls. The CPU runs at 100% capacity for 45 
# seconds. The developer thinks Python is just a "slow language."
#
# A senior software engineer understands "Memoization". They realize that 
# `fib(38)` is being calculated millions of times redundantly. They inject the 
# `@lru_cache` decorator from the `functools` library. The CPython interpreter 
# intercepts the function call, executes it once, and caches the result in a 
# Hash Table in RAM. The next time `fib(38)` is requested, the CPU bypasses 
# the calculation and returns the answer in O(1) time. The execution time 
# violently collapses from 45.0 seconds to 0.0001 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Algorithmic Memoization (Time-Space Tradeoff).
# - Execute caching via `@functools.lru_cache`.
# - Architect deterministic Cache Eviction Policies (LRU).
#
# ==============================================================================
"""

import time
import functools

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE BOTTLENECK)
# ==============================================================================
class MathematicalEngine:
    
    @staticmethod
    def fibonacci_slow(n: int) -> int:
        """
        The Junior Approach: Pure Recursion.
        Time Complexity: O(2^n) - Exponential Disaster.
        """
        if n < 2:
            return n
        return MathematicalEngine.fibonacci_slow(n - 1) + MathematicalEngine.fibonacci_slow(n - 2)

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def fibonacci_fast(n: int) -> int:
        """
        The Senior Approach: Memoized Recursion.
        Time Complexity: O(n) - Linear Speed.
        Space Complexity: O(n) - We trade RAM for CPU!
        """
        if n < 2:
            return n
        return MathematicalEngine.fibonacci_fast(n - 1) + MathematicalEngine.fibonacci_fast(n - 2)


# ==============================================================================
# 4. THE CACHE ARCHITECTURE SIMULATOR
# ==============================================================================
class CustomCacheSimulator:
    """
    Simulates exactly what `@lru_cache` is doing mathematically under the hood.
    """
    def __init__(self):
        # The Cache is just a standard Python Dictionary (Hash Table)!
        self.cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
    def execute(self, arg: int):
        # 1. We mathematically check the cache before touching the CPU!
        if arg in self.cache:
            self.cache_hits += 1
            return self.cache[arg]
            
        # 2. CACHE MISS! We must pay the CPU penalty.
        self.cache_misses += 1
        
        # Simulate heavy CPU math
        time.sleep(0.1) 
        result = arg * 2
        
        # 3. We store the result in RAM so we never have to calculate it again!
        self.cache[arg] = result
        return result


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_caching():
    section_header("Profiling & Optimization: Caching (Memoization)")
    
    # We will calculate Fibonacci 35. 
    # (Without caching, this takes ~2-4 seconds depending on CPU)
    target = 35
    
    print(f"  [EXECUTION] Calculating Fibonacci({target}) using O(2^n) recursion...")
    start_slow = time.time()
    res1 = MathematicalEngine.fibonacci_slow(target)
    time_slow = time.time() - start_slow
    print(f"  -> Result: {res1} | Time: {time_slow:.4f} seconds")
    
    print(f"\n  [EXECUTION] Calculating Fibonacci({target}) using O(N) @lru_cache...")
    start_fast = time.time()
    res2 = MathematicalEngine.fibonacci_fast(target)
    time_fast = time.time() - start_fast
    
    # We can mathematically inspect the cache performance!
    cache_info = MathematicalEngine.fibonacci_fast.cache_info()
    
    print(f"  -> Result: {res2} | Time: {time_fast:.6f} seconds")
    print(f"  -> [CACHE STATS] Hits: {cache_info.hits} | Misses: {cache_info.misses}")
    
    if time_fast > 0:
        speedup = time_slow / time_fast
        print(f"\n  [ARCHITECTURE PROOF]")
        print(f"  The `@lru_cache` decorator mathematically trapped the function calls,")
        print(f"  returning the result {speedup:,.0f}x faster. We effectively traded ")
        print(f"  Bytes of RAM to save Seconds of CPU time.")


def run_all_labs():
    demonstrate_caching()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Memoization', and how does it relate to the Time-Space Tradeoff in Computer Science?"
   Senior Answer: "Caching Deterministic Output. Memoization is the algorithmic act of storing the result of an expensive function call in memory so that subsequent calls with the exact same arguments can bypass the CPU. It is the ultimate manifestation of the Time-Space Tradeoff. We are mathematically sacrificing Space (RAM, to store the Hash Table of results) in order to drastically reduce Time (CPU cycles). This only works if the function is 'Deterministic' (or 'Pure')—meaning an input of $X$ will mathematically always return an output of $Y$."

2. Interviewer: "Why does the decorator `@lru_cache(maxsize=128)` specify a `maxsize`, and what does 'LRU' stand for?"
   Senior Answer: "Least Recently Used (Cache Eviction Policy). If you run a web server for a year and cache every single Database query, your RAM will mathematically hit 100% and the server will crash (OOM). A Cache Eviction Policy is mandatory. 'LRU' is an algorithm. When the cache hits the `maxsize` limit (e.g., $128$ items), the Python interpreter looks at the historical access patterns. It mathematically identifies the item that was accessed the furthest back in time (the Least Recently Used), deletes it from the Hash Table to free up RAM, and inserts the new item. This guarantees memory stability while maintaining high hit rates for popular data."

3. Interviewer: "If `@lru_cache` is so powerful, why don't we put it on every single function in the codebase?"
   Senior Answer: "Impure Functions and Unhashable Types. You cannot cache an 'Impure' function. If a function is `get_current_time()`, caching it is mathematically catastrophic because it will return the exact same time forever. If a function reads from a Database, caching it might return stale data if another user updated the Database. Furthermore, Python's cache relies on dictionaries, which require Hashable keys. If a function accepts a Mutable List as an argument (`def process(data: list)`), Python cannot hash the list. The interpreter will violently throw a `TypeError: unhashable type: 'list'`, preventing the cache from working."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Optimization (Caching) Completed.")
