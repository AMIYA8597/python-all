r"""
# Exponential Search: Architecture, Mechanics, and Practical Applications

## A. Concept Name
Exponential Search (also known as Doubling Search, Galloping Search, or the Bentley–Yao Algorithm).

## B. One-Sentence Definition
Exponential Search is an optimal two-phase search algorithm for sorted collections that first isolates a bounded interval $[2^{k-1}, \min(2^k, N-1)]$ containing the target by exponentially doubling an index pointer, and then performs a binary search within that localized window in $O(\log i)$ time, where $i$ is the target's index.

## C. Why Does This Exist? (What problem does it solve?)
In computer science and systems programming, standard Binary Search suffers from two major limitations:
1. **The Unbounded / Infinite Stream Problem**: Standard binary search strictly requires knowing the total size $N$ upfront to compute the initial midpoint $\lfloor(0 + (N-1)) / 2\rfloor$. When querying unbounded streams, memory-mapped files of unknown length, hardware sensor feeds, or remote paginated database cursors where computing `COUNT(*)` is cost-prohibitive, Binary Search cannot even begin. Exponential search discovers an upper bound dynamically in $O(\log i)$ steps without ever querying total size $N$.
2. **Head-Biased / Skewed Query Distributions**: If an array contains $N = 1,000,000,000$ elements, but the target resides near the front (e.g., index $i = 10$), standard binary search begins at index $500,000,000$ and takes $\approx \lceil \log_2(10^9) \rceil \approx 30$ comparisons. Exponential search checks indices $1, 2, 4, 8, 16$, establishes the window $[8, 16]$, and binary searches within those 8 elements, resolving in only $\approx 8$ total comparisons—a $> 3.5\times$ speedup!
3. **Galloping Mode in High-Performance Merging**: When merging two sorted lists where one list has long consecutive runs of elements smaller than the other (e.g., merging $[1, 2, 3, \dots, 1000]$ with $[500]$), stepping linearly costs $O(K)$ comparisons. Exponential "galloping" skips over huge chunks of data in $O(\log K)$ comparisons, forming the core optimization behind **Timsort** (Python's and Java's default sort).

## D. Intuition & Real-Life Analogy
- **Searching for an Unknown Highway Exit**:
  You are driving on an unfamiliar, endless rural highway looking for Exit 73. You have no map and do not know how long the highway is. You check Mile 1: not here. You double your distance to Mile 2, Mile 4, Mile 8, Mile 16, Mile 32, Mile 64, Mile 128.
  At Mile 128, you see the exit number is 135—you have overshot Exit 73!
  You now know with 100% certainty that Exit 73 is trapped between Mile 64 and Mile 128. You turn around and binary search only that 64-mile segment.
- **Sound Technician Volume Calibration**:
  When a microphone signal is too quiet, an engineer doubles the gain ($2\times, 4\times, 8\times, 16\times$) until the signal clips, then dials it down with binary refinements.

## E. Mental Model
Exponential search breaks the search space into two distinct sequential phases:
```text
Phase 1: EXPONENTIAL BOUNDING (Galloping)
Target = 42

Index:  [0]   [1]   [2]   [3]   [4]   [5]   [6]   [7]   [8]   [9]  [10]  [11]  [12]  [13]  [14]  [15]
Values: | 2 | | 5 | | 8 | |13| |19| |24| |31| |37| |42| |49| |56| |63| |71| |80| |92| |99|
Step 0: Check index 0 -> arr[0] = 2 != 42 (target is larger, continue)
Step 1: i = 1  -> arr[1]  = 5  < 42 -> Double i -> i = 2
Step 2: i = 2  -> arr[2]  = 8  < 42 -> Double i -> i = 4
Step 3: i = 4  -> arr[4]  = 19 < 42 -> Double i -> i = 8
Step 4: i = 8  -> arr[8]  = 42 <= 42 -> Double i -> i = 16 (or overshoot: arr[16] > 42)
Trapped Range: Low = i // 2 = 4 (or 8), High = min(i, N - 1) = 15

Phase 2: LOCALIZED BINARY SEARCH
Only search the isolated slice arr[8 .. 15]!
Mid = (8 + 15) // 2 = 11 -> arr[11] = 63 > 42 -> High = 10
Mid = (8 + 10) // 2 = 9  -> arr[9]  = 49 > 42 -> High = 8
Mid = (8 + 8)  // 2 = 8  -> arr[8]  = 42 == 42 -> MATCH FOUND at Index 8!
```

## F. Formal Technical Explanation
Let $A$ be a monotonically non-decreasing array of size $N$ (where $N$ may be finite or $\infty$).
1. **Base Check**: Inspect $A[0]$. If $A[0] == target$, return index $0$. If $A[0] > target$, return $-1$ (target cannot exist in a sorted non-negative indexed array).
2. **Phase 1 (Exponential Bounding)**:
   - Initialize pointer $i = 1$.
   - **Loop Invariant**: At the beginning of step $k$, $target > A[j]$ for all $j < 2^{k-1}$.
   - While $i < N$ and $A[i] \le target$:
     $$i \leftarrow i \times 2$$
   - Termination Condition: The loop terminates when either $i \ge N$ or $A[i] > target$.
3. **Phase 2 (Binary Search)**:
   - By the loop invariant and termination condition, the target must reside within the closed index range:
     $$[low, high] = \left[\left\lfloor \frac{i}{2} \right\rfloor, \min(i, N - 1)\right]$$
   - Standard binary search is executed exclusively over this interval.

## G. Mathematical Foundation
Let $i$ denote the actual 0-based index of the target in array $A$.

1. **Phase 1 Comparison Count**:
   The pointer values follow powers of two: $1, 2, 4, 8, \dots, 2^k$.
   The loop terminates at the smallest integer $k$ such that $2^k \ge i$.
   $$2^{k-1} \le i < 2^k \implies k = \lceil \log_2(i + 1) \rceil$$
   Comparisons made in Phase 1:
   $$C_{\text{Phase 1}} = 1 + \lceil \log_2(i + 1) \rceil$$
   *(1 comparison for index 0, plus $k$ comparisons for the powers of 2).*

2. **Phase 2 Comparison Count**:
   The binary search operates on an interval of length:
   $$W = high - low + 1 = 2^k - 2^{k-1} + 1 = 2^{k-1} + 1 \le i + 1$$
   The maximum number of comparisons in a binary search over window $W$ is:
   $$C_{\text{Phase 2}} \le \lceil \log_2(W) \rceil \le \lceil \log_2(2^{k-1} + 1) \rceil \le k$$

3. **Total Asymptotic Comparisons**:
   $$C_{\text{Total}} = C_{\text{Phase 1}} + C_{\text{Phase 2}} \le 1 + k + k = 2k + 1 \le 2 \lceil \log_2(i + 1) \rceil + 1 \in O(\log i)$$

4. **Information-Theoretic Optimality (Bentley–Yao Bound)**:
   In 1976, Jon Bentley and Andrew Yao proved that searching an unbounded sorted sequence of positive integers requires at least:
   $$\log_2 i + \log_2 \log_2 i + \dots + O(1) \quad \text{comparisons}$$
   Exponential search achieves $2 \log_2 i$ comparisons, which is within a constant factor of $2$ of the theoretical optimum for unbounded search without prior knowledge of $N$.

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - Best Case: $O(1)$ comparisons (occurs when $A[0] == target$).
  - Target near front ($i \ll N$): $O(\log i)$ comparisons.
  - Worst Case / Target Absent: $O(\log N)$ comparisons (when $i \approx N-1$ or target exceeds all elements).
- **Space Complexity**:
  - Iterative Implementation: $O(1)$ auxiliary memory (only variables `i`, `low`, `high`, `mid`).
  - Recursive Implementation: $O(\log i)$ auxiliary stack space due to recursion frames during the binary search phase.
- **Hardware & CPU Cache Locality**:
  In modern CPU architectures with multi-tiered caches (L1: 32KB, L2: 512KB, L3: 32MB, DRAM: GBs), standard binary search causes immediate cache misses on large arrays because the initial jumps leap by gigabytes across memory.
  Exponential search begins in the L1 cache ($A[0], A[1], A[2], A[4]$ share the same or adjacent 64-byte cache lines!). It only pays DRAM latency penalties if the target is genuinely located far away.

## I. Common Mistakes & Pitfalls
1. **The Index Zero Infinite Loop Bug**:
   Initializing $i = 0$ and doubling via $i = i \times 2$. Since $0 \times 2 = 0$, the pointer never advances, causing an infinite loop. Always inspect index 0 as a special case and initialize $i = 1$.
2. **Unbounded Index Overflow (`IndexError`)**:
   In finite arrays, failing to cap the upper bound of the binary search with $\min(i, N - 1)$. If $N = 10$ and $i$ reaches 16, evaluating `arr[16]` triggers `IndexError: list index out of range`.
3. **Degrading to Full Binary Search ($low = 0$)**:
   Setting the lower bound of Phase 2 to $0$ instead of $i // 2$. This discards the entire benefit of Phase 1, widening the search interval back to $[0, N-1]$ and degrading the runtime from $O(\log i)$ back to $O(\log N)$.
4. **Incorrect Unbounded Stream Termination**:
   When searching an unbounded stream where accessing an index beyond valid data raises an exception or returns a sentinel (e.g. `math.inf`), failing to catch the error in Phase 1 causes unhandled runtime crashes.
5. **Handling Duplicate Elements**:
   Standard exponential search returns an arbitrary index matching `target`. If the lowest index (first occurrence) is required, Phase 2 must use `bisect_left` lower-bound logic.

## J. Common Confusions
- **Exponential Search vs. Binary Search**:
  Binary Search requires a known, fixed array size $N$ upfront and always takes $\approx \log_2 N$ comparisons. Exponential search does not require knowing $N$ and takes $\approx 2 \log_2 i$ comparisons. When $i \ll N$, Exponential Search is substantially faster; when $i \approx N$, Binary Search is $\approx 2\times$ faster in terms of raw comparison count.
- **Exponential Search vs. Jump Search**:
  Jump Search steps forward by a *fixed* block size $\sqrt{N}$ and then performs a *linear search* within the block ($O(\sqrt{N})$ time). Exponential search steps forward by *exponentially increasing* powers of 2 and performs a *binary search* within the block ($O(\log i)$ time).
- **Exponential Search vs. Interpolation Search**:
  Interpolation Search estimates the target's position using numerical slope calculation ($O(\log \log N)$ on strictly uniform data). Exponential Search requires no assumptions about data distribution—it works on any monotonically ordered data.

## K. When To Use It
- The collection is unbounded, infinite, or streamed without an explicit size property (e.g., LeetCode 702: Search in a Sorted Array of Unknown Size).
- The array is sorted and targets are known or expected to be heavily skewed toward the beginning (small indices).
- Merging two sorted lists of drastically unequal sizes ($M \ll N$), where galloping search skips large non-matching segments in $O(M \log(N/M))$ time.
- External memory searches where reading block headers sequentially is cheaper than jumping across random disk sectors.

## L. When NOT To Use It
- The array is unsorted (use Linear Search or build a Hash Table).
- The data structure is a singly linked list (random access is absent; hopping to index $2^k$ requires $O(2^k)$ pointer steps, degrading total time to $O(i)$).
- Targets are uniformly distributed across a finite array with known size $N$ (Standard Binary Search takes $\log_2 N$ comparisons vs. Exponential Search's $2 \log_2 N$).

## M. Trade-offs
| Algorithm | Size $N$ Required? | Random Access? | Best Time | Time (Target at $i$) | Worst Time | Space |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | No | No | $O(1)$ | $O(i)$ | $O(N)$ | $O(1)$ |
| **Binary Search** | **Yes** | Yes | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ |
| **Jump Search** | **Yes** | Yes | $O(1)$ | $O(\sqrt{i})$ | $O(\sqrt{N})$ | $O(1)$ |
| **Exponential Search** | **No** | Yes | $O(1)$ | $O(\log i)$ | $O(\log N)$ | $O(1)$ |
| **Interpolation Search** | **Yes** | Yes | $O(1)$ | $O(\log \log i)$ (Uniform) | $O(N)$ (Skewed) | $O(1)$ |

## N. Debugging Tips
1. **Instrument the Doubling Sequence**: Print `(step, i, arr[i])` during Phase 1 to verify that $i$ follows $1, 2, 4, 8, 16, \dots$.
2. **Verify Phase 2 Clamping**: Assert that `low == i // 2` and `high == min(i, len(arr) - 1)` before invoking the binary search phase.
3. **Test Boundary Cases**: Test `target < arr[0]`, `target == arr[0]`, `target == arr[1]`, `target == arr[-1]`, and `target > arr[-1]`.

## O. Memory Hook
**"Zero first, then start at one;
Double up till bounding's done.
Cut the slice from half to bound;
Binary search will track it down!"**

## P. Active Recall Questions
1. Why does Exponential Search take $O(\log i)$ comparisons rather than $O(\log N)$?
2. Why is initializing $i = 0$ fatal to Exponential Search?
3. How does Exponential Search solve the problem of searching in an array of unknown or infinite size?
4. In what scenario is standard Binary Search faster than Exponential Search by a factor of 2?
5. How does Timsort use the galloping variant of Exponential Search to accelerate merging?

## Q. Interview Questions & Answers
- **Q1: How do you search for a target value in a sorted array of unknown (infinite) size where querying an out-of-bounds index raises an exception or returns a sentinel (e.g., LeetCode 702)?**  
  *Answer:* Standard binary search cannot be initialized because `high` is unknown. We use Exponential Search Phase 1: start at index $1$ and double $i = i \times 2$ until the reader throws an out-of-bounds sentinel or returns a value greater than `target`. Once bounded, set `low = i // 2` and `high = i`, and execute standard binary search within that range in $O(\log i)$ time and $O(1)$ space.
- **Q2: Why is the doubling multiplier $2$ chosen rather than $3$ or $4$? Could a base of $3$ or $1.5$ be theoretically faster?**  
  *Answer:* The base $b$ controls the trade-off between Phase 1 and Phase 2. With base $b$, Phase 1 takes $\log_b i$ steps, but the resulting binary search window has size $(b - 1) b^{k-1}$, taking $\log_2((b-1) b^{k-1}) \approx k \log_2 b = \log_2 i$ steps. The total comparisons evaluate to $\frac{\log_2 i}{\log_2 b} + \log_2(b - 1) + \log_2 i$. Minimizing this function with respect to $b$ yields $b \approx 2$ as the integer that minimizes comparison overhead and matches hardware bitwise shift optimizations (`i <<= 1`).
- **Q3: What is 'Galloping Mode' in Timsort and when is it triggered?**  
  *Answer:* When merging two sorted runs $A$ and $B$, Timsort begins in pairwise comparison mode. If one run consistently wins `MIN_GALLOP` times consecutively (default 7), Timsort switches to galloping mode. It uses exponential search ($1, 2, 4, 8, \dots$) in the winning run to locate where the current element of the losing run fits, copying large slices of memory via bulk `memcpy` rather than single comparisons. If the gallop slice is small, it switches back to linear mode to avoid galloping overhead.

## R. Project Connections
- **CPython Source Code**: `Objects/listobject.c` implements `gallop_left` and `gallop_right` in Timsort to accelerate list merges.
- **Search Engines (Lucene / Elasticsearch)**: Inverted index postings lists contain sorted document IDs. Finding the intersection of two queries (e.g., `termA AND termB`) uses galloping search along skip lists to bypass millions of non-matching document IDs in $O(\log i)$.
- **Database Storage Engines (RocksDB / LevelDB)**: Searching within SSTable data blocks uses exponential leaping to find the appropriate restart point offset.

## S. Edge Cases & Boundary Conditions
1. Empty array (`[]`) $\rightarrow$ Return $-1$.
2. Single-element array matching (`[42]`, target `42`) $\rightarrow$ Return `0`.
3. Single-element array non-matching (`[42]`, target `99`) $\rightarrow$ Return `-1`.
4. Target at index 0 $\rightarrow$ Handled in $O(1)$ base case, returns `0`.
5. Target at index 1 $\rightarrow$ Phase 1 stops immediately at $i=1$, returns `1`.
6. Target at the very last index $\rightarrow$ Phase 1 doubles until $i \ge N$, high is clamped to $N-1$, returns $N-1$.
7. Target smaller than smallest element $\rightarrow$ Return $-1$ immediately at base check.
8. Target larger than largest element $\rightarrow$ Phase 1 exceeds $N$, Phase 2 returns $-1$.

## T. Algorithmic Variants & Paradigms
- **Bounded Exponential Search**: Standard version operating on arrays with known length $N$.
- **Unbounded Stream Search**: Operating on an `ArrayReader` or generator where length is inaccessible.
- **Galloping Lower Bound (`bisect_left` style)**: Returns the first occurrence index among duplicate keys.
- **Galloping Intersection**: Intersects two sorted lists in $O(M \log(N/M))$ time where $M \ll N$.

## U. Algorithmic Comparison Table
| Algorithm | Precondition | Index of Target ($i$) | Time Complexity | Auxiliary Space | Random Access |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | None | Any | $O(i)$ | $O(1)$ | Not Required |
| **Binary Search** | Sorted, Bounded | Any | $O(\log N)$ | $O(1)$ | Required |
| **Exponential Search** | Sorted | $i \ll N$ | $O(\log i)$ | $O(1)$ | Required |
| **Exponential Search** | Sorted | $i \approx N$ | $O(\log N)$ | $O(1)$ | Required |
| **Galloping Merge** | 2 Sorted Lists | Disparate sizes | $O(M \log(N/M))$| $O(1)$ | Required |

## V. Practical Implementation Exercises
1. Implement Exponential Search on an `ArrayReader` interface where reading past the end raises `IndexError` and benchmark performance against standard binary search.
2. Implement Galloping List Intersection for two sorted lists where $|A| = 10$ and $|B| = 1,000,000$, demonstrating empirical comparison counts.
3. Implement a left-biased exponential search that locates the exact starting and ending range `[start, end]` of a duplicate target value in $O(\log i)$ time.

## W. Step-by-Step Execution Trace
Search target `55` in array `[2, 5, 8, 12, 16, 23, 38, 45, 55, 67, 72, 79, 84, 90, 95, 100]` ($N = 16$):
```text
Phase 1: Exponential Bounding
- Step 0: arr[0] = 2 != 55. Target is larger. Proceed to doubling.
- Step 1: i = 1  -> arr[1]  = 5  <= 55 -> Next i = 1 * 2 = 2
- Step 2: i = 2  -> arr[2]  = 8  <= 55 -> Next i = 2 * 2 = 4
- Step 3: i = 4  -> arr[4]  = 16 <= 55 -> Next i = 4 * 2 = 8
- Step 4: i = 8  -> arr[8]  = 55 <= 55 -> Next i = 8 * 2 = 16
- Step 5: i = 16 -> i >= N (16 >= 16) -> Stop Phase 1!
Identified Search Window: Low = i // 2 = 8, High = min(16, 16 - 1) = 15. Window slice: arr[8..15].

Phase 2: Localized Binary Search on arr[8..15]
- Iteration 1: Low = 8, High = 15 -> Mid = 8 + (15 - 8) // 2 = 11
               arr[11] = 79. 79 > 55 -> High = Mid - 1 = 10
- Iteration 2: Low = 8, High = 10 -> Mid = 8 + (10 - 8) // 2 = 9
               arr[9] = 67.  67 > 55 -> High = Mid - 1 = 8
- Iteration 3: Low = 8, High = 8  -> Mid = 8 + (8 - 8) // 2 = 8
               arr[8] = 55.  55 == 55 -> TARGET FOUND AT INDEX 8!
Total Comparisons: 5 (Phase 1) + 3 (Phase 2) = 8 comparisons (vs. 16 for Linear Search).
```

## X. Key Takeaways & Summary Anchor
- Exponential search breaks unbounded search into two steps: exponential doubling to bracket the target, followed by binary search to isolate it.
- Complexity is $O(\log i)$ where $i$ is the target index, making it dramatically faster than Binary Search ($O(\log N)$) when targets reside near the start of large collections.
- It is the industry-standard algorithm for searching unbounded streams and powers galloping mode in Timsort and Lucene search queries.
"""

