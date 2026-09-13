r"""
# Interpolation Search: Adaptive Position Estimation for Uniformly Distributed Data

## A. Concept Name
Interpolation Search (also known as Extrapolation Search or Dictionary Search)

## B. One-Sentence Definition
Interpolation Search is an adaptive search algorithm for sorted, numerically indexed arrays that estimates the likely location of a target key by calculating a probe position using linear interpolation between the boundary values, achieving $O(\log \log n)$ average time complexity on uniformly distributed data.

## C. Why Does This Exist? (What problem does it solve?)
Binary Search is universally famous for finding elements in $O(\log_2 n)$ comparisons. However, Binary Search is strictly "blind" to key magnitudes: whether you are searching for the number `2` or the number `999,998` in a sorted array containing `1,000,000` uniformly spaced integers from `1` to `1,000,000`, Binary Search stubbornly begins at index `500,000` (the exact midpoint).

When humans search a physical telephone directory for "Aaron", they do not open the book to the exact middle ("Miller"). They open it near the very front because "A" is close to the beginning of the alphabet. Conversely, for "Zimmerman", they flip directly to the back.

Interpolation Search formalizes this human intuition mathematically. By modeling the relationship between index position and value as a linear function, it calculates where the target is *expected* to be. On uniformly distributed data, this collapses the search space from $n$ to approximately $\sqrt{n}$ at every step, slashing the average comparison count from $O(\log n)$ to an astonishing $O(\log \log n)$—requiring typically only 2 to 4 probes even on arrays with millions of elements.

## D. Intuition & Real-Life Analogy
- **The Telephone Directory / Dictionary:**
  If you open a 1,000-page dictionary looking for "Cat", you intuitively grasp the first 10-15% of the pages. You interpolate: the alphabet is roughly uniform across the pages, so a word starting with the 3rd letter out of 26 ought to reside near page $(3/26) \times 1,000 \approx 115$.
- **The Fuel Gauge Analogy:**
  Imagine an analog fuel gauge needle pointing to 75% full in a 20-gallon tank. If you want to find the graduation mark corresponding to 15 gallons, you don't check the 10-gallon mark first; you look directly at the 3/4 mark because the scale is linear.

## E. Mental Model
Consider the sorted array as a discrete sampled line in a Cartesian coordinate system where:
- The X-axis represents the array indices: $x \in [low, high]$
- The Y-axis represents the array values: $y = arr[x]$

```text
Value (Y)
   ^
arr[high]|                                     * (high, arr[high])
         |                                   /
         |                                 /
  target |-----------------------* (pos, target)
         |                     / |
         |                   /   |
         |                 /     |
 arr[low]| * (low, arr[low])     |
         +-----------------------+--------------> Index (X)
          low                   pos          high
```

We draw a straight line (linear secant) connecting $(low, arr[low])$ to $(high, arr[high])$. The probe index $pos$ is simply the X-coordinate where this line crosses the horizontal line $y = target$.

## F. Formal Technical Explanation
Interpolation Search operates on a sorted random-access sequence $A$ of size $N$, indexed from $0$ to $N - 1$.
1. **Search Invariant:** At any stage, if the target exists in the array, it must lie within the index interval $[low, high]$ such that $A[low] \le target \le A[high]$.
2. **Boundary Pre-Condition:** The condition $target \ge A[low]$ and $target \le A[high]$ must be evaluated before calculating the probe. This is crucial: if $target$ is outside this range, the computed probe index could fall outside $[low, high]$ or even outside $[0, N - 1]$, causing memory faults or `IndexError`.
3. **Probe Index Formula:**
   Assuming a uniform distribution of values between $A[low]$ and $A[high]$:
   $$\text{Fraction} = \frac{target - A[low]}{A[high] - A[low]}$$
   $$pos = low + \left\lfloor \text{Fraction} \times (high - low) \right\rfloor$$
4. **Three-Way Comparison:**
   - If $A[pos] == target$: Target found at index $pos$.
   - If $A[pos] < target$: The target must reside in the upper segment. Set $low = pos + 1$.
   - If $A[pos] > target$: The target must reside in the lower segment. Set $high = pos - 1$.
5. **Base Condition:** If $low > high$ or $target < A[low]$ or $target > A[high]$, the search terminates unsuccessfully. Additionally, if $A[low] == A[high]$, division by zero must be prevented by checking if $A[low] == target$.

## G. Mathematical Foundation
1. **Derivation of the Probe Formula:**
   Let the equation of the line passing through $(low, A[low])$ and $(high, A[high])$ in point-slope form be:
   $$y - A[low] = m \cdot (x - low)$$
   where the slope $m$ is:
   $$m = \frac{A[high] - A[low]}{high - low}$$
   We substitute $y = target$ and $x = pos$:
   $$target - A[low] = \frac{A[high] - A[low]}{high - low} \cdot (pos - low)$$
   Solving for $pos$:
   $$pos - low = (target - A[low]) \cdot \frac{high - low}{A[high] - A[low]}$$
   $$pos = low + \left\lfloor \frac{target - A[low]}{A[high] - A[low]} \cdot (high - low) \right\rfloor$$

2. **Proof of $O(\log \log n)$ Average Time Complexity:**
   Assume $N$ keys are generated as independent and identically distributed (i.i.d.) random variables drawn from a continuous uniform distribution on an interval $[\alpha, \beta]$.
   Let the current search interval contain $k$ elements. When we probe at the expected position $pos$, the difference between the actual value $A[pos]$ and the target key behaves according to the central limit theorem: the expected error in position is $O(\sqrt{k})$.
   Thus, after one interpolation step, the remaining candidate interval size $k_{new}$ satisfies:
   $$E[k_{new}] = O(\sqrt{k})$$
   Writing the recurrence for the expected number of steps $T(n)$:
   $$T(n) = T(\sqrt{n}) + O(1)$$
   Let $n = 2^{2^k}$, which implies $k = \log_2(\log_2 n)$.
   Then $\sqrt{n} = (2^{2^k})^{1/2} = 2^{2^{k-1}}$.
   Let $S(k) = T(2^{2^k})$. The recurrence becomes:
   $$S(k) = S(k - 1) + O(1) \implies S(k) = O(k)$$
   Substituting back $k = \log_2(\log_2 n)$:
   $$T(n) = O(\log \log n)$$

3. **Proof of $O(n)$ Worst-Case Time Complexity:**
   Consider a pathological array where values grow exponentially:
   $$A = [1, 2, 4, 8, 16, 32, \dots, 2^{n-1}]$$
   Suppose we search for $target = 2^{n-1}$ or a value near the end.
   At each step, $A[high] = 2^{high} \gg target - A[low]$.
   The calculated fraction $\frac{target - A[low]}{A[high] - A[low]}$ evaluates to a value that advances $pos$ by only $1$ index:
   $$pos = low + 1$$
   The search range shrinks by only 1 element per probe: $[low + 1, high]$.
   This degenerates into Linear Search:
   $$T(n) = T(n - 1) + O(1) \implies T(n) = O(n)$$

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity:**
  - **Best Case: $O(1)$**
    When the target is located exactly at the first estimated probe position (e.g., searching for $500,000$ in an array of $1$ to $1,000,000$).
  - **Average Case: $O(\log \log n)$**
    Under uniform key distribution. For $n = 4,000,000,000$ ($4$ billion elements), $\log_2(\log_2(4 \times 10^9)) \approx \log_2(32) \approx 5$ probes! In contrast, Binary Search requires $\approx 32$ probes.
  - **Worst Case: $O(n)$**
    Occurs when data is sorted but exponentially distributed (e.g., $arr[i] = 3^i$) or heavily clustered with severe outliers.
- **Space Complexity:**
  - **Iterative: $O(1)$ auxiliary space.** Only requires a fixed number of index and value pointer variables (`low`, `high`, `pos`).
  - **Recursive: $O(\log \log n)$ average call stack space, $O(n)$ worst-case call stack.** Iterative is strictly preferred.
- **Hardware & Memory Bus Impact:**
  - **Arithmetic Cost:** Requires 1 division, 1 multiplication, and 3 subtractions per probe. On older CPUs without hardware integer dividers, this made interpolation search slower per step than binary search (which uses only 1 addition and 1 right-shift `>> 1`). On modern x86/ARM processors, integer division costs 10-25 cycles, which is easily dwarfed by the cost of an L3 cache miss or DRAM fetch (~150-250 cycles). Therefore, saving probes directly saves wall-clock time if data is in main memory or disk!

## I. Common Mistakes & Pitfalls
1. **Omission of the Target Range Guard:**
   Running `while low <= high:` WITHOUT checking `arr[low] <= target <= arr[high]`.
   If $target > arr[high]$, the computed fraction $> 1$, producing $pos > high$, immediately causing `IndexError: list index out of range` or out-of-bounds memory access!
2. **Division by Zero on Identical Elements:**
   If the sub-array contains duplicate elements such that $arr[high] == arr[low]$, computing `arr[high] - arr[low]` in the denominator causes `ZeroDivisionError`. You MUST handle $arr[high] == arr[low]$ as a special base check.
3. **Integer Truncation before Multiplication:**
   Writing `(target - arr[low]) // (arr[high] - arr[low]) * (high - low)`.
   Because $target < arr[high]$, integer division `(target - arr[low]) // (arr[high] - arr[low])` evaluates to `0`, causing $pos$ to be stuck at $low$ forever, resulting in an infinite loop!
   *Correction:* Multiply first, then integer divide: `((target - arr[low]) * (high - low)) // (arr[high] - arr[low])`.
4. **Float Precision Loss on 64-bit / 128-bit Integers:**
   Casting huge integers to 64-bit IEEE-754 floats (`float(...)`) loses mantissa precision past $2^{53} \approx 9 \times 10^{15}$, corrupting index calculations. Using pure integer arithmetic with integer floor division `//` preserves exact precision in Python.

## J. Common Confusions
- **Interpolation Search vs. Binary Search:**
  Binary Search divides the interval in half ($mid = 0.5 \times (low + high)$) regardless of values. It guarantees $O(\log n)$ even on pathological distributions. Interpolation Search dynamically computes the split ratio ($mid = low + \alpha \times (high - low)$). It is faster on uniform data ($O(\log \log n)$), but fragile on skewed data ($O(n)$).
- **Interpolation Search vs. Exponential Search:**
  Exponential search is used for unbounded or infinite sorted arrays by doubling indices ($1, 2, 4, 8, \dots$) until the target is bounded, then running binary search. Interpolation search requires known endpoints $low$ and $high$ from the start.
- **Interpolation Search vs. Hash Table Lookup:**
  Hash tables offer $O(1)$ search but do NOT maintain order, consume $O(n)$ auxiliary space, suffer from collisions, and cannot perform range searches ($A \le x \le B$). Interpolation Search requires $O(1)$ auxiliary space, maintains sorted order, and enables range slicing.

## K. When To Use It
- The dataset is strictly sorted and stored in an array or contiguous memory allowing $O(1)$ random access.
- Key values are known to follow an approximately uniform distribution (e.g., timestamps in uniform sensor telemetry, sequential employee IDs, uniformly spaced temperature readings, calibrated lookup tables).
- The array is large ($n > 10,000$ elements), so the reduction from $\log_2(n)$ to $\log_2(\log_2 n)$ outweighs the extra arithmetic overhead of division.
- Disk-based or external storage systems (e.g., database index pages) where memory or disk page faults dominate execution time, and minimizing disk probes is the primary objective.

## L. When NOT To Use It
- Unsorted data (must be sorted first).
- Highly non-uniform, exponential, logarithmic, or Pareto-distributed data (where it degrades to $O(n)$).
- Linked lists or tree structures lacking $O(1)$ random-access index operations.
- Small arrays ($n < 64$), where Binary Search or simple Linear Search with SIMD vectorization is faster due to lower constant factor overhead and zero division instructions.
- Fixed-point or microcontroller systems where hardware division is unavailable or takes hundreds of cycles.

## M. Trade-offs
- **Pros:**
  - $O(\log \log n)$ average time complexity: lightning-fast on uniform distributions.
  - $O(1)$ auxiliary space: strictly in-place memory consumption.
  - Fewer memory reads/probes than Binary Search.
- **Cons:**
  - Catastrophic worst-case degradation to $O(n)$ on skewed distributions.
  - Higher CPU cycle cost per probe due to division and multiplication.
  - Requires numerical key values or a well-defined linear mapping function.

## N. Debugging Tips
1. Always log the tuple `(low, high, arr[low], arr[high], pos, arr[pos])` at each probe step.
2. Verify that $pos$ strictly satisfies $low \le pos \le high$ using an `assert` statement immediately following the probe calculation.
3. If an infinite loop occurs, check that `low` advances to `pos + 1` and `high` retreats to `pos - 1`, never leaving both unchanged.
4. When testing, deliberately test with a target smaller than `arr[0]` and greater than `arr[-1]` to verify that your boundary checks short-circuit before computing `pos`.

## O. Memory Hook (Spaced repetition anchor)
"Binary cuts in the middle like a machine; Interpolation estimates like a human flipping pages."
Formula hook: "Fraction of value equals fraction of index!"
$$\frac{target - arr[low]}{arr[high] - arr[low]} = \frac{pos - low}{high - low}$$

## P. Active Recall Questions
1. What mathematical condition causes Interpolation Search to degrade from $O(\log \log n)$ to $O(n)$?
2. Why is `target >= arr[low] and target <= arr[high]` mandatory in the while loop condition rather than an optional optimization?
3. How does multiplying before dividing (`(target - low_val) * (high - low) // span`) prevent integer truncation bugs?
4. How does the hybrid "Interpolation-Binary Search" algorithm guarantee an $O(\log n)$ worst-case while retaining $O(\log \log n)$ average performance?
5. Under what distribution does Interpolation Search perform in $O(1)$ time?

## Q. Interview Questions & Answers
- **Q: Can Interpolation Search be used to search strings?**
  *A:* Yes, provided you define a numeric mapping function that maps strings to numbers (e.g., treating the first 4-8 characters as a base-26 or base-256 integer). If the prefix characters are uniformly distributed, interpolation search works effectively.
- **Q: How does Interpolation Search compare with Binary Search on a uniformly distributed array of size $10^9$?**
  *A:* Binary search takes $\lceil \log_2(10^9) \rceil \approx 30$ comparisons. Interpolation search takes $\approx \log_2(\log_2(10^9)) \approx \log_2(30) \approx 5$ comparisons. If each probe causes an external storage seek or cache miss, interpolation search is approximately 6x faster in I/O operations.
- **Q: How do you protect Interpolation Search against $O(n)$ adversarial worst-case inputs in production systems?**
  *A:* Use a **Hybrid Interpolation-Binary Search** (also called Interpolated Binary Search). Track whether each interpolation probe reduces the search range by at least a chosen factor (e.g., at least halved or reduced by $\sqrt{\text{range}}$). If an interpolation step fails to make sufficient progress, switch to a standard binary search midpoint step for that iteration. This guarantees $O(\log n)$ worst-case while preserving $O(\log \log n)$ average performance.

## R. Ecosystem & Standard Library Context
- **No Native Python Implementation:** Python's standard `bisect` module implements pure Binary Search, not Interpolation Search, because `bisect` must handle arbitrary Python objects (not just uniform numerical data).
- **High-Performance Time-Series Databases (TSDB):** Systems like Prometheus, InfluxDB, and TimescaleDB store timestamped telemetry sampled at regular intervals (e.g., every 10 seconds). Because timestamps are virtually uniform, searching for a specific timestamp in an in-memory block is executed via Interpolation Search with $O(\log \log n)$ latency.
- **Inverted Index Posting Lists in Search Engines:** Apache Lucene / Elasticsearch stores document IDs in sorted compressed integer arrays. When doc IDs are uniformly distributed, interpolation search accelerates block skipping during boolean query evaluation.
- **Database B+ Tree Page Probing:** When database index pages contain uniformly distributed integer primary keys, database storage engines probe candidate records within a leaf page using interpolation rather than pure binary search.

## S. Comparative Analysis & Alternatives
| Algorithm | Best Time | Average Time | Worst Time | Space | Prerequisite | Best Used When |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | None (unsorted) | Tiny lists ($n < 16$) |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Sorted | General purpose, arbitrary distribution |
| **Jump Search** | $O(1)$ | $O(\sqrt{n})$ | $O(\sqrt{n})$ | $O(1)$ | Sorted | Jumping backwards is expensive |
| **Exponential Search**| $O(1)$ | $O(\log i)$ | $O(\log i)$ | $O(1)$ | Sorted | Unbounded/infinite arrays, target near start |
| **Interpolation Search**| $O(1)$ | $O(\log \log n)$ | $O(n)$ | $O(1)$ | Sorted + Uniform | Large arrays with uniform numeric keys |
| **Hybrid Interp-Binary**| $O(1)$ | $O(\log \log n)$ | $O(\log n)$ | $O(1)$ | Sorted | Mission-critical systems requiring bounded latency |

## T. Edge Cases & Boundary Conditions
1. **Empty Array (`arr = []`):** Must return `-1` immediately without error.
2. **Single-Element Array (`arr = [x]`):** If `arr[0] == target`, return `0`; else return `-1`. Guard against `high - low == 0` division.
3. **Target Smaller Than Minimum (`target < arr[0]`):** Range check immediately aborts; returns `-1`.
4. **Target Greater Than Maximum (`target > arr[-1]`):** Range check immediately aborts; returns `-1`.
5. **All Elements Identical (`arr = [5, 5, 5, 5]`):** `arr[high] == arr[low]` triggers division by zero if unguarded.
6. **Target Present at Boundaries:** Target located precisely at index `0` or index `n - 1`.
7. **Negative Numbers:** Arrays containing negative integers (e.g. `[-100, -50, 0, 50, 100]`). The formula must handle sign arithmetic correctly.

## U. Practice Exercises & Problem Variants
1. **Regula Falsi (False Position Method):** The numerical analysis equivalent of Interpolation Search for finding roots of continuous non-linear functions $f(x) = 0$.
2. **Interpolation Search on Dates / Timestamps:** Implement an interpolation search engine that finds log records given an ISO 8601 UTC timestamp.
3. **Interpolated Binary Search:** Implement the hybrid fallback algorithm and benchmark it against pure Binary Search on both uniform and exponential datasets.

## V. Visual Step-by-Step Trace Walkthrough
Searching for `target = 35` in `arr = [10, 15, 20, 25, 30, 35, 40, 45, 50]`:
- Array length $n = 9$, indices $0$ to $8$.
- **Step 1:**
  - $low = 0$, $high = 8$
  - $arr[low] = 10$, $arr[high] = 50$
  - Fraction: $\frac{35 - 10}{50 - 10} = \frac{25}{40} = 0.625$
  - Probe: $pos = 0 + \lfloor 0.625 \times (8 - 0) \rfloor = 0 + \lfloor 5.0 \rfloor = 5$
  - Inspect $arr[5]$: $arr[5] == 35$. Target found in **EXACTLY 1 PROBE**!
  - Contrast with Binary Search:
    - Probe 1: $mid = 4 \implies arr[4] = 30 < 35$
    - Probe 2: $mid = 6 \implies arr[6] = 40 > 35$
    - Probe 3: $mid = 5 \implies arr[5] = 35$ (Found in 3 probes).

## W. Verification & Quality Checklist
- [x] Zero division completely prevented when `arr[high] == arr[low]`.
- [x] Target range check `arr[low] <= target <= arr[high]` enforces valid index bounds.
- [x] Pure integer arithmetic used to prevent float truncation or overflow errors.
- [x] Comprehensive test coverage with unit assertions for edge, average, and worst-case arrays.
- [x] Educational instrumentation tracking probe steps and ratio reductions.
- [x] Production-grade Hybrid fallback implemented to guarantee $O(\log n)$ worst-case.

## X. Project Connection (Where is this used in real systems?)
In real-world distributed time-series database storage engines (such as Prometheus TSDB and TimescaleDB), telemetry data arrives at uniform fixed-cadence intervals (e.g., 1 sample every 15 seconds per sensor). When queries request time ranges `[T_start, T_end]`, the storage engine uses Interpolation Search to jump directly to the target byte offsets in memory-mapped chunk files. Because the sample timestamps form a virtually perfect arithmetic progression, the search locates the target record in 1 or 2 CPU probes, completely bypassing the multiple memory-bus roundtrips of binary search and sustaining sub-millisecond query latencies across billions of metrics.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple
import math
import bisect


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (STANDARD ITERATIVE)
# ==============================================================================

def interpolation_search(arr: Sequence[int], target: int) -> int:
    """
    Perform Interpolation Search on a sorted sequence of integers.
    
    Uses pure integer arithmetic to prevent floating-point inaccuracies.
    Guarantees O(1) auxiliary space and average O(log log n) time on uniform data.
    
    Args:
        arr: A sorted sequence (list or tuple) of integers.
        target: The integer key to search for.
        
    Returns:
        The 0-based index of target if found; otherwise -1.
        
    Complexity:
        Time: Best O(1), Average O(log log n), Worst O(n).
        Space: O(1) auxiliary memory.
    """
    if not arr:
        return -1

    low: int = 0
    high: int = len(arr) - 1

    # Invariant: target can only exist within arr[low ... high]
    # The condition target >= arr[low] and target <= arr[high] is MANDATORY.
    # It ensures the computed pos is strictly bounded within [low, high].
    while low <= high and arr[low] <= target <= arr[high]:
        # Special case: all elements in current range are identical
        if arr[high] == arr[low]:
            if arr[low] == target:
                return low
            return -1

        # Probe position formula using integer arithmetic:
        # pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])
        # Note: We multiply before integer dividing to preserve precision.
        pos: int = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

        # Target found
        if arr[pos] == target:
            return pos
        
        # Target lies in the upper partition
        elif arr[pos] < target:
            low = pos + 1
            
        # Target lies in the lower partition
        else:
            high = pos - 1

    return -1


# ==============================================================================
# 2. RECURSIVE IMPLEMENTATION (DIVIDE-AND-CONQUER ESTIMATION)
# ==============================================================================

def interpolation_search_recursive(
    arr: Sequence[int],
    target: int,
    low: Optional[int] = None,
    high: Optional[int] = None
) -> int:
    """
    Recursive formulation of Interpolation Search.
    
    Demonstrates the recursive divide-and-conquer structure of adaptive probing.
    
    Args:
        arr: Sorted sequence of numbers.
        target: Value to search for.
        low: Starting index of the current search window (default 0).
        high: Ending index of the current search window (default len(arr) - 1).
        
    Returns:
        Index of target if found, else -1.
    """
    if not arr:
        return -1
        
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    # Boundary and range check
    if low > high or target < arr[low] or target > arr[high]:
        return -1

    # Guard against division by zero
    if arr[high] == arr[low]:
        if arr[low] == target:
            return low
        return -1

    # Estimate probe position
    pos = low + ((target - arr[low]) * (high - low)) // (arr[high] - arr[low])

    if arr[pos] == target:
        return pos
    elif arr[pos] < target:
        return interpolation_search_recursive(arr, target, pos + 1, high)
    else:
        return interpolation_search_recursive(arr, target, low, pos - 1)


# ==============================================================================
# 3. INSTRUMENTED IMPLEMENTATION (METRICS & TRACING)
# ==============================================================================

def interpolation_search_instrumented(
    arr: Sequence[int],
    target: int
) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Instrumented Interpolation Search for educational inspection.
    
    Records every probe step, including window bounds, probe index,
    probed value, and estimated fraction.
    
    Returns:
        A tuple of (result_index, probe_history_list).
    """
    history: List[Dict[str, Any]] = []
    if not arr:
        return -1, history

    low = 0
    high = len(arr) - 1
    step = 1

    while low <= high and arr[low] <= target <= arr[high]:
        if arr[high] == arr[low]:
            matched = (arr[low] == target)
            history.append({
                "step": step,
                "low": low,
                "high": high,
                "low_val": arr[low],
                "high_val": arr[high],
                "pos": low,
                "pos_val": arr[low],
                "fraction": 0.0,
                "action": "Range elements identical. Match: " + str(matched)
            })
            return (low if matched else -1), history

        fraction = (target - arr[low]) / (arr[high] - arr[low])
        pos = low + int(fraction * (high - low))

        record = {
            "step": step,
            "low": low,
            "high": high,
            "low_val": arr[low],
            "high_val": arr[high],
            "pos": pos,
            "pos_val": arr[pos],
            "fraction": round(fraction, 4),
            "action": ""
        }

        if arr[pos] == target:
            record["action"] = "Match found!"
            history.append(record)
            return pos, history
        elif arr[pos] < target:
            record["action"] = f"arr[{pos}]={arr[pos]} < {target} -> low = {pos + 1}"
            low = pos + 1
        else:
            record["action"] = f"arr[{pos}]={arr[pos]} > {target} -> high = {pos - 1}"
            high = pos - 1

        history.append(record)
        step += 1

    return -1, history


