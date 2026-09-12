"""
Module: 02-scipy-linear-algebra
Description: A textbook-grade, interactive masterclass on SciPy's Linear Algebra module (scipy.linalg).

=========================================================================================
                                SCI-PY LINEAR ALGEBRA
=========================================================================================

1. Introduction
---------------
The `scipy.linalg` module contains all the functions in `numpy.linalg`, plus some other
more advanced ones not contained in `numpy.linalg`. It is built on standard ATLAS, LAPACK,
and BLAS libraries, making it extremely fast.

2. Mathematical Background
--------------------------
Linear Algebra is the branch of mathematics concerning linear equations, linear functions,
and their representations in vector spaces and through matrices.

Key concepts covered here:
- Matrix Inversion and Determinants
- Solving Linear Systems (Ax = b)
- Matrix Decompositions (LU, QR, SVD, Cholesky)
- Eigenvalues and Eigenvectors
- Matrix Norms and Functions (e.g., matrix exponentials)

3. Big-O Complexity
-------------------
Most dense linear algebra operations fall into the O(N^3) time complexity class for N x N matrices.
- Matrix Multiplication: O(N^3) (naively, Strassen is O(N^2.81))
- LU Decomposition: O(N^3)
- Matrix Inversion: O(N^3)
- Singular Value Decomposition (SVD): O(N^3)
- Eigenvalue Decomposition: O(N^3)
Memory complexity for dense N x N matrices is O(N^2).
"""

import time
import numpy as np
import scipy.linalg as la
from typing import Tuple, List, Dict, Any

# =====================================================================
# 1. Basic Operations: Norms, Determinants, and Inverses
# =====================================================================

def basic_matrix_operations(matrix: np.ndarray) -> Dict[str, Any]:
    """
    Demonstrates basic matrix operations using scipy.linalg.
    
    Args:
        matrix: A square 2D numpy array.
        
    Returns:
        A dictionary containing the determinant, inverse, and Frobenius norm.
    """
    print("--- 1. Basic Matrix Operations ---")
    
    # 1. Determinant
    # Mathematically, the determinant is a scalar value that is a function of the 
    # entries of a square matrix. It characterizes some properties of the matrix and 
    # the linear map represented by the matrix.
    det = la.det(matrix)
    print(f"Matrix:\n{matrix}")
    print(f"Determinant: {det:.4f}")
    
    # 2. Inverse
    # The inverse of A is A^-1 such that A @ A^-1 = I (Identity matrix).
    # O(N^3) time complexity.
    try:
        inv = la.inv(matrix)
        print(f"Inverse:\n{inv}")
    except la.LinAlgError:
        print("Matrix is singular and cannot be inverted.")
        inv = None
        
    # 3. Norms
    # The norm is a function that assigns a strictly positive length or size to each 
    # vector in a vector space. For matrices, Frobenius norm is common.
    norm_frob = la.norm(matrix, ord='fro')
    print(f"Frobenius Norm: {norm_frob:.4f}\n")
    
    return {
        "determinant": det,
        "inverse": inv,
        "frobenius_norm": norm_frob
    }

# =====================================================================
# 2. Solving Linear Systems
# =====================================================================

