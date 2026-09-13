"""
# ==============================================================================
# LABORATORY: QUICK SORT (IN-PLACE DIVIDE & CONQUER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Merge Sort solves the O(N^2) problem, guaranteeing O(N log N).
# However, Merge Sort requires O(N) auxiliary memory. If you are sorting a 16GB 
# database, Merge Sort requires an extra 16GB of RAM to run.
#
# "Quick Sort" (invented by Tony Hoare in 1959) solves this. It sorts the array 
# strictly "In-Place" by swapping elements mathematically. It requires ZERO extra RAM 
# (aside from the tiny call stack).
# 
# It works by picking a "Pivot" element. It then dynamically scans the array and 
# throws everything smaller than the pivot to the left, and everything larger to 
# the right. The pivot is now perfectly locked into its final, correct position! 
# It then recursively calls Quick Sort on the left side and the right side.
#
# In practice, Quick Sort is almost always 2x to 3x FASTER than Merge Sort because 
# swapping elements in a single contiguous array is incredibly cache-friendly for 
# modern CPUs.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Partitioning logic (Lomuto vs Hoare).
# - Understand why it sorts In-Place.
# - Understand the Malicious Worst-Case O(N^2) flaw and how to fix it with Randomization.
# - Understand why it is Unstable.
#
# ==============================================================================
"""

import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LOMUTO PARTITION SCHEME
# ==============================================================================
def partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto Partition Scheme (Simpler to understand).
    1. Picks the very LAST element as the pivot.
    2. Maintains an index `i` that marks the boundary of the "Smaller than pivot" zone.
    3. Scans through the array. If it finds a small element, it swaps it into the zone.
    """
    pivot_value = arr[high]
    
    # `i` points to the last known position of the "Smaller" zone.
    # Initially, the zone is empty, so it points outside the boundary (low - 1).
    i = low - 1
    
    for j in range(low, high):
        # If the current element is smaller than or equal to the pivot...
        if arr[j] <= pivot_value:
            # Expand the "Smaller" zone by 1
            i += 1
            # Swap the small element into the zone!
            arr[i], arr[j] = arr[j], arr[i]
            
    # The scan is complete.
    # `i` points to the last element smaller than the pivot.
    # Therefore, `i + 1` is the exact spot the pivot belongs!
    # Swap the pivot into its final, permanent resting place.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Return the exact index of the permanently locked pivot.
    return i + 1


def quick_sort(arr: List[int], low: int, high: int) -> None:
    """
    Sorts an array strictly IN-PLACE.
    Average Time: O(N log N).
    Worst Time: O(N^2) (If array is already sorted and we pick the last element!).
    Space: O(log N) (Call stack only).
    """
    if low < high:
        # Partition the array and get the final locked index of the pivot
        pivot_index = partition(arr, low, high)
        
        # Recursively Quick Sort the left sub-array (everything smaller)
        quick_sort(arr, low, pivot_index - 1)
        
        # Recursively Quick Sort the right sub-array (everything larger)
        quick_sort(arr, pivot_index + 1, high)


def demonstrate_quick_sort():
    section_header("Algorithm: Quick Sort (Lomuto Partition)")
    
    arr = [10, 80, 30, 90, 40, 50, 70]
    print(f"Initial Unsorted Array: {arr}\n")
    
    # Pass the lowest index (0) and highest index (len - 1)
    quick_sort(arr, 0, len(arr) - 1)
    
    print(f"Final Sorted Array: {arr}")


# ==============================================================================
# 4. THE RANDOMIZED FIX (LAS VEGAS PARADIGM)
# ==============================================================================
def randomized_partition(arr: List[int], low: int, high: int) -> int:
    """
    Fixes the O(N^2) worst-case flaw of Quick Sort!
    """
    # If the array is already sorted, picking the last element as the pivot is fatal.
    # It partitions the array into [N-1 elements] and [0 elements], causing an O(N^2) degrade.
    #
    # THE FIX: Pick a completely RANDOM index, and swap it with the last element!
    # By making the pivot purely random, we destroy any malicious input pattern.
    random_pivot_index = random.randint(low, high)
    arr[random_pivot_index], arr[high] = arr[high], arr[random_pivot_index]
    
    # Now run the exact same Lomuto partition
    return partition(arr, low, high)


def randomized_quick_sort(arr: List[int], low: int, high: int) -> None:
    """Guarantees Expected O(N log N) time, regardless of how the input is formatted."""
    if low < high:
        pivot_index = randomized_partition(arr, low, high)
        randomized_quick_sort(arr, low, pivot_index - 1)
        randomized_quick_sort(arr, pivot_index + 1, high)

def demonstrate_randomized_quick_sort():
    section_header("Algorithm: Randomized Quick Sort")
    
    arr = [5, 4, 3, 2, 1]
    print(f"Malicious Array (Reverse Sorted): {arr}")
    print("Standard QuickSort would degrade to O(N^2) here.")
    
    randomized_quick_sort(arr, 0, len(arr) - 1)
    
    print(f"Randomized QuickSort easily handles it in O(N log N): {arr}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Quick Sort faster than Merge Sort in the real world, despite both being $O(N \\log N)$?
   Answer: CPU Cache (Locality of Reference). Quick Sort swaps elements within a single, contiguous array. The CPU L1 cache grabs massive chunks of the array at once, resulting in almost zero cache misses. Merge Sort constantly copies data back and forth between two completely different arrays in RAM, causing heavy cache misses and slow memory allocations.

2. Why is Quick Sort UNSTABLE?
   Answer: During the Partition step, if `arr[j]` is smaller than the pivot, it is immediately swapped with `arr[i]`. This is a "Long-Distance Swap". It violently throws the element across the array, completely destroying the original relative order of any duplicate elements that happen to be caught in the crossfire. (Merge sort is stable because it only compares adjacent elements during the merge).

3. What is the Hoare Partition Scheme?
   Answer: Tony Hoare's original partition algorithm uses TWO pointers (one at the beginning moving right, one at the end moving left). They stop when they find an element that belongs on the other side, and swap them. It is mathematically 3x faster than the Lomuto scheme (fewer swaps), but much harder to code correctly without creating infinite loops. (We taught Lomuto above because it is the industry standard for interviews).
"""

if __name__ == "__main__":
    demonstrate_quick_sort()
    demonstrate_randomized_quick_sort()
    print("\n[SUCCESS] Laboratory: Quick Sort Completed.")
