"""
Module: 03-numba-jit-math
Description: Comprehensive educational module exploring Numba's Just-In-Time (JIT)
compilation for accelerating mathematical and scientific computing in Python.

Learning Objectives:
1. Understand Just-In-Time (JIT) compilation and how Numba transforms Python bytecode to machine code.
2. Differentiate between `@jit(nopython=True)` (or `@njit`) and object mode.
3. Master advanced Numba features like `fastmath`, `parallel=True`, and `prange`.
4. Analyze the performance tradeoffs (Time/Space Complexity, compilation overhead).
5. Implement real-world algorithms (e.g., Monte Carlo Pi estimation, Mandelbrot) with Numba.

Theory & Mathematical Background:
Python is an interpreted language, which introduces significant overhead for mathematical
loops and tight computations (due to dynamic typing, GIL, and object unboxing).
Numba parses Python bytecode, uses type inference to determine data types, and utilizes 
the LLVM compiler infrastructure to generate highly optimized native machine code.

- **JIT vs AOT**: Numba is JIT (compiles at runtime on first execution) whereas C/C++ is AOT.
- **Fastmath**: Enabling `fastmath=True` allows the compiler to make aggressive math
  optimizations that might violate strict IEEE-754 compliance (e.g., reordering operations,
  assuming no NaNs) but yield substantial speedups.
- **Parallelism**: Numba can automatically thread loops using OpenMP or TBB via `prange`.

Big-O Analysis:
- Time Complexity: Algorithmic complexity remains the same, but the constant factor $C$ 
  in $O(N)$ is drastically reduced (often by 10x-100x, approaching C-like speeds).
- Space Complexity: Identical to NumPy implementations, usually $O(N)$ or $O(1)$ for 
  in-place operations. Numba requires a slight memory overhead for LLVM compilation at runtime.
"""

import math
import time
from typing import Callable

import numpy as np
import numba
from numba import njit, prange

# ============================================================================
# 1. BASIC USAGE: Pure Python vs NumPy vs Numba
# ============================================================================

def py_sum_squares(n: int) -> float:
    """
    Pure Python implementation of sum of squares.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    total = 0.0
    for i in range(n):
        total += i * i
    return total

def np_sum_squares(n: int) -> float:
    """
    NumPy implementation of sum of squares.
    Time Complexity: O(N)
    Space Complexity: O(N) - creates an array of size N in memory
    """
    return np.sum(np.arange(n, dtype=np.float64) ** 2)

@njit
def nb_sum_squares(n: int) -> float:
    """
    Numba JIT-compiled implementation of sum of squares.
    @njit is an alias for @jit(nopython=True).
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    total = 0.0
    for i in range(n):
        total += i * i
    return total


# ============================================================================
# 2. INTERMEDIATE USAGE: Fastmath and NumPy Array Operations
# ============================================================================

# Generating some dummy data for complex math operations
DATA_SIZE = 1_000_000
array_a = np.random.rand(DATA_SIZE).astype(np.float32)
array_b = np.random.rand(DATA_SIZE).astype(np.float32)

