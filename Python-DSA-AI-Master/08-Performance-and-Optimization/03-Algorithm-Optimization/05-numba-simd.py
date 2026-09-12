"""
Algorithm Optimization: Numba and JIT Compilation

Learning Objectives:
1. Understand Just-In-Time (JIT) compilation.
2. Use the `numba` library to compile Python math to native machine code.
3. Understand the `@jit(nopython=True)` decorator.
4. Compare native Python vs. Numba execution speed.

Concept Explanation:
Python is an interpreted language, which is inherently slower than compiled 
languages like C++ or Rust for numerical workloads. Numba is an open-source 
JIT compiler that translates a subset of Python and NumPy code into fast 
machine code at runtime using LLVM. This allows you to write Python `for` loops 
that run at C-like speeds without rewriting the logic in C.
"""

import time
import math
from typing import List

try:
    import numpy as np
    from numba import jit, njit
except ImportError:
    np = None
    jit = None
    print("Warning: Numba/NumPy not installed. Examples will be simulated.")

# --- Basic Implementation ---
def pure_python_monte_carlo_pi(nsamples: int) -> float:
    """Estimate Pi using Monte Carlo method in pure Python."""
    import random
    acc = 0
    for i in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

# --- Intermediate Implementation ---
# Define Numba compiled version if available
if jit is not None:
    @njit  # Equivalent to @jit(nopython=True)
    def numba_monte_carlo_pi(nsamples: int) -> float:
        import random
        acc = 0
        for i in range(nsamples):
            x = random.random()
            y = random.random()
            if (x ** 2 + y ** 2) < 1.0:
                acc += 1
        return 4.0 * acc / nsamples
else:
    def numba_monte_carlo_pi(nsamples: int) -> float:
        return pure_python_monte_carlo_pi(nsamples)

# --- Advanced Implementation / Performance Analysis ---
def compare_performance():
    if jit is None:
        return
        
    nsamples = 5_000_000
    print(f"Calculating Pi using {nsamples} samples...")
    
    # 1. Pure Python
    start = time.perf_counter()
    pi_py = pure_python_monte_carlo_pi(nsamples)
    t_py = time.perf_counter() - start
    print(f"Pure Python: {pi_py} | Time: {t_py:.4f}s")
    
    # 2. Numba (First run includes compilation time)
    start = time.perf_counter()
    pi_nb_compile = numba_monte_carlo_pi(nsamples)
    t_nb_compile = time.perf_counter() - start
    print(f"Numba (1st run w/ compile): {pi_nb_compile} | Time: {t_nb_compile:.4f}s")
    
    # 3. Numba (Second run is pure machine code)
    start = time.perf_counter()
    pi_nb = numba_monte_carlo_pi(nsamples)
    t_nb = time.perf_counter() - start
    print(f"Numba (2nd run): {pi_nb} | Time: {t_nb:.4f}s")
    
    print(f"Speedup vs Python: {t_py / t_nb:.1f}x")

# --- Edge Cases ---
def numba_edge_cases():
    """Numba 'nopython' mode fails if it encounters unsupported Python features."""
    if jit is None: return
    
    try:
        @njit
        def mixed_types_list():
            # Numba requires arrays/lists to be homogeneous types
            l = [1, 2.5, "string"] 
            return l
        # mixed_types_list() # This would throw a Numba typing error
    except Exception as e:
        print(f"Expected Error: {e}")

# --- Interview Challenge ---
"""
Challenge: Why is the first call to a Numba-decorated function slow?
Answer: The JIT compiler analyzes the argument types and compiles the LLVM 
IR down to machine code on the first invocation. Subsequent calls use the 
cached machine code.
"""

# --- Tests ---
def run_tests():
    if jit is not None:
        pi1 = pure_python_monte_carlo_pi(1000)
        pi2 = numba_monte_carlo_pi(1000)
        assert 2.5 < pi1 < 3.8
        assert 2.5 < pi2 < 3.8
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Numba JIT ---")
    compare_performance()
    run_tests()
