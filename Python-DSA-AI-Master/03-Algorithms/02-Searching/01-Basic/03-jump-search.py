r"""
# Jump Search (Block Search): Mechanics, Mathematical Optimization, and System Dynamics

## A. Concept Name
Jump Search (also known as Block Search).

## B. One-Sentence Definition
Jump Search is an algorithmic search technique for ordered arrays that reduces comparison overhead by advancing forward in fixed-size blocks of $m = \lfloor\sqrt{n}\rfloor$ elements until an interval bounding the target is identified, followed by a localized linear scan.

## C. Why Does This Exist? (What problem does it solve?)
While Binary Search boasts an asymptotically superior $O(\log n)$ comparison complexity, its access pattern requires jumping both forward and backward across distant memory addresses (e.g., from index $n/2$ to $n/4$ to $3n/8$).

In several real-world architectures and physical storage media, **jumping backward is significantly more expensive than stepping forward**:
1. **Physical Sequential Media**: On magnetic tape drives or optical discs, forward sequential reads are cheap, but seeking backward requires mechanical head repositioning or motor rewinding.
2. **Forward-Only Data Streams**: Network protocols or compressed file containers often support skipping ahead $K$ bytes efficiently, but rewinding requires re-establishing stream state or buffering.
3. **Hardware Prefetching & Cache Locality**: CPUs aggressively pre-fetch subsequent sequential cache lines. Jumping across massive strides invalidates L1/L2 caches, whereas Jump Search confines fine-grained exploration to a small, contiguous forward block.

Jump Search exists as an optimal compromise: it traverses strictly forward during the block-skipping phase, takes at most **one single step backward** to the start of the target block, and then scans forward linearly, achieving $O(\sqrt{n})$ time complexity.

## D. Intuition & Real-Life Analogy
- **Express and Local Subway Trains**: Imagine a subway system with 100 stations along a single line. An Express train stops only at every 10th station: 0, 10, 20, 30, 40... You wish to reach Station 34. You board the Express train and watch the stations: 0, 10, 20, 30... at Station 40, you realize you have overshot your destination. You get off, step back to Station 30, and board the Local train to check stations 31, 32, 33, and 34.
- **Flipping Through an 800-Page Textbook**: You are searching for Chapter 12. Instead of turning page-by-page from page 1, you flip ahead in 50-page chunks (page 50, 100, 150, 200...). Once you see Chapter 13 at page 250, you stop jumping, turn back to page 200, and flip page-by-page.

## E. Mental Model
```text
Sorted Array: [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610 ]
Length N = 16. Optimal Jump Step m = sqrt(16) = 4.
Target: 55

Phase 1: Block Leaping (Forward jumps by m = 4)
--------------------------------------------------------------------------------
Index:    0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
Array:  [ 0,   1,   1,   2,   3,   5,   8,  13,  21,  34,  55,  89, 144, 233, 377, 610 ]
                         ^                   ^                   ^
                       Jump 1              Jump 2              Jump 3
                   arr[3] = 2 < 55     arr[7] = 13 < 55    arr[11] = 89 >= 55
                                                            (OVERSHOOT DETECTED!)

Phase 2: Localized Linear Scan within Bounded Block [prev=8 to step=11]
--------------------------------------------------------------------------------
Index:             8            9           10           11
Subarray:       [ 21,          34,          55,          89 ]
                   ^
Step 2a: Check index 8  -> 21 == 55 (False, 21 < 55) -> Advance
                                ^
Step 2b: Check index 9  -> 34 == 55 (False, 34 < 55) -> Advance
                                             ^
Step 2c: Check index 10 -> 55 == 55 (True!) -> MATCH FOUND at index 10!
```

## F. Formal Technical Explanation
Given a monotonically non-decreasing sorted sequence $A$ of size $n$ ($A[0] \le A[1] \le \dots \le A[n-1]$) and target value $K$:
1. **Parameterization**: Compute block jump step $m = \lfloor\sqrt{n}\rfloor$.
2. **Phase 1 (Block Jumping)**:
   - Initialize `prev = 0` and `step = m`.
   - While $A[\min(\text{step}, n) - 1] < K$:
     - Set `prev = step`.
     - Increment `step = step + m`.
     - If `prev >= n`, the target exceeds all elements; terminate returning $-1$.
3. **Phase 2 (Linear Boundary Search)**:
   - The target is bounded within the subsegment $A[\text{prev} \dots \min(\text{step}, n) - 1]$.
   - While $A[\text{prev}] < K$:
     - Increment `prev = prev + 1`.
     - If `prev == \min(\text{step}, n)`: Reached the end of the block without finding $K$; terminate returning $-1$.
4. **Conclusion**:
   - If $A[\text{prev}] == K$, return index `prev`.
   - Otherwise, return $-1$.

## G. Mathematical Foundation
### Derivation of the Optimal Jump Size $m$:
Let $n$ be the length of the array and $m$ be the fixed block jump size.
- **Maximum Number of Jumps (Phase 1)**:
  In the worst case (target at the very end or absent), the algorithm jumps forward $\lfloor n/m \rfloor$ times.
- **Maximum Number of Linear Comparisons (Phase 2)**:
  Within the bounded block of length $m$, the last element was already verified to be $\ge K$ during Phase 1. Thus, at most $m - 1$ linear comparisons are required.
- **Total Comparisons Function $T(n, m)$**:
  $$T(n, m) = \frac{n}{m} + (m - 1)$$

To find the step size $m$ that minimizes total comparisons $T(n, m)$, compute the first derivative with respect to $m$ and set it to zero:
$$\frac{dT}{dm} = -\frac{n}{m^2} + 1 = 0$$
$$\frac{n}{m^2} = 1 \implies m^2 = n \implies m = \sqrt{n}$$

Verify with the second derivative test:
$$\frac{d^2T}{dm^2} = \frac{2n}{m^3} > 0 \quad (\forall n > 0, m > 0)$$
Since the second derivative is strictly positive, $m = \sqrt{n}$ is a strict global minimum.

### Total Operations with Optimal $m$:
$$T(n, \sqrt{n}) = \frac{n}{\sqrt{n}} + \sqrt{n} - 1 = 2\sqrt{n} - 1 = O(\sqrt{n})$$

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - Best Case: $O(1)$ (Target is found at index 0 on the first comparison).
  - Average Case: $O(\sqrt{n})$ (On average $\approx \frac{\sqrt{n}}{2}$ jumps $+ \frac{\sqrt{n}}{2}$ linear checks $\approx \sqrt{n}$ comparisons).
  - Worst Case: $O(\sqrt{n})$ ($2\sqrt{n} - 1$ comparisons when target is at index $n-2$ or absent).
- **Space Complexity**:
  - Auxiliary Space: $O(1)$ (Requires only three scalar integer variables: `prev`, `step`, and `jump_size`).
- **Memory & Cache Hierarchy Dynamics**:
  Unlike Binary Search, which exhibits $O(\log n)$ memory reads scattered across disparate pages, Jump Search confines its fine-grained linear phase to contiguous elements in the same memory cache line (64 bytes typically hold 8 to 16 integer values). This minimizes Translation Lookaside Buffer (TLB) misses and CPU cache invalidations during Phase 2.

## I. Common Mistakes & Pitfalls
1. **Index Out-of-Bounds on Final Jump**:
   If $n$ is not a perfect square, adding $m$ repeatedly can result in `step > n`. Evaluating `arr[step - 1]` without clamping using `min(step, n) - 1` raises an unhandled `IndexError`.
2. **Infinite Loop on $n = 0$ or $n = 1$**:
   If `math.isqrt(n)` returns 0 for an empty list or small input, `step += 0` causes an infinite loop. The jump size must be guarded: `max(1, math.isqrt(n))`.
3. **Applying Jump Search to Unsorted Data**:
   Jump Search requires the array to be monotonically ordered. If given an unsorted array, it will skip entire blocks that may contain the target, failing silently.
4. **Precision Issues with Floating-Point Square Roots**:
   Using `int(math.sqrt(n))` on very large inputs ($n > 2^{53}$) can encounter floating-point inaccuracies. Python 3.8+ provides `math.isqrt(n)`, which computes exact integer square roots using integer arithmetic.
5. **Searching Singly-Linked Lists**:
   Attempting to use Jump Search on a linked list requires $O(m)$ steps just to jump forward $m$ nodes. The total time becomes $\frac{n}{m} \cdot m + m = n + m = O(n)$, defeating the entire purpose of the algorithm.

## J. Common Confusions
- **Jump Search vs. Binary Search**:
  Binary Search is faster asymptotically ($O(\log n)$ vs $O(\sqrt{n})$). However, Binary Search requires bidirectional jumping. Jump Search requires only forward jumps until a single backward step to start the block, which is essential on unidirectional or seek-penalized storage media.
- **Jump Search vs. Exponential Search**:
  Exponential Search doubles the step size ($1, 2, 4, 8, \dots, 2^k$) and then applies **Binary Search** within the bounded range ($O(\log n)$ total). Jump Search uses a **constant** step size $\sqrt{n}$ and applies **Linear Search** ($O(\sqrt{n})$ total).
- **Jump Search vs. Interpolation Search**:
  Interpolation search estimates the target's position based on numerical key distribution ($O(\log \log n)$ average for uniform data). Jump search makes no distributional assumptions and requires only standard ordinal comparison operators.

## K. When To Use It
- Searching sorted arrays stored on media where jumping backward is expensive (e.g., magnetic tapes, optical discs, read-ahead disk streams).
- In forward-only data streams where seek-forward is supported, but rewind is costly or unsupported.
- Medium-sized sorted lists where CPU branch prediction and cache locality of sequential scans outperform binary search pointer manipulation.
- As a foundation for multi-level indexing (e.g., 2-level jump search in sparse databases).

## L. When NOT To Use It
- When random-access memory (RAM) is available and $N$ is large ($N \ge 10^4$). Binary Search ($O(\log n)$) should always be preferred in standard RAM. (For $N = 10^6$: Binary Search takes $\approx 20$ comparisons; Jump Search takes $\approx 2000$ comparisons!).
- When the data is unsorted (use Linear Search or Hash Table).
- On singly linked lists lacking skip pointers (degrades to $O(n)$).

## M. Trade-offs
| Algorithm | Best Time | Average Time | Worst Time | Backward Seeks | Array Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jump Search** | $O(1)$ | $O(\sqrt{n})$ | $O(\sqrt{n})$ | At most 1 | Sorted + Random Access |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | Up to $\log_2 n$ | Sorted + Random Access |
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | 0 | None (Any Iterable) |
| **Exponential Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | Up to $\log_2 n$ | Sorted + Random Access |

## N. Debugging Tips
- Trace jump windows: Log `(prev, min(step, n), arr[min(step, n)-1])` at each leap.
- Validate sorting: Check `arr == sorted(arr)` during debugging.
- Verify extreme boundaries: Test $n = 0$, $n = 1$, $n = 2$, target smaller than `arr[0]`, target larger than `arr[-1]`, and target at the exact leap boundary.

## O. Memory Hook
**"Leap like a frog by root of N, walk like an ant within the pen."**
Visualize a frog leaping over ponds in blocks of $\sqrt{N}$. Once it overshoots its target, an ant walks forward step-by-step through that single block.

## P. Active Recall Questions
1. Why does differentiating $T(n, m) = \frac{n}{m} + m - 1$ yield $m = \sqrt{n}$ as the optimal block size?
2. What happens to the time complexity of Jump Search if the block size is set to $m = 1$? What if $m = n$?
3. Why does Jump Search fail to achieve $O(\sqrt{n})$ on a standard singly linked list?
4. Under what physical hardware conditions would Jump Search outperform Binary Search?

## Q. Interview Questions & Answers
- **Q1: How would you search for a value in a sorted array of infinite or unknown size using jump intuition?**  
  *Answer:* When $n$ is unknown, we cannot compute $\sqrt{n}$. Instead, we perform **Exponential Search**: leap at indices $1, 2, 4, 8, 16, \dots, 2^k$ until `arr[2^k] >= target`. Then, perform a binary search or jump search between $2^{k-1}$ and $\min(2^k, \text{end})$. This completes in $O(\log i)$ time where $i$ is the target's position.
- **Q2: Can we improve Jump Search beyond $O(\sqrt{n})$ without switching to full Binary Search?**  
  *Answer:* Yes, through **Multi-Level Jump Search**. In a Two-Level Jump Search, we jump in primary blocks of size $n^{2/3}$. Once bounded, we jump in secondary sub-blocks of size $n^{1/3}$, and finally perform a linear scan of size $n^{1/3}$. The total worst-case time is $O(n^{1/3})$. In a $k$-level jump search, time complexity is $O(k \cdot n^{1/(k+1)})$, which converges to $O(\log n)$ as $k \to \log n$.
- **Q3: What occurs if the array contains duplicate elements? Does Jump Search guarantee returning the first occurrence?**  
  *Answer:* No. Jump Search finds *an* occurrence of the target within the bounded block, but it does not guarantee the *first* occurrence if duplicate elements span across multiple blocks. To find the first occurrence, the linear scan must be extended backward across previous blocks if `arr[prev] == target`.

## R. Key Takeaways & Summary Anchor
- Jump Search achieves $O(\sqrt{n})$ time by dividing a sorted array into blocks of size $\lfloor\sqrt{n}\rfloor$.
- Mathematical optimization proves $m = \sqrt{n}$ balances the number of block jumps ($\frac{n}{m}$) and within-block linear scans ($m - 1$).
- Jump Search is ideal for media where backward seeking is expensive (tapes, optical discs, read-ahead streams).
- In standard random-access RAM with large $n$, Binary Search ($O(\log n)$) remains the standard choice.

## S. Edge Cases & Boundary Conditions
1. Empty array (`[]`) $\rightarrow$ Return `-1`.
2. Single-element array matching (`[10]`, target `10`) $\rightarrow$ Return `0`.
3. Single-element array non-matching (`[10]`, target `5`) $\rightarrow$ Return `-1`.
4. Target smaller than first element (`target < arr[0]`) $\rightarrow$ Bounded in first block, linear scan terminates at index 0, returns `-1`.
5. Target larger than last element (`target > arr[-1]`) $\rightarrow$ Jumps exhaust array, returns `-1`.
6. Target located exactly at block boundary (`arr[k * m - 1] == target`) $\rightarrow$ Correctly detected and returned.
7. Two-element array $\rightarrow$ Step size $\lfloor\sqrt{2}\rfloor = 1$, functions smoothly.

## T. Algorithmic Variants & Paradigms
- **Standard Jump Search**: Jump size $\lfloor\sqrt{n}\rfloor$, linear scan.
- **Two-Level Jump Search**: Two-tier block hierarchy achieving $O(n^{1/3})$.
- **Diagnostic Traced Jump Search**: Logs every leap and comparison for educational introspection.

## U. Algorithmic Comparison Table
| Algorithm | Prerequisite | Average Time | Worst Time | Space | Primary Access Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | None | $O(n)$ | $O(n)$ | $O(1)$ | Strictly forward |
| **Jump Search** | Sorted | $O(\sqrt{n})$ | $O(\sqrt{n})$ | $O(1)$ | Forward leaps + 1 step back |
| **Two-Level Jump** | Sorted | $O(n^{1/3})$ | $O(n^{1/3})$ | $O(1)$ | 2 forward tiers + 1 step back |
| **Binary Search** | Sorted | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Bidirectional random seeks |
| **Interpolation** | Sorted + Uniform | $O(\log \log n)$ | $O(n)$ | $O(1)$ | Distribution-based seeks |

## V. Practical Implementation Exercises
1. Modify `jump_search` to guarantee returning the *first* occurrence in an array with duplicate values.
2. Implement a generic $k$-level jump search and observe how varying $k$ bridges $O(\sqrt{n})$ to $O(\log n)$.
3. Instrument Jump Search and Binary Search to count exact cache-line crossings on a $10^5$-element integer array.

## W. Step-by-Step Execution Trace
Search target `55` in sorted array `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]` ($n=16, m=4$):
| Phase | Action | `prev` | `step` | Index Checked | Value | Condition Check | Result |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Jump | Leap 1 | 0 | 4 | 3 | 2 | $2 < 55$ | True $\rightarrow$ Continue jumping |
| Jump | Leap 2 | 4 | 8 | 7 | 13 | $13 < 55$ | True $\rightarrow$ Continue jumping |
| Jump | Leap 3 | 8 | 12 | 11 | 89 | $89 < 55$ | False $\rightarrow$ Target bounded in $[8, 11]$ |
| Scan | Step 1 | 8 | 12 | 8 | 21 | $21 < 55$ | True $\rightarrow$ Advance `prev` to 9 |
| Scan | Step 2 | 9 | 12 | 9 | 34 | $34 < 55$ | True $\rightarrow$ Advance `prev` to 10 |
| Scan | Step 3 | 10 | 12 | 10 | 55 | $55 == 55$ | Match found! Return index 10 |

## X. Project Connection
- **Database Storage Engines (B+ Tree Page Slots)**: In engines like SQLite or PostgreSQL, index pages contain slot directories. To find a tuple within a page, the engine often scans slot arrays using fixed jump strides before reading record headers.
- **Video Decoding & Streaming**: Video files (e.g., MP4/H.264) place Keyframes (I-frames) at fixed intervals (e.g., every 30 frames). Seeking to frame 75 involves jumping past keyframes at 0, 30, 60, 90, recognizing 90 overshoots, stepping back to 60, and sequentially decoding frames 61 through 75.
- **Sparse Indexing in Big Data Systems**: Apache Kafka and SSTable formats (RocksDB/Cassandra) store sparse index checkpoints every $K$ kilobytes. To read a message offset, the storage layer leaps to the nearest checkpoint and linearly scans consecutive records.
"""

