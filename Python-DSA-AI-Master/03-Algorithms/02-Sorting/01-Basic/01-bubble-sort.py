r"""
# Bubble Sort (Exchange Sort): Comprehensive Pedagogical Reference

## A. Concept Name
Bubble Sort (also historically known as Sinking Sort, Exchange Sort, or Adjacent Comparison Sort).

## B. One-Sentence Definition
Bubble Sort is an elementary comparison-based sorting algorithm that repeatedly steps through a linear sequence, compares adjacent element pairs, and swaps them if they violate the desired order, iteratively propagating ("bubbling") the extremum of the unsorted segment to its final position.

## C. Why Does This Exist? (What problem does it solve?)
1. **The Fundamental Ordering Problem**: In computing, unsorted data requires $O(N)$ time for linear search. Sorting transforms data into an ordered sequence, enabling $O(\log N)$ binary search, $O(1)$ extremum retrieval, efficient deduplication, and divide-and-conquer processing.
2. **Pedagogical Invariant Grounding**: Bubble Sort is computer science's premier pedagogical vehicle for teaching nested loop mechanics, loop invariants, state flags, and algorithmic time complexity.
3. **Adaptive Early Termination**: Unlike naive algorithms that run for a fixed number of cycles, Bubble Sort naturally detects whether an array is already sorted in a single pass ($O(N)$ best-case verification).
4. **Locality of Reference in Constrained Hardware**: Bubble Sort relies exclusively on *adjacent* swaps ($j$ and $j+1$). In sequential storage devices (e.g., magnetic tape reels, delay-line memories, or systolic hardware arrays), swapping distant elements incurs prohibitive physical seek latency; adjacent exchanges can be executed in-place with zero random-access overhead.

## D. Intuition & Real-Life Analogy
- **Carbonated Soda Bubbles**: When a carbonated drink is poured into a glass, gas bubbles rise toward the surface because they are lighter (less dense) than the surrounding liquid. In Bubble Sort, larger (or "heavier") values sink to the bottom (the high-index end of the array), while smaller ("lighter") elements bubble up to the front.
- **Physical Lineup by Height**: Imagine an elementary school classroom lining up by height. The teacher asks students to compare themselves only to the peer directly to their right. If student $A$ is taller than student $B$, they switch spots. As the teacher walks down the line from front to back, the absolute tallest student in the room inevitably gets dragged along until reaching the very end of the line. Repeating this process $N-1$ times ensures everyone is sorted.

## E. Mental Model
Visualize an array of size $N$ partitioned into two dynamic zones:
1. An **Unsorted Prefix**: Initially spanning indices $[0 \dots N - 1]$, shrinking by one element from the right with each completed outer pass.
2. A **Sorted Suffix**: Initially empty, growing from right to left as $[N - i \dots N - 1]$ after pass $i$.

```text
Pass 0: [ 5, 1, 4, 2, 8 ]  -> Compare (5,1)->swap, (5,4)->swap, (5,2)->swap, (5,8)->ok
Result: [ 1, 4, 2, 5 | 8 ] (8 is finalized in sorted suffix)

Pass 1: [ 1, 4, 2, 5 | 8 ]  -> Compare (1,4)->ok, (4,2)->swap, (4,5)->ok
Result: [ 1, 2, 4 | 5, 8 ] (5 and 8 finalized)

Pass 2: [ 1, 2, 4 | 5, 8 ]  -> Compare (1,2)->ok, (2,4)->ok
Result: [ 1, 2 | 4, 5, 8 ] (No swaps occurred! Early exit triggered.)
Final:  [ 1, 2, 4, 5, 8 ]
```

During each pass, an active "bubble cursor" slides across the unsorted prefix. Whichever element is currently largest is carried along on the cursor like an escalator passenger until it encounters an even larger element or reaches the boundary of the sorted suffix.

## F. Formal Technical Explanation
Formally, let $A = [a_0, a_1, \dots, a_{N-1}]$ be a sequence of elements drawn from a totally ordered set $(S, \le)$.
Bubble Sort establishes the following loop invariant:

> **Outer Loop Invariant**: At the start of pass $i$ (where $0 \le i < N$), the sub-array $A[N-i \dots N-1]$ contains the $i$ largest elements of the original collection in strictly sorted order, and every element in the unsorted prefix $A[0 \dots N-1-i]$ is less than or equal to every element in the sorted suffix:
> $$\max_{0 \le k \le N-1-i} A[k] \le \min_{N-i \le m < N} A[m]$$

The inner loop executes adjacent comparisons:
$$\forall j \in [0, N - 2 - i]: \quad \text{if } A[j] > A[j+1] \implies \text{swap}(A[j], A[j+1])$$

Because swaps occur **only** when $A[j] > A[j+1]$ (strict inequality), equal elements preserve their relative initial order. Therefore, standard Bubble Sort is a **stable** sorting algorithm.

## G. Mathematical Foundation
1. **Inversions and Swap Equivalence**:
   - An **inversion** in an array $A$ is a pair of indices $(p, q)$ such that $p < q$ and $A[p] > A[q]$.
   - An adjacent swap between $A[j]$ and $A[j+1]$ changes the relative order of *only* that specific pair. If $A[j] > A[j+1]$, swapping them reduces the total inversion count of the entire array by **exactly 1**.
   - Therefore, the number of swaps performed by Bubble Sort is identically equal to the number of inversions in the input array:
     $$\text{Swaps}(A) = I(A) = \sum_{p < q} \mathbf{1}_{\{A[p] > A[q]\}}$$

2. **Comparison Count Analysis**:
   - Without early termination, the number of comparisons is fixed:
     $$C(N) = \sum_{i=0}^{N-2} (N - 1 - i) = \sum_{k=1}^{N-1} k = \frac{(N - 1)N}{2} = \frac{N^2 - N}{2} \in \Theta(N^2)$$
   - With the boolean `swapped` flag optimization:
     - Best-case (already sorted array): $C_{\text{best}}(N) = N - 1 \in \Theta(N)$.
     - Worst-case (reverse sorted array): $C_{\text{worst}}(N) = \frac{N(N-1)}{2} \in \Theta(N^2)$.

3. **Average Inversion Expectation**:
   - For a random permutation of $N$ distinct keys, the probability that any given pair $(p, q)$ is inverted is $\frac{1}{2}$.
   - By linearity of expectation, the expected number of inversions is:
     $$\mathbb{E}[I(A)] = \sum_{1 \le p < q \le N} \mathbb{P}(A[p] > A[q]) = \binom{N}{2} \times \frac{1}{2} = \frac{N(N - 1)}{4}$$
   - Thus, Bubble Sort requires an average of $\frac{N(N-1)}{4}$ swaps, cementing its $\Theta(N^2)$ average time complexity.

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - **Best Case**: $O(N)$ comparisons, $0$ swaps. Occurs when the input array is already completely sorted; the first pass executes $N-1$ comparisons, records zero swaps, and breaks out immediately.
  - **Average Case**: $\Theta(N^2)$ comparisons and $\Theta(N^2)$ swaps ($\approx \frac{N^2}{2}$ comparisons, $\approx \frac{N^2}{4}$ swaps).
  - **Worst Case**: $\Theta(N^2)$ comparisons and $\Theta(N^2)$ swaps ($\frac{N(N-1)}{2}$ comparisons and swaps). Occurs when the array is in reverse sorted order.
- **Space Complexity**:
  - **Auxiliary Space**: $O(1)$ auxiliary space for iterative implementation. Only scalar variables (`i`, `j`, `swapped`, `temp`) are allocated on the call stack.
  - **Recursive Bubble Sort Space**: $O(N)$ auxiliary stack frames due to recursion depth.
- **Cache & Memory Bus Impact**:
  - **Spatial Locality**: Excellent read locality. The inner loop scans contiguous memory sequentially ($A[j]$ and $A[j+1]$ reside in the same CPU cache line).
  - **Write Amplification**: Horrible write profile. Because every inversion triggers two memory writes, Bubble Sort generates up to $N(N-1)$ store instructions. On SSDs, Flash, or non-volatile RAM, this causes severe wear.

## I. Common Mistakes & Pitfalls
1. **Inefficient Inner Loop Upper Bound**:
   - *Bug*: Looping `for j in range(n - 1)` instead of `for j in range(n - 1 - i)`.
   - *Consequence*: Redundantly re-checking elements in the sorted suffix, doubling total comparison overhead while keeping the asymptotic class $O(N^2)$.
2. **Missing the Early Exit Optimization**:
   - *Bug*: Omitting the `swapped` boolean flag.
   - *Consequence*: Forces $O(N^2)$ runtime even when given an already sorted array, destroying the algorithm's unique adaptive advantage.
3. **Index-Out-of-Bounds Error**:
   - *Bug*: Writing `for j in range(n - i): if arr[j] > arr[j+1]:`
   - *Consequence*: When $j = n - 1 - i$ and $i = 0$, $j+1 = n$, causing an `IndexError: list index out of range`.
4. **Breaking Stability via Non-Strict Inequality**:
   - *Bug*: Swapping when `arr[j] >= arr[j+1]`.
   - *Consequence*: Equal elements swap places, destroying the relative order of identical keys and rendering the sort unstable.
5. **The "Turtles and Rabbits" Asymmetry**:
   - Large values ("rabbits") move toward the right very rapidly (one step per swap, traveling across the entire array in a single pass).
   - Small values ("turtles") situated near the end of the array move toward the left agonizingly slowly (only one index per outer pass!). A single turtle at index $N-1$ forces $N-1$ full outer passes even if the rest of the array is perfectly sorted.

## J. Common Confusions
- **Bubble Sort vs. Selection Sort**:
  - Bubble Sort does many swaps per pass ($O(N^2)$ total) but stops early if sorted ($O(N)$ best case).
  - Selection Sort does at most ONE swap per pass ($O(N)$ total writes) but always does $\Theta(N^2)$ comparisons regardless of initial ordering.
  - Bubble Sort is stable; Selection Sort is inherently unstable.
- **Bubble Sort vs. Insertion Sort**:
  - Both have $O(N)$ best case and $O(N^2)$ worst case.
  - Insertion Sort scans backward into a sorted prefix, shifting elements rather than swapping them (1 assignment vs 3 assignments per swap), typically executing $2\times$ to $3\times$ faster in practical wall-clock time.
- **Swapping vs. Shifting**:
  - A swap `a, b = b, a` requires reading and writing both locations (3 pointer moves in C).
  - Shifting `arr[j+1] = arr[j]` requires only a single write, which is why Insertion Sort dominates Bubble Sort in practice.

## K. When To Use It
- **Teaching and Education**: When introducing recursion, loop invariants, stability, and algorithmic performance trade-offs.
- **Verification of Nearly Sorted Arrays**: When data is known in advance to have at most $k \ll N$ out-of-order elements at the high end.
- **Hardware-Constrained Systolic Arrays**: In custom FPGA or ASIC pipelines where processing elements can only exchange messages with immediately adjacent registers.

## L. When NOT To Use It
- **Production Sorting**: Never use Bubble Sort in production for general datasets ($N > 30$). Use standard library routines like Python's `list.sort()` (Timsort) which runs in $O(N \log N)$ worst-case and $O(N)$ best-case.
- **Write-Sensitive Media**: On EEPROM, Flash memory, or cloud block storage where write amplification incurs financial cost or hardware wear.
- **Large Datasets**: For $N = 100,000$, Bubble Sort requires $\approx 5 \times 10^9$ operations (several seconds to minutes in Python), whereas an $O(N \log N)$ sort completes in a few milliseconds.

## M. Trade-offs
| Attribute | Bubble Sort | Insertion Sort | Selection Sort | QuickSort | Merge Sort |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Best Time** | $O(N)$ | $O(N)$ | $\Theta(N^2)$ | $O(N \log N)$ | $O(N \log N)$ |
| **Average Time** | $O(N^2)$ | $O(N^2)$ | $\Theta(N^2)$ | $O(N \log N)$ | $O(N \log N)$ |
| **Worst Time** | $O(N^2)$ | $O(N^2)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(N \log N)$ |
| **Auxiliary Space** | $O(1)$ | $O(1)$ | $O(1)$ | $O(\log N)$ | $O(N)$ |
| **Stable?** | Yes | Yes | No | No | Yes |
| **Max Swaps/Writes**| $O(N^2)$ | $O(N^2)$ shifts | $O(N)$ swaps | $O(N \log N)$ | $O(N \log N)$ |
| **Adaptive?** | Yes ($O(N)$) | Yes ($O(N)$) | No | No | Partially |

## N. Debugging Tips
1. **Instrument Comparisons and Swaps**: Always maintain separate integer counters for `comparisons` and `swaps`. In a sorted array, swaps must equal 0 and comparisons must equal $N-1$.
2. **Track the Unsorted Boundary**: Print the array after each pass formatted with a visual vertical pipe `|` separating the unsorted prefix from the sorted suffix.
3. **Verify the Invariant with Assertions**: Inside your test loops, assert that the suffix slice `arr[n - i:]` is identical to `sorted(arr[n - i:])` after each iteration $i$.

## O. Memory Hook
**"Bubbles Rise, Turtles Crawl:
Compare your neighbor, swap if tall!
If a pass has swaps of zero,
Early exit is your hero!"**

## P. Active Recall Questions
1. Why does an adjacent swap reduce the inversion count of an array by exactly 1, whereas a non-adjacent swap can reduce it by more?
2. What is a "turtle" in Bubble Sort terminology, and why does Cocktail Shaker Sort fix it?
3. If an array of size $N$ requires 0 swaps during the first pass, what is the exact number of comparisons performed?
4. How does replacing `if arr[j] > arr[j+1]:` with `if arr[j] >= arr[j+1]:` compromise stability?
5. Prove why the inner loop can safely terminate at index $N - 1 - i$ instead of $N - 2$.

## Q. Interview Questions & Answers
- **Q1: What is the exact relationship between Bubble Sort swaps and array inversions?**
  *Answer*: Each swap in Bubble Sort exchanges two strictly adjacent elements $A[j]$ and $A[j+1]$. Because no elements between indices $j$ and $j+1$ are affected, the relative order of all other pairs in the array remains strictly unchanged. If $A[j] > A[j+1]$, swapping them inverts that single pair from out-of-order to in-order, decrementing the global inversion count by exactly 1. Hence, the total number of swaps executed by Bubble Sort is identical to the number of inversions in the input array.

- **Q2: Why is Bubble Sort considered an "adaptive" algorithm, and how does that affect its Big O notation?**
  *Answer*: An algorithm is adaptive if its execution time improves when the input possesses existing order. With the standard `swapped` boolean flag, Bubble Sort monitors whether any exchange occurs during an entire scan of the unsorted segment. If the array is already sorted, the flag remains `False` after the first pass ($N-1$ comparisons, 0 swaps), and the algorithm terminates immediately. Thus, while its worst-case is $O(N^2)$, its best-case bound is adaptively $O(N)$ or $\Omega(N)$.

- **Q3: What is Cocktail Shaker Sort (Bidirectional Bubble Sort), and what specific problem does it resolve?**
  *Answer*: In standard Bubble Sort, large values ("rabbits") move rapidly to the right, but small values located near the end ("turtles") advance leftward by only one position per outer pass. For example, in $[2, 3, 4, 5, 1]$, the number $1$ is a turtle requiring 4 full passes. Cocktail Shaker Sort traverses alternately from left-to-right (bubbling the maximum) and from right-to-left (sinking the minimum), allowing turtles to traverse the entire array in a single reverse pass.

- **Q4: Can Bubble Sort be implemented recursively? What are the implications for complexity?**
  *Answer*: Yes. A recursive Bubble Sort replaces the outer loop with a recursive function call: pass 1 bubbles the maximum element to the end of array size $N$, then the function recursively invokes itself on the prefix of size $N-1$. While the time complexity remains $O(N^2)$ worst-case and $O(N)$ best-case, the auxiliary space increases from $O(1)$ to $O(N)$ due to call stack frames, risking a `RecursionError` on large arrays.

## R. Project Connections
- **CPython Sorting**: CPython’s built-in `list.sort()` uses **Timsort** (created by Tim Peters in 2002). Timsort detects natural monotonic runs and uses Insertion Sort for small blocks ($N \le 32$ or $64$), never Bubble Sort, because Insertion Sort requires significantly fewer memory operations.
- **Graphics Pipeline Sorting**: In early 3D rendering engines without depth buffers (Z-buffers), the Painter's Algorithm sorted polygon faces by depth from back to front. When polygon positions only changed slightly between video frames (high temporal coherence), an adaptive Bubble Sort pass could restore order in near $O(N)$ time.
- **Hardware Sorting Networks**: Batcher's Odd-Even Mergesort and systolic sorting arrays are physical electronic implementations inspired by adjacent comparison-exchange primitives.

## S. Edge Cases & Boundary Conditions
1. **Empty Array (`[]`)**: Should return `[]` immediately without errors.
2. **Single Element (`[42]`)**: Should return `[42]` after 0 passes.
3. **Two Elements (`[2, 1]` and `[1, 2]`)**: Verifies minimum swap and non-swap behavior.
4. **Already Sorted (`[1, 2, 3, 4, 5]`)**: Must complete in 1 pass ($N-1$ comparisons, 0 swaps).
5. **Reverse Sorted (`[5, 4, 3, 2, 1]`)**: Must perform exactly $\frac{N(N-1)}{2}$ comparisons and swaps.
6. **All Identical Elements (`[7, 7, 7, 7]`)**: Must trigger early exit in 1 pass without performing any swaps.
7. **Negative Numbers and Floats (`[-3.5, 0.0, -10.2, 4.8]`)**: Must handle arbitrary comparable types correctly.
8. **Duplicate Elements with Custom Keys**: Must preserve the initial relative sequence of duplicate keys (stability test).

## T. Algorithmic Variants & Optimizations
1. **Standard Optimized Bubble Sort**: Uses a `swapped` boolean flag to break early if no swaps occurred.
2. **Last-Swap Position Optimization**: Instead of decrementing the unsorted boundary by 1 each pass, track the index of the *last swap performed*. All elements past that index are guaranteed to be sorted, allowing the boundary to jump multiple positions when suffixes are already ordered.
3. **Cocktail Shaker Sort (Bidirectional Bubble Sort)**: Scans left-to-right to bubble the maximum, then right-to-left to sink the minimum, mitigating the "turtle" problem.
4. **Recursive Bubble Sort**: Demonstrates structural recursion over sequence prefixes.

## U. Comparative Analysis / Comparison Table
```text
+-----------------------+------------+------------+------------+-----------+---------+-------------------+
| Algorithm             | Best Time  | Avg Time   | Worst Time | Space     | Stable? | Swaps / Writes    |
+-----------------------+------------+------------+------------+-----------+---------+-------------------+
| Bubble Sort (Optim.)  | O(N)       | O(N^2)     | O(N^2)     | O(1)      | Yes     | O(N^2) swaps      |
| Cocktail Shaker Sort  | O(N)       | O(N^2)     | O(N^2)     | O(1)      | Yes     | O(N^2) swaps      |
| Selection Sort        | Theta(N^2) | Theta(N^2) | Theta(N^2) | O(1)      | No      | O(N) swaps        |
| Insertion Sort        | O(N)       | O(N^2)     | O(N^2)     | O(1)      | Yes     | O(N^2) shifts     |
| Merge Sort            | O(N log N) | O(N log N) | O(N log N) | O(N)      | Yes     | O(N log N) writes |
| QuickSort (Randomized)| O(N log N) | O(N log N) | O(N^2)     | O(log N)  | No      | O(N log N) swaps  |
| Timsort (Python std)  | O(N)       | O(N log N) | O(N log N) | O(N)      | Yes     | O(N log N) writes |
+-----------------------+------------+------------+------------+-----------+---------+-------------------+
```

## V. Practice Exercises & Solutions
- **Exercise 1**: Implement an inversion counter using Bubble Sort and verify that the count matches the number of adjacent swaps.
- **Exercise 2**: Implement the "Last-Swap Optimization" where the inner loop bound jumps to the last recorded swap position.
- **Exercise 3**: Write a test verifying that Bubble Sort preserves the relative ordering of objects with identical primary sort keys.

## W. Step-by-Step Execution Trace
Tracing `arr = [64, 34, 25, 12, 22, 11, 90]`, length $N = 7$:

```text
Initial Array: [64, 34, 25, 12, 22, 11, 90]

--- PASS 0 (Limit index: 5) ---
Compare (64, 34) -> Swap!  -> [34, 64, 25, 12, 22, 11, 90]
Compare (64, 25) -> Swap!  -> [34, 25, 64, 12, 22, 11, 90]
Compare (64, 12) -> Swap!  -> [34, 25, 12, 64, 22, 11, 90]
Compare (64, 22) -> Swap!  -> [34, 25, 12, 22, 64, 11, 90]
Compare (64, 11) -> Swap!  -> [34, 25, 12, 22, 11, 64, 90]
Compare (64, 90) -> OK     -> [34, 25, 12, 22, 11, 64, 90]
End of Pass 0: Suffix [90] finalized. Swaps this pass: 5

--- PASS 1 (Limit index: 4) ---
Compare (34, 25) -> Swap!  -> [25, 34, 12, 22, 11, 64, 90]
Compare (34, 12) -> Swap!  -> [25, 12, 34, 22, 11, 64, 90]
Compare (34, 22) -> Swap!  -> [25, 12, 22, 34, 11, 64, 90]
Compare (34, 11) -> Swap!  -> [25, 12, 22, 11, 34, 64, 90]
Compare (34, 64) -> OK     -> [25, 12, 22, 11, 34, 64, 90]
End of Pass 1: Suffix [64, 90] finalized. Swaps this pass: 4

--- PASS 2 (Limit index: 3) ---
Compare (25, 12) -> Swap!  -> [12, 25, 22, 11, 34, 64, 90]
Compare (25, 22) -> Swap!  -> [12, 22, 25, 11, 34, 64, 90]
Compare (25, 11) -> Swap!  -> [12, 22, 11, 25, 34, 64, 90]
Compare (25, 34) -> OK     -> [12, 22, 11, 25, 34, 64, 90]
End of Pass 2: Suffix [34, 64, 90] finalized. Swaps this pass: 3

--- PASS 3 (Limit index: 2) ---
Compare (12, 22) -> OK     -> [12, 22, 11, 25, 34, 64, 90]
Compare (22, 11) -> Swap!  -> [12, 11, 22, 25, 34, 64, 90]
Compare (22, 25) -> OK     -> [12, 11, 22, 25, 34, 64, 90]
End of Pass 3: Suffix [25, 34, 64, 90] finalized. Swaps this pass: 1

--- PASS 4 (Limit index: 1) ---
Compare (12, 11) -> Swap!  -> [11, 12, 22, 25, 34, 64, 90]
Compare (12, 22) -> OK     -> [11, 12, 22, 25, 34, 64, 90]
End of Pass 4: Suffix [22, 25, 34, 64, 90] finalized. Swaps this pass: 1

--- PASS 5 (Limit index: 0) ---
Compare (11, 12) -> OK     -> [11, 12, 22, 25, 34, 64, 90]
End of Pass 5: Swaps this pass: 0 -> EARLY TERMINATION TRIGGERED!

Total Passes: 6 (Saved 1 pass out of 7)
Total Comparisons: 5 + 4 + 3 + 2 + 1 + 0 = 15
Total Swaps: 5 + 4 + 3 + 1 + 1 + 0 = 14 (Identical to initial inversion count)
Sorted Array: [11, 12, 22, 25, 34, 64, 90]
```

## X. Key Takeaways & Summary Anchor
- **Core Action**: Repeatedly compare adjacent pairs and swap them if out of order.
- **Loop Invariant**: After pass $i$, the last $i$ elements are in their permanent, sorted positions.
- **Swaps Equal Inversions**: Bubble Sort swap count is an exact measure of disorder (inversions).
- **Adaptivity**: With the `swapped` flag, already sorted arrays complete in $O(N)$ time.
- **Production Truth**: Never deploy Bubble Sort in production; use Timsort (`list.sort()`), but master Bubble Sort to deeply understand loop bounds, stability, and invariant reasoning.
"""

