"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (ALGORITHM CACHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive percentage of CPU time in enterprise applications is wasted 
# recalculating mathematical truths that have already been solved. 
#
# A junior engineer implements a recursive Fibonacci function. To calculate 
# Fib(40), the CPU executes 102,334,155 recursive calls, taking 30 seconds.
#
# A senior engineer adds `@lru_cache`. The CPU calculates Fib(40) in exactly 
# 40 steps, reducing execution time from 30 seconds to 0.00001 seconds, achieving 
# an unfathomable performance increase through the architectural concept of 
# "Space-Time Tradeoff" (sacrificing a tiny amount of RAM to save massive CPU time).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Memoization using `@lru_cache` and `@cache`.
# - Understand the strict requirements for Hashability in Caching.
# - Prove the exponential performance collapse of naive recursion.
#
# ==============================================================================
"""

import timeit
import functools
from typing import Dict, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE RECURSION (THE EXPONENTIAL COLLAPSE)
# ==============================================================================
def fib_naive(n: int) -> int:
    """
    Time Complexity: O(2^N)
    A catastrophic recursive implementation.
    """
    if n <= 1:
        return n
    # It blindly calculates both branches all the way down to 1!
    return fib_naive(n - 1) + fib_naive(n - 2)

# ==============================================================================
# 4. MANUAL MEMOIZATION (THE HASH TABLE PROOF)
# ==============================================================================
# We can manually inject a Hash Table to intercept duplicate calls!
# Time Complexity: O(N)
def fib_memo(n: int, cache: Dict[int, int] = None) -> int:
    if cache is None:
        cache = {}
        
    # THE O(1) INTERCEPTION!
    # If we have mathematically solved this before, return it instantly!
    if n in cache:
        return cache[n]
        
    if n <= 1:
        return n
        
    # Calculate it ONCE, and immediately lock it into the cache!
    result = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    cache[n] = result
    return result

# ==============================================================================
# 5. PYTHON LRU CACHE (THE PRODUCTION STANDARD)
# ==============================================================================
# `lru_cache` (Least Recently Used) wraps our function in a highly optimized 
# C-level Hash Table. `maxsize=None` means it will cache an infinite number of 
# calls (becoming identical to `functools.cache` in Python 3.9+).
@functools.lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


# ==============================================================================
# 6. MATHEMATICAL SPEED & COMPLEXITY PROOF
# ==============================================================================
def demonstrate_caching_performance():
    section_header("Performance Proof: Naive vs Memoization vs LRU")
    
    target_n = 35 # High enough to cause pain, low enough to not crash.
    print(f"  Calculating Fibonacci({target_n})...")
    
    print("\n  [NAIVE EXECUTION - O(2^N)]")
    start_naive = timeit.default_timer()
    ans_naive = fib_naive(target_n)
    end_naive = timeit.default_timer()
    time_naive = end_naive - start_naive
    print(f"    -> Result: {ans_naive}")
    print(f"    -> Time:   {time_naive:.4f} seconds (Catastrophic!)")
    
    print("\n  [MANUAL MEMOIZATION - O(N)]")
    start_memo = timeit.default_timer()
    ans_memo = fib_memo(target_n)
    end_memo = timeit.default_timer()
    time_memo = end_memo - start_memo
    print(f"    -> Result: {ans_memo}")
    print(f"    -> Time:   {time_memo:.6f} seconds")
    
    print("\n  [LRU CACHE - C-LEVEL O(N)]")
    # For a fair test, we clear the cache before starting!
    fib_lru.cache_clear()
    
    start_lru = timeit.default_timer()
    ans_lru = fib_lru(target_n)
    end_lru = timeit.default_timer()
    time_lru = end_lru - start_lru
    
    # We can inspect the internal C-level cache statistics!
    stats = fib_lru.cache_info()
    
    print(f"    -> Result: {ans_lru}")
    print(f"    -> Time:   {time_lru:.6f} seconds")
    print(f"    -> Cache Stats: {stats}")
    print(f"       (Misses: {stats.misses} [The initial calculations])")
    print(f"       (Hits:   {stats.hits} [The intercepted duplicate calls!])")


# ==============================================================================
# 7. THE HASHABILITY CONSTRAINT
# ==============================================================================
@functools.lru_cache(maxsize=128)
def process_data(data: Any) -> int:
    return len(data)

def demonstrate_hashability():
    section_header("The Hashability Constraint for Caching")
    
    print("  Attempting to cache a Tuple (Immutable)...")
    try:
        process_data((1, 2, 3))
        print("    -> SUCCESS! Tuples are hashable.")
    except Exception as e:
        print(f"    -> FAILED: {e}")
        
    print("\n  Attempting to cache a List (Mutable)...")
    try:
        # A junior engineer tries to pass a List into an LRU cache function.
        # It instantly triggers a TypeError!
        process_data([1, 2, 3])
    except TypeError as e:
        print(f"    -> FAILED AS EXPECTED! Error: {e}")
        print("       (Lists cannot be hashed because they can change in RAM!)")


def run_all_labs():
    demonstrate_caching_performance()
    demonstrate_hashability()


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the naive recursive Fibonacci function degrade into $O(2^N)$ time complexity?"
   Senior Answer: "Naive recursion creates a binary tree of execution. `Fib(5)` strictly calls `Fib(4)` and `Fib(3)`. But `Fib(4)` *also* calls `Fib(3)`! The exact same mathematical subtree for `Fib(3)` is completely recalculated from scratch multiple times. At each level, the number of function calls mathematically doubles. For `Fib(40)`, the CPU must physically evaluate over $100$ million distinct branches, resulting in an exponential $O(2^N)$ collapse."

2. Interviewer: "Why does `functools.lru_cache` instantly throw a `TypeError: unhashable type: 'list'` when you pass a list into the function?"
   Senior Answer: "Caching mechanisms are strictly implemented using Hash Tables (Dictionaries) to achieve $O(1)$ lookup time. The function's parameters are mathematically hashed to generate the Key. In Python, mutable structures like Lists and Dictionaries are explicitly unhashable. If you could hash a list, cache the result, and then later mutate the list in RAM, the mathematical hash would physically change, destroying the integrity of the Cache routing table! Therefore, CPython rigidly enforces that only Immutable objects (Strings, Tuples, Integers) can be passed into an LRU Cache."

3. Interviewer: "What does `maxsize` in `@lru_cache` mathematically protect against?"
   Senior Answer: "It protects against an Out-Of-Memory (OOM) crash! The 'Space-Time Tradeoff' dictates that caching saves CPU time by burning RAM. If you set `maxsize=None` on a function that processes 50,000,000 unique URLs, the C-level Hash Table will permanently lock all 50,000,000 results into RAM, completely bypassing the Garbage Collector, and violently crashing the server. By setting `maxsize=128`, the cache operates as a true 'Least Recently Used' Ring Buffer. Once 128 unique calls are cached, the 129th call mathematically evicts the oldest, coldest entry from the Hash Table, guaranteeing a strict, predictable ceiling on memory consumption."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Algorithm Optimization (Caching) Completed.")