from typing import List, Optional, Sequence, Tuple
import bisect
import math


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATIONS
# ==============================================================================

def jump_search(arr: Sequence[int], target: int) -> int:
    """
    Standard Jump Search (Block Search) Implementation.
    
    Finds the index of `target` in a monotonically sorted sequence `arr`.
    Uses the mathematically optimal block size m = math.isqrt(n).
    
    Args:
        arr (Sequence[int]): A sorted sequence of comparable integers.
        target (int): The value to locate.
        
    Returns:
        int: 0-based index of target if found, else -1.
        
    Complexity:
        Time: O(1) Best, O(sqrt(N)) Average & Worst.
        Space: O(1) Auxiliary space.
    """
    n = len(arr)
    if n == 0:
        return -1
    
    # Calculate optimal jump step size: m = floor(sqrt(n))
    # Using max(1, ...) ensures non-zero step for single-element arrays
    step = max(1, math.isqrt(n))
    prev = 0
    
    # Phase 1: Jump forward in blocks of size 'step'
    # Check the boundary element of each block: arr[min(step, n) - 1]
    while arr[min(step, n) - 1] < target:
        prev = step
        step += max(1, math.isqrt(n))
        if prev >= n:
            return -1
            
    # Phase 2: Perform linear search within the identified block [prev, min(step, n))
    while arr[prev] < target:
        prev += 1
        # If we reach the end of the block or end of array without finding target
        if prev == min(step, n):
            return -1
            
    # Check if the element at prev matches the target
    if arr[prev] == target:
        return prev
        
    return -1