from typing import Any, List, Optional, Protocol, Sequence, Tuple, TypeVar
import bisect
import math

T = TypeVar("T")


# ==============================================================================
# 1. STEP COUNTER & EDUCATIONAL FROM-SCRATCH IMPLEMENTATION
# ==============================================================================

class SearchStepCounter:
    """Deterministic operation tracker for searching algorithms."""
    def __init__(self) -> None:
        self.comparisons: int = 0

    def compare(self) -> None:
        self.comparisons += 1

    def reset(self) -> None:
        self.comparisons = 0


def binary_search_window(
    arr: Sequence[T],
    target: T,
    low: int,
    high: int,
    counter: Optional[SearchStepCounter] = None,
) -> int:
    """
    Standard iterative binary search localized to a specific window [low, high].
    
    Args:
        arr: Monotonically ordered sequence of elements.
        target: Value to locate.
        low: Inclusive starting index of search window.
        high: Inclusive ending index of search window.
        counter: Optional step counter tracking comparisons.
        
    Returns:
        int: 0-based index of target if found, or -1 if absent.
    """
    while low <= high:
        if counter:
            counter.compare()
        mid = low + (high - low) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def exponential_search(
    arr: Sequence[T],
    target: T,
    counter: Optional[SearchStepCounter] = None,
) -> int:
    """
    Standard Bounded Exponential Search.
    
    Finds the index of `target` in a sorted sequence in O(log i) time, where i
    is the index of target.
    
    Args:
        arr: Monotonically sorted sequence of elements.
        target: Value to search for.
        counter: Optional step counter tracking comparisons.
        
    Returns:
        int: Index of target if found, or -1 if absent.
        
    Complexity:
        Time: O(1) Best case, O(log i) Average/Worst case.
        Space: O(1) Auxiliary space.
    """
    n = len(arr)
    if n == 0:
        return -1

    # Base Check: Index 0
    if counter:
        counter.compare()
    if arr[0] == target:
        return 0
    if arr[0] > target:
        return -1

    # Phase 1: Exponential Bounding (Galloping)
    i = 1
    while i < n:
        if counter:
            counter.compare()
        if arr[i] > target:
            break
        i *= 2

    # Phase 2: Localized Binary Search
    low = i // 2
    high = min(i, n - 1)
    return binary_search_window(arr, target, low, high, counter)


