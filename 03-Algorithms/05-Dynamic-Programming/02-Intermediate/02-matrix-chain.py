"""
# ==============================================================================
# LABORATORY: MATRIX CHAIN MULTIPLICATION (INTERVAL DP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you have 3 Matrices: A, B, and C.
# Matrix multiplication is Associative. You can do `(A * B) * C`, or you can 
# do `A * (B * C)`. Mathematically, the final matrix will be identical.
#
# But computationally? The number of CPU operations is wildly different!
# Imagine the dimensions:
# A = 10 x 30
# B = 30 x 5
# C = 5 x 60
#
# Path 1: (A * B) * C
# 1. A*B takes 10 * 30 * 5 = 1,500 operations. (Creates a 10x5 matrix).
# 2. Result * C takes 10 * 5 * 60 = 3,000 operations.
# Total: 4,500 operations.
#
# Path 2: A * (B * C)
# 1. B*C takes 30 * 5 * 60 = 9,000 operations. (Creates a 30x60 matrix).
# 2. A * Result takes 10 * 30 * 60 = 18,000 operations.
# Total: 27,000 operations!
#
# Path 1 is 6X faster! If you are writing a Deep Learning library (PyTorch) 
# or a 3D Graphics Engine (OpenGL), you MUST figure out the optimal parentheses 
# placement BEFORE you start multiplying massive matrices.
#
# This introduces "Interval DP" (Partition DP). Instead of iterating `i` and `j` 
# normally, we must build the DP table DIAGONALLY, based on the `length` of the 
# interval!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Interval DP (Looping by Length).
# - Master the Partition split `k`.
# - Calculate the `cost` of merging two partitions.
#
# ==============================================================================
"""

import sys
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. INTERVAL DP TABULATION
# ==============================================================================
def matrix_chain_order(p: List[int]) -> int:
    """
    `p` represents the dimensions of the matrices.
    Matrix `i` has dimension `p[i-1] x p[i]`.
    If we have 4 matrices, `p` has 5 elements.
    
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    """
    n = len(p)
    # The number of matrices is n - 1
    matrix_count = n - 1
    
    # 1. STATE DEFINITION
    # `dp[i][j]` represents the MINIMUM operations to multiply matrices from index `i` to `j`.
    dp = [[0 for _ in range(matrix_count + 1)] for _ in range(matrix_count + 1)]
    
    # 2. INITIALIZATION
    # A single matrix `i` to `i` requires 0 multiplications.
    # The diagonal dp[i][i] is already initialized to 0.
    
    # 3. THE INTERVAL DP LOOP
    # We CANNOT loop `i` and `j` sequentially. 
    # To solve `dp[1][4]`, we need the answers to `dp[1][2]` and `dp[3][4]`. 
    # Therefore, we must solve ALL intervals of length 2, then ALL intervals of 
    # length 3, etc.
    
    # Loop over the `length` of the chain
    for length in range(2, matrix_count + 1):
        
        # Loop over the starting index `i`
        for i in range(1, matrix_count - length + 2):
            
            # Calculate the ending index `j` based on start + length
            j = i + length - 1
            
            # We want to find the MINIMUM, so initialize to Infinity
            dp[i][j] = sys.maxsize
            
            # 4. THE PARTITION LOOP (k)
            # We try splitting the interval (i to j) at EVERY possible point `k`.
            # e.g. If calculating (A B C D), we try:
            # (A) * (B C D)  -> k = 1
            # (A B) * (C D)  -> k = 2
            # (A B C) * (D)  -> k = 3
            for k in range(i, j):
                
                # --- STATE TRANSITION EQUATION ---
                # Cost 1: The minimum cost to multiply the LEFT group (i to k)
                # Cost 2: The minimum cost to multiply the RIGHT group (k+1 to j)
                # Cost 3: The cost to multiply the two resulting matrices together!
                #         The resulting left matrix is size: p[i-1] x p[k]
                #         The resulting right matrix is size: p[k] x p[j]
                #         Cost to multiply them = p[i-1] * p[k] * p[j]
                
                cost = dp[i][k] + dp[k + 1][j] + (p[i - 1] * p[k] * p[j])
                
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    
    # The answer for the entire chain (matrix 1 to matrix_count) is in the top right!
    return dp[1][matrix_count]


def demonstrate_matrix_chain():
    section_header("Algorithm: Matrix Chain Multiplication")
    
    # p = [10, 30, 5, 60]
    # Matrix 1 (A) = 10 x 30
    # Matrix 2 (B) = 30 x 5
    # Matrix 3 (C) = 5 x 60
    p1 = [10, 30, 5, 60]
    
    print(f"Matrix Dimensions Array: {p1}")
    print("A: 10x30 | B: 30x5 | C: 5x60")
    
    ans1 = matrix_chain_order(p1)
    print(f"\nMinimum Operations: {ans1}")
    print("Path: (A * B) * C = (10*30*5) + (10*5*60) = 1500 + 3000 = 4500.")
    print("Compare to: A * (B * C) = (30*5*60) + (10*30*60) = 9000 + 18000 = 27000!")
    
    
    p2 = [40, 20, 30, 10, 30]
    # 4 Matrices
    print(f"\nMatrix Dimensions Array: {p2}")
    ans2 = matrix_chain_order(p2)
    print(f"Minimum Operations: {ans2} (Expected: 26000)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we loop by `length` instead of `i` and `j`?
   Answer: This is the defining characteristic of "Interval DP" or "Partition DP". The State Transition Equation relies on smaller subarrays. If you just loop `i` from 1 to N, and `j` from 1 to N, when you reach `dp[1][4]`, the algorithm will try to read `dp[3][4]` which hasn't been calculated yet! By looping by `length` (2, then 3, then 4), we guarantee that all smaller subarrays are fully calculated before we ever attempt to query them.

2. Why is the Time Complexity $O(N^3)$?
   Answer: We have 3 nested loops. The outer loop is `length` (runs $O(N)$ times). The middle loop is the start index `i` (runs $O(N)$ times). The inner loop is the partition point `k`, which loops from `i` to `j` (runs $O(N)$ times). $N \\times N \\times N = O(N^3)$. 

3. How do we output the actual parentheses grouping, not just the number of operations?
   Answer: We must maintain a secondary DP table (often called `bracket[i][j]`). Whenever `cost < dp[i][j]`, we update `dp[i][j] = cost`, AND we save the optimal `k` index into `bracket[i][j] = k`. After the algorithm finishes, we write a small recursive function that reads the `bracket` matrix to print `(`, `)`, and `A_i` in the correct order.
"""

if __name__ == "__main__":
    demonstrate_matrix_chain()
    print("\n[SUCCESS] Laboratory: Matrix Chain Multiplication Completed.")
