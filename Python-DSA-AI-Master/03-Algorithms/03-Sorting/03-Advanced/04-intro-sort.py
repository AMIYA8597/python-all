"""
Intro Sort (Introspective Sort)

Learning Objectives:
1. Understand the concept of hybrid sorting algorithms.
2. Learn how Intro Sort combines Quick Sort, Heap Sort, and Insertion Sort.
3. Analyze the time and space complexity of Intro Sort.
4. Implement a robust Intro Sort algorithm in Python.

Concept Explanation:
Intro Sort is a hybrid sorting algorithm that provides both fast average performance and
(asymptotically) optimal worst-case performance. It begins with Quick Sort and switches
to Heap Sort when the recursion depth exceeds a level based on the logarithm of the number
of elements being sorted (usually 2 * log2(N)). For very small sub-arrays, it can switch
to Insertion Sort. This guarantees O(N log N) worst-case time complexity while maintaining
the speed of Quick Sort in most practical scenarios. C++'s std::sort uses Introsort.

Performance Analysis:
- Time Complexity: O(N log N) worst, average, and best case.
- Space Complexity: O(log N) due to recursion stack of Quick Sort.
- Stability: Not stable (due to Quick Sort and Heap Sort).

Edge Cases Handled:
- Empty lists and single-element lists.
- Already sorted or reverse-sorted lists.
- Lists with many duplicate elements.
"""

import math
from typing import List, TypeVar, Protocol, Any

class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...

T = TypeVar('T', bound=Comparable)

def insertion_sort(arr: List[T], start: int, end: int) -> None:
    """Sorts a portion of the array using Insertion Sort."""
    for i in range(start + 1, end + 1):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def heapify(arr: List[T], n: int, i: int, start: int) -> None:
    """Heapify a subtree rooted at index i in a portion of the array."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[start + left] > arr[start + largest]:
        largest = left
    if right < n and arr[start + right] > arr[start + largest]:
        largest = right

    if largest != i:
        arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
        heapify(arr, n, largest, start)

def heap_sort(arr: List[T], start: int, end: int) -> None:
    """Sorts a portion of the array using Heap Sort."""
    n = end - start + 1
    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, start)
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[start + i], arr[start] = arr[start], arr[start + i]
        heapify(arr, i, 0, start)

def median_of_three(arr: List[T], a: int, b: int, c: int) -> int:
    """Returns the index of the median of three elements."""
    if arr[a] < arr[b]:
        if arr[b] < arr[c]:
            return b
        elif arr[a] < arr[c]:
            return c
        else:
            return a
    else:
        if arr[a] < arr[c]:
            return a
        elif arr[b] < arr[c]:
            return c
        else:
            return b

def partition(arr: List[T], low: int, high: int) -> int:
    """Partitions the array for Quick Sort."""
    mid = low + (high - low) // 2
    pivot_idx = median_of_three(arr, low, mid, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
    
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def introsort_util(arr: List[T], start: int, end: int, depth_limit: int) -> None:
    """Recursive utility function for Intro Sort."""
    size = end - start + 1
    if size <= 16:
        # Small subarrays are sorted using Insertion Sort
        insertion_sort(arr, start, end)
        return
    
    if depth_limit == 0:
        # If recursion depth limit is reached, fallback to Heap Sort
        heap_sort(arr, start, end)
        return
    
    # Otherwise, use Quick Sort
    pivot = partition(arr, start, end)
    introsort_util(arr, start, pivot - 1, depth_limit - 1)
    introsort_util(arr, pivot + 1, end, depth_limit - 1)

def intro_sort(arr: List[T]) -> None:
    """
    Main function to perform Intro Sort on the given array.
    Mutates the array in-place.
    """
    if not arr or len(arr) <= 1:
        return
    
    max_depth = 2 * math.floor(math.log2(len(arr)))
    introsort_util(arr, 0, len(arr) - 1, max_depth)


# ==============================================================================
# Interview Challenge
# ==============================================================================
# Problem: Given a stream of data where elements can be arbitrarily large, but
# you only have a limited amount of memory, design a sorting strategy.
# Solution: Intro Sort is an in-memory algorithm. For this challenge, you would
# likely need an External Sort. However, if the data fits in memory but you are
# worried about worst-case time complexity of Quick Sort (e.g. adversarial inputs),
# Intro Sort is the perfect countermeasure because it guarantees O(N log N).

# ==============================================================================
# Tests
# ==============================================================================
def run_tests() -> None:
    test_cases = [
        ([], []),
        ([1], [1]),
        ([3, 1, 2], [1, 2, 3]),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([3, 3, 3, 1, 2, 3], [1, 2, 3, 3, 3, 3]),
        ([5, -1, 0, -5, 10, 2], [-5, -1, 0, 2, 5, 10]),
        ([10]*100, [10]*100), # Large duplicate array
    ]
    
    for i, (input_arr, expected) in enumerate(test_cases):
        arr_copy = input_arr[:]
        intro_sort(arr_copy)
        assert arr_copy == expected, f"Test {i+1} failed: {arr_copy} != {expected}"
        print(f"Test {i+1} passed!")

if __name__ == "__main__":
    print("Running Intro Sort Tests...")
    run_tests()
    print("All tests passed successfully.")
