"""
# ==============================================================================
# LABORATORY: ADVANCED PERFORMANCE & MEMORY OPTIMIZATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When writing Python for High-Frequency Trading, massive ML pipelines, or 
# high-throughput APIs, standard optimizations aren't enough. You must understand 
# Zero-Copy protocols (memoryview) to prevent RAM duplication, how JIT compilers 
# (PyPy) work, and how to rigorously eliminate function call overhead.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Eliminate function call overhead (inlining in Python).
# - Master `memoryview` for Zero-Copy byte manipulation.
# - Understand PyPy (Just-In-Time Compilation).
# - Pre-computing and lookups (O(1) dictionary maps vs math).
#
# ==============================================================================
"""

import timeit
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FUNCTION CALL OVERHEAD & INLINING
# ==============================================================================

def add_numbers(x: int, y: int) -> int:
    return x + y

def demonstrate_call_overhead():
    """
    Function calls in Python are incredibly expensive because Python must push
    state to the stack, create a new local namespace dictionary, and resolve it.
    For critical inner loops (e.g., inside an algorithm), you must manually INLINE.
    """
    section_header("Function Call Overhead")
    
    # 1. Loop WITH function calls
    def loop_with_calls():
        total = 0
        for i in range(1_000_000):
            total = add_numbers(total, i)
        return total

    # 2. Loop INLINED (No function calls)
    def loop_inlined():
        total = 0
        for i in range(1_000_000):
            total += i
        return total
        
    time_calls = timeit.timeit(loop_with_calls, number=10)
    time_inlined = timeit.timeit(loop_inlined, number=10)
    
    print(f"Time WITH function calls: {time_calls:.4f}s")
    print(f"Time INLINED (manual):    {time_inlined:.4f}s")
    print(f"Inlining is {time_calls/time_inlined:.2f}x faster!")


# ==============================================================================
# 4. ZERO-COPY PROTOCOLS (MEMORYVIEW)
# ==============================================================================

def demonstrate_memoryview():
    """
    Slicing a byte string creates a massive COPY of the memory.
    If you are parsing a 1GB network packet, `data[500:]` creates a new 1GB string!
    `memoryview` allows you to slice memory WITHOUT copying it (Zero-Copy).
    """
    section_header("Zero-Copy Protocols (memoryview)")
    
    # 100 MB of raw bytes
    raw_data = b"x" * 100_000_000 
    
    print("--- Normal Slicing (Creates a copy) ---")
    start = time.perf_counter()
    # This allocates 50MB of brand new RAM!
    slice_copy = raw_data[50_000_000:] 
    print(f"Sliced 50MB in: {time.perf_counter() - start:.6f}s")
    
    print("\n--- Memoryview Slicing (Zero-Copy) ---")
    start = time.perf_counter()
    
    # We wrap the bytes in a memoryview. 
    # It acts like a window looking at the original memory.
    m_view = memoryview(raw_data)
    
    # This takes O(1) time and 0 extra RAM, regardless of size!
    slice_view = m_view[50_000_000:] 
    print(f"MemoryView sliced in: {time.perf_counter() - start:.6f}s (Instant!)")
    
    assert slice_copy == slice_view, "The data is identical."


# ==============================================================================
# 5. PRE-COMPUTING / LOOKUP TABLES
# ==============================================================================

def demonstrate_lookup_tables():
    """
    In tight loops, math operations can be slow. Pre-computing all possible 
    answers and storing them in an O(1) lookup table (dictionary/list) is much faster.
    """
    section_header("Lookup Tables vs Real-time Math")
    
    # We want to perform some "complex" operation in a loop
    def complex_math(x: int) -> int:
        return (x * 123) % 17
        
    # Pre-compute all answers for inputs 0 to 100
    LOOKUP_TABLE = {i: complex_math(i) for i in range(101)}
    
    def math_loop():
        total = 0
        for i in range(100):
            total += complex_math(i)
        return total
            
    def lookup_loop():
        total = 0
        for i in range(100):
            total += LOOKUP_TABLE[i]
        return total
        
    time_math = timeit.timeit(math_loop, number=100000)
    time_lookup = timeit.timeit(lookup_loop, number=100000)
    
    print(f"Real-time Math time: {time_math:.4f}s")
    print(f"Lookup Table time:   {time_lookup:.4f}s")
    print(f"Lookup Table is {time_math/time_lookup:.2f}x faster!")


# ==============================================================================
# 6. PYPY (JIT COMPILATION)
# ==============================================================================

def demonstrate_pypy():
    section_header("PyPy (Just-In-Time Compilation)")
    
    print("""
CPython (Standard Python): 
 - Compiles code to Bytecode (.pyc).
 - Interprets the Bytecode line-by-line using a C loop.
 - Slow for math because of type checking overhead.

PyPy (Alternative Interpreter):
 - Uses a JIT (Just-In-Time) Compiler.
 - It watches the program run. If it notices a function is called thousands of times 
   (a "hot loop"), it compiles that specific function down to raw Machine Code (Assembly) 
   ON THE FLY.
 - PyPy can run pure Python code 5x to 10x faster than CPython with NO code changes!
 
Why doesn't everyone use PyPy?
 - PyPy has a heavier startup time and memory footprint.
 - C-extensions (like NumPy, Pandas, TensorFlow) are deeply integrated with CPython's 
   internal C-API. Historically, these did not work well with PyPy, though compatibility 
   is improving.
    """)


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why are function calls slow in Python?
   Answer: Python must push the current frame to the stack, create a new local namespace dictionary, resolve all arguments, and then clean it all up. For extremely tight loops, it is faster to manually inline the code.

2. What does `memoryview` do?
   Answer: It allows you to slice and pass around large blocks of memory (like byte strings or arrays) WITHOUT copying the underlying data (Zero-Copy protocol), saving massive amounts of RAM and CPU time.

3. How does PyPy achieve massive speedups over standard CPython?
   Answer: PyPy includes a JIT (Just-In-Time) compiler. It monitors the execution of the program, identifies "hot" loops or functions, and compiles them directly into raw machine code at runtime, completely bypassing the bytecode interpreter.
"""

if __name__ == "__main__":
    demonstrate_call_overhead()
    demonstrate_memoryview()
    demonstrate_lookup_tables()
    demonstrate_pypy()
    print("\n[SUCCESS] Laboratory: Advanced Performance Completed.")