from __future__ import annotations
import copy
import dataclasses
from typing import Any, Callable, Generic, List, Optional, Protocol, Sequence, Tuple, TypeVar

# ==============================================================================
# 1. PROTOCOLS AND METRICS DATA STRUCTURES
# ==============================================================================

class Comparable(Protocol):
    """Protocol for elements supporting strict ordering."""
    def __lt__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...


T = TypeVar("T", bound=Comparable)


@dataclasses.dataclass
class SortMetrics:
    """Telemetry data collected during sorting execution."""
    comparisons: int = 0
    swaps: int = 0
    passes_executed: int = 0
    early_termination: bool = False

    def reset(self) -> None:
        """Reset all metric counters to zero."""
        self.comparisons = 0
        self.swaps = 0
        self.passes_executed = 0
        self.early_termination = False

    def __str__(self) -> str:
        return (
            f"Metrics(comparisons={self.comparisons}, swaps={self.swaps}, "
            f"passes={self.passes_executed}, early_exit={self.early_termination})"
        )


# ==============================================================================
# 2. FROM-SCRATCH EDUCATIONAL IMPLEMENTATIONS
# ==============================================================================

def bubble_sort(arr: List[T], metrics: Optional[SortMetrics] = None) -> List[T]:
    """
    Standard in-place optimized Bubble Sort with early exit flag.
    
    Time Complexity:
        - Best: O(N) when already sorted.
        - Average: O(N^2)
        - Worst: O(N^2) when reverse sorted.
    Space Complexity:
        - Auxiliary: O(1) in-place.
        
    Args:
        arr: The list of comparable items to be sorted in-place.
        metrics: Optional SortMetrics object to record comparisons and swaps.
        
    Returns:
        The sorted list (same reference as input).
    """
    n = len(arr)
    if n <= 1:
        if metrics:
            metrics.passes_executed = 0
        return arr

    if metrics is None:
        metrics = SortMetrics()

    for i in range(n - 1):
        metrics.passes_executed += 1
        swapped = False
        
        # Inner loop compares adjacent elements up to the unsorted boundary
        for j in range(0, n - 1 - i):
            metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                metrics.swaps += 1
                swapped = True
                
        # If no two elements were swapped in this pass, the array is strictly sorted
        if not swapped:
            metrics.early_termination = True
            break

    return arr


