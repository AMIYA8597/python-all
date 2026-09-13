# ==============================================================================
# THEORY: ADVANCED STANDARD LIBRARY MASTERCLASS
# ==============================================================================

## 1. WHY THIS MATTERS
The Python Standard Library is often described as "batteries included". While beginners learn `math`, `random`, and `os`, the true power of Python lies in its advanced, highly optimized C-backed standard modules.

Many developers waste time reinventing the wheel or installing heavy third-party packages (like `pandas` or `numpy`) for tasks that the standard library can handle natively in microseconds. 

Mastering the advanced standard library is the defining characteristic of a Senior Python Developer. It allows you to write dependency-free, blisteringly fast, and architecturally beautiful code.

This textbook module covers the deep internals of `collections`, `itertools`, `functools`, `typing` (Advanced), and `contextlib`.

---

## 2. THE `collections` MODULE (HIGH-PERFORMANCE DATA STRUCTURES)

Python's built-in `list`, `dict`, and `set` are incredible, but they are general-purpose. The `collections` module provides specialized container datatypes.

### 2.1 `collections.deque` (Double-Ended Queue)
A standard Python `list` is a dynamic array. 
- `list.append()` is $O(1)$.
- `list.insert(0, item)` is $O(N)$ because every single element in the array must physically shift one memory address to the right. If the list has 10 million items, this is catastrophic.

A `deque` is implemented as a Doubly-Linked List of memory blocks.
- `deque.append()` is $O(1)$.
- `deque.appendleft()` is $O(1)$! It instantly snaps a new node to the front of the chain.

**Use Case:** Breadth-First Search (BFS) Queues, Sliding Window algorithms, and maintaining a history of the last $N$ items (`deque(maxlen=N)`).

### 2.2 `collections.defaultdict`
When building a frequency map or grouping data, a standard `dict` throws a `KeyError` if the key doesn't exist. You usually have to write clumsy `.get(key, 0)` or `if key not in d:` checks.

A `defaultdict` takes a "default factory" function (like `int`, `list`, or `set`). If a key is missing, it instantly calls the factory, inserts the default value, and returns it.

```python
from collections import defaultdict
# Grouping names by their first letter
names = ["Alice", "Bob", "Charlie", "Anna"]
groups = defaultdict(list)

for name in names:
    groups[name[0]].append(name) 
# No KeyError! Output: {'A': ['Alice', 'Anna'], 'B': ['Bob'], 'C': ['Charlie']}
```

### 2.3 `collections.Counter`
A subclass of dictionary explicitly designed for tallying hashable objects.
It is written in C and is ridiculously fast.

```python
from collections import Counter
votes = ["Yes", "No", "Yes", "Yes", "Abstain"]
tally = Counter(votes)
print(tally.most_common(1)) # [('Yes', 3)]
```

### 2.4 `collections.namedtuple`
Before Python 3.7 introduced `@dataclass`, `namedtuple` was the king of lightweight data objects. It creates a tuple subclass with named fields.
- **Memory:** It has the exact same memory footprint as a standard tuple (no `__dict__` overhead!).
- **Immutability:** It cannot be modified after creation, making it hashable and thread-safe.

---

## 3. THE `itertools` MODULE (ALGORITHMIC COMBINATORICS)

The `itertools` module is a collection of fast, memory-efficient tools for creating iterators for efficient looping. It brings Functional Programming concepts (like those in Haskell) directly into Python.

Because these functions return *Generators*, they compute values LAZILY. You can create an iterator representing 10 Trillion permutations, and it will consume exactly 0 bytes of RAM!

### 3.1 Infinite Iterators
- `itertools.count(start, step)`: Counts forever. Perfect for zipping with streams.
- `itertools.cycle(iterable)`: Loops through an iterable infinitely (e.g., Round-Robin scheduling).