def jump_search_with_trace(
    arr: Sequence[int], 
    target: int
) -> Tuple[int, List[str]]:
    """
    Instrumented Jump Search returning execution diagnostic traces.
    
    Logs every block jump and linear comparison, serving as a pedagogical tool.
    
    Args:
        arr (Sequence[int]): Sorted sequence of integers.
        target (int): Value to search for.
        
    Returns:
        Tuple[int, List[str]]: (found_index_or_-1, trace_logs)
    """
    traces: List[str] = []
    n = len(arr)
    if n == 0:
        traces.append("Array is empty. Immediate termination.")
        return -1, traces
    
    step = max(1, math.isqrt(n))
    prev = 0
    traces.append(f"Initialized Jump Search: N={n}, Jump Size m={step}")
    
    # Phase 1: Jumping
    jump_count = 0
    while arr[min(step, n) - 1] < target:
        jump_count += 1
        check_idx = min(step, n) - 1
        traces.append(
            f"[Phase 1: Jump {jump_count}] Checked index {check_idx} (value {arr[check_idx]}). "
            f"{arr[check_idx]} < {target}. Leaping forward."
        )
        prev = step
        step += max(1, math.isqrt(n))
        if prev >= n:
            traces.append(f"[Phase 1] prev ({prev}) >= N ({n}). Target is greater than all elements.")
            return -1, traces
            
    check_idx = min(step, n) - 1
    traces.append(
        f"[Phase 1: Bounded] Checked index {check_idx} (value {arr[check_idx]}). "
        f"{arr[check_idx]} >= {target}. Target bounded in index range [{prev}, {min(step, n) - 1}]."
    )
    
    # Phase 2: Linear Scan
    scan_step = 0
    while arr[prev] < target:
        scan_step += 1
        traces.append(
            f"[Phase 2: Linear Scan {scan_step}] Checked index {prev} (value {arr[prev]}). "
            f"{arr[prev]} < {target}. Advancing pointer."
        )
        prev += 1
        if prev == min(step, n):
            traces.append(f"[Phase 2] Exhausted block without finding target {target}.")
            return -1, traces
            
    if arr[prev] == target:
        traces.append(f"[Phase 2: Success] Found target {target} at index {prev}!")
        return prev, traces
        
    traces.append(f"[Phase 2: Failure] Element at index {prev} is {arr[prev]} > {target}. Target absent.")
    return -1, traces