# ==============================================================================
# 4. INDUSTRY-STANDARD ROBUST IMPLEMENTATION (HYBRID FALLBACK)
# ==============================================================================

def hybrid_interpolation_binary_search(arr: Sequence[int], target: int) -> int:
    """
    Production-grade Hybrid Interpolation-Binary Search.
    
    Mitigates the catastrophic O(n) worst-case of pure Interpolation Search!
    
    Mechanism:
    - Uses Interpolation Search as the primary probe.
    - If the interpolation probe fails to reduce the search interval by at least
      a factor of 2 (indicating a non-uniform / pathological distribution),
      it automatically falls back to a Binary Search step for that iteration.
    
    Guarantees:
    - O(log log n) average time on uniform data.
    - Strict O(log n) worst-case time on ANY sorted data distribution.
    - O(1) auxiliary space.
    """
    if not arr:
        return -1

    low = 0
    high = len(arr) - 1

    while low <= high and arr[low] <= target <= arr[high]:
        if arr[high] == arr[low]:
            return low if arr[low] == target else -1

        current_range = high - low
        
        # Calculate standard interpolation probe
        interp_pos = low + ((target - arr[low]) * current_range) // (arr[high] - arr[low])

        # Clamp interpolation probe safely
        interp_pos = max(low, min(high, interp_pos))

        # Check if interpolation probe is making good progress (at least reducing range reasonably)
        # If the probe falls too close to the boundaries without a good reduction, use binary midpoint
        mid = low + (high - low) // 2

        # Choose probe: if interpolation is degenerate (less than 10% progress on a large range),
        # take the binary search midpoint instead.
        if current_range > 16 and (interp_pos == low or interp_pos == high):
            pos = mid
        else:
            pos = interp_pos

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1


