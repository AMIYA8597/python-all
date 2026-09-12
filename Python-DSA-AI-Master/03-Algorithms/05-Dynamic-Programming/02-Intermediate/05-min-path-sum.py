"""
Module: Minimum Path Sum

Learning Objectives:
- Solve grid-based DP problems.
- Perform state-space reduction from 2D to 1D.

Concept Explanation:
Given an M x N grid filled with non-negative numbers, find a path from top-left to
bottom-right which minimizes the sum of all numbers along its path. You can only
move right or down.

Performance Analysis:
- Basic (Recursive): O(2^(M+N)) Time, O(M+N) Space
- Intermediate (2D DP): O(M*N) Time, O(M*N) Space
- Advanced (1D DP): O(M*N) Time, O(N) Space

Edge Cases:
- Grid with only 1 row or 1 column
- Empty grid

Interview Challenge:
"Modify the algorithm if you are allowed to move diagonally as well."
"""
from typing import List, Dict, Tuple

def min_path_sum_recursive(grid: List[List[int]], i: int, j: int) -> int:
    if i == len(grid) - 1 and j == len(grid[0]) - 1:
        return grid[i][j]
    if i >= len(grid) or j >= len(grid[0]):
        return float('inf')
    return grid[i][j] + min(min_path_sum_recursive(grid, i+1, j), min_path_sum_recursive(grid, i, j+1))

def min_path_sum_2d(grid: List[List[int]]) -> int:
    if not grid or not grid[0]: return 0
    m, n = len(grid), len(grid[0])
    dp = [[0]*n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1, m): dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n): dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    return dp[m-1][n-1]

def min_path_sum_1d(grid: List[List[int]]) -> int:
    if not grid or not grid[0]: return 0
    m, n = len(grid), len(grid[0])
    dp = [0]*n
    dp[0] = grid[0][0]
    for j in range(1, n): dp[j] = dp[j-1] + grid[0][j]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j-1])
    return dp[n-1]

def test_min_path_sum():
    grid = [[1,3,1],[1,5,1],[4,2,1]]
    assert min_path_sum_2d(grid) == 7
    assert min_path_sum_1d(grid) == 7
    print("Min Path Sum tests passed.")

if __name__ == "__main__":
    test_min_path_sum()
