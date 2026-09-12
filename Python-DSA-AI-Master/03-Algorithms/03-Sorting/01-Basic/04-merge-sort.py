"""
## A. Concept Name
Merge Sort Algorithm

## B. Motivation / Problem Statement
Sorting a large dataset efficiently can be slow using simple algorithms like Bubble or Insertion Sort (which take O(N^2) time). We need a method that consistently performs well, sorting large arrays in a guaranteed O(N log N) time regardless of the initial order.

## C. Real-world Analogy
Imagine you have a large stack of papers to sort alphabetically. Doing it all at once is overwhelming. Instead, you split the stack in half, and give half to a friend. You both split your stacks again until everyone has single pieces of paper. A single paper is already sorted! Then, you pair up, merging your two sorted stacks by looking at the top of each, picking the smaller one, and building a new sorted stack. This merging continues until you have one giant sorted stack again.

## D. Definition & Intuition
Merge Sort is a quintessential Divide and Conquer algorithm. It divides the input array into two halves, calls itself for the two halves, and then merges the two sorted halves. The fundamental intuition is that merging two already sorted lists is much faster (linear time) than sorting a large unsorted list.

## E. Core Algorithm (Divide & Conquer)
1. **Divide**: If the array has more than one element, find the middle point to divide the array into two halves.
2. **Conquer**: Recursively call merge sort on the left half and the right half.
3. **Combine (Merge)**: Merge the two sorted halves back into a single sorted array.

## F. Step-by-step Walkthrough
For array [38, 27, 43, 3]:
1. Divide into [38, 27] and [43, 3].
2. Divide [38, 27] into [38] and [27]. Divide [43, 3] into [43] and [3].
3. Merge [38] and [27] -> [27, 38].
4. Merge [43] and [3] -> [3, 43].
5. Merge [27, 38] and [3, 43] -> [3, 27, 38, 43].

## G. Time Complexity Analysis
- **Best Case:** O(N log N)
- **Average Case:** O(N log N)
- **Worst Case:** O(N log N)
The tree always splits exactly in half (log N levels), and merging takes O(N) time at each level.

## H. Space Complexity Analysis
- **Auxiliary Space:** O(N)
Temporary arrays are created during the merge phase to hold elements before copying them back to the original array. This makes it non-in-place.

## I. Trade-offs (Pros & Cons)
- **Pros:** Guaranteed O(N log N) time complexity, stable sorting algorithm (preserves relative order of equal elements), works excellently for Linked Lists.
- **Cons:** Requires O(N) extra memory space, which makes it less suitable for systems with tight memory constraints compared to Quick Sort or Heap Sort.

## J. Code Implementation
See the `merge_sort` function below for a professional, generic, and type-hinted implementation in Python.

## K. Edge Cases & Constraints
- Empty arrays `[]`: Should be returned as-is (handled by `len(arr) > 1` check).
- Single-element arrays `[42]`: Already sorted, no action needed.
- Arrays with duplicate elements: Correctly handled and stability is preserved.
- Extremely large arrays: Standard recursive implementation might hit recursion depth limits; an iterative version can bypass this.

## L. Common Pitfalls
- Forgetting to copy the remaining elements of the left or right halves during the merge step.
- Off-by-one errors when calculating the middle index or slicing arrays.
- Mutating the array incorrectly during the merge step resulting in lost elements.

## M. Best Practices & Optimization
- Use Python's built-in `list.sort()` or `sorted()` (Timsort) for production code, as it's highly optimized in C.
- For a small number of elements, Insertion Sort is faster. A hybrid approach (like Timsort) switches to Insertion Sort for small sub-arrays.

## N. Variations (In-place, Bottom-up)
- **Iterative (Bottom-up) Merge Sort:** Avoids recursive stack overhead by merging sub-arrays of size 1, then size 2, then 4, etc.
- **In-place Merge Sort:** Possible but highly complex and often degrades time performance significantly.

## O. Technical Interview Questions
1. *Why is Merge Sort preferred for Linked Lists over Quick Sort?*
   (Linked lists lack O(1) random access; Merge Sort only needs sequential access and can run in O(1) extra space on linked lists).
2. *Is Merge Sort stable? Explain why.*
   (Yes. During the merge step, the element from the left half is picked first when two elements are equal).

## P. History & Origin
Merge sort was invented by John von Neumann in 1945. It is one of the oldest sorting algorithms and laid the foundation for modern external sorting techniques.

## Q. Industry Applications
- External Sorting: Sorting massive datasets that don't fit into RAM by reading/writing blocks to disk.
- E-commerce: Sorting product listings predictably.
- Built-in functions: Foundational to Timsort (Python, Java standard sorts).

## R. Comparison with Alternative Algorithms
- **vs Quick Sort:** Quick Sort is usually faster in practice and uses O(log N) space, but has an O(N^2) worst case and is not stable.
- **vs Heap Sort:** Heap Sort is O(N log N) and uses O(1) space, but is not stable and generally slower in practice due to poor cache locality.

## S. Prerequisites for Understanding
- Recursion and call stacks.
- Array indexing and slicing.
- Basic understanding of Big-O notation.

## T. Next Steps & Related Topics
- Implement the iterative (bottom-up) version of Merge Sort.
- Study Timsort to see how Merge Sort combines with Insertion Sort.
- Learn about External Sorting algorithms.

## U. Visual Representation (Mental Model)
          [38, 27, 43, 3]
         /               \
    [38, 27]           [43, 3]
    /      \           /      \
  [38]    [27]       [43]    [3]
    \      /           \      /
    [27, 38]           [3, 43]
         \               /
          [3, 27, 38, 43]

## V. Glossary of Terms
- **Divide and Conquer:** A paradigm of solving problems by breaking them into smaller, independent subproblems.
- **Stable Sort:** A sort that preserves the relative order of equal elements.
- **In-place:** Using minimal extra memory (usually O(1) or O(log N)).

## W. References & Further Reading
- Introduction to Algorithms (CLRS) - Chapter 2
- Donald Knuth's The Art of Computer Programming, Volume 3

## X. Project Connection
Understanding Merge Sort is crucial for tasks requiring stable sorting, processing massive datasets out-of-core, and building custom high-performance data processing pipelines in data science or backend engineering.
"""

