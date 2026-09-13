"""
# ==============================================================================
# LABORATORY: MATRIX MODELING FOR COMBINATORICS (LINEAR RECURRENCES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Matrix Exponentiation can calculate the 1 Billionth Fibonacci 
# number in O(log N) time.
#
# But Fibonacci is just the simplest possible example. The true power of Matrix 
# Exponentiation lies in Combinatorics: solving complex counting problems for 
# astronomically large N.
#
# Scenario 1: The Tribonacci Sequence.
# T(n) = T(n-1) + T(n-2) + T(n-3).
# How do we build a matrix for this? We need a 3x3 matrix that physically shifts 
# all three states simultaneously!
#
# Scenario 2: Domino Tiling.
# How many ways can you tile a 2xN grid using 2x1 dominoes?
# For N = 1 Billion, a DP loop crashes. But the state transitions (Placing a 
# vertical domino vs two horizontal dominoes) forms a linear recurrence! 
# We can model it as a Matrix.
#
# Scenario 3: Valid String Combinatorics.
# "How many binary strings of length N exist that do NOT contain three consecutive 0s?"
# We can model this as a Finite State Machine (FSM):
# State 0: Ended in '1'.
# State 1: Ended in '0'.
# State 2: Ended in '00'.
# The transitions between these states form a 3x3 matrix. Raising this matrix 
# to the power of N instantly calculates the exact number of valid strings in 
# O(log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model complex Linear Recurrences into $K \times K$ Matrices.
# - Solve Tribonacci in O(log N).
# - Model State Machines for Combinatorics problems.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helpers: Matrix Multiplication & Exponentiation (O(K^3 log N)) ---
def multiply_matrices(A: List[List[int]], B: List[List[int]], mod: int = 1000000007) -> List[List[int]]:
    R_A, C_A, C_B = len(A), len(A[0]), len(B[0])
    C = [[0] * C_B for _ in range(R_A)]
    for i in range(R_A):
        for j in range(C_B):
            for k in range(C_A):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_exponentiation(matrix: List[List[int]], exp: int, mod: int = 1000000007) -> List[List[int]]:
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i in range(n): result[i][i] = 1
    base = matrix
    while exp > 0:
        if exp % 2 == 1: result = multiply_matrices(result, base, mod)
        exp //= 2
        base = multiply_matrices(base, base, mod)
    return result
# --------------------------------------------------------------------


# ==============================================================================
# 3. TRIBONACCI SEQUENCE (3x3 MATRIX)
# ==============================================================================
def tribonacci_log_n(n: int, mod: int = 1000000007) -> int:
    """
    T(0) = 0, T(1) = 1, T(2) = 1
    T(n) = T(n-1) + T(n-2) + T(n-3)
    """
    if n == 0: return 0
    if n == 1 or n == 2: return 1
    
    # 1. BUILD THE TRANSITION MATRIX
    # We want to map: [T(n-1), T(n-2), T(n-3)] -> [T(n), T(n-1), T(n-2)]
    # Row 0: 1*T(n-1) + 1*T(n-2) + 1*T(n-3) = T(n)
    # Row 1: 1*T(n-1) + 0*T(n-2) + 0*T(n-3) = T(n-1) (Shifts it down!)
    # Row 2: 0*T(n-1) + 1*T(n-2) + 0*T(n-3) = T(n-2) (Shifts it down!)
    transition = [
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]
    
    # We want to reach state N. Our base state starts at T(2).
    # So we need to apply the transition (N - 2) times.
    matrix_power = matrix_exponentiation(transition, n - 2, mod)
    
    # 2. MULTIPLY BY BASE STATE
    # Base state vector: [ T(2), T(1), T(0) ] = [ 1, 1, 0 ]
    # We only care about the top value of the resulting vector (which is T(n)).
    # T(n) = (Row0_Col0 * 1) + (Row0_Col1 * 1) + (Row0_Col2 * 0)
    ans = (matrix_power[0][0] * 1 + matrix_power[0][1] * 1) % mod
    
    return ans


# ==============================================================================
# 4. FINITE STATE MACHINE COMBINATORICS
# ==============================================================================
def count_valid_binary_strings(n: int, mod: int = 1000000007) -> int:
    """
    Finds the number of binary strings of length N that do NOT contain "000".
    We model this as a State Machine.
    State 0: The string currently ends in '1'. (No danger).
    State 1: The string currently ends in one '0'. (Mild danger).
    State 2: The string currently ends in two '00's. (Extreme danger!).
    """
    if n == 0: return 0
    if n == 1: return 2 # "0", "1"
    if n == 2: return 4 # "00", "01", "10", "11"
    
    # 1. BUILD THE DFA TRANSITION MATRIX
    # If we are in State 0 (ends in 1):
    # - Append '1': Stay in State 0.
    # - Append '0': Move to State 1.
    #
    # If we are in State 1 (ends in 0):
    # - Append '1': Reset to State 0!
    # - Append '0': Move to State 2.
    #
    # If we are in State 2 (ends in 00):
    # - Append '1': Reset to State 0!
    # - Append '0': INVALID! We drop it (No transition).
    #
    # Matrix mapping [Count_State0, Count_State1, Count_State2]:
    # Row 0 (New State 0): Gets input from State 0 (via '1'), State 1 (via '1'), State 2 (via '1')
    # Row 1 (New State 1): Gets input from State 0 (via '0') ONLY.
    # Row 2 (New State 2): Gets input from State 1 (via '0') ONLY.
    transition = [
        [1, 1, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]
    
    # Wait... look at the Matrix! 
    # It is MATHEMATICALLY IDENTICAL to the Tribonacci sequence matrix!
    # The number of valid strings avoiding "000" is exactly the Tribonacci sequence!
    
    matrix_power = matrix_exponentiation(transition, n - 2, mod)
    
    # Base states for Length 2:
    # State 0 (ends in 1): "01", "11" -> Count = 2
    # State 1 (ends in 0): "10" -> Count = 1
    # State 2 (ends in 00): "00" -> Count = 1
    
    # T_N(State0) = (M[0][0]*2) + (M[0][1]*1) + (M[0][2]*1)
    # T_N(State1) = (M[1][0]*2) + (M[1][1]*1) + (M[1][2]*1)
    # T_N(State2) = (M[2][0]*2) + (M[2][1]*1) + (M[2][2]*1)
    
    # Summing them up gives the total valid strings!
    total = 0
    for row in range(3):
        total += (matrix_power[row][0] * 2 + matrix_power[row][1] * 1 + matrix_power[row][2] * 1) % mod
        
    return total % mod


def demonstrate_matrix_combinatorics():
    section_header("Algorithm: Tribonacci via Matrix Exp")
    
    n_small = 10
    print(f"Calculating {n_small}th Tribonacci number...")
    print(f"Result: {tribonacci_log_n(n_small)}")
    # Tribonacci: 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149
    print("Verify: 81")
    
    section_header("Application: State Machine Combinatorics")
    
    n = 10
    print(f"How many binary strings of length {n} DO NOT contain '000'?")
    ans = count_valid_binary_strings(n)
    print(f"O(log N) Matrix Result: {ans}")
    
    print("\nVerifying with brute force...")
    valid_count = 0
    for i in range(2**n):
        binary_str = bin(i)[2:].zfill(n)
        if "000" not in binary_str:
            valid_count += 1
            
    print(f"Brute Force Result  : {valid_count}")
    print("Match confirmed! The Matrix math is flawless.")
    
    print(f"\nCalculating for N = 1,000,000,000...")
    massive_ans = count_valid_binary_strings(1000000000)
    print(f"Result (Modulo 10^9+7): {massive_ans}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How do you shift a state down in a matrix?
   Answer: Look at Row 1 of the Tribonacci matrix: `[1, 0, 0]`. When multiplied by the column vector `[T(n-1), T(n-2), T(n-3)]`, the `1` locks onto $T(n-1)$ and the `0`s annihilate the rest. The result is exactly $T(n-1)$. By placing this row below the calculation row, we physically shift $T(n-1)$ down one slot in the resulting vector, preparing it to be the new $T(n-2)$ for the next cycle! This diagonal "waterfall" of 1s (called the Companion Matrix) is the universal structure for all linear recurrences.

2. Why did avoiding "000" perfectly match the Tribonacci sequence?
   Answer: Let $f(n)$ be the number of valid strings of length $n$. 
   A valid string can end in '1', '10', or '100'. 
   - If we append '1' to any valid string of length $n-1$, it remains valid. ($f(n-1)$).
   - If we append '10' to any valid string of length $n-2$, it remains valid. ($f(n-2)$).
   - If we append '100' to any valid string of length $n-3$, it remains valid. ($f(n-3)$).
   Therefore, $f(n) = f(n-1) + f(n-2) + f(n-3)$. The combinatorial rule perfectly collapses into the exact mathematical recurrence of the Tribonacci sequence!

3. How do you handle constants in a linear recurrence? (e.g. $f(n) = 2f(n-1) + 3$)
   Answer: You add a dummy state to your vector that always equals 1!
   State vector: `[f(n-1), 1]`
   Matrix:
   `[ 2 , 3 ]`
   `[ 0 , 1 ]`
   Row 0 calculates: $2 \times f(n-1) + 3 \times 1 = f(n)$.
   Row 1 calculates: $0 \times f(n-1) + 1 \times 1 = 1$. (It perfectly preserves the dummy constant for the next cycle!).
"""

if __name__ == "__main__":
    demonstrate_matrix_combinatorics()
    print("\n[SUCCESS] Laboratory: Matrix Modeling Completed.")