# ==============================================================================
# 2. TWO-LEVEL HIERARCHICAL JUMP SEARCH
# ==============================================================================

def two_level_jump_search(arr: Sequence[int], target: int) -> int:
    """
    Two-Level Hierarchical Jump Search.
    
    Applies two tiers of block leaping before the localized linear scan:
    - Tier 1: Leaps by primary blocks of size ~ n^(2/3).
    - Tier 2: Leaps by secondary sub-blocks of size ~ n^(1/3).
    - Tier 3: Linear scan within final sub-block of size ~ n^(1/3).
    
    Achieves O(n^(1/3)) worst-case comparison complexity.
    
    Args:
        arr (Sequence[int]): Sorted sequence of integers.
        target (int): Value to search for.
        
    Returns:
        int: 0-based index of target if found, else -1.
    """
    n = len(arr)
    if n == 0:
        return -1
    
    # Compute block sizes: primary = n^(2/3), secondary = n^(1/3)
    secondary_size = max(1, int(math.pow(n, 1/3)))
    primary_size = max(secondary_size, int(math.pow(n, 2/3)))
    
    # Tier 1: Primary Jumps
    p_prev = 0
    p_step = primary_size
    while p_step < n and arr[p_step - 1] < target:
        p_prev = p_step
        p_step += primary_size
    p_end = min(p_step, n)
    
    # Tier 2: Secondary Jumps within [p_prev, p_end)
    s_prev = p_prev
    s_step = s_prev + secondary_size
    while s_step < p_end and arr[s_step - 1] < target:
        s_prev = s_step
        s_step += secondary_size
    s_end = min(s_step, p_end)
    
    # Tier 3: Local Linear Scan within [s_prev, s_end)
    for idx in range(s_prev, s_end):
        if arr[idx] == target:
            return idx
        if arr[idx] > target:
            return -1
            
    return -1


