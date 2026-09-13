"""
Memory Management: __slots__ Optimization

Learning Objectives:
1. Understand how Python stores object attributes in a dictionary (__dict__).
2. Learn how to use __slots__ to reduce memory footprint.
3. Compare memory usage between slotted and non-slotted classes.
4. Understand the limitations and edge cases of __slots__.

Concept Explanation:
By default, Python uses a dictionary (`__dict__`) to store instance attributes. This provides
flexibility but incurs a significant memory overhead, especially for millions of instances.
Defining `__slots__` tells Python to use a static array for attribute storage instead,
drastically reducing memory usage and slightly improving attribute access time.
"""

import sys
import timeit
from typing import Tuple

# --- Basic Implementation ---
class PointDict:
    """A standard class using __dict__ for attributes."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointSlots:
    """An optimized class using __slots__."""
    __slots__ = ('x', 'y')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# --- Intermediate Implementation ---
class InheritanceDict(PointDict):
    """Inheritance without slots."""
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

class InheritanceSlots(PointSlots):
    """Inheritance with slots. Subclass must declare its own slots!"""
    __slots__ = ('z',)
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

# --- Advanced Implementation / Performance Analysis ---
def compare_memory() -> Tuple[int, int]:
    """Compare memory usage of instances (shallow size)."""
    pd = PointDict(1.0, 2.0)
    ps = PointSlots(1.0, 2.0)
    
    # Measure object size + dict size if present
    pd_size = sys.getsizeof(pd) + sys.getsizeof(pd.__dict__)
    ps_size = sys.getsizeof(ps)
    return pd_size, ps_size

def compare_creation_time() -> None:
    """Compare instantiation time."""
    setup = "from __main__ import PointDict, PointSlots"
    t_dict = timeit.timeit("PointDict(1.0, 2.0)", setup=setup, number=1000000)
    t_slots = timeit.timeit("PointSlots(1.0, 2.0)", setup=setup, number=1000000)
    print(f"Creation Time - Dict:  {t_dict:.4f}s")
    print(f"Creation Time - Slots: {t_slots:.4f}s")

# --- Edge Cases ---
def demonstrate_edge_cases() -> None:
    """Demonstrate edge cases like missing __dict__ and multiple inheritance issues."""
    ps = PointSlots(1, 2)
    try:
        ps.z = 3  # Cannot add new attributes dynamically
    except AttributeError as e:
        print(f"Expected AttributeError: {e}")

# --- Interview Challenge ---
"""
Challenge: Design a class hierarchy representing an Abstract Syntax Tree (AST) node
where memory is critical (millions of nodes). Provide a base class and a leaf node
using slots.

Solution provided below in tests.
"""

class ASTNode:
    __slots__ = ()
    pass

class Literal(ASTNode):
    __slots__ = ('value',)
    def __init__(self, value: int):
        self.value = value

# --- Tests ---
def run_tests() -> None:
    """Run validation tests."""
    pd = PointDict(1, 2)
    ps = PointSlots(1, 2)
    assert hasattr(pd, '__dict__')
    assert not hasattr(ps, '__dict__')
    
    node = Literal(42)
    assert node.value == 42
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: __slots__ ---")
    d_size, s_size = compare_memory()
    print(f"Memory (Dict): {d_size} bytes")
    print(f"Memory (Slots): {s_size} bytes")
    if d_size > 0:
        print(f"Memory Reduction: {(d_size - s_size) / d_size * 100:.1f}%")
    compare_creation_time()
    demonstrate_edge_cases()
    run_tests()
