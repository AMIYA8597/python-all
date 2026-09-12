"""
Longest Increasing Subsequence (LIS)

This module explains the Longest Increasing Subsequence problem and demonstrates
different Dynamic Programming and Greedy/Binary Search approaches.

Learning Objectives:
1. Identify problems that require finding subsequences with specific properties.
2. Formulate a dynamic programming relation for LIS.
3. Understand the optimization from O(N^2) DP to O(N log N) using Binary Search (Patience Sorting).
4. Learn how to reconstruct the actual LIS, not just its length.

Concept Explanation:
Given an integer array nums, return the length of the longest strictly increasing subsequence.
A subsequence is a sequence that can be derived from an array by deleting some or no elements
without changing the order of the remaining elements. For example, [3, 6, 2, 7] is a subsequence
of the array [0, 3, 1, 6, 2, 2, 7].

Beginner Explanation:
Imagine a line of people with different heights. You want to pick out a group of people
from left to right such that each person you pick is strictly taller than the previous
one you picked. You want this group to be as large as possible. You can skip people,
but you can't rearrange them.

Professional Implementation:
We will implement two versions:
1. Classic DP O(N^2)
2. Optimized Binary Search O(N log N)
"""

from typing import List
import bisect

def length_of_lis_dp(nums: List[int]) -> int:
    """
    Find the length of the LIS using classic Dynamic Programming.
    
    Algorithm:
    dp[i] represents the length of the longest increasing subsequence that ends with nums[i].
    For each element i, we look back at all elements j (where j < i).
    If nums[i] > nums[j], we can append nums[i] to the subsequence ending at j.
    Thus, dp[i] = max(dp[i], dp[j] + 1).
    
    Time Complexity: O(N^2) where N is the length of nums.
    Space Complexity: O(N) for the dp array.
    """
    if not nums:
        return 0
        
    n = len(nums)
    # Initialize dp array with 1s, since each element is at least an LIS of length 1 (itself).
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)

def length_of_lis_optimized(nums: List[int]) -> int:
    """
    Find the length of the LIS using Binary Search (Patience Sorting).
    
    Algorithm:
    Maintain a list `sub` which stores the smallest tail of all increasing subsequences
    of length `i+1` in `sub[i]`.
    For each number, we use binary search to find the index of the smallest number in `sub`
    that is >= num.
    If such a number exists, we replace it with `num` (greedily keeping tails as small as possible).
    If `num` is larger than all elements in `sub`, we append it to `sub`.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N) for the sub array.
    """
    if not nums:
        return 0
        
    sub: List[int] = []
    
    for num in nums:
        # bisect_left finds the index of the first element >= num
        idx = bisect.bisect_left(sub, num)
        
        # If num is greater than all elements, append it
        if idx == len(sub):
            sub.append(num)
        # Otherwise, replace the element to keep the potential tails small
        else:
            sub[idx] = num
            
    # Note: `sub` is NOT necessarily the actual LIS, but its length is correct.
    return len(sub)

# ==========================================
# Interview Challenge & Common Mistakes
# ==========================================
# Challenge: Can you also return the ACTUAL Longest Increasing Subsequence, not just the length?
# Solution: You can modify the DP approach to keep a `parent` array that tracks the index 
# `j` that provided the max `dp[i]`. Then backtrack from the index with the max DP value.
#
# Common Mistake: Thinking that the `sub` array in the O(N log N) approach contains 
# the actual LIS. It does NOT. It just maintains the smallest possible tails for different lengths.

def test_lis():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    expected_length = 4 # e.g., [2, 3, 7, 101] or [2, 5, 7, 18]
    
    assert length_of_lis_dp(nums) == expected_length, "DP LIS failed"
    assert length_of_lis_optimized(nums) == expected_length, "Optimized LIS failed"
    
    assert length_of_lis_optimized([7, 7, 7, 7]) == 1, "All same elements failed"
    assert length_of_lis_optimized([0, 1, 0, 3, 2, 3]) == 4, "Example 2 failed"
    
    print("All LIS tests passed successfully!")

if __name__ == "__main__":
    test_lis()
