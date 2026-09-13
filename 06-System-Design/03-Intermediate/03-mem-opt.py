"""
System Design: Memory Optimization in Python
============================================

Learning Objectives:
1. Understand how Python manages memory under the hood (reference counting, garbage collection).
2. Learn techniques to reduce the memory footprint of Python objects.
3. Master the use of `__slots__` to optimize memory usage of classes.
4. Understand String Interning and Flyweight design patterns for memory efficiency.
5. Learn how to use generators and memory views for large data processing.

Concept Explanation:
--------------------
Python is a high-level language with automatic memory management. Every object in Python has an overhead (at least 28 bytes for an integer in CPython 64-bit, and dictionaries for class instance attributes). 
When designing systems that load millions of objects (e.g., ORM models, data ingestion pipelines, games), this overhead can lead to excessive memory consumption and frequent garbage collection pauses (OOM errors or latency spikes).

Techniques:
- `__slots__`: Prevents the creation of a per-instance `__dict__` and `__weakref__`, significantly reducing memory.
- Generators: Yield items one by one instead of loading everything into memory (Lists vs Generators).
- String Interning: Reusing the same string objects in memory.
- `array` module / `memoryview`: Using contiguous typed arrays instead of lists of generic Python objects.

Industry Use Cases:
-------------------
- High-frequency trading systems where low latency (less GC) and caching are required.
- Data science pipelines loading massive CSVs/JSONs.
- Game servers tracking millions of entities (players, NPCs, items).

Basic Implementation:
---------------------
"""
import sys
import gc
from typing import List, Generator, Any, Tuple

# 1. Basic vs Optimized Class (using __slots__)

class PointBasic:
    """A simple point class with a __dict__ for attributes."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointOptimized:
    """A memory-optimized point class using __slots__."""
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# 2. Generator for Large Data Processing

def load_data_basic(num_items: int) -> List[int]:
    """Loads all items into memory at once."""
    return [i for i in range(num_items)]

def load_data_optimized(num_items: int) -> Generator[int, None, None]:
    """Yields items one by one, keeping memory footprint O(1)."""
    for i in range(num_items):
        yield i


# Professional Implementation
# ---------------------------
# Let's implement a system that caches repeating strings (Flyweight pattern / Manual Interning)
# and uses __slots__ to represent a massive log of events.

class Event:
    __slots__ = ['timestamp', 'event_type', 'user_id']
    
    def __init__(self, timestamp: int, event_type: str, user_id: int):
        self.timestamp = timestamp
        self.event_type = event_type
        self.user_id = user_id

class EventProcessor:
    def __init__(self):
        self.event_type_cache = {}
        self.events: List[Event] = []
        
    def add_event(self, timestamp: int, raw_event_type: str, user_id: int):
        # String interning/flyweight: avoid duplicating identical strings in memory
        if raw_event_type not in self.event_type_cache:
            # sys.intern() can also be used for exact string interning in Python
            self.event_type_cache[raw_event_type] = sys.intern(raw_event_type)
            
        interned_type = self.event_type_cache[raw_event_type]
        self.events.append(Event(timestamp, interned_type, user_id))


def compare_memory():
    # Comparing Point classes
    p_basic = PointBasic(1.0, 2.0)
    p_opt = PointOptimized(1.0, 2.0)
    
    # __dict__ overhead
    dict_size = sys.getsizeof(p_basic.__dict__) if hasattr(p_basic, '__dict__') else 0
    basic_size = sys.getsizeof(p_basic) + dict_size
    opt_size = sys.getsizeof(p_opt)
    
    return basic_size, opt_size

# Complexity Analysis:
# Time Complexity: O(1) for object creation in both cases.
# Space Complexity: O(N * (sizeof(object) + sizeof(__dict__))) vs O(N * sizeof(object)).
# With `__slots__`, we save approximately 100-200 bytes per object. For 1 million objects, this is 100-200 MBs.

# Common Mistakes:
# 1. Inheriting from a class without __slots__ will implicitly create a __dict__ for the subclass, negating the benefits.
# 2. Adding properties to __slots__ that are not used, wasting memory.
# 3. Over-optimizing small scripts where development time is more valuable than a few MBs of RAM.

# Interview Challenge:
# Q: How does Python's Garbage Collection work, and how can you optimize a system that is experiencing GC pauses?
# A: Python uses Reference Counting primarily, supplemented by a Generational Garbage Collector to detect cyclic references. 
# To optimize GC pauses: 1. Reduce the total number of objects created (e.g., Object Pooling). 2. Break cyclic references manually or using `weakref`. 3. Tune GC thresholds (`gc.set_threshold()`) or disable GC temporarily during critical paths if you know cycles aren't being formed.

if __name__ == "__main__":
    print("Running Memory Optimization Tests...")
    
    # Test __slots__ memory savings
    basic_mem, opt_mem = compare_memory()
    print(f"Basic Point memory size: ~{basic_mem} bytes")
    print(f"Optimized Point memory size: ~{opt_mem} bytes")
    assert opt_mem < basic_mem, "Optimized version should use less memory."
    
    # Test Flyweight/Interning
    processor = EventProcessor()
    for i in range(1000):
        processor.add_event(1600000000 + i, "USER_LOGIN", i)
        
    # All events should point to the exact same string object in memory
    assert processor.events[0].event_type is processor.events[999].event_type
    
    print("All tests passed successfully.")
