\"\"\"
Knuth Optimization in Dynamic Programming
=========================================

1. Introduction & Why it Exists:
--------------------------------
Knuth Optimization is an advanced Dynamic Programming (DP) technique introduced by 
Donald Knuth. It is used to optimize DP problems that transition over intervals, 
typically reducing the time complexity from O(N^3) to O(N^2).
It applies when the DP state transitions involve an optimal splitting point `k`
between an interval `[i, j]`.

2. Learning Objectives:
-----------------------
- Understand the criteria for applying Knuth Optimization (Monge property).
- Learn how to track optimal split points.
- Implement Knuth Optimization for the Optimal Binary Search Tree (OBST) or 
  similar interval DP problems.
- Analyze time and space complexity improvements.

3. Concept Explanation:
-----------------------
Typical interval DP recurrence:
DP[i][j] = min(DP[i][k] + DP[k+1][j] + Cost(i, j)) for i <= k < j

If the Cost function satisfies:
1. Quadrangle inequality (Monge property): 
   Cost(a, c) + Cost(b, d) <= Cost(a, d) + Cost(b, c) for a <= b <= c <= d
2. Monotonicity: 
   Cost(b, c) <= Cost(a, d) for a <= b <= c <= d

Then the optimal split point `K[i][j]` (the `k` that minimizes DP[i][j]) satisfies:
K[i][j-1] <= K[i][j] <= K[i+1][j]

This reduces the search space for `k` from `O(N)` to `K[i+1][j] - K[i][j-1]`, leading 
to an amortized `O(1)` per state, reducing total time to `O(N^2)`.
\"\"\"

from typing import List, Tuple
import sys

def optimal_bst_naive(keys: List[int], freq: List[int]) -> int:
    \"\"\"
    Naive O(N^3) solution for Optimal Binary Search Tree.
    \"\"\"
    n = len(keys)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    # Prefix sums for quick cost calculations
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + freq[i]
        
    def cost(i: int, j: int) -> int:
        return prefix[j] - prefix[i]

    # Length of interval
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            dp[i][j] = sys.maxsize
            # Try all roots
            for r in range(i, j):
                c = dp[i][r] + dp[r+1][j] + cost(i, j)
                if c < dp[i][j]:
                    dp[i][j] = c
                    
    return dp[0][n]


def optimal_bst_knuth(keys: List[int], freq: List[int]) -> int:
    \"\"\"
    Optimized O(N^2) solution using Knuth Optimization.
    \"\"\"
    n = len(keys)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    opt = [[0] * (n + 1) for _ in range(n + 1)]
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + freq[i]
        
    def cost(i: int, j: int) -> int:
        return prefix[j] - prefix[i]

    # Base cases: length 1
    for i in range(n):
        dp[i][i+1] = freq[i]
        opt[i][i+1] = i

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            dp[i][j] = sys.maxsize
            
            # Knuth optimization: restrict search space
            left = opt[i][j-1]
            right = opt[i+1][j] if i + 1 < n and j <= n and opt[i+1][j] != 0 else j - 1
            
            # Ensure right does not exceed j-1
            right = min(right, j - 1)

            for r in range(left, right + 1):
                c = dp[i][r] + dp[r+1][j] + cost(i, j)
                if c < dp[i][j]:
                    dp[i][j] = c
                    opt[i][j] = r
                    
    return dp[0][n]


if __name__ == \"__main__\":
    # Simple tests
    keys = [10, 12, 20]
    freq = [34, 8, 50]
    
    res_naive = optimal_bst_naive(keys, freq)
    res_knuth = optimal_bst_knuth(keys, freq)
    
    assert res_naive == res_knuth, \"Mismatch between naive and optimized!\"
    print(f\"Naive: {res_naive}, Knuth: {res_knuth}\")
    print(\"All assertions passed for Knuth Optimization.\")
