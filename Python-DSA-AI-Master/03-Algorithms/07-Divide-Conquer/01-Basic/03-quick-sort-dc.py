"""
Quick Sort using Divide and Conquer.

Learning Objectives:
1. Understand quick sort and partitioning.
2. Implement different partition schemes (Lomuto, Hoare).
3. Analyze performance and worst-case scenarios.

Concept Explanation:
Quick Sort selects a 'pivot' element from the array and partitions the other elements 
into two sub-arrays, according to whether they are less than or greater than the pivot.
"""

from typing import List
import random

def quick_sort_basic(arr: List[int]) -> List[int]:
    """Basic out-of-place implementation for readability."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_basic(left) + middle + quick_sort_basic(right)

def partition(arr: List[int], low: int, high: int) -> int:
    """Lomuto partition scheme."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_advanced(arr: List[int], low: int = 0, high: int = None) -> None:
    """Advanced in-place implementation."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_advanced(arr, low, pi - 1)
        quick_sort_advanced(arr, pi + 1, high)

"""
Performance Analysis:
- Time Complexity: Best/Average O(n log n). Worst O(n^2) when already sorted.
- Space Complexity: O(log n) auxiliary stack space.

Edge Cases:
- Pre-sorted arrays (use randomized pivot to mitigate O(n^2)).
- Arrays with many duplicate elements.
- Empty arrays.

Interview Challenge:
Find the Kth largest element in an unsorted array using QuickSelect.
"""

def test_quick_sort():
    arr = [10, 7, 8, 9, 1, 5]
    res = quick_sort_basic(arr)
    assert res == sorted(arr)
    
    arr2 = [10, 7, 8, 9, 1, 5]
    quick_sort_advanced(arr2)
    assert arr2 == sorted(arr)
    print("All tests passed.")

if __name__ == "__main__":
    test_quick_sort()
