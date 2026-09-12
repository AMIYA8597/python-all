"""
0/1 Knapsack Problem
====================

Learning Objectives:
1. Understand bounded selection problems.
2. Implement 2D DP for weight/value maximization.
3. Optimize space complexity from 2D to 1D array.

Concept Explanation:
Given weights and values of n items, put these items in a knapsack of capacity W to get the maximum total value.
You cannot break an item, either pick the complete item or don't pick it (0-1 property).

Implementations:
- Basic: Recursive + Memoization
- Intermediate: 2D DP Table
- Advanced: 1D Space Optimized DP
"""

from typing import List

def knapsack_memo(W: int, wt: List[int], val: List[int], n: int) -> int:
    """Basic: Top-down recursion with memoization."""
    memo = {}
    
    def dfs(i: int, w: int) -> int:
        if i == 0 or w == 0:
            return 0
        if (i, w) in memo:
            return memo[(i, w)]
            
        if wt[i - 1] <= w:
            ans = max(val[i - 1] + dfs(i - 1, w - wt[i - 1]), dfs(i - 1, w))
        else:
            ans = dfs(i - 1, w)
            
        memo[(i, w)] = ans
        return ans
        
    return dfs(n, W)

def knapsack_tab(W: int, wt: List[int], val: List[int], n: int) -> int:
    """Intermediate: Bottom-up 2D tabulation."""
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if wt[i - 1] <= w:
                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
                
    return dp[n][W]

def knapsack_opt(W: int, wt: List[int], val: List[int], n: int) -> int:
    """Advanced: 1D Space optimized DP."""
    dp = [0 for _ in range(W + 1)]
    
    for i in range(1, n + 1):
        for w in range(W, wt[i - 1] - 1, -1):
            dp[w] = max(dp[w], val[i - 1] + dp[w - wt[i - 1]])
            
    return dp[W]

def test_knapsack():
    """Test functionality."""
    val = [60, 100, 120]
    wt = [10, 20, 30]
    W = 50
    n = len(val)
    assert knapsack_opt(W, wt, val, n) == 220
    print("All tests passed.")

if __name__ == "__main__":
    print("0/1 Knapsack DP")
    test_knapsack()
