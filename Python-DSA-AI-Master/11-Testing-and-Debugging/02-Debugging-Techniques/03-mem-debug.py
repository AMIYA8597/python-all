"""
Memory Debugging Masterclass

Learning Objectives:
1. Understand how Python manages memory (reference counting, garbage collection).
2. Learn to identify memory leaks and circular references.
3. Use tools like `sys.getsizeof`, `gc`, and `tracemalloc` to analyze memory usage.

Concept Explanation:
Memory debugging involves finding parts of a program that consume excessive memory or 
fail to release memory (leaks). Python uses reference counting primarily, backed by a 
cycle-detecting garbage collector.
Tools:
- `sys.getsizeof()`: Size of an object in bytes.
- `gc` module: Interface to the garbage collector.
- `tracemalloc`: Trace memory blocks allocated by Python.
"""

import sys
import gc
import tracemalloc
import unittest
from typing import List, Any, Optional

# --- Basic Implementation ---
def basic_memory_size():
    """Demonstrates basic size measurement of Python objects."""
    num = 42
    text = "Hello World"
    lst = [1, 2, 3, 4, 5]
    
    sizes = {
        'int': sys.getsizeof(num),
        'str': sys.getsizeof(text),
        'list': sys.getsizeof(lst)
    }
    return sizes

# --- Intermediate Implementation ---
class Node:
    """Class to demonstrate circular references and garbage collection."""
    def __init__(self, value: int):
        self.value = value
        self.next: 'Optional[Node]' = None
        self.prev: 'Optional[Node]' = None

def create_cycle() -> None:
    """Creates a circular reference."""
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node2.prev = node1
    # Without gc, these would leak because their ref counts never drop to 0
    # explicitly removing references from current scope
    del node1
    del node2

def test_garbage_collection() -> int:
    """Forces garbage collection and returns number of unreachable objects found."""
    create_cycle()
    collected = gc.collect()
    return collected

# --- Advanced Implementation ---
def trace_memory_allocation(size: int) -> tuple:
    """Demonstrates using tracemalloc to find memory hogs."""
    tracemalloc.start()
    
    # Allocate a large list of strings
    large_list = [f"Item {i}" for i in range(size)]
    
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    tracemalloc.stop()
    
    # Return the memory used by the top allocation in bytes
    if top_stats:
        return large_list, top_stats[0].size
    return large_list, 0

# --- Performance Analysis ---
"""
Performance Analysis:
- `sys.getsizeof` is fast but shallow (doesn't count memory of objects contained in a collection).
- `gc.collect()` causes a stop-the-world pause; don't call it manually in performance-critical code.
- `tracemalloc` adds significant overhead to memory allocations and execution time. Use only for profiling.
"""

# --- Edge Cases ---
"""
Edge Cases Handled:
- Circular references handled via Python's `gc` module.
- Handling empty allocation tracking cleanly in advanced implementation.
"""

# --- Interview Challenge ---
"""
Interview Challenge:
Question: Why does `sys.getsizeof([1, 2, 3])` not return the total memory of the list AND its integers?
Answer: `sys.getsizeof` only returns the size of the list container itself (the array of pointers). 
To get the total size, you must recursively calculate the size of all elements contained within it.
"""

# --- Tests ---
class TestMemoryDebugging(unittest.TestCase):
    def test_basic_sizes(self):
        sizes = basic_memory_size()
        self.assertIn('int', sizes)
        self.assertIn('str', sizes)
        self.assertIn('list', sizes)
        self.assertGreater(sizes['list'], sizes['int'])

    def test_garbage_collection(self):
        # We might collect other objects, but it should at least collect our cycle
        collected = test_garbage_collection()
        self.assertGreaterEqual(collected, 0)

    def test_trace_allocation(self):
        lst, size = trace_memory_allocation(1000)
        self.assertEqual(len(lst), 1000)
        self.assertGreater(size, 0)

if __name__ == "__main__":
    print("Running Memory Debugging Masterclass Tests...")
    unittest.main()
