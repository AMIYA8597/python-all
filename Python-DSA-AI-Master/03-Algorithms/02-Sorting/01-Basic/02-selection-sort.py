"""
## A. Concept Name
Selection Sort

## B. Problem Statement
Sort an array of elements in a specific order (ascending or descending) using in-place comparisons.

## C. Core Idea
Divide the input list into two parts: a sorted sublist of items which is built up from left to right at the front (left) of the list and a sublist of the remaining unsorted items that occupy the rest of the list.

## D. How it Works (Algorithm Steps)
1. Set the first unsorted element as the minimum.
2. Iterate through the rest of the array to find the true minimum element.
3. Swap the found minimum element with the first unsorted element.
4. Move the boundary of the sorted and unsorted subarrays one element to the right.
5. Repeat steps 1-4 until the array is sorted.

## E. Time Complexity (Big O)
- Best Case: O(N^2)
- Average Case: O(N^2)
- Worst Case: O(N^2)

## F. Space Complexity
O(1) auxiliary space, as it sorts in-place.

## G. Real-World Analogy
Sorting a hand of cards by looking for the smallest card in your hand, moving it to the leftmost position, then finding the next smallest card and placing it next to the first one, and so on.

## H. Iterative Implementation
Provided in the functions below.

## I. Recursive Implementation
Can be implemented recursively, though iterative is standard.

## J. Optimizations
Selection sort is generally inefficient on large lists, and has no common optimizations that improve its O(N^2) time complexity.

## K. Standard Library Equivalents
Python's built-in `sort()` and `sorted()` functions use Timsort, which is highly optimized.

## L. Typical Use Cases
- When memory space is extremely limited (O(1) auxiliary space).
- When writing to memory is significantly more expensive than reading (Selection sort does at most O(N) swaps).

## M. Edge Cases
- Empty array
- Array with one element
- Array that is already sorted
- Array with duplicate elements

## N. Constraints & Assumptions
Elements must be comparable.

## O. Error Handling
Type checking could be added for non-comparable elements.

## P. Testing Strategy
Test with empty lists, single elements, reversed lists, and lists with duplicates.

## Q. Related Data Structures
Arrays, Lists.

## R. Related Algorithms
Bubble Sort, Insertion Sort (other simple O(N^2) algorithms).

## S. Interview Potential
Low for direct implementation, but good for understanding fundamental algorithm concepts and explaining swap bounds.

## T. Typical Pitfalls
Using it on large datasets where O(N log N) algorithms (Merge Sort, Quick Sort) are needed.

## U. Best Practices
Avoid using Selection Sort in production; use standard library sorts.

## V. Memory Management
Very memory efficient due to in-place swapping.

## W. Debugging Tips
Print the array at each outer loop iteration to see the sorted subarray grow.

## X. Project Connection
Can be used as a simple fallback sorting algorithm in embedded systems projects or as an educational baseline for comparing algorithm efficiencies in an AI sorting visualization tool.
"""

def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.
    
    Args:
        arr (list): A list of comparable elements.
        
    Returns:
        list: The sorted list (sorted in-place).
    """
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
    return arr

if __name__ == "__main__":
    sample_data = [64, 25, 12, 22, 11]
    print(f"Original array: {sample_data}")
    sorted_data = selection_sort(sample_data.copy())
    print(f"Sorted array:   {sorted_data}")
