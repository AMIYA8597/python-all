"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (MEMORY OPTIMIZATION & INTERNALS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a data processing pipeline that loads 10 Million User 
# profiles from a CSV into RAM to perform analysis.
#
# A junior engineer writes a standard Python `class User:` and instantiates 
# 10 Million objects. Suddenly, the server crashes with an Out-Of-Memory (OOM) 
# error! 
#
# Why? Because in Python, every single object dynamically stores its attributes 
# in an internal Dictionary (`__dict__`). Dictionaries are hash tables. Hash 
# tables pre-allocate massive chunks of empty memory to prevent hash collisions. 
# Your "small" User object actually consumes 300 bytes of RAM. 
# 10 Million * 300 bytes = 3 Gigabytes of pure overhead!
#
# By using advanced memory optimization techniques like `__slots__`, Generators, 
# or moving from Arrays of Objects (AoS) to Structures of Arrays (SoA) via 
# NumPy, you can mathematically reduce that 3 GB overhead down to 40 MB!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Python `__slots__` to destroy `__dict__` overhead.
# - Understand Generators (Lazy Evaluation) to bypass O(N) memory allocation.
# - Understand Garbage Collection (Reference Counting).
#
# ==============================================================================
"""

import sys
import tracemalloc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PYTHON __slots__ (DESTROYING DICTIONARY OVERHEAD)
# ==============================================================================
class HeavyUser:
    """Standard Python Class. Dynamically uses __dict__."""
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

class LightUser:
    """
    Optimized Python Class using __slots__.
    By strictly declaring the allowed attributes in advance, Python completely 
    deletes the underlying __dict__ hash table, storing the attributes in a 
    hyper-compact C-level array!
    """
    __slots__ = ['id', 'name', 'age']
    
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

def demonstrate_slots():
    section_header("Memory Optimization (__slots__)")
    
    heavy = HeavyUser(1, "Alice", 25)
    light = LightUser(1, "Alice", 25)
    
    # Measuring exact memory footprint
    size_heavy = sys.getsizeof(heavy) + sys.getsizeof(heavy.__dict__)
    size_light = sys.getsizeof(light)
    
    print("Memory Footprint of a single Instance:")
    print(f"  HeavyUser (Standard) : {size_heavy} bytes")
    print(f"  LightUser (__slots__): {size_light} bytes")
    
    savings = ((size_heavy - size_light) / size_heavy) * 100
    print(f"\nUsing __slots__ reduced RAM usage by {savings:.1f}%!")
    print("For 10 Million users, you just saved hundreds of Megabytes of RAM.")


# ==============================================================================
# 4. GENERATORS (LAZY EVALUATION)
# ==============================================================================
def load_massive_dataset_list(n: int) -> list[int]:
    """Eager Evaluation: Forces all N elements to exist in RAM simultaneously."""
    dataset = []
    for i in range(n):
        dataset.append(i * 2)
    return dataset

def load_massive_dataset_generator(n: int):
    """
    Lazy Evaluation (Generator): 
    The `yield` keyword mathematically pauses the function, returning ONE element.
    It does NOT allocate an array. It only calculates the next element when requested!
    """
    for i in range(n):
        yield i * 2

def demonstrate_generators():
    section_header("Memory Optimization (Generators vs Lists)")
    
    n = 1_000_000 # 1 Million items
    
    print("Task: Process a dataset of 1 Million elements.")
    
    # Measure RAM usage for List
    tracemalloc.start()
    eager_list = load_massive_dataset_list(n)
    current, peak_list = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Measure RAM usage for Generator
    tracemalloc.start()
    lazy_gen = load_massive_dataset_generator(n)
    current, peak_gen = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"\nRAM Spiked (Eager List) : {peak_list / 1_000_000:.2f} MB")
    print(f"RAM Spiked (Generator)  : {peak_gen / 1_000_000:.6f} MB")
    
    print("\nGenerators process infinite data using strictly O(1) RAM!")


def run_all_labs():
    demonstrate_slots()
    demonstrate_generators()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. If `__slots__` reduces RAM by 60%, why doesn't Python use it by default for every class?
   Answer: Python is fundamentally a "Dynamic" language. The core philosophy of Python allows you to write `obj.new_attribute = "Hello"` anywhere in your code, at runtime, dynamically injecting new properties into an object. This is only possible because of the underlying `__dict__` hash table! If Python enforced `__slots__` by default, it would mathematically freeze the structure of the class at creation time, violently rejecting any dynamic attribute assignment, turning Python into a rigid, statically-typed language (like Java or C++). You must explicitly opt-in to `__slots__` when you know your class structure is perfectly fixed and you need scale.

2. Explain how the `yield` keyword mathematically bypasses $O(N)$ memory limits.
   Answer: In a standard function with `return [array]`, the CPU physically calculates all $N$ elements, requests $N$ slots of memory from the RAM (malloc), fills them, and hands the massive block of memory to you. `yield` creates a Generator Object (a State Machine). When you loop over a Generator, it calculates *exactly one* element, hands it to you, and physically pauses its execution state. Once you process that element, it is Garbage Collected. The CPU then resumes the Generator to calculate the *next* single element. Because only 1 element exists in RAM at any given millisecond, it requires strictly $O(1)$ memory, regardless of whether $N$ is 10 or 10 Trillion!

3. How does Python's core Garbage Collector (Reference Counting) work, and what is a "Reference Cycle" memory leak?
   Answer: Every object in Python has a hidden integer called a Reference Count. If variable `A = Object`, the count is 1. If `B = A`, the count is 2. When `B` goes out of scope, the count drops to 1. When `A` goes out of scope, the count drops to 0! The very millisecond the count hits 0, CPython violently deallocates the object from RAM. It is instant and deterministic. However, if Object 1 points to Object 2, and Object 2 points back to Object 1 (a Circular Linked List), their Reference Counts will NEVER mathematically reach 0, even if the main program abandons them! This causes a silent Memory Leak. Python runs a secondary, slower "Tracing GC" periodically in the background specifically to hunt down and destroy these isolated cyclical islands.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Memory Optimization) Completed.")
