"""
Minimum Coins Problem (Greedy approach)

Learning Objectives:
1. Understand when greedy algorithms work for coin change.
2. Implement greedy strategy to find minimum coins.
3. Recognize the limitations of greedy strategy for arbitrary coin systems.

Concept Explanation:
Given a value V and an infinite supply of coins of various denominations, the goal is to make change 
for V using the minimum number of coins.
The greedy strategy is to always pick the largest denomination coin that is smaller than or equal to 
the remaining value.
Note: This greedy strategy works for canonical coin systems (like US currency: 1, 5, 10, 25) 
but may fail for arbitrary systems (e.g., coins [1, 3, 4], value 6 -> greedy gives 4+1+1=3 coins, optimal is 3+3=2 coins).

Performance Analysis:
- Time Complexity: O(N) where N is the number of coins chosen if sorted.
- Space Complexity: O(1) auxiliary space.

Edge Cases:
- Target value is 0.
- No coin can form the value (though usually a 1-coin is assumed).

Interview Challenge:
"Find the minimum number of coins to make a given value. Does your algorithm always work for any coin system?"
"""

from typing import List, Dict
import unittest

def min_coins_basic(coins: List[int], amount: int) -> int:
    """Basic greedy coin change returning min coins."""
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        if amount == 0:
            break
        count += amount // coin
        amount %= coin
        
    return count if amount == 0 else -1

def min_coins_intermediate(coins: List[int], amount: int) -> List[int]:
    """Intermediate implementation returning the actual coins used."""
    coins.sort(reverse=True)
    result = []
    
    for coin in coins:
        if amount == 0:
            break
        num_coins = amount // coin
        result.extend([coin] * num_coins)
        amount %= coin
        
    return result if amount == 0 else []

def min_coins_advanced(coins: List[int], amount: int) -> Dict[int, int]:
    """Advanced implementation returning a dictionary of coin counts."""
    coins.sort(reverse=True)
    result = {}
    
    for coin in coins:
        if amount == 0:
            break
        num_coins = amount // coin
        if num_coins > 0:
            result[coin] = num_coins
        amount %= coin
        
    return result if amount == 0 else {}

class TestMinCoins(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(min_coins_basic([1, 2, 5, 10, 20, 50, 100, 500, 1000], 93), 5) # 50, 20, 20, 2, 1
        
    def test_intermediate(self):
        self.assertEqual(min_coins_intermediate([1, 5, 10, 25], 36), [25, 10, 1])
        
    def test_advanced(self):
        self.assertEqual(min_coins_advanced([1, 5, 10, 25], 36), {25: 1, 10: 1, 1: 1})
        self.assertEqual(min_coins_advanced([2], 3), {})

if __name__ == "__main__":
    unittest.main()
