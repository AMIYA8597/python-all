"""
Module Docstring: Digit Dynamic Programming (Digit DP)

Learning Objectives:
- Understand state representation for Digit DP.
- Solve counting problems for numbers with specific digit properties.
- Learn the concept of 'tight' bounds.

Concept Explanation:
Digit DP is used to count the number of integers in a range [L, R] that satisfy a certain property by constructing the numbers digit by digit.
"""

from typing import List, Dict, Tuple
import sys

def basic_digit_dp(bound: str) -> int:
    """Basic: Count numbers <= bound without digit '3'"""
    memo = {}
    def dp(idx: int, tight: bool) -> int:
        if idx == len(bound): return 1
        state = (idx, tight)
        if state in memo: return memo[state]
        
        limit = int(bound[idx]) if tight else 9
        ans = 0
        for d in range(limit + 1):
            if d == 3: continue
            ans += dp(idx + 1, tight and (d == limit))
            
        memo[state] = ans
        return ans
    return dp(0, True)

def intermediate_digit_dp(bound: str, sum_val: int) -> int:
    """Intermediate: Count numbers <= bound with digit sum == sum_val"""
    memo = {}
    def dp(idx: int, tight: bool, current_sum: int) -> int:
        if current_sum > sum_val: return 0
        if idx == len(bound): return 1 if current_sum == sum_val else 0
        state = (idx, tight, current_sum)
        if state in memo: return memo[state]
        
        limit = int(bound[idx]) if tight else 9
        ans = 0
        for d in range(limit + 1):
            ans += dp(idx + 1, tight and (d == limit), current_sum + d)
            
        memo[state] = ans
        return ans
    return dp(0, True, 0)

def advanced_digit_dp(L: str, R: str) -> int:
    """Advanced: Valid numbers in range [L, R] with advanced property"""
    # Computes f(R) - f(L-1)
    pass

# Performance Analysis:
# Time Complexity: O(Length * Limit * States). Usually very fast, e.g. O(18 * 2 * K).
# Space Complexity: O(Length * Limit * States) for memoization table.

# Edge Cases:
# - Lower bound is 0 or negative.
# - Handling leading zeros if the problem depends on number length.

# Interview Challenge: 
# Find the number of integers in [1, 10^18] where no two adjacent digits are the same.

def run_tests():
    assert basic_digit_dp("2") == 3 # 0, 1, 2
    assert intermediate_digit_dp("20", 2) == 2 # 2, 11, 20
    print("Digit DP tests passed.")

if __name__ == "__main__":
    run_tests()