def exponential_search_recursive(
    arr: Sequence[T],
    target: T,
    bound: int = 1,
) -> int:
    """
    Recursive implementation of Exponential Search.
    Demonstrates recursive range-bounding followed by recursive binary search.
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0

    def _find_bound(i: int) -> Tuple[int, int]:
        if i >= n or arr[i] > target:
            return i // 2, min(i, n - 1)
        return _find_bound(i * 2)

    def _binary_search(low: int, high: int) -> int:
        if low > high:
            return -1
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return _binary_search(mid + 1, high)
        else:
            return _binary_search(low, mid - 1)

    low_bound, high_bound = _find_bound(bound)
    return _binary_search(low_bound, high_bound)


# ==============================================================================
# 2. SPECIALIZED & ADVANCED PRODUCTION VARIANTS
# ==============================================================================

class ArrayReader(Protocol):
    """
    Interface for an unbounded or unknown-size array (LeetCode 702 paradigm).
    Accessing an index beyond the data boundary returns a sentinel or raises an exception.
    """
    def get(self, index: int) -> int:
        ...


class InfiniteMockArray:
    """
    Simulates an unbounded sorted stream of data of unknown length.
    Calling `get(index)` for an out-of-bounds index returns 2^31 - 1 (sentinel infinity).
    """
    SENTINEL_INFINITY = 2147483647

    def __init__(self, data: List[int]) -> None:
        self._data = sorted(data)

    def get(self, index: int) -> int:
        if 0 <= index < len(self._data):
            return self._data[index]
        return self.SENTINEL_INFINITY


def unbounded_exponential_search(reader: ArrayReader, target: int) -> int:
    """
    Searches an unbounded or unknown-size array using an ArrayReader interface.
    Solves LeetCode 702: Search in a Sorted Array of Unknown Size.
    
    Complexity:
        Time: O(log i) where i is target index.
        Space: O(1) Auxiliary.
    """
    # Base Check
    val_0 = reader.get(0)
    if val_0 == target:
        return 0
    if val_0 > target:
        return -1

    # Phase 1: Exponential Bounding without knowing N
    i = 1
    while reader.get(i) < target:
        i *= 2

    # Phase 2: Binary Search in [i // 2, i]
    low = i // 2
    high = i

    while low <= high:
        mid = low + (high - low) // 2
        val = reader.get(mid)
        if val == target:
            return mid
        elif val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def exponential_search_first_occurrence(arr: Sequence[T], target: T) -> int:
    """
    Finds the first (leftmost) occurrence of `target` in a sorted array with duplicates.
    Implements lower-bound (bisect_left) semantics.
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    if arr[0] > target:
        return -1

    i = 1
    while i < n and arr[i] < target:
        i *= 2

    low = i // 2
    high = min(i, n - 1)
    result = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1  # Keep looking left for first occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result


