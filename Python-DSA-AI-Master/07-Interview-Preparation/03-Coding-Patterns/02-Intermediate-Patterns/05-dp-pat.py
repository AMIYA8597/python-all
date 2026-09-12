"""
Dynamic Programming Pattern

Learning Objectives:
1. Understand Overlapping Subproblems and Optimal Substructure.
2. Distinguish between Memoization (Top-Down) and Tabulation (Bottom-Up).
3. Identify when a problem can be solved with DP.
4. Master common DP patterns: 1D arrays, 2D grids, strings.
5. Analyze space and time complexity optimizations.

Concept Explanation:
Dynamic Programming is an optimization over plain recursion. Whenever we see a recursive solution that has repeated calls for same inputs, we can optimize it using DP. It trades space for time.
"""

from typing import List

# Basic Implementation: Climbing Stairs (1D DP)
def climb_stairs(n: int) -> int:
    """Time: O(N), Space: O(1)"""
    if n <= 2:
        return n
    # We only need the last two values, so we optimize space to O(1)
    one, two = 1, 1
    for i in range(n - 1):
        temp = one
        one = one + two
        two = temp
    return one

# Intermediate Implementation: Coin Change (Knapsack pattern)
def coin_change(coins: List[int], amount: int) -> int:
    """Time: O(amount * len(coins)), Space: O(amount)"""
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != amount + 1 else -1

# Advanced Implementation: Longest Common Subsequence (2D DP)
def longest_common_subsequence(text1: str, text2: str) -> int:
    """Time: O(M * N), Space: O(M * N)"""
    dp = [[0] * (len(text2) + 1) for _ in range(len(text1) + 1)]
    
    for i in range(len(text1) - 1, -1, -1):
        for j in range(len(text2) - 1, -1, -1):
            if text1[i] == text2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i][j + 1], dp[i + 1][j])
                
    return dp[0][0]

# Edge Cases to Handle:
# 1. Base cases appropriately initialized.
# 2. Out of bounds checking in iterative tabulation.
# 3. Impossible combinations returning proper defaults (e.g., -1 for Coin Change).

# Interview Challenge: Longest Increasing Subsequence
def length_of_LIS(nums: List[int]) -> int:
    """Time: O(N^2) or O(N log N) with binary search. Using O(N^2) DP here."""
    LIS = [1] * len(nums)
    
    for i in range(len(nums) - 1, -1, -1):
        for j in range(i + 1, len(nums)):
            if nums[i] < nums[j]:
                LIS[i] = max(LIS[i], 1 + LIS[j])
                
    return max(LIS)

def run_tests():
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "def") == 0
    
    assert length_of_LIS([10,9,2,5,3,7,101,18]) == 4
    
    print("All Dynamic Programming tests passed!")

if __name__ == "__main__":
    run_tests()
