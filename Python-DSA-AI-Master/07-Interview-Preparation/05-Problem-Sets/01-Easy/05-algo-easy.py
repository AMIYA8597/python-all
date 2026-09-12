"""
Algorithms Easy Problem Set

Learning Objectives:
1. Master fundamental search techniques like Binary Search.
2. Understand basic dynamic programming concepts (memoization/tabulation).
3. Apply stack data structures for parsing algorithms.

Concepts Explained:
- Binary Search is a divide and conquer technique with O(log n) time complexity, requiring a sorted array.
- Dynamic Programming (Climbing Stairs) breaks problems into overlapping subproblems.
- Stacks (Valid Parentheses) follow LIFO order, perfect for matching nested structures.
"""

from typing import List
import time

def binary_search(nums: List[int], target: int) -> int:
    """
    Given an array of integers nums which is sorted in ascending order, and an integer target,
    write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.
    Must write an algorithm with O(log n) runtime complexity.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

def climb_stairs(n: int) -> int:
    """
    You are climbing a staircase. It takes n steps to reach the top.
    Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
    """
    if n <= 2:
        return n
        
    prev1 = 1
    prev2 = 2
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev1 = prev2
        prev2 = current
        
    return prev2

def is_valid_parentheses(s: str) -> bool:
    """
    Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack

def performance_analysis():
    print("Performance Analysis for Binary Search:")
    nums = list(range(1000000))
    target = 999999
    start = time.time()
    binary_search(nums, target)
    print(f"Time taken: {time.time() - start:.6f} seconds")

# Interview Challenge: First Bad Version (Conceptually similar to Binary Search)
def first_bad_version(n: int, isBadVersion) -> int:
    left, right = 1, n
    while left < right:
        mid = left + (right - left) // 2
        if isBadVersion(mid):
            right = mid
        else:
            left = mid + 1
    return left

def test_algo_easy():
    print("Testing Binary Search...")
    assert binary_search([-1,0,3,5,9,12], 9) == 4
    assert binary_search([-1,0,3,5,9,12], 2) == -1
    
    print("Testing Climb Stairs...")
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    
    print("Testing Valid Parentheses...")
    assert is_valid_parentheses("()") is True
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("(]") is False
    
    print("All tests passed!")

if __name__ == "__main__":
    test_algo_easy()
    performance_analysis()
