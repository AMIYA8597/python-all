"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - PERFORMANCE TRAPS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I need to parse a 10 GB file and concatenate the lines into a 
# single string. I wrote `result += line` in a loop. Why is my server frozen?"
#
# A junior engineer has no idea. A senior engineer knows that Strings in Python 
# are mathematically IMMUTABLE. When you do `a += b`, Python does not just append 
# the memory. It forces the CPU to allocate a massive brand new chunk of RAM, 
# copy `a` into it, copy `b` into it, and then destroy the old `a`. In a loop 
# of 1 Million iterations, this results in O(N^2) catastrophic memory thrashing!
# You MUST use `''.join(list_of_strings)`.
#
# Interviewer: "I instantiated 10 Million Object nodes for a Graph. My server 
# crashed with an Out-Of-Memory (OOM) error. I cannot use less objects. Fix it."
# 
# A senior engineer knows that every Python object possesses a hidden Hash Table 
# (`__dict__`) to store its attributes, which wastes hundreds of bytes per object. 
# By using `__slots__`, you physically destroy the Hash Table and replace it 
# with a statically allocated C-struct array, instantly saving 60% of RAM!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master String Immutability (`+=` vs `.join()`).
# - Master Memory Optimization with `__slots__`.
# - Understand exact memory profiling using `sys.getsizeof()`.
#
# ==============================================================================
"""

import sys
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STRING IMMUTABILITY AND O(N^2) THRASHING
# ==============================================================================
def demonstrate_string_concatenation():
    section_header("String Immutability (`+=` vs `.join`)")
    
    # We will simulate 100,000 strings.
    # We keep the number small enough not to actually crash the script, but large 
    # enough to clearly show the mathematical scaling disaster.
    iterations = 100_000
    words = ["A"] * iterations
    
    print(f"Task: Concatenate {iterations} strings together.")
    
    # --- BAD METHOD: `+=` (O(N^2)) ---
    start = time.perf_counter()
    bad_string = ""
    for w in words:
        # EVERY loop creates a completely new string in RAM and copies everything!
        bad_string += w
    end = time.perf_counter()
    bad_time = end - start
    print(f"  -> `+=` Loop Time: {bad_time:.4f} seconds (Memory Thrashing!)")
    
    # --- GOOD METHOD: `.join()` (O(N)) ---
    start = time.perf_counter()
    # Python calculates the EXACT final size of the array, allocates RAM EXACTLY 
    # once, and drops all strings into it instantly.
    good_string = "".join(words)
    end = time.perf_counter()
    good_time = end - start
    print(f"  -> `.join()` Time:  {good_time:.6f} seconds (Perfect O(N))")
    
    if good_time > 0:
        print(f"\nThe `.join()` method was {bad_time / good_time:.0f}x faster!")


# ==============================================================================
# 4. __SLOTS__ (MASSIVE MEMORY OPTIMIZATION)
# ==============================================================================
class HeavyNode:
    """
    A standard Python class. 
    It possesses a hidden `__dict__` (Hash Table) to allow dynamic variable injection.
    Hash tables require massive memory overallocation to prevent collisions!
    """
    def __init__(self, val1, val2, val3):
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3

class LightNode:
    """
    A __slots__ optimized class.
    We explicitly tell the CPython compiler: "I mathematically SWEAR that I will 
    never, ever add a new variable to this class other than these three."
    CPython deletes the Hash Table entirely and builds a static C-array!
    """
    __slots__ = ['val1', 'val2', 'val3']
    
    def __init__(self, val1, val2, val3):
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3

def demonstrate_slots():
    section_header("__slots__ Memory Optimization")
    
    heavy = HeavyNode(1, 2, 3)
    light = LightNode(1, 2, 3)
    
    # Calculating the true memory footprint!
    # A standard object size + the size of its internal Hash Table!
    heavy_size = sys.getsizeof(heavy) + sys.getsizeof(heavy.__dict__)
    
    # A slotted object doesn't have a __dict__ at all!
    light_size = sys.getsizeof(light)
    
    print(f"Memory used by ONE Heavy Node: {heavy_size} bytes")
    print(f"Memory used by ONE Light Node:  {light_size} bytes")
    
    # Let's project this to 10 Million nodes (A standard graph size)
    MB = 1024 * 1024
    heavy_total_mb = (heavy_size * 10_000_000) / MB
    light_total_mb = (light_size * 10_000_000) / MB
    
    print("\nProjecting to 10 Million Objects (Large Graph):")
    print(f"  Heavy Nodes Total RAM: {heavy_total_mb:.0f} MB")
    print(f"  Light Nodes Total RAM:  {light_total_mb:.0f} MB")
    
    print(f"\nBy adding EXACTLY ONE LINE of code (`__slots__`), we saved ")
    print(f"{(heavy_total_mb - light_total_mb):.0f} Megabytes of RAM!")
    
    print("\nProof that Hash Tables are destroyed:")
    try:
        light.new_variable = "Hacked!"
    except AttributeError as e:
        print(f"  [CRASH PREVENTED] {e} (Dynamic injection is mathematically blocked!)")


def run_all_labs():
    demonstrate_string_concatenation()
    demonstrate_slots()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does `a += b` for strings result in $O(N^2)$ algorithmic complexity inside a loop?"
   Senior Answer: "In Python, Strings are strictly Immutable. They are written as highly optimized, statically sized C-arrays in RAM. When you execute `a += b`, the CPython engine cannot simply append data to the end of `a` because there is no allocated space! It must ask the OS for a brand new, larger block of RAM, physically copy every byte of `a` into it, physically copy every byte of `b` into it, and then mark the old memory for Garbage Collection. If you do this in a loop of 1 Million strings, the CPU performs $1 + 2 + 3 + ... + 1,000,000$ memory copies, which is a mathematical Arithmetic Progression resolving to $O(N^2)$. It is a catastrophic memory thrashing disaster. You must use `.join()` which pre-calculates the exact required final memory size and allocates it exactly once ($O(N)$)."

2. Interviewer: "I created 50 Million Python objects and ran out of RAM. How does `__slots__` magically fix this?"
   Senior Answer: "Python is a dynamic language. By default, every single Object you create contains a hidden `__dict__`. This is a fully functional Hash Table that allows you to dynamically inject new variables at runtime (e.g., `obj.hacked = 5`). Hash Tables are incredibly memory-heavy because they must overallocate empty arrays (RAM holes) to prevent hash collisions! For 50 Million objects, you are creating 50 Million massive Hash Tables. When you define `__slots__ = ['x', 'y']`, you mathematically command the CPython compiler to physically destroy the `__dict__` architecture for that class, and replace it with a statically sized, rigid C-struct. You lose the ability to dynamically inject variables, but you instantly save up to 60% of physical RAM."

3. Interviewer: "How do you mathematically profile a Python script to find the exact line causing a CPU bottleneck?"
   Senior Answer: "You never guess. You must use deterministic profiling tools. The built-in `cProfile` module acts as a C-level hook that intercepts every single function call and return, logging the exact cumulative time and call count. However, `cProfile` only gives you function-level granularity. If I have a massive 500-line function, I must use `line_profiler`. By placing a `@profile` decorator on the function, the engine compiles statistics for every single physical line of code inside the function, instantly exposing the exact algorithmic bottleneck down to the microsecond."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Performance Traps) Completed.")
