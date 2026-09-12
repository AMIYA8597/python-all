"""
## A. Concept Name
Merge Sort

## B. Real-World Analogy
Imagine you have a large stack of unsorted papers. You divide the stack in half, and hand each half to two assistants. They keep dividing their stacks until everyone has just one paper. Then, they start combining their papers, comparing them and keeping them sorted, until the entire stack is merged back together in sorted order.

## C. AI Connection
Merge sort's divide-and-conquer approach is conceptually similar to how distributed AI training splits data batches across multiple GPUs, processes them independently, and then merges the gradients or results. 

## D. Visual Tracing
[8, 3, 5, 4, 7, 6, 1, 2] -> Divide
[8, 3, 5, 4] and [7, 6, 1, 2] -> Divide further
...
Merge sorted parts:
[3, 4, 5, 8] and [1, 2, 6, 7] -> [1, 2, 3, 4, 5, 6, 7, 8]

## E. Core Logic
1. Divide: If the array has more than one element, split it into two halves.
2. Conquer: Recursively sort both halves.
3. Combine: Merge the two sorted halves into a single sorted array.

## F. Big O Complexity
- Time Complexity: O(n log n) in all cases (Best, Average, Worst).
- Space Complexity: O(n) because of the temporary arrays used for merging.

## G. Step-by-Step Implementation
Divide the array, recursively sort the parts, and merge them using two pointers.

## H. Edge Cases
Handles empty arrays and single-element arrays naturally.

## I. Common Pitfalls
Forgetting to copy the remaining elements after the main while loop finishes.

## J. Optimization Techniques
For small sub-arrays (e.g., length < 15), switch to Insertion Sort for better practical performance.

## K. Testing Strategies
Test with reversed arrays, already sorted arrays, arrays with duplicate elements, and empty arrays.

## L. Historical Context
Invented by John von Neumann in 1945 as a foundational divide-and-conquer sorting algorithm.

## M. Space-Time Tradeoffs
Uses extra O(n) space to achieve guaranteed O(n log n) time complexity, unlike Quicksort which is in-place but has a worst-case O(n^2) time.

## N. Real-World Applications
Used in external sorting where data doesn't fit in memory (e.g., sorting large files).

## O. Comparison with Other Algorithms
More predictable than Quicksort, but uses more memory. Better than Bubble or Insertion sort for large datasets.

## P. Interactive Exercise
Trace the algorithm on paper with the array [4, 2, 7, 1, 3] to see exactly when merging happens.

## Q. Review Questions
1. Why does Merge Sort require O(n) auxiliary space?
2. Is Merge Sort stable? Why?

## R. Glossary of Terms
- Divide and Conquer: Breaking down a problem into smaller, similar subproblems.
- Stable Sort: Retains the relative order of equal elements.

## S. References & Further Reading
Introduction to Algorithms (CLRS) - Chapter on Divide-and-Conquer.

## T. Self-Evaluation
Can you write the merge step from memory without looking at the code?

## U. Code Variations
Bottom-up (iterative) Merge Sort avoids recursion overhead.

## V. Debugging Tips
Use print statements inside the merge step to watch the temporary array get populated.

## W. Expert Advice
In Python, the built-in `list.sort()` (Timsort) is a hybrid of Merge Sort and Insertion Sort.

## X. Project Connection
In AI applications, sorting huge datasets is a common preprocessing step. Merge sort is highly parallelizable and stable, making it ideal for distributed computing environments where large datasets need to be ordered before feeding into machine learning pipelines.
"""

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

if __name__ == "__main__":
    sample_array = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {sample_array}")
    sorted_array = merge_sort(sample_array.copy())
    print(f"Sorted array: {sorted_array}")
