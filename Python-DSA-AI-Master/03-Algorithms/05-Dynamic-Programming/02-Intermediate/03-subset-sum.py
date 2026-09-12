"""
Subset Sum Problem (Dynamic Programming)

This module explains the Subset Sum problem and demonstrates how to solve it using 
Dynamic Programming (Tabulation and Space Optimization).

Learning Objectives:
1. Master the 0/1 Knapsack style dynamic programming pattern.
2. Understand 2D tabulation for subset problems.
3. Learn how to optimize 2D DP space into 1D arrays.
4. Analyze time and space complexity tradeoffs.

Concept Explanation:
Given a set of non-negative integers, and a value `target`, determine if there is a subset 
of the given set with sum equal to given `target`.
This is a classic decision problem, often a subproblem for partitioning an array (e.g., 
Partition Equal Subset Sum).

Beginner Explanation:
Imagine you have a wallet with specific coins and bills: [3, 34, 4, 12, 5, 2].
You want to pay exactly 9 dollars. Can you find a combination of your money that adds up 
to exactly 9? Yes, 4 + 5 = 9. What about 30? No combination works.
Dynamic programming solves this by keeping track of all the sums we CAN make using the 
first `i` items, and then systematically adding the `i+1`th item to see what new sums we can make.

Professional Implementation:
We will implement standard 2D DP and an optimized 1D DP array approach.
"""

from typing import List

def subset_sum_2d(nums: List[int], target: int) -> bool:
    """
    Determine if a subset sums to target using 2D DP tabulation.
    
    Algorithm:
    dp[i][j] will be True if there is a subset of elements from nums[0...i-1] 
    that sums to j.
    
    Time Complexity: O(N * target) where N is len(nums).
    Space Complexity: O(N * target) for the 2D DP table.
    """
    n = len(nums)
    # dp[i][j] is True if sum j can be formed using first i elements
    dp = [[False for _ in range(target + 1)] for _ in range(n + 1)]
    
    # Base case: If target is 0, we can always form it with an empty subset
    for i in range(n + 1):
        dp[i][0] = True
        
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            # If current element is greater than the target sum, we can't include it
            if nums[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                # We can either exclude the item OR include the item
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i - 1]]
                
    return dp[n][target]

def subset_sum_1d(nums: List[int], target: int) -> bool:
    """
    Determine if a subset sums to target using 1D space-optimized DP.
    
    Algorithm:
    Notice that dp[i][j] only relies on dp[i-1][...]. We can optimize the space 
    by only keeping the previous row. Furthermore, by iterating `j` backwards, 
    we can use a single 1D array.
    
    Time Complexity: O(N * target)
    Space Complexity: O(target) - highly optimized!
    """
    # dp[j] will be True if sum j can be formed
    dp = [False] * (target + 1)
    
    # Base case: sum 0 is always possible
    dp[0] = True
    
    for num in nums:
        # Traverse backwards from target down to num
        # This prevents reusing the same number multiple times in the same step
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
            
    return dp[target]

# ==========================================
# Interview Challenge & Common Mistakes
# ==========================================
# Challenge: Partition Equal Subset Sum (LeetCode 416). Can you partition an array into 
# two subsets such that the sum of elements in both subsets is equal?
# Solution: Calculate total sum. If total is odd, return False. If even, call 
# subset_sum_1d(nums, target=total // 2).
#
# Common Mistake: In the 1D space optimization, traversing `j` forwards instead of backwards.
# If you traverse forwards, you might use the current `num` multiple times (which solves the 
# Unbounded Knapsack / Coin Change problem, not Subset Sum!). 
# Always traverse backwards for 0/1 Knapsack type problems!

def test_subset_sum():
    nums = [3, 34, 4, 12, 5, 2]
    
    # Target 9: True (4 + 5)
    assert subset_sum_2d(nums, 9) == True
    assert subset_sum_1d(nums, 9) == True
    
    # Target 30: False
    assert subset_sum_2d(nums, 30) == False
    assert subset_sum_1d(nums, 30) == False
    
    # Target 0: True (empty subset)
    assert subset_sum_1d(nums, 0) == True
    
    print("All Subset Sum tests passed successfully!")

if __name__ == "__main__":
    test_subset_sum()
