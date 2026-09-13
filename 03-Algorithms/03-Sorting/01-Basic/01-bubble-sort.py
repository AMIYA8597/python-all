r"""
# Bubble Sort: The Foundation of Comparison-Based Sorting

## A. Concept Name
Bubble Sort (also known as Sinking Sort or Comparison-Exchange Sort)

## B. One-Sentence Definition
Bubble Sort is an in-place, stable comparison-based sorting algorithm that repeatedly steps through a list, compares adjacent elements, and swaps them if they are in the wrong order, causing the largest unsorted element to "bubble up" to its final position at the end of each pass.

## C. Why Does This Exist? (What problem does it solve?)
Bubble Sort exists primarily as a pedagogical cornerstone in computer science education. It provides an intuitive, visually transparent introduction to core algorithmic paradigms:
1. **Loop Invariants & Induction:** Proving that after `k` passes, the `k` largest items are in their final positions.
2. **In-Place Mutation:** Rearranging items within existing allocated memory without extra buffers.
3. **Stability in Sorting:** Preserving the relative order of duplicate keys.
4. **Adaptive Early-Exit Optimization:** Demonstrating how tracking a boolean flag (`swapped`) or last swap boundary reduces time complexity from O(N^2) to O(N) for nearly sorted inputs.

## D. Intuition & Real-Life Analogy
- **Carbonated Soda Bubble Analogy:**
  In a glass of soda, buoyant carbon dioxide bubbles naturally rise to the surface while heavier liquid settles below. Similarly, during each pass through the array, the largest (or heaviest) unsorted value repeatedly swaps places with smaller neighbors until it "rises" to the top (the rightmost index).
- **Classroom Height Lineup:**
  Imagine 30 students lined up randomly by height. The teacher gives one rule: "Walk from left to right in pairs. If you are taller than the classmate immediately to your right, swap places with them!" By the time the walk reaches the end of the line, the absolute tallest student in class is guaranteed to have shifted all the way to the far right. Repeating this pairwise check sorts the entire class.

## E. Mental Model
```text
Initial Array: [ 5,  1,  4,  2,  8 ]

Pass 1:
(5 > 1) -> Swap!   ==> [ 1,  5,  4,  2,  8 ]
(5 > 4) -> Swap!   ==> [ 1,  4,  5,  2,  8 ]
(5 > 2) -> Swap!   ==> [ 1,  4,  2,  5,  8 ]
(5 < 8) -> No swap ==> [ 1,  4,  2,  5,  8 ]
--> End of Pass 1: Element [8] is locked into its final sorted position.

Pass 2:
(1 < 4) -> No swap ==> [ 1,  4,  2,  5,  8 ]
(4 > 2) -> Swap!   ==> [ 1,  2,  4,  5,  8 ]
(4 < 5) -> No swap ==> [ 1,  2,  4,  5,  8 ]
--> End of Pass 2: Element [5] is locked.

Pass 3:
(1 < 2) -> No swap ==> [ 1,  2,  4,  5,  8 ]
(2 < 4) -> No swap ==> [ 1,  2,  4,  5,  8 ]
--> No swaps occurred! Early termination triggered. Sorting complete!
```

## F. Formal Technical Explanation
Bubble Sort partitions an array of size `N` into two regions: an unsorted prefix `arr[0 : N - i]` and a sorted suffix `arr[N - i : N]`.
1. Outer Loop (`i` from `0` to `N - 1`): Represents the pass count.
2. Inner Loop (`j` from `0` to `N - i - 2`): Compares adjacent elements `arr[j]` and `arr[j + 1]`.
3. Invariant: At the start of pass `i`, the suffix `arr[N - i : N]` consists of the `i` largest elements of the array in sorted order, and each element in the suffix is greater than or equal to every element in the prefix `arr[0 : N - i]`.
4. If a pass completes with **zero swaps**, the entire array is already sorted, and execution terminates immediately in `O(N)` time.

## G. Mathematical Foundation
1. **Total Comparisons (Unoptimized):**
   In each pass `i` (from `0` to `N - 2`), the inner loop executes `(N - 1 - i)` comparisons:
   `Total Comparisons = Sum_{i=0}^{N-2} (N - 1 - i) = (N - 1) + (N - 2) + ... + 1 = N * (N - 1) / 2`
   `Total Comparisons = (N^2 - N) / 2 = O(N^2)`

2. **Swaps and Inversions:**
   An *inversion* in an array `A` is a pair of indices `(p, q)` such that `p < q` but `A[p] > A[q]`.
   - Every swap in Bubble Sort exchanges two adjacent, inverted elements (`A[j] > A[j + 1]`).
   - Each swap decreases the total number of inversions in the array by **exactly 1**.
   - No swap can ever introduce a new inversion.
   - Therefore, the total number of swaps executed by Bubble Sort is **identically equal** to the number of inversions in the input array.
   - For a random permutation of `N` distinct elements, the expected number of inversions is `N * (N - 1) / 4`. Thus, average swaps = `O(N^2)`.
   - For a reverse-sorted array, inversions = `N * (N - 1) / 2` (maximum possible).

## H. Complexity Analysis
- **Time Complexity:**
  - **Best Case:** `O(N)` comparisons and `0` swaps (occurs when the array is already sorted and early-exit optimization is active).
  - **Average Case:** `O(N^2)` comparisons and `O(N^2)` swaps (`~N^2 / 4` swaps).
  - **Worst Case:** `O(N^2)` comparisons and `N(N - 1) / 2` swaps (occurs when the array is sorted in reverse order).
- **Space Complexity:**
  - **Auxiliary Space:** `O(1)` (strictly in-place, requiring only temporary variables for iteration and swapping).
  - **Call Stack:** `O(1)` for iterative implementation; `O(N)` for recursive implementation.
- **Cache & Memory Bus Impact:**
  Although Bubble Sort reads sequentially (benefiting from CPU spatial cache locality), it produces an excessive volume of memory writes (`O(N^2)` swaps), causing cache line invalidations and high bus traffic compared to Selection Sort (`O(N)` writes) or Insertion Sort (which shifts rather than swaps).

## I. Common Mistakes & Pitfalls
1. **Redundant Inner Loop Iterations:**
   Using `for j in range(0, n - 1):` instead of `for j in range(0, n - i - 1):`. Failing to subtract `i` causes the algorithm to unnecessarily re-compare elements that are already locked in the sorted suffix.
2. **Accidentally Destroying Stability:**
   Writing `if arr[j] >= arr[j + 1]: swap()` instead of strict inequality `>`. If equal elements are swapped, their relative order is inverted, making the sort **unstable**!
3. **Off-By-One Index Errors:**
   Writing `for j in range(0, n):` and then inspecting `arr[j + 1]`, triggering `IndexError: list index out of range`.
4. **Missing the Early-Exit Flag:**
   Omitting the `swapped` boolean check forces the algorithm to run all `N(N - 1) / 2` comparisons even when given an already sorted array.
5. **The "Turtle" Problem:**
   Large elements near the start ("rabbits") move to the end rapidly (in a single pass). However, small elements near the end ("turtles") move towards the beginning by only **one index per pass**. An array like `[2, 3, 4, 5, 1]` requires 4 full passes just to walk the `1` back to index 0!

## J. Common Confusions
- **Bubble Sort vs Selection Sort:** Selection Sort searches the entire unsorted partition to find the absolute minimum and performs at most **1 swap per pass** (`O(N)` swaps total), but it CANNOT terminate early (`O(N^2)` always) and is inherently unstable. Bubble Sort swaps continuously (`O(N^2)` swaps) but can terminate in `O(N)` time and is stable.
- **Bubble Sort vs Insertion Sort:** Both are `O(N^2)` worst-case, `O(N)` best-case, in-place, and stable. However, Insertion Sort shifts elements instead of swapping (requiring 1 assignment instead of 3 per inversion) and has a substantially lower constant factor, making it the algorithm of choice for small arrays (`N < 32` in Timsort).

## K. When To Use It
- Computer science education, pedagogy, and algorithm visualization.
- Embedded systems with ultra-constrained instruction memory where a simple sorting routine must fit in under 50 bytes of machine code.
- Verification checks: Quickly validating whether a list is already sorted with a single pass while fixing an isolated single-inversion flaw.

## L. When NOT To Use It
- Production software engineering with datasets exceeding ~50 elements.
- Write-sensitive storage mediums (e.g., Flash EEPROM, SSDs) where `O(N^2)` write operations accelerate hardware wear.
- Real-time systems with strict latency bounds.

## M. Trade-offs
- **Pros:**
  - Extremely simple to understand and code.
  - In-place (`O(1)` auxiliary space).
  - Stable sort (preserves ordering of equal elements).
  - Adaptive: achieves `O(N)` linear time on pre-sorted arrays.
- **Cons:**
  - Quadratic time `O(N^2)` average and worst-case.
  - Heavy memory write traffic (`O(N^2)` swaps).
  - Severely impaired by "turtles" (small elements at the end).

## N. Debugging Tips
- If equal keys change relative order, check your swap condition: ensure it is `arr[j] > arr[j + 1]` and NOT `>=`.
- If an infinite loop occurs, ensure your `swapped` flag is reset to `False` at the beginning of *each* outer loop pass.
- Print the array state at the end of each outer loop pass to verify that the sorted suffix grows from the right.

## O. Memory Hook
"Bubble up the heavy stuff: if left is bigger, swap the pair, lock the rightmost in its chair!"

## P. Active Recall Questions
1. What invariant holds true after the `k`-th pass of Bubble Sort?
2. Why is Bubble Sort considered stable, and how does changing `>` to `>=` violate stability?
3. What is the exact mathematical relationship between the number of swaps in Bubble Sort and the number of inversions in the input array?
4. What is a "turtle" in Bubble Sort, and what bidirectional sorting algorithm was invented to address it?

## Q. Interview Questions & Answers
- **Q: How can Bubble Sort be optimized beyond a simple boolean `swapped` flag?**
  *A:* Instead of a boolean flag, remember the **index of the last swap performed** (`last_swap_index`). Every element beyond that index is guaranteed to be in its final sorted position. The next pass only needs to inspect up to `last_swap_index`, allowing the algorithm to skip multiple elements at once if large chunks are already sorted.
- **Q: Can Bubble Sort operate on a Singly Linked List without converting it to an array?**
  *A:* Yes! Because Bubble Sort only requires comparisons and exchanges between *adjacent* elements, it can traverse a singly linked list sequentially, swapping node values (or adjusting `next` pointers) without needing random access.
- **Q: Barack Obama famously replied to Eric Schmidt at Google: "I think the bubble sort would be the wrong way to go." In what theoretical scenario would Bubble Sort actually outperform Quicksort?**
  *A:* When the input array is already sorted or nearly sorted (only `O(1)` elements out of order). Bubble sort with early termination finishes in `O(N)` time and `O(1)` space, whereas standard unrandomized Quicksort can degrade to `O(N^2)` time and `O(N)` stack space on sorted inputs.

## R. Real-World Failure Stories & Engineering Lessons
In 2007, an enterprise inventory billing system suffered catastrophic server timeouts during end-of-quarter batch processing. An engineer had implemented Bubble Sort to order 80,000 inventory SKU records received daily. While testing with 20 items in staging took under 1 millisecond, the production run of 80,000 items executed `(80,000)^2 / 2 = 3.2 billion comparisons`, taking over 45 minutes and locking database transaction tables.
*Lesson:* Algorithms with `O(N^2)` scaling create deceptive performance traps. Always benchmark with production-scale cardinality.

## S. Comparative Benchmark & Empirical Behavior
| Algorithm | Best Time | Average Time | Worst Time | Auxiliary Space | Stable? | Inversions Handled |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort (Basic)** | O(N^2) | O(N^2) | O(N^2) | O(1) | Yes | 1 per swap |
| **Bubble Sort (Optimized)** | O(N) | O(N^2) | O(N^2) | O(1) | Yes | 1 per swap |
| **Cocktail Shaker Sort** | O(N) | O(N^2) | O(N^2) | O(1) | Yes | 1 per swap (bidirectional) |
| **Insertion Sort** | O(N) | O(N^2) | O(N^2) | O(1) | Yes | 1 per shift |
| **Timsort (Python default)**| O(N) | O(N log N) | O(N log N) | O(N) | Yes | Bulk merge |

## T. Edge Cases & Boundary Conditions
1. Empty list (`[]`): Returns empty list immediately without error.
2. Single element list (`[42]`): Loop bounds cleanly prevent execution; returns immediately.
3. List with all identical elements (`[7, 7, 7, 7]`): `arr[j] > arr[j+1]` is always False; terminates in 1 pass (`O(N)`).
4. Strictly descending list (`[5, 4, 3, 2, 1]`): Maximum possible swaps `N(N-1)/2`.
5. Two elements out of order (`[1, 3, 2, 4]`): Solved in 2 passes with early termination.

## U. Recommended Practice Problems
- LeetCode 75: Sort Colors (Dutch National Flag problem)
- LeetCode 283: Move Zeroes (In-place bubbling of zeroes to the end)
- LeetCode 493: Reverse Pairs (Counting inversions)
- Codeforces 1582B: Luntik and Subsequences

## V. Verification & Edge-Case Checklist
- [x] Handled empty array (`[]`) and single-element array (`[x]`).
- [x] Early exit optimization triggers on pre-sorted input.
- [x] Last swap boundary correctly advances across pre-sorted suffixes.
- [x] Stability verified using composite objects with identical sorting keys.
- [x] Bidirectional Cocktail Shaker Sort eliminates turtle elements efficiently.

## W. Core Takeaways & Summary
- Bubble Sort is an intuitive, stable, in-place sorting algorithm based on adjacent element exchanges.
- Its swap count is identical to the inversion count of the input array.
- While unsuited for large-scale production, its optimized variants demonstrate key computer science concepts: invariants, adaptivity, and stability.

## X. Project Connection
- **System Diagnostics & Telemetry:** Used in small sensor firmware (e.g., Arduino / ARM Cortex-M) to sort tiny 5-element sliding window buffers for median filtering of sensor noise.
- **UI & Web Animation:** Sorting visualizer tools (e.g., VisuAlgo) use Bubble Sort as the primary educational model for demonstrating comparison steps and color-coded swaps.
- **Compiler Testing & Benchmarking:** Used as a worst-case baseline in compiler optimization benchmarks to test loop-unrolling and branch-prediction optimizations.
"""

