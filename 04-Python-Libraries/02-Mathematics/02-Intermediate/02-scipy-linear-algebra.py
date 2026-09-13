"""
# ==============================================================================
# LABORATORY: LINEAR ALGEBRA (SCIPY.LINALG)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Linear Algebra is the mathematical language of modern Artificial Intelligence.
# When a Neural Network "learns", it is physically just multiplying thousands 
# of massive matrices together and calculating gradients.
# 
# While NumPy has a basic `np.linalg` module, `scipy.linalg` is the industry 
# gold standard. It contains highly advanced bindings to the legendary Fortran 
# libraries BLAS (Basic Linear Algebra Subprograms) and LAPACK (Linear Algebra 
# PACKage), written in the 1970s and 1990s.
#
# These libraries are so absurdly optimized for CPU hardware vectorization 
# (SIMD) that it is virtually impossible to write a faster matrix multiplication 
# algorithm in any language on Earth.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Solve Systems of Linear Equations using $Ax = B$.
# - Calculate Eigenvalues and Eigenvectors (The core of Google's PageRank).
# - Perform Matrix Decompositions (LU, Singular Value Decomposition - SVD).
#
# ==============================================================================
"""

import numpy as np
from scipy import linalg

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SOLVING LINEAR SYSTEMS (Ax = B)
# ==============================================================================
def demonstrate_solve():
    section_header("Solving Linear Systems (Ax = B)")
    
    # Imagine a word problem:
    # 3 Apples and 2 Bananas cost $12.
    # 2 Apples and 5 Bananas cost $19.
    # What is the exact price of an Apple and a Banana?
    
    # Mathematically:
    # 3x + 2y = 12
    # 2x + 5y = 19
    
    # We construct the Coefficient Matrix (A):
    A = np.array([
        [3, 2],
        [2, 5]
    ])
    
    # We construct the Constant Vector (B):
    B = np.array([12, 19])
    
    # To solve this manually, you would calculate the Inverse of A, and multiply 
    # it by B: x = A^(-1) * B.
    # DO NOT DO THIS! Calculating inverses is mathematically unstable and slow.
    # `linalg.solve` uses LAPACK factorization, which is vastly faster and safer.
    
    solution = linalg.solve(A, B)
    print("Matrix A (Coefficients):")
    print(A)
    print("\nVector B (Constants):")
    print(B)
    
    print(f"\nSolution [Apple Price, Banana Price]: {solution}")
    
    # Verify the math! (A * x should equal B)
    # The `@` operator in Python 3.5+ performs native Matrix Multiplication!
    verification = A @ solution
    print(f"Verification (A @ solution): {verification} (Matches B perfectly!)")


# ==============================================================================
# 4. EIGENVALUES AND EIGENVECTORS
# ==============================================================================
def demonstrate_eigen():
    section_header("Eigenvalues and Eigenvectors")
    
    # When you multiply a Vector by a Matrix, the vector usually changes 
    # direction and scale (it gets rotated and stretched).
    #
    # An EIGENVECTOR of a matrix is a magical vector that, when multiplied by 
    # the matrix, ONLY changes scale! It DOES NOT rotate! 
    # The EIGENVALUE is the exact amount it was stretched by.
    #
    # Why care? Google's original PageRank algorithm modeled the entire internet 
    # as a massive matrix of hyperlinks. The "importance" of every webpage on 
    # Earth was mathematically derived by finding the dominant Eigenvector of 
    # that matrix!
    
    A = np.array([
        [4, -2],
        [1,  1]
    ])
    
    # `eig` returns a tuple containing an array of Eigenvalues, and a 2D array 
    # whose columns are the corresponding Eigenvectors!
    eigenvalues, eigenvectors = linalg.eig(A)
    
    print("Matrix A:")
    print(A)
    
    print(f"\nEigenvalues (Lambda): {eigenvalues.real}")
    
    print("\nEigenvectors (Normalized Columns):")
    print(eigenvectors)
    
    # Verification of the mathematical definition: A * v = Lambda * v
    print("\nVerification (First Eigenvalue/Vector):")
    lambda_1 = eigenvalues.real[0]
    v_1 = eigenvectors[:, 0] # Extract the first column
    
    left_side = A @ v_1
    right_side = lambda_1 * v_1
    
    print(f"A * v      = {left_side}")
    print(f"Lambda * v = {right_side}")
    print("(They match perfectly! The vector was only scaled, not rotated!)")


