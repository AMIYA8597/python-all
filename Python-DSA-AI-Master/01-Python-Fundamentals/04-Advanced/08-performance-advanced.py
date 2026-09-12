"""
## A. Concept Name
Advanced Performance Optimization (Generators, `__slots__`, and Memoization)

## B. One-Sentence Definition
A set of techniques that drastically reduce Python's memory footprint and execution time by avoiding dictionary overhead (`__slots__`), avoiding full list allocations (generators), and caching repetitive function results (`lru_cache`).

## C. Why Does This Exist?
Python is dynamically typed and prioritizes flexibility. Objects use flexible dictionaries (`__dict__`) to store attributes, lists allocate all elements in memory, and functions recompute logic by default. These defaults consume massive amounts of memory and CPU. We need specific tools to bypass these defaults for performance-critical or data-heavy applications.

## D. Intuition
- **Generators**: Instead of building a whole factory of cars at once and parking them in a huge lot, build one car, deliver it, and build the next.
- **`__slots__`**: Instead of a flexible, resizable backpack (`__dict__`), use a molded case with exact cutouts for what you need.
- **Memoization**: If you just solved a massive math problem, write down the answer so you don't have to solve it again if asked five minutes later.

## E. Real-Life Analogy
Imagine a restaurant kitchen:
- **List vs Generator**: A list prepares 1,000 meals before serving any, requiring a massive kitchen (memory). A generator prepares and serves one meal at a time.
- **`__slots__`**: Giving a chef a standardized rigid toolbelt with exactly two slots (knife, spoon) rather than a giant magic bag that can hold anything but weighs 50 lbs.
- **`lru_cache`**: The host remembering that the VIP customer always orders the steak, rather than asking them to read the menu every time.

## F. Mental Model
- Memory is space; execution is time. 
- Lists = O(N) space. Generators = O(1) space.
- Standard class = Dict overhead per instance. `__slots__` class = Array-like fixed overhead per instance.
- Uncached recursive function = Repeated tree branches. Cached = DAG (Directed Acyclic Graph) where overlapping branches are pruned.

## G. Visual Explanation
```text
Without __slots__:
Instance -> __dict__ (Hash Table) -> {"x": 1.0, "y": 2.0} [Overhead: ~104+ bytes]

With __slots__:
Instance -> [1.0, 2.0] (Static Array) [Overhead: ~40-50 bytes]

Without cache: fib(4)
       fib(4)
      /      \
  fib(3)     fib(2)
  /    \      /    \
fib(2) fib(1) fib(1) fib(0)
(fib(2) is calculated twice)

With lru_cache: fib(4)
       fib(4)
      /      \
  fib(3)   [CACHE HIT]
  /    \
fib(2) fib(1)
```

## H. Formal Explanation
- **Generators**: Objects that implement the iterator protocol (`__iter__` and `__next__`) using the `yield` keyword. They suspend state (local variables and instruction pointer) between calls.
- **`__slots__`**: A class-level attribute that tells the CPython interpreter to allocate space for the listed attributes directly on the instance struct, preventing the creation of an instance `__dict__` and `__weakref__`.
- **`functools.lru_cache`**: A decorator that wraps a function with a memoizing callable that saves up to the `maxsize` most recent calls. It uses a dictionary to map arguments to results and a doubly linked list to track usage order (Least Recently Used).

## I. Mathematical Foundation (if applicable)
For a memoized recursive function like Fibonacci:
- Unmemoized time complexity: O(2^n)
- Memoized time complexity: O(n) space and time.

For a generator vs list of size N:
- List space: O(N) memory
- Generator space: O(1) memory

## J. From-Scratch Implementation (if applicable)
See the `fibonacci_slow` and `sum_list` vs `sum_generator` functions below.

## K. Library / Production Implementation (if applicable)
Python provides `functools.lru_cache` for memoization and generator expressions `(x for x in data)` for lazy evaluation.

## L. Trace (walk through example)
1. `res = fibonacci_fast(3)` is called.
2. `fibonacci_fast` calls `fibonacci_fast(2)` and `fibonacci_fast(1)`.
3. Results are calculated and stored in the cache dict: `{(1,): 1, (2,): 1, (3,): 2}`.
4. If `fibonacci_fast(2)` is called again anywhere, the wrapper checks the dict for the key `(2,)`, finds `1`, and returns it instantly without entering the function body.

## M. Complexity
- **Time**: `lru_cache` reduces time complexity of overlapping subproblems drastically (e.g., O(2^N) to O(N)).
- **Space**: 
  - Generators reduce space from O(N) to O(1).
  - `__slots__` reduces space per object by roughly 40-50%.
  - `lru_cache` increases space complexity to store the cached arguments and results.

## N. Common Mistakes
- **Mutating arguments in lru_cache**: Arguments to an `lru_cache` function must be hashable. Passing a `list` or `dict` will raise a `TypeError`.
- **Inheriting with `__slots__`**: If a subclass doesn't define `__slots__` (even an empty one `__slots__ = ()`), it will create a `__dict__`, negating the memory benefits.
- **Consuming a generator twice**: Generators are one-time use. Iterating over them again yields nothing.

## O. Common Confusions
- **Generators vs Comprehensions**: `[x for x in range(10)]` makes a list in memory immediately. `(x for x in range(10))` makes a generator object.
- **Why isn't `__slots__` the default?**: Because it breaks Python's dynamic nature (like adding attributes at runtime, or multiple inheritance complexities). It's an opt-in optimization.

## P. When To Use
- `__slots__`: When you are creating millions of instances of a simple data class (e.g., ORM models, point clouds, large parsed datasets).
- Generators: Processing large files, continuous streams of data, or anytime you don't need the whole dataset in memory at once.
- `lru_cache`: Expensive computations that are called repeatedly with the same arguments (e.g., API calls, recursive math, dynamic programming).

## Q. When NOT To Use
- `__slots__`: For singletons, configuration objects, or objects that need dynamic monkey-patching.
- Generators: When you need to access elements by index (e.g., `gen[5]`), need the length (`len(gen)`), or need to iterate multiple times.
- `lru_cache`: Functions with side effects (like printing or writing to a database), or functions whose output depends on external mutable state (like reading the current time).

## R. Trade-offs
- **Generators**: Gain memory efficiency, lose random access and multi-pass iteration.
- **`__slots__`**: Gain memory efficiency and slight attribute access speed, lose dynamic attributes and multiple inheritance flexibility.
- **Memoization**: Gain CPU speed, lose memory (to store the cache).

## S. Debugging
- `lru_cache`: You can view cache stats using `func.cache_info()` (hits, misses, maxsize, currsize) and clear it with `func.cache_clear()`.
- Generators: Since they evaluate lazily, errors inside them might not trigger until you actually iterate over them. Use `list(gen)` to force evaluation if debugging.

## T. Memory Hook (a short memorable principle)
"Slots save space, Generators stream, Cache avoids the repeated dream."

## U. Active Recall (questions before answers)
1. What error do you get if you pass a list to an `@lru_cache` function?
2. How do you find out how many cache hits an `@lru_cache` function has had?
3. What happens if you try to add a new attribute `z` to a `PointWithSlots` instance?

## V. Practice (exercises)
1. Write a function that reads a huge log file and yields only lines containing "ERROR". Use a generator to ensure you don't load the whole file into memory.
2. Create a class hierarchy using `__slots__` to ensure the memory savings are inherited properly.

## W. Interview Question
Challenge: Write a generator function `chunker` that takes an iterable and a chunk size, and yields lists of that size, without loading the whole iterable into memory.

## X. Project Connection
In high-throughput AI data pipelines, you load gigabytes of text. Using generators prevents Out-Of-Memory (OOM) errors. When representing tokens or nodes in a graph structure, `__slots__` saves gigabytes of RAM. `lru_cache` is frequently used in tree-search algorithms (like minimax or MCTS) to avoid re-evaluating identical board states.
"""

