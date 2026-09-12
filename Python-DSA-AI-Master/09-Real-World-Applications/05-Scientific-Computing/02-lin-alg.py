"""
Linear Algebra in Python

===============================================================================
Learning Objectives:
1. Understand the core concepts of Linear Algebra: Vectors, Matrices, Operations.
2. Implement basic matrix operations from scratch to grasp the underlying mechanics.
3. Learn how to use Python's premier scientific computing library, `numpy`, for efficient linear algebra.
4. Solve systems of linear equations using matrix algebra.

Concept Explanation:
Linear Algebra is the branch of mathematics concerning linear equations, linear functions,
and their representations in vector spaces and through matrices. It is the mathematical
foundation of nearly all modern scientific computing and machine learning algorithms.

Key Concepts:
- **Vectors**: Mathematical quantities with both magnitude and direction, often represented as 1D arrays.
- **Matrices**: 2D arrays of numbers. Matrices represent linear transformations.
- **Dot Product / Matrix Multiplication**: The core operation for combining vectors and matrices.
- **Determinant & Inverse**: Properties of square matrices. The inverse of matrix A (A^-1) allows solving Ax = b as x = A^-1 * b.
- **Eigenvalues & Eigenvectors**: Special vectors that only scale (do not rotate) when a specific matrix transformation is applied.

Performance Considerations:
While implementing matrix operations in pure Python using nested lists is an excellent learning exercise,
it is extremely slow for large matrices (O(N^3) for naive multiplication).
In practice, ALWAYS use `numpy`. Numpy delegates these heavy operations to highly optimized,
compiled C/Fortran libraries (like BLAS and LAPACK) that utilize CPU vectorization (SIMD) and caching.

Industry Use Cases:
- Deep Learning (neural network weights, forward/backward propagation).
- Recommender Systems (Matrix Factorization, Singular Value Decomposition).
- Computer Graphics (Translations, Rotations, Projections).
===============================================================================
"""

import math
from typing import List

# Type aliases for clarity
Vector = List[float]
Matrix = List[List[float]]

# =============================================================================
# 1. Pure Python Implementation (Educational Purpose)
# =============================================================================

def dot_product(v1: Vector, v2: Vector) -> float:
    """Computes the dot product of two vectors."""
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length.")
    return sum(x * y for x, y in zip(v1, v2))

def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Multiplies matrix A (m x n) by matrix B (n x p) to return matrix C (m x p).
    Naive O(m * n * p) implementation.
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Inner dimensions must match (cols_A == rows_B).")
        
    # Initialize the result matrix with zeros
    C = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    # Compute the matrix product
    for i in range(rows_A):
        for j in range(cols_B):
            # C[i][j] is the dot product of the i-th row of A and the j-th col of B
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
                
    return C

def transpose(M: Matrix) -> Matrix:
    """Returns the transpose of a matrix."""
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


# =============================================================================
# 2. Professional Implementation using NumPy (Industry Standard)
# =============================================================================
try:
    import numpy as np
except ImportError:
    print("WARNING: numpy is not installed. Professional examples will not run.")
    np = None

def numpy_examples() -> None:
    """Demonstrates efficient linear algebra using numpy."""
    if np is None: return
    
    print("\n--- NumPy Linear Algebra Examples ---")
    
    # Define matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # 1. Matrix Multiplication (Dot Product)
    C = np.dot(A, B)
    # Alternatively: C = A @ B  (Python 3.5+)
    print(f"Matrix A @ B:\n{C}")
    
    # 2. Solving a system of linear equations: Ax = b
    # 1x + 2y = 5
    # 3x + 4y = 11
    b = np.array([5, 11])
    x = np.linalg.solve(A, b)
    print(f"Solution for Ax = b: x = {x}")
    
    # Verify: A * x should equal b
    assert np.allclose(np.dot(A, x), b), "Solution is incorrect!"
    
    # 3. Eigenvalues and Eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"Eigenvalues of A: {eigenvalues}")
    
    # 4. Matrix Inverse
    A_inv = np.linalg.inv(A)
    print(f"Inverse of A:\n{A_inv}")
    # A @ A_inv should be the identity matrix (with small floating point errors)
    identity = np.dot(A, A_inv)
    print(f"A @ A_inv (Identity):\n{np.round(identity)}")


# =============================================================================
# Main Execution and Tests
# =============================================================================

if __name__ == "__main__":
    print("--- Pure Python Linear Algebra ---")
    
    # Test dot product
    v1 = [1, 2, 3]
    v2 = [4, 5, 6]
    dp = dot_product(v1, v2)
    print(f"Dot product of {v1} and {v2}: {dp}")
    assert dp == 32 # (1*4 + 2*5 + 3*6)
    
    # Test matrix multiplication
    A = [
        [1, 2],
        [3, 4]
    ]
    B = [
        [2, 0],
        [1, 2]
    ]
    
    C = matrix_multiply(A, B)
    print("Matrix Multiplication result:")
    for row in C:
        print(row)
        
    expected_C = [[4, 4], [10, 8]]
    assert C == expected_C, "Matrix multiplication failed!"
    
    # Test transpose
    T = transpose(A)
    print("Transpose of A:")
    for row in T:
        print(row)
    assert T == [[1, 3], [2, 4]], "Transpose failed!"
    
    print("\nPure Python tests passed successfully!")
    
    # Run Numpy examples if available
    numpy_examples()

"""
===============================================================================
Interview Challenge:
Matrix operations are easily parallelizable. The naive matrix multiplication
we implemented is O(N^3). 

1. Can you explain Strassen's Algorithm and its time complexity compared to the 
   naive approach?
2. If you were forced to optimize the pure Python `matrix_multiply` function 
   without using external libraries like NumPy, what strategies would you use?
   (Hint: consider list comprehensions, avoiding repetitive len() calls, and 
   possibly using flat lists / 1D arrays for cache locality).
===============================================================================
"""
