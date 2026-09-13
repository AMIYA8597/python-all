# Python Interview Guide: From Zero to Advanced

This is an extremely comprehensive, professional-grade interview guide for Python software engineers. It covers core internals, advanced concepts, architecture, and realistic interview scenarios.

---

## 1. Core Python Architecture & Internals

### 1.1 Memory Management & Garbage Collection
**Question:** How does Python manage memory? What happens when you create an object?
**Answer:**
Python manages memory dynamically through a private heap containing all Python objects. Management of this heap is ensured by the Python memory manager.
1. **Reference Counting:** Every object has a reference count. When it drops to zero, memory is immediately deallocated.
   - *Example:* `a = [1, 2, 3]` (ref count=1), `b = a` (ref count=2), `del a` (ref count=1).
2. **Generational Garbage Collection:** Reference counting cannot detect cyclic references (e.g., node A points to B, B points to A). Python has a built-in cycle-detecting garbage collector that runs periodically. It uses a generational approach (Gen 0, 1, and 2). New objects start in Gen 0. If they survive a GC sweep, they move to Gen 1, and so on.

**Interview Trap:** Assuming `gc.collect()` frees memory back to the OS. It frees memory back to the Python memory pool, but the OS might not immediately reclaim it due to memory fragmentation.

### 1.2 The Global Interpreter Lock (GIL)
**Question:** What is the GIL? How does it affect concurrency?
**Answer:**
The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once.
- **Why?** CPython's memory management is not thread-safe.
- **Impact:** CPU-bound multithreaded Python code will not utilize multiple cores and may run *slower* than single-threaded code due to context switching overhead.
- **Solutions:**
  - I/O-bound tasks: Threading or `asyncio` work perfectly (the GIL is released during I/O operations like network calls or file reads).
  - CPU-bound tasks: Use `multiprocessing` (spawns separate OS processes, each with its own GIL and memory) or C-extensions (like NumPy) that release the GIL during heavy computation.
  *Note: PEP 703 aims to make the GIL optional in future Python versions (nogil).*

---

## 2. Advanced Language Features

### 2.1 Decorators
**Question:** Explain decorators and write a parameterized decorator that retries a failing function.
**Answer:**
A decorator is a function that takes another function and extends its behavior without explicitly modifying it, utilizing closures.

```python
import time
from functools import wraps

def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func) # Preserves function metadata (name, docstring)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_retries=3, delay=2)
def unstable_network_call():
    print("Calling...")
    raise ConnectionError("Network failed")
```

### 2.2 Generators & Yield
**Question:** What is the difference between a list comprehension and a generator expression? When would you use `yield`?
**Answer:**
- **List Comprehension (`[x for x in data]`):** Evaluates entirely in memory. Fast, but crashes with large datasets (`MemoryError`).
- **Generator Expression (`(x for x in data)`):** Lazy evaluation. Yields one item at a time. Minimal memory footprint.
- **`yield`:** Pauses function execution and saves its local state. On the next `next()` call, it resumes where it left off. Excellent for processing streaming data or large files chunk by chunk.

### 2.3 Context Managers (`with` statement)
**Question:** How would you write a custom context manager for a database connection?
**Answer:**
You need to implement `__enter__` and `__exit__`.

```python
class DBConnection:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = None

    def __enter__(self):
        print(f"Connecting to {self.dsn}")
        self.conn = "mock_connection_object"
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        if exc_type is not None:
            print(f"Rolling back due to: {exc_val}")
        # Return True to suppress exceptions, False (default) to propagate
        return False
```

---

## 3. Data Structures & Complexity

Python interviews often test if you know the internal implementations of built-in types.

| Operation | `list` (Dynamic Array) | `dict` (Hash Table) | `set` (Hash Table) | `collections.deque` (Doubly Linked List) |
| :--- | :--- | :--- | :--- | :--- |
| Append/Add | O(1) amortized | O(1) amortized | O(1) amortized | O(1) |
| Insert at start (index 0)| O(N) | N/A | N/A | O(1) (using `appendleft`) |
| Lookup / `x in collection` | O(N) | O(1) average | O(1) average | O(N) |
| Delete element | O(N) | O(1) | O(1) | O(N) (O(1) at ends) |

**Pro Tip:** If you need a FIFO queue, NEVER use a Python list (`list.pop(0)` is O(N)). Always use `collections.deque`.

---

## 4. Object-Oriented Programming (OOP) & SOLID

**Question:** How does Python handle Multiple Inheritance, and what is the MRO?
**Answer:**
Python supports multiple inheritance. The **Method Resolution Order (MRO)** determines the order in which base classes are searched when calling a method. Python uses the C3 Linearization algorithm.
You can view it using `ClassName.__mro__` or `ClassName.mro()`. `super()` relies strictly on the MRO to delegate calls to the next class in the hierarchy, which avoids calling a common ancestor multiple times (the Diamond Problem).

### SOLID Principles in Python Context
1. **Single Responsibility (SRP):** A class should have one reason to change. (e.g., Don't put SQL queries inside your HTTP router class).
2. **Open/Closed (OCP):** Open for extension, closed for modification. Use abstract base classes (`abc.ABC`) and polymorphism instead of massive `if/elif` chains checking object types.
3. **Liskov Substitution (LSP):** Subclasses must be substitutable for their base classes. If a base class method returns a `list`, the subclass override shouldn't return a `dict`. Use Python type hinting (`mypy`) to enforce this.
4. **Interface Segregation (ISP):** Better to have many small specific interfaces (via Mixins or small ABCs) than one massive general-purpose class.
5. **Dependency Inversion (DIP):** Depend on abstractions, not concretions. Pass database connection objects into classes (Dependency Injection) rather than importing and instantiating a specific DB driver inside the class.

---

## 5. System Design (Python Centric)

### Microservices vs Monolith
Python frameworks like Django are great for Monoliths, while FastAPI/Flask are standard for Microservices.
- **Scaling Python:** Because of the GIL, a single Python process uses one core. To scale a backend, you run multiple worker processes (e.g., using `Gunicorn` with `uvicorn` workers) orchestrated by a reverse proxy (Nginx) or load balancer.
- **Asynchronous Tasks:** For heavy workloads (video processing, sending 10k emails), do not block the HTTP request. Offload work to a message broker (RabbitMQ/Redis) and process it via distributed task queues like **Celery**.

### Caching
- **In-memory:** `functools.lru_cache` for localized, single-process caching.
- **Distributed:** Redis/Memcached. Important for scaling across multiple Python processes where local memory isn't shared.

---

## 6. Real-World Debugging Scenario

**Interviewer:** "We have a Python service in production. Memory usage grows by 100MB every hour until it OOM crashes. How do you debug this?"
**Your Action Plan:**
1. **Identify it's a leak:** A steady, unbounded increase is a leak, not just a high-water mark.
2. **Tools:** I would use `tracemalloc`, a built-in Python library that tracks memory allocations. I would take a snapshot of memory, wait 10 minutes, take another, and compare them (`snapshot2.compare_to(snapshot1, 'lineno')`) to find the exact line of code allocating the unfreed memory.
3. **Common Python Causes:** 
   - Appending to global lists/dicts indefinitely.
   - Caching without eviction policies (using `{}` instead of `lru_cache`).
   - Circular references with custom `__del__` methods (though modern Python handles this better, it can still cause GC issues in complex C-extensions).
   - Leaving open file descriptors or database connections without using context managers.

---
*End of Guide. Master these concepts, practice implementing decorators and data structures from scratch, and understand the GIL inside out to ace senior Python interviews.*
