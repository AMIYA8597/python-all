"""
Randomized QuickSort Algorithm

Learning Objectives:
1. Understand the QuickSort algorithm and its divide-and-conquer strategy.
2. Learn how randomization can improve the average-case performance and prevent worst-case scenarios.
3. Implement Randomized QuickSort in Python using different partition schemes.
4. Analyze the time and space complexity of Randomized QuickSort.

Concept Explanation:
QuickSort is an efficient sorting algorithm that selects a 'pivot' element and partitions the array
such that all elements smaller than the pivot are to its left, and all greater elements are to its right.
In standard QuickSort, a deterministic pivot choice (e.g., first or last element) can lead to O(N^2)
time complexity if the array is already sorted. Randomized QuickSort mitigates this by choosing a
random pivot, ensuring an expected O(N log N) time complexity regardless of the input distribution.
"""

import random
from typing import List

# Basic Implementation: Randomized QuickSort using extra space (easy to understand)
def randomized_quicksort_basic(arr: List[int]) -> List[int]:
    """Basic randomized quicksort using list comprehensions and extra space."""
    if len(arr) <= 1:
        return arr
    
    pivot_idx = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_idx]
    
    left = [x for i, x in enumerate(arr) if x < pivot or (x == pivot and i != pivot_idx)]
    right = [x for i, x in enumerate(arr) if x > pivot]
    
    return randomized_quicksort_basic(left) + [pivot] + randomized_quicksort_basic(right)

# Intermediate Implementation: In-place Randomized QuickSort (Lomuto Partition Scheme)
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

def randomized_partition(arr: List[int], low: int, high: int) -> int:
    """Selects a random pivot and swaps it to the end before partitioning."""
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    return partition(arr, low, high)

def randomized_quicksort_inplace(arr: List[int], low: int, high: int) -> None:
    """In-place randomized quicksort."""
    if low < high:
        pi = randomized_partition(arr, low, high)
        randomized_quicksort_inplace(arr, low, pi - 1)
        randomized_quicksort_inplace(arr, pi + 1, high)

# Advanced Implementation: 3-Way Randomized QuickSort (Dutch National Flag)
def randomized_quicksort_3way(arr: List[int], low: int, high: int) -> None:
    """3-Way Randomized QuickSort to handle duplicate elements efficiently."""
    if low >= high:
        return
        
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[low] = arr[low], arr[pivot_idx]
    pivot = arr[low]
    
    lt, gt, i = low, high, low + 1
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
            
    randomized_quicksort_3way(arr, low, lt - 1)
    randomized_quicksort_3way(arr, gt + 1, high)

# Performance Analysis
def performance_analysis():
    """
    Time Complexity:
    - Best Case: O(N log N)
    - Average Case: Expected O(N log N)
    - Worst Case: O(N^2) - Highly improbable due to randomization.
    
    Space Complexity:
    - In-place Lomuto: O(log N) expected for recursion stack, O(N) worst-case stack depth.
    - 3-Way: O(log N) expected stack space.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Empty array.
    - Single element array.
    - Array with all identical elements (3-Way QuickSort handles this in O(N)).
    - Already sorted / reverse sorted array (Randomized QuickSort avoids O(N^2)).
    """
    pass

# Interview Challenge
def k_closest_elements(arr: List[int], k: int, x: int) -> List[int]:
    """
    Challenge: Find the K closest elements to x in an unsorted array.
    """
    arr_copy = arr.copy()
    def dist(val): return abs(val - x)
    arr_copy.sort(key=lambda val: (dist(val), val))
    return arr_copy[:k]

# Tests
def run_tests():
    arr = [10, 7, 8, 9, 1, 5]
    res = randomized_quicksort_basic(arr)
    assert res == [1, 5, 7, 8, 9, 10]
    
    arr2 = [3, 2, 1, 5, 6, 4]
    randomized_quicksort_inplace(arr2, 0, len(arr2)-1)
    assert arr2 == [1, 2, 3, 4, 5, 6]
    
    arr3 = [4, 4, 4, 1, 2, 8, 9, 4]
    randomized_quicksort_3way(arr3, 0, len(arr3)-1)
    assert arr3 == [1, 2, 4, 4, 4, 4, 8, 9]
    
    empty = []
    randomized_quicksort_inplace(empty, 0, -1)
    assert empty == []
    
    single = [1]
    randomized_quicksort_inplace(single, 0, 0)
    assert single == [1]

    print("All Randomized QuickSort tests passed!")

if __name__ == "__main__":
    run_tests()
