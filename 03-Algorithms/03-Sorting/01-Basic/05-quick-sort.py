"""
# ==============================================================================
# LABORATORY: HOARE'S QUICK SORT & QUICK SELECT
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Previously, we learned the "Lomuto" Partition Scheme for Quick Sort. It is 
# easy to teach and easy to code. However, Tony Hoare (the inventor of Quick Sort) 
# designed a different partitioning scheme that is mathematically superior.
#
# "Hoare's Partition Scheme" uses two pointers starting at opposite ends of the 
# array, moving towards each other. It performs exactly 3x FEWER swaps than 
# Lomuto! In performance-critical systems (like the C++ Standard Library), 
# Hoare's scheme is always preferred.
#
# Furthermore, what if you don't want to sort the array? What if the interview 
# asks: "Find the 5th Largest element in this array"?
# If you sort it, it takes O(N log N) time.
# But we can hack Quick Sort's partition logic to find the Kth element in 
# strictly O(N) time! This algorithm is called "Quick Select".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Hoare's Partition Scheme.
# - Understand why Hoare is faster but trickier.
# - Implement Quick Select to find the K-th smallest/largest element in O(N).
#
# ==============================================================================
"""

import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HOARE'S PARTITION SCHEME
# ==============================================================================
def hoare_partition(arr: List[int], low: int, high: int) -> int:
    """
    Tony Hoare's original partition scheme.
    Uses two pointers converging to the middle.
    Returns the index where the array is partitioned. 
    WARNING: Unlike Lomuto, the returned index is NOT necessarily the final 
    locked position of the pivot! It is just a valid splitting boundary.
    """
    # Pick the first element as the pivot
    pivot = arr[low]
    
    # Initialize pointers slightly outside the bounds
    i = low - 1
    j = high + 1
    
    while True:
        # Move the left pointer forward until it finds an element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
            
        # Move the right pointer backward until it finds an element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
            
        # If the pointers cross, the partition is complete!
        # Return the right pointer as the boundary.
        if i >= j:
            return j
            
        # The pointers stopped on elements that are on the WRONG SIDE of the pivot.
        # Swap them to put them on the correct sides!
        arr[i], arr[j] = arr[j], arr[i]


def quick_sort_hoare(arr: List[int], low: int, high: int) -> None:
    if low < high:
        # Partition and get the boundary
        boundary = hoare_partition(arr, low, high)
        
        # NOTE THE DIFFERENCE:
        # Lomuto locks the pivot, so we do (low, pivot-1) and (pivot+1, high).
        # Hoare DOES NOT guarantee the pivot is locked exactly at `boundary`.
        # So we MUST include `boundary` in the left side.
        quick_sort_hoare(arr, low, boundary)
        quick_sort_hoare(arr, boundary + 1, high)

def demonstrate_hoare():
    section_header("Algorithm: Quick Sort (Hoare Partition)")
    
    arr = [9, -3, 5, 2, 6, 8, -6, 1, 3]
    print(f"Initial Unsorted: {arr}")
    
    quick_sort_hoare(arr, 0, len(arr) - 1)
    print(f"Final Sorted:     {arr}")


# ==============================================================================
# 4. QUICK SELECT (O(N) K-th ELEMENT)
# ==============================================================================
def quick_select(arr: List[int], low: int, high: int, k: int) -> int:
    """
    Finds the K-th SMALLEST element in an array in O(N) expected time.
    (If K=0, it finds the absolute minimum).
    
    We use the LOMUTO partition here because we NEED the pivot to be locked 
    into its final, exact index to know if we found K!
    """
    # Randomize the pivot to prevent O(N^2) worst case
    pivot_idx = random.randint(low, high)
    arr[high], arr[pivot_idx] = arr[pivot_idx], arr[high]
    
    # Standard Lomuto Partition
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Lock the pivot in place
    locked_idx = i + 1
    arr[locked_idx], arr[high] = arr[high], arr[locked_idx]
    
    # THE MAGIC OF QUICK SELECT:
    if locked_idx == k:
        # We got incredibly lucky! The pivot landed exactly on the Kth index.
        # We are completely done!
        return arr[locked_idx]
        
    elif locked_idx > k:
        # The pivot landed to the RIGHT of K.
        # We only need to search the LEFT half! We completely ignore the right half.
        return quick_select(arr, low, locked_idx - 1, k)
        
    else:
        # The pivot landed to the LEFT of K.
        # We only need to search the RIGHT half!
        return quick_select(arr, locked_idx + 1, high, k)

def demonstrate_quick_select():
    section_header("Algorithm: Quick Select (Kth Smallest)")
    
    arr = [10, 4, 5, 8, 6, 11, 26]
    print(f"Array: {arr}")
    
    # We want the 3rd smallest. (Indices: 0=1st, 1=2nd, 2=3rd).
    # So K = 2.
    k_index = 2
    
    # Notice we pass a COPY of the array, because Quick Select scrambles it!
    ans = quick_select(arr.copy(), 0, len(arr) - 1, k_index)
    
    print(f"\nLooking for K-Index {k_index} (The {k_index+1}rd smallest)")
    print(f"Result: {ans}")
    
    # Verify manually
    sorted_arr = sorted(arr)
    print(f"Verification -> Sorted array is: {sorted_arr}")
    print(f"Index {k_index} is indeed: {sorted_arr[k_index]}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Hoare's Partition faster than Lomuto's?
   Answer: Lomuto moves one pointer from left to right, doing a swap every single time it finds an element smaller than the pivot. If an array is already sorted, Lomuto will literally swap every element with itself, wasting CPU cycles. Hoare moves two pointers from opposite sides and ONLY swaps when both pointers find an element on the wrong side. Mathematically, Hoare performs 3x fewer swaps.

2. Why do we use Lomuto for Quick Select instead of Hoare?
   Answer: Because Quick Select requires the pivot to be locked into its *exact, final index* so we can compare it to `K`. Hoare's partition does not guarantee the pivot is locked in the correct place; it just guarantees a valid dividing line. 

3. Why is Quick Select $O(N)$ time instead of $O(N \\log N)$?
   Answer: In Quick Sort, you must recursively process BOTH halves of the array. In Quick Select, you instantly throw away half of the array! The work done is $N + N/2 + N/4 + N/8...$ which mathematically converges to strictly $2N$. Thus, it is $O(N)$.
"""

if __name__ == "__main__":
    demonstrate_hoare()
    demonstrate_quick_select()
    print("\n[SUCCESS] Laboratory: Advanced Quick Sort Completed.")
