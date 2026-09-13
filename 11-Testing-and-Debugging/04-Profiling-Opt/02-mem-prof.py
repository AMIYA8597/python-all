"""
Memory Profiling in Python

Learning Objectives:
1. Understand how Python manages memory and the importance of memory profiling.
2. Learn to use the `tracemalloc` module to trace memory allocations.
3. Identify memory leaks or areas of high memory consumption.

Concept Explanation:
Memory profiling involves monitoring a program's memory usage over time. Python's 
automatic garbage collection handles most memory management, but memory leaks can 
still occur (e.g., holding references to large objects). `tracemalloc` is a built-in
module to trace memory blocks allocated by Python.

Imports:
- tracemalloc: For tracing memory allocation.
- sys: For basic size checks.
"""

import sys
import tracemalloc
from typing import List, Any, Dict

# ==========================================
# Basic Implementation: sys.getsizeof
# ==========================================

def basic_memory_check() -> None:
    """Uses sys.getsizeof to check the size of objects in bytes."""
    my_list = list(range(10000))
    my_generator = (i for i in range(10000))
    
    print(f"Size of list (10000 items): {sys.getsizeof(my_list)} bytes")
    print(f"Size of generator (10000 items): {sys.getsizeof(my_generator)} bytes")

# ==========================================
# Intermediate Implementation: Using tracemalloc
# ==========================================

def create_large_objects() -> List[Dict[str, int]]:
    """Creates a large list of dictionaries to consume memory."""
    return [{"id": i, "value": i * 2} for i in range(100000)]

def profile_memory_usage() -> None:
    """Uses tracemalloc to trace memory allocations."""
    tracemalloc.start()
    
    # Snapshot 1: Before allocation
    snapshot1 = tracemalloc.take_snapshot()
    
    # Allocate memory
    data = create_large_objects()
    
    # Snapshot 2: After allocation
    snapshot2 = tracemalloc.take_snapshot()
    
    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("[ Top 3 Memory Differences ]")
    for stat in top_stats[:3]:
        print(stat)
        
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")
    
    tracemalloc.stop()

# ==========================================
# Advanced Implementation: Finding Memory Leaks
# ==========================================

class MemoryLeakSimulator:
    """Simulates a memory leak by continually appending to a class-level list."""
    _leaked_data: List[List[int]] = []
    
    @classmethod
    def process_data(cls) -> None:
        """Processes data but inadvertently stores a reference to it."""
        chunk = list(range(10000))
        cls._leaked_data.append(chunk) # Leak!

def detect_leak() -> None:
    """Traces memory across iterations to detect leaks."""
    tracemalloc.start()
    
    for _ in range(5):
        MemoryLeakSimulator.process_data()
        
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("\n[ Top Memory Allocations (Leak Detection) ]")
    for stat in top_stats[:3]:
        print(stat)
        
    tracemalloc.stop()

# ==========================================
# Edge Cases & Interview Challenge
# ==========================================

"""
Edge Cases:
1. `sys.getsizeof()` only returns the size of the container, not the objects it contains.
   You need a recursive function to find the deep size of an object.
2. C-extensions might allocate memory outside of Python's allocator, which tracemalloc
   might not catch.

Interview Challenge:
Question: Explain the difference between reference counting and garbage collection in Python.
How can circular references lead to memory leaks, and how does the `gc` module help?
Hint: Reference counting cannot detect cyclic references (A -> B -> A). The gc module
specifically looks for reference cycles.
"""

def test_memory_profiling() -> None:
    """Basic test for memory profiling concepts."""
    assert sys.getsizeof([]) < sys.getsizeof([1, 2, 3])
    print("Tests passed.")

if __name__ == "__main__":
    print("--- Memory Profiling ---")
    print("1. Basic Size Checks:")
    basic_memory_check()
    
    print("\n2. Tracemalloc Profiling:")
    profile_memory_usage()
    
    print("\n3. Leak Detection Simulation:")
    detect_leak()
    
    print("\n4. Running Tests:")
    test_memory_profiling()
