"""
Cyclic Sort Pattern - Comprehensive Guide

Learning Objectives:
- Understand the Cyclic Sort pattern and its intuition
- Solve problems involving arrays containing numbers in a given range
- Sort arrays in O(N) time and O(1) space when elements are within a fixed range
- Find missing, duplicate, and multiple missing/duplicate numbers

Concept Explanation:
This pattern describes an interesting approach to deal with problems involving arrays containing numbers in a given range. For example, take an array containing numbers from 1 to n. The most efficient way to sort this array is to iterate through the array and place each number at its correct index. That is, the number 1 should be at index 0, number 2 at index 1, and so on.

When to use:
- The array values are in a specific range, e.g., 1 to n or 0 to n.
- You are asked to find missing/duplicate/smallest missing positive numbers in O(N) time and O(1) space.
"""

from typing import List

# Basic: Cyclic Sort
def cyclic_sort(nums: List[int]) -> List[int]:
    """
    We are given an array containing 'n' objects. Each object, when created, was assigned a unique number from 1 to 'n'.
    Write a function to sort the objects in-place on their creation numbers in O(n) and without any extra space.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    i = 0
    while i < len(nums):
        j = nums[i] - 1
        if nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]  # swap
        else:
            i += 1
    return nums


# Intermediate: Find the Missing Number
def find_missing_number(nums: List[int]) -> int:
    """
    We are given an array containing 'n' distinct numbers taken from the range 0 to 'n'.
    Since the array has only 'n' numbers out of the total 'n+1' numbers, find the missing number.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    i, n = 0, len(nums)
    while i < n:
        j = nums[i]
        if nums[i] < n and nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]  # swap
        else:
            i += 1

    # find the first number missing from its index
    for i in range(n):
        if nums[i] != i:
            return i

    return n


# Advanced: Find all Duplicate Numbers
def find_all_duplicates(nums: List[int]) -> List[int]:
    """
    We are given an unsorted array containing 'n' numbers taken from the range 1 to 'n'.
    The array has some numbers appearing twice, find all these duplicate numbers without using extra space.
    Time Complexity: O(N)
    Space Complexity: O(1) - ignoring output list
    """
    i = 0
    while i < len(nums):
        j = nums[i] - 1
        if nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]  # swap
        else:
            i += 1

    duplicateNumbers = []
    for i in range(len(nums)):
        if nums[i] != i + 1:
            duplicateNumbers.append(nums[i])

    return duplicateNumbers


def run_tests():
    print("Testing Cyclic Sort...")
    assert cyclic_sort([3, 1, 5, 4, 2]) == [1, 2, 3, 4, 5]
    assert find_missing_number([4, 0, 3, 1]) == 2
    assert find_all_duplicates([3, 4, 4, 5, 5]) == [4, 5]
    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
