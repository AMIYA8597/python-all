"""
# ==============================================================================
# LABORATORY: GREEDY COIN CHANGE (CANONICAL VS NON-CANONICAL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know that the "Coin Change" problem requires Dynamic Programming.
# If you have coins [1, 3, 4] and need to make 6 cents, a Greedy Algorithm will 
# take the largest coin first (4), then two 1s (4 + 1 + 1 = 3 coins).
# Dynamic Programming will correctly evaluate (3 + 3 = 2 coins).
#
# BUT WAIT! 
# In the real world, if you buy a coffee for $2.25 and hand the cashier $5.00, 
# the cashier's brain does NOT run a Dynamic Programming algorithm! 
# The cashier instantly hands you two $1 bills, two quarters, and a dime.
# 
# Why does the Cashier's Greedy Algorithm work perfectly in the real world?
# Because modern currency systems (US, Euro, Yen) are mathematically designed 
# to be "Canonical". 
# A Canonical Coin System guarantees that the Greedy Heuristic (taking the 
# largest denomination possible) will ALWAYS yield the mathematically optimal 
# minimum number of coins.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Canonical vs Non-Canonical mathematical boundaries.
# - Implement the blazing-fast O(N) Greedy Coin Change.
# - Prove why Greedy fails on arbitrary arrays.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GREEDY COIN CHANGE (O(N))
# ==============================================================================
def min_coins_greedy(coins: List[int], amount: int) -> int:
    """
    Given a sorted array of coins (descending) and an amount, 
    return the minimum number of coins using the Greedy Heuristic.
    
    Time Complexity: O(N) where N is the number of coin denominations.
                     (Technically O(1) if denominations are a fixed currency set).
    Space Complexity: O(1)
    """
    # 1. We MUST sort the coins in DESCENDING order to guarantee we try the 
    # largest denominations first!
    coins.sort(reverse=True)
    
    coin_count = 0
    current_amount = amount
    
    # 2. THE GREEDY LOOP
    for coin in coins:
        if current_amount == 0:
            break
            
        # How many of THIS specific coin can we greedily shove into the amount?
        # e.g., 275 cents // 25 cents = 11 quarters!
        num_coins = current_amount // coin
        
        if num_coins > 0:
            coin_count += num_coins
            # Subtract the value we just consumed from the remainder
            current_amount -= (num_coins * coin)
            
            print(f" -> Took {num_coins} coin(s) of denomination {coin}")
            
    # If the remaining amount is not 0, it means the coin system cannot 
    # physically make the exact change (e.g., no 1-cent coin).
    if current_amount > 0:
        return -1
        
    return coin_count


def demonstrate_canonical_systems():
    section_header("Algorithm: Greedy Coin Change (Cashier Algorithm)")
    
    # US Currency System: 1c, 5c, 10c, 25c, 100c
    us_coins = [1, 5, 10, 25, 100]
    amount = 289 # $2.89
    
    print(f"Currency System (Canonical): {us_coins}")
    print(f"Amount required: {amount} cents.\n")
    
    print("Executing O(N) Greedy Algorithm...")
    ans = min_coins_greedy(us_coins.copy(), amount)
    print(f"Total Coins: {ans} (Expected: 9)")
    
    # Let's break the currency system!
    section_header("When Greedy Fails (Non-Canonical)")
    bad_coins = [1, 3, 4]
    amount2 = 6
    
    print(f"Currency System (Non-Canonical): {bad_coins}")
    print(f"Amount required: {amount2} cents.\n")
    
    ans2 = min_coins_greedy(bad_coins.copy(), amount2)
    print(f"Greedy Total Coins: {ans2} (It picked 4, 1, 1).")
    print("DP Total Coins: 2 (It would pick 3, 3).")
    print("The Greedy algorithm failed catastrophically!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What exactly makes a coin system "Canonical"?
   Answer: A coin system is definitively Canonical if, for every possible amount $X$, the Greedy algorithm produces the exact same minimum number of coins as the Dynamic Programming algorithm. Mathematically, a system like $[1, C, C^2, C^3]$ (where each coin is a multiple of the previous) is always canonical. The US system ($1, 5, 10, 25$) is canonical, even though 25 is not a multiple of 10, due to a specific mathematical theorem (Pearson's theorem).

2. Why is the Cashier's Greedy algorithm $O(N)$ instead of the DP's $O(N \\times Amount)$?
   Answer: DP has to literally iterate through every single integer from $0$ up to $Amount$, checking the optimal state for each sub-penny. The Greedy algorithm uses integer division `amount // coin`, which allows it to skip the sub-amounts entirely and instantly lock in the maximum possible count of that denomination in a single $O(1)$ CPU cycle. It just evaluates the 4 or 5 denominations in the array, making it $O(N)$.

3. If an interviewer gives you a random array of coins like `[1, 7, 10]`, which algorithm should you write?
   Answer: You MUST write the Dynamic Programming solution. Unless the interviewer explicitly states "This is a standard currency system" or "Assume the greedy choice property holds", you cannot trust an arbitrary array to be canonical. (For `[1, 7, 10]` and target `14`, Greedy gives `10+1+1+1+1 = 5` coins. DP correctly gives `7+7 = 2` coins).
"""

if __name__ == "__main__":
    demonstrate_canonical_systems()
    print("\n[SUCCESS] Laboratory: Greedy Coin Change Completed.")
