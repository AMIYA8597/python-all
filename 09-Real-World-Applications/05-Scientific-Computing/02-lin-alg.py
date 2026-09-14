"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (LINEAR ALGEBRA & NUMPY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A graphics engineer needs to rotate a 3D model containing 50,000 vertices. 
# They write a triple-nested Python `for` loop to multiply the X,Y,Z coordinates 
# by the Sin/Cos rotation matrix. It takes 1.5 seconds. At 60 Frames Per Second, 
# this mathematical operation must complete in 0.016 seconds. The game stutters 
# violently and crashes.
#
# A senior mathematical engineer understands "Matrix Vectorization". They import 
# `NumPy`. They structure the 50,000 vertices as a single C-level memory block 
# (a Matrix). They execute `np.dot(vertices, rotation_matrix)`. NumPy mathematically 
# offloads the multiplication to the CPU's hardware SIMD registers (or a GPU Tensor 
# Core) using the BLAS/LAPACK Fortran libraries. The rotation completes in 0.002 
# seconds, rendering 500 Frames Per Second flawlessly.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical architecture of N-Dimensional Arrays (Tensors).
# - Execute Matrix Dot Products (The foundation of Neural Networks).
# - Execute algorithmic systems of linear equations using `scipy.linalg`.
#
# ==============================================================================
"""

import timeit
import random

# Gracefully handle missing NumPy/SciPy dependencies
try:
    import numpy as np
    from scipy import linalg
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATRIX MULTIPLICATION (THE DOT PRODUCT)
# ==============================================================================
# A Dot Product is the fundamental mathematical operation behind Artificial 
# Neural Networks, 3D Graphics Rendering, and Quantum Computing simulations.

def demonstrate_matrix_dot_product():
    section_header("Mathematical Vectorization: Matrix Dot Products")
    
    if not HAS_NUMPY:
        print("  [ERROR] NumPy is not installed. Run `pip install numpy scipy`.")
        return
        
    print("  [SCENARIO] Multiplying a massive Neural Network Weight Matrix against an Input Vector.")
    
    # 1. We construct a 1000x1000 Matrix (e.g., 1 million Neural Network Weights!)
    MATRIX_SIZE = 1000
    print(f"  [INIT] Generating a {MATRIX_SIZE}x{MATRIX_SIZE} C-level Matrix in RAM...")
    
    # NumPy generates this instantly in C!
    weights = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
    
    # We construct the 1000x1 Input Vector
    inputs = np.random.rand(MATRIX_SIZE)
    
    
    # --- A: NAIVE PYTHON LOOP ---
    print("\n  [SCENARIO A: PURE PYTHON `FOR` LOOP]")
    # We must manually convert the NumPy arrays to Python Lists to simulate 
    # the terrible performance of raw Python bytecode!
    py_weights = weights.tolist()
    py_inputs = inputs.tolist()
    
    start_py = timeit.default_timer()
    py_result = [0.0] * MATRIX_SIZE
    
    # The mathematical O(N^2) Dot Product logic!
    for row_idx in range(MATRIX_SIZE):
        row_sum = 0.0
        for col_idx in range(MATRIX_SIZE):
            row_sum += py_weights[row_idx][col_idx] * py_inputs[col_idx]
        py_result[row_idx] = row_sum
        
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Execution Time: {time_py:.4f} seconds")
    
    
    # --- B: NUMPY BLAS ACCELERATION ---
    print("\n  [SCENARIO B: NUMPY MATRIX DOT PRODUCT (np.dot)]")
    start_np = timeit.default_timer()
    
    # This single line executes the exact same O(N^2) logic, but entirely in 
    # C/Fortran using CPU-level SIMD instructions!
    np_result = np.dot(weights, inputs)
    
    end_np = timeit.default_timer()
    time_np = end_np - start_np
    print(f"    -> Execution Time: {time_np:.6f} seconds")
    
    
    speedup = time_py / time_np
    print(f"\n  [CONCLUSION] NumPy achieved an astronomical {speedup:.1f}x hardware speedup!")
    print("  The CPython Interpreter is mathematically incapable of processing Deep Learning.")


# ==============================================================================
# 4. SOLVING SYSTEMS OF LINEAR EQUATIONS
# ==============================================================================
# Scenario: A Quantitative Trading algorithm needs to solve this system of equations:
# 3x + 2y - z  = 1
# 2x - 2y + 4z = -2
# -x + 0.5y - z = 0
# We must find the exact mathematical values for x, y, and z!

def demonstrate_linear_systems():
    section_header("Mathematical Solvers: Systems of Linear Equations")
    
    if not HAS_NUMPY:
        return
        
    print("  [SCENARIO] Solving a 3-Variable Mathematical System (x, y, z).")
    
    # 1. We abstract the Equations into a Coefficient Matrix (A)
    # 3x  + 2y   - 1z
    # 2x  - 2y   + 4z
    # -1x + 0.5y - 1z
    A = np.array([
        [ 3.0,  2.0, -1.0],
        [ 2.0, -2.0,  4.0],
        [-1.0,  0.5, -1.0]
    ])
    
    # 2. We abstract the Constants into a Vector (B)
    B = np.array([1.0, -2.0, 0.0])
    
    print("\n  [EXECUTION: SCIPY LINALG.SOLVE]")
    print("    -> Mathematically executing A * X = B...")
    
    # We use the highly optimized LAPACK Fortran routine to mathematically 
    # calculate the Inverted Matrix (A^-1) and execute the Dot Product!
    X = linalg.solve(A, B)
    
    print("\n  [RESULT: THE EXACT MATHEMATICAL SOLUTION]")
    print(f"    -> x = {X[0]:.2f}")
    print(f"    -> y = {X[1]:.2f}")
    print(f"    -> z = {X[2]:.2f}")
    
    # We prove it works by plugging the answers back into the Matrix!
    # np.dot(A, X) MUST equal B!
    validation = np.dot(A, X)
    
    print("\n  [INTEGRITY CHECK]")
    print(f"    -> Expected B Vector: {B}")
    print(f"    -> Calculated B:      {validation}")
    
    # We use np.allclose because of IEEE 754 float drifting!
    if np.allclose(validation, B):
        print("    -> PASS: Mathematical integrity is absolute.")
    else:
        print("    -> FAIL: Precision error detected.")


def run_all_labs():
    demonstrate_matrix_dot_product()
    demonstrate_linear_systems()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is a `numpy.array` exponentially faster than a standard Python `list` when multiplying 1,000,000 numbers?"
   Senior Answer: "Architectural Memory Layout. A standard Python `list` is an array of C-pointers. If you have 1,000,000 integers in a Python list, the CPU must jump to 1,000,000 completely random locations in RAM to find the actual integer objects, causing catastrophic Cache Misses and destroying execution speed. A `numpy.array` is a mathematically contiguous block of raw C-memory. The 1,000,000 integers are physically packed side-by-side on the silicon. When the CPU processes the NumPy array, it mathematically streams the data sequentially through the L1 Cache. Furthermore, because NumPy guarantees uniformity (all elements are 64-bit floats), it can trigger SIMD (Single Instruction, Multiple Data) CPU registers, processing 4 or 8 floats in a single clock cycle, completely bypassing Python's bytecode overhead."

2. Interviewer: "Under the hood, what is `np.dot` physically invoking when you multiply two massive matrices?"
   Senior Answer: "`np.dot` does not execute custom Python or C code written by the NumPy developers. It acts as an architectural wrapper that dynamically links to an underlying BLAS (Basic Linear Algebra Subprograms) library installed on the OS (such as Intel MKL, OpenBLAS, or Apple Accelerate). These BLAS libraries are written in Fortran and highly optimized C. They are physically tuned to the specific micro-architecture of the host CPU (e.g., using AVX-512 instructions on Intel processors). By delegating the operation to BLAS, NumPy mathematically guarantees that the matrix multiplication runs at the absolute theoretical limit of the host hardware."

3. Interviewer: "When solving $Ax = B$, why should you use `scipy.linalg.solve(A, B)` instead of manually calculating the inverse matrix with `np.linalg.inv(A) * B`?"
   Senior Answer: "Numerical Instability and Float Catastrophes. Mathematically, $x = A^{-1}B$ is correct. However, physically calculating the Inverse Matrix ($A^{-1}$) in a computer is one of the most computationally expensive and numerically unstable operations in Computer Science. Due to IEEE 754 Floating Point limitations, inverting a matrix often introduces massive, cascading precision errors (especially if the matrix is 'ill-conditioned' or near-singular). The function `scipy.linalg.solve` intelligently avoids calculating the full inverse. It utilizes advanced matrix decompositions (like LU Decomposition or Cholesky Decomposition via LAPACK), mathematically solving for $x$ directly. This is significantly faster, requires far less RAM, and is mathematically immune to the catastrophic float drifting caused by manual inversion."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scientific Computing (Linear Algebra) Completed.")
