r"""
# Insertion Sort: Comprehensive Pedagogical and Practical Guide

## A. Concept Name
Insertion Sort (including In-Place Shift, Binary Insertion Sort, and Linked List Insertion Sort).

## B. One-Sentence Definition
Insertion Sort is an intuitive, comparison-based, in-place, and stable sorting algorithm that incrementally builds a sorted prefix of an array by removing one element at a time from the unsorted portion and inserting it into its correct relative position among the already-sorted elements.

## C. Why Does This Exist? (What problem does it solve?)
While asymptotically superior algorithms such as Quick Sort, Merge Sort, and Heap Sort achieve $O(N \log N)$ complexity, they introduce significant architectural overhead: recursion stack allocation, cache misses from non-local memory jumps, and complex partitioning or merging logic.

Insertion Sort solves several critical real-world problems:
1. **Low-Overhead Sorting for Small Datasets ($N \le 32$ to $64$)**:
   The constant factor hidden inside Big-O notation is exceptionally small for Insertion Sort. On small collections, it executes fewer CPU machine instructions and exhibits superior cache locality compared to Quick Sort or Merge Sort.
2. **Adaptive Sorting for Nearly Sorted Data**:
   When an input sequence is already partially or substantially sorted (e.g., append operations on a sorted log, or real-time event streams with minor clock skews), Insertion Sort runs in near-linear time $O(N + I)$, where $I$ is the number of inversions. If $I \ll N^2$, it outperforms even Quick Sort.
3. **Online Streaming Capabilities**:
   Insertion Sort can sort data continuously as it arrives over a network socket or user input stream, maintaining a perpetually sorted list without needing the entire dataset upfront.
4. **Stable In-Place Reordering**:
   It achieves strict sorting stability ($O(1)$ auxiliary memory without reordering equal keys), which is vital for multi-column database ordering.
5. **The Foundational Base-Case Engine for Hybrid Sorts**:
   Industrial sorting engines—including **Timsort** (used in CPython, Java SE, Android, and V8) and **Introsort** (used in C++ `std::sort`)—switch to Insertion Sort once divide-and-conquer recursions reach small partitions ($N \le 32$ or $N \le 64$).

## D. Intuition & Real-Life Analogy
- **Sorting a Hand of Playing Cards**:
  Imagine you are dealt a hand of playing cards face down on a table. You pick up the cards one by one into your left hand:
  - Your left hand always holds a sorted sub-hand.
  - When picking up a new card (the "key") with your right hand, you scan your left hand from right to left (from largest to smallest).
  - You slide each card that is larger than your new card one slot to the right to make room.
  - As soon as you encounter a card smaller than or equal to the new card, you slide your new card into the vacant slot.
- **Library Book Reshelving**:
  A librarian returns books to a shelf one by one. For each book, they find the correct alphabetical position on the shelf, slide the existing books to the right, and slot the new book into place.

## E. Mental Model
Consider an array partitioned into two logical zones:
`[ SORTED PREFIX | KEY | UNSORTED SUFFIX ]`

```text
Initial Array: [ 7, 3, 5, 2 ]

Pass 1 (i = 1):
  Prefix: [ 7 ]  | Key: 3 | Suffix: [ 5, 2 ]
  Compare Key (3) with 7 -> 7 > 3, shift 7 right.
  Slot Key (3) at index 0.
  State:  [ 3, 7, 5, 2 ]

Pass 2 (i = 2):
  Prefix: [ 3, 7 ] | Key: 5 | Suffix: [ 2 ]
  Compare Key (5) with 7 -> 7 > 5, shift 7 right.
  Compare Key (5) with 3 -> 3 <= 5, stop shifting!
  Slot Key (5) at index 1.
  State:  [ 3, 5, 7, 2 ]

Pass 3 (i = 3):
  Prefix: [ 3, 5, 7 ] | Key: 2 | Suffix: [ ]
  Compare Key (2) with 7 -> shift 7 right.
  Compare Key (2) with 5 -> shift 5 right.
  Compare Key (2) with 3 -> shift 3 right.
  Slot Key (2) at index 0.
  State:  [ 2, 3, 5, 7 ] (Fully Sorted!)
```

## F. Formal Technical Explanation
Insertion Sort establishes and maintains a rigorous **Loop Invariant**:
- **Loop Invariant**: At the start of each outer loop iteration indexed by $i$ ($1 \le i < N$), the subarray $A[0 \dots i-1]$ consists of the elements originally residing in $A[0 \dots i-1]$, but rearranged in strictly non-decreasing sorted order.
- **Initialization**: Prior to the first iteration ($i = 1$), the subarray $A[0 \dots 0]$ contains exactly one element. A single-element list is trivially sorted. Thus, the invariant holds.
- **Maintenance**: In iteration $i$, the element $A[i]$ is extracted into variable `key`. The inner loop shifts elements $A[j]$ (for $j = i-1, i-2, \dots$) that are strictly greater than `key` one position to the right ($A[j+1] = A[j]$). The shift ceases when $j < 0$ or $A[j] \le \text{key}$. Setting $A[j+1] = \text{key}$ places `key` in its correct relative sorted location. Subarray $A[0 \dots i]$ now contains the elements originally in $A[0 \dots i]$ in sorted order, preserving the invariant for iteration $i+1$.
- **Termination**: The outer loop terminates when $i = N$. Substituting $i = N$ into the loop invariant yields that subarray $A[0 \dots N-1]$ consists of all elements originally in $A$ in sorted order. The entire array is sorted.

## G. Mathematical Foundation
Let $N$ denote the length of array $A$.
1. **Inversions**:
   An inversion is a pair of indices $(j, k)$ such that $j < k$ and $A[j] > A[k]$.
   Let $I$ be the total count of inversions in array $A$:
   $$I = |\{ (j, k) \mid 0 \le j < k < N \text{ and } A[j] > A[k] \}|$$
   Every single element shift performed in the inner loop of Insertion Sort resolves exactly one inversion. Therefore, the total number of element shifts across the entire execution is identically equal to $I$.

2. **Best-Case Analysis (Already Sorted Array)**:
   - $A[0] \le A[1] \le \dots \le A[N-1] \implies I = 0$.
   - For every $i \in [1, N-1]$, the inner loop condition `A[j] > key` fails on the very first comparison ($j = i - 1$).
   - Total comparisons: $C_{\text{best}} = \sum_{i=1}^{N-1} 1 = N - 1$.
   - Total shifts: $S_{\text{best}} = 0$.
   - Time Complexity: $\Theta(N)$.

3. **Worst-Case Analysis (Strictly Reverse-Sorted Array)**:
   - $A[0] > A[1] > \dots > A[N-1] \implies I = \frac{N(N-1)}{2}$.
   - For each $i$, the key must be compared with and shifted past all $i$ elements in the prefix:
   - Total comparisons: $C_{\text{worst}} = \sum_{i=1}^{N-1} i = \frac{N(N-1)}{2}$.
   - Total shifts: $S_{\text{worst}} = \sum_{i=1}^{N-1} i = \frac{N(N-1)}{2}$.
   - Time Complexity: $\Theta(N^2)$.

4. **Average-Case Analysis (Random Permutation)**:
   - Assuming uniform distribution over all $N!$ permutations of distinct keys:
   - The probability that any pair $(j, k)$ forms an inversion is exactly $\frac{1}{2}$.
   - Expected number of inversions:
     $$E[I] = \frac{1}{2} \cdot \binom{N}{2} = \frac{N(N-1)}{4}$$
   - On average, the inner loop scans halfway through the sorted prefix before finding the insertion slot:
     $$E[C] \approx \sum_{i=1}^{N-1} \frac{i}{2} \approx \frac{N^2}{4} \implies \Theta(N^2)$$

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - Best Case: $O(N)$ comparisons, $O(1)$ shifts (Array already sorted).
  - Average Case: $O(N^2)$ comparisons and shifts ($\approx N^2/4$ operations).
  - Worst Case: $O(N^2)$ comparisons and shifts ($\approx N^2/2$ operations).
  - Adaptive Bound: $O(N + I)$ where $I$ is the number of inversions.
- **Space Complexity**:
  - Auxiliary Space: $O(1)$ (In-place; requires only scalar registers for `key`, `i`, and `j`).
  - Stack Space: $O(1)$ iterative; $O(N)$ for naive recursive variants.
- **Hardware & Cache Dynamics**:
  - **Spatial Locality**: Inner loop shifts read and write contiguous memory backwards. Modern CPU hardware prefetchers and store buffers efficiently pipeline sequential contiguous operations.
  - **Branch Predictor Friendly**: When the array is nearly sorted, the inner loop branch (`key < arr[j]`) is predicted as `False` with near-100% accuracy, causing zero pipeline flushes.
  - **Memory Bus Traffic**: By shifting values (`arr[j+1] = arr[j]`) instead of swapping (`arr[j], arr[j+1] = arr[j+1], arr[j]`), Insertion Sort performs 1 write per shift rather than 2 writes and 2 reads, cutting memory bus traffic by more than 50%.

## I. Common Mistakes & Pitfalls
1. **Swapping Instead of Shifting**:
   Beginners often implement Insertion Sort by repeatedly swapping adjacent elements:
   ```python
   # INEFFICIENT (3x memory bus penalty)
   while j >= 0 and arr[j] > arr[j + 1]:
       arr[j], arr[j + 1] = arr[j + 1], arr[j]
       j -= 1
   ```
   Each tuple swap performs 2 reads and 2 writes. The optimized approach extracts `key = arr[i]`, performs single writes (`arr[j+1] = arr[j]`), and writes `arr[j+1] = key` once at the end.
2. **Breaking Stability**:
   Using `key <= arr[j]` instead of `key < arr[j]` in the inner loop condition causes equal elements to shift past each other, destroying sorting stability.
3. **Off-by-One Boundary Condition**:
   Using `while j > 0` instead of `while j >= 0` leaves the element at index `0` uninspected, failing whenever the key belongs at the very beginning of the array.
4. **Outer Loop Range**:
   Starting the outer loop at `0` instead of `1` is redundant; an array slice of length 1 is already sorted.
5. **Binary Insertion Sort Fallacy**:
   Believing that Binary Insertion Sort achieves $O(N \log N)$ overall time complexity. Binary search reduces the *comparison* count to $O(N \log N)$, but sliding elements in an array still requires $O(N^2)$ memory writes.

## J. Common Confusions
- **Insertion Sort vs. Selection Sort**:
  - *Selection Sort* searches the entire unsorted suffix to find the global minimum and swaps it once into place. It ALWAYS performs $\Theta(N^2)$ comparisons, even if the array is already sorted. It is non-adaptive and inherently unstable.
  - *Insertion Sort* takes the next unsorted element and searches the sorted prefix to find its insertion position. It is adaptive ($O(N)$ best case) and stable.
- **Insertion Sort vs. Bubble Sort**:
  - Both are $O(N^2)$ average/worst-case, $O(N)$ best-case, stable, and in-place.
  - However, Insertion Sort examines only as many elements as necessary in the prefix, whereas Bubble Sort scans through elements repeatedly. In practice, Insertion Sort is 2x to 3x faster than Bubble Sort and has negligible constant factors.
- **Insertion Sort vs. Shellsort**:
  - Shellsort is a generalization of Insertion Sort that allows exchanges of elements that are far apart ($h$-sorting), breaking the $O(N^2)$ barrier down to $O(N^{4/3})$ or $O(N \log^2 N)$, but sacrificing stability.

## K. When To Use It
- Small arrays ($N \le 32$ to $64$).
- Nearly sorted arrays where only a few elements are out of order ($I = O(N)$).
- Online/streaming data: elements arrive continuously and must be maintained in sorted order.
- Embedded systems with stringent memory limits where $O(1)$ auxiliary RAM is required.
- As the sub-routine for small partitions inside divide-and-conquer algorithms (Timsort, Introsort).

## L. When NOT To Use It
- Large unsorted datasets ($N > 1,000$), where quadratic time $O(N^2)$ causes severe performance bottlenecks.
- Reverse-sorted large datasets (worst-case quadratic behavior).
- Real-time hard-deadline systems sorting large arrays where predictable $O(N \log N)$ worst-case latency is mandatory (use Merge Sort or Heap Sort).

## M. Trade-offs
| Algorithm | Best Time | Avg Time | Worst Time | Space | Stable? | Adaptive? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Insertion Sort** | $\mathbf{O(N)}$ | $O(N^2)$ | $O(N^2)$ | $\mathbf{O(1)}$ | **Yes** | **Yes** |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | No |
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Yes |
| **Quick Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | No | No |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | No |
| **Timsort** | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Yes |

## N. Debugging Tips
- Trace state per iteration: Print `(i, key, j, arr)` after each outer iteration.
- Instrument counters for comparisons and shifts to empirically confirm $O(N)$ vs $O(N^2)$ on test arrays.
- Verify stability using composite keys (e.g., `(primary_key, insertion_index)`).
- Edge test: Verify lists with duplicate keys (`[3, 3, 3]`), descending order (`[5, 4, 3, 2, 1]`), and single element (`[42]`).

## O. Memory Hook
**"Pick a key, slide to the right, insert the card where it fits tight!"**
Visualize holding playing cards: pull one card out, slide larger cards right, drop the key into the newly opened gap.

## P. Active Recall Questions
1. Why does Insertion Sort achieve $O(N)$ time on an already sorted list, whereas Selection Sort remains $O(N^2)$?
2. What is an inversion, and why is the total number of shifts in Insertion Sort exactly equal to the inversion count $I$?
3. Why does Binary Insertion Sort fail to reduce overall worst-case time complexity from $O(N^2)$ to $O(N \log N)$?
4. How does replacing adjacent swaps with shift assignments reduce memory bus pressure?
5. In what way does Timsort use Insertion Sort to achieve state-of-the-art performance in standard libraries?

## Q. Interview Questions & Answers
- **Q1: How do you sort a Singly Linked List in $O(1)$ auxiliary space using Insertion Sort? How does its time complexity compare to array-based Insertion Sort?**  
  *Answer:* Create a dummy node representing the head of the sorted list. Iterate through the original list; for each node, scan the sorted list from the head to find the insertion location, and splice the node in via pointer rewiring. While pointer splicing takes $O(1)$ time (avoiding array memory shifts), finding the position still requires $O(N)$ pointer traversals because linked lists lack random access. Thus, time complexity remains $O(N^2)$ worst-case, with $O(1)$ auxiliary space.
- **Q2: You are given an array where every element is at most $k$ positions away from its sorted position ($k$-sorted array). What is the time complexity of Insertion Sort on this array?**  
  *Answer:* In a $k$-sorted array, for any element at index $i$, the inner loop shifts at most $k$ elements to the right. Therefore, the inner loop executes at most $k$ iterations for each of the $N-1$ elements. Total time complexity is $O(N \cdot k)$. When $k$ is a small constant ($k \ll N$), Insertion Sort runs in $O(N)$ linear time, outperforming Quick Sort and matching a Min-Heap approach ($O(N \log k)$) with zero heap allocation overhead.
- **Q3: Why is Insertion Sort preferred over Quick Sort for tiny partitions in hybrid sorting algorithms?**  
  *Answer:* Quick Sort incurs significant fixed overhead: recursive function call frame allocations, pivot selection logic, three-way partitioning branches, and cache misses from jumping across the full partition width. For $N \le 32$, this constant factor overhead dwarfs the quadratic $N^2$ cost of Insertion Sort. Insertion Sort executes in tight, branch-predicted loops with minimal instruction counts and high spatial cache locality.

## R. Project Connections (Where is this used in real systems?)
- **CPython (`Objects/listobject.c`)**: Timsort uses `binarysort()` (a binary insertion sort variant) to sort small chunks (called "runs") of size up to 64 before merging them.
- **Java JDK (`java.util.DualPivotQuicksort`)**: Java's standard primitive array sort delegates partitions smaller than 47 elements directly to Insertion Sort.
- **Linux Kernel (`lib/sort.c` & Task Scheduler)**: Used for sorting small device arrays and maintaining real-time scheduling priority runqueues when tasks arrive mostly ordered.
- **Game Engine Rendering (Z-Buffering / Sprite Sorting)**: Transparent 2D sprites must be drawn back-to-front every frame. Because camera and entity positions change only incrementally between frames (60 FPS), sprite depth arrays remain nearly sorted frame-to-frame. Insertion Sort re-sorts thousands of sprites in near-linear $O(N)$ time.

## S. Edge Cases & Boundary Conditions
1. Empty list (`[]`): Outer loop does not execute; returns `[]`.
2. Single-element list (`[10]`): Outer loop does not execute; returns `[10]`.
3. Two elements sorted (`[1, 2]`): 1 comparison, 0 shifts.
4. Two elements reversed (`[2, 1]`): 1 comparison, 1 shift.
5. All elements identical (`[5, 5, 5, 5]`): 1 comparison per element, 0 shifts; preserves order.
6. Strictly ascending array (`[1, 2, 3, 4, 5]`): $N-1$ comparisons, 0 shifts ($O(N)$ best case).
7. Strictly descending array (`[5, 4, 3, 2, 1]`): $\frac{N(N-1)}{2}$ comparisons and shifts ($O(N^2)$ worst case).
8. Duplicate elements mixed: Demonstrates algorithm stability.

## T. Algorithmic Variants & Paradigms
- **Standard In-Place Insertion Sort**: Uses shift optimization (`arr[j+1] = arr[j]`).
- **Binary Insertion Sort**: Uses binary search (`bisect`) to locate the insertion index in $O(\log N)$ comparisons, followed by $O(N)$ slice shift.
- **Recursive Insertion Sort**: Demonstrates inductive divide-and-conquer logic (functional programming paradigm).
- **Singly Linked List Insertion Sort**: Demonstrates in-place pointer manipulation without array memory copying.
- **Generic Key Insertion Sort**: Supports custom comparator functions and reverse sorting.

## U. Algorithmic Comparison Table
| Algorithm | Best Time | Avg Time | Worst Time | Aux Space | Stable? | Online? | Inversions Handled |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Insertion** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Yes | $O(N + I)$ |
| **Binary Insertion** | $O(N \log N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Yes | Minimizes comparisons |
| **Selection Sort** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No | No | Unconditional $O(N^2)$ |
| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | No | Adjacent swaps |
| **Shellsort** | $O(N \log N)$ | $O(N^{4/3})$| $O(N^{3/2})$ | $O(1)$ | No | No | Gap-based sub-arrays |

## V. Practical Implementation Exercises
1. Modify Insertion Sort to track the exact count of comparisons and shifts executed, and verify against theoretical inversion counts.
2. Implement Binary Insertion Sort on a Python list using `bisect_right` to maintain stability.
3. Construct an in-place Linked List Insertion Sort without creating new nodes.
4. Build an online streaming median tracker backed by an insertion-sorted buffer.

## W. Step-by-Step Execution Trace
Sorting array `[8, 3, 5, 4, 1]` ($N = 5$):
| Pass ($i$) | Key | Subarray Before Pass | Inner Comparisons ($j$) | Shifts Performed | Subarray After Pass |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 3 | `[8 | 3, 5, 4, 1]` | `8 > 3` (True) | `arr[1] = 8` | `[3, 8 | 5, 4, 1]` |
| 2 | 5 | `[3, 8 | 5, 4, 1]` | `8 > 5` (True), `3 > 5` (False)| `arr[2] = 8` | `[3, 5, 8 | 4, 1]` |
| 3 | 4 | `[3, 5, 8 | 4, 1]` | `8 > 4` (True), `5 > 4` (True), `3 > 4` (False) | `arr[3]=8, arr[2]=5` | `[3, 4, 5, 8 | 1]` |
| 4 | 1 | `[3, 4, 5, 8 | 1]` | `8>1`, `5>1`, `4>1`, `3>1` (All True) | `arr[4]=8, arr[3]=5, arr[2]=4, arr[1]=3` | `[1, 3, 4, 5, 8]` |

Total Inversions = $1 + 1 + 2 + 4 = 8$ shifts. Final Sorted Array: `[1, 3, 4, 5, 8]`.

## X. Key Takeaways & Summary Anchor
- Insertion Sort builds a sorted prefix one element at a time.
- Runtime is strictly bounded by $O(N + I)$, making it linear for nearly sorted inputs.
- Always implement the shifting optimization (`arr[j+1] = arr[j]`) instead of swapping.
- It remains the gold-standard base case inside production hybrid sorting engines like Timsort.
"""

