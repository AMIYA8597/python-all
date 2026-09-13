"""
# ==============================================================================
# LABORATORY: ITERTOOLS & FUNCTOOLS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The `itertools` module provides C-optimized building blocks for iterators. 
# It is essential for competitive programming and heavy data pipelines where 
# generating permutations in Python loops is too slow.
# The `functools` module provides higher-order functions like `lru_cache` 
# which can transform an O(2^N) recursive algorithm into O(N) with one line of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Infinite iterators (count, cycle, repeat).
# - Master Combinatoric iterators (permutations, combinations, product).
# - Understand `itertools.groupby`.
# - Master `functools.lru_cache` and Memoization.
# - Understand `functools.partial` for function freezing.
# - Understand `functools.reduce`.
#
# ==============================================================================
"""

import time
import itertools
from functools import lru_cache, partial, reduce

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. ITERTOOLS: INFINITE ITERATORS
# ==============================================================================
def demonstrate_infinite_iters():
    """
    WARNING: These never stop. You MUST use a `break` or `islice` to terminate them.
    """
    section_header("Itertools: count, cycle, repeat")
    
    # 1. count(start, step)
    print("count(10, 2) for 3 iterations:")
    for i in itertools.count(10, 2):
        print(f" {i}")
        if i >= 14: break
        
    # 2. cycle(iterable)
    print("\ncycle('AB') for 5 iterations:")
    count = 0
    for char in itertools.cycle("AB"):
        print(f" {char}")
        count += 1
        if count == 5: break
        
    # 3. repeat(object, times)
    print("\nrepeat('Python', 3):")
    for word in itertools.repeat("Python", 3):
        print(f" {word}")


# ==============================================================================
# 4. ITERTOOLS: COMBINATORICS (DSA ESSENTIAL)
# ==============================================================================
def demonstrate_combinatorics():
    """
    Crucial for solving backtracking and brute-force DSA questions in C-speed.
    """
    section_header("Itertools: Combinations, Permutations, Product")
    
    letters = ['A', 'B', 'C']
    
    # Permutations (Order matters: AB is different from BA)
    perms = list(itertools.permutations(letters, 2))
    print(f"Permutations of {letters} choose 2:\n {perms}")
    
    # Combinations (Order doesn't matter: AB is the same as BA)
    combs = list(itertools.combinations(letters, 2))
    print(f"\nCombinations of {letters} choose 2:\n {combs}")
    
    # Cartesian Product (Equivalent to nested for loops)
    # product(A, B) -> every element of A paired with every element of B
    print("\nCartesian Product of [1, 2] and ['X', 'Y']:")
    prod = list(itertools.product([1, 2], ['X', 'Y']))
    print(f" {prod}")


# ==============================================================================
# 5. ITERTOOLS: GROUPBY
# ==============================================================================
def demonstrate_groupby():
    """
    Groups contiguous elements sharing the same key.
    TRAP: The input MUST be sorted by the key first, otherwise groupby breaks!
    """
    section_header("Itertools: groupby")
    
    # Unsorted data
    data = [
        {'name': 'Alice', 'role': 'Admin'},
        {'name': 'Bob',   'role': 'User'},
        {'name': 'Charlie', 'role': 'Admin'}
    ]
    
    # 1. MUST SORT FIRST
    data.sort(key=lambda x: x['role'])
    
    # 2. THEN GROUP
    grouped = itertools.groupby(data, key=lambda x: x['role'])
    
    for role, group_iter in grouped:
        names = [item['name'] for item in group_iter]
        print(f"Role: {role} -> {names}")


# ==============================================================================
# 6. FUNCTOOLS: LRU_CACHE (MEMOIZATION)
# ==============================================================================

# Without cache: O(2^N) Time Complexity (Exponential)
def fib_slow(n: int) -> int:
    if n < 2: return n
    return fib_slow(n-1) + fib_slow(n-2)

# With cache: O(N) Time Complexity (Linear)
@lru_cache(maxsize=None)
def fib_fast(n: int) -> int:
    if n < 2: return n
    return fib_fast(n-1) + fib_fast(n-2)

def demonstrate_lru_cache():
    section_header("Functools: @lru_cache (Memoization)")
    
    # Test Slow
    start = time.perf_counter()
    res1 = fib_slow(35)
    end = time.perf_counter()
    print(f"fib_slow(35) = {res1} | Time: {end - start:.4f}s")
    
    # Test Fast
    start = time.perf_counter()
    res2 = fib_fast(35)
    end = time.perf_counter()
    print(f"fib_fast(35) = {res2} | Time: {end - start:.4f}s")
    print(f"Cache Stats: {fib_fast.cache_info()}")


# ==============================================================================
# 7. FUNCTOOLS: PARTIAL & REDUCE
# ==============================================================================
def multiply(x: int, y: int) -> int:
    return x * y

def demonstrate_partial_reduce():
    """
    partial: Freezes some arguments of a function, returning a new function.
    reduce: Applies a rolling computation to sequential pairs of values in a list.
    """
    section_header("Functools: partial & reduce")
    
    # PARTIAL
    # Create a new function that acts exactly like multiply(x, 2)
    double = partial(multiply, y=2)
    print(f"partial: double(10) = {double(10)}")
    
    # REDUCE
    # reduce(lambda x,y: x*y, [1,2,3,4]) calculates (((1*2)*3)*4) = 24
    nums = [1, 2, 3, 4, 5]
    factorial = reduce(lambda a, b: a * b, nums)
    print(f"reduce: factorial of {nums} = {factorial}")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `itertools.permutations` and `combinations`?
   Answer: Permutations care about order (AB and BA are distinct). Combinations do not (AB and BA are identical).

2. What is the biggest trap when using `itertools.groupby`?
   Answer: You MUST sort the data by the exact same key function BEFORE passing it to `groupby`, because it only groups *contiguous* identical keys.

3. How does `@lru_cache` work under the hood?
   Answer: It maintains a dictionary mapping the function's arguments to its return values. If called again with the same arguments, it bypasses the function entirely and returns the dictionary value.

4. What is the time complexity difference for computing Fibonacci(N) with and without `@lru_cache`?
   Answer: Without it, the recursive tree branches infinitely and takes O(2^N) time. With it, each value is computed exactly once, taking O(N) time.
"""

if __name__ == "__main__":
    demonstrate_infinite_iters()
    demonstrate_combinatorics()
    demonstrate_groupby()
    demonstrate_lru_cache()
    demonstrate_partial_reduce()
    print("\n[SUCCESS] Laboratory: Itertools & Functools Completed.")
