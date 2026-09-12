"""
Maximum Subarray Problem using Divide and Conquer.

Learning Objectives:
1. Solve the maximum subarray problem using divide and conquer.
2. Compare with Kadane's algorithm.
3. Understand crossing subarrays.

Concept Explanation:
Find the contiguous subarray within a one-dimensional array of numbers which has the largest sum.
Using D&C, we divide the array into two halves, find max subarray in left half, right half,
and crossing the midpoint.
"""

from typing import List, Tuple

def max_crossing_sum(arr: List[int], low: int, mid: int, high: int) -> int:
    left_sum = float('-inf')
    sm = 0
    for i in range(mid, low - 1, -1):
        sm += arr[i]
        if sm > left_sum:
            left_sum = sm

    right_sum = float('-inf')
    sm = 0
    for i in range(mid + 1, high + 1):
        sm += arr[i]
        if sm > right_sum:
            right_sum = sm

    return left_sum + right_sum

def max_subarray_dc(arr: List[int], low: int, high: int) -> int:
    """Divide and conquer implementation."""
    if low == high:
        return arr[low]

    mid = (low + high) // 2

    return max(
        max_subarray_dc(arr, low, mid),
        max_subarray_dc(arr, mid + 1, high),
        max_crossing_sum(arr, low, mid, high)
    )

def max_subarray_kadane(arr: List[int]) -> int:
    """Advanced Kadane's algorithm O(n) for comparison."""
    max_so_far = float('-inf')
    current_max = 0
    for i in range(len(arr)):
        current_max += arr[i]
        if max_so_far < current_max:
            max_so_far = current_max
        if current_max < 0:
            current_max = 0
    return max_so_far

"""
Performance Analysis:
- D&C Time Complexity: O(n log n).
- Kadane's Time Complexity: O(n).
- Space Complexity: O(log n) for D&C stack.

Edge Cases:
- All negative numbers.
- Empty array.
- Single element array.

Interview Challenge:
Find the indices of the maximum subarray.
"""

def test_max_subarray():
    arr = [-2, -5, 6, -2, -3, 1, 5, -6]
    assert max_subarray_dc(arr, 0, len(arr) - 1) == 7
    assert max_subarray_kadane(arr) == 7
    print("All tests passed.")

if __name__ == "__main__":
    test_max_subarray()
