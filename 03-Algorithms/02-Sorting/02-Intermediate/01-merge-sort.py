"""
# ==============================================================================
# LABORATORY: MERGE SORT (DIVIDE & CONQUER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Bubble, Insertion, and Selection sort all take O(N^2) time. If you sort 100,000 
# items, they take 10 Billion operations (seconds/minutes).
# 
# "Merge Sort" breaks the O(N^2) barrier. It was invented by John von Neumann in 
# 1945. It uses the "Divide and Conquer" paradigm.
# 1. Divide the array perfectly in half over and over until you just have arrays 
#    of length 1. (An array of length 1 is mathematically already sorted!).
# 2. Merge those tiny sorted arrays back together, two at a time.
#
# Because merging two sorted arrays takes strictly linear time O(N), and we only 
# split the array log(N) times, the total time is guaranteed O(N log N).
# For 100,000 items, this is only 1.6 Million operations (milliseconds).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Divide and Conquer framework.
# - Understand the Two-Pointer Merge logic.
# - Understand why Merge Sort is Stable.
# - Understand its weakness: O(N) Space Complexity.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MERGE SORT IMPLEMENTATION
# ==============================================================================
def merge_sort(arr: List[int]) -> List[int]:
    """
    Sorts an array using Merge Sort.
    Time Complexity: O(N log N) Best, Average, and Worst case.
    Space Complexity: O(N) (Creates new arrays during the split/merge).
    """
    # 1. BASE CASE
    # If the array has 1 or 0 elements, it is mathematically already sorted!
    if len(arr) <= 1:
        return arr
        
    # 2. DIVIDE
    mid = len(arr) // 2
    
    # We slice the array into two completely new arrays in memory.
    # (Note: In strict C implementations, we pass indices to save memory, 
    # but slicing in Python makes the recursive concept much easier to read).
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    print(f"Dividing: {arr} -> {left_half} and {right_half}")
    
    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)
    
    # 3. CONQUER (MERGE)
    # Merge the two sorted halves back into a single sorted array.
    return merge(left_sorted, right_sorted)


def merge(left: List[int], right: List[int]) -> List[int]:
    """
    The heart of Merge Sort. 
    Takes two ALREADY SORTED arrays, and merges them into a single sorted array 
    in strictly O(N) time using two pointers.
    """
    merged = []
    i = 0 # Pointer for the Left array
    j = 0 # Pointer for the Right array
    
    # While both arrays still have elements left...
    while i < len(left) and j < len(right):
        
        # Compare the two elements at the pointers
        # CRITICAL STABILITY CHECK: We use `<=` instead of `<`.
        # If left[i] and right[j] are EXACTLY EQUAL, we always pick the Left one!
        # This guarantees that elements that originally came first (Left side) 
        # stay first in the final array. This makes Merge Sort STABLE.
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Once one of the arrays is completely empty, the loop breaks.
    # But the OTHER array still has leftover elements!
    # Because those leftover elements are already sorted, we just append them all.
    while i < len(left):
        merged.append(left[i])
        i += 1
        
    while j < len(right):
        merged.append(right[j])
        j += 1
        
    print(f" Merged: {left} and {right} -> {merged}")
    return merged

def demonstrate_merge_sort():
    section_header("Algorithm: Merge Sort Execution")
    
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"Initial Array: {arr}\n")
    
    sorted_arr = merge_sort(arr)
    
    print(f"\nFinal Sorted Array: {sorted_arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Merge Sort take $O(N \\log N)$ time?
   Answer: The array is repeatedly divided in half. You can only divide $N$ in half $\\log_2 N$ times before you reach single elements. Therefore, the "Recursion Tree" is exactly $\\log_2 N$ levels deep. At each level of the tree, the algorithm merges a total of $N$ elements across all the sub-arrays. (Work at each level is $O(N)$) $\\times$ (Total Levels is $\\log_2 N$) = $O(N \\log N)$.

2. What is the major weakness of Merge Sort compared to Quick Sort?
   Answer: Space Complexity. Merge sort CANNOT merge two sub-arrays easily without creating a third, temporary "merged" array in memory. It requires $O(N)$ auxiliary RAM. If you are sorting a 16GB file, you need 32GB of RAM to run Merge Sort. Quick Sort operates strictly "in-place", requiring only $O(\\log N)$ RAM for the call stack.

3. Does Python's `list.sort()` use Merge Sort?
   Answer: It uses **Timsort** (named after Tim Peters). Timsort is a hybrid of Merge Sort and Insertion Sort! It recognizes that real-world data often has small chunks of data that are already partially sorted. It uses Insertion Sort on small chunks (size ~32) because Insertion Sort is incredibly fast for tiny arrays, and then uses Merge Sort to combine those 32-element chunks!
"""

if __name__ == "__main__":
    demonstrate_merge_sort()
    print("\n[SUCCESS] Laboratory: Merge Sort Completed.")