def galloping_intersect_sorted(small_arr: List[int], large_arr: List[int]) -> List[int]:
    """
    Galloping intersection of two sorted arrays of drastically unequal sizes.
    Used in search engines (Lucene) and query optimizers to intersect postings lists.
    
    Complexity:
        Time: O(M log(N / M)) where M = len(small_arr) and N = len(large_arr).
    """
    intersection: List[int] = []
    large_index = 0
    n = len(large_arr)

    for item in small_arr:
        if large_index >= n:
            break
        # Exponential search in large_arr starting from large_index
        if large_arr[large_index] == item:
            intersection.append(item)
            large_index += 1
            continue

        step = 1
        curr = large_index
        while curr + step < n and large_arr[curr + step] < item:
            step *= 2

        low = curr + step // 2
        high = min(curr + step, n - 1)

        # Binary search
        pos = -1
        while low <= high:
            mid = low + (high - low) // 2
            if large_arr[mid] == item:
                pos = mid
                break
            elif large_arr[mid] < item:
                low = mid + 1
            else:
                high = mid - 1

        if pos != -1:
            intersection.append(item)
            large_index = pos + 1
        else:
            large_index = low

    return intersection


# ==============================================================================
# 3. INDUSTRY-STANDARD / PYTHONIC IMPLEMENTATION
# ==============================================================================