# ==============================================================================
# 3. INDUSTRY-STANDARD / PRODUCTION EQUIVALENT (BISECT)
# ==============================================================================

def binary_search_bisect(arr: Sequence[int], target: int) -> int:
    """
    Industry-standard baseline using Python's standard library `bisect`.
    
    In general in-memory software engineering, Binary Search is preferred over
    Jump Search due to O(log N) complexity. This serves as a comparative benchmark.
    
    Args:
        arr (Sequence[int]): Sorted sequence of integers.
        target (int): Value to locate.
        
    Returns:
        int: Index if found, else -1.
    """
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DEBUGGING COMMENTARY
# ==============================================================================

def jump_search_buggy_index_out_of_bounds(arr: Sequence[int], target: int) -> int:
    """
    BUGGY IMPLEMENTATION #1: Unclamped Step Indexing.
    
    This implementation fails to clamp `step` with `min(step, n)` when checking
    the block boundary `arr[step - 1]`.
    
    Diagnostic Analysis:
    - Failing Case: arr = [1, 2, 3, 4, 5], target = 10 (n=5, step=2)
    - Trace: 
      Iteration 1: check arr[1]=2 < 10. prev=2, step=4.
      Iteration 2: check arr[3]=4 < 10. prev=4, step=6.
      Iteration 3: evaluates arr[6 - 1] -> arr[5] -> IndexError: list index out of range!
    - Resolution: Always use `arr[min(step, n) - 1]` to safely bound the leap.
    """
    n = len(arr)
    if n == 0:
        return -1
    step = int(math.sqrt(n))
    prev = 0
    # BUG: step is not clamped to n!
    while arr[step - 1] < target:  # <- Raises IndexError when step > n!
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return -1


