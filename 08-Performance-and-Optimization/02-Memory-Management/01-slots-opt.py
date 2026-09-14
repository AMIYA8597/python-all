"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (MEMORY MANAGEMENT - SLOTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# By default, every single class instance in Python contains a hidden `__dict__` 
# that stores its attributes. A dictionary is a Hash Table, which is heavily 
# optimized for speed, but catastrophic for memory because it must over-allocate 
# RAM to prevent hash collisions.
#
# A junior engineer instantiates 5,000,000 `Point3D(x, y, z)` objects to render 
# a 3D simulation. Python allocates 5,000,000 hidden Hash Tables. The server 
# crashes with a MemoryError, requiring expensive hardware upgrades.
#
# A senior engineer adds `__slots__ = ['x', 'y', 'z']` to the class. This completely 
# destroys the hidden `__dict__` and replaces it with a fixed-size C-array, 
# instantly reducing RAM consumption by 50-70% and drastically speeding up 
# attribute access times due to CPU cache locality.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `__slots__` implementation.
# - Prove memory savings mathematically using `sys.getsizeof` and `pympler`.
# - Understand the architecture of Python's dynamic attributes.
#
# ==============================================================================
"""

import sys
import timeit

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE CLASS (DYNAMIC HASH TABLE)
# ==============================================================================
class DynamicPoint:
    """
    A standard Python class. 
    It maintains a hidden `__dict__` Hash Table for its attributes.
    This allows you to do `p.new_attr = 5` at runtime, but costs massive RAM.
    """
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

# ==============================================================================
# 4. SLOTTED CLASS (FIXED C-ARRAY)
# ==============================================================================
class SlottedPoint:
    """
    An optimized Python class using `__slots__`.
    We are mathematically forbidding the creation of the `__dict__`.
    Memory is allocated in a fixed, contiguous block.
    """
    # Instructs CPython to use a fixed C-style struct!
    __slots__ = ['x', 'y', 'z']
    
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


# ==============================================================================
# 5. MATHEMATICAL MEMORY PROOF
# ==============================================================================
def demonstrate_memory_savings():
    section_header("Mathematical Proof of Memory Overhead")
    
    dp = DynamicPoint(1.0, 2.0, 3.0)
    sp = SlottedPoint(1.0, 2.0, 3.0)
    
    # 1. Measure the base object size
    dp_size = sys.getsizeof(dp)
    sp_size = sys.getsizeof(sp)
    
    # 2. Measure the hidden dictionary! (Slotted objects don't have one!)
    # `sys.getsizeof` does NOT recursively calculate the dictionary size by default!
    dp_dict_size = sys.getsizeof(dp.__dict__)
    
    total_dp_size = dp_size + dp_dict_size
    total_sp_size = sp_size # No dictionary!
    
    print(f"  [DYNAMIC POINT]")
    print(f"    -> Base Object Size:   {dp_size} bytes")
    print(f"    -> Hidden __dict__:    {dp_dict_size} bytes")
    print(f"    -> Total Memory Cost:  {total_dp_size} bytes")
    
    print(f"\n  [SLOTTED POINT]")
    print(f"    -> Base Object Size:   {sp_size} bytes")
    print(f"    -> Hidden __dict__:    DOES NOT EXIST (0 bytes)")
    print(f"    -> Total Memory Cost:  {total_sp_size} bytes")
    
    savings = ((total_dp_size - total_sp_size) / total_dp_size) * 100
    print(f"\n  [CONCLUSION] __slots__ reduced RAM consumption by {savings:.2f}% per object!")
    
    # Proof of architectural rigidity
    print("\n  [ARCHITECTURE PROOF]")
    print("    Attempting to dynamically add an attribute to DynamicPoint...")
    dp.color = "red"
    print("    -> SUCCESS! (Hash Table expanded)")
    
    print("    Attempting to dynamically add an attribute to SlottedPoint...")
    try:
        sp.color = "red"
    except AttributeError as e:
        print(f"    -> FAILED AS EXPECTED! Error: {e}")


# ==============================================================================
# 6. CPU ACCESS SPEED PROOF
# ==============================================================================
def demonstrate_speed_benefits():
    section_header("Mathematical Proof of CPU Speed Acceleration")
    
    setup_dynamic = """
from __main__ import DynamicPoint
dp = DynamicPoint(1.0, 2.0, 3.0)
    """
    
    setup_slotted = """
from __main__ import SlottedPoint
sp = SlottedPoint(1.0, 2.0, 3.0)
    """
    
    # We are testing the raw speed of attribute read access
    stmt_dynamic = "dp.x; dp.y; dp.z"
    stmt_slotted = "sp.x; sp.y; sp.z"
    
    iterations = 5_000_000
    
    print(f"  Executing {iterations:,} attribute read requests...")
    
    time_dynamic = timeit.timeit(stmt=stmt_dynamic, setup=setup_dynamic, number=iterations)
    time_slotted = timeit.timeit(stmt=stmt_slotted, setup=setup_slotted, number=iterations)
    
    print(f"    -> Dynamic Access Time: {time_dynamic:.4f}s")
    print(f"    -> Slotted Access Time: {time_slotted:.4f}s")
    
    speedup = ((time_dynamic - time_slotted) / time_dynamic) * 100
    print(f"\n  [CONCLUSION] __slots__ accelerated CPU access speeds by {speedup:.2f}%!")


def run_all_labs():
    demonstrate_memory_savings()
    demonstrate_speed_benefits()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does Python attach a `__dict__` to classes by default instead of using fixed memory like C++ or Java?"
   Senior Answer: "Python is fundamentally a dynamic language. It prioritizes developer velocity and runtime flexibility over raw memory optimization. The `__dict__` allows developers to dynamically inject brand-new attributes into an object at runtime (Monkey Patching), which is heavily used in Mocking frameworks, testing, and dynamic ORMs. C++ and Java enforce static typing and rigid memory layouts at compile-time, physically forbidding dynamic structural modifications. `__slots__` is Python's opt-in mechanism to sacrifice that dynamic flexibility in exchange for C-like memory strictness."

2. Interviewer: "Why is attribute access actually *faster* when using `__slots__`?"
   Senior Answer: "When you access `obj.x` on a standard object, the CPython interpreter must execute a cryptographic hash on the string `'x'`, traverse the memory pointers into the `__dict__` Hash Table, resolve potential hash collisions, and finally extract the value. This scatters memory access across the RAM. When using `__slots__`, CPython creates a static C-struct with predefined memory offsets. Accessing `obj.x` becomes a direct $O(1)$ pointer arithmetic operation (e.g., `Base Address + 8 bytes`), entirely bypassing the hashing algorithm and drastically improving CPU L1 Cache locality."

3. Interviewer: "If `__slots__` is so mathematically superior for RAM and CPU, why shouldn't we just put it on every single class we ever write?"
   Senior Answer: "Because it destroys Python's dynamic ecosystem. 1. You can no longer dynamically add attributes. 2. Multiple Inheritance becomes a nightmare; you cannot inherit from two classes that both define `__slots__` with overlapping layouts. 3. It breaks legacy serialization tools (like some older `pickle` protocols) that explicitly look for `__dict__`. 4. If you have a class that is only instantiated 10 times (like a Database Connection Manager), the memory savings of `__slots__` (a few kilobytes) are completely irrelevant, but the loss of dynamic flexibility is permanent. `__slots__` should strictly be reserved for 'Data Classes' that will be instantiated millions of times (e.g., Nodes in a massive Graph or 3D coordinate vectors)."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Memory Management (Slots) Completed.")
