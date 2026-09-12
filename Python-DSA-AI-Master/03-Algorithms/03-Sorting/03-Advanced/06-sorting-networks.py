"""
Sorting Networks (Bitonic Sort)

Learning Objectives:
1. Understand the concept of Sorting Networks and how they differ from comparison sorts.
2. Learn about Data-independent sorting algorithms.
3. Understand Bitonic Sort as a prime example of a sorting network.
4. Implement Bitonic Sort in Python and analyze its parallelization potential.

Concept Explanation:
A sorting network is an abstract mathematical model of a sorting algorithm, consisting of 
"wires" and "comparator modules". Their sequence of comparisons is not data-dependent. 
No matter what the input data is, the same pairs of elements are compared in the same order.
This makes them highly suitable for hardware implementation and parallel execution (e.g., on GPUs).

Bitonic Sort is one of the most famous sorting networks. It works by building "bitonic sequences"
(a sequence that monotonically increases then decreases, or vice-versa) and then recursively
merging them into a fully sorted sequence.
Note: Standard Bitonic Sort works only for arrays where the size is a power of 2 (N = 2^k).

Performance Analysis:
- Time Complexity: O(log^2 N) parallel steps, O(N log^2 N) overall comparisons.
- Space Complexity: O(log^2 N) recursion stack, or O(1) iterative hardware.
- Stability: Varies by implementation, but typically stable if comparators preserve order.

Edge Cases Handled:
- Small arrays.
- Works best when length is a power of 2; we handle it gracefully by padding or restricting.
"""

import math
from typing import List, TypeVar, Protocol, Any

class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...

T = TypeVar('T', bound=Comparable)

def comp_and_swap(arr: List[T], i: int, j: int, direction: int) -> None:
    """
    Compares and swaps elements based on the desired sort direction.
    direction = 1 for ASCENDING, 0 for DESCENDING.
    """
    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr: List[T], low: int, cnt: int, direction: int) -> None:
    """
    Recursively sorts a bitonic sequence in ascending (1) or descending (0) order.
    """
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, direction)
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

def bitonic_sort_util(arr: List[T], low: int, cnt: int, direction: int) -> None:
    """
    First produces a bitonic sequence by recursively sorting its two halves
    in opposite sorting orders, and then calls bitonic_merge to make them in same order.
    """
    if cnt > 1:
        k = cnt // 2
        # Sort first half in ASCENDING order (1)
        bitonic_sort_util(arr, low, k, 1)
        # Sort second half in DESCENDING order (0)
        bitonic_sort_util(arr, low + k, k, 0)
        # Merge whole sequence in desired direction
        bitonic_merge(arr, low, cnt, direction)

def is_power_of_two(n: int) -> bool:
    return (n != 0) and (n & (n - 1) == 0)

def bitonic_sort(arr: List[T]) -> None:
    """
    Main function to sort an array using Bitonic Sort.
    Note: Length of the array must be a power of 2 for this basic implementation.
    """
    if not arr or len(arr) <= 1:
        return
    
    n = len(arr)
    if not is_power_of_two(n):
        raise ValueError(f"Bitonic Sort requires array size to be a power of 2, got {n}")

    # 1 for ASCENDING
    bitonic_sort_util(arr, 0, n, 1)

# ==============================================================================
# Interview Challenge
# ==============================================================================
# Problem: You are designing a sorting algorithm for a GPU where thousands of 
# threads can execute instructions simultaneously, but conditional branching 
# (if-else) causes significant performance penalties. Which algorithm do you choose?
# Solution: A Sorting Network, like Bitonic Sort. Since the sequence of comparisons 
# is fixed and data-independent, it completely avoids conditional branching in the 
# control flow. Thousands of comparators can run in parallel, exploiting the GPU's 
# architecture efficiently.

# ==============================================================================
# Tests
# ==============================================================================
def run_tests() -> None:
    # We only test with sizes that are powers of 2.
    test_cases = [
        ([], []),
        ([1], [1]),
        ([3, 1, 4, 2], [1, 2, 3, 4]),
        ([9, 8, 7, 6, 5, 4, 3, 2], [2, 3, 4, 5, 6, 7, 8, 9]),
        ([1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]),
        ([5, -1, 0, -5, 10, 2, 8, 9], [-5, -1, 0, 2, 5, 8, 9, 10]),
        ([10]*16, [10]*16),
    ]
    
    for i, (input_arr, expected) in enumerate(test_cases):
        arr_copy = input_arr[:]
        bitonic_sort(arr_copy)
        assert arr_copy == expected, f"Test {i+1} failed: {arr_copy} != {expected}"
        print(f"Test {i+1} passed!")

    # Test error handling for non-power of 2
    try:
        bitonic_sort([1, 2, 3])
        assert False, "Should have raised ValueError for length 3"
    except ValueError:
        print("Error handling for non-power of 2 passed!")

if __name__ == "__main__":
    print("Running Sorting Network (Bitonic Sort) Tests...")
    run_tests()
    print("All tests passed successfully.")