def jump_search_buggy_zero_step(arr: Sequence[int], target: int) -> int:
    """
    BUGGY IMPLEMENTATION #2: Zero-Step Infinite Loop on Small Arrays.
    
    For n < 4, `int(math.sqrt(n))` can evaluate to 0 (e.g. For empty arrays or if n < 1).
    Even for n = 1, `math.isqrt(1) = 1`, but if someone computes `step = int(math.sqrt(n) * 0.5)`
    or fails to guard step against 0, `step` increments by 0 repeatedly.
    
    Diagnostic Analysis:
    - Failing Case: Empty list or unvalidated step size = 0.
    - Trace: `step += 0` causes while condition to never progress -> Infinite Loop / Hang!
    - Resolution: Ensure step size is strictly at least 1 using `max(1, math.isqrt(n))`.
    """
    n = len(arr)
    if n == 0:
        return -1
    step = 0  # <- Simulated flawed step calculation
    prev = 0
    # Guarding against hanging the test suite: we break if step == 0 to illustrate the bug
    if step == 0:
        # If left unhandled: while arr[min(step, n) - 1] < target: step += 0 -> HANGS FOREVER!
        return -999  # Flag representing fatal zero-step flaw
    return -1


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite executing assert validations on all Jump Search variants.
    """
    print(">>> Running Jump Search Test Suite...")
    
    # Test Datasets
    empty_list: List[int] = []
    single_element_list: List[int] = [42]
    two_element_list: List[int] = [10, 20]
    fibonacci_arr: List[int] = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    dense_arr: List[int] = list(range(0, 1000, 3))  # 334 elements
    
    # 1. Standard Jump Search Tests
    assert jump_search(fibonacci_arr, 55) == 10, "Failed to find middle element 55"
    assert jump_search(fibonacci_arr, 0) == 0, "Failed to find first element (best case)"
    assert jump_search(fibonacci_arr, 610) == 15, "Failed to find last element"
    assert jump_search(fibonacci_arr, 100) == -1, "Failed on missing element between values"
    assert jump_search(fibonacci_arr, -5) == -1, "Failed on element smaller than minimum"
    assert jump_search(fibonacci_arr, 999) == -1, "Failed on element larger than maximum"
    assert jump_search(empty_list, 10) == -1, "Failed on empty list"
    assert jump_search(single_element_list, 42) == 0, "Failed on matching single-element list"
    assert jump_search(single_element_list, 99) == -1, "Failed on missing single-element list"
    assert jump_search(two_element_list, 10) == 0, "Failed on two-element list first item"
    assert jump_search(two_element_list, 20) == 1, "Failed on two-element list second item"
    assert jump_search(two_element_list, 15) == -1, "Failed on two-element list missing item"
    
    # 2. Dense Array & Exhaustive Validation
    for expected_idx, val in enumerate(dense_arr):
        res = jump_search(dense_arr, val)
        assert res == expected_idx, f"Exhaustive test failed for value {val} at index {expected_idx}"
    assert jump_search(dense_arr, 4) == -1, "Failed on absent value in dense array"
    
    # 3. Two-Level Hierarchical Jump Search Tests
    assert two_level_jump_search(fibonacci_arr, 55) == 10, "Two-level failed on 55"
    assert two_level_jump_search(fibonacci_arr, 0) == 0, "Two-level failed on first element"
    assert two_level_jump_search(fibonacci_arr, 610) == 15, "Two-level failed on last element"
    assert two_level_jump_search(fibonacci_arr, 100) == -1, "Two-level failed on missing element"
    assert two_level_jump_search(empty_list, 5) == -1, "Two-level failed on empty list"
    for expected_idx, val in enumerate(dense_arr):
        res = two_level_jump_search(dense_arr, val)
        assert res == expected_idx, f"Two-level dense test failed for {val}"
        
    # 4. Instrumented Trace Verification
    idx, trace_logs = jump_search_with_trace(fibonacci_arr, 55)
    assert idx == 10, "Traced jump search failed to find index 10"
    assert len(trace_logs) > 0, "Traced search failed to generate log entries"
    
    # 5. Comparative Bisect Baseline Tests
    assert binary_search_bisect(fibonacci_arr, 55) == 10
    assert binary_search_bisect(fibonacci_arr, 100) == -1
    
    # 6. Buggy Implementations Diagnostic Verification
    # Buggy index out of bounds raises IndexError on out-of-range target
    try:
        jump_search_buggy_index_out_of_bounds([1, 2, 3, 4, 5], 10)
        raised = False
    except IndexError:
        raised = True
    assert raised is True, "Expected buggy unclamped search to raise IndexError"
    
    # Buggy zero step returns indicator
    assert jump_search_buggy_zero_step([1, 2, 3], 2) == -999, "Expected zero-step bug detection"
    
    print("[+] All Jump Search test suites passed successfully!")


# ==============================================================================
# 6. MAIN DRIVER & VISUAL EDUCATIONAL TRACES
# ==============================================================================

def main() -> None:
    """
    Main driver executing unit tests and displaying step-by-step diagnostic traces.
    """
    run_tests()
    
    print("\n" + "=" * 75)
    print("EDUCATIONAL TRACE: JUMP SEARCH IN ACTION")
    print("=" * 75)
    
    demo_arr = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    target_val = 55
    
    print(f"Target Value : {target_val}")
    print(f"Sorted Array : {demo_arr}")
    print(f"Array Size N : {len(demo_arr)}")
    print(f"Jump Size m  : floor(sqrt({len(demo_arr)})) = {math.isqrt(len(demo_arr))}")
    print("-" * 75)
    
    idx, trace_logs = jump_search_with_trace(demo_arr, target_val)
    for line in trace_logs:
        print(f" -> {line}")
        
    print("-" * 75)
    print(f"Final Result : Target {target_val} located at index {idx}.")
    print("=" * 75)


if __name__ == "__main__":
    main()
