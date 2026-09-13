"""
# ==============================================================================
# LABORATORY: INTROSORT (INTROSPECTIVE SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Quick Sort is incredibly fast on average, but if a hacker feeds it a maliciously 
# crafted array, it degrades to O(N^2) time, crashing the server.
# Heap Sort is mathematically guaranteed to always finish in O(N log N) time, but 
# it has terrible CPU cache performance and is slow in practice.
# Insertion Sort is O(N^2), but it is blazing fast for arrays smaller than 16 items.
#
# Can we combine all three into the ultimate sorting algorithm?
# Yes! Invented by David Musser in 1997, "Introsort" (Introspective Sort) is the 
# default algorithm used in C++ (`std::sort`).
#
# 1. It starts by running Quick Sort.
# 2. It tracks its own recursion depth. If the recursion goes deeper than `2 * log2(N)`, 
#    the algorithm "introspects" (realizes it is being attacked by a worst-case 
#    input), instantly aborts Quick Sort, and switches to Heap Sort to guarantee 
#    an O(N log N) finish!
# 3. If a sub-array shrinks below 16 items, it stops sorting it entirely!
# 4. At the very end, it runs one massive Insertion Sort over the nearly-sorted 
#    array, finishing it in O(N) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of pure Quick Sort.
# - Understand the exact mathematical threshold for switching algorithms.
# - Implement a basic version of Introsort.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE THREE SUBROUTINES
# ==============================================================================
def insertion_sort(arr: List[int], low: int, high: int) -> None:
    """Standard Insertion Sort for small subarrays or the final pass."""
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def partition(arr: List[int], low: int, high: int) -> int:
    """Standard Lomuto Partition for Quick Sort."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def sift_down(arr: List[int], start: int, end: int, root: int) -> None:
    """Standard Sift Down for Heap Sort."""
    largest = root
    left = 2 * root + 1 - start # Offset calculation because we are sorting a subarray
    right = 2 * root + 2 - start
    
    # Absolute index in the array
    abs_left = start + left
    abs_right = start + right
    abs_root = start + root
    
    if abs_left <= end and arr[abs_left] > arr[start + largest]:
        largest = left
    if abs_right <= end and arr[abs_right] > arr[start + largest]:
        largest = right
        
    if largest != root:
        arr[abs_root], arr[start + largest] = arr[start + largest], arr[abs_root]
        sift_down(arr, start, end, largest)

def heap_sort(arr: List[int], low: int, high: int) -> None:
    """In-place Heap Sort restricted to a specific subarray."""
    n = high - low + 1
    # Build Max Heap
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, low, high, i)
        
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[low], arr[low + i] = arr[low + i], arr[low]
        sift_down(arr, low, low + i - 1, 0)


# ==============================================================================
# 4. THE INTROSORT ALGORITHM
# ==============================================================================
def introsort_recursive(arr: List[int], low: int, high: int, max_depth: int) -> None:
    """
    The core recursive engine.
    Switches between Quick Sort and Heap Sort dynamically.
    """
    n = high - low + 1
    
    # 1. INSERTION SORT THRESHOLD
    # If the chunk is smaller than 16 items, we don't sort it!
    # We leave it slightly unsorted. We will fix it at the very end.
    if n <= 16:
        return
        
    # 2. HEAP SORT THRESHOLD (INTROSPECTION)
    # If our recursion has gone too deep, Quick Sort has gone rogue.
    # Kill the Quick Sort and switch to Heap Sort immediately!
    if max_depth == 0:
        print(f" [Introsort] Maximum recursion depth reached at size {n}. Switching to Heap Sort!")
        heap_sort(arr, low, high)
        return
        
    # 3. STANDARD QUICK SORT
    # If everything is fine, keep doing Quick Sort.
    pivot_idx = partition(arr, low, high)
    
    # Notice we subtract 1 from max_depth to track the recursion limit!
    introsort_recursive(arr, low, pivot_idx - 1, max_depth - 1)
    introsort_recursive(arr, pivot_idx + 1, high, max_depth - 1)


def introsort(arr: List[int]) -> List[int]:
    """
    The main wrapper function.
    Calculates the mathematical threshold, calls the engine, and finishes with Insertion Sort.
    """
    n = len(arr)
    if n <= 1:
        return arr
        
    # Mathematical threshold: 2 * log2(N)
    max_depth = 2 * math.floor(math.log2(n))
    print(f"Calculated Max Recursion Depth: {max_depth}")
    
    # Phase 1: Quick Sort / Heap Sort engine
    introsort_recursive(arr, 0, n - 1, max_depth)
    
    # Phase 2: Final Insertion Sort pass
    # Because all elements are within 16 indices of their final position, 
    # Insertion Sort will finish this massive array in almost strict O(N) time!
    print(" [Introsort] Running final O(N) Insertion Sort over the entire array...")
    insertion_sort(arr, 0, n - 1)
    
    return arr


def demonstrate_introsort():
    section_header("Algorithm: Introsort (C++ std::sort)")
    
    # We will generate a malicious "Reverse Sorted" array to intentionally 
    # trigger the Quick Sort worst-case scenario and force the Heap Sort switch!
    arr = list(range(200, 0, -1))
    
    print(f"Malicious Array (Reverse Sorted, Size {len(arr)})\n")
    
    introsort(arr)
    
    print(f"\nFinal Sorted Array (First 20 items): {arr[:20]} ...")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the "Introspective" part of Introsort actually mean?
   Answer: It means the algorithm "looks at itself" while running. It tracks its own recursion depth state variable. If the depth exceeds a mathematical limit, it detects that it is performing poorly and changes its own strategy mid-execution.

2. Why do we skip sorting arrays smaller than 16, and run a massive Insertion Sort at the end? Why not just Insertion Sort them immediately?
   Answer: It is an optimization for the CPU Instruction Cache. Calling `insertion_sort()` thousands of times recursively for every tiny array adds massive function-call overhead. By just `return`ing out of the tiny arrays, we skip the overhead. Running exactly ONE massive `insertion_sort()` at the very end on the entire array is vastly faster, and because no element is more than 16 slots away from its true position, it still runs in $O(N)$ time.

3. Why did Python switch from Introsort to Timsort?
   Answer: Introsort is an Unstable sort (because both Quick Sort and Heap Sort are Unstable). C++ doesn't care about stability by default (`std::stable_sort` is a separate function). Python explicitly wanted its default `list.sort()` to be Stable. Timsort is Stable, and performs exceptionally well on partially-sorted data, making it better for high-level language workloads.
"""

if __name__ == "__main__":
    demonstrate_introsort()
    print("\n[SUCCESS] Laboratory: Introsort Completed.")
