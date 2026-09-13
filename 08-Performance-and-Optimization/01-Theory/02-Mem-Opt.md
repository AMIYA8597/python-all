# Memory Optimization and Garbage Collection in Python

## 1. Prerequisites
- **Python Fundamentals:** Understanding of variables, objects, and mutability.
- **Computer Science Basics:** Basic understanding of the Heap vs. the Stack.

## 2. Learning Objectives
- Understand the physical memory layout of a Python object (`PyObject`).
- Master the dual-system Garbage Collection mechanism in CPython (Reference Counting + Cyclic GC).
- Learn how to detect and debug memory leaks using the `gc` and `tracemalloc` modules.
- Implement memory optimization techniques like `__slots__`, Generators, and Array structures.

## 3. Why This Topic Exists
Python abstracts memory management away from the developer. You don't have to call `malloc()` or `free()` like in C. 
However, this abstraction comes at a massive cost. A simple integer in Python takes 28 bytes (compared to 4 bytes in C). When your application scales to processing gigabytes of data or millions of objects, this overhead can crash your servers with Out of Memory (OOM) errors. Understanding how Python manages memory is the only way to write highly scalable backend systems and data processing pipelines.

## 4. The Anatomy of a Python Object
In CPython, *everything* is an object. Every object is a C struct called `PyObject` allocated on the private heap.
A `PyObject` contains:
1. **Reference Count** (`ob_refcnt`): An integer tracking how many variables point to this object.
2. **Type Pointer** (`ob_type`): A pointer to the object's type (e.g., `int`, `str`), which defines what methods can be called on it.
3. **The Value itself**: The actual data.

*Because of this metadata, even a simple number like `5` consumes significantly more memory than a raw C integer.*

## 5. Garbage Collection (GC) in CPython

CPython uses a two-part system to clean up memory.

### Mechanism 1: Reference Counting (The Primary System)
Every time you assign an object to a variable, pass it to a function, or put it in a list, its Reference Count goes up. Every time a variable goes out of scope or is reassigned, the count goes down.
**Rule:** The absolute exact microsecond an object's reference count hits `0`, Python immediately destroys the object and frees the memory.

*Advantage:* Instant, deterministic memory cleanup.
*Fatal Flaw:* **Reference Cycles**.

### Mechanism 2: The Cyclic Garbage Collector
What happens if Object A points to Object B, and Object B points back to Object A? Their reference counts will never drop below 1, even if the rest of your program completely loses track of them. This is a memory leak.
To fix this, Python runs a background process called the **Cyclic Garbage Collector**.
- It periodically scans objects looking for isolated cycles and deletes them.
- It uses **Generational GC**. It groups objects into 3 generations (0, 1, 2). New objects go into Gen 0. If they survive a GC sweep, they are promoted to Gen 1. The GC sweeps Gen 0 very frequently, but sweeps Gen 2 very rarely.

## 6. Memory Optimization Techniques

### 1. `__slots__`
By default, every custom class instance in Python stores its attributes in a dynamic dictionary (`__dict__`). Dictionaries are hash tables that over-allocate memory to avoid collisions. If you create 1,000,000 instances of a `Point` class, you have 1,000,000 dictionaries overhead!
**Solution:** Define `__slots__`. This tells Python "Do NOT create a `__dict__`. Allocate exactly enough memory for these specific attributes in a fixed-size array."

```python
class NormalPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
# SlottedPoint uses ~40% less memory!
```

### 2. Generators & Lazy Evaluation
Do not load massive files or database tables into a list in RAM. Use `yield` to stream them one at a time.
```python
# BAD: Loads 10GB file into RAM all at once
lines = open('huge_log.txt').readlines()

# GOOD: Loads one line into RAM at a time
def read_log(path):
    with open(path) as f:
        for line in f:
            yield line
```

### 3. Using Appropriate Data Structures
- If you need an array of raw numbers, do not use a Python `list`. Use `array.array('i', [...])` or `numpy.array`. They store numbers in contiguous C-style arrays without the `PyObject` overhead.

## 7. Code Implementation: Profiling Memory

```python
import sys
import gc
import tracemalloc

def demonstrate_refcount():
    print("--- 1. Reference Counting ---")
    a = []          # Ref count = 1
    b = a           # Ref count = 2
    c = [a, b]      # Ref count = 4 (c has 2 pointers to it)
    print(f"Reference count of empty list: {sys.getrefcount(a)}") 
    # getrefcount() temporarily adds 1 to the count while executing

def demonstrate_memory_leak():
    print("\n--- 2. Reference Cycles ---")
    class Node:
        def __init__(self, name):
            self.name = name
            self.ref = None
            
    node_a = Node("A")
    node_b = Node("B")
    
    # Create a cycle
    node_a.ref = node_b
    node_b.ref = node_a
    
    # Delete the original variables
    del node_a
    del node_b
    
    # The nodes are still in memory because their ref counts are 1!
    # Let's force the cyclic GC to clean them up.
    collected = gc.collect()
    print(f"Cyclic GC collected {collected} unreachable objects from the cycle!")

def profile_slots_memory():
    print("\n--- 3. Tracing Memory (Slots vs No Slots) ---")
    class Normal:
        def __init__(self):
            self.val = 1
            
    class Slotted:
        __slots__ = ['val']
        def __init__(self):
            self.val = 1

    tracemalloc.start()
    normal_objects = [Normal() for _ in range(100000)]
    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory used by 100,000 Normal objects: {current / 1024 / 1024:.2f} MB")
    tracemalloc.stop()
    
    del normal_objects
    gc.collect()

    tracemalloc.start()
    slotted_objects = [Slotted() for _ in range(100000)]
    current, peak = tracemalloc.get_traced_memory()
    print(f"Memory used by 100,000 Slotted objects: {current / 1024 / 1024:.2f} MB")
    tracemalloc.stop()

if __name__ == "__main__":
    demonstrate_refcount()
    demonstrate_memory_leak()
    profile_slots_memory()
```

## 8. Common Mistakes
- **String Concatenation in Loops:** Doing `text += new_string` inside a loop creates a brand new string object in memory on every iteration, leaving the old one to be garbage collected. Use `"".join(list_of_strings)` instead.
- **Accidental Global Variables:** Variables attached to the global scope or class level never get their reference counts reduced to 0 until the program terminates.

## 9. Active Recall
1. Why does a Python integer take up more bytes than a C integer?
2. What is the fatal flaw of Reference Counting?
3. How does `__slots__` save memory?
4. How can you force Python to clean up cyclic references manually?

## 10. Interview Questions
**Q: "We have a Python script processing a massive CSV file, and it keeps crashing with an Out of Memory error. How do you fix it?"**
*Answer:* I would immediately check if the script is trying to load the entire file into a list or pandas DataFrame at once. I would refactor it to use a Generator to yield and process one row at a time. If the entire dataset must be kept in memory for some reason, I would ensure we are not creating custom class instances with `__dict__` overhead, instead using `__slots__`, or migrating the data into a dense structure like a NumPy array.

**Q: Explain how Generational Garbage Collection works in Python.**
*Answer:* Python categorizes objects into three generations (0, 1, 2) based on age. New objects go into Gen 0. The GC assumes "most objects die young" (like local variables in a function). Therefore, it scans Gen 0 very frequently. If an object survives a scan, it moves to Gen 1. If it survives again, it moves to Gen 2. Gen 2 is scanned very rarely, which saves significant CPU cycles compared to scanning the entire heap every time.
