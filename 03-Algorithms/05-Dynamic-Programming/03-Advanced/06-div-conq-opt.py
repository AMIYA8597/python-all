"""
# ==============================================================================
# LABORATORY: DIVIDE & CONQUER DP OPTIMIZATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Divide & Conquer DP is another legendary optimization technique (like the 
# Convex Hull Trick), used to shatter O(N^3) or O(N^2) time limits down to 
# O(N^2 log N) or O(N log N).
#
# It applies when your DP state transition looks like this:
# dp[i][j] = min( dp[i-1][k] + cost(k, j) ) for all k < j
#
# Normally, to fill row `i`, you loop `j` from 1 to N. For every `j`, you loop 
# `k` from 1 to `j`. That's an O(N^2) transition per row!
#
# But what if the optimal split point `k` (let's call it `opt(i, j)`) is Monotonic?
# Monotonicity means: as `j` moves to the right, the optimal `k` MUST ALSO move 
# to the right (or stay the same). 
# Mathematically: opt(i, j) <= opt(i, j+1)
#
# If this is true, we don't need to loop `k` from 1 to `j` every time!
# If we calculate the middle element `j_mid`, and find its optimal split is `k_mid`, 
# we instantly know that all `j < j_mid` MUST have their `k <= k_mid`, and all 
# `j > j_mid` MUST have their `k >= k_mid`.
# We can use Divide and Conquer to recursively split the search space in half, 
# dropping the inner loops from O(N^2) to O(N log N)!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Optimal Split Monotonicity.
# - Implement the `compute(L, R, optL, optR)` recursive engine.
# - Understand how this reduces the `k` search space.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DIVIDE & CONQUER ENGINE
# ==============================================================================

# A theoretical `cost` function. 
# For D&C Optimization to work, this cost function MUST satisfy the 
# "Quadrangle Inequality". (Usually related to placing K post offices among 
# N villages, or splitting an array into K groups to minimize variance).
def cost(k: int, j: int) -> int:
    """Mock cost function for demonstration."""
    # The cost of grouping items from index `k` to `j`.
    # (In a real problem, this is calculated using Prefix Sums in O(1) time).
    return (j - k) ** 2


def divide_and_conquer_dp_layer(
    dp_prev: List[float], 
    dp_curr: List[float], 
    L: int, 
    R: int, 
    optL: int, 
    optR: int
):
    """
    Computes a single ROW (layer `i`) of the DP table using the previous ROW (`i-1`).
    Instead of looping L to R, we recursively divide and conquer the row.
    
    `L`, `R`: The range of `j` we are currently calculating for `dp_curr`.
    `optL`, `optR`: The known bounds for the optimal `k` search space!
    """
    if L > R:
        return
        
    # 1. Find the MIDDLE element of the current `j` range.
    mid_j = (L + R) // 2
    
    best_cost = math.inf
    best_k = -1
    
    # 2. Search for the optimal `k`, BUT we only search between optL and optR!
    # We do NOT search from 0 to mid_j. The bounds have been narrowed!
    
    # We must ensure k doesn't exceed mid_j (can't split after the interval ends).
    search_upper_bound = min(mid_j, optR)
    
    for k in range(optL, search_upper_bound + 1):
        
        # --- STATE TRANSITION ---
        current_cost = dp_prev[k] + cost(k, mid_j)
        
        if current_cost < best_cost:
            best_cost = current_cost
            best_k = k
            
    # 3. Store the optimal answer for `mid_j`
    dp_curr[mid_j] = best_cost
    
    # 4. DIVIDE AND CONQUER!
    # Because of Monotonicity, we know the optimal `k` for the LEFT half of `j` 
    # must be less than or equal to `best_k`.
    divide_and_conquer_dp_layer(dp_prev, dp_curr, L, mid_j - 1, optL, best_k)
    
    # We know the optimal `k` for the RIGHT half of `j` must be greater than 
    # or equal to `best_k`.
    divide_and_conquer_dp_layer(dp_prev, dp_curr, mid_j + 1, R, best_k, optR)


def demonstrate_div_conq():
    section_header("Algorithm: Divide & Conquer DP")
    
    n = 8
    # Suppose we are at Layer 1 (e.g. 1 group), and want to calculate Layer 2.
    # dp_prev represents the costs at Layer 1.
    dp_prev = [math.inf] + [cost(0, x) for x in range(1, n + 1)]
    dp_curr = [0.0] * (n + 1)
    
    print(f"Array Size: {n}")
    print(f"Previous DP Layer: {[round(x, 1) for x in dp_prev[1:]]}")
    
    print("\nExecuting Divide & Conquer DP layer computation...")
    # Compute dp_curr for j in range [1, N], knowing the optimal k is in [0, N].
    divide_and_conquer_dp_layer(dp_prev, dp_curr, 1, n, 0, n)
    
    print(f"Current DP Layer:  {[round(x, 1) for x in dp_curr[1:]]}")
    print("\nThe execution split the array in half recursively, restricting the `k` ")
    print("search bounds for the left and right sides independently in O(N log N) time!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the "Quadrangle Inequality"?
   Answer: It is the mathematical proof required to use this optimization. It states: $Cost(a, c) + Cost(b, d) \\le Cost(a, d) + Cost(b, c)$ for $a \\le b \\le c \\le d$. If the cost function satisfies this (like grouping elements on a 1D line to minimize distance to a post office), it guarantees that the optimal split points $opt(i, j)$ are monotonically increasing!

2. How much does this optimize the time complexity?
   Answer: Without D&C, calculating row $i$ takes $O(N^2)$ because you loop $j$ from $1$ to $N$, and $k$ from $1$ to $j$. With D&C, the recursion tree has a depth of $\\log N$. At each depth level, the summation of all the `for k in range(optL, optR)` loops across all nodes on that level is mathematically bounded by $O(N)$. Therefore, calculating a row drops perfectly to $O(N \\log N)$.

3. Is this an iterative or recursive optimization?
   Answer: The outer loop (looping through the rows/layers `i` from $1$ to $K$) is Iterative. But the inner calculation of the row itself `divide_and_conquer_dp_layer()` is purely Recursive.
"""

if __name__ == "__main__":
    demonstrate_div_conq()
    print("\n[SUCCESS] Laboratory: Divide & Conquer DP Completed.")
