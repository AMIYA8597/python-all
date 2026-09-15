import os

filepath = r"d:\work\python-all\12-Resources-References\01-Documentation\01-Py-Ref.md"
os.makedirs(os.path.dirname(filepath), exist_ok=True)

parts = []

parts.append("""# The Comprehensive Python Reference Guide

Welcome to the Master Reference Guide for Python. This document serves as a textbook-depth resource covering advanced topics in Python programming. It spans from the intricacies of core language features like advanced data structures, decorators, and metaclasses, to modern architectural paradigms such as asynchronous programming. Furthermore, it addresses robust software engineering practices, including the testing pyramid and performance profiling.

Whether you are a senior developer looking to solidify your understanding of Python's memory model, or a mid-level engineer implementing an asynchronous microservice, this guide acts as your ultimate cheat sheet and curriculum companion.

---

## 1. Advanced Data Structures and Memory Optimization

Python's built-in data structures (`list`, `dict`, `set`, `tuple`) are highly optimized C implementations. However, for specialized use cases, the standard library provides more robust options, primarily found in the `collections` and `heapq` modules. Understanding when and why to use these structures requires a fundamental grasp of time complexity (Big O notation) and memory allocation.

### 1.1 The `collections` Module

The `collections` module provides specialized container datatypes providing alternatives to Python's general-purpose built-in containers.

#### `namedtuple`
`namedtuple` creates tuple subclasses with named fields. They offer the memory efficiency of tuples while allowing field access via attribute lookup, improving code readability. Under the hood, `namedtuple` generates a class dynamically using `exec()`, which makes it just as fast as a standard tuple but far more descriptive.

```python
from collections import namedtuple

# Define a Point namedtuple
Point = namedtuple('Point', ['x', 'y', 'z'], defaults=[0])
p = Point(11, y=22)

print(p.x, p.y, p.z)  # Output: 11 22 0
print(p[0])           # Output: 11 (Standard tuple access still works)
```

Because they are immutable, fields cannot be updated after creation, making them ideal for representing fixed records, rows fetched from a database, or composite keys in a dictionary. For mutable alternatives, Python 3.3+ introduced `types.SimpleNamespace`, and Python 3.7+ introduced `@dataclass`.

#### `deque` (Double-Ended Queue)
A `deque` is a list-like container with fast appends and pops on either end. While standard lists are implemented as dynamically sized arrays, making `insert(0, value)` an O(n) operation due to memory shifts, `deque` is implemented as a doubly-linked list (specifically, a list of memory blocks), ensuring O(1) time complexity for operations at both ends.

```python
from collections import deque

dq = deque(['b', 'c', 'd'])
dq.append('e')       # O(1) Add to right
dq.appendleft('a')   # O(1) Add to left

print(dq) # deque(['a', 'b', 'c', 'd', 'e'])

dq.pop()             # O(1) Remove from right
dq.popleft()         # O(1) Remove from left
```
*Use Case*: Implementing queues, breadth-first search (BFS) algorithms, or keeping a moving window of the last `N` items (using the `maxlen` argument, which automatically discards old items as new ones are added).

#### `Counter`
A `Counter` is a `dict` subclass for counting hashable objects. It is an unordered collection where elements are stored as dictionary keys and their counts are stored as dictionary values. The underlying implementation relies on the highly optimized C hash table used by standard dictionaries.

```python
from collections import Counter

words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
word_counts = Counter(words)

print(word_counts)           # Counter({'apple': 3, 'banana': 2, 'orange': 1})
print(word_counts.most_common(1)) # [('apple', 3)]

# Multisets mathematics
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2) # Counter({'a': 4, 'b': 3})
print(c1 - c2) # Counter({'a': 2}) # Keeps only positive counts
```
*Use Case*: Histogram generation, frequency analysis, multiset operations, or tracking inventory counts.

#### `defaultdict`
`defaultdict` is a dictionary subclass that calls a factory function to supply missing values, preventing `KeyError`. It intercepts the `__missing__` dunder method internally, avoiding the overhead of `dict.setdefault()` or `dict.get()`.

```python
from collections import defaultdict

# Grouping items by length
words = ['cat', 'dog', 'mouse', 'bird']
grouped = defaultdict(list)

for word in words:
    grouped[len(word)].append(word)

print(grouped) # defaultdict(<class 'list'>, {3: ['cat', 'dog'], 5: ['mouse'], 4: ['bird']})
```

### 1.2 Heap Queue (`heapq`)

The `heapq` module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm. In Python, heaps are represented as standard lists, with `heapq` providing functions to maintain the heap invariant (min-heap by default). Accessing the smallest item is O(1), while pushing or popping is O(log n).

```python
import heapq

data = [1, 5, 2, 8, 3]
heapq.heapify(data) # Transforms list into a heap in-place in O(N) time
print(data)         # Output: [1, 3, 2, 8, 5] - Note: only data[0] is guaranteed to be smallest

heapq.heappush(data, 0) # Pushes 0, maintains heap invariant
smallest = heapq.heappop(data) # Pops the smallest item (0)

# Finding the N largest or smallest elements efficiently
# Faster than sorting the entire list for small N
print(heapq.nlargest(2, data))  # [8, 5]
print(heapq.nsmallest(2, data)) # [1, 2]
```
*Use Case*: Priority queues, scheduling algorithms (Dijkstra's, A* search), merging sorted iterables (`heapq.merge`), and finding k-th elements in large datasets.

### 1.3 Memory Layout and `__slots__`

In Python, every object has a `__dict__` attribute that stores its instance variables dynamically. This hash table approach provides immense flexibility but consumes significant memory overhead. For classes with millions of instantiated objects, this memory footprint becomes a bottleneck.

By defining `__slots__` at the class level, you instruct Python to forego the dynamic `__dict__` creation and instead allocate memory statically for a fixed set of attributes.

```python
import sys

class StandardPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = StandardPoint(1, 2)
p2 = SlottedPoint(1, 2)

# Notice the memory difference
print(sys.getsizeof(p1) + sys.getsizeof(p1.__dict__)) # Much larger footprint
print(sys.getsizeof(p2)) # Leaner, C-struct-like footprint
```

---

## 2. Decorators and Metaprogramming

Decorators provide a powerful way to modify or enhance the behavior of functions, methods, or classes dynamically. They are the practical application of Higher-Order Functions and lexical closures.

### 2.1 Function Decorators and Closures

A closure occurs when a nested function captures and remembers the variables from its enclosing scope, even after the outer function has finished executing. Decorators leverage this to store state or configuration for the wrapped function.

```python
import time
from functools import wraps

def timer_decorator(func):
    @wraps(func) # Essential: preserves the original function's metadata (__name__, __doc__)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f}s")
        return result
    return wrapper

@timer_decorator
def complex_calculation(n):
    ""\"Calculates the sum of squares up to n.""\"
    return sum(i * i for i in range(n))

complex_calculation(1000000)
print(complex_calculation.__name__) # Prints 'complex_calculation' thanks to @wraps
```

### 2.2 Decorators with Arguments

To pass arguments to a decorator (e.g., `@retry(retries=3)`), you need a decorator factory: an outer function that accepts the arguments and returns the actual decorator. This results in three levels of nested functions.

```python
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator
```

### 2.3 Class Decorators

Decorators can also target classes. A class decorator receives the class object and returns a modified or entirely new class object. They are excellent alternatives to inheritance or metaclasses for cross-cutting concerns.

```python
def add_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith('_'))
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
```

---

## 3. Metaclasses and Class Creation

Metaclasses are the "classes of classes." Just as an object is an instance of a class, a class itself is an instance of a metaclass. In Python, the default metaclass is `type`. They allow interception of class creation, modifying attributes, enforcing interfaces, and automating boilerplate.

### 3.1 Understanding Class Execution

When Python executes a `class` statement, it performs three major steps:
1. Resolves the correct metaclass (usually `type`).
2. Prepares a namespace dictionary (using `__prepare__`).
3. Executes the class body within that namespace.
4. Calls the metaclass to construct the class object (`type(name, bases, attrs)`).

### 3.2 Building a Custom Metaclass

To create a custom metaclass, you inherit from `type` and override the `__new__` or `__init__` methods.
- `__new__(mcs, name, bases, attrs)`: Called *before* the class is created. Use this to modify `attrs` or `bases`.
- `__init__(cls, name, bases, attrs)`: Called *after* the class object is allocated in memory.

```python
class SingletonMeta(type):
    ""\"
    A metaclass that implements the Singleton pattern.
    Ensures only one instance of the class exists globally.
    ""\"
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # type.__call__ is what gets triggered when you do MyClass()
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        pass # Only runs once
```

---

## 4. Async Patterns (`asyncio`)

Asynchronous programming in Python via `asyncio` implements cooperative multitasking. It allows single-threaded, concurrent code using coroutines, enabling massive scalability for I/O-bound operations (network requests, database queries, file I/O). Unlike multithreading (bound by the GIL) or multiprocessing (heavy OS context switching), `asyncio` handles thousands of connections in a single process.

### 4.1 Core Concepts and Terminology

- **Coroutine**: A function defined with `async def`. It does not execute immediately but returns a coroutine object. Execution occurs when it is `await`ed.
- **Event Loop**: The beating heart of `asyncio`. It tracks active tasks, distributes execution time, and handles system I/O callbacks via mechanisms like `epoll` or `kqueue`.
- **Task**: A wrapper around a coroutine that actively schedules it to run on the event loop concurrently with other tasks.
- **Future**: A low-level primitive representing the eventual result of an asynchronous operation (similar to Promises in JavaScript).

### 4.2 The Awaitable Lifecycle

```python
import asyncio
import time

async def fetch_data(task_id, delay):
    print(f"Task {task_id}: Starting fetch...")
    # yield control back to the event loop, unblocking the thread
    await asyncio.sleep(delay) 
    print(f"Task {task_id}: Finished fetch after {delay}s")
    return {"id": task_id, "data": "dummy"}

async def main():
    start = time.perf_counter()
    
    # asyncio.gather schedules multiple awaitables concurrently
    # It waits for all to finish and returns their results in order
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 3),
        fetch_data(3, 1)
    )
    
    end = time.perf_counter()
    print(f"Total time: {end - start:.2f}s (Not 6s!)")
    print("Results:", results)

# The standard entry point for an asyncio program
if __name__ == "__main__":
    # asyncio.run(main())
    pass
```

### 4.3 Advanced Concurrency Patterns

#### 1. Bounded Concurrency (Semaphores)
When scraping web pages or calling external microservices, unbounded concurrency can lead to rate-limiting, IP bans, or out-of-memory errors. Semaphores act as a concurrency bottleneck.

```python
async def fetch_with_semaphore(sem, session, url):
    async with sem: # Acquire semaphore before proceeding
        # e.g., async with session.get(url) as response:
        await asyncio.sleep(0.5) 
        return f"200 OK from {url}"

async def bounded_scraper():
    urls = [f"http://api.example.com/item/{i}" for i in range(100)]
    # Limit to maximum 10 concurrent requests
    semaphore = asyncio.Semaphore(10) 
    
    # create_task schedules them immediately
    tasks = [asyncio.create_task(fetch_with_semaphore(semaphore, None, url)) for url in urls]
    
    # Wait for all 100 to finish
    results = await asyncio.gather(*tasks)
```

#### 2. Task Cancellation and Timeouts
In distributed systems, handling failures and timeouts gracefully is mandatory to prevent hanging connections.

```python
async def flaky_database_query():
    try:
        print("Executing heavy query...")
        await asyncio.sleep(10)
        return "Query Results"
    except asyncio.CancelledError:
        print("Query was cancelled by the caller! Performing rollback...")
        # Await necessary cleanup (shielding it from being cancelled itself)
        await asyncio.shield(asyncio.sleep(0.1)) 
        raise # Must re-raise to propagate cancellation

async def execute_with_timeout():
    try:
        # Will inject a CancelledError into the coroutine after 2.0s
        result = await asyncio.wait_for(flaky_database_query(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation failed: Database timeout exceeded.")
```

---

## 5. The Testing Pyramid and Advanced Pytest

The testing pyramid dictates a structured approach to quality assurance: a massive foundation of fast unit tests, a middle layer of integration tests verifying boundaries, and a tiny apex of brittle End-to-End (E2E) UI tests.

### 5.1 Pytest Architecture and Fixtures

`pytest` is the industry standard due to its modular architecture, rich assertion rewriting (allowing standard `assert foo == bar` instead of `self.assertEqual`), and powerful fixture dependency injection.

#### Fixtures: Scoping and Teardown
Fixtures replace standard `setUp` and `tearDown` methods. The `yield` keyword elegantly separates initialization from cleanup within a single function. Scoping determines how often a fixture is invoked.

```python
import pytest
import sqlite3

# scope="session": Runs once per test suite invocation. Perfect for expensive DB spins.
@pytest.fixture(scope="session")
def db_connection():
    # SETUP
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    print("\\n[DB Session Started]")
    
    yield conn  # Hand control to the test function
    
    # TEARDOWN
    conn.close()
    print("\\n[DB Session Closed]")

# scope="function" (default): Runs for every test.
@pytest.fixture
def db_transaction(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    db_connection.rollback() # Ensure isolation between tests

def test_insert_user(db_transaction):
    db_transaction.execute("INSERT INTO users VALUES (1, 'Alice')")
    assert db_transaction.execute("SELECT count(*) FROM users").fetchone()[0] == 1
```

#### Parametrization
Avoid duplicating test logic. Parametrization runs the same test function multiple times with different matrix inputs, generating distinct test cases in the report.

```python
def is_valid_email(email):
    return "@" in email and "." in email

@pytest.mark.parametrize("email, expected_result", [
    ("user@domain.com", True),
    ("invalid_email.com", False),
    ("user@domain", False),
    ("", False)
])
def test_email_validation(email, expected_result):
    assert is_valid_email(email) is expected_result
```

### 5.2 Mocking, Patching, and Side Effects

Unit testing requires isolating the Subject Under Test. The `unittest.mock` module provides tools to replace real dependencies (network calls, clocks, randomizers) with verifiable stubs.

```python
from unittest.mock import patch, MagicMock
import requests

def process_payment(user_id, amount):
    response = requests.post("https://api.stripe.com/charge", json={"id": user_id, "amount": amount})
    if response.status_code == 200:
        return "Success"
    raise ValueError("Payment failed")

# @patch replaces the target object in the specified module namespace
@patch('requests.post')
def test_process_payment_success(mock_post):
    # Configure the mock's return value
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    result = process_payment("user123", 50.0)
    
    assert result == "Success"
    # Verify the contract was respected
    mock_post.assert_called_once_with(
        "https://api.stripe.com/charge", 
        json={"id": "user123", "amount": 50.0}
    )

@patch('requests.post')
def test_process_payment_failure_side_effect(mock_post):
    # side_effect is used to raise exceptions or iterate through multiple returns
    mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")
    
    with pytest.raises(requests.exceptions.Timeout):
        process_payment("user123", 50.0)
```

---

## 6. Profiling, Benchmarking, and Performance Optimization

"Premature optimization is the root of all evil," but deferred profiling is the root of production outages. Profiling replaces guesswork with empirical data, allowing you to target the 20% of the codebase causing 80% of the latency.

### 6.1 Macro CPU Profiling (`cProfile`)

`cProfile` is a deterministic C-extension profiler built into Python. It records the total time spent in every function execution across your entire program.

#### Execution and CLI Output
```bash
python -m cProfile -s tottime my_script.py
```
- `-s tottime`: Sorts by internal time spent in the function (excluding calls to sub-functions). This finds your CPU bottlenecks.
- `-s cumtime`: Sorts by cumulative time (including sub-functions). This finds your architectural bottlenecks.

Output columns:
- `ncalls`: Total number of times the function was called. High `ncalls` + low `tottime` suggests function call overhead.
- `tottime`: Total time spent in the function itself.
- `percall`: `tottime` divided by `ncalls`.
- `cumtime`: Cumulative time spent in this and all subfunctions.

#### Visualization via SnakeViz
Analyzing raw `cProfile` text output is grueling. Exporting the binary `.prof` file and visualizing it via interactive icicle graphs is the industry standard.

```bash
# 1. Generate binary profile file
python -m cProfile -o app_profile.prof my_app.py

# 2. View in browser via snakeviz (pip install snakeviz)
snakeviz app_profile.prof
```

### 6.2 Micro CPU Profiling (`line_profiler`)

Once `cProfile` identifies the slow function, `line_profiler` identifies the exact line of code causing the delay. This requires a third-party installation.

1. `pip install line_profiler`
2. Add the `@profile` decorator to the suspect function. (Do not import it; the runner injects it).
```python
@profile
def slow_function():
    data = [i for i in range(100000)] # Line 1
    total = sum(data)                 # Line 2
    return total
```
3. Run using `kernprof`:
```bash
kernprof -l -v my_app.py
```
*Output will show time percentage per line, clearly indicating if a list comprehension or a specific math operation is the culprit.*

### 6.3 Memory Profiling and Leak Detection

Memory bounds are often more critical than CPU bounds in containerized environments (Kubernetes OOMKills).

#### `memory_profiler`
Analyzes RAM allocation line-by-line.
1. `pip install memory_profiler`
2. Add `@profile` and run:
```bash
python -m memory_profiler my_app.py
```
*Note: Memory profiling hooks deep into the interpreter and drastically slows down execution. Run it on isolated scripts.*

#### `tracemalloc` (Built-in standard library)
For tracking down memory leaks in long-running processes (like APIs), `tracemalloc` snapshots memory allocation blocks over time.

```python
import tracemalloc
import gc

tracemalloc.start()

# ... Code that simulates a memory leak ...
leaky_list = []
for i in range(10000):
    leaky_list.append(str(i) * 100)
    
# Force garbage collection to ensure we only see uncollected objects
gc.collect()

# Take a snapshot and compare or analyze
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 5 Memory Consuming Lines ]")
for stat in top_stats[:5]:
    print(stat)
```

### 6.4 Micro-Benchmarking with `timeit`

For rapid A/B testing of specific algorithms or data structure choices, `timeit` bypasses profiler overhead and runs code thousands of times to get statistically significant averages.

```bash
# Compare list comprehension vs map via CLI
python -m timeit -n 10000 "[str(x) for x in range(100)]"
python -m timeit -n 10000 "list(map(str, range(100)))"
```

```python
# Programmatic timing
import timeit

setup = "import re; string = 'hello 123 world'; pattern = re.compile(r'\\d+')"
# Test pre-compiled regex vs inline compilation
t1 = timeit.timeit("pattern.search(string)", setup=setup, number=100000)
t2 = timeit.timeit("re.search(r'\\d+', string)", setup="import re; string = 'hello 123 world'", number=100000)

print(f"Pre-compiled: {t1:.4f}s")
print(f"Inline:       {t2:.4f}s")
```

---

## Conclusion

This comprehensive manual encapsulates the core competencies required for advanced Python engineering. 

Mastery of data structures and their memory implications (Big-O, `__slots__`) ensures performant code at scale. Metaprogramming via decorators and metaclasses allows for elegant, DRY architectural design. Embracing `asyncio` unlocks massive I/O concurrency vital for modern microservices and web scrapers. 

However, architecture is meaningless without reliability; strict adherence to the Testing Pyramid using Pytest fixtures and mock isolation guarantees correctness. Finally, leveraging empirical profiling tools (`cProfile`, `line_profiler`, `tracemalloc`) empowers engineers to diagnose and resolve production bottlenecks methodically, rather than relying on intuition. 

By integrating these practices into your daily workflow, you transition from writing functional scripts to architecting robust, enterprise-grade Python software.
""")

final_content = "".join(parts)
word_count = len(final_content.split())

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"Successfully wrote {word_count} words to {filepath}")
