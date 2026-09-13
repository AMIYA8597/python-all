"""
# ==============================================================================
# LABORATORY: MATRIX EXPONENTIATION (O(LOG N) LINEAR RECURRENCES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned Binary Exponentiation (Fast Power). It calculates X^N in O(log N).
# 
# What if N is massive? Like N = 1,000,000,000.
# Imagine a Dynamic Programming problem: "Find the 1 Billionth Fibonacci number, 
# modulo 10^9 + 7."
#
# A standard DP loop takes O(N) time. Looping 1 Billion times in Python will take 
# roughly 10 seconds and TLE (Time Limit Exceeded) on a coding interview platform.
#
# Can we jump straight to the 1 Billionth number instantly?
# Yes! The secret is MATRIX EXPONENTIATION.
#
# Fast Exponentiation works on integers, but mathematically, it also perfectly 
# applies to Matrices! 
# We can represent the state transition of the Fibonacci sequence as a 2x2 matrix:
# [ 1  1 ]   [ F(n)   ]   [ F(n+1) ]
# [ 1  0 ] * [ F(n-1) ] = [ F(n)   ]
#
# By continuously multiplying this state vector by the Transformation Matrix, 
# we walk through the sequence.
# But wait! Because of matrix algebra rules, multiplying the state by the matrix 
# N times is mathematically identical to raising the Matrix ITSELF to the N-th power!
#
# Transformation_Matrix^N * Initial_State = Final_State.
#
# We can calculate Matrix^N using Binary Exponentiation! This instantly calculates 
# the 1 Billionth state in exactly O(log N) time (roughly 30 matrix multiplications).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement O(K^3) Matrix Multiplication (where K is matrix size).
# - Implement Matrix Binary Exponentiation.
# - Solve Fibonacci in O(log N) time.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CORE MATRIX OPERATIONS
# ==============================================================================
def multiply_matrices(A: List[List[int]], B: List[List[int]], mod: int = 1000000007) -> List[List[int]]:
    """
    Standard Matrix Multiplication.
    Time Complexity: O(R1 * C1 * C2) -> O(K^3) for square matrices of size K.
    Since K is usually very small (e.g., 2x2 for Fibonacci), this is effectively O(1).
    """
    R_A = len(A)
    C_A = len(A[0])
    R_B = len(B)
    C_B = len(B[0])
    
    if C_A != R_B:
        raise ValueError("Invalid matrix dimensions for multiplication!")
        
    # Create the result matrix filled with 0s
    C = [[0] * C_B for _ in range(R_A)]
    
    for i in range(R_A):
        for j in range(C_B):
            for k in range(C_A):
                # The dot product of Row i from A, and Column j from B
                # We apply modulo at every step to prevent integer overflow!
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
                
    return C


def matrix_exponentiation(matrix: List[List[int]], exp: int, mod: int = 1000000007) -> List[List[int]]:
    """
    Calculates Matrix^Exp in strict O(K^3 * log(Exp)) time!
    """
    n = len(matrix)
    
    # 1. INITIALIZE IDENTITY MATRIX
    # The Identity Matrix (1s on the diagonal, 0s elsewhere) is the mathematical 
    # equivalent of the number "1" in matrix multiplication.
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
        
    base = matrix
    
    # 2. BINARY EXPONENTIATION LOOP
    # Exact same logic as integer fast power!
    while exp > 0:
        if exp % 2 == 1:
            result = multiply_matrices(result, base, mod)
            
        exp //= 2
        base = multiply_matrices(base, base, mod)
        
    return result


# ==============================================================================
# 4. APPLICATION: O(LOG N) FIBONACCI
# ==============================================================================
def fibonacci_log_n(n: int, mod: int = 1000000007) -> int:
    """
    Calculates the N-th Fibonacci number instantly, bypassing linear DP loops.
    """
    if n == 0: return 0
    if n == 1: return 1
    
    # The Transition Matrix for Fibonacci:
    # F(n) = 1*F(n-1) + 1*F(n-2)
    # F(n-1) = 1*F(n-1) + 0*F(n-2)
    transition = [
        [1, 1],
        [1, 0]
    ]
    
    # We want to jump to state N. 
    # Because our initial base state is [F(1), F(0)], we only need to jump (N-1) times!
    matrix_power = matrix_exponentiation(transition, n - 1, mod)
    
    # The Base State Vector:
    # [ F(1) ] = [ 1 ]
    # [ F(0) ] = [ 0 ]
    
    # Final Math: Matrix_Power * Base_State
    # result_F_n = (matrix_power[0][0] * F(1)) + (matrix_power[0][1] * F(0))
    # Since F(0) is 0, the second term vanishes!
    # result_F_n = matrix_power[0][0] * 1
    
    return matrix_power[0][0] % mod


def demonstrate_matrix_exp():
    section_header("Algorithm: Matrix Exponentiation")
    
    n_small = 10
    print(f"Calculating {n_small}th Fibonacci number...")
    print(f"O(log N) Result: {fibonacci_log_n(n_small)}")
    # Verification: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55
    print("Verification : 55")
    
    section_header("The 1 Billionth State Transition")
    
    # 1 Billionth Fibonacci Number!
    # O(N) DP loop would take roughly 10 seconds.
    # O(log N) Matrix Exp takes < 1 millisecond.
    n_massive = 1000000000
    mod = 1000000007
    print(f"Calculating {n_massive:,}th Fibonacci number modulo {mod}...")
    ans = fibonacci_log_n(n_massive, mod)
    print(f"Instantly Calculated Result: {ans}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Transformation Matrix `[[1, 1], [1, 0]]` mathematically work?
   Answer: It perfectly encodes the linear recurrence relation. 
   When we multiply it by the state vector `[F(n-1), F(n-2)]`:
   Row 1: `(1 * F(n-1)) + (1 * F(n-2))`. This perfectly calculates the formula for $F(n)$!
   Row 2: `(1 * F(n-1)) + (0 * F(n-2))`. This perfectly shifts $F(n-1)$ down into the second slot, preparing it to be the new $F(n-2)$ for the next cycle!
   The matrix is a mathematically pure factory conveyor belt.

2. Does Matrix Exponentiation only work for Fibonacci?
   Answer: No! It works for ANY "Linear Recurrence Relation".
   If a problem says: "A valid sequence of length $N$ cannot have 3 consecutive 'A's. How many valid sequences exist?", you can model the "states" (Ended in 0 A's, 1 A, 2 A's) as a $3 \times 3$ Transformation Matrix. You can then instantly calculate the answer for $N = 10^{18}$ by raising the $3 \times 3$ matrix to the power of $10^{18}$ in exactly $O(\log N)$ operations! It is the ultimate weapon for massive combinatorics problems.

3. What is the time complexity if the transition matrix is size $K \times K$?
   Answer: Matrix multiplication takes $O(K^3)$ time (using the standard 3-nested `for` loops). Since we must multiply matrices $\log_2(N)$ times during binary exponentiation, the absolute final time complexity is $O(K^3 \log N)$. This means Matrix Exponentiation is only fast if the number of states ($K$) is relatively small (usually $K \le 50$). If $K$ is massive, the $K^3$ term will bottleneck the algorithm.
"""

if __name__ == "__main__":
    demonstrate_matrix_exp()
    print("\n[SUCCESS] Laboratory: Matrix Exponentiation Completed.")