### 3.2 Combinatoric Generators
If you are solving LeetCode or Project Euler, these are your best friends.
- `itertools.permutations(iterable, r)`: Returns all possible orderings. (Order matters: AB != BA).
- `itertools.combinations(iterable, r)`: Returns all possible groups. (Order doesn't matter: AB == BA).
- `itertools.product(*iterables)`: The Cartesian Product. This replaces heavily nested `for` loops!

**Replacing nested loops:**
```python
# Bad, heavily nested:
for x in range(10):
    for y in range(10):
        for z in range(10):
            print(x, y, z)

# Masterful, flat:
import itertools
for x, y, z in itertools.product(range(10), repeat=3):
    print(x, y, z)
```

### 3.3 `itertools.groupby`
Groups adjacent identical elements. 
*CRITICAL WARNING:* The input MUST be sorted by the grouping key first! `groupby` only compares adjacent items.

---

## 4. THE `functools` MODULE (HIGHER-ORDER FUNCTIONS)

Functions that act on or return other functions.

### 4.1 `functools.lru_cache` (Memoization)
The single most powerful decorator in the standard library. "LRU" stands for Least Recently Used.
If you have a pure function (same inputs always yield same outputs, like Fibonacci), decorating it with `@lru_cache` instantly caches the results in memory.
An exponential $O(2^N)$ recursive function instantly collapses into $O(N)$ linear time!

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 4.2 `functools.partial`
"Freezes" some portion of a function's arguments and keywords, resulting in a new object with a simplified signature.
Incredibly useful for passing functions as callbacks to APIs that don't support custom arguments (like `multiprocessing.Pool.map` or GUI button clicks).

```python
from functools import partial
def power(base, exp): return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)

print(square(5)) # 25
```

### 4.3 `functools.wraps`
Whenever you write a custom Decorator in Python, the wrapper function completely overwrites the original function's metadata (its `__name__`, its `__doc__` string).
You MUST use `@wraps` inside your decorator to physically copy the metadata from the original function to the wrapper, or else documentation generators (like Sphinx) and debuggers will break!

---

## 5. THE `contextlib` MODULE (RESOURCE MANAGEMENT)

Python's `with` statement guarantees that resources (files, network sockets, database connections) are cleanly closed, even if an exception occurs.

Instead of writing a massive Class with `__enter__` and `__exit__` dunder methods, `contextlib` allows you to create Context Managers using simple Generators!

### 5.1 `@contextmanager`
```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        # Yield passes control BACK to the 'with' block!
        yield
    finally:
        # This code runs when the 'with' block finishes or crashes!
        end = time.perf_counter()
        print(f"{label} took {end - start:.4f} seconds")

with timer("Heavy Math"):
    sum(x*x for x in range(1000000))
```

### 5.2 `contextlib.suppress`
A beautiful, Pythonic way to ignore specific exceptions without writing an ugly `try...except...pass` block.

```python
import os
from contextlib import suppress

# If the file doesn't exist, it just fails silently and continues!
with suppress(FileNotFoundError):
    os.remove("temporary_cache.txt")
```

---

## 6. ACTIVE RECALL & INTERVIEW SCENARIOS

> **Scenario 1:** "You need to find all unique pairs of students in a classroom of 30. How do you do it?"
**Answer:** I would use `itertools.combinations(students, 2)`. It mathematically generates all unique pairs in $O(1)$ memory without me having to write a clumsy double `for` loop with index tracking.

> **Scenario 2:** "Why use `deque` instead of `list` for a Queue?"
**Answer:** A `list` is a contiguous dynamic array. Popping from the front (`list.pop(0)`) requires shifting every single remaining element one byte to the left in RAM, causing $O(N)$ time complexity. A `deque` is a doubly-linked list. Popping from the front is $O(1)$ because it just severs the pointer to the head node.

> **Scenario 3:** "You wrote a recursive algorithm, but it is taking hours to run. How do you fix it?"
**Answer:** I would import `functools.lru_cache`. By slapping `@lru_cache(maxsize=None)` on the recursive function, Python will automatically hash the input arguments and store the return values in a hidden dictionary. The overlapping subproblems will hit the cache in $O(1)$ time instead of spawning exponential recursive branches.

---
**[END OF MODULE]**