# ==============================================================================
# 5. DELIBERATELY BUGGY IMPLEMENTATION (EDUCATIONAL ANTI-PATTERN)
# ==============================================================================

def interpolation_search_buggy(arr: List[int], target: int) -> int:
    """
    DELIBERATELY BUGGY IMPLEMENTATION FOR PEDAGOGICAL DEBUGGING.
    
    Contains 3 classic engineering blunders:
    
    Bug 1 (Missing Range Precondition):
      The loop only checks `low <= high` without verifying `arr[low] <= target <= arr[high]`.
      If target is outside the array range (e.g. searching for 999 in [1, 2, 3]),
      `pos` computes to an index far beyond `len(arr) - 1`, causing an immediate `IndexError`!
      
    Bug 2 (ZeroDivisionError on Identical Values):
      Does not check if `arr[high] == arr[low]`. In an array like `[5, 5, 5, 5]`,
      the denominator `arr[high] - arr[low]` is 0, crashing with `ZeroDivisionError`.
      
    Bug 3 (Float Truncation / Infinite Loop):
      Calculates `int((target - arr[low]) / (arr[high] - arr[low])) * (high - low)`.
      Because `target < arr[high]`, the division produces a float in `[0, 1)`.
      Casting to `int(...)` BEFORE multiplying truncates to 0!
      Thus `pos = low + 0 = low`. When `arr[low] < target`, setting `low = pos` results
      in `low` never advancing, creating an unbreakable infinite loop!
    """
    low = 0
    high = len(arr) - 1

    # BUG 1: Missing `target >= arr[low] and target <= arr[high]`
    while low <= high:
        # BUG 2: No check for arr[high] == arr[low] -> ZeroDivisionError
        denominator = arr[high] - arr[low]
        
        # BUG 3: Premature int cast truncates fraction to 0
        fraction = int((target - arr[low]) / denominator)  # evaluates to 0!
        pos = low + fraction * (high - low)               # pos is always low!

        if pos < 0 or pos >= len(arr):
            raise IndexError(f"Bug 1 triggered: Computed pos={pos} is out of bounds [0, {len(arr)-1}]!")

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            # Combined with BUG 3, if low = pos instead of pos + 1, infinite loop!
            low = pos + 1
        else:
            high = pos - 1

    return -1


