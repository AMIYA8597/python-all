"""
Array Easy Problem Set

Learning Objectives:
1. Master fundamental array traversal techniques.
2. Understand space-time trade-offs using hash maps.
3. Learn how to track minimum and maximum states during iteration.

Concepts Explained:
- Arrays are contiguous memory allocations, providing O(1) read/write access given an index.
- Common patterns for easy array problems include:
  * Two pointers (often moving towards each other)
  * Hash Maps for constant time lookups
  * State variables to keep track of max/min values seen so far.

This module covers common easy array interview questions.
"""

from typing import List
import time

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    Basic approach (O(n^2)) is nested loops.
    Advanced approach (O(n)) uses a hash map to store the complement.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def max_profit(prices: List[int]) -> int:
    """
    You are given an array prices where prices[i] is the price of a given stock on the ith day.
    Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
    """
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
            
    return max_profit

def contains_duplicate(nums: List[int]) -> bool:
    """
    Given an integer array nums, return true if any value appears at least twice in the array,
    and return false if every element is distinct.
    """
    return len(set(nums)) != len(nums)

def performance_analysis():
    print("Performance Analysis for Two Sum:")
    nums = [i for i in range(10000)] + [10001, 10002]
    target = 20003
    start = time.time()
    two_sum(nums, target)
    print(f"Time taken: {time.time() - start:.6f} seconds")

# Interview Challenge: Implement finding the missing number in an array containing n distinct numbers taken from 0, 1, 2, ..., n.
def missing_number(nums: List[int]) -> int:
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum

def test_array_easy():
    print("Testing Two Sum...")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    
    print("Testing Max Profit...")
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0
    
    print("Testing Contains Duplicate...")
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False
    
    print("Testing Missing Number...")
    assert missing_number([3, 0, 1]) == 2
    
    print("All tests passed!")

if __name__ == "__main__":
    test_array_easy()
    performance_analysis()