@njit
def euclidean_distance_nb(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates Euclidean distance without fastmath.
    """
    dist = 0.0
    for i in range(x.shape[0]):
        dist += (x[i] - y[i]) ** 2
    return math.sqrt(dist)

@njit(fastmath=True)
def euclidean_distance_fastmath(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates Euclidean distance with fastmath=True.
    By relaxing strict IEEE 754 precision, LLVM can vectorize this loop (SIMD).
    """
    dist = 0.0
    for i in range(x.shape[0]):
        dist += (x[i] - y[i]) ** 2
    return math.sqrt(dist)


# ============================================================================
# 3. ADVANCED USAGE: Parallelization with Numba prange
# ============================================================================

@njit(parallel=True, fastmath=True)
def monte_carlo_pi_parallel(n_samples: int) -> float:
    """
    Estimates Pi using the Monte Carlo method.
    parallel=True and prange allows Numba to distribute the loop across multiple CPU cores.
    
    Mathematical intuition:
    Area of circle = pi * r^2. Area of square = (2r)^2 = 4r^2.
    Ratio = pi / 4. 
    By generating random points (x, y) in [0, 1]x[0, 1], the probability that 
    x^2 + y^2 <= 1 is pi / 4.
    """
    inside_circle = 0
    # prange instructs Numba to run this loop in parallel
    for _ in prange(n_samples):
        x = np.random.random()
        y = np.random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
            
    return (inside_circle / n_samples) * 4.0


# ============================================================================
# 4. PERFORMANCE & EDGE CASES ANALYSIS
# ============================================================================

def benchmark(func: Callable, *args, iterations: int = 5, name: str = "") -> float:
    """
    Benchmarking helper function.
    Executes a function multiple times and returns the average execution time.
    NOTE: Numba functions compile on the first run, so we do a warm-up call.
    """
    # Warm-up (compilation phase for Numba)
    _ = func(*args)
    
    start = time.perf_counter()
    for _ in range(iterations):
        _ = func(*args)
    end = time.perf_counter()
    
    avg_time = (end - start) / iterations
    print(f"{name: <30} | Avg Time: {avg_time:.6f} sec")
    return avg_time

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases.
    """
    print("\n--- Performance Analysis & Edge Cases ---")
    print("1. Compilation Overhead: Numba compiles on the FIRST call.")
    print("   If a script only runs briefly, compilation time might exceed execution time savings.")
    print("2. Unsupported Python Features: Numba nopython mode does not support dictionaries (except typed dicts),")
    print("   mixed-type lists, or string manipulations easily. Stick to numeric types and NumPy arrays.")
    print("3. Memory Allocation: Creating NumPy arrays inside Numba loops can slow down performance.")
    print("   Preallocate arrays in Python and pass them as arguments.")
    print("4. fastmath=True: Use with caution. It assumes no NaN or Inf values. If present, behavior is undefined.")


# ============================================================================
# 5. INTERVIEW CHALLENGE: The Mandelbrot Set (Fractal generation)
# ============================================================================

@njit(parallel=True, fastmath=True)
def mandelbrot_numba(width: int, height: int, max_iter: int) -> np.ndarray:
    """
    Generates a Mandelbrot fractal image (2D array).
    Formula: z_{n+1} = z_n^2 + c
    If |z| > 2, it diverges.
    
    This is computationally heavy and perfect for Numba parallelization.
    """
    image = np.zeros((height, width), dtype=np.int32)
    
    # Map pixel coordinates to complex plane
    # Real axis [-2.0, 1.0], Imaginary axis [-1.5, 1.5]
    real_min, real_max = -2.0, 1.0
    imag_min, imag_max = -1.5, 1.5
    
    for row in prange(height):
        for col in range(width):
            c_real = real_min + (col / width) * (real_max - real_min)
            c_imag = imag_min + (row / height) * (imag_max - imag_min)
            
            z_real = 0.0
            z_imag = 0.0
            
            # Iteration to determine divergence
            for i in range(max_iter):
                # z^2 = (x + iy)^2 = x^2 - y^2 + i(2xy)
                z_real_next = z_real*z_real - z_imag*z_imag + c_real
                z_imag_next = 2.0 * z_real * z_imag + c_imag
                
                z_real = z_real_next
                z_imag = z_imag_next
                
                if z_real*z_real + z_imag*z_imag > 4.0:
                    image[row, col] = i
                    break
            else:
                image[row, col] = max_iter
                
    return image


def run_tests() -> None:
    """
    Simple test suite to validate implementations.
    """
    print("\n--- Running Tests ---")
    
    # 1. Test sum of squares
    py_res = py_sum_squares(100)
    nb_res = nb_sum_squares(100)
    assert math.isclose(py_res, nb_res), f"Sum of squares mismatch: {py_res} != {nb_res}"
    
    # 2. Test Euclidean distance
    x = np.array([0.0, 0.0], dtype=np.float32)
    y = np.array([3.0, 4.0], dtype=np.float32)
    dist = euclidean_distance_fastmath(x, y)
    assert math.isclose(dist, 5.0), f"Euclidean distance failed: {dist} != 5.0"
    
    # 3. Test Monte Carlo Pi
    pi_estimate = monte_carlo_pi_parallel(10_000)
    # Pi should be roughly ~3.14 (allowing wide margin due to randomness)
    assert 2.9 < pi_estimate < 3.4, f"Pi estimation way off: {pi_estimate}"
    
    print("All mathematical validation tests passed successfully!")


if __name__ == "__main__":
    print(f"{'='*60}")
    print(f"========== Exploring NUMBA JIT MATH ==========")
    print(f"{'='*60}\n")
    
    # 1. Basic Iteration Benchmarks
    print("1. Benchmarking Sum of Squares (N = 10,000,000):")
    n_val = 10_000_000
    benchmark(py_sum_squares, n_val, name="Pure Python Sum")
    benchmark(np_sum_squares, n_val, name="NumPy Vectorized Sum")
    benchmark(nb_sum_squares, n_val, name="Numba JIT Sum")
    
    # 2. Math Intensive Benchmarks (Distance)
    print("\n2. Benchmarking Euclidean Distance (N = 1,000,000):")
    benchmark(euclidean_distance_nb, array_a, array_b, name="Numba @njit Distance")
    benchmark(euclidean_distance_fastmath, array_a, array_b, name="Numba @njit(fastmath) Distance")
    
    # 3. Parallel Pi Estimation
    print("\n3. Benchmarking Monte Carlo Pi Estimation:")
    samples = 10_000_000
    pi_val = monte_carlo_pi_parallel(samples) # Warmup and compute
    print(f"Estimated Pi (N={samples}): {pi_val}")
    benchmark(monte_carlo_pi_parallel, samples, name="Numba Parallel Pi (10M)")
    
    # 4. Mandelbrot Set (Heavy computation)
    print("\n4. Generating Mandelbrot Set (1024x1024, 100 max_iter):")
    m_img = mandelbrot_numba(1024, 1024, 100) # Warmup
    benchmark(mandelbrot_numba, 1024, 1024, 100, name="Numba Mandelbrot Generation")
    print(f"Mandelbrot Array Shape: {m_img.shape}, Max Iterations Found: {np.max(m_img)}")
    
    # 5. Performance and Edge Cases
    analyze_performance_and_edge_cases()
    
    # 6. Tests
    run_tests()
    
    print(f"\n{'='*60}")
    print(f"========== END OF NUMBA JIT MATH ==========")
    print(f"{'='*60}\n")
