"""
Module: Matrix Chain Multiplication

Learning Objectives:
- Master interval/partition DP.
- Understand how parenthesization affects scalar multiplications.

Concept Explanation:
Given a sequence of matrices, find the most efficient way to multiply them. The problem
is to determine the optimal parenthesization of a matrix chain product that minimizes
scalar multiplications.

Performance Analysis:
- Basic (Recursive): O(2^N) Time, O(N) Space
- Intermediate (Memoized): O(N^3) Time, O(N^2) Space
- Advanced (Bottom-Up): O(N^3) Time, O(N^2) Space

Edge Cases:
- Less than 2 matrices
- Matrices with large dimensions causing integer overflow

Interview Challenge:
"Print the optimal parenthesization string for the matrices."
"""
from typing import List, Dict, Tuple

def mcm_recursive(p: List[int], i: int, j: int) -> int:
    if i == j: return 0
    min_cost = float('inf')
    for k in range(i, j):
        cost = mcm_recursive(p, i, k) + mcm_recursive(p, k+1, j) + p[i-1]*p[k]*p[j]
        if cost < min_cost:
            min_cost = cost
    return int(min_cost)

def mcm_memo(p: List[int], i: int, j: int, memo: Dict[Tuple[int, int], int]) -> int:
    if i == j: return 0
    if (i, j) in memo: return memo[(i, j)]
    min_cost = float('inf')
    for k in range(i, j):
        cost = mcm_memo(p, i, k, memo) + mcm_memo(p, k+1, j, memo) + p[i-1]*p[k]*p[j]
        if cost < min_cost:
            min_cost = cost
    memo[(i, j)] = int(min_cost)
    return memo[(i, j)]

def mcm_dp(p: List[int]) -> int:
    n = len(p)
    dp = [[0]*n for _ in range(n)]
    for L in range(2, n):
        for i in range(1, n-L+1):
            j = i+L-1
            dp[i][j] = float('inf')
            for k in range(i, j):
                q = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
                if q < dp[i][j]:
                    dp[i][j] = q
    return dp[1][n-1]

def test_mcm():
    p = [1, 2, 3, 4]
    assert mcm_recursive(p, 1, 3) == 18
    assert mcm_dp(p) == 18
    print("MCM tests passed.")

if __name__ == "__main__":
    test_mcm()
