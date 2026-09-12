"""
Longest Common Subsequence (LCS)
================================

Learning Objectives:
1. Apply DP to sequence alignment problems.
2. Master 2D DP table construction.
3. Reconstruct the optimal solution from a DP table.

Concept Explanation:
Given two strings text1 and text2, return the length of their longest common subsequence.

Implementations:
- Basic: Recursive with memoization
- Intermediate: 2D array tabulation
- Advanced: Space-optimized 1D array
"""

from typing import List

def lcs_memo(text1: str, text2: str) -> int:
    """Basic: Top-down recursion with memoization."""
    memo = {}
    
    def dfs(i: int, j: int) -> int:
        if i == len(text1) or j == len(text2):
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
            
        if text1[i] == text2[j]:
            ans = 1 + dfs(i + 1, j + 1)
        else:
            ans = max(dfs(i + 1, j), dfs(i, j + 1))
            
        memo[(i, j)] = ans
        return ans
        
    return dfs(0, 0)

def lcs_tab(text1: str, text2: str) -> int:
    """Intermediate: 2D Tabulation."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]

def lcs_opt(text1: str, text2: str) -> int:
    """Advanced: Space optimized."""
    m, n = len(text1), len(text2)
    if m < n:
        text1, text2, m, n = text2, text1, n, m
        
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr[:]
        
    return prev[n]

def test_lcs():
    """Test typical cases."""
    assert lcs_opt("abcde", "ace") == 3
    assert lcs_opt("abc", "abc") == 3
    assert lcs_opt("abc", "def") == 0
    print("All tests passed.")

if __name__ == "__main__":
    print("LCS DP")
    test_lcs()
