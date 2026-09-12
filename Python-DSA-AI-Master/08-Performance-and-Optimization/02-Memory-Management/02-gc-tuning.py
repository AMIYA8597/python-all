"""
Memory Management: Garbage Collection Tuning

Learning Objectives:
1. Understand Python's Garbage Collection (GC) mechanism (reference counting + cyclic GC).
2. Learn how to interact with the `gc` module.
3. Discover how to temporarily disable or tune the garbage collector for performance.
4. Profile the impact of GC operations.

Concept Explanation:
Python uses reference counting as its primary memory management technique. However,
to handle reference cycles (e.g., A references B, B references A), a generational
garbage collector runs periodically. Disabling or tuning this cyclic GC can yield
performance improvements during bulk object creation or deletion phases, provided
you avoid memory leaks.
"""

import gc
import time
from typing import List

# --- Basic Implementation ---
def trigger_gc() -> int:
    """Manually trigger garbage collection and return the number of collected objects."""
    unreachable = gc.collect()
    return unreachable

# --- Intermediate Implementation ---
class Node:
    """A node that creates a reference cycle."""
    def __init__(self, name: str):
        self.name = name
        self.ref = None

def create_cycles(count: int) -> None:
    """Create reference cycles that reference counting alone cannot clean up."""
    for i in range(count):
        n1 = Node(f"A{i}")
        n2 = Node(f"B{i}")
        n1.ref = n2
        n2.ref = n1

# --- Advanced Implementation / Performance Analysis ---
def performance_with_gc(count: int) -> float:
    """Measure time to create cyclic objects with GC enabled."""
    gc.enable()
    start = time.perf_counter()
    create_cycles(count)
    end = time.perf_counter()
    return end - start

def performance_without_gc(count: int) -> float:
    """Measure time to create cyclic objects with GC temporarily disabled."""
    gc.disable()
    start = time.perf_counter()
    create_cycles(count)
    # Re-enable and collect to avoid actual memory leaks after the operation
    gc.enable()
    gc.collect()
    end = time.perf_counter()
    return end - start

# --- Edge Cases ---
def threshold_tuning() -> None:
    """Demonstrate getting and setting GC thresholds."""
    orig_thresholds = gc.get_threshold()
    print(f"Original GC Thresholds: {orig_thresholds}")
    # Tuning: Increase thresholds to reduce GC frequency
    gc.set_threshold(7000, 20, 20)
    print(f"New GC Thresholds: {gc.get_threshold()}")
    # Revert
    gc.set_threshold(*orig_thresholds)

# --- Interview Challenge ---
"""
Challenge: Write a context manager that temporarily disables the GC to 
speed up a memory-intensive block of code, and re-enables it afterwards.

Solution below.
"""

class GCDisabled:
    def __enter__(self):
        self.was_enabled = gc.isenabled()
        gc.disable()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.was_enabled:
            gc.enable()

# --- Tests ---
def run_tests() -> None:
    """Run validation tests."""
    with GCDisabled():
        assert not gc.isenabled()
    assert gc.isenabled()
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: GC Tuning ---")
    COUNT = 100_000
    t_gc_on = performance_with_gc(COUNT)
    t_gc_off = performance_without_gc(COUNT)
    
    print(f"Time with GC on:  {t_gc_on:.4f}s")
    print(f"Time with GC off: {t_gc_off:.4f}s")
    
    threshold_tuning()
    run_tests()
