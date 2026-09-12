r"""
# Insertion Sort: Building a Sorted Array One Element at a Time

## A. Concept Name
Insertion Sort

## B. One-Sentence Definition
Insertion Sort is an in-place, stable comparison-based sorting algorithm that builds a final sorted array one element at a time by repeatedly taking the next unsorted element and inserting it into its correct position within the already sorted portion of the array.

## C. Why Does This Exist? (What problem does it solve?)
Insertion Sort serves two main purposes:
1. **Pedagogical:** It is an intuitive introduction to sorting algorithms that mimics human behavior (like sorting cards).
2. **Practical Efficiency:** It is extremely efficient for small datasets (typically < 10-20 elements) and nearly sorted data, making it the algorithm of choice for the base cases in hybrid sorting algorithms like Timsort (used in Python) and Introsort (used in C++ std::sort).

## D. Intuition & Real-Life Analogy
- **Sorting Playing Cards:**
  Imagine you are dealt cards one by one. You hold the sorted cards in your left hand. When you receive a new card, you compare it against the cards in your left hand from right to left, and insert it in the correct position. At all times, the cards in your left hand remain sorted.

## E. Mental Model
```text
Initial Array: [ 5,  1,  4,  2,  8 ]
Sorted portion is initially just [5]. Unsorted is [1, 4, 2, 8].

Pass 1 (insert 1):
[ 5 | 1, 4, 2, 8 ] -> Compare 1 with 5. 1 < 5, so shift 5 right. Insert 1.
==> [ 1, 5 | 4, 2, 8 ]

Pass 2 (insert 4):
[ 1, 5 | 4, 2, 8 ] -> Compare 4 with 5. 4 < 5, shift 5 right. Compare 4 with 1. 4 > 1, insert 4.
==> [ 1, 4, 5 | 2, 8 ]

Pass 3 (insert 2):
[ 1, 4, 5 | 2, 8 ] -> Compare 2 with 5 (shift), 4 (shift), 1 (insert).
==> [ 1, 2, 4, 5 | 8 ]

Pass 4 (insert 8):
[ 1, 2, 4, 5 | 8 ] -> Compare 8 with 5. 8 > 5, no shifts needed. Insert 8.
==> [ 1, 2, 4, 5, 8 ] (Fully sorted)
```

## F. Formal Technical Explanation
Insertion Sort iterates through the array starting from index 1 to `N-1`. During the `i`-th iteration:
1. The element at index `i` (the "key") is selected.
2. The prefix of the array from index `0` to `i-1` is already sorted.
3. The algorithm scans the sorted prefix from right to left.
4. It shifts all elements strictly greater than the key one position to the right.
5. It inserts the key into the vacated position.
This invariant ensures that after `i` passes, the first `i+1` elements are sorted.

## G. Mathematical Foundation
1. **Total Comparisons & Shifts:**
   In the worst case (reverse sorted array), the `i`-th element requires `i` comparisons and `i` shifts.
   `Sum_{i=1}^{N-1} i = N * (N - 1) / 2 = O(N^2)`
2. **Inversions:**
   An inversion is a pair `(p, q)` where `p < q` and `A[p] > A[q]`.
   Each shift operation resolves exactly one inversion. Thus, the total number of shifts is equal to the number of inversions in the initial array.
3. **Best Case:**
   If the array is already sorted, there are 0 inversions. The inner loop makes 1 comparison and 0 shifts per element, leading to `O(N)` time complexity.

## H. Complexity Analysis
- **Time Complexity:**
  - **Best Case:** `O(N)` comparisons, `O(1)` shifts. (Array already sorted).
  - **Average Case:** `O(N^2)` comparisons and shifts.
  - **Worst Case:** `O(N^2)` comparisons and shifts. (Reverse sorted).
- **Space Complexity:**
  - **Auxiliary Space:** `O(1)` (Strictly in-place).
- **Cache & Memory Impact:**
  Highly cache-friendly due to sequential memory access and shifting adjacent elements, leading to excellent spatial locality compared to more complex algorithms.

## I. Common Mistakes & Pitfalls
1. **Starting the Outer Loop at Index 0:**
   The element at index 0 is trivially sorted by itself. The outer loop should start at index 1.
2. **Swapping Instead of Shifting:**
   A common mistake is implementing Insertion Sort by repeatedly swapping adjacent elements (like Bubble Sort). True Insertion Sort saves the key, shifts elements right, and does a single write for the key. Swapping requires 3 writes per inversion; shifting requires only 1.
3. **Violating Stability:**
   Using `>=` instead of `>` for the shift condition will cause equal elements to be shifted, changing their relative order and breaking stability.

## J. Common Confusions
- **Insertion Sort vs Selection Sort:** Selection Sort finds the absolute minimum in the remaining array and places it at the end of the sorted prefix (always `O(N^2)`). Insertion Sort takes the next element and places it where it belongs in the sorted prefix (adaptive, `O(N)` best case).
- **Insertion Sort vs Bubble Sort:** Both are `O(N^2)` and stable. However, Insertion Sort shifts instead of swapping and has significantly lower overhead, making it much faster in practice.

## K. When To Use It
- Small datasets (`N < 20`).
- Nearly sorted arrays where elements are at most `k` places away from their final positions (runs in `O(Nk)`).
- Adding a few new elements to an already sorted array.
- As the base case in hybrid algorithms like Timsort.

## L. When NOT To Use It
- Large, randomly shuffled datasets (performance degrades quadratically).
- Scenarios where `O(N log N)` guarantees are strictly required for worst-case inputs.

## M. Trade-offs
- **Pros:**
  - Extremely fast for small or nearly sorted arrays.
  - In-place and stable.
  - Very low memory overhead and highly cache-friendly.
  - Only requires a single write per inversion resolved (shifting instead of swapping).
- **Cons:**
  - `O(N^2)` time complexity makes it unscalable for large inputs.

## N. Debugging Tips
- If the first element is getting overwritten or lost, check if you correctly stored `current_value = arr[i]` before the inner loop.
- If stability is broken, double-check your comparison operator (use `>` for ascending sort, not `>=`).
- Ensure the inner loop handles the case where the key belongs at index 0 (the loop should run while `j >= 0`).

## O. Memory Hook
"Save the card, shift the bigger ones right, drop the card in the gap."

## P. Active Recall Questions
1. Why does the outer loop of Insertion Sort start at index 1 instead of 0?
2. How does Insertion Sort achieve O(N) time complexity on a sorted array?
3. What is the fundamental difference between how Insertion Sort and Selection Sort build their sorted prefixes?
4. Why is shifting more efficient than swapping in Insertion Sort?

## Q. Interview Questions & Answers
- **Q: Is it possible to optimize Insertion Sort using Binary Search?**
  *A:* Yes. This is called Binary Insertion Sort. Binary search can find the correct insertion index in `O(log i)` comparisons instead of `O(i)`. However, you still have to physically shift all the elements to make room, which takes `O(i)` time. Thus, the overall worst-case time complexity remains `O(N^2)`.
- **Q: Why does Python's built-in `sort()` (Timsort) use Insertion Sort under the hood?**
  *A:* For small arrays (e.g., length < 32 or 64), the constant factor overhead of recursion and array allocation in Merge Sort outweighs its algorithmic efficiency. Insertion Sort has virtually zero overhead, making it faster for these small chunks ("runs").

## R. Project Connections
- **Python's `list.sort()` (Timsort):** Uses Insertion Sort to extend small "runs" (consecutive sorted segments) to a minimum size.
- **V8 JavaScript Engine:** Uses Insertion Sort for sorting small arrays (typically fewer than 10 elements) or small partitions during Quicksort.
- **Database Index Maintenance:** Often used to insert new records into small, already-sorted B-Tree nodes.

## S. Real-World Failure Stories & Engineering Lessons
In early implementations of the C++ standard library, some `std::sort` algorithms strictly used Quicksort. Developers noticed that for small arrays of structs, `std::sort` was surprisingly slow compared to hand-rolled C loops. The standard library was later updated to Introsort, which falls back to Insertion Sort for partitions smaller than 16 elements, drastically reducing function call overhead and improving cache locality.
*Lesson:* Algorithmic complexity `O(N log N)` doesn't mean "always faster." For small `N`, constant factors matter more than asymptotic scaling.

## T. Comparative Benchmark & Empirical Behavior
| Algorithm | Best Time | Average Time | Worst Time | Auxiliary Space | Stable? | Overhead |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Insertion Sort** | O(N) | O(N^2) | O(N^2) | O(1) | Yes | Very Low |
| **Bubble Sort** | O(N) | O(N^2) | O(N^2) | O(1) | Yes | High (Swaps) |
| **Selection Sort**| O(N^2) | O(N^2) | O(N^2) | O(1) | No | Low |
| **Merge Sort** | O(N log N)| O(N log N) | O(N log N) | O(N) | Yes | High |
| **Timsort** | O(N) | O(N log N) | O(N log N) | O(N) | Yes | Medium |

## U. Edge Cases & Boundary Conditions
1. Empty list (`[]`): Outer loop does not execute; returns immediately.
2. Single element (`[42]`): Outer loop does not execute; array is already sorted.
3. Pre-sorted list (`[1, 2, 3]`): Inner loop condition immediately fails; completes in `O(N)` time.
4. Reverse sorted list (`[3, 2, 1]`): Maximum number of shifts (`O(N^2)`); worst-case scenario.
5. All identical elements (`[7, 7, 7]`): Inner loop immediately fails; stability is maintained.

## V. Recommended Practice Problems
- LeetCode 147: Insertion Sort List (Implementing Insertion Sort on a Singly Linked List)
- LeetCode 75: Sort Colors
- Hackerrank: Insertion Sort - Part 1 & Part 2

## W. Verification & Edge-Case Checklist
- [x] Handled empty array and single-element array correctly.
- [x] Inner loop bounds check `j >= 0` to prevent index out of bounds.
- [x] Correct shift logic used instead of repetitive swapping.
- [x] Strict inequality `>` (or `<` for reverse) used to maintain stability.
- [x] Best-case `O(N)` behavior verified by early termination of the inner loop.

## X. Core Takeaways & Summary
- Insertion Sort is the champion of simple sorts, highly optimized for small or nearly sorted arrays.
- It operates by shifting elements to make space for the current key, requiring only `O(1)` space and preserving stability.
- Its real-world importance comes from its role as the foundational base-case algorithm in modern standard libraries (Timsort, Introsort).
"""

