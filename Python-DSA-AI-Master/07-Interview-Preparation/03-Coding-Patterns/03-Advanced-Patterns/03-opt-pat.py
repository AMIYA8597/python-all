"""
Optimization Patterns (Dynamic Programming, Greedy)
===================================================

Learning Objectives:
1. Master identifying optimal substructure and overlapping subproblems.
2. Implement Bottom-Up (Tabulation) and Top-Down (Memoization) DP.
3. Understand when a Greedy approach works vs when DP is required.

Concept Explanation:
Dynamic Programming (DP) is a method for solving complex problems by breaking them 
down into simpler subproblems. It is applicable when the subproblems overlap and have 
optimal substructure. 
Greedy algorithms make the locally optimal choice at each stage.
"""

from typing import List, Dict
import unittest

class OptimizationProblems:
    
    @staticmethod
    def knapsack_01_memo(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Basic/Intermediate DP: 0/1 Knapsack using Top-Down Memoization.
        """
        memo = {}
        
        def dp(i: int, w: int) -> int:
            if i < 0 or w == 0:
                return 0
            if (i, w) in memo:
                return memo[(i, w)]
                
            if weights[i] > w:
                res = dp(i - 1, w)
            else:
                res = max(dp(i - 1, w), values[i] + dp(i - 1, w - weights[i]))
            
            memo[(i, w)] = res
            return res
            
        return dp(len(weights) - 1, capacity)

    @staticmethod
    def knapsack_01_tab(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Advanced DP: 0/1 Knapsack using Bottom-Up Tabulation (Space Optimized).
        """
        n = len(weights)
        dp = [0] * (capacity + 1)
        
        for i in range(n):
            # Traverse backwards to prevent re-using the same item
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
                
        return dp[capacity]
        
    @staticmethod
    def jump_game_greedy(nums: List[int]) -> bool:
        """
        Greedy Optimization: Can reach the last index?
        Instead of O(N^2) DP, Greedy is O(N).
        """
        goal = len(nums) - 1
        for i in range(len(nums) - 1, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0

# --- Performance Analysis ---
# DP Knapsack: Time O(N * W), Space O(W) with optimized tabulation.
# Greedy Jump Game: Time O(N), Space O(1).
# 
# Edge Cases: Capacity 0, No items, Items with weight > capacity.

class TestOptimization(unittest.TestCase):
    def setUp(self):
        self.weights = [1, 2, 3]
        self.values = [6, 10, 12]
        self.capacity = 5
        self.expected = 22 # items 1 and 2 (weights 2+3, vals 10+12)
        
    def test_knapsack_memo(self):
        res = OptimizationProblems.knapsack_01_memo(self.weights, self.values, self.capacity)
        self.assertEqual(res, self.expected)
        
    def test_knapsack_tab(self):
        res = OptimizationProblems.knapsack_01_tab(self.weights, self.values, self.capacity)
        self.assertEqual(res, self.expected)

    def test_jump_game(self):
        self.assertTrue(OptimizationProblems.jump_game_greedy([2,3,1,1,4]))
        self.assertFalse(OptimizationProblems.jump_game_greedy([3,2,1,0,4]))

if __name__ == '__main__':
    unittest.main()