import sys
import time
from functools import lru_cache
from typing import Iterator, Iterable, List, Any


# --- Basic Implementation: Generators vs Lists ---
def sum_list(n: int) -> int:
    """Creates a full list in memory before summing. HIGH memory usage."""
    data = [i for i in range(n)]
    return sum(data)

def sum_generator(n: int) -> int:
    """Uses a generator expression. LOW memory usage (O(1))."""
    data = (i for i in range(n))
    return sum(data)


# --- Intermediate Implementation: __slots__ for Memory Efficiency ---
class PointWithoutSlots:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointWithSlots:
    """Using __slots__ prevents the creation of __dict__ and __weakref__."""
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# --- Advanced Implementation: Memoization (lru_cache) ---
def fibonacci_slow(n: int) -> int:
    """O(2^n) time complexity without caching."""
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

@lru_cache(maxsize=128)
def fibonacci_fast(n: int) -> int:
    """O(n) time complexity due to LRU Cache."""
    if n < 2:
        return n
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)


# --- Interview Challenge Implementation ---
def chunker(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """Yields chunks of a given size from an iterable."""
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


# --- Tests ---
def run_tests() -> None:
    print("Testing Advanced Performance...")

    n = 100000

    # Test Generator vs List Memory
    # (Checking sys.getsizeof on the object itself, not the items)
    list_comp = [i for i in range(n)]
    gen_comp = (i for i in range(n))
    
    assert sys.getsizeof(list_comp) > sys.getsizeof(gen_comp)
    assert sum_list(n) == sum_generator(n)

    # Test __slots__ Memory
    p1 = PointWithoutSlots(1.0, 2.0)
    p2 = PointWithSlots(1.0, 2.0)
    
    # Calculate approximate size (object + dict vs just object)
    size1 = sys.getsizeof(p1) + sys.getsizeof(p1.__dict__)
    size2 = sys.getsizeof(p2)
    assert size1 > size2

    # Test LRU Cache Speed
    start = time.time()
    res_fast = fibonacci_fast(35)
    time_fast = time.time() - start
    
    # We only test slow up to a smaller number to avoid hanging
    start = time.time()
    res_slow = fibonacci_slow(30)  
    time_slow = time.time() - start
    
    assert res_fast == 9227465
    assert time_fast < 0.01  # Should be instant
    print(f"Fibonacci Fast: {time_fast:.6f}s")
    print(f"Fibonacci Slow (smaller N): {time_slow:.6f}s")

    # Test Chunker
    chunks = list(chunker(range(10), 3))
    assert chunks == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
