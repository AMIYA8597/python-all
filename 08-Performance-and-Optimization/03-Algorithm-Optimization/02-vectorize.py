"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (ALGORITHM VECTORIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python is universally regarded as a "slow" language because it executes `for` 
# loops at the bytecode level, dynamically Type-Checking and Object-Boxing every 
# single variable during every single iteration.
#
# Yet, the entire global Machine Learning and AI industry (TensorFlow, PyTorch, 
# Pandas) runs on Python! How? Vectorization.
#
# A junior engineer calculates the dot product of two arrays using a standard 
# `for` loop. The Python interpreter chokes, taking 500ms to process 1M elements.
#
# A senior engineer uses `numpy`. The exact same mathematical operation is pushed 
# down into compiled C and Fortran code, bypassing the Python interpreter entirely. 
# The CPU utilizes SIMD (Single Instruction, Multiple Data) to process blocks of 
# memory concurrently in hardware, dropping execution time to 2ms (a 250x speedup!).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master identifying Python bytecode overhead.
# - Master Vectorization with `numpy`.
# - Understand the architecture of hardware SIMD acceleration.
#
# ==============================================================================
"""

import timeit
import random
import math
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE NAIVE PYTHON LOOP (BYTECODE OVERHEAD)
# ==============================================================================
def python_dot_product(list_a: list, list_b: list) -> float:
    """
    Time Complexity: O(N)
    This is standard Python. During every iteration, CPython must:
    1. Look up the index `i`.
    2. Extract the PyObject pointers from both lists.
    3. Determine that both are floats (Dynamic Type Checking).
    4. Pass them to the C-level multiplication function.
    5. Allocate a BRAND NEW PyObject in RAM to store the result.
    6. Add the result to the accumulator.
    7. Destroy the temporary PyObject via Reference Counting.
    (This is an unfathomable amount of wasted CPU cycles!)
    """
    result = 0.0
    for i in range(len(list_a)):
        result += list_a[i] * list_b[i]
    return result


# ==============================================================================
# 4. MATHEMATICAL VECTORIZATION PROOF
# ==============================================================================
def demonstrate_vectorization():
    section_header("Performance Proof: Bytecode Loops vs SIMD Vectorization")
    
    if not HAS_NUMPY:
        print("  [ERROR] NumPy is not installed. Run `pip install numpy`.")
        return
        
    N = 5_000_000 # 5 Million Elements!
    print(f"  Generating {N:,} elements for testing...")
    
    # 1. Generate standard Python lists
    py_list_a = [random.random() for _ in range(N)]
    py_list_b = [random.random() for _ in range(N)]
    
    # 2. Generate optimized C-arrays (NumPy)
    np_array_a = np.array(py_list_a, dtype=np.float64)
    np_array_b = np.array(py_list_b, dtype=np.float64)
    
    print("\n  [NAIVE PYTHON LOOP]")
    start_py = timeit.default_timer()
    # The CPU suffers through millions of dynamic type checks!
    res_py = python_dot_product(py_list_a, py_list_b)
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Result: {res_py:.2f}")
    print(f"    -> Time:   {time_py:.4f} seconds")
    
    print("\n  [NUMPY VECTORIZATION (SIMD)]")
    start_np = timeit.default_timer()
    # The Python Interpreter does NOTHING! It simply hands the memory pointers 
    # to compiled C-code and waits for the hardware to finish!
    res_np = np.dot(np_array_a, np_array_b)
    end_np = timeit.default_timer()
    time_np = end_np - start_np
    print(f"    -> Result: {res_np:.2f}")
    print(f"    -> Time:   {time_np:.4f} seconds")
    
    # MATHEMATICAL PROOF
    speedup = time_py / time_np
    print(f"\n  [CONCLUSION] Vectorization bypassed the Python Interpreter, resulting in a {speedup:.1f}x speedup!")


# ==============================================================================
# 5. BROADCASTING (NO-LOOP ARCHITECTURE)
# ==============================================================================
def demonstrate_broadcasting():
    section_header("The Power of Broadcasting (Math without Loops)")
    
    if not HAS_NUMPY:
        return
        
    print("  [SCENARIO] We want to add +10 to every element in the array.")
    
    # Naive Python forces a List Comprehension (Bytecode Loop)
    py_list = [1, 2, 3, 4, 5]
    print(f"  Naive Python: {[x + 10 for x in py_list]}")
    
    # NumPy Broadcasting applies the scalar mathematically across the entire 
    # contiguous memory block in C without a Python loop!
    np_array = np.array([1, 2, 3, 4, 5])
    
    print(f"  NumPy Array:  {np_array + 10}")
    print("  (This executes at near bare-metal C speeds!)")


def run_all_labs():
    demonstrate_vectorization()
    demonstrate_broadcasting()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Python is so incredibly slow at executing mathematical `for` loops, how does it physically dominate the AI and Machine Learning ecosystem?"
   Senior Answer: "The Python that Data Scientists execute is effectively just an API wrapper for highly optimized C, C++, and Fortran binaries. When you invoke `np.dot()` or a PyTorch tensor multiplication, the Python interpreter immediately yields execution to compiled low-level libraries (like BLAS or LAPACK). The mathematically heavy loop executes entirely outside of the Python Virtual Machine, operating directly on contiguous blocks of RAM at near bare-metal speeds, completely bypassing Python's dynamic type-checking and GIL overhead."

2. Interviewer: "What is 'SIMD', and how does Vectorization leverage it mathematically?"
   Senior Answer: "SIMD stands for 'Single Instruction, Multiple Data'. In a standard Python loop, the CPU executes one mathematical instruction (e.g., 'multiply') on one piece of data, and then repeats. Modern CPUs contain advanced hardware registers (like AVX-512) that can hold multiple data points simultaneously. When we 'Vectorize' an algorithm using NumPy, the compiled C-code commands the CPU to execute a *single* multiplication instruction that simultaneously multiplies 4, 8, or 16 numbers in parallel at the absolute hardware level. This physically compresses execution time by an order of magnitude."

3. Interviewer: "If NumPy is so much faster, why does it actually run SLOWER than a standard Python loop if I only have an array of 5 elements?"
   Senior Answer: "Because of 'Crossing the C-API Boundary'. When you call a NumPy function from Python, the interpreter must physically package the command, convert Python objects into C-types, and hand execution over to the C runtime. This context switch has a fixed, non-zero microsecond overhead. If the mathematical work is microscopic (like adding 5 numbers), the time spent translating the request to C is vastly larger than the time it would have taken Python to just calculate it in bytecode! Vectorization only achieves exponential speedups when operating on massive arrays where the $O(1)$ C-API overhead is mathematically dwarfed by the $O(N)$ execution savings."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Algorithm Optimization (Vectorization) Completed.")