from typing import Any, Callable, List, Optional, Sequence, Tuple, TypeVar
import bisect
import copy

T = TypeVar("T")


# ==============================================================================
# DATA STRUCTURE: SINGLY LINKED LIST (FOR LINKED LIST INSERTION SORT)
# ==============================================================================

class ListNode:
    """A node in a singly linked list for educational sorting demonstrations."""
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        values = []
        curr = self
        while curr:
            values.append(str(curr.val))
            curr = curr.next
        return " -> ".join(values)


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATIONS
# ==============================================================================

def insertion_sort(arr: List[T]) -> List[T]:
    """
    Standard In-Place Insertion Sort with Shift Optimization.
    
    Mutates the given list in-place and returns it.
    
    Args:
        arr (List[T]): The mutable list of comparable items to sort.
        
    Returns:
        List[T]: The sorted list (same reference).
        
    Complexity:
        Time: O(N) Best, O(N^2) Average, O(N^2) Worst.
        Space: O(1) Auxiliary.
    """
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Shift elements of arr[0..i-1] that are greater than key to the right
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        # Place key into its sorted slot
        arr[j + 1] = key
    return arr


def insertion_sort_with_stats(arr: List[T]) -> Tuple[List[T], int, int]:
    """
    Educational Insertion Sort tracking comparisons and shifts.
    
    Args:
        arr (List[T]): The list to sort.
        
    Returns:
        Tuple[List[T], int, int]: (Sorted list, comparison_count, shift_count).
    """
    comparisons = 0
    shifts = 0
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if key < arr[j]:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
        
    return arr, comparisons, shifts


