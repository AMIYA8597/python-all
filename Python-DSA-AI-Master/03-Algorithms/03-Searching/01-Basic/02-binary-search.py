"""
## A. Concept Name
Binary Search

## B. Core Idea / Intuition
Search a sorted array by repeatedly dividing the search interval in half.

## C. Real-World Analogy
Think of searching for a word in a dictionary: you open the book in the middle, and if the word is earlier, you search the left half; if later, the right half.

## D. Time Complexity
- Best Case: O(1)
- Average Case: O(log n)
- Worst Case: O(log n)

## E. Space Complexity
O(1) auxiliary space for iterative, O(log n) for recursive.

## F. In-Place
Yes.

## G. Stable
Not applicable (typically search algorithms just find one matching element).

## H. Recursive or Iterative
Can be both; iterative is preferred in Python to avoid stack overflow.

## I. Data Structure Used
Array / List (must be sorted).

## J. Algorithmic Paradigm
Divide and Conquer.

## K. Pre-requisites
Loops/Recursion, Arrays, Array must be sorted.

## L. Applications
Finding elements in sorted arrays, dictionary lookups, debugging (git bisect).

## M. Trade-offs
Fast for searching, but requires the array to be sorted first which takes O(n log n) time. Not suitable for unsorted or frequently changing data.

## N. Common Mistakes
Off-by-one errors with `left` and `right` updates (e.g., `left = mid` instead of `left = mid + 1`). Calculating `mid` with `(left + right) // 2` can cause overflow in other languages.

## O. Optimization
Using `left + (right - left) // 2` prevents integer overflow in fixed-width integers.

## P. Testing Edge Cases
Target not in list, target is first element, target is last element, empty list, single element.

## Q. Visual Trace
Searching for 7 in [1, 3, 5, 7, 9, 11]: 
Mid is 5 (index 2). 7 > 5, so search right half [7, 9, 11]. 
Mid is 9 (index 4). 7 < 9, so search left half [7]. 
Mid is 7 (index 3). Found!

## R. Interview Tips
Be flawless. Know when to use `left <= right` versus `left < right` for exact match vs insertion point.

## S. Code Variants
Finding first/last occurrence, search in rotated sorted array, binary search on answer.

## T. Related Concepts
Ternary Search, Interpolation Search, Jump Search.

## U. Further Reading
Introduction to Algorithms (CLRS) - Binary Search chapter.

## V. FAQ
Q: Can binary search be applied to linked lists? A: No, because it requires O(1) random access.

## W. Practice Problems
Find First and Last Position of Element in Sorted Array, Search in Rotated Sorted Array.

## X. Project Connection
Used internally in databases for querying indexed columns. Helpful for fast lookups over a static, pre-sorted dataset.
"""

def binary_search(arr, target):
    """
    Perform a binary search for the target in a sorted list.
    
    :param arr: A sorted list of elements
    :param target: The element to search for
    :return: The index of the target if found, otherwise -1
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

if __name__ == "__main__":
    # Example usage
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    search_target = 7
    result = binary_search(sorted_array, search_target)
    
    if result != -1:
        print(f"Element {search_target} found at index {result}.")
    else:
        print(f"Element {search_target} not found in the array.")
