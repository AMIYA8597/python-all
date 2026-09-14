"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (DATA SCIENCE OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A data scientist writes a custom simulation algorithm using Pandas. Because 
# the algorithm requires looping through rows depending on complex previous states, 
# they are mathematically forced to use `.apply()` or a `for` loop. The 
# simulation of 10,000,000 rows takes 14 hours to execute. Pandas SIMD 
# vectorization cannot save them here.
#
# A senior optimization engineer understands "JIT Compilation". They install 
# `Numba`. They isolate the mathematical loop, add a `@njit` decorator, and 
# run the script. Numba mathematically intercepts the Python bytecode, translates 
# it into raw C++ equivalent LLVM machine code in memory, and bypasses the CPython 
# Interpreter completely. The simulation execution time collapses from 14 hours 
# to 3.5 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Just-In-Time (JIT) Compilation for raw numerical arrays.
# - Prove the extreme CPU overhead of the CPython Interpreter.
# - Differentiate between Pandas Vectorization and Numba JIT.
#
# ==============================================================================
"""

import timeit
import math
import random

# Gracefully handle missing dependencies
try:
    import numpy as np
    from numba import njit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False
    
def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE COMPLEX SIMULATION (THE BOTTLENECK)
# ==============================================================================
# We simulate a "Random Walk" or "Monte Carlo" simulation.
# The value of Step N mathematically depends on Step N-1, meaning we CANNOT 
# easily vectorize this in Pandas. We are forced to loop sequentially.

def python_random_walk(steps: int) -> float:
    """
    Standard Python Execution.
    The CPython Interpreter must evaluate every single variable assignment, 
    type check, and function call (math.sqrt) dynamically during runtime!
    """
    position = 0.0
    for i in range(1, steps + 1):
        # A complex arbitrary mathematical calculation
        if i % 2 == 0:
            position += math.sqrt(i) * 0.5
        else:
            position -= math.sqrt(i) * 0.3
    return position


# ==============================================================================
# 4. THE LLVM MACHINE CODE (NUMBA JIT)
# ==============================================================================
# Numba only works on pure mathematical operations and NumPy arrays!
# It will fail if you pass complex Python objects (like lists of strings or dictionaries).

if HAS_NUMBA:
    # @njit forces Numba to compile in "No Python" mode.
    # It mathematically guarantees the CPython interpreter is entirely bypassed.
    @njit
    def numba_random_walk(steps: int) -> float:
        """
        JIT Compiled Execution.
        When this runs the FIRST time, Numba freezes the thread, compiles this 
        code into raw C/Assembly LLVM bytecode, caches it in RAM, and executes it.
        """
        position = 0.0
        for i in range(1, steps + 1):
            if i % 2 == 0:
                position += math.sqrt(i) * 0.5
            else:
                position -= math.sqrt(i) * 0.3
        return position


# ==============================================================================
# 5. MATHEMATICAL PROOF OF COMPILATION
# ==============================================================================
def demonstrate_jit_compilation():
    section_header("Performance Proof: Python Bytecode vs LLVM Machine Code")
    
    if not HAS_NUMBA:
        print("  [ERROR] Numba/NumPy is not installed.")
        print("  Run `pip install numba numpy` to execute this lab.")
        return
        
    # 50 Million Iterations!
    STEPS = 50_000_000 
    print(f"  [INIT] Simulating {STEPS:,} sequential mathematical steps...")
    
    
    print("\n  [SCENARIO A: PURE PYTHON INTERPRETER]")
    start_py = timeit.default_timer()
    res_py = python_random_walk(STEPS)
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Final Position: {res_py:.2f}")
    print(f"    -> Execution Time: {time_py:.4f} seconds")
    
    
    print("\n  [SCENARIO B: NUMBA LLVM (FIRST RUN - COMPILING...)]")
    # The first run includes the overhead of translating Python to Assembly!
    start_jit_1 = timeit.default_timer()
    res_jit_1 = numba_random_walk(STEPS)
    end_jit_1 = timeit.default_timer()
    time_jit_1 = end_jit_1 - start_jit_1
    print(f"    -> Final Position: {res_jit_1:.2f}")
    print(f"    -> Execution Time: {time_jit_1:.4f} seconds (Included Compilation Tax!)")
    
    
    print("\n  [SCENARIO C: NUMBA LLVM (SECOND RUN - CACHED C-EXECUTION)]")
    # The second run is raw, uninterrupted bare-metal CPU execution.
    start_jit_2 = timeit.default_timer()
    res_jit_2 = numba_random_walk(STEPS)
    end_jit_2 = timeit.default_timer()
    time_jit_2 = end_jit_2 - start_jit_2
    print(f"    -> Final Position: {res_jit_2:.2f}")
    print(f"    -> Execution Time: {time_jit_2:.4f} seconds")
    
    
    speedup = time_py / time_jit_2
    print(f"\n  [CONCLUSION] Numba achieved a {speedup:.1f}x hardware speedup!")
    print("  By writing one decorator (`@njit`), you achieved the exact performance")
    print("  of writing the algorithm in pure C/C++.")


def run_all_labs():
    demonstrate_jit_compilation()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why can't we just put the `@njit` decorator on every single function in our Django web server to make it 100x faster?"
   Senior Answer: "Numba is strictly a mathematical JIT compiler (targeting the LLVM backend). It only understands basic primitives: Floats, Integers, and highly structured NumPy C-Arrays. It mathematically does NOT understand complex Python objects, dictionaries, HTTP requests, or Django ORM models. If you put `@njit` on a Django API endpoint, Numba will violently crash because it cannot translate a dynamic WSGI request object into raw C-structs. Numba is exclusively reserved for the microscopic mathematical 'leaf' functions inside a Data Science or Quantitative Trading pipeline that are physically burning CPU cycles inside heavy `for` loops."

2. Interviewer: "What is the difference between AOT (Ahead-Of-Time) compilation like Cython, and JIT (Just-In-Time) compilation like Numba?"
   Senior Answer: "Cython is AOT. The developer must manually rewrite their Python code using C-type hints (`cdef int i = 0`), and explicitly run a build script (`python setup.py build_ext`). The script invokes the GCC compiler to generate a physical `.so` or `.pyd` binary file on the hard drive *before* the application ever boots. Numba is JIT. The code remains $100\\%$ pure Python. When the application boots, and the interpreter hits the `@njit` function for the *very first time*, it dynamically pauses execution, mathematically translates the bytecode into Assembly in RAM, executes it, and caches the Assembly in RAM for the next call. JIT is infinitely easier to deploy but incurs a tiny 'Warmup Tax' on the first execution."

3. Interviewer: "If Pandas is backed by C (NumPy), why did we need Numba to optimize the Random Walk simulation?"
   Senior Answer: "Pandas/NumPy achieves speed through 'SIMD Vectorization' (Single Instruction, Multiple Data). Vectorization mathematically requires executing an identical operation across an entire array simultaneously (e.g., `array * 5`). However, a Random Walk simulation is 'State Dependent'. Step $N$ cannot be calculated until Step $N-1$ is fully complete! This mathematical dependency physically breaks SIMD vectorization, forcing the developer to use a slow sequential `for` loop. When forced into a sequential loop, the CPython bytecode overhead returns. Numba eliminates this overhead by compiling the sequential loop itself into raw C."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Science (Numba JIT) Completed.")