def binary_insertion_sort(arr: List[T]) -> List[T]:
    """
    Binary Insertion Sort.
    
    Uses binary search to locate the exact insertion slot for the key in O(log N)
    comparisons, then shifts elements right in O(N).
    Preserves stability by inserting after any identical keys (bisect_right semantics).
    
    Args:
        arr (List[T]): List to sort in-place.
        
    Returns:
        List[T]: Sorted list.
        
    Complexity:
        Comparisons: O(N log N) in all cases.
        Shifts/Data Movement: O(N^2) Average/Worst, O(1) Best.
        Space: O(1) Auxiliary.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        # Binary search for insertion position in sorted prefix arr[0..i]
        low = 0
        high = i
        while low < high:
            mid = (low + high) // 2
            if key < arr[mid]:
                high = mid
            else:
                # Maintain stability: key goes to the right of equal elements
                low = mid + 1
        
        # Shift elements from low to i - 1 one position right
        for j in range(i, low, -1):
            arr[j] = arr[j - 1]
        arr[low] = key
        
    return arr


def insertion_sort_recursive(arr: List[T], n: Optional[int] = None) -> List[T]:
    """
    Recursive Insertion Sort.
    
    Demonstrates inductive reduction: sort subarray arr[0..n-2], then insert arr[n-1].
    Note: Educational only. Limited by Python's recursion depth limit.
    
    Args:
        arr (List[T]): The list to sort.
        n (Optional[int]): Prefix length to sort. Defaults to len(arr).
        
    Returns:
        List[T]: The sorted list.
    """
    if n is None:
        n = len(arr)
        
    # Base Case: An array of length 0 or 1 is already sorted
    if n <= 1:
        return arr
        
    # Inductive Step: Recursively sort the first n - 1 elements
    insertion_sort_recursive(arr, n - 1)
    
    # Insert the n-th element (index n - 1) into the sorted prefix
    key = arr[n - 1]
    j = n - 2
    while j >= 0 and key < arr[j]:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key
    
    return arr


def insertion_sort_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Insertion Sort on a Singly Linked List.
    
    Sorts a linked list in-place by rewiring node pointers without allocating
    array buffers.
    
    Args:
        head (Optional[ListNode]): Head of unsorted linked list.
        
    Returns:
        Optional[ListNode]: Head of sorted linked list.
        
    Complexity:
        Time: O(N^2) Worst/Average, O(N) Best.
        Space: O(1) Auxiliary.
    """
    if not head or not head.next:
        return head
        
    dummy = ListNode(0)  # Dummy node pointing to head of sorted chain
    curr = head
    
    while curr:
        next_temp = curr.next  # Save next node to process
        
        # Find insertion position in the sorted chain starting from dummy
        prev = dummy
        while prev.next and prev.next.val < curr.val:
            prev = prev.next
            
        # Splice curr between prev and prev.next
        curr.next = prev.next
        prev.next = curr
        
        curr = next_temp
        
    return dummy.next


