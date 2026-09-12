"""
Algorithm Optimization: Vectorization

Learning Objectives:
1. Understand the concept of Vectorization vs. Scalar loops.
2. Learn how Python's overhead slows down pure `for` loops.
3. Discover how libraries like NumPy perform operations in fast C code.
4. Apply broadcasting to apply operations across arrays.

Concept Explanation:
Vectorization replaces explicit loops with array operations. Instead of processing
a single element at a time (scalar), you apply the operation to an entire array
(vector) at once. NumPy executes these array operations in highly optimized, 
compiled C code, avoiding Python's interpreter overhead and often utilizing SIMD 
(Single Instruction, Multiple Data) CPU instructions.
"""

import time
import math
from typing import List

try:
    import numpy as np
except ImportError:
    np = None
    print("Warning: NumPy not installed. Advanced examples will be skipped.")

# --- Basic Implementation ---
def scalar_addition(a: List[float], b: List[float]) -> List[float]:
    """Naive element-wise addition using a pure Python loop."""
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result

def list_comp_addition(a: List[float], b: List[float]) -> List[float]:
    """Slightly faster list comprehension using zip."""
    return [x + y for x, y in zip(a, b)]

# --- Intermediate Implementation ---
def vectorized_addition(a, b):
    """Vectorized addition using NumPy (if available)."""
    if np is None:
        return []
    return a + b

# --- Advanced Implementation / Performance Analysis ---
def scalar_complex_math(arr: List[float]) -> List[float]:
    """Apply sin(x)^2 + cos(x)^2 to a list."""
    return [math.sin(x)**2 + math.cos(x)**2 for x in arr]

def vectorized_complex_math(arr):
    """Apply sin(x)^2 + cos(x)^2 to a numpy array."""
    if np is None:
        return []
    return np.sin(arr)**2 + np.cos(arr)**2

def compare_performance(size: int = 1_000_000):
    if np is None:
        return
        
    print(f"Comparing operations on array of size {size}...")
    
    # Data Setup
    py_list = list(range(size))
    np_arr = np.arange(size, dtype=np.float64)
    
    # 1. Simple Addition
    py_list_b = list(range(size))
    np_arr_b = np.arange(size, dtype=np.float64)
    
    start = time.perf_counter()
    scalar_addition(py_list, py_list_b)
    t_py_add = time.perf_counter() - start
    
    start = time.perf_counter()
    vectorized_addition(np_arr, np_arr_b)
    t_np_add = time.perf_counter() - start
    
    print(f"Addition -> Python: {t_py_add:.4f}s | NumPy: {t_np_add:.4f}s | Speedup: {t_py_add/t_np_add:.1f}x")
    
    # 2. Complex Math
    start = time.perf_counter()
    scalar_complex_math(py_list)
    t_py_math = time.perf_counter() - start
    
    start = time.perf_counter()
    vectorized_complex_math(np_arr)
    t_np_math = time.perf_counter() - start
    
    print(f"Math     -> Python: {t_py_math:.4f}s | NumPy: {t_np_math:.4f}s | Speedup: {t_py_math/t_np_math:.1f}x")

# --- Edge Cases ---
def memory_overhead_edge_case():
    """Vectorization can cause memory spikes if intermediate arrays are huge."""
    if np is None: return
    # a * b + c creates an intermediate array for (a * b) before adding c.
    # For massive arrays, use in-place operations like np.add(a, b, out=c)
    pass

# --- Interview Challenge ---
"""
Challenge: Given a 2D matrix (list of lists) representing an image, 
write a function to threshold it (values > 128 become 255, else 0).
Compare scalar vs numpy.
"""
def threshold_scalar(img: List[List[int]]) -> List[List[int]]:
    return [[255 if p > 128 else 0 for p in row] for row in img]

def threshold_vectorized(img):
    if np is None: return []
    return np.where(img > 128, 255, 0)

# --- Tests ---
def run_tests():
    a = [1, 2, 3]
    b = [4, 5, 6]
    assert scalar_addition(a, b) == [5, 7, 9]
    assert list_comp_addition(a, b) == [5, 7, 9]
    
    if np is not None:
        an = np.array(a)
        bn = np.array(b)
        assert np.array_equal(vectorized_addition(an, bn), np.array([5, 7, 9]))
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Vectorization ---")
    compare_performance()
    run_tests()
