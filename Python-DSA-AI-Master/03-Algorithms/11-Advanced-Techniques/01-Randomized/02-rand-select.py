"""
Randomized QuickSelect Algorithm

Learning Objectives:
1. Understand the QuickSelect algorithm for finding the k-th smallest/largest element.
2. Recognize how it modifies the QuickSort partition method.
3. Analyze expected vs worst-case time complexities.

Concept Explanation:
QuickSelect is a selection algorithm to find the k-th smallest element in an unordered list. 
It is related to the QuickSort algorithm. Instead of recurring on both sides of the partition,
QuickSelect only recurs into the side that contains the k-th element. The expected time 
complexity is O(N), but worst-case is O(N^2) without randomization. 
"""

import random
from typing import List

# Basic Implementation: QuickSelect with Extra Space
def randomized_quickselect_basic(arr: List[int], k: int) -> int:
    """Find the k-th smallest element (1-indexed) using extra space."""
    if not arr:
        raise ValueError("Array is empty")
    
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k <= len(left):
        return randomized_quickselect_basic(left, k)
    elif k <= len(left) + len(mid):
        return pivot
    else:
        return randomized_quickselect_basic(right, k - len(left) - len(mid))

# Intermediate Implementation: In-place Randomized QuickSelect
def partition(arr: List[int], low: int, high: int) -> int:
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def randomized_quickselect_inplace(arr: List[int], low: int, high: int, k: int) -> int:
    """Find the k-th smallest element (1-indexed) in-place."""
    if low == high:
        return arr[low]
        
    pi = partition(arr, low, high)
    
    count = pi - low + 1
    
    if count == k:
        return arr[pi]
    elif count > k:
        return randomized_quickselect_inplace(arr, low, pi - 1, k)
    else:
        return randomized_quickselect_inplace(arr, pi + 1, high, k - count)

# Advanced Implementation: Iterative QuickSelect
def iterative_quickselect(arr: List[int], k: int) -> int:
    """Iterative in-place QuickSelect."""
    low, high = 0, len(arr) - 1
    while low <= high:
        pi = partition(arr, low, high)
        count = pi - low + 1
        
        if count == k:
            return arr[pi]
        elif count > k:
            high = pi - 1
        else:
            low = pi + 1
            k -= count
    return -1

# Performance Analysis
def performance_analysis():
    """
    Time Complexity:
    - Expected: O(N)
    - Worst Case: O(N^2) if bad pivots are chosen consistently, though rare.
    
    Space Complexity:
    - Extra Space version: O(N) auxiliary space.
    - In-place Recursive: O(N) worst-case recursion stack, O(log N) expected.
    - Iterative In-place: O(1) auxiliary space.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - k > len(arr) or k <= 0
    - Array with duplicate elements
    - Array already sorted
    """
    pass

# Interview Challenge
def find_kth_largest(arr: List[int], k: int) -> int:
    """
    Challenge: Find the K-th LARGEST element in an array.
    """
    target = len(arr) - k + 1
    return iterative_quickselect(arr, target)

# Tests
def run_tests():
    arr = [7, 10, 4, 3, 20, 15]
    assert randomized_quickselect_basic(arr, 3) == 7
    assert randomized_quickselect_inplace(arr.copy(), 0, len(arr)-1, 3) == 7
    assert iterative_quickselect(arr.copy(), 3) == 7
    
    assert find_kth_largest(arr.copy(), 2) == 15
    
    dup_arr = [3, 2, 1, 5, 6, 4, 4]
    assert randomized_quickselect_basic(dup_arr, 4) == 4
    
    print("All Randomized QuickSelect tests passed!")

if __name__ == "__main__":
    run_tests()
