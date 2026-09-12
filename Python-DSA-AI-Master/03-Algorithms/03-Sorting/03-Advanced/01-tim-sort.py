"""
## A. Concept Name
Tim Sort

## B. One-Sentence Definition
Tim Sort is a hybrid, stable sorting algorithm derived from merge sort and insertion sort, designed to perform well on many kinds of real-world data.

## C. Learning Objectives
1. Understand the hybrid nature of Tim Sort (Merge Sort + Insertion Sort).
2. Learn how runs are identified and merged.
3. Analyze the time and space complexity of Tim Sort.
4. Implement a simplified version of Tim Sort.

## D. Intuition
Imagine you have a deck of cards that is already partially sorted in small chunks. Instead of shuffling them all and sorting from scratch, you first sort the small unsorted chunks (using a fast method for small sets, like Insertion Sort), and then you carefully merge these sorted chunks together (using Merge Sort).

## E. Problem Statement
Given an array of integers, sort the array in ascending order efficiently, taking advantage of any pre-existing order (natural runs) in the data.

## F. Algorithm Steps
1. Divide the array into small blocks known as 'runs' (usually of size 32-64).
2. Sort these small runs using Insertion Sort.
3. Merge the sorted runs together using the Merge function from Merge Sort until the entire array is sorted.

## G. Complexity
- Best Case Time: O(n) - when the array is already sorted.
- Average Case Time: O(n log n)
- Worst Case Time: O(n log n)
- Space Complexity: O(n) auxiliary space for the merging process.

## H. Space Complexity Analysis
Tim Sort requires O(n) space in the worst case to merge the runs, although optimizations can reduce this overhead in practice.

## I. Edge Cases
- Empty array.
- Array with one element.
- Array with all identical elements.
- Array already sorted or reverse sorted.

## J. Common Pitfalls
- Using an incorrect run size can degrade performance.
- Failing to handle the remainder of the array when dividing into runs.

## K. Debugging
- Check if `calc_min_run` returns a value between 32 and 64 (inclusive).
- Ensure that the merge function properly handles leftover elements in both left and right subarrays.

## L. Optimization Techniques
- Python's actual Tim Sort implements "Galloping" mode to speed up the merge process when one array has many elements that are smaller/larger than the other.

## M. Prerequisites
- Merge Sort
- Insertion Sort
- Bitwise operations (for calculating min run)

## N. Real-World Applications
- Python's built-in `sorted()` and `list.sort()`.
- Java's `Arrays.sort()` for objects.
- V8 engine's `Array.prototype.sort()` for JavaScript.

## O. Diagram / Visual Representation
Array: [5, 21, 7, 23, 190] -> (divided into runs) -> [5, 21] and [7, 23, 190]
Sort runs (Insertion Sort): [5, 21] and [7, 23, 190]
Merge runs: [5, 7, 21, 23, 190]

## P. Comparison with Alternatives
- Faster than pure Merge Sort and Quick Sort on real-world data with existing order.
- Stable, unlike Quick Sort.
- Requires O(n) space, whereas Quick Sort is O(log n) space.

## Q. Testing / TDD
- Test with random arrays.
- Test with already sorted arrays.
- Test with reverse sorted arrays.
- Test with large arrays to see the benefit of runs.

## R. Language-Specific Features
- Python's dynamic typing allows Tim Sort to be generic (using `Protocol` and `TypeVar` for typing).

## S. Variations / Extensions
- Can be customized with different `MIN_MERGE` values based on architecture cache sizes.

## T. Interview Questions
Why does Tim Sort use Insertion Sort for small runs instead of just continuing to use Merge Sort?
Answer: Insertion Sort is very fast for small arrays (typically < 64 elements) due to low overhead and cache locality.

## U. Exercises / Practice
- Implement Galloping mode in the merge step.
- Modify the algorithm to sort in descending order.

## V. Summary / Key Takeaways
- Tim Sort combines the best of Insertion Sort (speed on small arrays) and Merge Sort (efficiency on large arrays).
- Identifying natural runs is key to its O(n) best-case performance.

## W. Further Reading
- Python's original `listobject.c` source code by Tim Peters.

## X. Project Connection
Integrate Tim Sort into a data processing pipeline where data arrives partially sorted (e.g., log files by timestamp) to achieve near O(n) sorting times.
"""

from typing import List, TypeVar, Protocol

T = TypeVar('T', bound=Protocol['__lt__'])

MIN_MERGE = 32

def calc_min_run(n: int) -> int:
    """Returns the minimum length of a run from 23 - 64 so that
    the len(array)/minrun is less than or equal to a power of 2.
    """
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(arr: List[int], left: int, right: int) -> None:
    """Sorts a portion of the array using insertion sort."""
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def merge(arr: List[int], l: int, m: int, r: int) -> None:
    """Merges two sorted runs."""
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])

    i, j, k = 0, 0, l
    while i < len1 and j < len2:
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1

    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1

def tim_sort(arr: List[int]) -> None:
    """Main Tim Sort function."""
    n = len(arr)
    min_run = calc_min_run(n)

    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size

def test_tim_sort() -> None:
    """Tests for Tim Sort."""
    arr = [5, 21, 7, 23, 190]
    tim_sort(arr)
    assert arr == [5, 7, 21, 23, 190], "Basic test failed"

    # Edge cases
    empty: List[int] = []
    tim_sort(empty)
    assert empty == [], "Empty test failed"

    single = [1]
    tim_sort(single)
    assert single == [1], "Single element test failed"

    print("All Tim Sort tests passed!")

if __name__ == "__main__":
    test_tim_sort()
