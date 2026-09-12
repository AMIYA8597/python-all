"""
Rod Cutting Problem - Dynamic Programming

Concept Explanation:
The Rod Cutting problem is a classic dynamic programming problem. Given a rod of length `n` inches and an array of prices that includes prices of all pieces of size smaller than `n`, determine the maximum value obtainable by cutting up the rod and selling the pieces. For example, if length of the rod is 8 and the values of different pieces are given, we want to maximize the revenue.
This is similar to the Unbounded Knapsack problem, where we can use multiple instances of a given length to achieve the target length.

Learning Objectives:
1. Understand how to break down the Rod Cutting problem into overlapping subproblems.
2. Implement recursive (Top-Down with Memoization) and iterative (Bottom-Up) approaches.
3. Reconstruct the optimal solution (which pieces to cut).
4. Analyze the time and space complexity of the algorithms.

Industry Use Cases:
- Resource allocation and cutting stock problems in manufacturing.
- Portfolio optimization and budgeting problems where fractional shares aren't allowed.
- Similar underlying logic applies to network bandwidth allocation.
"""

from typing import List, Tuple, Dict

def rod_cutting_recursive(prices: List[int], n: int) -> int:
    """
    Basic recursive approach (exponential time complexity).
    Not recommended for large `n`.
    """
    if n <= 0:
        return 0
    max_val = float('-inf')
    for i in range(n):
        # i goes from 0 to n-1. The length is i+1, price is prices[i]
        max_val = max(max_val, prices[i] + rod_cutting_recursive(prices, n - i - 1))
    return int(max_val)


def rod_cutting_memoized(prices: List[int], n: int) -> int:
    """
    Top-Down approach using memoization.
    
    Time Complexity: O(n^2) - We compute max value for each length from 1 to n. For each, we do a loop of up to n iterations.
    Space Complexity: O(n) for the memo dictionary and the recursion stack.
    """
    memo: Dict[int, int] = {}
    
    def dp(length: int) -> int:
        if length == 0:
            return 0
        if length in memo:
            return memo[length]
        
        max_val = -1
        for i in range(length):
            # Try cutting a piece of length i+1
            max_val = max(max_val, prices[i] + dp(length - i - 1))
        
        memo[length] = max_val
        return max_val
        
    return dp(n)


def rod_cutting_bottom_up(prices: List[int], n: int) -> int:
    """
    Bottom-Up iterative approach.
    
    Time Complexity: O(n^2)
    Space Complexity: O(n) for the dp array.
    """
    # dp[i] will hold the maximum revenue for rod of length i
    dp = [0] * (n + 1)
    
    for length in range(1, n + 1):
        max_val = -1
        for i in range(length):
            max_val = max(max_val, prices[i] + dp[length - i - 1])
        dp[length] = max_val
        
    return dp[n]


def rod_cutting_with_cuts(prices: List[int], n: int) -> Tuple[int, List[int]]:
    """
    Bottom-Up iterative approach that also reconstructs the solution.
    Returns a tuple of (max_revenue, list_of_cut_lengths).
    """
    dp = [0] * (n + 1)
    # cut[i] will hold the first cut length that gives the optimal revenue for length i
    cut = [0] * (n + 1)
    
    for length in range(1, n + 1):
        max_val = -1
        best_first_cut = -1
        for i in range(length):
            if max_val < prices[i] + dp[length - i - 1]:
                max_val = prices[i] + dp[length - i - 1]
                best_first_cut = i + 1
        dp[length] = max_val
        cut[length] = best_first_cut
        
    # Reconstruct the cuts
    actual_cuts = []
    curr_length = n
    while curr_length > 0:
        c = cut[curr_length]
        actual_cuts.append(c)
        curr_length -= c
        
    return dp[n], actual_cuts


# -----------------------------------------------------------------------------
# Interview Challenge
# -----------------------------------------------------------------------------
# You are given a rod of length n, but there is a fixed cost `c` for every cut you make.
# Find the maximum revenue. 
# Hint: You only pay the cut cost if you actually make a cut (i.e. length is split into >1 piece).

def rod_cutting_with_cost(prices: List[int], n: int, c: int) -> int:
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        # Base case: no cut at all
        max_val = prices[length - 1]
        for i in range(1, length):
            # We cut a piece of length i, leaving length - i
            max_val = max(max_val, prices[i - 1] + dp[length - i] - c)
        dp[length] = max_val
    return dp[n]


if __name__ == "__main__":
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    n = 8
    
    print("--- Rod Cutting Problem ---")
    print(f"Prices: {prices}")
    print(f"Rod Length: {n}")
    
    assert rod_cutting_recursive(prices, n) == 22
    assert rod_cutting_memoized(prices, n) == 22
    assert rod_cutting_bottom_up(prices, n) == 22
    
    max_rev, cuts = rod_cutting_with_cuts(prices, n)
    assert max_rev == 22
    assert sorted(cuts) == [2, 6]  # 5 + 17 = 22
    print(f"Optimal Revenue: {max_rev}, Cuts: {cuts}")
    print("All tests passed!")
