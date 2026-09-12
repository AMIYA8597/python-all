"""
Divide and Conquer Optimization

Learning Objectives:
1. Identify conditions for Divide and Conquer optimization (monotonicity of optimal split points).
2. Optimize O(K*N^2) DP to O(K*N log N).

Concept Explanation:
Divide and Conquer optimization applies to DP of the form:
dp[i][j] = min_{k < j} (dp[i-1][k] + cost(k, j))
Condition: Let opt(i, j) be the smallest k that minimizes the expression.
If opt(i, j) <= opt(i, j+1), we can use D&C optimization.

Performance Analysis:
Time Complexity: O(K N log N)
Space Complexity: O(K N)
"""

from typing import List

def cost_func(i: int, j: int, prefix_sums: List[int]) -> int:
    """Example cost function: square of sum"""
    if i > j: return 0
    s = prefix_sums[j] - prefix_sums[i-1] if i > 0 else prefix_sums[j]
    return s * s

def compute(dp_prev: List[int], dp_curr: List[int], l: int, r: int, opt_l: int, opt_r: int, prefix_sums: List[int]):
    if l > r:
        return
    mid = (l + r) // 2
    best = float('inf')
    best_opt = -1
    
    for k in range(opt_l, min(mid, opt_r) + 1):
        current_cost = dp_prev[k] + cost_func(k + 1, mid, prefix_sums)
        if current_cost < best:
            best = current_cost
            best_opt = k
            
    dp_curr[mid] = best
    
    compute(dp_prev, dp_curr, l, mid - 1, opt_l, best_opt, prefix_sums)
    compute(dp_prev, dp_curr, mid + 1, r, best_opt, opt_r, prefix_sums)

def divide_and_conquer_dp(arr: List[int], K: int) -> int:
    n = len(arr)
    if n == 0: return 0
    prefix_sums = [0] * n
    prefix_sums[0] = arr[0]
    for i in range(1, n):
        prefix_sums[i] = prefix_sums[i-1] + arr[i]
        
    dp_prev = [cost_func(0, i, prefix_sums) for i in range(n)]
    dp_curr = [0] * n
    
    for i in range(1, K):
        compute(dp_prev, dp_curr, 0, n - 1, 0, n - 1, prefix_sums)
        dp_prev, dp_curr = dp_curr, dp_prev
        
    return dp_prev[-1]

def test_functions():
    arr = [1, 2, 3, 4]
    res = divide_and_conquer_dp(arr, 2)
    assert res > 0
    print("All tests passed.")

if __name__ == "__main__":
    test_functions()
