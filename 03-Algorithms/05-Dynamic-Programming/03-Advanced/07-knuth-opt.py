"""
# ==============================================================================
# LABORATORY: KNUTH OPTIMIZATION (INTERVAL DP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned Interval DP when solving "Matrix Chain Multiplication".
# We looped over `length`, then `i` (start), then `j` (end), and finally we 
# searched for a partition point `k` between `i` and `j`. 
# Three nested loops = O(N^3) Time.
#
# In 1971, Donald Knuth (the legendary author of "The Art of Computer Programming") 
# proved a mathematical theorem while solving the "Optimal Binary Search Tree" problem.
#
# He proved that if the `cost` function satisfies the Quadrangle Inequality, 
# then the optimal partition point `opt(i, j)` is strictly bounded by the 
# optimal partition points of the smaller intervals inside it!
#
# Specifically: opt(i, j-1) <= opt(i, j) <= opt(i+1, j)
#
# This means we do NOT need to loop `k` from `i` to `j-1`! 
# We only loop `k` from `opt[i][j-1]` to `opt[i+1][j]`.
# 
# While this looks like it just makes the inner loop slightly smaller, the math 
# is truly magical: The sum of the sizes of these restricted windows across the 
# entire DP table perfectly telescopes. The inner loop amortizes to O(1) average 
# time. The O(N^3) algorithm collapses into O(N^2)!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Knuth Bound: `opt[i][j-1] <= k <= opt[i+1][j]`.
# - Implement the `opt` 2D matrix to track optimal splits.
# - Apply it to an Optimal BST or Minimum Cost Tree problem.
#
# ==============================================================================
"""

import sys
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. INTERVAL DP WITH KNUTH OPTIMIZATION
# ==============================================================================
def cost(i: int, j: int, prefix_sums: List[int]) -> int:
    """
    Standard cost function for 'Minimum Cost to merge items i to j'.
    Usually defined as the sum of all elements in the interval [i, j].
    Calculated in O(1) using a Prefix Sum array.
    """
    if i == 0:
        return prefix_sums[j]
    return prefix_sums[j] - prefix_sums[i - 1]


def solve_optimal_bst_knuth(freqs: List[int]) -> int:
    """
    Problem: Combine items into a Binary Search Tree such that the total cost 
    (depth * frequency) is minimized. Identical logic to "Merge Stones".
    
    Time Complexity: O(N^2) (Down from O(N^3)!)
    Space Complexity: O(N^2)
    """
    n = len(freqs)
    if n == 0: return 0
    
    # 1. PRE-CALCULATE PREFIX SUMS FOR O(1) COST QUERIES
    prefix_sums = [0] * n
    prefix_sums[0] = freqs[0]
    for i in range(1, n):
        prefix_sums[i] = prefix_sums[i - 1] + freqs[i]
        
    # 2. DP AND OPT TABLES
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # `opt[i][j]` stores the EXACT index `k` that yielded the minimum cost for dp[i][j].
    opt = [[0 for _ in range(n)] for _ in range(n)]
    
    # 3. BASE CASES (Length = 1)
    # Merging an interval of size 1 costs 0 (it's already merged).
    # The optimal split point for an interval of size 1 is just its own index.
    for i in range(n):
        dp[i][i] = 0
        opt[i][i] = i
        
    # 4. INTERVAL DP LOOP (Loop by Length)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            dp[i][j] = sys.maxsize
            
            # --- KNUTH OPTIMIZATION BOUNDS ---
            # Instead of `for k in range(i, j):`, we use the magical bounds!
            # The optimal K must lie between the optimal K of the interval WITHOUT 
            # the rightmost element, and the interval WITHOUT the leftmost element!
            
            left_bound = opt[i][j - 1]
            right_bound = opt[i + 1][j]
            
            # We must use `right_bound + 1` in the range because `k` can potentially 
            # be `j-1`, but NEVER `j` (you can't split an array after the last element).
            # We take `min(right_bound + 1, j)` to prevent out of bounds.
            for k in range(left_bound, min(right_bound + 1, j)):
                
                # State Transition: Left Subtree + Right Subtree + Cost of merging them.
                current_cost = dp[i][k] + dp[k + 1][j] + cost(i, j, prefix_sums)
                
                if current_cost < dp[i][j]:
                    dp[i][j] = current_cost
                    # Save the optimal K into the OPT table so future, larger intervals 
                    # can use it for their Knuth bounds!
                    opt[i][j] = k
                    
    # The final answer is the interval from 0 to N-1
    return dp[0][n - 1]


def demonstrate_knuth():
    section_header("Algorithm: Knuth Optimization (O(N^2) Interval DP)")
    
    freqs = [3, 4, 2, 1, 3, 6, 9]
    print(f"Frequencies (Costs): {freqs}")
    print(f"N = {len(freqs)}")
    
    print("\nExecuting Knuth Optimized Interval DP...")
    ans = solve_optimal_bst_knuth(freqs)
    
    print(f"Minimum Cost to merge: {ans}")
    print("Without Knuth Optimization, the inner `k` loop would execute N^3 times.")
    print("With the bounds `opt[i][j-1] <= k <= opt[i+1][j]`, the `k` loop amortizes")
    print("to strictly O(1) on average across the entire grid!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How exactly does the Knuth Bound `opt[i][j-1] <= k <= opt[i+1][j]` amortize to $O(N^2)$?
   Answer: Imagine evaluating all intervals of length $L$. The number of iterations for the inner $k$ loop across the entire diagonal is: 
   $\\sum_{i=1}^{N-L+1} [opt(i+1, i+L-1) - opt(i, i+L-2)]$. 
   Notice how this is a Telescoping Sum! Almost every term cancels out with the adjacent interval. The total number of iterations for the ENTIRE diagonal collapses to $opt(N-L+2, N) - opt(1, L-1)$, which is strictly bounded by $N$. Since there are $N$ diagonals, the total time is $O(N \\times N) = O(N^2)$!

2. Does Knuth Optimization work on Matrix Chain Multiplication?
   Answer: NO. This is a massive trap. Matrix Chain Multiplication does NOT satisfy the necessary mathematical properties (specifically, the Monotonicity of the optimal split point on the 2D grid). Knuth Optimization only works on problems like Optimal Binary Search Tree or Merge Stones, where the Cost Function strictly satisfies the Quadrangle Inequality and Monotonicity.

3. Why do we need `opt[i][i] = i` in the Base Cases?
   Answer: Because when we evaluate length 2 ($i$ and $i+1$), the Knuth loop bounds are `opt[i][j-1]` which maps to `opt[i][i]`, and `opt[i+1][j]` which maps to `opt[i+1][i+1]`. If these base cases are not initialized to their own indices, the bounds will read $0$, and the $k$ loop will completely break, generating wrong answers for the rest of the matrix.
"""

if __name__ == "__main__":
    demonstrate_knuth()
    print("\n[SUCCESS] Laboratory: Knuth Optimization Completed.")