def exponential_search_bisect(arr: Sequence[int], target: int) -> int:
    """
    Production-grade exponential search leveraging Python's built-in `bisect`.
    Combines Python-level exponential bounding with C-level binary search.
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    if arr[0] > target:
        return -1

    i = 1
    while i < n and arr[i] <= target:
        i *= 2

    low = i // 2
    high = min(i, n)

    # bisect_left returns insertion index
    idx = bisect.bisect_left(arr, target, lo=low, hi=high)
    if idx < n and arr[idx] == target:
        return idx
    return -1


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DEBUGGING COMMENTARY
# ==============================================================================

def exponential_search_buggy_zero_loop(arr: Sequence[int], target: int) -> int:
    """
    BUGGY IMPLEMENTATION #1: Starting at index 0 (Infinite Loop).
    
    Diagnostic Analysis:
    - Failing Behavior: `i = 0`; `i = i * 2` evaluates to `0 * 2 = 0`.
      The index never increments, locking the thread in an infinite loop!
    - Resolution: Inspect index 0 separately, then start doubling from `i = 1`.
    """
    if not arr:
        return -1
    i = 0  # <- BUG: 0 * 2 == 0 forever!
    while i < len(arr) and arr[i] <= target:
        i = i * 2  # Infinite loop!
        if i == 0:
            # Safeguard to prevent freezing tests during diagnostic execution
            raise TimeoutError("Buggy exponential search hung in infinite loop: i * 2 == 0!")
    return -1


def exponential_search_buggy_out_of_bounds(arr: Sequence[int], target: int) -> int:
    """
    BUGGY IMPLEMENTATION #2: Missing Bounds Clamping.
    
    Diagnostic Analysis:
    - Failing Behavior: Setting `high = i` without `min(i, len(arr) - 1)`.
      When `i` doubles past the end of the array, `arr[mid]` raises an `IndexError`.
    - Resolution: Always clamp high with `min(i, len(arr) - 1)`.
    """
    n = len(arr)
    if not arr or arr[0] > target:
        return -1
    if arr[0] == target:
        return 0

    i = 1
    while i < n and arr[i] <= target:
        i *= 2

    # BUG: high is set to i without min(i, n - 1), leading to IndexError
    low = i // 2
    high = i  # <- BUG: Can exceed len(arr) - 1!
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:  # Crashes if mid >= n!
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def exponential_search_buggy_low_bound(arr: Sequence[int], target: int) -> int:
    """
    BUGGY IMPLEMENTATION #3: Setting Lower Bound to 0.
    
    Diagnostic Analysis:
    - Failing Behavior: Correctly bounds `i`, but then sets `low = 0` instead of `low = i // 2`.
      This throws away all the work done in Phase 1, forcing binary search across
      the entire prefix and destroying the O(log i) guarantee.
    """
    n = len(arr)
    if not arr or arr[0] > target:
        return -1
    if arr[0] == target:
        return 0

    i = 1
    while i < n and arr[i] <= target:
        i *= 2

    low = 0  # <- BUG: Should be i // 2! Destroys localized O(log i) window.
    high = min(i, n - 1)
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite validating functional correctness across all edge cases.
    """
    print(">>> Executing Exponential Search Test Suite...")

    # Test Datasets
    empty_arr: List[int] = []
    single_arr: List[int] = [42]
    small_arr: List[int] = [2, 5, 8, 12, 16, 23, 38, 45, 55, 67, 72, 79, 84, 90, 95, 100]
    dup_arr: List[int] = [1, 2, 4, 4, 4, 4, 8, 16, 32]
    large_arr: List[int] = list(range(0, 200_000, 2))  # 100,000 even numbers: 0, 2, 4, ...

    # 1. Base Boundary Tests
    assert exponential_search(empty_arr, 10) == -1, "Failed on empty array"
    assert exponential_search(single_arr, 42) == 0, "Failed on single matching element"
    assert exponential_search(single_arr, 99) == -1, "Failed on single non-matching element"
    assert exponential_search(single_arr, 5) == -1, "Failed on single element smaller"

    # 2. Target Location Tests (Index 0, Index 1, Index Last, Middle)
    assert exponential_search(small_arr, 2) == 0, "Failed to find element at index 0 (best case)"
    assert exponential_search(small_arr, 5) == 1, "Failed to find element at index 1"
    assert exponential_search(small_arr, 55) == 8, "Failed to find element in middle"
    assert exponential_search(small_arr, 100) == 15, "Failed to find element at last index"

    # 3. Missing Elements Tests
    assert exponential_search(small_arr, 1) == -1, "Failed on element smaller than minimum"
    assert exponential_search(small_arr, 50) == -1, "Failed on absent element in middle"
    assert exponential_search(small_arr, 999) == -1, "Failed on element larger than maximum"

    # 4. Large Dataset Performance Test (O(log i) verification)
    counter = SearchStepCounter()
    idx_early = exponential_search(large_arr, 16, counter)  # Target at index 8
    assert idx_early == 8
    # For index 8, Phase 1 takes ~5 comparisons, Phase 2 takes ~3 comparisons => <= 10 total
    assert counter.comparisons <= 12, f"Too many comparisons for early index: {counter.comparisons}"

    counter.reset()
    idx_late = exponential_search(large_arr, 199_998, counter)  # Target at index 99,999
    assert idx_late == 99_999
    # For index 100,000, total comparisons is <= 2 * log2(100,000) ~ 36
    assert counter.comparisons <= 40, f"Too many comparisons for late index: {counter.comparisons}"

    # 5. Recursive Version Tests
    assert exponential_search_recursive(small_arr, 2) == 0
    assert exponential_search_recursive(small_arr, 55) == 8
    assert exponential_search_recursive(small_arr, 100) == 15
    assert exponential_search_recursive(small_arr, 999) == -1
    assert exponential_search_recursive(empty_arr, 5) == -1

    # 6. Unbounded / Unknown Size Array (ArrayReader) Tests
    reader = InfiniteMockArray(small_arr)
    assert unbounded_exponential_search(reader, 2) == 0
    assert unbounded_exponential_search(reader, 55) == 8
    assert unbounded_exponential_search(reader, 100) == 15
    assert unbounded_exponential_search(reader, 999) == -1
    assert unbounded_exponential_search(reader, 1) == -1

    # 7. First Occurrence Duplicate Search Tests
    assert exponential_search_first_occurrence(dup_arr, 4) == 2, "Failed to find first duplicate occurrence"
    assert exponential_search_first_occurrence(dup_arr, 1) == 0
    assert exponential_search_first_occurrence(dup_arr, 32) == 8
    assert exponential_search_first_occurrence(dup_arr, 99) == -1

    # 8. Galloping List Intersection Tests
    postings_a = [3, 8, 19, 45, 99]
    postings_b = list(range(0, 100))  # 0 .. 99
    assert galloping_intersect_sorted(postings_a, postings_b) == [3, 8, 19, 45, 99]
    assert galloping_intersect_sorted([5, 10, 15], [1, 2, 3, 4]) == []

    # 9. Pythonic bisect Implementation Tests
    assert exponential_search_bisect(small_arr, 2) == 0
    assert exponential_search_bisect(small_arr, 55) == 8
    assert exponential_search_bisect(small_arr, 100) == 15
    assert exponential_search_bisect(small_arr, 999) == -1
    assert exponential_search_bisect(empty_arr, 1) == -1

    # 10. Buggy Functions Diagnostic Assertions
    # Bug 1: Must catch infinite loop safeguard
    try:
        exponential_search_buggy_zero_loop([1, 2, 3], 2)
        assert False, "Expected buggy zero loop to raise TimeoutError"
    except TimeoutError:
        pass  # Expected behavior

    # Bug 2: Must catch out-of-bounds error on target larger than array
    try:
        exponential_search_buggy_out_of_bounds([1, 2, 3, 4, 5], 99)
        assert False, "Expected out of bounds error"
    except IndexError:
        pass  # Expected behavior

    print("[+] All 10 unit test suites passed successfully!")


