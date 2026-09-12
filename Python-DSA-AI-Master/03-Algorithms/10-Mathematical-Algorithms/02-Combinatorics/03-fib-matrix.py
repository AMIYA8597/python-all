"""
Module: Fibonacci sequence via Matrix Exponentiation

Learning Objectives:
1. Review traditional Fibonacci algorithms.
2. Understand matrix exponentiation.
3. Compute the nth Fibonacci number in O(log n) time.

Concept Explanation:
- The Fibonacci sequence can be represented as a matrix multiplication:
  | F(n)   | = | 1 1 | ^ (n-1) * | F(1) |
  | F(n-1) |   | 1 0 |           | F(0) |
- Using binary exponentiation on matrices, we can compute F(n) in O(log n) time.

Performance Analysis:
- Recursive: O(2^n)
- Iterative DP: O(n)
- Matrix Exponentiation: O(log n) time, O(1) space.

Edge Cases:
- n = 0, n = 1
- Negative n (typically invalid or generalized to negative Fibonacci).
"""

from typing import List

# --- Basic Implementation ---
def fib_iterative(n: int) -> int:
    """O(n) time, O(1) space Fibonacci."""
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# --- Intermediate Implementation ---
def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Multiplies two 2x2 matrices."""
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

# --- Advanced Implementation ---
def matrix_power(M: List[List[int]], p: int) -> List[List[int]]:
    """Computes M^p in O(log p) time."""
    res = [[1, 0], [0, 1]] # Identity matrix
    base = M
    while p > 0:
        if p % 2 == 1:
            res = matrix_multiply(res, base)
        base = matrix_multiply(base, base)
        p //= 2
    return res

def fib_matrix(n: int) -> int:
    """Computes nth Fibonacci number using matrix exponentiation."""
    if n <= 1:
        return n
    T = [[1, 1], [1, 0]]
    T_n_minus_1 = matrix_power(T, n - 1)
    return T_n_minus_1[0][0]

# --- Interview Challenge ---
# Problem: Climbing Stairs with max k steps
# Given n steps, you can take 1 to k steps at a time. Count ways.
def climb_stairs_k(n: int, k: int) -> int:
    """O(n*k) dynamic programming approach."""
    if n <= 1: return 1
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i] += dp[i - j]
    return dp[n]

# --- Tests ---
def run_tests():
    assert fib_iterative(10) == 55
    assert fib_matrix(10) == 55
    assert fib_matrix(0) == 0
    assert fib_matrix(1) == 1
    assert climb_stairs_k(4, 2) == 5 # 1111, 112, 121, 211, 22
    print("All tests passed for 03-fib-matrix.py!")

if __name__ == "__main__":
    run_tests()
