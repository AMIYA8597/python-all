# Python Comprehensive Reference Guide

## Introduction
Python is a multi-paradigm, dynamically typed, interpreted, and garbage-collected programming language. Its design philosophy emphasizes code readability and simplicity. This document serves as a deep dive into Python's core mechanics, advanced concepts, and internal implementations.

## 1. The Python Object Model

Everything in Python is an object, and every object has three defining properties:
- **Identity:** The memory address of the object, accessible via `id()`.
- **Type:** Defines the operations supported by the object, accessible via `type()`.
- **Value:** The data held by the object.

### Mutable vs. Immutable
- **Immutable:** Ints, floats, strings, tuples, frozensets. Modifying an immutable object creates a *new* object.
- **Mutable:** Lists, dictionaries, sets, bytearrays. Modifying a mutable object changes it in place.

*Performance Consideration:* String concatenation in a loop (`str += next_str`) can be O(N^2) due to immutability. Use `''.join(list_of_strings)` which is O(N).

## 2. Memory Management & CPython Internals

CPython manages memory primarily through two mechanisms:
1.  **Reference Counting:** Every object maintains a count of references pointing to it. When the count drops to zero, the object is immediately deallocated.
2.  **Generational Garbage Collector (GC):** Reference counting cannot handle cyclical references (e.g., two objects pointing to each other). The cyclic GC runs periodically to detect and clean up these cycles, categorizing objects into three "generations" based on their lifespan to optimize performance.

### The Global Interpreter Lock (GIL)
The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once. 
- **Impact:** This makes multithreading in Python CPU-bound tasks effectively single-core. 
- **Solution:** Use the `multiprocessing` module for CPU-bound tasks, which creates separate processes with their own GIL and memory space. Multithreading is still highly effective for I/O-bound tasks (network requests, file operations).

## 3. Advanced Features

### Generators and Iterators
An iterator is any object that implements the `__iter__()` and `__next__()` dunder methods. Generators are a simpler way to create iterators using the `yield` keyword.
- **Why use them?** They evaluate lazily, meaning they generate items one at a time on the fly, drastically reducing memory consumption for large datasets.

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Uses minimal memory regardless of 'n'
for val in fibonacci(10):
    print(val)
```

### Decorators
Decorators are higher-order functions that take a function as an argument and return a modified function, allowing you to add behavior to functions dynamically without modifying their code.

```python
import functools
import time

def timer(func):
    """Decorator to measure execution time."""
    @functools.wraps(func) # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} secs")
        return result
    return wrapper

@timer
def heavy_computation():
    return sum(i * i for i in range(1000000))
```

### Metaclasses
Metaclasses are the "classes of classes". While classes define the behavior of instances, metaclasses define the behavior of classes. The default metaclass is `type`.
- **Use Case:** Automating class registration, validating attributes during class creation, or implementing Singletons.

## 4. Common Pitfalls & Security

- **Mutable Default Arguments:** Never use mutable types (lists, dicts) as default arguments. They are evaluated only *once* when the function is defined, not each time it is called.
  ```python
  # BAD
  def add_item(item, basket=[]):
      basket.append(item)
      return basket
  
  # GOOD
  def add_item(item, basket=None):
      if basket is None:
          basket = []
      basket.append(item)
      return basket
  ```
- **Security:** Avoid using `eval()` or `exec()` with untrusted input, as they can execute arbitrary code. Use `ast.literal_eval()` for safely evaluating strings containing Python literals.

## 5. Async/Await (Asynchronous I/O)
Python 3.5 introduced `async` and `await` for cooperative multitasking. It uses an Event Loop to manage coroutines, switching between them when one hits an I/O operation (like `await asyncio.sleep(1)`). This is highly efficient for web servers (e.g., FastAPI) and network crawlers.

## 6. Type Hinting
Introduced in PEP 484, type hints do not enforce types at runtime (Python remains dynamically typed) but allow static analysis tools (like `mypy`) and IDEs to catch errors before execution.

```python
from typing import List, Dict, Optional, Union

def process_data(items: List[str], config: Optional[Dict[str, int]] = None) -> Union[bool, str]:
    if not items:
        return False
    return "Processed"
```

## Interview Questions
1. How does Python's Garbage Collection handle cyclical references?
2. Explain the difference between `__new__` and `__init__`.
3. What is the GIL, and how does it affect concurrent programming in Python?
4. Write a decorator that retries a failing function up to 3 times before raising an exception.
