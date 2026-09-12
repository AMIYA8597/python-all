"""
Inversion Counting using Merge Sort.

Learning Objectives:
1. Understand how to count inversions using D&C.
2. Modify merge sort to track cross-inversions.
3. Apply algorithm to practical ranking problems.

Concept Explanation:
An inversion is a pair of indices (i, j) such that i < j and A[i] > A[j].
We can count inversions efficiently while performing Merge Sort. When merging two halves,
if an element from the right half is smaller than an element from the left half,
it forms an inversion with all remaining elements in the left half.
"""

from typing import List, Tuple

def get_inversions_brute(arr: List[int]) -> int:
    """O(n^2) brute force method."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count

def merge_and_count(arr: List[int], temp_arr: List[int], left: int, mid: int, right: int) -> int:
    i = left    
    j = mid + 1 
    k = left    
    inv_count = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            k += 1
            i += 1
        else:
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)
            k += 1
            j += 1

    while i <= mid:
        temp_arr[k] = arr[i]
        k += 1
        i += 1

    while j <= right:
        temp_arr[k] = arr[j]
        k += 1
        j += 1

    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]
        
    return inv_count

def merge_sort_and_count(arr: List[int], temp_arr: List[int], left: int, right: int) -> int:
    inv_count = 0
    if left < right:
        mid = (left + right) // 2

        inv_count += merge_sort_and_count(arr, temp_arr, left, mid)
        inv_count += merge_sort_and_count(arr, temp_arr, mid + 1, right)
        inv_count += merge_and_count(arr, temp_arr, left, mid, right)
        
    return inv_count

def get_inversions_fast(arr: List[int]) -> int:
    """O(n log n) implementation."""
    temp_arr = [0]*len(arr)
    return merge_sort_and_count(arr, temp_arr, 0, len(arr)-1)

"""
Performance Analysis:
- Time Complexity: O(n log n).
- Space Complexity: O(n) for temporary array.

Edge Cases:
- Already sorted array (0 inversions).
- Reverse sorted array (n*(n-1)/2 inversions).
- Arrays with duplicates.

Interview Challenge:
Find the number of reverse pairs where A[i] > 2*A[j] and i < j.
"""

def test_inversions():
    arr = [1, 20, 6, 4, 5]
    assert get_inversions_brute(arr) == 5
    # The fast version modifies array, so we pass a copy
    assert get_inversions_fast(list(arr)) == 5
    print("All tests passed.")

if __name__ == "__main__":
    test_inversions()
