"""
# ==============================================================================
# LABORATORY: COIN CHANGE (THE FAILURE OF GREEDY ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of coin denominations (e.g. `[1, 3, 4]`) and a target 
# `amount` (e.g. `6`). You have an infinite supply of each coin. 
# Find the MINIMUM number of coins needed to make that amount.
#
# A junior developer will immediately use a "Greedy Algorithm". 
# The logic: "To use the fewest coins, always grab the BIGGEST coin possible!"
# So for amount=6, the greedy algorithm grabs 4. Remaining=2. Grabs 1, Grabs 1.
# Total coins used: 3 (4 + 1 + 1 = 6).
#
# But look closer. What if we just grabbed two 3s? (3 + 3 = 6).
# Total coins used: 2! 
# THE GREEDY ALGORITHM IS WRONG. It completely fails on non-standard coin sets.
#
# To guarantee the absolute optimal answer, we MUST explore every valid combination.
# Because the subproblems heavily overlap, we use Dynamic Programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Greedy fails.
# - Define the DP State: `dp[i]`.
# - Define the Transition Equation: `dp[i] = min(dp[i], dp[i - coin] + 1)`.
# - Implement Bottom-Up Tabulation.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BOTTOM-UP DYNAMIC PROGRAMMING
# ==============================================================================
def coin_change(coins: List[int], amount: int) -> int:
    """
    Time Complexity: O(amount * len(coins)).
    Space Complexity: O(amount) for the DP array.
    """
    
    # 1. STATE DEFINITION
    # `dp[i]` represents the MINIMUM number of coins required to make amount `i`.
    
    # 2. INITIALIZATION
    # We pre-fill the array with `math.inf` (Infinity) because we are looking 
    # for a MINIMUM. If we initialized with 0, `min()` would always pick 0!
    # The array size is `amount + 1` so we can easily index `dp[amount]`.
    dp = [float('inf')] * (amount + 1)
    
    # 3. BASE CASE
    # It takes exactly 0 coins to make the amount 0.
    dp[0] = 0
    
    # 4. TABULATION LOOP
    # We calculate the answer for EVERY amount from 1 up to our target.
    for curr_amount in range(1, amount + 1):
        
        # At this `curr_amount`, try using every single coin we have available.
        for coin in coins:
            
            # Can we even use this coin? (The coin can't be bigger than the amount).
            if coin <= curr_amount:
                
                # --- STATE TRANSITION EQUATION ---
                # If we use this `coin`, the remaining amount is `curr_amount - coin`.
                # We already calculated the optimal answer for that remaining amount 
                # (it is sitting in our DP array)!
                # So the cost of this path is: 1 (for this coin) + dp[remaining].
                # We update `dp[curr_amount]` if this path is smaller!
                dp[curr_amount] = min(dp[curr_amount], 1 + dp[curr_amount - coin])
                
    # 5. RETURN
    # If the target amount is still Infinity, it means it was mathematically 
    # impossible to construct that amount with the given coins!
    return int(dp[amount]) if dp[amount] != float('inf') else -1


def demonstrate_coin_change():
    section_header("Algorithm: Coin Change (DP Tabulation)")
    
    coins1 = [1, 2, 5]
    amount1 = 11
    print(f"Test 1 - Coins: {coins1}, Target: {amount1}")
    print(f"Optimal Minimum Coins: {coin_change(coins1, amount1)} (Expected: 3 -> 5+5+1)")
    
    # The trap that breaks Greedy Algorithms!
    coins2 = [1, 3, 4]
    amount2 = 6
    print(f"\nTest 2 - Coins: {coins2}, Target: {amount2}")
    print(f"Greedy would say 3 (4+1+1).")
    print(f"DP calculates: {coin_change(coins2, amount2)} (Expected: 2 -> 3+3)")
    
    # Impossible amount
    coins3 = [2]
    amount3 = 3
    print(f"\nTest 3 - Coins: {coins3}, Target: {amount3}")
    print(f"Optimal Minimum Coins: {coin_change(coins3, amount3)} (Expected: -1)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Greedy Algorithm work for US Currency, but not for `[1, 3, 4]`?
   Answer: US Currency `[1, 5, 10, 25]` forms a "Canonical Coin System". It is a mathematically proven property that for canonical systems, the Greedy Algorithm ALWAYS perfectly aligns with the DP solution. However, for arbitrary coin sets (like `[1, 3, 4]`), it is non-canonical, meaning the Greedy heuristic is mathematically wrong and DP is strictly required.

2. Why do we initialize the DP array with Infinity?
   Answer: Because our State Transition Equation uses the `min()` function. `dp = min(current_best, new_path)`. If we initialized the array with `0` (which is standard for counting problems), `min(0, 1 + dp[...])` would ALWAYS return `0`. By starting at Infinity, the very first valid path we find will overwrite the Infinity with a real number.

3. Can we Space-Optimize this from $O(Amount)$ to $O(1)$?
   Answer: NO. In Fibonacci `dp[i] = dp[i-1] + dp[i-2]`, we knew exactly how far back we had to look (exactly 1 and 2 steps). In Coin Change, `dp[i] = 1 + dp[i-coin]`. The `coin` could be 1, or it could be 50,000. Because we don't know the exact jump distances, we must keep the entire $O(Amount)$ array in RAM so we can jump backwards dynamically.
"""

if __name__ == "__main__":
    demonstrate_coin_change()
    print("\n[SUCCESS] Laboratory: Coin Change DP Completed.")
