"""
Binary Search Pattern

Learning Objectives:
1. Understand the core concept of Binary Search.
2. Master the standard template to avoid off-by-one errors.
3. Learn how to adapt binary search for finding first/last occurrences.
4. Explore binary search on answer space (advanced).
5. Analyze time and space complexity.

Concept Explanation:
Binary Search is a highly efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one. Time complexity is O(log N).
"""

from typing import List

# Basic Implementation: Standard Binary Search
def binary_search(nums: List[int], target: int) -> int:
    """Time: O(log N), Space: O(1)"""
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

# Intermediate Implementation: Find First Occurrence
def find_first(nums: List[int], target: int) -> int:
    """Time: O(log N), Space: O(1)"""
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1 # Keep searching to the left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

# Advanced Implementation: Binary Search on Answer Space (Koko Eating Bananas)
import math
def min_eating_speed(piles: List[int], h: int) -> int:
    """Time: O(N log(Max P)), Space: O(1)"""
    left, right = 1, max(piles)
    res = right
    
    while left <= right:
        k = left + (right - left) // 2
        
        hours = 0
        for p in piles:
            hours += math.ceil(p / k)
            
        if hours <= h:
            res = k
            right = k - 1
        else:
            left = k + 1
            
    return res

# Edge Cases to Handle:
# 1. Empty array or target out of bounds.
# 2. Integer overflow when calculating mid (use `left + (right - left) // 2`).
# 3. Array with all identical elements.

# Interview Challenge: Search in Rotated Sorted Array
def search_rotated(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
            
        # Left sorted portion
        if nums[left] <= nums[mid]:
            if target > nums[mid] or target < nums[left]:
                left = mid + 1
            else:
                right = mid - 1
        # Right sorted portion
        else:
            if target < nums[mid] or target > nums[right]:
                right = mid - 1
            else:
                left = mid + 1
                
    return -1

def run_tests():
    assert binary_search([-1,0,3,5,9,12], 9) == 4
    assert binary_search([-1,0,3,5,9,12], 2) == -1
    
    assert find_first([1, 2, 2, 2, 3, 4], 2) == 1
    assert find_first([1, 2, 2, 2, 3, 4], 5) == -1
    
    assert min_eating_speed([3,6,7,11], 8) == 4
    assert min_eating_speed([30,11,23,4,20], 5) == 30
    
    assert search_rotated([4,5,6,7,0,1,2], 0) == 4
    assert search_rotated([4,5,6,7,0,1,2], 3) == -1
    
    print("All Binary Search tests passed!")

if __name__ == "__main__":
    run_tests()
