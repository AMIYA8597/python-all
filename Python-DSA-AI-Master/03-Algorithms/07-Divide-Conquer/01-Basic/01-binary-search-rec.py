"""
Binary Search (Recursive) using Divide and Conquer.

Learning Objectives:
1. Understand the divide and conquer paradigm applied to searching.
2. Implement recursive binary search.
3. Analyze time and space complexity.

Concept Explanation:
Binary search is a divide and conquer algorithm that finds the position of a target
value within a sorted array. It compares the target value to the middle element of the array.
If they are not equal, the half in which the target cannot lie is eliminated, and the search
continues on the remaining half.
"""

from typing import List, Optional

def binary_search_basic(arr: List[int], target: int) -> int:
    """Basic iterative implementation for comparison."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def binary_search_recursive(arr: List[int], target: int, left: int, right: int) -> int:
    """Intermediate recursive implementation."""
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

def binary_search_advanced(arr: List[int], target: int) -> int:
    """Advanced implementation with wrapper and validation."""
    if not arr:
        return -1
    return binary_search_recursive(arr, target, 0, len(arr) - 1)

"""
Performance Analysis:
- Time Complexity: O(log n)
- Space Complexity: O(log n) due to call stack for recursive version. (Iterative is O(1)).

Edge Cases:
- Empty array.
- Target smaller than all elements.
- Target larger than all elements.
- Target not in array.
- Duplicate elements (returns one of the indices).

Interview Challenge:
Find the first or last occurrence of a target number in a sorted array with duplicates.
"""

def test_binary_search():
    arr = [1, 3, 5, 7, 9, 11]
    assert binary_search_advanced(arr, 7) == 3
    assert binary_search_advanced(arr, 2) == -1
    assert binary_search_advanced([], 5) == -1
    assert binary_search_advanced([5], 5) == 0
    print("All tests passed.")

if __name__ == "__main__":
    test_binary_search()
