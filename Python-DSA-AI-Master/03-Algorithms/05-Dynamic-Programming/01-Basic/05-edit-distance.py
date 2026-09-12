"""
Edit Distance (Levenshtein Distance)
====================================

Learning Objectives:
1. Apply DP to calculate string similarity.
2. Map operations (insert, delete, replace) to state transitions.
3. Understand applications in spell checkers and NLP.

Concept Explanation:
Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.
Operations allowed: Insert, Delete, Replace.

Implementations:
- Basic: Recursive + Memoization
- Intermediate: 2D Tabulation
- Advanced: Space Optimized 1D
"""

def edit_distance_memo(word1: str, word2: str) -> int:
    """Basic: Top-down recursion with memoization."""
    memo = {}
    
    def dfs(i: int, j: int) -> int:
        if i == len(word1): return len(word2) - j
        if j == len(word2): return len(word1) - i
        if (i, j) in memo: return memo[(i, j)]
        
        if word1[i] == word2[j]:
            ans = dfs(i + 1, j + 1)
        else:
            ans = 1 + min(dfs(i + 1, j),     # Delete
                          dfs(i, j + 1),     # Insert
                          dfs(i + 1, j + 1)) # Replace
                          
        memo[(i, j)] = ans
        return ans
        
    return dfs(0, 0)

def edit_distance_tab(word1: str, word2: str) -> int:
    """Intermediate: 2D tabulation."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # Delete
                                   dp[i][j - 1],      # Insert
                                   dp[i - 1][j - 1])  # Replace
                                   
    return dp[m][n]

def edit_distance_opt(word1: str, word2: str) -> int:
    """Advanced: 1D Space Optimized."""
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2, m, n = word2, word1, n, m
        
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr[:]
        
    return prev[n]

def test_edit_distance():
    """Test functionality."""
    assert edit_distance_opt("horse", "ros") == 3
    assert edit_distance_opt("intention", "execution") == 5
    assert edit_distance_opt("", "a") == 1
    print("All tests passed.")

if __name__ == "__main__":
    print("Edit Distance DP")
    test_edit_distance()