from typing import TypeVar, List, Callable

T = TypeVar('T')

def insertion_sort(
    arr: List[T],
    key: Callable[[T], any] = lambda x: x,
    reverse: bool = False
) -> None:
    """
    Sorts a list in-place using the Insertion Sort algorithm.
    
    Args:
        arr (List[T]): The list of elements to sort.
        key (Callable): Function to extract a comparison key. Defaults to identity.
        reverse (bool): If True, sorts in descending order. Defaults to False.
        
    Returns:
        None: The list is modified in-place.
    """
    n = len(arr)
    
    # Start from the second element (index 1), assume index 0 is trivially sorted
    for i in range(1, n):
        current_value = arr[i]
        current_key = key(current_value)
        
        # Position to compare against (end of the sorted portion)
        j = i - 1
        
        # Shift elements of arr[0..i-1], that are greater (or lesser for reverse) 
        # than current_key, to one position ahead of their current position
        if reverse:
            while j >= 0 and key(arr[j]) < current_key:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            while j >= 0 and key(arr[j]) > current_key:
                arr[j + 1] = arr[j]
                j -= 1
                
        # Insert the current_value at the correct position
        arr[j + 1] = current_value


if __name__ == "__main__":
    print("Running Insertion Sort Tests...")
    
    # Test 1: Basic integer sorting
    nums = [12, 11, 13, 5, 6]
    insertion_sort(nums)
    assert nums == [5, 6, 11, 12, 13], f"Test 1 Failed: {nums}"
    
    # Test 2: Reverse sorting
    nums_reverse = [12, 11, 13, 5, 6]
    insertion_sort(nums_reverse, reverse=True)
    assert nums_reverse == [13, 12, 11, 6, 5], f"Test 2 Failed: {nums_reverse}"
    
    # Test 3: Stability test with objects
    class Item:
        def __init__(self, val, ident):
            self.val = val
            self.ident = ident
        def __repr__(self):
            return f"({self.val}, '{self.ident}')"
            
    items = [Item(3, 'a'), Item(1, 'b'), Item(3, 'c'), Item(2, 'd')]
    insertion_sort(items, key=lambda x: x.val)
    # 3, 'a' should appear before 3, 'c'
    assert items[2].ident == 'a' and items[3].ident == 'c', "Stability Test Failed"
    
    # Test 4: Nearly sorted array (best case scenario)
    nearly_sorted = [1, 2, 3, 5, 4]
    insertion_sort(nearly_sorted)
    assert nearly_sorted == [1, 2, 3, 4, 5], "Nearly sorted test failed"
    
    print("All Insertion Sort tests passed successfully!")
