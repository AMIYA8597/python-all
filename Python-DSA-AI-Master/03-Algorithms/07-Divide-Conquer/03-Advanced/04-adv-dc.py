"""
Advanced Divide and Conquer Patterns.

Learning Objectives:
1. Recognize problems solvable by median of medians (selection algorithm).
2. Understand Master Theorem applications.
3. Solve complex sequence problems.

Concept Explanation:
We'll implement a deterministic O(n) selection algorithm (Median of Medians) to find
the k-th smallest element. This avoids the O(n^2) worst case of QuickSelect.
"""

from typing import List

def get_median(arr: List[int]) -> int:
    arr.sort()
    return arr[len(arr) // 2]

def kth_smallest(arr: List[int], l: int, r: int, k: int) -> int:
    """Deterministic selection using Median of Medians."""
    if k > 0 and k <= r - l + 1:
        n = r - l + 1
        
        # Divide arr[] in groups of size 5
        median = []
        i = 0
        while i < n // 5:
            median.append(get_median(arr[l + i*5 : l + i*5 + 5]))
            i += 1
            
        # For last group with less than 5 elements
        if i * 5 < n:
            median.append(get_median(arr[l + i*5 : l + i*5 + n % 5]))
            i += 1
            
        # Find median of all medians using recursive call
        if i == 1:
            med_of_med = median[0]
        else:
            med_of_med = kth_smallest(median, 0, i - 1, i // 2)

        # Partition array around med_of_med
        pos = partition(arr, l, r, med_of_med)
        
        # If position is same as k
        if pos - l == k - 1:
            return arr[pos]
        if pos - l > k - 1:  # If position is more, recur for left
            return kth_smallest(arr, l, pos - 1, k)
            
        # Else recur for right subarray
        return kth_smallest(arr, pos + 1, r, k - pos + l - 1)
        
    return 10**9

def partition(arr: List[int], l: int, r: int, x: int) -> int:
    for i in range(l, r):
        if arr[i] == x:
            arr[i], arr[r] = arr[r], arr[i]
            break
            
    x = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] <= x:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[r] = arr[r], arr[i]
    return i

"""
Performance Analysis:
- Time Complexity: O(n) deterministic worst-case time.
- Space Complexity: O(log n) for recursion stack and medians array.

Edge Cases:
- Small arrays.
- Array with all duplicates.

Interview Challenge:
Why use groups of 5? What happens if you use groups of 3 or 7?
"""

def test_adv_dc():
    arr = [12, 3, 5, 7, 4, 19, 26]
    n = len(arr)
    k = 3
    # 3rd smallest is 5 (sorted: 3, 4, 5, 7, 12, 19, 26)
    assert kth_smallest(arr, 0, n - 1, k) == 5
    
    k = 7
    assert kth_smallest(arr, 0, n - 1, k) == 26
    print("All tests passed.")

if __name__ == "__main__":
    test_adv_dc()