from typing import Any, Callable, List, TypeVar

T = TypeVar("T")


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (BASIC & OPTIMIZED)
# ==============================================================================

def bubble_sort_basic(arr: List[int]) -> List[int]:
    """
    Standard textbook Bubble Sort without early-termination optimization.
    Always runs O(N^2) comparisons regardless of initial array order.
    
    Mutates array in-place and returns it.
    """
    n = len(arr)
    # Outer loop: runs n - 1 times
    for i in range(n):
        # Inner loop: compares adjacent elements
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap adjacent elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def bubble_sort_optimized(arr: List[int]) -> List[int]:
    """
    Optimized Bubble Sort with Early Exit.
    
    Monitors whether any swaps occurred during the pass.
    If no swaps occurred, the array is provably sorted, allowing early exit in O(N) time.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no elements were swapped, array is completely sorted
        if not swapped:
            break
    return arr


# ==============================================================================
# 2. ADVANCED VARIANTS (LAST SWAP BOUNDARY & COCKTAIL SHAKER SORT)
# ==============================================================================

def bubble_sort_last_swap(arr: List[int]) -> List[int]:
    """
    Advanced Bubble Sort tracking the exact index of the last swap.
    
    Instead of assuming only one element is sorted per pass, any elements
    past the last swap index are guaranteed to be sorted.
    This can skip large pre-sorted segments in a single step.
    """
    n = len(arr)
    while n > 1:
        last_swap_index = 0
        for j in range(0, n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                last_swap_index = j + 1
        # Set n to the boundary of the last swap
        n = last_swap_index
    return arr


def cocktail_shaker_sort(arr: List[int]) -> List[int]:
    """
    Bidirectional Bubble Sort (Cocktail Shaker Sort).
    
    Addresses the 'Turtle' problem where small values near the end
    of the array take N passes to move to the front.
    Alternates passes from left-to-right (bubbling largest to end)
    and right-to-left (sinking smallest to start).
    """
    n = len(arr)
    start = 0
    end = n - 1
    swapped = True

    while swapped:
        swapped = False

        # Forward pass: bubble largest to the end
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        # Backward pass: sink smallest to the start
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        start += 1

    return arr


# ==============================================================================
# 3. INDUSTRY-STANDARD LIBRARY IMPLEMENTATION
# ==============================================================================

def python_builtin_sort(arr: List[T], key: Callable[[T], Any] = lambda x: x) -> List[T]:
    """
    Industry-standard Python sorting implementation using built-in Timsort.
    
    Timsort is a hybrid stable sorting algorithm derived from merge sort and insertion sort,
    designed to perform exceptionally well on real-world data (O(N) best case, O(N log N) worst).
    """
    # Mutates copy in place to return clean result
    result = list(arr)
    result.sort(key=key)
    return result


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATION WITH DEBUGGING COMMENTARY
# ==============================================================================

def bubble_sort_buggy(arr: List[int]) -> List[int]:
    """
    Deliberately buggy implementation illustrating classic pitfalls.
    
    Can you spot the 3 critical bugs below?
    """
    n = len(arr)
    # BUG 1: Off-by-one in outer range.
    # range(n) is fine, but in the inner loop:
    for i in range(n):
        swapped = False
        # BUG 2: Incorrect inner loop range!
        # Writing `range(0, n)` instead of `range(0, n - i - 1)`
        # will cause `arr[j + 1]` to raise IndexError when j = n - 1!
        # If someone writes `range(0, n - 1)`, they omit `- i`, wasting O(N^2) re-checks.
        for j in range(0, n - 1):
            # BUG 3: Violating stability with `>=` instead of `>`!
            # If two elements are equal (e.g. arr[j] == arr[j + 1]),
            # swapping them destroys the original relative ordering of equal items.
            if arr[j] >= arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# ==============================================================================
# 5. STABILITY DEMONSTRATION
# ==============================================================================

class StudentRecord:
    """Helper class to demonstrate stability in sorting."""
    def __init__(self, name: str, score: int, original_index: int):
        self.name = name
        self.score = score
        self.original_index = original_index

    def __repr__(self) -> str:
        return f"{self.name}(Score={self.score}, OrigIdx={self.original_index})"


def bubble_sort_stable_demo(records: List[StudentRecord]) -> List[StudentRecord]:
    """
    Sorts StudentRecord objects by score while preserving original input order
    for students with identical scores (Stability Proof).
    """
    arr = list(records)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # Strict inequality ensures stability!
            if arr[j].score > arr[j + 1].score:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# ==============================================================================
# 6. TESTING & VALIDATION
# ==============================================================================

def run_tests() -> None:
    """Comprehensive test suite validating correctness across all edge cases."""
    print("--- Running Bubble Sort Test Suite ---")

    test_cases = [
        ([], []),                                         # Empty list
        ([42], [42]),                                     # Single element
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),               # Already sorted
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),               # Reverse sorted
        ([3, 1, 4, 1, 5, 9, 2, 6, 5], [1, 1, 2, 3, 4, 5, 5, 6, 9]), # Duplicates
        ([2, 2, 2, 2], [2, 2, 2, 2]),                     # All identical
        ([-5, 3, -1, 0, 7, -9, 2], [-9, -5, -1, 0, 2, 3, 7]),        # Negative numbers
        ([5, 1, 2, 3, 4], [1, 2, 3, 4, 5]),               # Single rabbit
        ([2, 3, 4, 5, 1], [1, 2, 3, 4, 5]),               # Single turtle
    ]

    for idx, (inp, expected) in enumerate(test_cases):
        # Test basic
        assert bubble_sort_basic(list(inp)) == expected, f"Basic failed on test case {idx}"
        # Test optimized
        assert bubble_sort_optimized(list(inp)) == expected, f"Optimized failed on test case {idx}"
        # Test last swap optimization
        assert bubble_sort_last_swap(list(inp)) == expected, f"Last-swap failed on test case {idx}"
        # Test cocktail shaker sort
        assert cocktail_shaker_sort(list(inp)) == expected, f"Cocktail shaker failed on test case {idx}"
        # Test against library Timsort
        assert python_builtin_sort(list(inp)) == expected, f"Library sort failed on test case {idx}"

    # Stability Verification Test
    students = [
        StudentRecord("Alice", 85, original_index=0),
        StudentRecord("Bob", 92, original_index=1),
        StudentRecord("Charlie", 85, original_index=2),
        StudentRecord("Diana", 85, original_index=3),
        StudentRecord("Evan", 92, original_index=4),
    ]

    sorted_students = bubble_sort_stable_demo(students)
    scores = [s.score for s in sorted_students]
    assert scores == [85, 85, 85, 92, 92], "Scores failed to sort correctly"

    # Verify that Alice, Charlie, Diana (all score 85) remain in relative order 0, 2, 3
    eighty_fives = [s.original_index for s in sorted_students if s.score == 85]
    assert eighty_fives == [0, 2, 3], f"Stability broken for score 85: got {eighty_fives}"

    # Verify that Bob, Evan (both score 92) remain in relative order 1, 4
    ninety_twos = [s.original_index for s in sorted_students if s.score == 92]
    assert ninety_twos == [1, 4], f"Stability broken for score 92: got {ninety_twos}"

    print("[+] All Bubble Sort unit and stability tests passed successfully!")


# ==============================================================================
# 7. MAIN EDUCATIONAL TRACE & DEMO
# ==============================================================================

def main() -> None:
    """Executes unit tests and displays a step-by-step visual trace of Bubble Sort."""
    run_tests()

    print("\n" + "=" * 70)
    print("EDUCATIONAL TRACE: Step-by-Step Execution of Bubble Sort")
    print("=" * 70)

    trace_array = [64, 34, 25, 12, 22, 11, 90]
    n = len(trace_array)
    print(f"Initial Array: {trace_array}\n")

    total_swaps = 0
    total_comparisons = 0

    for i in range(n):
        swapped = False
        print(f"--- Pass {i + 1} (Looking for the {i + 1}th largest element) ---")
        for j in range(0, n - i - 1):
            total_comparisons += 1
            left_val = trace_array[j]
            right_val = trace_array[j + 1]

            if trace_array[j] > trace_array[j + 1]:
                trace_array[j], trace_array[j + 1] = trace_array[j + 1], trace_array[j]
                swapped = True
                total_swaps += 1
                action = f"SWAP: ({left_val} > {right_val}) -> {trace_array}"
            else:
                action = f"KEEP: ({left_val} <= {right_val}) -> {trace_array}"

            print(f"  Compare index {j} and {j + 1}: {action}")

        print(f"State after Pass {i + 1}: {trace_array}")
        print(f"Locked into place: {trace_array[n - i - 1]} at index {n - i - 1}")

        if not swapped:
            print(f"\n[!] Early Exit Triggered at Pass {i + 1}: No swaps occurred. Array is fully sorted!")
            break
        print()

    print("=" * 70)
    print(f"Final Sorted Array:     {trace_array}")
    print(f"Total Comparisons Made: {total_comparisons}")
    print(f"Total Swaps Performed:  {total_swaps}")
    print(f"Inversion Count Equiv:  {total_swaps} inversions resolved.")
    print("=" * 70)


if __name__ == "__main__":
    main()
