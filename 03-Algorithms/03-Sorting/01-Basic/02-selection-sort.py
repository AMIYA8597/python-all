"""
# ==============================================================================
# LABORATORY: SELECTION SORT & DOUBLE SELECTION SORT
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Selection Sort operates in O(N^2) time. It scans the array, finds the minimum, 
# and swaps it to the front. 
# 
# But think mathematically: if we are already spending O(N) time scanning the 
# entire remaining array to find the minimum... why don't we find the MAXIMUM at 
# the exact same time, and swap it to the end?
#
# This is called "Double Selection Sort" (or Cocktail Selection Sort). 
# By finding both the Min and the Max in a single pass, we cut the total number 
# of iterations in EXACTLY half! 
# 
# While it is mathematically still O(N^2) according to Big-O notation, it runs 
# 2x faster in the real world. This demonstrates how algorithmic optimizations 
# can squeeze performance out of naive logic.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement Standard Selection Sort.
# - Implement Double (Bidirectional) Selection Sort.
# - Understand the insidious edge case when Min and Max overlap during swaps.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD SELECTION SORT (RECAP)
# ==============================================================================
def standard_selection_sort(arr: List[int]) -> List[int]:
    """
    Time Complexity: O(N^2)
    Space Complexity: O(1)
    """
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ==============================================================================
# 4. DOUBLE SELECTION SORT (MIN-MAX SORT)
# ==============================================================================
def double_selection_sort(arr: List[int]) -> List[int]:
    """
    Finds BOTH the minimum and maximum in the same pass.
    Cuts the number of loops from N to N/2.
    """
    left = 0
    right = len(arr) - 1
    
    # We loop until the left and right pointers meet in the middle
    while left < right:
        min_idx = left
        max_idx = left
        
        # Scan the unsorted window to find BOTH min and max
        for i in range(left, right + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            if arr[i] > arr[max_idx]:
                max_idx = i
                
        # 1. Swap the minimum to the front of the window
        arr[left], arr[min_idx] = arr[min_idx], arr[left]
        
        # THE DEADLY EDGE CASE:
        # What if the MAXIMUM element was sitting at the `left` index?
        # We just swapped `arr[left]` with `arr[min_idx]`!
        # This means the maximum element has been MOVED. It is now sitting at `min_idx`.
        # If we don't update `max_idx`, we will accidentally swap the wrong number to the end!
        if max_idx == left:
            max_idx = min_idx
            
        # 2. Swap the maximum to the end of the window
        arr[right], arr[max_idx] = arr[max_idx], arr[right]
        
        # Shrink the window from both sides
        left += 1
        right -= 1
        
    return arr

def demonstrate_double_selection():
    section_header("Algorithm: Double Selection Sort")
    
    arr = [23, 78, 45, 8, 32, 56, 1]
    print(f"Initial Unsorted Array: {arr}\n")
    
    sorted_arr = double_selection_sort(arr.copy())
    
    print(f"Final Sorted Array: {sorted_arr}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Does Double Selection Sort change the Big-O Time Complexity?
   Answer: NO. Standard Selection Sort takes $(N^2)/2$ operations. Double Selection Sort takes $(N^2)/4$ operations. In Big-O notation, we drop all constants and fractions, so they are both $O(N^2)$. However, in actual clock time, Double Selection is twice as fast.

2. Why is the edge-case check `if max_idx == left: max_idx = min_idx` strictly required?
   Answer: Because we do the swaps sequentially. First, we swap the Minimum to the `left`. If the Maximum happened to be located exactly at the `left` index originally, it just got physically moved to wherever the Minimum used to be! We must update the `max_idx` pointer to point to this new location before executing the second swap, otherwise we lose the maximum value.
"""

if __name__ == "__main__":
    demonstrate_double_selection()
    print("\n[SUCCESS] Laboratory: Double Selection Sort Completed.")
