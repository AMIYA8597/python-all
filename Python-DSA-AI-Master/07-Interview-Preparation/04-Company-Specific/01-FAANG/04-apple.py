"""
Module: Apple Interview Questions (Python)

Learning Objectives:
- Master array manipulations without division.
- Implement word break using Dynamic Programming.
- Focus on space-time tradeoffs in array problems.

Concept Explanation:
Apple frequently asks system design level thinking in coding rounds (e.g. avoiding division for product of array) and dynamic programming concepts (Word Break).

Performance Analysis:
- Product of Array Except Self: Time O(N), Space O(1) (excluding output).
- Word Break: Time O(N^2) or O(N * M) where M is dict size, Space O(N).
"""

from typing import List

# Basic/Intermediate: Product of Array Except Self
def product_except_self(nums: List[int]) -> List[int]:
    """
    Given an integer array nums, return an array answer such that answer[i] 
    is equal to the product of all the elements of nums except nums[i].
    Must run in O(N) and not use division.
    """
    n = len(nums)
    res = [1] * n
    
    # Left products
    left_prod = 1
    for i in range(n):
        res[i] = left_prod
        left_prod *= nums[i]
        
    # Right products
    right_prod = 1
    for i in range(n - 1, -1, -1):
        res[i] *= right_prod
        right_prod *= nums[i]
        
    return res

# Advanced: Word Break (Dynamic Programming)
def word_break(s: str, wordDict: List[str]) -> bool:
    """
    Determine if s can be segmented into a space-separated sequence of dictionary words.
    """
    word_set = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True # Empty string is valid
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break # Move to next i
                
    return dp[len(s)]

def test_apple_questions():
    print("Testing Product Except Self...")
    assert product_except_self([1,2,3,4]) == [24,12,8,6]
    assert product_except_self([-1,1,0,-3,3]) == [0,0,9,0,0]
    print("Passed.")

    print("Testing Word Break...")
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print("Passed.")

if __name__ == "__main__":
    test_apple_questions()
    print("All Apple interview tests passed!")
