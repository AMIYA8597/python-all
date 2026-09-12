"""
Medium-Level Dynamic Programming Problems for Interview Preparation
===================================================================

This module covers medium-level Dynamic Programming (DP) problems. DP is a method 
for solving complex problems by breaking them down into simpler subproblems.

Topics Covered:
1. Longest Increasing Subsequence (1D DP)
2. Coin Change (1D DP)
3. Longest Common Subsequence (2D DP)
4. Word Break (1D DP / String)

Beginner Explanation:
Dynamic Programming is essentially recursion with memorization. If you find yourself 
calculating the same subproblem repeatedly, you can cache (memoize) the result.
Alternatively, you can build up the solution from the smallest subproblems to the largest 
(tabulation / bottom-up DP).

Deep Technical Explanation:
- Identifying DP Problems: 
  1. Optimal Substructure: The optimal solution can be constructed from optimal solutions of its subproblems.
  2. Overlapping Subproblems: The problem can be broken down into subproblems which are reused several times.
- Top-Down vs Bottom-Up:
  - Top-Down (Memoization): Start from the goal and recurse down, caching results. Good if not all subproblems need to be evaluated.
  - Bottom-Up (Tabulation): Start from the base cases and build up iteratively. Prevents recursion depth issues and often has better constant factors for space/time.

Real-World Use Cases:
- Sequence alignment in bioinformatics (DNA sequencing)
- Diff algorithms (used in Git) for finding longest common subsequences
- Resource allocation and combinatorial optimization
"""

from typing import List

# -----------------------------------------------------------------------------
# 1. Longest Increasing Subsequence (LIS)
# -----------------------------------------------------------------------------
"""
Problem: Given an integer array nums, return the length of the longest strictly increasing subsequence.

Approach (DP):
Let dp[i] be the length of the LIS ending at index i.
For each element i, we check all elements j before it (where j < i).
If nums[i] > nums[j], we can append nums[i] to the subsequence ending at j.
So, dp[i] = max(dp[i], dp[j] + 1)

Time Complexity: O(N^2) using standard DP. (Can be O(N log N) using Binary Search + DP).
Space Complexity: O(N)
"""

def lengthOfLIS(nums: List[int]) -> int:
    """
    Returns the length of the longest increasing subsequence in O(N^2) time.
    """
    if not nums:
        return 0
        
    # dp[i] is the length of LIS ending at index i
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)

# -----------------------------------------------------------------------------
# 2. Coin Change
# -----------------------------------------------------------------------------
"""
Problem: You are given an integer array coins representing coins of different denominations 
and an integer amount representing a total amount of money. Return the fewest number of coins 
that you need to make up that amount. If impossible, return -1.

Approach (Bottom-Up DP):
Let dp[a] be the minimum number of coins needed for amount a.
Initialize dp array with infinity, except dp[0] = 0.
For each amount from 1 to `amount`, try every coin denomination `c`.
If `a - c >= 0`, then dp[a] = min(dp[a], dp[a - c] + 1)

Time Complexity: O(Amount * len(coins))
Space Complexity: O(Amount) for the DP array.
"""

def coinChange(coins: List[int], amount: int) -> int:
    """
    Finds the minimum number of coins to make a given amount.
    """
    # Initialize DP table. amount + 1 represents 'infinity'
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    # If dp[amount] is still amount + 1, it means we couldn't form the amount
    return dp[amount] if dp[amount] != amount + 1 else -1

# -----------------------------------------------------------------------------
# 3. Longest Common Subsequence (LCS)
# -----------------------------------------------------------------------------
"""
Problem: Given two strings text1 and text2, return the length of their longest common subsequence.

Approach (2D Bottom-Up DP):
Let dp[i][j] be the length of LCS of text1[0..i-1] and text2[0..j-1].
If text1[i-1] == text2[j-1]: 
    They match, so we add 1 to the result of excluding both characters: dp[i][j] = 1 + dp[i-1][j-1]
Else:
    They don't match, we take the max of excluding character from text1 or text2: 
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

Time Complexity: O(M * N) where M, N are lengths of the strings.
Space Complexity: O(M * N) (can be optimized to O(min(M, N)) by just keeping two rows).
"""

def longestCommonSubsequence(text1: str, text2: str) -> int:
    """
    Finds the length of the longest common subsequence of two strings.
    """
    m, n = len(text1), len(text2)
    # Create an (m+1) x (n+1) grid initialized to 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]

# -----------------------------------------------------------------------------
# 4. Word Break
# -----------------------------------------------------------------------------
"""
Problem: Given a string s and a dictionary of strings wordDict, return true if s can be 
segmented into a space-separated sequence of one or more dictionary words.

Approach (Bottom-Up DP):
Let dp[i] be true if s[0...i-1] can be segmented.
Initialize dp array of size len(s) + 1 with False. dp[0] = True (empty string).
For each length `i` from 1 to len(s):
    For each `j` from 0 to i - 1:
        If dp[j] is True and s[j:i] is in wordDict:
            dp[i] = True
            Break (no need to check other j's)

Time Complexity: O(N^3) in Python due to string slicing s[j:i] taking O(N).
Space Complexity: O(N) for the DP array.
"""

def wordBreak(s: str, wordDict: List[str]) -> bool:
    """
    Determines if string s can be segmented into words from wordDict.
    """
    word_set = set(wordDict) # O(1) lookup
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True # Base case
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break # We found a valid segmentation ending at i, move to next i
                
    return dp[n]


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing Medium DP Problems...")

    # Test LIS
    print(f"LIS length: {lengthOfLIS([10,9,2,5,3,7,101,18])}") # Expected: 4
    
    # Test Coin Change
    print(f"Coin Change: {coinChange([1,2,5], 11)}") # Expected: 3
    print(f"Coin Change (impossible): {coinChange([2], 3)}") # Expected: -1
    
    # Test LCS
    print(f"LCS length: {longestCommonSubsequence('abcde', 'ace')}") # Expected: 3
    
    # Test Word Break
    print(f"Word Break: {wordBreak('leetcode', ['leet', 'code'])}") # Expected: True
    print(f"Word Break: {wordBreak('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'])}") # Expected: False
    
    print("All tests passed.")
