"""
# ==============================================================================
# LABORATORY: HEAP SORT (O(N log N) IN-PLACE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned the two most famous sorting algorithms:
# - Merge Sort: Guarantees O(N log N) time, but wastes O(N) memory.
# - Quick Sort: Uses O(1) memory, but has a catastrophic O(N^2) worst-case time.
#
# Is there a "Holy Grail" algorithm that guarantees O(N log N) time AND strictly 
# uses O(1) In-Place memory?
# Yes. It's called "Heap Sort" (invented by J.W.J. Williams in 1964).
#
# Heap Sort temporarily converts the input array into a "Max Heap" data structure 
# in-place. The absolute largest element is now mathematically guaranteed to be 
# sitting at index 0. 
# It swaps index 0 with the last element, shrinks the "Heap Boundary", and fixes 
# the heap. It repeats this until the array is perfectly sorted!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to represent a Binary Tree in an Array.
# - Implement the O(N) `build_max_heap` algorithm.
# - Implement the Heap Sort loop.
# - Understand why it is mathematically superior, but practically slower.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HEAP SORT IMPLEMENTATION
# ==============================================================================
def sift_down(arr: List[int], n: int, i: int) -> None:
    """
    Sifts a node down to its proper place to maintain the Max-Heap property.
    `n` is the size of the heap.
    `i` is the index of the node we are sifting down.
    Time Complexity: O(log N)
    """
    largest = i
    left_child = 2 * i + 1
    right_child = 2 * i + 2
    
    # Check if left child exists and is greater than the current node
    if left_child < n and arr[left_child] > arr[largest]:
        largest = left_child
        
    # Check if right child exists and is greater than the current largest
    if right_child < n and arr[right_child] > arr[largest]:
        largest = right_child
        
    # If the largest is NOT the current node, we must swap them!
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # The node has been swapped downwards. 
        # We must recursively sift it down further!
        sift_down(arr, n, largest)


def heap_sort(arr: List[int]) -> List[int]:
    """
    Time Complexity: O(N log N) Best, Average, and Worst.
    Space Complexity: O(1) In-Place.
    """
    n = len(arr)
    
    # 1. BUILD THE MAX HEAP (O(N) Time)
    # We only need to sift down the non-leaf nodes.
    # The last non-leaf node is mathematically always at `(n // 2) - 1`.
    # We sift them down backwards, all the way to index 0.
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)
        
    print(f" Array converted to Max-Heap: {arr}")
    print(" (Notice the maximum element is sitting at Index 0!)")
    
    # 2. EXTRACT ELEMENTS ONE BY ONE (O(N log N) Time)
    # We start at the very last index, and work our way backwards to index 1.
    for i in range(n - 1, 0, -1):
        
        # The absolute largest element is at index 0.
        # Swap it with the element at index `i` (throwing the max to the back).
        arr[0], arr[i] = arr[i], arr[0]
        
        # The element at index `i` is now locked! It is in its final sorted position.
        # We now have a broken heap at index 0.
        # Sift index 0 down, but limit the heap size to `i` (ignoring the locked elements at the back).
        sift_down(arr, i, 0)
        
    return arr

def demonstrate_heap_sort():
    section_header("Algorithm: Heap Sort")
    
    arr = [12, 11, 13, 5, 6, 7]
    print(f"Initial Unsorted Array: {arr}\n")
    
    sorted_arr = heap_sort(arr)
    
    print(f"\nFinal Sorted Array: {sorted_arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. If Heap Sort guarantees $O(N \\log N)$ time and $O(1)$ space, why does Python use Timsort and C++ use Introsort (Quick Sort variant)? Why isn't Heap Sort the king of all sorting algorithms?
   Answer: CPU Caching (Locality of Reference). Quick Sort compares adjacent elements in memory, which means the CPU Cache hits nearly 100% of the time. Heap Sort jumps wildly around the array. Comparing index `i` with `2*i+1` means jumping across massive gaps in memory. This causes catastrophic CPU Cache Misses. In the real world, Heap Sort is often 2x to 3x slower than Quick Sort.

2. What is Introsort (Introspective Sort)?
   Answer: It is a hybrid sorting algorithm used in C++. It starts by running Quick Sort (for the raw speed and cache performance). But it tracks the recursion depth. If the recursion goes too deep (indicating the malicious $O(N^2)$ worst-case has been triggered), it instantly aborts Quick Sort and switches to Heap Sort, guaranteeing it finishes in $O(N \\log N)$ time!

3. Is Heap Sort stable?
   Answer: NO. The very first step of building the Max Heap violently throws elements up and down the tree structure across large gaps in the array. This completely destroys the relative order of duplicate elements.
"""

if __name__ == "__main__":
    demonstrate_heap_sort()
    print("\n[SUCCESS] Laboratory: Heap Sort Completed.")