def bubble_sort_last_swap_optimized(arr: List[T], metrics: Optional[SortMetrics] = None) -> List[T]:
    """
    Optimized Bubble Sort using the last-swap position technique.
    
    Rather than decrementing the outer loop boundary by 1 each time,
    this variant sets the new boundary to the index of the LAST swap.
    Any elements past that index are mathematically proven to be in sorted order.
    
    Args:
        arr: The list of comparable items to be sorted in-place.
        metrics: Optional SortMetrics object.
        
    Returns:
        The sorted list.
    """
    n = len(arr)
    if n <= 1:
        return arr

    if metrics is None:
        metrics = SortMetrics()

    limit = n - 1
    while limit > 0:
        metrics.passes_executed += 1
        last_swap_idx = 0
        for j in range(limit):
            metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                metrics.swaps += 1
                last_swap_idx = j
                
        if last_swap_idx == 0:
            metrics.early_termination = True
            break
        limit = last_swap_idx

    return arr


def cocktail_shaker_sort(arr: List[T], metrics: Optional[SortMetrics] = None) -> List[T]:
    """
    Cocktail Shaker Sort (Bidirectional Bubble Sort).
    
    Alternates passes from left-to-right (bubbling the maximum to the high end)
    and right-to-left (sinking the minimum to the low end). This resolves the
    "turtle" problem where small elements near the end take many passes to travel left.
    
    Args:
        arr: The list of comparable items to be sorted in-place.
        metrics: Optional SortMetrics object.
        
    Returns:
        The sorted list.
    """
    n = len(arr)
    if n <= 1:
        return arr

    if metrics is None:
        metrics = SortMetrics()

    start = 0
    end = n - 1
    swapped = True

    while swapped and start < end:
        swapped = False
        metrics.passes_executed += 1

        # Forward pass: bubble largest element to the right
        for j in range(start, end):
            metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                metrics.swaps += 1
                swapped = True

        end -= 1
        if not swapped:
            metrics.early_termination = True
            break

        swapped = False
        metrics.passes_executed += 1

        # Backward pass: sink smallest element to the left
        for j in range(end - 1, start - 1, -1):
            metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                metrics.swaps += 1
                swapped = True

        start += 1
        if not swapped:
            metrics.early_termination = True
            break

    return arr


