# 05-par-sci.py
"""
Parallel Scientific Computing Basics

Scientific computations often involve heavy math on large arrays.
While NumPy is fast, sometimes you need explicit parallelism or JIT compilation
for custom algorithms. This script demonstrates using Numba to speed up
a numerical algorithm.

Topics Covered:
1. Python loops (slow).
2. Just-In-Time (JIT) compilation using `numba` (fast).

Prerequisites:
    pip install numpy numba
"""

import numpy as np
import time

# Try to import numba, gracefully fallback if not installed
try:
    from numba import jit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

def mandelbrot_kernel(c, max_iter):
    """Calculates the number of iterations before divergence for a single complex number."""
    z = 0.0j
    for i in range(max_iter):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i
    return max_iter

def compute_mandelbrot_python(c_array, max_iter):
    """Computes the Mandelbrot set using pure Python loops."""
    rows, cols = c_array.shape
    result = np.zeros((rows, cols), dtype=np.int32)
    for i in range(rows):
        for j in range(cols):
            result[i, j] = mandelbrot_kernel(c_array[i, j], max_iter)
    return result

if HAS_NUMBA:
    # Compile the kernel function
    mandelbrot_kernel_jit = jit(nopython=True)(mandelbrot_kernel)
    
    @jit(nopython=True)
    def compute_mandelbrot_numba(c_array, max_iter):
        """Computes the Mandelbrot set using Numba JIT compilation."""
        rows, cols = c_array.shape
        result = np.zeros((rows, cols), dtype=np.int32)
        for i in range(rows):
            for j in range(cols):
                result[i, j] = mandelbrot_kernel_jit(c_array[i, j], max_iter)
        return result

def main():
    print("Parallel Scientific Computing: Numba JIT Example\n")
    
    # Setup the complex plane
    width, height = 500, 500
    x = np.linspace(-2.0, 1.0, width)
    y = np.linspace(-1.5, 1.5, height)
    X, Y = np.meshgrid(x, y)
    c_array = X + 1j * Y
    max_iter = 100
    
    print(f"Computing Mandelbrot set for a {width}x{height} grid...")
    
    # Benchmark Python
    start = time.time()
    res_py = compute_mandelbrot_python(c_array, max_iter)
    py_time = time.time() - start
    print(f"Pure Python Time: {py_time:.4f} seconds")
    
    # Benchmark Numba if available
    if HAS_NUMBA:
        # First run includes compilation time
        _ = compute_mandelbrot_numba(c_array, max_iter)
        
        start = time.time()
        res_numba = compute_mandelbrot_numba(c_array, max_iter)
        numba_time = time.time() - start
        
        print(f"Numba JIT Time:   {numba_time:.4f} seconds")
        print(f"Speedup:          {py_time / numba_time:.2f}x")
    else:
        print("\nNumba is not installed. To see the speedup, run: pip install numba")

if __name__ == "__main__":
    main()