# ==============================================================================
# 2. ADVANCED / GENERIC PRODUCTION-GRADE IMPLEMENTATION
# ==============================================================================

def insertion_sort_generic(
    arr: List[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    """
    Production-grade Generic In-Place Insertion Sort.
    
    Supports custom key extractors and reverse ordering, mirroring Python's
    built-in sort semantics.
    
    Args:
        arr (List[T]): List of items to sort in-place.
        key (Optional[Callable[[T], Any]]): Transformation function applied to each element.
        reverse (bool): If True, sorts descending; otherwise ascending.
        
    Returns:
        List[T]: The sorted list.
    """
    if key is None:
        key = lambda x: x
        
    n = len(arr)
    for i in range(1, n):
        current_item = arr[i]
        current_val = key(current_item)
        j = i - 1
        
        if not reverse:
            # Ascending: Shift items strictly greater than current_val
            while j >= 0 and key(arr[j]) > current_val:
                arr[j + 1] = arr[j]
                j -= 1
        else:
            # Descending: Shift items strictly smaller than current_val
            while j >= 0 and key(arr[j]) < current_val:
                arr[j + 1] = arr[j]
                j -= 1
                
        arr[j + 1] = current_item
        
    return arr


# ==============================================================================
# 3. INDUSTRY-STANDARD / LIBRARY USAGE
# ==============================================================================

def online_stream_insertion(stream_data: Sequence[T]) -> List[T]:
    """
    Simulates online stream sorting using Python's standard `bisect.insort`.
    
    Demonstrates how Insertion Sort concepts power online stream maintenance.
    `bisect.insort` performs binary search for O(log N) comparisons, followed
    by list insertion.
    
    Args:
        stream_data (Sequence[T]): Streaming data items arriving sequentially.
        
    Returns:
        List[T]: Continuously maintained sorted collection.
    """
    sorted_buffer: List[T] = []
    for item in stream_data:
        # bisect.insort inserts item into sorted_buffer preserving sorted order
        bisect.insort(sorted_buffer, item)
    return sorted_buffer


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DEBUGGING COMMENTARY
# ==============================================================================

def insertion_sort_buggy_swap_and_instability(arr: List[Any]) -> List[Any]:
    """
    BUGGY IMPLEMENTATION #1: Inefficient Swapping and Broken Stability.
    
    Flaws:
    1. Condition `arr[j] >= arr[j + 1]` uses `>=` instead of `>`, which swaps
       equal elements, destroying sorting stability.
    2. Performs repeated tuple swaps instead of shifts, causing 2x memory writes.
    
    Diagnostic Analysis:
    - Input: [('A', 1), ('B', 1)]
    - Result: [('B', 1), ('A', 1)] (Relative order inverted!)
    - Fix: Change condition to strictly greater (`>`) and replace swaps with shifts.
    """
    for i in range(1, len(arr)):
        j = i - 1
        while j >= 0 and arr[j] >= arr[j + 1]:  # <- BUG: '>=' breaks stability!
            arr[j], arr[j + 1] = arr[j + 1], arr[j]  # <- Inefficient swap
            j -= 1
    return arr


def insertion_sort_buggy_off_by_one(arr: List[T]) -> List[T]:
    """
    BUGGY IMPLEMENTATION #2: Off-By-One Boundary Error on Prefix Scan.
    
    Flaw:
    The inner loop checks `while j > 0` instead of `while j >= 0`.
    As a result, index 0 is never inspected. If the key is the smallest
    element encountered so far, it will never be placed at index 0!
    
    Diagnostic Analysis:
    - Input: [5, 2, 4]
    - Pass 1 (key=2): j stops at 1 (does not check j=0). 2 is slotted at index 1!
    - Output: [5, 2, 4] instead of [2, 4, 5].
    - Fix: Change condition to `while j >= 0`.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j > 0 and key < arr[j]:  # <- BUG: Ignores index 0!
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite validating all implementations and edge cases.
    """
    print(">>> Running Insertion Sort Comprehensive Test Suite...")
    
    # Test Datasets
    empty_list: List[int] = []
    single_list: List[int] = [42]
    already_sorted: List[int] = [1, 2, 3, 4, 5, 6, 7]
    reverse_sorted: List[int] = [7, 6, 5, 4, 3, 2, 1]
    with_duplicates: List[int] = [4, 2, 7, 2, 4, 1, 3]
    negative_values: List[int] = [-5, 12, -20, 0, 7, -3]
    
    # 1. Standard In-Place Insertion Sort Tests
    assert insertion_sort(empty_list.copy()) == [], "Failed on empty list"
    assert insertion_sort(single_list.copy()) == [42], "Failed on single element"
    assert insertion_sort(already_sorted.copy()) == [1, 2, 3, 4, 5, 6, 7], "Failed on sorted array"
    assert insertion_sort(reverse_sorted.copy()) == [1, 2, 3, 4, 5, 6, 7], "Failed on reverse array"
    assert insertion_sort(with_duplicates.copy()) == [1, 2, 2, 3, 4, 4, 7], "Failed on duplicates"
    assert insertion_sort(negative_values.copy()) == [-20, -5, -3, 0, 7, 12], "Failed on negatives"
    
    # 2. Performance & Inversion Metric Tests
    sorted_res, comps_sorted, shifts_sorted = insertion_sort_with_stats([1, 2, 3, 4, 5])
    assert comps_sorted == 4, f"Expected 4 comparisons on sorted array, got {comps_sorted}"
    assert shifts_sorted == 0, f"Expected 0 shifts on sorted array, got {shifts_sorted}"
    
    rev_res, comps_rev, shifts_rev = insertion_sort_with_stats([5, 4, 3, 2, 1])
    # For N=5 reverse: Inversions = 5 * 4 // 2 = 10
    assert shifts_rev == 10, f"Expected exactly 10 shifts for reverse array, got {shifts_rev}"
    assert comps_rev == 10, f"Expected 10 comparisons for reverse array, got {comps_rev}"
    
    # 3. Binary Insertion Sort Tests
    assert binary_insertion_sort(empty_list.copy()) == []
    assert binary_insertion_sort(single_list.copy()) == [42]
    assert binary_insertion_sort(reverse_sorted.copy()) == [1, 2, 3, 4, 5, 6, 7]
    assert binary_insertion_sort(with_duplicates.copy()) == [1, 2, 2, 3, 4, 4, 7]
    
    # 4. Recursive Insertion Sort Tests
    assert insertion_sort_recursive(reverse_sorted.copy()) == [1, 2, 3, 4, 5, 6, 7]
    assert insertion_sort_recursive(with_duplicates.copy()) == [1, 2, 2, 3, 4, 4, 7]
    assert insertion_sort_recursive([]) == []
    
    # 5. Singly Linked List Insertion Sort Tests
    def build_ll(vals: List[int]) -> Optional[ListNode]:
        if not vals:
            return None
        head = ListNode(vals[0])
        curr = head
        for v in vals[1:]:
            curr.next = ListNode(v)
            curr = curr.next
        return head
        
    def ll_to_list(head: Optional[ListNode]) -> List[int]:
        res = []
        curr = head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res
        
    ll_head = build_ll([4, 2, 1, 3])
    sorted_ll = insertion_sort_linked_list(ll_head)
    assert ll_to_list(sorted_ll) == [1, 2, 3, 4], "Linked list insertion sort failed"
    assert insertion_sort_linked_list(None) is None
    
    # 6. Generic Sort Tests (Custom Keys & Reverse)
    words = ["banana", "pie", "apple", "kiwi"]
    insertion_sort_generic(words, key=len)
    assert words == ["pie", "kiwi", "apple", "banana"], "Generic key=len sort failed"
    
    nums = [10, 40, 20, 30]
    insertion_sort_generic(nums, reverse=True)
    assert nums == [40, 30, 20, 10], "Generic reverse sort failed"
    
    # 7. Stability Verification
    # Sorting by student score; identical scores should preserve original relative name ordering
    students = [("Alice", 85), ("Bob", 92), ("Charlie", 85), ("David", 70)]
    insertion_sort_generic(students, key=lambda s: s[1])
    assert students == [("David", 70), ("Alice", 85), ("Charlie", 85), ("Bob", 92)], \
        "Stability test failed: Alice must precede Charlie!"
        
    # 8. Library Equivalent Comparison
    stream_input = [7, 2, 9, 1, 5]
    assert online_stream_insertion(stream_input) == sorted(stream_input)
    
    # 9. Buggy Implementations Verification
    # Buggy #1 demonstrates stability failure
    unstable_items = [("First", 10), ("Second", 10)]
    insertion_sort_buggy_swap_and_instability(unstable_items)
    assert unstable_items == [("Second", 10), ("First", 10)], "Buggy #1 was expected to invert stability"
    
    # Buggy #2 demonstrates off-by-one boundary failure
    buggy_arr = [5, 2, 4]
    insertion_sort_buggy_off_by_one(buggy_arr)
    assert buggy_arr != [2, 4, 5], "Buggy #2 was expected to fail on smallest element"
    
    print("[+] All Insertion Sort test suites passed successfully!")


# ==============================================================================
# 6. MAIN EXECUTION & VISUAL EDUCATIONAL TRACE
# ==============================================================================

def main() -> None:
    """
    Main driver executing unit tests and rendering an educational execution trace.
    """
    run_tests()
    
    print("\n" + "=" * 78)
    print("EDUCATIONAL VISUAL TRACE: INSERTION SORT STEP-BY-STEP")
    print("=" * 78)
    
    trace_array = [8, 3, 5, 4, 1]
    print(f"Initial Unsorted Array: {trace_array}")
    print("-" * 78)
    print(f"{'Pass':<6} | {'Key':<5} | {'Sorted Subarray':<18} | {'Shift Action':<28} | {'Resulting Array'}")
    print("-" * 78)
    
    arr = trace_array.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        sorted_prefix = str(arr[:i])
        j = i - 1
        shifts = []
        
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            shifts.append(f"Shift {arr[j]}")
            j -= 1
        arr[j + 1] = key
        
        shift_str = ", ".join(shifts) if shifts else "None (Already in place)"
        print(f"{i:<6} | {key:<5} | {sorted_prefix:<18} | {shift_str:<28} | {arr}")
        
    print("-" * 78)
    print(f"Final Sorted Output:   {arr}")
    print("=" * 78)


if __name__ == "__main__":
    main()
