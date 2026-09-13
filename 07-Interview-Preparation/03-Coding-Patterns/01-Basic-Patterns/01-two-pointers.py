"""
Two Pointers Pattern - Comprehensive Guide

Learning Objectives:
- Understand the Two Pointers technique and when to use it
- Implement two pointers from ends and from same direction
- Analyze time and space complexity of two pointers solutions
- Solve common interview challenges using this pattern

Concept Explanation:
The Two Pointers pattern involves using two variables (pointers) to iterate through a linear data structure, typically an array or linked list. 
The pointers can move towards each other, in the same direction, or independently based on certain conditions. This technique is especially useful for searching pairs in a sorted array, reversing elements, or finding subsets.

When to use:
- Dealing with sorted arrays (or linked lists) and need to find a set of elements that fulfill certain constraints
- The set of elements in the array is a pair, a triplet, or even a subarray

Basic/Intermediate/Advanced Implementations provided below.
"""

from typing import List, Tuple, Optional

# Basic: Pair with Target Sum
def pair_with_target_sum(arr: List[int], target_sum: int) -> List[int]:
    """
    Given an array of sorted numbers and a target sum, find a pair in the array whose sum is equal to the given target.
    Returns indices of the two numbers.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target_sum:
            return [left, right]
        if target_sum > current_sum:
            left += 1  # We need a pair with a bigger sum
        else:
            right -= 1  # We need a pair with a smaller sum
    return [-1, -1]


# Intermediate: Remove Duplicates
def remove_duplicates(arr: List[int]) -> int:
    """
    Given an array of sorted numbers, remove all duplicates in-place.
    Returns the length of the new subarray.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not arr:
        return 0
    next_non_duplicate = 1
    for i in range(1, len(arr)):
        if arr[next_non_duplicate - 1] != arr[i]:
            arr[next_non_duplicate] = arr[i]
            next_non_duplicate += 1
    return next_non_duplicate


# Advanced: Triplet Sum to Zero (3Sum)
def search_triplets(arr: List[int]) -> List[List[int]]:
    """
    Given an array of unsorted numbers, find all unique triplets in it that add up to zero.
    Time Complexity: O(N^2)
    Space Complexity: O(N) for sorting
    """
    arr.sort()
    triplets = []
    for i in range(len(arr) - 2):
        if i > 0 and arr[i] == arr[i-1]:
            continue  # skip same element to avoid duplicate triplets
        search_pair(arr, -arr[i], i+1, triplets)
    return triplets

def search_pair(arr: List[int], target_sum: int, left: int, triplets: List[List[int]]):
    right = len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target_sum:
            triplets.append([-target_sum, arr[left], arr[right]])
            left += 1
            right -= 1
            while left < right and arr[left] == arr[left - 1]:
                left += 1
            while left < right and arr[right] == arr[right + 1]:
                right -= 1
        elif target_sum > current_sum:
            left += 1
        else:
            right -= 1

# Edge Cases:
# - Empty arrays
# - Arrays with identical elements
# - No matching target

def run_tests():
    print("Testing Two Pointers...")
    assert pair_with_target_sum([1, 2, 3, 4, 6], 6) == [1, 3]
    assert remove_duplicates([2, 3, 3, 3, 6, 9, 9]) == 4
    trips = search_triplets([-3, 0, 1, 2, -1, 1, -2])
    print(f"Triplets: {trips}")
    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
