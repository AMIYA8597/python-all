"""
# ==============================================================================
# LABORATORY: TIMSORT (THE KING OF MODERN SORTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# What algorithm does Python actually use when you call `list.sort()`?
# It doesn't use Quick Sort (unstable, O(N^2) worst-case).
# It doesn't use plain Merge Sort (wastes too much memory, slow for tiny arrays).
# 
# In 2002, Tim Peters invented **Timsort** specifically for Python. It was so 
# astonishingly fast and stable that it became the default sorting algorithm for 
# Java, Android, and V8 (JavaScript) as well!
#
# Timsort is an Adaptive Hybrid algorithm. It recognizes a fundamental truth about 
# real-world data: data is almost NEVER completely random. It usually contains 
# "Runs" (chunks of data that are already partially sorted).
# 
# Timsort scans the array to find these natural Runs. If a Run is backwards 
# (descending), it instantly reverses it! If a Run is too short (e.g. < 32 items), 
# it uses Insertion Sort to forcefully build it up to size 32. 
# Finally, it uses a highly optimized Merge Sort to merge all these chunks together.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Timsort drops to O(N) in the Best Case.
# - Understand the MIN_MERGE threshold (Insertion Sort vs Merge Sort crossover).
# - Implement a basic educational version of Timsort.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TIMSORT SUBROUTINES
# ==============================================================================
# We define MIN_MERGE as 32. Any array smaller than this will be sorted exclusively 
# using Insertion Sort, because recursion/merging overhead is too slow for small N.
MIN_MERGE = 32

def insertion_sort_timsort(arr: List[int], left: int, right: int) -> None:
    """
    Standard Insertion Sort, but modified to operate ONLY on a specific 
    slice of the array from `left` to `right`.
    """
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_timsort(arr: List[int], left: int, mid: int, right: int) -> None:
    """
    Standard Merge algorithm.
    (Note: A true production Timsort uses "Galloping Mode" to skip massive 
    blocks of elements during the merge if one array is much larger. We use a 
    standard merge here for educational clarity).
    """
    # Create temporary copies of the left and right halves
    len1 = mid - left + 1
    len2 = right - mid
    
    left_part = arr[left : left + len1]
    right_part = arr[mid + 1 : mid + 1 + len2]
    
    i = 0
    j = 0
    k = left
    
    # Merge the copies back into the original array
    while i < len1 and j < len2:
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
        
    # Copy remaining elements
    while i < len1:
        arr[k] = left_part[i]
        k += 1
        i += 1
        
    while j < len2:
        arr[k] = right_part[j]
        k += 1
        j += 1


# ==============================================================================
# 4. THE TIMSORT ALGORITHM
# ==============================================================================
def timsort(arr: List[int]) -> List[int]:
    """
    Educational implementation of Timsort.
    Time Complexity: O(N) Best, O(N log N) Average/Worst.
    Space Complexity: O(N) Auxiliary space for merging.
    """
    n = len(arr)
    
    # 1. Chop the array into MIN_MERGE sized chunks, and Insertion Sort them!
    # (If the array is already mostly sorted, Insertion Sort finishes in O(N) time).
    for i in range(0, n, MIN_MERGE):
        # Calculate the boundary of the chunk
        right_boundary = min((i + MIN_MERGE - 1), (n - 1))
        insertion_sort_timsort(arr, i, right_boundary)
        
    # 2. Start merging the chunks together!
    # Chunk size starts at MIN_MERGE. We double it every pass.
    size = MIN_MERGE
    
    while size < n:
        for left in range(0, n, 2 * size):
            
            # Find the midpoint (where the left chunk ends)
            mid = left + size - 1
            
            # Find the rightmost boundary
            right = min((left + 2 * size - 1), (n - 1))
            
            # If the midpoint is beyond the array boundary, there is no right 
            # chunk to merge with! We can skip.
            if mid < right:
                merge_timsort(arr, left, mid, right)
                
        # Double the chunk size
        size *= 2
        
    return arr

def demonstrate_timsort():
    section_header("Algorithm: Timsort (Insertion + Merge Hybrid)")
    
    # Let's generate a list of 100 elements
    import random
    arr = [random.randint(1, 1000) for _ in range(100)]
    
    print(f"Initial Unsorted Array (First 20): {arr[:20]} ...")
    print("Executing Timsort...")
    
    # Sort
    timsort(arr)
    
    print(f"\nFinal Sorted Array (First 20): {arr[:20]} ...")
    
    # Verify correctness
    print(f"\nVerification (Python's built-in sorted()): {arr == sorted(arr)}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Timsort guarantee $O(N)$ Best Case, while Merge Sort is always $O(N \\log N)$?
   Answer: Because Timsort uses Insertion Sort for the foundational chunks! If you feed Timsort an array that is already perfectly sorted, the Insertion Sort pass does 1 comparison per element and finishes in exactly $O(N)$ time. Then, during the Merge phase, Timsort realizes there is only 1 massive sorted chunk, and completely skips the merge logic. Plain Merge Sort blindly divides and reconstructs the array regardless of its initial state.

2. What is "Galloping Mode" in a production Timsort?
   Answer: When merging two arrays, if Timsort notices that it has pulled 7 elements *in a row* from the Left array, it assumes the Left array is currently full of much smaller numbers. It activates "Galloping Mode" and uses Exponential Search ($O(\\log K)$) to find exactly how many more elements from the Left array it can safely pull in one massive chunk, instead of checking them 1 by 1.

3. Why is MIN_MERGE usually set between 32 and 64?
   Answer: It is mathematically proven that Insertion Sort is faster than Merge/Quick Sort for arrays smaller than ~45 elements, due to having zero recursive overhead and tiny constant factors. Picking a power of 2 (like 32) ensures that the subsequent Merge trees are perfectly balanced.
"""

if __name__ == "__main__":
    demonstrate_timsort()
    print("\n[SUCCESS] Laboratory: Timsort Completed.")
