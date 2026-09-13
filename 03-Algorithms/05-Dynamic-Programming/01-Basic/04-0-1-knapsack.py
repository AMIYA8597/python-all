"""
# ==============================================================================
# LABORATORY: 0/1 KNAPSACK PROBLEM (NP-HARD PSEUDO-POLYNOMIAL DP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are a thief in a jewelry store. Your backpack (Knapsack) can only hold a 
# maximum of `W` pounds. There are `N` items in the store, each with a specific 
# Weight and a specific Value (e.g. Gold: 10 lbs, $50,000. Silver: 2 lbs, $3,000).
# Which items do you steal to maximize your total profit?
#
# This is the 0/1 Knapsack Problem. "0/1" means you must either steal the ENTIRE 
# item (1), or leave it (0). You cannot break a diamond in half and take 50% of it. 
# (If you could take fractions, you would just use a simple Greedy algorithm!).
#
# Mathematically, this problem is NP-Hard. There is no known fast algorithm that 
# solves it perfectly in true Polynomial time. 
# However, Dynamic Programming solves it in "Pseudo-Polynomial" time: O(N * W). 
# If the maximum weight of the backpack (W) is a small, reasonable number, the 
# algorithm runs instantly. If W is 10 Billion, the algorithm crashes because it 
# tries to build an array of size 10 Billion.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Pseudo-Polynomial Time vs True Polynomial Time.
# - Master the 0/1 Knapsack State Transition (Include vs Exclude).
# - Implement 2D Tabulation.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 0/1 KNAPSACK (2D TABULATION)
# ==============================================================================
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Time Complexity: O(N * W) where N is number of items, W is the capacity.
    Space Complexity: O(N * W) for the 2D DP matrix.
    """
    n = len(weights)
    
    # 1. STATE DEFINITION
    # `dp[i][w]` represents the Maximum Value we can achieve using ONLY the 
    # first `i` items, given a backpack capacity of exactly `w`.
    
    # 2. INITIALIZATION
    # Matrix of size (N+1) x (W+1).
    # Row 0 represents having 0 items available to steal. Max profit is always $0.
    # Col 0 represents a backpack with 0 capacity. Max profit is always $0.
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # 3. TABULATION LOOP
    # Loop through every item (1 to N)
    for i in range(1, n + 1):
        
        # Extract the weight and value of the CURRENT item we are considering.
        # (Remember 0-indexing for the input arrays).
        curr_weight = weights[i - 1]
        curr_value = values[i - 1]
        
        # Loop through every possible backpack capacity (1 to W)
        for w in range(1, capacity + 1):
            
            # --- STATE TRANSITION EQUATION ---
            
            # Option 1: EXCLUDE THE ITEM.
            # We skip this item. Our profit is whatever the max profit was for 
            # this exact capacity using the PREVIOUS items (Look UP one row).
            exclude_profit = dp[i - 1][w]
            
            # Option 2: INCLUDE THE ITEM.
            # Can we even fit it?
            if curr_weight <= w:
                # We steal it! We gain `curr_value`. 
                # But we just consumed `curr_weight` capacity from our backpack!
                # We must look up the best profit we got from the PREVIOUS items 
                # using the REMAINING capacity: `w - curr_weight`.
                include_profit = curr_value + dp[i - 1][w - curr_weight]
                
                # Take whichever option yielded more money!
                dp[i][w] = max(exclude_profit, include_profit)
                
            else:
                # The item is too heavy. We are FORCED to exclude it.
                dp[i][w] = exclude_profit
                
    # The absolute max profit using ALL items and FULL capacity is at the bottom right.
    return dp[n][capacity]


def demonstrate_knapsack():
    section_header("Algorithm: 0/1 Knapsack")
    
    # Example: 3 items available.
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    
    print(f"Items available: {len(weights)}")
    print("Item 1: 10 lbs, $60")
    print("Item 2: 20 lbs, $100")
    print("Item 3: 30 lbs, $120")
    print(f"Backpack Capacity: {capacity} lbs\n")
    
    # Note: A Greedy algorithm (Value/Weight ratio) would take:
    # Item 1 (Ratio 6) -> 10 lbs
    # Item 2 (Ratio 5) -> 20 lbs
    # Remaining capacity: 20 lbs. Item 3 (30 lbs) doesn't fit. 
    # Greedy total: $160.
    
    # But DP calculates:
    # Item 2 (20 lbs) + Item 3 (30 lbs) = 50 lbs exactly. 
    # Total: $100 + $120 = $220!
    
    ans = knapsack(weights, values, capacity)
    print(f"Optimal Max Profit calculated by DP: ${ans}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is it called "Pseudo-Polynomial" Time?
   Answer: The Time Complexity is $O(N \\times W)$. $N$ is the number of items. $W$ is the maximum weight capacity. This looks like a polynomial equation. BUT $W$ is not the "size of the input". If you pass the number `1,000,000` as the capacity, it only takes 32 bits (4 bytes) to represent that number in the computer's memory. But the algorithm will literally loop 1 Million times! The runtime is exponential relative to the physical binary size of the input, making it technically NP-Hard, even though it runs fast for small numbers.

2. Can we space-optimize this to a 1D array?
   Answer: Yes! Notice that row `i` only ever reads data from row `i-1`. You can squash the matrix into a single 1D array of size `W`. However, there is a massive trap: When iterating through the capacities `w`, you MUST iterate BACKWARDS (from `capacity` down to `0`). If you iterate forwards, you will accidentally overwrite the `i-1` values before you finish reading them, and mathematically turn the algorithm into the "Unbounded Knapsack" (Coin Change) problem where items can be used infinitely!
"""

if __name__ == "__main__":
    demonstrate_knapsack()
    print("\n[SUCCESS] Laboratory: 0/1 Knapsack Completed.")
