"""
# ==============================================================================
# LABORATORY: NUMPY ARCHITECTURE (VECTORIZATION & BROADCASTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python is too slow for Data Science. A standard Python `list` is not an array 
# of numbers; it is an array of memory pointers pointing to scattered `PyObject` 
# instances in RAM. Looping through a Python list causes catastrophic CPU Cache misses.
#
# NumPy provides the `ndarray` (N-Dimensional Array).
# An `ndarray` is a single, unbroken, strictly contiguous block of raw $C$ memory.
# It forces Homogeneity (every element must be the exact same type, e.g., float64).
# 
# Because the memory is contiguous, the CPU can pre-fetch it perfectly. Because 
# the types are locked, NumPy completely bypasses the Python interpreter and hands 
# the math directly to $C$-compiled BLAS libraries, utilizing hardware SIMD 
# (Single Instruction, Multiple Data) to compute 8 math operations per clock cycle!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Prove the extreme speed of Vectorization over Python `for` loops.
# - Understand NumPy Slicing Memory Views (zero-copy operations).
# - Master Broadcasting rules (scaling dimensions without using RAM).
#
# ==============================================================================
"""

import numpy as np
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. VECTORIZATION VS PYTHON LOOPS
# ==============================================================================
def demonstrate_vectorization():
    section_header("The Speed of Vectorization")
    
    # Let's create an array of 10 Million numbers.
    n = 10_000_000
    print(f"Allocating {n:,} numbers in RAM...")
    
    # Python List
    py_list_A = list(range(n))
    py_list_B = list(range(n))
    
    # NumPy Arrays
    np_array_A = np.arange(n, dtype=np.int64)
    np_array_B = np.arange(n, dtype=np.int64)
    
    # 1. THE PYTHON WAY (Agonizingly Slow)
    start = time.perf_counter()
    py_result = [a + b for a, b in zip(py_list_A, py_list_B)]
    py_time = time.perf_counter() - start
    
    # 2. THE NUMPY WAY (Vectorized C Math)
    start = time.perf_counter()
    # There is no loop! We just add the arrays directly.
    np_result = np_array_A + np_array_B
    np_time = time.perf_counter() - start
    
    print(f"\nPython List Comprehension: {py_time:.4f} seconds")
    print(f"NumPy Vectorized Addition: {np_time:.4f} seconds")
    print(f"\nSPEEDUP: NumPy was {py_time / np_time:.0f}x faster!")


# ==============================================================================
# 4. SLICING AND MEMORY VIEWS
# ==============================================================================
def demonstrate_views():
    section_header("Memory Views (Zero-Copy Operations)")
    
    # In pure Python, slicing a list creates a brand new physical copy in RAM.
    # py_list = [1, 2, 3]
    # sub_list = py_list[1:] (This allocates new memory)
    
    # NumPy datasets are massive (Gigabytes). If slicing copied the data, your 
    # computer would instantly crash with OutOfMemory errors.
    # Therefore, NumPy slicing returns a "VIEW". It is literally looking at the 
    # exact same physical C memory, just changing the pointer offsets!
    
    arr = np.array([10, 20, 30, 40, 50])
    print(f"Original Array: {arr}")
    
    # Create a slice (a View)
    view = arr[1:4] # [20, 30, 40]
    print(f"View Array    : {view}")
    
    # If we mutate the View, it MUTATES THE ORIGINAL ARRAY!
    view[0] = 999
    
    print("\n[MUTATING THE VIEW... view[0] = 999]")
    print(f"View Array    : {view}")
    print(f"Original Array: {arr} <-- It changed!")
    
    # If you explicitly WANT a deep physical copy in RAM, you must call `.copy()`
    safe_copy = arr[1:4].copy()


# ==============================================================================
# 5. BROADCASTING RULES
# ==============================================================================
def demonstrate_broadcasting():
    section_header("NumPy Broadcasting (Virtual Memory)")
    
    # Broadcasting allows NumPy to perform math on matrices of DIFFERENT shapes 
    # without allocating any extra memory!
    
    # A 3x3 Matrix
    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    
    # A 1D Vector of 3 elements
    vector = np.array([10, 100, 1000])
    
    print("Matrix (3x3):")
    print(matrix)
    print("\nVector (3):")
    print(vector)
    
    # We want to add the vector to EVERY ROW of the matrix.
    # The naive way is to physically allocate a new 3x3 matrix where the vector 
    # is duplicated 3 times in RAM.
    # NumPy Broadcasting does this VIRTUALLY during the C-loop!
    
    result = matrix + vector
    
    print("\nResult (Matrix + Vector):")
    print(result)
    
    # Rule: Dimensions are checked right-to-left. They must either be exactly 
    # equal, or one of them must be exactly 1!
    print("\nMath executed perfectly with zero memory duplication overhead.")


def run_all_labs():
    demonstrate_vectorization()
    demonstrate_views()
    demonstrate_broadcasting()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a NumPy array completely destroy a Python `list` in mathematical performance?
   Answer: A Python `list` is a fragmented array of pointers. When you loop through it, the CPU must fetch the pointer, follow it to a random location in RAM, read the `PyObject` header, dynamically check if the object is an integer or float, and finally perform the math. This causes massive CPU Cache misses. A NumPy `ndarray` is a single, contiguous slab of raw C memory containing homogeneous types (e.g., exclusively 64-bit integers). The CPU pre-fetches the entire block perfectly into L1 Cache, skips all dynamic type-checking, and executes the math using SIMD hardware vectorization (processing multiple numbers per clock cycle).

2. You slice a 10 GB NumPy array to extract the last column: `col = matrix[:, -1]`. How much RAM did this consume, and why?
   Answer: Exactly 0 bytes! NumPy slicing does NOT copy physical data. It returns a "View". A View simply creates a tiny metadata object containing new pointer "Strides" that dictate how to read the original contiguous block of memory. Modifying the `col` variable will instantly mutate the original 10 GB matrix! If you specifically want to protect the original data, you must force a physical RAM allocation by calling `.copy()`.

3. What are the rules of NumPy Broadcasting?
   Answer: Broadcasting allows mathematical operations between arrays of mismatched shapes without allocating extra memory. NumPy aligns the shapes of the two arrays starting from the right-most dimension (trailing dimension). Two dimensions are compatible ONLY if:
   a) They are exactly equal.
   b) One of them is exactly `1` (NumPy will mathematically "stretch" the `1` dimension to match the other dimension virtually during C execution).
   If they don't match, NumPy throws a `ValueError`.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NumPy Basics Completed.")
