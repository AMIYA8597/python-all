"""
# ==============================================================================
# LABORATORY: INSERTION SORT & SHELL SORT
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Insertion Sort is O(N^2) in the worst case, but it possesses a magical property: 
# it is "Adaptive". If you feed it an array that is ALREADY mostly sorted, it 
# instantly drops to O(N) time!
#
# Because of this, it is the most frequently executed sorting algorithm in the 
# world. Python's `list.sort()` (Timsort) and Java's `Arrays.sort()` both 
# actively look for small sub-arrays (size 32) and use Insertion Sort on them, 
# completely avoiding the overhead of complex algorithms like Quick Sort.
#
# In 1959, Donald Shell realized that Insertion Sort's only flaw is that it 
# moves elements exactly 1 slot at a time. If a small element is stuck at the 
# end of a massive array, it takes N shifts to move it to the front.
# He invented "Shell Sort" to fix this, shifting elements by a large "Gap" first, 
# then shrinking the gap down to 1.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Adaptive O(N) nature of Insertion Sort.
# - Implement Shell Sort (Diminishing Increment Sort).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ADAPTIVE INSERTION SORT
# ==============================================================================
def insertion_sort(arr: List[int]) -> List[int]:
    """
    Standard Insertion Sort.
    Best Case: O(N) (Array is already sorted)
    Worst Case: O(N^2) (Array is reversed)
    Space: O(1)
    """
    n = len(arr)
    comparisons = 0
    shifts = 0
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        comparisons += 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            shifts += 1
            j -= 1
            if j >= 0: comparisons += 1
            
        arr[j + 1] = key
        
    print(f"Stats: {comparisons} Comparisons, {shifts} Shifts.")
    return arr

def demonstrate_adaptive():
    section_header("Algorithm: Insertion Sort (Adaptive Behavior)")
    
    almost_sorted = [1, 2, 3, 5, 4, 6, 7]
    print(f"Almost Sorted Array: {almost_sorted}")
    print("Running Insertion Sort...")
    insertion_sort(almost_sorted)
    
    reversed_arr = [7, 6, 5, 4, 3, 2, 1]
    print(f"\nReversed Array: {reversed_arr}")
    print("Running Insertion Sort (Worst Case)...")
    insertion_sort(reversed_arr)


# ==============================================================================
# 4. SHELL SORT (OPTIMIZED INSERTION SORT)
# ==============================================================================
def shell_sort(arr: List[int]) -> List[int]:
    """
    Shell Sort: Improves Insertion Sort by comparing elements separated by a "Gap".
    Time Complexity: Depends on the Gap Sequence. (Typically O(N^(3/2)) or O(N log^2 N)).
    Space Complexity: O(1)
    """
    n = len(arr)
    
    # 1. Start with a large gap, usually half the array size
    gap = n // 2
    
    # 2. Keep shrinking the gap until it reaches 0
    while gap > 0:
        
        # 3. Perform a "Gapped" Insertion Sort
        for i in range(gap, n):
            key = arr[i]
            j = i
            
            # Instead of checking the element immediately to the left (j - 1),
            # we check the element a 'gap' distance away (j - gap)!
            while j >= gap and arr[j - gap] > key:
                arr[j] = arr[j - gap]
                j -= gap
                
            arr[j] = key
            
        # 4. Shrink the gap
        gap //= 2
        
    return arr

def demonstrate_shell_sort():
    section_header("Algorithm: Shell Sort")
    
    arr = [35, 33, 42, 10, 14, 19, 27, 44, 26, 31]
    print(f"Initial Unsorted Array: {arr}\n")
    
    sorted_arr = shell_sort(arr)
    print(f"Final Sorted Array: {sorted_arr}")
    print("\nNotice how Shell Sort can rapidly throw a small element from the end of the array to the front using Gaps, instead of shifting it 1 slot at a time.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Python's Timsort use Insertion Sort instead of Selection Sort?
   Answer: Because Insertion Sort is *Adaptive*. If Timsort encounters a chunk of data that is already sorted, Insertion Sort just does 1 comparison per element and immediately stops, finishing in $O(N)$ time. Selection Sort is mathematically forced to scan the entire remaining array every time, always taking $O(N^2)$ regardless of the input.

2. Is Shell Sort Stable?
   Answer: NO. Standard Insertion Sort is stable because it only shifts elements 1 spot at a time. Shell Sort jumps elements across large gaps. If you have two 5s in an array, a gap-jump might accidentally throw the second 5 in front of the first 5, destroying their relative order. Shell sort trades stability for extreme speed.
"""

if __name__ == "__main__":
    demonstrate_adaptive()
    demonstrate_shell_sort()
    print("\n[SUCCESS] Laboratory: Shell Sort Completed.")
