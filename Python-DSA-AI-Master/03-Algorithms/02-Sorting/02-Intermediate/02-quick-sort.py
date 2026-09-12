"""
## A. Concept Name
Quick Sort

## B. One-Sentence Definition
Quick Sort is a highly efficient, divide-and-conquer sorting algorithm that selects a 'pivot' element and partitions the other elements into two sub-arrays according to whether they are less than or greater than the pivot.

## C. Why Does This Exist?
It provides a very fast average-case sorting mechanism that is often faster in practice than other O(N log N) algorithms like Merge Sort, particularly for in-place sorting implementations.

## D. Intuition
Pick an element. Put everything smaller to its left, everything larger to its right. Now do the same for the left side and the right side recursively.

## E. Real-Life Analogy
Imagine organizing a stack of test papers. You pick a middle score (the pivot). All papers with lower scores go in a pile to the left, and all higher scores go to the right. You then repeat this process for the left and right piles.

## F. Mental Model
Divide and conquer: partitioning around a pivot creates smaller sub-problems. The base case is an array of length 0 or 1, which is inherently sorted.

## G. Visual Explanation
Array: [3, 6, 8, 10, 1, 2, 1]
Pivot: 10 (or middle which is 10)
Let's trace with middle element 10:
left = [3, 6, 8, 1, 2, 1], middle = [10], right = []
Then recursively sort left...

## H. Formal Explanation
Quick sort uses a divide-and-conquer approach. It picks an element as a pivot and partitions the given array around the picked pivot. The sub-arrays are then recursively sorted. 

## I. Mathematical Foundation
The recurrence relation for the average case is T(N) = 2T(N/2) + O(N), resolving to O(N log N) by the Master Theorem. The worst-case is T(N) = T(N-1) + O(N), resolving to O(N^2).

## J. From-Scratch Implementation
See `quick_sort` below. (The provided implementation is out-of-place for readability).

## K. Library / Production Implementation
Many programming languages use variations of Quick Sort (like Introsort, which combines Quick Sort and Heap Sort) for their standard sorting libraries.

## L. Trace (walk through example)
arr = [3, 6, 8, 10, 1, 2, 1]
pivot = 10 (index 3)
left = [3, 6, 8, 1, 2, 1], middle = [10], right = []
recurse left:
pivot = 1 (index 3 of left)
left = [], middle = [1, 1], right = [3, 6, 8, 2]
...and so on until merged.

## M. Complexity
- Time Complexity: O(N log N) average, O(N^2) worst case.
- Space Complexity: O(log N) average for the recursion stack (O(N) in worst case), though the provided out-of-place version uses O(N) extra space.

## N. Common Mistakes
Choosing a bad pivot (like always the first element on an already sorted array) leading to O(N^2) performance. Forgetting the base case in recursion.

## O. Common Confusions
Confusing Quick Sort with Merge Sort. Quick Sort does the heavy lifting during partitioning (before recursive calls), while Merge Sort does it during merging (after recursive calls).

## P. When To Use
When you need a fast, general-purpose sorting algorithm. In-place Quick Sort is very memory efficient.

## Q. When NOT To Use
When stable sorting is required (standard Quick Sort is not stable), or when worst-case O(N^2) time complexity is unacceptable (e.g., in critical real-time systems without pivot randomization).

## R. Trade-offs
Fast average time vs. worst-case O(N^2) time. In-place implementations use little memory but aren't stable, while out-of-place implementations (like the one below) are readable but use O(N) extra memory.

## S. Debugging
Print the array at each recursive step along with the chosen pivot and the resulting left and right partitions to visualize the divide-and-conquer tree.

## T. Memory Hook
"Quickly pivot and partition!"

## U. Active Recall
1. What is the average time complexity of Quick Sort?
2. How does the choice of pivot affect performance?

## V. Practice
Modify the provided `quick_sort` to be an in-place algorithm that doesn't create new lists for `left`, `middle`, and `right`.

## W. Interview Question
How can you optimize Quick Sort to guarantee O(N log N) worst-case performance? (Hint: Introsort, or using Median of Medians).

## X. Project Connection
In our AI Master project, Quick Sort is utilized in the data ingestion module to rapidly sort incoming streaming data based on timestamp or priority before feeding it into the model for inference. Useful for sorting confidence scores or feature values during data preprocessing in machine learning pipelines.
"""

def quick_sort(arr):
    """
    Sorts an array using the Quick Sort algorithm.
    
    Args:
        arr (list): A list of comparable elements.
        
    Returns:
        list: A new sorted list.
    """
    if len(arr) <= 1:
        return arr
        
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    sample_data = [3, 6, 8, 10, 1, 2, 1]
    print("Original array:", sample_data)
    sorted_data = quick_sort(sample_data)
    print("Sorted array:  ", sorted_data)
