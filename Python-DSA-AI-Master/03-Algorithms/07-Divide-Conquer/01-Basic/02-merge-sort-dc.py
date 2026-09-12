"""
Merge Sort using Divide and Conquer.

Learning Objectives:
1. Understand the classic divide and conquer sorting algorithm.
2. Implement the merge operation efficiently.
3. Analyze sorting performance.

Concept Explanation:
Merge Sort divides the input array into two halves, calls itself for the two halves,
and then merges the two sorted halves.
"""

from typing import List

def merge_sort_basic(arr: List[int]) -> List[int]:
    """Basic out-of-place implementation."""
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort_basic(arr[:mid])
    right = merge_sort_basic(arr[mid:])
    
    return _merge(left, right)

def _merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_advanced(arr: List[int]) -> None:
    """Advanced in-place-like implementation (modifies original list)."""
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort_advanced(L)
        merge_sort_advanced(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

"""
Performance Analysis:
- Time Complexity: O(n log n) in all cases.
- Space Complexity: O(n) for the auxiliary array.

Edge Cases:
- Empty array or single-element array.
- Already sorted array.
- Reverse sorted array.
- Array with all identical elements.

Interview Challenge:
Count the number of inversions in an array using merge sort.
"""

def test_merge_sort():
    arr1 = [38, 27, 43, 3, 9, 82, 10]
    res1 = merge_sort_basic(arr1)
    assert res1 == sorted(arr1)
    
    arr2 = [38, 27, 43, 3, 9, 82, 10]
    merge_sort_advanced(arr2)
    assert arr2 == sorted(arr1)
    print("All tests passed.")

if __name__ == "__main__":
    test_merge_sort()