# ==============================================================================
# 5. SINGULAR VALUE DECOMPOSITION (SVD)
# ==============================================================================
def demonstrate_svd():
    section_header("Singular Value Decomposition (SVD)")
    
    # SVD is the most important matrix decomposition in Machine Learning.
    # It decomposes ANY matrix into three separate matrices: U * S * V^T
    # It is the mathematical engine behind Principal Component Analysis (PCA) 
    # and Recommender Systems (like Netflix predicting what movie you will like).
    
    # An abstract 3x2 matrix
    M = np.array([
        [1, 2],
        [3, 4],
        [5, 6]
    ])
    
    # Perform SVD
    # U: Left singular vectors (Orthogonal)
    # s: Singular values (1D array of the diagonal elements, sorted by importance!)
    # Vh: Right singular vectors transposed (Orthogonal)
    U, s, Vh = linalg.svd(M)
    
    print("Original Matrix M:")
    print(M)
    
    print("\nSingular Values (s):")
    print(s)
    print("Notice how the first value is vastly larger. SVD mathematically ")
    print("extracts the absolute most 'important' hidden features of the data!")
    
    # Reconstruct the original matrix to prove the decomposition works!
    # Because `s` is returned as a 1D array, we must convert it into a full 
    # diagonal matrix of the correct shape to perform the math: M = U @ Sigma @ Vh
    Sigma = np.zeros((M.shape[0], M.shape[1]))
    np.fill_diagonal(Sigma, s)
    
    reconstruction = U @ Sigma @ Vh
    
    print("\nReconstructed Matrix (U @ Sigma @ Vh):")
    print(np.round(reconstruction, 2))


def run_all_labs():
    demonstrate_solve()
    demonstrate_eigen()
    demonstrate_svd()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why should you use `scipy.linalg.solve(A, B)` instead of calculating the inverse `inv(A) @ B`?
   Answer: Calculating the mathematical inverse of a large matrix requires $O(N^3)$ operations and is highly susceptible to floating-point truncation errors (especially if the matrix is nearly singular). `linalg.solve` does NOT calculate the inverse. It uses LAPACK factorization (like LU Decomposition) to solve the system of equations directly. This is significantly faster, requires far less RAM, and is mathematically immune to the catastrophic floating-point errors that plague raw inverse calculations.

2. What is an Eigenvector, and why is it important in Machine Learning?
   Answer: When a matrix multiplies a vector, it typically rotates and stretches it. An Eigenvector is a special vector that only gets stretched (scaled), completely resisting rotation! The scaling factor is the Eigenvalue. In ML (specifically Principal Component Analysis - PCA), the Eigenvectors of a dataset's Covariance Matrix represent the exact physical axes (dimensions) along which the data varies the most. This allows us to compress a 1,000-dimensional dataset into 3 dimensions by keeping only the 3 Eigenvectors with the largest Eigenvalues!

3. What is the difference between `numpy.linalg` and `scipy.linalg`?
   Answer: They share a lot of the same functions, but `scipy.linalg` is officially guaranteed to be compiled against advanced BLAS/LAPACK libraries. It contains a much larger ecosystem of advanced matrix decompositions (Schur, QZ, Cholesky), matrix functions (Matrix Exponentials `expm`, used heavily in quantum mechanics and differential equations), and provides explicit access to lower-level LAPACK routines. If you are doing serious linear algebra, `scipy` is the standard.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SciPy Linear Algebra Completed.")
