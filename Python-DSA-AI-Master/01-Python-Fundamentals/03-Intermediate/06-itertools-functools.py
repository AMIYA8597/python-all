"""
## A. Concept Name
Itertools and Functools

## B. One-Sentence Definition
`itertools` provides fast, memory-efficient tools for creating complex iterators, while `functools` offers higher-order functions that act on or return other functions to enhance functional programming in Python.

## C. Why Does This Exist?
To provide standardized, highly optimized C implementations for common functional programming patterns and combinatorial iteration, saving developers from writing inefficient, bug-prone boilerplate loops.

## D. Intuition
Instead of loading all data into memory at once or writing complex nested loops, you can build a pipeline of data processors (iterators) that lazily evaluate data on demand. Similarly, you can use decorators/wrappers to augment functions with new behaviors (like caching or pre-filling arguments) without altering their internal code.

## E. Real-Life Analogy
`itertools` is like an assembly line conveyor belt where items are processed one by one without needing a massive warehouse to store them all. `functools` is like adding a specialized tool attachment to a Swiss Army knife (e.g., `partial` fixing the size of a wrench, or `lru_cache` keeping a notepad of previous calculations).

## F. Mental Model
Think of data as a flowing stream rather than a stagnant pond. `itertools` provides the pipes and valves to route, combine, and split this stream. `functools` provides the specialized operators that sit along the stream to transform or cache the results of functions acting on that data.

## G. Visual Explanation
```
itertools.product(['A', 'B'], [1, 2]):
'A' -> 1 => ('A', 1)
'A' -> 2 => ('A', 2)
'B' -> 1 => ('B', 1)
'B' -> 2 => ('B', 2)

functools.partial(power, exp=2):
power(base, exp) ----[fix exp=2]----> square(base)
```

## H. Formal Explanation
`itertools` contains a set of fast, memory-efficient tools for working with iterators (e.g., infinite iterators, combinatoric iterators). Iterators compute their values on the fly, yielding elements one at a time via `next()`.
`functools` provides higher-order functions: functions that take other functions as arguments or return them. Key utilities include `@lru_cache` for memoization, `partial` for freezing some portion of a function's arguments, and `reduce` for cumulatively applying a function to items of an iterable.

## I. Mathematical Foundation (if applicable)
Combinatorics:
- Permutations of $n$ items taken $r$ at a time: $P(n,r) = n! / (n-r)!$
- Combinations of $n$ items taken $r$ at a time: $C(n,r) = n! / (r! (n-r)!)$
- Cartesian Product: $A \times B = \{(a,b) \mid a \in A, b \in B\}$

## J. From-Scratch Implementation (if applicable)
```python
def my_cycle(iterable):
    # A simplified version of itertools.cycle
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
            yield element
```

## K. Library / Production Implementation (if applicable)
Python's `itertools` are implemented in C for blazing fast execution. `functools.lru_cache` is a C-optimized thread-safe caching decorator using a doubly-linked list and a dictionary to evict the least recently used elements efficiently.

## L. Trace (walk through example)
For `functools.reduce(lambda x, y: x * y, [1, 2, 3, 4])`:
1. `x=1, y=2` -> returns 2
2. `x=2, y=3` -> returns 6
3. `x=6, y=4` -> returns 24.
Result = 24.

## M. Complexity
- **Time Complexity:** $O(N)$ for most linear iteration tools (like `chain`). Combinatorials like `permutations` generate $O(N!)$ items. `lru_cache` lookups are $O(1)$.
- **Space Complexity:** $O(1)$ memory overhead for iterators (they yield on-the-fly). `lru_cache` consumes $O(N)$ space up to the configured `maxsize`.

## N. Common Mistakes
- Iterating over an `itertools` object twice. Iterators are exhausted after one pass; you must recreate them or cast to a list if you need to loop again.
- Using `itertools.groupby` without sorting the data by the key first.
- Mutating arguments passed to a function decorated with `@lru_cache` (arguments must be hashable, e.g., tuples instead of lists).

## O. Common Confusions
- Difference between `combinations` (order doesn't matter, AB is same as BA) and `permutations` (order matters, AB is different from BA).
- Forgetting that `reduce` needs an initial value for empty sequences, otherwise it raises `TypeError`.

## P. When To Use
- `itertools`: When processing large datasets, generating combinations, or needing custom iteration patterns without loading everything into memory.
- `functools`: When needing memoization (`@lru_cache`, `@cache`), function parameter freezing (`partial`), or rich comparison sorting (`cmp_to_key`).

## Q. When NOT To Use
- Don't use iterators if you need random access (e.g., `my_iter[5]`). Convert to a list first, if memory permits.
- Don't use `reduce` if a simple `for` loop or `sum()` / `math.prod()` is more readable and pythonic.

## R. Trade-offs
- **Iterators vs Lists:** Iterators save vast amounts of memory but lack features like indexing, slicing, and length (`len()`).
- **Caching vs Memory:** `lru_cache` speeds up repeated calls exponentially (e.g., recursive Fibonacci) but consumes memory to store the results.

## S. Debugging
- Print iterators by converting them to lists: `print(list(my_iter))`, but remember this exhausts them!
- For `lru_cache`, use `func.cache_info()` to check hits, misses, and current size, and `func.cache_clear()` to reset the cache.

## T. Memory Hook (a short memorable principle)
"Itertools for the Flow, Functools for the Pro." (Itertools routes data, Functools enhances functions).

## U. Active Recall (questions before answers)
1. What happens if you run `groupby` on an unsorted list?
   - It will create multiple groups for the same key if identical keys are not adjacent.
2. How do you prevent `reduce` from failing on empty lists?
   - Provide the third argument, the `initial` value.
3. Why does `lru_cache` fail if you pass a list as an argument?
   - Lists are unhashable, and dictionary keys (used internally by the cache) must be hashable.

## V. Practice (exercises)
1. Write a function that uses `itertools.product` to find all combinations of a 3-digit lock.
2. Use `functools.partial` to create a `print_stderr` function that prints to `sys.stderr` by default.

## W. Interview Question
"How would you group a list of log dictionaries by the 'status' key, and how would you optimize an expensive overlapping recursive function?"
- Answer: Use `itertools.groupby` after sorting by 'status', and use `functools.lru_cache` to memoize the recursive function.

## X. Project Connection
In a web scraping pipeline, `itertools` helps chunk URLs and process them sequentially without eating RAM, while `functools.lru_cache` caches database lookups or expensive API responses to prevent redundant network calls.
"""