def solve_linear_system(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Solves the linear equation system Ax = b.
    
    Using `scipy.linalg.solve` is faster and more numerically stable than 
    computing the inverse (x = A^-1 @ b). It uses LAPACK routines (typically 
    LU decomposition) under the hood.
    
    Time Complexity: O(N^3)
    
    Args:
        A: Coefficients matrix (N x N)
        b: Ordinate/dependent variable values (N x 1 or N)
        
    Returns:
        x: Solution vector.
    """
    print("--- 2. Solving Linear Systems (Ax = b) ---")
    print(f"A:\n{A}")
    print(f"b:\n{b}")
    
    x = la.solve(A, b)
    
    print(f"Solution x:\n{x}")
    # Verification: A @ x should be extremely close to b
    print(f"Verification (A @ x):\n{A @ x}\n")
    return x

# =====================================================================
# 3. Matrix Decompositions (LU, QR, SVD)
# =====================================================================

def matrix_decompositions(A: np.ndarray) -> None:
    """
    Demonstrates major matrix factorizations/decompositions.
    These are foundational algorithms for numerical linear algebra.
    """
    print("--- 3. Matrix Decompositions ---")
    
    # a. LU Decomposition
    # Factors a matrix as the product of a lower triangular matrix (L) and 
    # an upper triangular matrix (U). Often includes a permutation matrix (P) for numerical stability.
    # A = P @ L @ U
    P, L, U = la.lu(A)
    print("LU Decomposition (A = P @ L @ U):")
    print(f"P (Permutation):\n{P}")
    print(f"L (Lower Triangular):\n{L}")
    print(f"U (Upper Triangular):\n{U}")
    print(f"Reconstruction (P@L@U):\n{P @ L @ U}\n")
    
    # b. QR Decomposition
    # Factors a matrix into an orthogonal matrix (Q) and an upper triangular matrix (R).
    # A = Q @ R
    # Useful for solving least squares problems and eigenvalue algorithms.
    Q, R = la.qr(A)
    print("QR Decomposition (A = Q @ R):")
    print(f"Q (Orthogonal):\n{Q}")
    print(f"R (Upper Triangular):\n{R}\n")
    
    # c. Singular Value Decomposition (SVD)
    # Generalizes eigendecomposition to non-square matrices.
    # A = U @ Sigma @ V^H
    U_svd, s, Vh = la.svd(A)
    print("Singular Value Decomposition (A = U @ Sigma @ V^H):")
    print(f"Singular values (s): {s}\n")

# =====================================================================
# 4. Eigenvalues and Eigenvectors
# =====================================================================

def eigen_problems(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes eigenvalues and eigenvectors for a square matrix.
    
    Equation: A @ v = lambda * v
    Where 'lambda' is the eigenvalue and 'v' is the eigenvector.
    
    Returns:
        eigenvalues, eigenvectors
    """
    print("--- 4. Eigenvalues and Eigenvectors ---")
    
    eigvals, eigvecs = la.eig(A)
    
    print(f"Eigenvalues:\n{eigvals}")
    print(f"Eigenvectors:\n{eigvecs}\n")
    
    return eigvals, eigvecs

# =====================================================================
# 5. Real-World Application: Image Compression via SVD
# =====================================================================

def image_compression_svd(k: int = 2) -> None:
    """
    Demonstrates how SVD can be used for lossy image compression.
    By keeping only the top 'k' singular values, we can approximate the original
    image using a fraction of the data.
    
    Args:
        k: Number of singular values to keep.
    """
    print("--- 5. Real-World Application: Image Compression via SVD ---")
    
    # Create a synthetic 10x10 "image" with some pattern
    image = np.array([
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    ], dtype=float)
    
    # Perform SVD
    U, s, Vh = la.svd(image)
    
    # Reconstruct the image using only the top k singular values
    # Sigma is a diagonal matrix of singular values
    Sigma_k = np.diag(s[:k])
    
    # U_k is N x k, Sigma_k is k x k, Vh_k is k x M
    compressed_image = U[:, :k] @ Sigma_k @ Vh[:k, :]
    
    print(f"Original Image (10x10, Rank {np.linalg.matrix_rank(image)}):\n{image.astype(int)}")
    print(f"\nCompressed Image using top {k} singular values:\n{np.round(compressed_image, 1)}")
    
    # Calculate compression ratio
    original_size = image.shape[0] * image.shape[1]
    compressed_size = (image.shape[0] * k) + k + (k * image.shape[1])
    print(f"\nOriginal size (elements): {original_size}")
    print(f"Compressed size (elements): {compressed_size}")
    print(f"Space Saved: {(1 - compressed_size/original_size)*100:.1f}%\n")

# =====================================================================
# 6. Performance & Edge Cases
# =====================================================================

def performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and edge cases in linear algebra operations.
    """
    print("--- 6. Performance & Edge Cases ---")
    
    # Edge Case: Singular Matrix
    A_singular = np.array([[1, 2], [2, 4]])
    print("Attempting to solve with a singular matrix (det = 0):")
    print(A_singular)
    try:
        b = np.array([1, 1])
        la.solve(A_singular, b)
    except la.LinAlgError as e:
        print(f"Caught expected LinAlgError: {e}")
        
    # Edge Case: Ill-conditioned Matrix
    # Small changes in input cause massive changes in output.
    A_ill = np.array([[1, 1], [1, 1.000000001]])
    cond = np.linalg.cond(A_ill)
    print(f"\nCondition number of ill-conditioned matrix: {cond:.2e}")
    print("Large condition numbers (>1e14) indicate potential precision loss in solving linear systems.\n")

# =====================================================================
# 7. Interview Challenge: PageRank Algorithm Simulation
# =====================================================================

def interview_challenge_pagerank(links: np.ndarray, num_iterations: int = 100, d: float = 0.85) -> np.ndarray:
    """
    Interview Challenge: Implement a simplified Google PageRank algorithm using Eigenvector Centrality.
    
    PageRank can be modeled as finding the dominant eigenvector of the modified 
    adjacency matrix of the web graph.
    
    Args:
        links: N x N adjacency matrix where links[i, j] = 1 if node j links to node i.
        num_iterations: Number of power iterations.
        d: Damping factor (probability of clicking a link vs jumping to random page).
        
    Returns:
        ranks: The PageRank scores for each node.
    """
    print("--- 7. Interview Challenge: PageRank (Eigenvector Centrality) ---")
    N = links.shape[0]
    
    # Normalize columns so they sum to 1 (Stochastic Matrix)
    col_sums = links.sum(axis=0)
    # Handle sink nodes (nodes with no outbound links) by linking them to all nodes
    col_sums[col_sums == 0] = N
    links_normalized = links / col_sums
    
    # Create the Google Matrix (incorporating damping factor)
    M = d * links_normalized + (1 - d) / N * np.ones((N, N))
    
    # Using Power Iteration to find the principal eigenvector
    # Start with equal probability for all pages
    v = np.ones(N) / N
    
    for _ in range(num_iterations):
        v = M @ v
        
    print(f"Adjacency Matrix:\n{links}")
    print(f"Calculated PageRanks:\n{v}\n")
    return v

# =====================================================================
# Test Suite
# =====================================================================

def run_tests() -> None:
    """
    Test suite to validate implementations.
    """
    print("--- Running Tests ---")
    try:
        # Test linear solver
        A = np.array([[3, 1], [1, 2]])
        b = np.array([9, 8])
        x = la.solve(A, b)
        assert np.allclose(x, [2., 3.]), "Solve linear system failed"
        
        # Test determinant
        assert np.isclose(la.det(A), 5.0), "Determinant failed"
        
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")

if __name__ == "__main__":
    print("========== Exploring SCIPY LINEAR ALGEBRA ==========\n")
    
    # 1. Basic Operations
    A_sq = np.array([[4, 3], [6, 3]])
    basic_matrix_operations(A_sq)
    
    # 2. Linear Systems
    b_vec = np.array([10, 12])
    solve_linear_system(A_sq, b_vec)
    
    # 3. Matrix Decompositions
    A_decomp = np.array([[12, -51, 4], [6, 167, -68], [-4, 24, -41]])
    matrix_decompositions(A_decomp)
    
    # 4. Eigen Problems
    eigen_problems(np.array([[0, 1], [-2, -3]]))
    
    # 5. Real-World Application
    image_compression_svd(k=2)
    
    # 6. Performance and Edge Cases
    performance_and_edge_cases()
    
    # 7. Interview Challenge (PageRank)
    # Graph: A <-> B, B -> C, C -> A
    # A=0, B=1, C=2
    web_graph = np.array([
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0]
    ], dtype=float)
    interview_challenge_pagerank(web_graph)
    
    # 8. Run Tests
    run_tests()
    
    print("========== END OF SCIPY LINEAR ALGEBRA ==========\n")