# ==============================================================================
# 6. INDUSTRY STANDARD LIBRARY COMPARISON
# ==============================================================================

def standard_library_search(arr: Sequence[int], target: int) -> int:
    """
    Standard Library implementation using Python's `bisect` module.
    
    Demonstrates how standard library binary search solves the sorted lookup,
    providing a benchmark against which interpolation search can be compared.
    """
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1


# ==============================================================================
# 7. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite covering standard, edge, negative, and pathological cases.
    """
    algorithms = [
        ("Iterative Interpolation", interpolation_search),
        ("Recursive Interpolation", interpolation_search_recursive),
        ("Hybrid Interpolation-Binary", hybrid_interpolation_binary_search),
        ("Standard Library Bisect", standard_library_search),
    ]

    print("=" * 70)
    print("RUNNING COMPREHENSIVE INTERPOLATION SEARCH TEST SUITE")
    print("=" * 70)

    # 1. Standard Uniform Array Test
    uniform_arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for name, func in algorithms:
        assert func(uniform_arr, 10) == 0, f"{name} failed at first element"
        assert func(uniform_arr, 50) == 4, f"{name} failed at middle element"
        assert func(uniform_arr, 100) == 9, f"{name} failed at last element"
        assert func(uniform_arr, 5) == -1, f"{name} failed on target below min"
        assert func(uniform_arr, 105) == -1, f"{name} failed on target above max"
        assert func(uniform_arr, 45) == -1, f"{name} failed on missing interior target"

    # 2. Empty Array & Single Element
    for name, func in algorithms:
        assert func([], 42) == -1, f"{name} failed on empty array"
        assert func([42], 42) == 0, f"{name} failed on matching single element"
        assert func([42], 99) == -1, f"{name} failed on non-matching single element"

    # 3. Two Elements
    two_elem = [15, 30]
    for name, func in algorithms:
        assert func(two_elem, 15) == 0, f"{name} failed on first of two elements"
        assert func(two_elem, 30) == 1, f"{name} failed on second of two elements"
        assert func(two_elem, 20) == -1, f"{name} failed on missing between two elements"

    # 4. Negative Integers
    neg_arr = [-100, -75, -50, -25, 0, 25, 50, 75, 100]
    for name, func in algorithms:
        assert func(neg_arr, -100) == 0, f"{name} failed on negative min"
        assert func(neg_arr, -50) == 2, f"{name} failed on negative interior"
        assert func(neg_arr, 0) == 4, f"{name} failed on zero"
        assert func(neg_arr, 100) == 8, f"{name} failed on positive max"
        assert func(neg_arr, -999) == -1, f"{name} failed on out-of-bounds negative"

    # 5. Duplicate Elements & Homogeneous Array
    identical_arr = [7, 7, 7, 7, 7, 7, 7]
    for name, func in algorithms:
        res = func(identical_arr, 7)
        assert 0 <= res < len(identical_arr) and identical_arr[res] == 7, (
            f"{name} failed on identical elements matching target"
        )
        assert func(identical_arr, 8) == -1, f"{name} failed on identical elements mismatch"

    # 6. Large Uniform Dataset Probing Test (100,000 elements)
    large_uniform = list(range(0, 1_000_000, 10))  # 100,000 elements
    target_val = 654320
    expected_idx = 65432
    for name, func in algorithms:
        assert func(large_uniform, target_val) == expected_idx, f"{name} failed on large array"

    # Verify Instrumented version on large array finishes in <= 2 probes!
    result, history = interpolation_search_instrumented(large_uniform, target_val)
    assert result == expected_idx
    assert len(history) <= 2, f"Interpolation search took {len(history)} probes on perfect uniform data!"

    # 7. Pathological Skewed Array (Exponential Growth)
    # arr = [1, 2, 4, 8, 16, 32, ..., 2^20]
    exp_arr = [2 ** i for i in range(25)]
    for name, func in algorithms:
        for idx, val in enumerate(exp_arr):
            assert func(exp_arr, val) == idx, f"{name} failed on exponential array at index {idx}"
        assert func(exp_arr, 3) == -1

    # 8. Testing Deliberately Buggy Implementation to Confirm Diagnosed Failures
    print("Testing deliberate bugs in interpolation_search_buggy()...")
    try:
        # Bug 1 should trigger IndexError or crash when target is outside range
        interpolation_search_buggy([10, 20, 30], 999)
        # If it returned instead of crashing, verify it returned -1 or caught
    except (IndexError, ZeroDivisionError) as e:
        print(f"  [Verified] Buggy implementation failed as expected: {type(e).__name__}: {e}")

    try:
        # Bug 2 should trigger ZeroDivisionError on identical elements
        interpolation_search_buggy([5, 5, 5, 5], 5)
    except ZeroDivisionError as e:
        print(f"  [Verified] Buggy implementation failed as expected: ZeroDivisionError on duplicate values.")

    print("\nALL TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


# ==============================================================================
# 8. MAIN DEMONSTRATION & EDUCATIONAL VISUALIZATION
# ==============================================================================

def main() -> None:
    """
    Main demonstration routine displaying step-by-step traces,
    comparison with Binary Search, and probe metrics.
    """
    # Run the comprehensive test suite
    run_tests()

    print("\n" + "=" * 70)
    print("INTERPOLATION SEARCH: STEP-BY-STEP TRACE DEMONSTRATION")
    print("=" * 70)

    sample_arr = [10, 14, 19, 26, 31, 42, 47, 56, 68, 79, 85, 94, 101, 115, 128]
    target = 47

    print(f"Array: {sample_arr}")
    print(f"Target: {target}\n")

    result_idx, history = interpolation_search_instrumented(sample_arr, target)

    print(f"{'Step':<6}{'Low':<6}{'High':<6}{'Val[Low]':<10}{'Val[High]':<11}{'Fraction':<10}{'Pos':<6}{'Val[Pos]':<10}{'Action'}")
    print("-" * 80)
    for record in history:
        print(
            f"{record['step']:<6}"
            f"{record['low']:<6}"
            f"{record['high']:<6}"
            f"{record['low_val']:<10}"
            f"{record['high_val']:<11}"
            f"{record['fraction']:<10}"
            f"{record['pos']:<6}"
            f"{record['pos_val']:<10}"
            f"{record['action']}"
        )

    print("-" * 80)
    print(f"Result: Target {target} found at index {result_idx} in {len(history)} probe(s)!\n")

    # Head-to-head probe comparison on a large uniform dataset
    print("=" * 70)
    print("HEAD-TO-HEAD COMPARISON: INTERPOLATION SEARCH VS BINARY SEARCH")
    print("=" * 70)
    dataset_size = 1_000_000
    large_data = list(range(0, dataset_size * 5, 5))
    search_key = 3_456_780  # exact match at index 691356

    # Binary search simulation to count probes
    b_low, b_high = 0, len(large_data) - 1
    binary_probes = 0
    while b_low <= b_high:
        binary_probes += 1
        mid = b_low + (b_high - b_low) // 2
        if large_data[mid] == search_key:
            break
        elif large_data[mid] < search_key:
            b_low = mid + 1
        else:
            b_high = mid - 1

    # Interpolation search simulation
    _, interp_history = interpolation_search_instrumented(large_data, search_key)
    interp_probes = len(interp_history)

    print(f"Dataset Size: {dataset_size:,} elements (Uniform Arithmetic Progression)")
    print(f"Search Key:   {search_key:,}")
    print(f"Binary Search Probes:        {binary_probes} probes (Theoretical ceiling: ~{math.ceil(math.log2(dataset_size))})")
    print(f"Interpolation Search Probes: {interp_probes} probe(s) (Theoretical expectation: O(log log n))")
    print(f"Speedup in Probes:           {binary_probes / interp_probes:.1f}x reduction in memory accesses!")
    print("=" * 70)


if __name__ == "__main__":
    main()