from typing import TypeVar, List, Callable

T = TypeVar('T')

def merge_sort(
    arr: List[T],
    key: Callable[[T], any] = lambda x: x,
    reverse: bool = False
) -> None:
    """
    Sorts a list in-place using the recursive Merge Sort algorithm.
    
    Note: While the list is modified in-place for the user, 
    this algorithm internally allocates O(N) temporary space for merging.
    
    Args:
        arr (List[T]): The list of elements to sort.
        key (Callable): Function to extract a comparison key. Defaults to identity.
        reverse (bool): If True, sorts in descending order. Defaults to False.
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        
        # Divide
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        # Conquer
        merge_sort(left_half, key, reverse)
        merge_sort(right_half, key, reverse)
        
        # Merge
        i = j = k = 0
        
        # Merge the temp arrays back into arr
        while i < len(left_half) and j < len(right_half):
            val_left = key(left_half[i])
            val_right = key(right_half[j])
            
            # Decide order based on 'reverse' flag
            if reverse:
                condition = val_left >= val_right
            else:
                condition = val_left <= val_right
                
            if condition:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
            
        # Check for any remaining elements in left_half
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            
        # Check for any remaining elements in right_half
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


if __name__ == "__main__":
    print("Running Merge Sort Tests...")
    
    # Test 1: Basic integer sorting
    nums = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(nums)
    assert nums == [3, 9, 10, 27, 38, 43, 82], f"Test 1 Failed: {nums}"
    
    # Test 2: Reverse sorting
    nums_reverse = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(nums_reverse, reverse=True)
    assert nums_reverse == [82, 43, 38, 27, 10, 9, 3], f"Test 2 Failed: {nums_reverse}"
    
    # Test 3: String sorting by length
    words = ["recursion", "tree", "node", "algorithm", "big-o"]
    merge_sort(words, key=len)
    assert words == ["tree", "node", "big-o", "recursion", "algorithm"], f"Test 3 Failed: {words}"
    
    # Test 4: Edge cases (empty and single element)
    empty = []
    merge_sort(empty)
    assert empty == []
    
    single = [42]
    merge_sort(single)
    assert single == [42]
    
    print("All Merge Sort tests passed successfully!")
