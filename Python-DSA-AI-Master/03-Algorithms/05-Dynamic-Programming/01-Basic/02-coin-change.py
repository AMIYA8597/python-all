"""
Coin Change Problem - Dynamic Programming
=========================================

Learning Objectives:
1. Understand unbounded knapsack problems.
2. Learn how to build up a DP array iteratively.
3. Handle cases where no solution exists.

Concept Explanation:
Given a set of coin denominations and a total amount, find the minimum number of coins needed.
If it's not possible, return -1.

Implementations:
- Basic: Recursion with memoization
- Intermediate: Tabulation
- Advanced: Finding all combinations (similar variant)
"""

from typing import List, Dict

def coin_change_memo(coins: List[int], amount: int) -> int:
    """Basic: Top-down with memoization."""
    memo: Dict[int, int] = {}
    
    def dfs(rem: int) -> int:
        if rem < 0: return -1
        if rem == 0: return 0
        if rem in memo: return memo[rem]
        
        min_coins = float('inf')
        for coin in coins:
            res = dfs(rem - coin)
            if res >= 0 and res < min_coins:
                min_coins = 1 + res
                
        memo[rem] = min_coins if min_coins != float('inf') else -1
        return memo[rem]
        
    return dfs(amount)

def coin_change_tab(coins: List[int], amount: int) -> int:
    """Intermediate: Bottom-up tabulation."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins: List[int], amount: int) -> int:
    """Advanced: Find number of combinations that make up that amount."""
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
            
    return dp[amount]

def test_coin_change():
    """Test edge cases and standard cases."""
    assert coin_change_tab([1, 2, 5], 11) == 3
    assert coin_change_tab([2], 3) == -1
    assert coin_change_tab([1], 0) == 0
    print("All tests passed.")

if __name__ == "__main__":
    print("Coin Change DP")
    test_coin_change()