# ==============================================================================
# 6. MAIN EXECUTION & VISUAL EDUCATIONAL TRACE
# ==============================================================================

def main() -> None:
    """
    Main driver executing test suite and displaying visual step-by-step trace.
    """
    run_tests()

    print("\n" + "=" * 80)
    print("EDUCATIONAL TRACE: EXPONENTIAL SEARCH IN ACTION")
    print("=" * 80)

    demo_arr = [2, 5, 8, 12, 16, 23, 38, 45, 55, 67, 72, 79, 84, 90, 95, 100]
    target = 55
    n = len(demo_arr)

    print(f"Target Value: {target}")
    print(f"Input Array (N={n}):")
    print(demo_arr)
    print("-" * 80)
    print("PHASE 1: EXPONENTIAL BOUNDING (Galloping)")
    print(f"{'Step':<6} | {'Pointer i':<10} | {'Value arr[i]':<14} | {'Condition (arr[i] <= Target)':<30} | {'Action'}")
    print("-" * 80)

    # Step 0
    print(f"{'0':<6} | {'0':<10} | {demo_arr[0]:<14} | {f'{demo_arr[0]} == {target} (False)':<30} | Target > arr[0]. Proceed to double.")

    i = 1
    step_num = 1
    while i < n and demo_arr[i] <= target:
        cond_str = f"{demo_arr[i]} <= {target} (True)"
        action = f"Double pointer: i -> {i * 2}"
        print(f"{step_num:<6} | {i:<10} | {demo_arr[i]:<14} | {cond_str:<30} | {action}")
        i *= 2
        step_num += 1

    if i < n:
        cond_str = f"{demo_arr[i]} <= {target} (False)"
        action = "Target exceeded! Terminate Phase 1."
        print(f"{step_num:<6} | {i:<10} | {demo_arr[i]:<14} | {cond_str:<30} | {action}")
    else:
        cond_str = f"i ({i}) >= N ({n}) (True)"
        action = "Array end reached! Terminate Phase 1."
        print(f"{step_num:<6} | {i:<10} | {'Out of Bounds':<14} | {cond_str:<30} | {action}")

    low = i // 2
    high = min(i, n - 1)
    print("-" * 80)
    print(f"Window Established: Low = {low} (arr[{low}] = {demo_arr[low]}), High = {high} (arr[{high}] = {demo_arr[high]})")
    print(f"Localized Sub-array Slice: {demo_arr[low:high+1]}")
    print("-" * 80)
    print("PHASE 2: LOCALIZED BINARY SEARCH")
    print(f"{'Iter':<6} | {'Low':<6} | {'High':<6} | {'Mid':<6} | {'Value arr[mid]':<16} | {'Action'}")
    print("-" * 80)

    b_iter = 1
    final_idx = -1
    while low <= high:
        mid = low + (high - low) // 2
        val = demo_arr[mid]
        if val == target:
            action = f"MATCH FOUND! Return index {mid}."
            print(f"{b_iter:<6} | {low:<6} | {high:<6} | {mid:<6} | {val:<16} | {action}")
            final_idx = mid
            break
        elif val < target:
            action = f"{val} < {target} -> Low = mid + 1 ({mid + 1})"
            print(f"{b_iter:<6} | {low:<6} | {high:<6} | {mid:<6} | {val:<16} | {action}")
            low = mid + 1
        else:
            action = f"{val} > {target} -> High = mid - 1 ({mid - 1})"
            print(f"{b_iter:<6} | {low:<6} | {high:<6} | {mid:<6} | {val:<16} | {action}")
            high = mid - 1
        b_iter += 1

    print("-" * 80)
    print(f"Result: Target {target} located at index {final_idx} in {step_num + b_iter} total operations.")
    print("=" * 80)


if __name__ == "__main__":
    main()
