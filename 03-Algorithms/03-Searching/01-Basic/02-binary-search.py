"""
# ==============================================================================
# LABORATORY: BINARY SEARCH (EDGE CASES & BIAS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Although the basic idea of binary search is comparatively straightforward, 
# the details can be surprisingly tricky..." - Donald Knuth (The Art of Computer Programming)
#
# Almost everyone can write a basic Binary Search. Almost everyone fails when 
# asked to find the *first* occurrence of a duplicate element, or when asked to 
# avoid infinite loops when the search space shrinks to 2 elements.
#
# This laboratory covers the exact mechanics of Binary Search boundaries (`<` vs `<=`), 
# pointer math (`mid + 1` vs `mid`), and Midpoint Bias (Left-leaning vs Right-leaning).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why `left <= right` is used for basic searches.
# - Understand why `left < right` is used for boundary searches.
# - Master Left-Biased vs Right-Biased Midpoint calculation to avoid infinite loops.
# - Implement `lower_bound` and `upper_bound` manually.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LOWER BOUND (FIND FIRST OCCURRENCE)
# ==============================================================================
def lower_bound(arr: List[int], target: int) -> int:
    """
    Finds the index of the FIRST element that is >= target.
    If target is not found, it returns the index where it SHOULD be inserted.
    
    Notice the loop is `left < right` (no equals).
    """
    left = 0
    right = len(arr) # Notice right is N, not N-1. It represents "Out of Bounds".
    
    while left < right:
        # Standard Left-Biased Midpoint. 
        # If left=0 and right=1, mid will be 0.
        mid = left + (right - left) // 2
        
        if arr[mid] >= target:
            # The target might be exactly at `mid`, OR it might be further left.
            # We CANNOT do `right = mid - 1`, because `mid` might be the correct answer!
            # So we strictly lock `right = mid`.
            right = mid
        else:
            # `arr[mid]` is strictly less than target. The target MUST be to the right.
            # We can safely discard `mid` entirely.
            left = mid + 1
            
    # When the loop breaks, left == right. Both point to the correct answer.
    return left


# ==============================================================================
# 4. UPPER BOUND (FIND LAST OCCURRENCE)
# ==============================================================================
def find_last_occurrence(arr: List[int], target: int) -> int:
    """
    Finds the EXACT index of the LAST occurrence of the target.
    Returns -1 if not found.
    """
    left = 0
    right = len(arr) - 1
    
    while left < right:
        # THE INFINITE LOOP TRAP:
        # If we use standard `mid = left + (right - left) // 2` (Left-Biased),
        # and we have [5, 5] (left=0, right=1), mid will be 0.
        # If arr[mid] == target, we set `left = mid` (left = 0).
        # The next loop: left=0, right=1. Mid is 0 again. INFINITE LOOP!
        
        # THE FIX: RIGHT-BIASED MIDPOINT
        # Add 1 before dividing. If left=0, right=1, mid becomes 1.
        mid = left + (right - left + 1) // 2
        
        if arr[mid] <= target:
            # The target might be at `mid`, OR it might be further right.
            # Lock `left = mid`. (This is why we needed the Right-Biased mid).
            left = mid
        else:
            # `arr[mid]` is strictly greater. Target must be left.
            right = mid - 1
            
    # Verification step
    if left < len(arr) and arr[left] == target:
        return left
    return -1


def demonstrate_boundaries():
    section_header("Algorithm: Lower Bound and Last Occurrence")
    
    # Indices: 0  1  2  3  4  5  6  7  8
    arr =    [ 1, 2, 4, 4, 4, 4, 6, 8, 9 ]
    target = 4
    
    print(f"Array: {arr}")
    print(f"Target: {target} (Duplicates exist!)")
    
    first = lower_bound(arr, target)
    print(f"\nLower Bound (First Occurrence): Index {first} (Expected: 2)")
    
    last = find_last_occurrence(arr, target)
    print(f"Last Occurrence: Index {last} (Expected: 5)")
    
    # Counting duplicates using Binary Search math
    count = last - first + 1
    print(f"Total occurrences calculated in O(log N) time: {count}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `left < right` guarantee termination without an infinite loop in `lower_bound`?
   Answer: Because we use a Left-Biased midpoint (`mid = left + (right - left) // 2`). This guarantees that `mid` is always strictly less than `right`. Therefore, the assignment `right = mid` mathematically shrinks the search space by at least 1 element every time.

2. Why do we set `right = len(arr)` instead of `len(arr) - 1` for `lower_bound`?
   Answer: Because we are asking "Where should I insert this target?". If the target is larger than every element in the array (e.g. searching for 99 in `[1, 2, 3]`), it belongs at the very end of the array (Index 3). If `right` was capped at `len(arr) - 1` (Index 2), the algorithm could never return Index 3!

3. When must you use a Right-Biased Midpoint?
   Answer: Whenever your logic contains `left = mid`. If you use a Left-Biased midpoint, and the search space shrinks to 2 elements, `mid` will equal `left`. Assigning `left = mid` does absolutely nothing, causing an infinite loop. A Right-Biased midpoint (`+ 1 // 2`) ensures `mid` equals `right`, forcing `left` to move forward.
"""

if __name__ == "__main__":
    demonstrate_boundaries()
    print("\n[SUCCESS] Laboratory: Binary Search Edge Cases Completed.")
