"""
## A. Concept Name
Radix Sort

## B. One-Sentence Definition
Radix Sort is a non-comparative integer sorting algorithm that sorts data with integer keys by grouping keys by the individual digits which share the same significant position and value.

## C. Why Does This Exist?
It exists to overcome the O(N log N) lower bound of comparison-based sorting algorithms, offering an O(N) linear time complexity for specific data types like integers or strings of a fixed size.

## D. Intuition
Instead of comparing whole numbers directly, sort them digit by digit, from the least significant digit (LSD) to the most significant digit (MSD). Because each digit sort is stable, by the time you sort the MSD, the whole array is ordered.

## E. Real-Life Analogy
Imagine sorting a deck of cards with 3-digit numbers. First, sort all cards into 10 piles based on the last digit. Then collect them (preserving order) and re-sort into 10 piles based on the middle digit. Finally, collect them and sort by the first digit. The cards are now fully sorted.

## F. Mental Model
Think of Radix Sort as running a stable bucket sort multiple times. For a d-digit number, you will run the bucket sort (typically Counting Sort) d times. The stability of the underlying sort ensures that numbers with the same current digit retain their relative order from the previous digit's sort.

## G. Visual Explanation
Array: [170, 45, 75, 90, 802, 24, 2, 66]
Sort by 1s digit:
[170, 90] (0), [802, 2] (2), [24] (4), [45, 75] (5), [66] (6)
Array becomes: [170, 90, 802, 2, 24, 45, 75, 66]

Sort by 10s digit:
[802, 2] (0), [24] (2), [45] (4), [66] (6), [170, 75] (7), [90] (9)
Array becomes: [802, 2, 24, 45, 66, 170, 75, 90]

Sort by 100s digit:
[2, 24, 45, 66, 75, 90] (0), [170] (1), [802] (8)
Array becomes: [2, 24, 45, 66, 75, 90, 170, 802]

## H. Formal Explanation
Radix Sort distributes elements into buckets based on their radix (base). For decimal numbers, the radix is 10. It uses Counting Sort as a stable subroutine. By repeatedly sorting the array starting from the lowest place value to the highest place value, the final array is strictly sorted.

## I. Mathematical Foundation
If the array has N elements and the maximum number has d digits in base b, the subroutine Counting Sort takes O(N + b) time. Since this is done d times, the total time complexity is O(d * (N + b)).

## J. From-Scratch Implementation
See `radix_sort` and `counting_sort_for_radix` below.

## K. Library / Production Implementation
Most general-purpose standard libraries (like Python's `list.sort()`) use Timsort (O(N log N)). Radix sort is typically implemented custom for specific high-performance computing contexts (e.g., GPU sorting algorithms or specialized database indexing) where sorting massive integer arrays is a bottleneck.

## L. Trace (walk through example)
arr = [170, 45, 75, 90, 802, 24, 2, 66]
max1 = 802 (3 digits). We will sort 3 times (exp = 1, 10, 100).
exp = 1: Sort by LSD. Result: [170, 90, 802, 2, 24, 45, 75, 66]
exp = 10: Sort by middle digit. Result: [802, 2, 24, 45, 66, 170, 75, 90]
exp = 100: Sort by MSD. Result: [2, 24, 45, 66, 75, 90, 170, 802]

## M. Complexity
- Time Complexity: O(d * (N + b)) where d is the max digits, b is base (10).
- Space Complexity: O(N + b) for the Counting Sort subroutine output and count arrays.
- Stability: Stable.
- In-place: Not in-place.

## N. Common Mistakes
Implementing the subroutine without stability. If the Counting Sort isn't stable, the previous digit sorts are ruined. Also, forgetting to handle negative numbers (classic Radix sort assumes non-negative).

## O. Common Confusions
Confusing Radix Sort with Bucket Sort or Counting Sort. Radix Sort uses Counting Sort internally for each digit phase. Bucket Sort divides elements into ranges.

## P. When To Use
When you need to sort a large number of integers, strings, or fixed-length keys, and you know the maximum length (d) is relatively small. Highly effective when N is huge and d is small.

## Q. When NOT To Use
When sorting floating-point numbers or objects lacking a natural integer/string representation. Also, if d is very large (e.g., arbitrary precision integers), O(d * N) can become slower than O(N log N). Not ideal if memory is strictly constrained.

## R. Trade-offs
Fast linear-like time complexity, but requires extra space O(N + b) and works best only for specific data types. Not cache-friendly due to scattered bucket accesses.

## S. Debugging
Print the array state at the end of each `while max1 / exp >= 1` loop iteration. Verify that the numbers are sorted based strictly on the current and previous digit positions.

## T. Memory Hook
"Radix means Root/Base. Sort digit by digit, from tail to head, keeping it stable."

## U. Active Recall
1. Why does Radix Sort require a stable subroutine?
2. What is the time complexity if all numbers have exactly 5 digits in base 10?

## V. Practice
Modify `radix_sort` to handle arrays containing negative integers. (Hint: Split into positive and negative arrays, sort separately, reverse the negative array, and concatenate).

## W. Interview Question
Can you use Radix Sort to sort an array of English words? If so, how would you align them? (Hint: Pad shorter words and sort from the rightmost character).

## X. Project Connection
In the AI Master project, Radix Sort can be used to perform lightning-fast lexicographical sorts on millions of tokenized integer sequences in NLP tasks, or for Z-order curve indexing in spatial data structures for computer vision.
"""

from typing import List

def counting_sort_for_radix(arr: List[int], exp1: int) -> None:
    """
    A function to do counting sort of arr[] according to
    the digit represented by exp.
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Store count of occurrences in count[]
    for i in range(n):
        index = arr[i] // exp1
        count[index % 10] += 1
        
    # Change count[i] so that count[i] now contains actual
    # position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    # Build the output array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        
    # Copying the output array to arr[],
    # so that arr now contains sorted numbers according to current digit
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr: List[int]) -> List[int]:
    """
    Implementation of Radix Sort.
    """
    if not arr:
        return arr
        
    # Find the maximum number to know number of digits
    max1 = max(arr)
    
    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
    exp = 1
    while max1 / exp >= 1:
        counting_sort_for_radix(arr, exp)
        exp *= 10
        
    return arr

def complexity_analysis():
    """
    Time Complexity: O(d * (n + b))
    - d is the number of digits
    - b is the base (10 for decimal numbers)
    
    Space Complexity: O(n + b)
    Stability: Stable (because Counting Sort is stable).
    """
    pass

def run_tests():
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    expected = [2, 24, 45, 66, 75, 90, 170, 802]
    
    radix_sort(arr)
    assert arr == expected
    
    print("[+] Radix Sort tests passed!")

if __name__ == "__main__":
    run_tests()
