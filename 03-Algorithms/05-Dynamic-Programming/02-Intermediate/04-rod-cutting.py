"""
# ==============================================================================
# LABORATORY: ROD CUTTING (UNBOUNDED KNAPSACK MAXIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You own a lumber yard. You have a long rod of wood of length N.
# You can sell the entire rod as one piece, or you can cut it into smaller 
# pieces. You have a price sheet that tells you exactly how much money a piece 
# of length `L` sells for.
# How do you cut the rod to maximize your total profit?
#
# E.g. Rod Length: 8
# Prices: [1, 5, 8, 9, 10, 17, 17, 20] (Index+1 is the length).
# If you sell it as one piece of length 8, you make $20.
# If you cut it into two pieces of length 2 and 6, you make $5 + $17 = $22.
#
# Mathematically, this is the "Unbounded Knapsack" problem. 
# It is identical to Coin Change, but instead of finding the MINIMUM coins, 
# we want to find the MAXIMUM profit. And just like Coin Change, we can reuse 
# the same piece length infinitely (you can cut a length 8 rod into eight 
# length 1 pieces).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Unbounded Knapsack (Infinite reuse of items).
# - Master 1D Array Tabulation with the FORWARD loop.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 1D TABULATION (O(N^2))
# ==============================================================================
def cut_rod(prices: List[int], n: int) -> int:
    """
    Time Complexity: O(N^2) (We calculate DP for N lengths, and at each length, 
                             we iterate through all possible cuts up to that length).
    Space Complexity: O(N) for the DP array.
    """
    
    # 1. STATE DEFINITION
    # `dp[i]` represents the MAXIMUM PROFIT achievable from a rod of length `i`.
    
    # 2. INITIALIZATION
    # Array of size N+1.
    # A rod of length 0 yields $0 profit.
    dp = [0] * (n + 1)
    
    # 3. TABULATION LOOP
    # We calculate the absolute best profit for a rod of length 1, then length 2, 
    # all the way up to length N.
    for i in range(1, n + 1):
        
        max_profit = -1
        
        # At this current rod length `i`, we try making a FIRST CUT of every 
        # possible size `j` (from 1 up to `i`).
        for j in range(1, i + 1):
            
            # --- STATE TRANSITION EQUATION ---
            # If we make a cut of length `j`, we sell that piece for `prices[j-1]`.
            # (Remember `prices` is 0-indexed, so length 1 is at index 0).
            # The REMAINING rod has length `i - j`.
            # We already calculated the maximum optimal profit for that remaining 
            # rod length, and it is stored in `dp[i - j]`.
            
            current_profit = prices[j - 1] + dp[i - j]
            
            if current_profit > max_profit:
                max_profit = current_profit
                
        # Store the absolute best profit for this length `i`
        dp[i] = max_profit
        
    return dp[n]


def demonstrate_rod_cutting():
    section_header("Algorithm: Rod Cutting")
    
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    n = 8
    
    print(f"Rod Length: {n}")
    print(f"Price Table:")
    for length, price in enumerate(prices):
        print(f" Length {length + 1}: ${price}")
        
    print("\nExecuting Unbounded Knapsack DP...")
    ans = cut_rod(prices, n)
    
    print(f"Maximum Profit: ${ans} (Expected: 22)")
    print("Optimal Strategy: Cut into pieces of Length 2 ($5) and Length 6 ($17).")
    
    
    prices2 = [3, 5, 8, 9, 10, 17, 17, 20]
    print(f"\nModified Price Table. Length 1 now sells for $3!")
    ans2 = cut_rod(prices2, n)
    print(f"Maximum Profit: ${ans2} (Expected: 24)")
    print("Optimal Strategy: Cut into eight pieces of Length 1 ($3 * 8 = 24).")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the inner loop `for j in range(1, i+1)` enforce the "Unbounded/Infinite Reuse" rule?
   Answer: Because we are reading from `dp[i - j]`. The value in `dp[i - j]` was calculated EARLIER in the exact same `dp` array. That previous answer might have already used a piece of length `j`. By adding `prices[j-1]` to it, we are mathematically using the piece `j` multiple times! (Unlike 0/1 Knapsack where we read from a frozen 2D row to strictly prevent reuse).

2. How do you print the actual CUTS made, instead of just the maximum profit number?
   Answer: You need a secondary array, just like in Matrix Chain Multiplication. Create `cuts = [0] * (n + 1)`. Inside the `if current_profit > max_profit:` block, record the cut: `cuts[i] = j`. After the function finishes, trace backwards: start at `n`, the first cut is `cuts[n]`. Then look at `cuts[n - cuts[n]]`, and so on until you reach 0.

3. If the Time Complexity is $O(N^2)$, what happens if the rod length is 1 Billion?
   Answer: The DP approach crashes. If the length is massive, you must use the "Greedy Value/Weight Density" approach. You calculate the Density of each piece (e.g. Length 2 for $5 is 2.5/unit). You greedily cut the rod entirely into the highest density piece until the remainder is small enough to run DP on.
"""

if __name__ == "__main__":
    demonstrate_rod_cutting()
    print("\n[SUCCESS] Laboratory: Rod Cutting Completed.")
