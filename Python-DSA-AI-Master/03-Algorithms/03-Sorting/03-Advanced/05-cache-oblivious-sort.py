"""
Cache-Oblivious Sorting Algorithms

Learning Objectives:
1. Understand the concept of the cache-oblivious model.
2. Learn how algorithms can efficiently use CPU cache without knowing its size.
3. Implement a recursive Merge Sort and analyze its cache-oblivious properties.
4. Analyze the I/O complexity of cache-oblivious sorting.

Concept Explanation:
A cache-oblivious algorithm is designed to take advantage of a processor cache without
having the size of the cache (or the size of the cache lines) as an explicit parameter.
This is typically achieved through divide-and-conquer recursively. 
When the subproblem size becomes small enough to fit into the cache, it operates 
without further cache misses.

While Funnelsort is a strictly O(N/B * log_{M/B}(N/B)) optimal cache-oblivious sorting
algorithm, a standard recursive Merge Sort on arrays also exhibits cache-oblivious 
properties compared to iterative/bottom-up approaches or Tree-based sorts. The
recursive division naturally falls into cache blocks.

Performance Analysis:
- Time Complexity: O(N log N)
- Space Complexity: O(N) auxiliary space for merging.
- Cache/IO Complexity (Merge Sort): O( (N/B) * log_2(N/B) ) where B is block size.

Edge Cases Handled:
- Empty arrays.
- Small arrays.
- Pre-sorted arrays.
"""

from typing import List, TypeVar, Protocol, Any

class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...

T = TypeVar('T', bound=Comparable)

def cache_oblivious_merge(arr: List[T], temp: List[T], left: int, mid: int, right: int) -> None:
    """
    Merges two halves. For true cache-obliviousness, spatial locality is key.
    We read arrays linearly, which optimally uses cache lines.
    """
    i = left
    j = mid + 1
    k = left

    # Merging elements with spatial locality (sequential memory access)
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1

    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    # Copy back to original array
    for i in range(left, right + 1):
        arr[i] = temp[i]

def cache_oblivious_sort_util(arr: List[T], temp: List[T], left: int, right: int) -> None:
    """
    Recursive division ensures that eventually sub-arrays fit entirely into 
    L1/L2/L3 caches without knowing their sizes.
    """
    if left >= right:
        return

    mid = left + (right - left) // 2

    # Divide
    cache_oblivious_sort_util(arr, temp, left, mid)
    cache_oblivious_sort_util(arr, temp, mid + 1, right)

    # Conquer (Merge)
    cache_oblivious_merge(arr, temp, left, mid, right)

def cache_oblivious_sort(arr: List[T]) -> None:
    """
    Main function for cache-oblivious sort (implemented via Recursive Merge Sort).
    """
    if not arr or len(arr) <= 1:
        return
    
    # Allocate a single temporary array for merging to avoid 
    # memory fragmentation and improve locality.
    temp = [None] * len(arr)
    cache_oblivious_sort_util(arr, temp, 0, len(arr) - 1)

# ==============================================================================
# Interview Challenge
# ==============================================================================
# Problem: Why is standard Heapsort considered cache-unfriendly, and how does
# cache-oblivious sorting fix this?
# Solution: Heapsort accesses elements at indices `i`, `2i`, `2i+1`, which causes
# large jumps in memory. For a large array, these jumps cause frequent cache misses.
# Cache-oblivious sorting (like Funnelsort or Recursive Merge Sort) accesses memory 
# sequentially or operates on small contiguous sub-arrays that fit entirely in cache,
# minimizing cache misses without tuning for a specific hardware architecture.

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
        ([10]*100, [10]*100),
    ]
    
    for i, (input_arr, expected) in enumerate(test_cases):
        arr_copy = input_arr[:]
        cache_oblivious_sort(arr_copy)
        assert arr_copy == expected, f"Test {i+1} failed: {arr_copy} != {expected}"
        print(f"Test {i+1} passed!")

if __name__ == "__main__":
    print("Running Cache Oblivious Sort Tests...")
    run_tests()
    print("All tests passed successfully.")