def bubble_sort_recursive(arr: List[T], n: Optional[int] = None) -> List[T]:
    """
    Recursive formulation of Bubble Sort.
    
    Recursion Base Case:
        When n == 1, an array of size 1 is trivially sorted.
    Recursive Step:
        Perform one complete pass of adjacent swaps over arr[0 ... n-1],
        guaranteeing arr[n-1] is the maximum element.
        Then recursively call bubble_sort_recursive(arr, n - 1).
        
    Space Complexity:
        O(N) auxiliary call stack frames.
    """
    if n is None:
        n = len(arr)

    if n <= 1:
        return arr

    # One pass of bubble sort over arr[0 ... n-1]
    swapped = False
    for j in range(n - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            swapped = True

    # If no elements were swapped, entire array is already sorted
    if not swapped:
        return arr

    # Recurse on prefix of size n - 1
    return bubble_sort_recursive(arr, n - 1)


def bubble_sort_pure(sequence: Sequence[T]) -> List[T]:
    """
    Pure, non-mutating functional Bubble Sort returning a new list.
    Preserves immutability of input data structures.
    """
    cloned = list(sequence)
    return bubble_sort(cloned)


# ==============================================================================
# 3. INDUSTRY-STANDARD LIBRARY IMPLEMENTATION
# ==============================================================================

def production_sort(sequence: Sequence[T], reverse: bool = False) -> List[T]:
    """
    Industry-standard sorting using Python's built-in Timsort algorithm.
    
    Timsort is an adaptive, stable, natural merge sort with O(N log N) worst-case
    and O(N) best-case time complexity, engineered by Tim Peters.
    In real-world software, developers must always use built-in sort routines
    rather than hand-rolled Bubble Sort.
    """
    # sorted() creates a new sorted list using CPython's highly optimized C implementation
    return sorted(sequence, reverse=reverse)


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DIAGNOSTIC COMMENTARY
# ==============================================================================

def buggy_bubble_sort_off_by_one(arr: List[int]) -> List[int]:
    """
    BUGGY IMPLEMENTATION #1: Off-by-One Loop Bound / Index Error.
    
    What is wrong:
        The inner loop executes: `for j in range(0, n - i):`
        When i = 0 and j reaches n - 1, accessing `arr[j + 1]` triggers:
        `IndexError: list index out of range`.
        
    Diagnostic Lesson:
        Because Python ranges are exclusive of the stop value, checking
        index `j + 1` requires the loop stop value to be at most `len(arr) - 1`.
    """
    n = len(arr)
    # The erroneous inner loop bound:
    # for i in range(n):
    #     for j in range(0, n - i):  <-- BUG: j reaches n - 1, so j + 1 causes IndexError!
    #         if arr[j] > arr[j + 1]:
    #             arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    # Safe demonstration reproducing the boundary without crashing:
    copy_arr = list(arr)
    try:
        for i in range(n):
            for j in range(0, n - i):
                if j + 1 >= len(copy_arr):
                    raise IndexError(f"IndexError caught! j={j}, j+1={j+1}, len={len(copy_arr)}")
                if copy_arr[j] > copy_arr[j + 1]:
                    copy_arr[j], copy_arr[j + 1] = copy_arr[j + 1], copy_arr[j]
    except IndexError as e:
        # Returning partial result with debugging note
        print(f"[Debug Caught Bug #1]: {e}")
    return copy_arr


def buggy_bubble_sort_stability_violation(arr: List[Any]) -> List[Any]:
    """
    BUGGY IMPLEMENTATION #2: Stability Violation via `>=` Comparison.
    
    What is wrong:
        The condition is written as `if arr[j] >= arr[j + 1]:` instead of `>`.
        When two identical keys are encountered, they swap positions.
        This destroys stability, meaning records with equal keys are shuffled.
        
    Diagnostic Lesson:
        To guarantee stability in any comparison sort, elements with equal keys
        must NEVER swap or leapfrog one another. Always use strict inequality (`>`).
    """
    cloned = list(arr)
    n = len(cloned)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            # BUG: >= swaps equal elements, destroying stable ordering!
            if cloned[j] >= cloned[j + 1]:
                cloned[j], cloned[j + 1] = cloned[j + 1], cloned[j]
    return cloned


# ==============================================================================
# 5. EDUCATIONAL TRACE ENGINE
# ==============================================================================

def trace_bubble_sort(arr: List[int]) -> List[int]:
    """
    Executes Bubble Sort while printing a granular, educational step-by-step trace.
    """
    cloned = list(arr)
    n = len(cloned)
    print(f"\n{'='*70}")
    print(f"BEGINNING BUBBLE SORT TRACE FOR: {cloned}")
    print(f"{'='*70}")

    total_comps = 0
    total_swaps = 0

    for i in range(n - 1):
        swapped = False
        unsorted_limit = n - 1 - i
        print(f"\n>>> PASS {i}: Active Unsorted Slice [0 .. {unsorted_limit}]")
        print(f"    Current Array State: {cloned[:unsorted_limit + 1]} | {cloned[unsorted_limit + 1:]}")

        for j in range(unsorted_limit):
            total_comps += 1
            left, right = cloned[j], cloned[j + 1]
            if left > right:
                cloned[j], cloned[j + 1] = cloned[j + 1], cloned[j]
                total_swaps += 1
                swapped = True
                print(f"    Step {j}: Compare ({left} > {right}) -> SWAP!  => {cloned}")
            else:
                print(f"    Step {j}: Compare ({left} <= {right}) -> OK     => {cloned}")

        print(f"    Pass {i} Complete: Element '{cloned[unsorted_limit]}' is finalized in sorted suffix.")
        if not swapped:
            print("    [EARLY EXIT] No swaps occurred during this entire pass. Array is fully sorted!")
            break

    print(f"\nFINAL SORTED ARRAY: {cloned}")
    print(f"Total Comparisons: {total_comps} | Total Swaps: {total_swaps}")
    print(f"{'='*70}\n")
    return cloned


# ==============================================================================
# 6. COMPREHENSIVE TEST SUITE
# ==============================================================================

@dataclasses.dataclass
class KeyVal:
    """Helper record to rigorously verify sort stability."""
    key: int
    val: str

    def __lt__(self, other: KeyVal) -> bool:
        return self.key < other.key

    def __gt__(self, other: KeyVal) -> bool:
        return self.key > other.key

    def __le__(self, other: KeyVal) -> bool:
        return self.key <= other.key

    def __ge__(self, other: KeyVal) -> bool:
        return self.key >= other.key


def count_inversions(arr: Sequence[int]) -> int:
    """Brute force helper to count inversions for swap verification."""
    inv = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv += 1
    return inv


def run_tests() -> None:
    """
    Comprehensive test suite validating functional correctness, invariants,
    edge cases, stability, and algorithmic properties.
    """
    print(">>> Running Comprehensive Bubble Sort Test Suite...")

    # 1. Edge Case: Empty List
    empty_list: List[int] = []
    assert bubble_sort(empty_list) == [], "Failed on empty list."
    assert cocktail_shaker_sort([]) == [], "Cocktail failed on empty list."
    assert bubble_sort_recursive([]) == [], "Recursive failed on empty list."

    # 2. Edge Case: Single Element
    single = [42]
    assert bubble_sort(single) == [42], "Failed on single element."
    assert cocktail_shaker_sort([42]) == [42], "Cocktail failed on single element."
    assert bubble_sort_recursive([42]) == [42], "Recursive failed on single element."

    # 3. Edge Case: Two Elements
    assert bubble_sort([2, 1]) == [1, 2], "Failed on two elements unsorted."
    assert bubble_sort([1, 2]) == [1, 2], "Failed on two elements sorted."

    # 4. Already Sorted Array (Adaptive O(N) verification)
    sorted_input = [1, 2, 3, 4, 5, 6, 7, 8]
    metrics = SortMetrics()
    result = bubble_sort(list(sorted_input), metrics)
    assert result == sorted_input, "Failed on already sorted array."
    assert metrics.swaps == 0, f"Expected 0 swaps on sorted array, got {metrics.swaps}"
    assert metrics.comparisons == len(sorted_input) - 1, (
        f"Expected {len(sorted_input) - 1} comparisons, got {metrics.comparisons}"
    )
    assert metrics.early_termination is True, "Early termination was not triggered on sorted array."

    # 5. Reverse Sorted Array (Worst-Case verification)
    rev_input = [5, 4, 3, 2, 1]
    metrics.reset()
    result = bubble_sort(list(rev_input), metrics)
    assert result == [1, 2, 3, 4, 5], "Failed on reverse sorted array."
    expected_worst_comps = len(rev_input) * (len(rev_input) - 1) // 2
    assert metrics.comparisons == expected_worst_comps, (
        f"Expected {expected_worst_comps} comparisons, got {metrics.comparisons}"
    )
    assert metrics.swaps == expected_worst_comps, (
        f"Expected {expected_worst_comps} swaps, got {metrics.swaps}"
    )

    # 6. Mathematical Inversion Count Invariant Test: Swaps == Inversions
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [8, 7, 6, 5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [1, 3, 2, 5, 4, 7, 6],
    ]
    for case in test_cases:
        inversions = count_inversions(case)
        m = SortMetrics()
        bubble_sort(list(case), m)
        assert m.swaps == inversions, (
            f"Invariant violation for {case}: swaps ({m.swaps}) != inversions ({inversions})"
        )

    # 7. Duplicate Elements & Homogeneous List
    duplicates = [3, 1, 2, 3, 1, 2, 3]
    assert bubble_sort(list(duplicates)) == sorted(duplicates), "Failed on duplicates."
    all_same = [7, 7, 7, 7, 7]
    m_same = SortMetrics()
    assert bubble_sort(list(all_same), m_same) == [7, 7, 7, 7, 7]
    assert m_same.swaps == 0, "Identical elements caused unnecessary swaps."
    assert m_same.early_termination is True, "Identical array failed early exit."

    # 8. Negative Numbers and Floating Points
    float_list = [3.14, -2.71, 0.0, -100.5, 42.0]
    assert bubble_sort(list(float_list)) == sorted(float_list), "Failed on float list."

    # 9. Stability Verification
    # We tag duplicate keys with distinct values to see if their relative order is retained.
    stable_input = [
        KeyVal(key=2, val="A"),
        KeyVal(key=1, val="B"),
        KeyVal(key=2, val="C"),
        KeyVal(key=1, val="D"),
        KeyVal(key=2, val="E"),
    ]
    stable_output = bubble_sort(list(stable_input))
    # For key=1, relative order must be B then D
    ones = [item.val for item in stable_output if item.key == 1]
    assert ones == ["B", "D"], f"Stability violated for key 1: got {ones}"
    # For key=2, relative order must be A then C then E
    twos = [item.val for item in stable_output if item.key == 2]
    assert twos == ["A", "C", "E"], f"Stability violated for key 2: got {twos}"

    # 10. Verify Deliberate Stability Violation Bug
    unstable_output = buggy_bubble_sort_stability_violation(list(stable_input))
    unstable_twos = [item.val for item in unstable_output if item.key == 2]
    # The bug should have reversed or altered the order of key=2 elements
    assert unstable_twos != ["A", "C", "E"], "Buggy stability sort failed to demonstrate flaw."

    # 11. Test Cocktail Shaker Sort and Turtle Resolution
    # In [2, 3, 4, 5, 1], '1' is a turtle.
    turtle_arr = [2, 3, 4, 5, 1]
    m_cocktail = SortMetrics()
    cocktail_res = cocktail_shaker_sort(list(turtle_arr), m_cocktail)
    assert cocktail_res == [1, 2, 3, 4, 5], "Cocktail Shaker failed on turtle array."

    # 12. Test Last-Swap Optimized Variant
    m_last_swap = SortMetrics()
    last_swap_res = bubble_sort_last_swap_optimized(list(turtle_arr), m_last_swap)
    assert last_swap_res == [1, 2, 3, 4, 5], "Last-swap optimized variant failed."

    # 13. Test Recursive Implementation
    for case in test_cases:
        assert bubble_sort_recursive(list(case)) == sorted(case), (
            f"Recursive Bubble Sort failed on case {case}"
        )

    # 14. Test Pure Functional Variant
    original_tuple = (5, 2, 8, 1, 9)
    pure_res = bubble_sort_pure(original_tuple)
    assert pure_res == [1, 2, 5, 8, 9]
    assert isinstance(pure_res, list)

    # 15. Standard Library Production Sort Equivalence
    for case in test_cases:
        assert production_sort(case) == sorted(case)
        assert production_sort(case, reverse=True) == sorted(case, reverse=True)

    print(">>> All 15 Test Categories Passed Successfully!\n")


# ==============================================================================
# 7. MAIN DEMONSTRATION BLOCK
# ==============================================================================

def main() -> None:
    """
    Main driver executing tests, demonstrating step-by-step traces,
    and comparing algorithm variants.
    """
    print("=" * 80)
    print("      BUBBLE SORT (EXCHANGE SORT): TEXTBOOK PEDAGOGICAL DEMONSTRATION      ")
    print("=" * 80)

    # 1. Run full unit test suite
    run_tests()

    # 2. Educational Step-by-Step Execution Trace
    sample_data = [64, 34, 25, 12, 22, 11, 90]
    trace_bubble_sort(sample_data)

    # 3. Demonstrating "Turtles vs Rabbits" Asymmetry
    print("=" * 80)
    print("DEMONSTRATION: TURTLES VS. RABBITS ASYMMETRY")
    print("=" * 80)
    
    # A rabbit (large value near start):
    rabbit_data = [99, 1, 2, 3, 4, 5]
    m_rabbit = SortMetrics()
    bubble_sort(list(rabbit_data), m_rabbit)
    print(f"Rabbit Array  : {rabbit_data}")
    print(f"  Standard Bubble Sort -> Passes: {m_rabbit.passes_executed}, Swaps: {m_rabbit.swaps}")

    # A turtle (small value near end):
    turtle_data = [2, 3, 4, 5, 6, 1]
    m_turtle = SortMetrics()
    bubble_sort(list(turtle_data), m_turtle)
    print(f"Turtle Array  : {turtle_data}")
    print(f"  Standard Bubble Sort -> Passes: {m_turtle.passes_executed}, Swaps: {m_turtle.swaps}")

    # Cocktail shaker resolving the turtle:
    m_cocktail_turtle = SortMetrics()
    cocktail_shaker_sort(list(turtle_data), m_cocktail_turtle)
    print(f"  Cocktail Shaker Sort -> Passes: {m_cocktail_turtle.passes_executed}, Swaps: {m_cocktail_turtle.swaps}")
    print("Notice how Cocktail Shaker resolves the turtle in fewer total passes!\n")

    # 4. Demonstrate Deliberate Bug Catching
    print("=" * 80)
    print("DEMONSTRATION: DELIBERATE BUG REPRODUCTION")
    print("=" * 80)
    print("Calling buggy_bubble_sort_off_by_one([10, 20, 30]):")
    buggy_bubble_sort_off_by_one([10, 20, 30])

    print("\nBubble Sort pedagogical demonstration concluded successfully.")


if __name__ == "__main__":
    main()
