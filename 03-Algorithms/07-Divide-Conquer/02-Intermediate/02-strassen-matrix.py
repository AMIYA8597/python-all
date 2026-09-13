"""
# ==============================================================================
# LABORATORY: STRASSEN'S MATRIX MULTIPLICATION (THEORY OF COMPUTATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# How does a computer multiply two matrices?
# The standard mathematical formula (Row-by-Column dot product) uses three nested 
# `for` loops. Time Complexity: O(N^3).
# If you multiply two massive 10,000 x 10,000 matrices (common in AI/Deep Learning), 
# O(N^3) takes 1 Trillion operations.
#
# For centuries, mathematicians assumed O(N^3) was the absolute physical limit.
#
# In 1969, Volker Strassen proved them wrong using Divide & Conquer.
# If you divide a matrix into 4 quadrants (TopLeft, TopRight, BottomLeft, BottomRight), 
# a naive D&C algorithm requires 8 recursive multiplications. 
# Recurrence: T(N) = 8 * T(N/2) + O(N^2). Master Theorem: O(N^3). No improvement.
#
# Strassen discovered a bizarre, magical algebraic trick. By doing 10 extra matrix 
# additions (which are fast, O(N^2)), you can calculate the quadrants using 
# ONLY 7 recursive multiplications instead of 8!
#
# Recurrence: T(N) = 7 * T(N/2) + O(N^2). 
# Master Theorem: O(N^log2(7)) = O(N^2.807).
#
# Strassen's algorithm shattered the O(N^3) barrier and sparked a 50-year race 
# to find the absolute limit of matrix multiplication (currently around O(N^2.37)).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how a constant factor reduction in Recursion alters Big-O.
# - Implement the 7 Magical Strassen Equations.
# - Understand why Strassen's is usually only theoretical for small matrices.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATRIX MATH HELPERS (O(N^2) Addition/Subtraction)
# ==============================================================================
def add_matrix(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub_matrix(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


# ==============================================================================
# 4. STRASSEN'S ALGORITHM O(N^2.807)
# ==============================================================================
def strassen(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """
    Multiplies two NxN matrices A and B using Strassen's 7-Multiplication algorithm.
    (Assumes N is a power of 2 for simplicity).
    """
    n = len(A)
    
    # 1. BASE CASE (Standard O(N^3) multiplication for tiny matrices)
    # The algebraic overhead of Strassen's is so massive that it is actually 
    # SLOWER than standard O(N^3) for small matrices! We cut it off early.
    if n <= 2:
        # Standard 2x2 Matrix Multiplication
        ans = [[0, 0], [0, 0]]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    ans[i][j] += A[i][k] * B[k][j]
        return ans

    # 2. DIVIDE (Split matrices into 4 quadrants)
    mid = n // 2
    
    # Slice the Python lists into 4 blocks
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    # 3. CONQUER (The 7 Magical Strassen Equations)
    # Notice we ONLY make 7 recursive calls to `strassen`!
    # A standard D&C algorithm requires 8.
    M1 = strassen(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen(add_matrix(A21, A22), B11)
    M3 = strassen(A11, sub_matrix(B12, B22))
    M4 = strassen(A22, sub_matrix(B21, B11))
    M5 = strassen(add_matrix(A11, A12), B22)
    M6 = strassen(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen(sub_matrix(A12, A22), add_matrix(B21, B22))
    
    # 4. COMBINE (Assemble the resulting quadrants)
    # By algebraically combining those 7 matrices, we magically reconstruct 
    # the 4 quadrants of the final answer!
    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)
    
    # Stitch the 4 quadrants back into a single NxN matrix
    C = [[0]*n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
            
    return C


def demonstrate_strassen():
    section_header("Algorithm: Strassen's Matrix Multiplication")
    
    # 4x4 Matrices (N must be a power of 2 for this simple implementation)
    A = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    
    B = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ] # B is the Identity Matrix! A * B should = A!
    
    print("Matrix A:")
    for row in A: print(row)
        
    print("\nExecuting Strassen's O(N^2.81) Algorithm...")
    C = strassen(A, B)
    
    print("\nResulting Matrix C:")
    for row in C: print(row)
    print("\n(Notice how multiplying by the Identity Matrix perfectly returned A).")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does changing 8 multiplications to 7 physically change the Big-O Time Complexity?
   Answer: Because of the Recurrence Relation in the Master Theorem. $T(N) = aT(N/b) + f(N)$. The time complexity is dominated by $O(N^{\\log_b(a)})$. With 8 recursive calls, $\\log_2(8) = 3$, meaning $O(N^3)$. By finding a math trick that only requires 7 recursive calls, $a$ becomes 7. $\\log_2(7) = 2.807$. We physically altered the exponent of the polynomial growth rate!

2. If Strassen's is mathematically faster, why do standard Python/C++ libraries still use $O(N^3)$ algorithms for small matrices?
   Answer: "Hidden Constant Factors". While Strassen's is asymptotically faster for massive matrices (e.g., $N > 1000$), it requires doing 18 matrix additions/subtractions just to set up the 7 equations. Memory allocation and recursion overhead completely destroy the performance for small matrices. Real-world implementations (like NumPy/BLAS) use optimized hardware-level $O(N^3)$ (like SIMD instructions) until the matrix reaches a specific massive threshold, at which point it switches to Strassen's.

3. Are there algorithms faster than Strassen's $O(N^{2.807})$?
   Answer: Yes! The Coppersmith-Winograd algorithm achieves $O(N^{2.372})$. In 2020, Alman and Williams proved a bound of $O(N^{2.3728596})$. In 2022, DeepMind's AlphaTensor AI discovered new matrix multiplication equations that beat human-designed algorithms. However, these "Galactic Algorithms" have such insanely massive constant overheads that they are literally never used in real-world software.
"""

if __name__ == "__main__":
    demonstrate_strassen()
    print("\n[SUCCESS] Laboratory: Strassen's Algorithm Completed.")