import itertools
import functools
from typing import List, Tuple, Any, Callable


# Basic Implementation: itertools (Combinatorics and Chaining)
def basic_itertools() -> None:
    print("--- Basic Itertools ---")
    # Product (Cartesian product)
    colors = ['Red', 'Blue']
    sizes = ['S', 'M']
    print(f"Product: {list(itertools.product(colors, sizes))}")

    # Permutations (order matters)
    print(f"Permutations: {list(itertools.permutations([1, 2, 3], 2))}")

    # Combinations (order doesn't matter)
    print(f"Combinations: {list(itertools.combinations([1, 2, 3], 2))}")

    # Chaining iterables
    chained = itertools.chain([1, 2], [3, 4])
    print(f"Chained: {list(chained)}")


# Intermediate Implementation: functools (partial and reduce)
def intermediate_functools() -> None:
    print("\n--- Intermediate Functools ---")
    # partial: Fixes certain arguments of a function
    def power(base: int, exp: int) -> int:
        return base ** exp

    square = functools.partial(power, exp=2)
    cube = functools.partial(power, exp=3)
    
    print(f"Square of 5: {square(5)}")
    print(f"Cube of 5: {cube(5)}")

    # reduce: Applies a rolling computation to sequential pairs
    numbers = [1, 2, 3, 4, 5]
    product = functools.reduce(lambda x, y: x * y, numbers)
    print(f"Product of {numbers}: {product}")


# Advanced Implementation: lru_cache and Infinite Iterators
@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Calculates Fibonacci with memoization."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def advanced_itertools() -> None:
    print("\n--- Advanced Itertools ---")
    # Infinite iterators
    counter = itertools.count(start=10, step=2)
    print(f"Count: {[next(counter) for _ in range(3)]}")
    
    cycler = itertools.cycle(['A', 'B'])
    print(f"Cycle: {[next(cycler) for _ in range(5)]}")


# Performance Analysis
def analyze_performance() -> None:
    print("\n--- Performance Analysis ---")
    import timeit
    
    # Memoized vs Non-memoized Fibonacci
    def slow_fib(n: int) -> int:
        if n < 2: return n
        return slow_fib(n-1) + slow_fib(n-2)
        
    t1 = timeit.timeit("slow_fib(20)", globals=locals(), number=10)
    t2 = timeit.timeit("fibonacci(20)", globals=globals(), number=10)
    
    print(f"Time for slow_fib(20) x10: {t1:.6f}s")
    print(f"Time for lru_cache fibonacci(20) x10: {t2:.6f}s")
    print("Memoization dramatically reduces time complexity for overlapping subproblems.")

# Edge Cases
def handle_edge_cases() -> None:
    print("\n--- Edge Cases ---")
    
    # Empty lists in reduce
    try:
        functools.reduce(lambda x, y: x + y, [])
    except TypeError:
        print("Caught TypeError: reduce on empty sequence requires an initial value.")
        
    res = functools.reduce(lambda x, y: x + y, [], 0)
    print(f"Reduce with initial value 0: {res}")


# Interview Challenge
def group_by_key(data: List[dict], key: str) -> dict:
    """
    Challenge: Group a list of dictionaries by a specific key using itertools.groupby.
    Note: groupby requires the data to be sorted by the grouping key first!
    """
    sorted_data = sorted(data, key=lambda x: x[key])
    grouped = {}
    for k, g in itertools.groupby(sorted_data, key=lambda x: x[key]):
        grouped[k] = list(g)
    return grouped


# Tests
def run_tests() -> None:
    # Test grouping
    data = [{'role': 'admin', 'name': 'Alice'}, {'role': 'user', 'name': 'Bob'}, {'role': 'admin', 'name': 'Charlie'}]
    grouped = group_by_key(data, 'role')
    assert len(grouped['admin']) == 2
    assert len(grouped['user']) == 1
    
    # Test cache
    assert fibonacci(10) == 55
    assert fibonacci.cache_info().hits > 0 # Check cache was used
    
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Running Itertools and Functools Examples ---")
    basic_itertools()
    intermediate_functools()
    advanced_itertools()
    analyze_performance()
    handle_edge_cases()
    run_tests()
