r"""
# Fibonacci Search: Division-Free Divide-and-Conquer Search

## A. Concept Name
Fibonacci Search (also known as Fibonacci Search Technique or Division-Free Search)

## B. One-Sentence Definition
Fibonacci Search is a comparison-based divide-and-conquer search algorithm for sorted arrays that partitions intervals into lengths corresponding to consecutive Fibonacci numbers, eliminating the need for division or multiplication operations by relying strictly on integer addition and subtraction.

## C. Why Does This Exist? (What problem does it solve?)
In standard Binary Search, the algorithm partitions the search window exactly in half at every step:
$$\text{mid} = \text{low} + \frac{\text{high} - \text{low}}{2}$$
This division by 2 (or integer shift) is trivial on modern general-purpose x86/ARM CPUs. However:
1. **The Division Cost in Hardware:** On low-power microcontrollers (such as 8-bit/16-bit PIC, AVR, legacy DSPs, and older ARM Cortex-M0 chips without a hardware integer division unit), integer division must be emulated in software routines taking 20 to 80 clock cycles, whereas addition and subtraction execute in **exactly 1 clock cycle**. Fibonacci Search replaces all division operations in the inner loop with simple additions and subtractions.
2. **Asymmetric Partitioning for Non-Uniform Memory Access:** Binary Search always cuts 50/50. Fibonacci Search divides the array into unequal segments proportional to the Golden Ratio ($\approx 61.8\%$ and $38.2\%$). In sequential or mechanical storage media (e.g., magnetic tape reels, certain serial flash memory architectures, or hierarchical disk drives), seeking forward is significantly cheaper than rewinding backward. The asymmetric stepping of Fibonacci Search can be aligned with physical hardware access characteristics.
3. **Foundation for Continuous Optimization:** Fibonacci Search was originally introduced by Jack Kiefer in 1953 as a minimax-optimal procedure for locating the maximum or minimum of a unimodal continuous function within a given interval using a minimal number of function evaluations. It serves as the discrete foundation for the Golden Section Search.

## D. Intuition & Real-Life Analogy
- **The Golden Ratio Nautilus Shell:**
  Nature constructs seashells, sunflower seed spirals, and pinecones using the Fibonacci sequence ($1, 1, 2, 3, 5, 8, 13, 21, \dots$). Instead of cutting an object strictly in half, each chamber grows by the sum of the previous two. Fibonacci Search cuts the array into two adjacent Fibonacci blocks ($F_{m-1}$ and $F_{m-2}$).
- **The Broken Calculator on a Long Highway:**
  Imagine you are driving along a 144-mile highway looking for a specific roadside diner. Your GPS computer is broken: its division and multiplication buttons are fried, but the addition, subtraction, and memory recall buttons work perfectly. You have a printed sheet of Fibonacci numbers ($144, 89, 55, 34, 21, 13, \dots$). By subtracting the next smaller Fibonacci number from your current position, you can pinpoint the diner's exact mile marker with zero division calculations!

## E. Mental Model
Consider an array padded conceptually to length $F_m - 1$, where $F_m$ is the smallest Fibonacci number $\ge n$:
```text
|<------------------------- F_m - 1 ------------------------->|
+-----------------------------------+-------------------------+
|        Subarray 1 (F_{m-1} - 1)   |  Subarray 2 (F_{m-2} - 1)|
+-----------------------------------+-------------------------+
                                    ^
                                Probe index i
```
At any point in the search:
- The active interval has size bounded by $F_m - 1$.
- We probe at index: $i = \min(\text{offset} + F_{m-2}, n - 1)$.
- If $arr[i] == target$: Target found!
- If $arr[i] > target$: Target lies in the left subarray. We discard the right subarray and reduce our Fibonacci window by **2 levels** ($F_m \leftarrow F_{m-2}$). The `offset` does not move.
- If $arr[i] < target$: Target lies in the right subarray. We discard the left subarray, shift our `offset` forward to $i$, and reduce our Fibonacci window by **1 level** ($F_m \leftarrow F_{m-1}$).

Because $F_m = F_{m-1} + F_{m-2}$, stepping down the Fibonacci sequence only requires subtraction:
$$F_{m-2} = F_m - F_{m-1} \quad \text{and} \quad F_{m-3} = F_{m-1} - F_{m-2}$$
No division or multiplication is ever performed!

## F. Formal Technical Explanation
1. **Fibonacci Sequence Definition:**
   $$F_0 = 0, \quad F_1 = 1, \quad F_m = F_{m-1} + F_{m-2} \quad \text{for } m \ge 2$$
2. **Initialization:**
   Find the smallest Fibonacci number $F_m \ge n$ (the array size). Let $F_{m-1}$ and $F_{m-2}$ be the two preceding Fibonacci numbers.
   Initialize `offset = -1`. The variable `offset` marks the highest index eliminated from the left side of the search space.
3. **Inner Loop Invariant ($F_m > 1$):**
   Calculate the candidate probe index:
   $$i = \min(offset + F_{m-2}, n - 1)$$
   The `min` clamp is essential because the array length $n$ might be smaller than $F_m - 1$.
4. **Three-Way Comparison:**
   - **Case 1 ($arr[i] == target$):** Return $i$.
   - **Case 2 ($arr[i] > target$):**
     The target must reside between $offset + 1$ and $i - 1$.
     The length of this remaining subsegment is at most $F_{m-2} - 1$.
     We step down **two Fibonacci steps**:
     $$F_m \leftarrow F_{m-2}, \quad F_{m-1} \leftarrow F_{m-1} - F_{m-2}, \quad F_{m-2} \leftarrow F_m - F_{m-1}$$
     `offset` remains unchanged.
   - **Case 3 ($arr[i] < target$):**
     The target must reside between $i + 1$ and the current upper bound.
     The length of this remaining subsegment is at most $F_{m-1} - 1$.
     We step down **one Fibonacci step**:
     $$F_m \leftarrow F_{m-1}, \quad F_{m-1} \leftarrow F_{m-2}, \quad F_{m-2} \leftarrow F_m - F_{m-1}$$
     Update `offset = i`.
5. **Residual Check ($F_{m-1} == 1$):**
   When the loop terminates with $F_m \le 1$, exactly one possible element could remain unchecked at index $offset + 1$.
   If $F_{m-1} == 1$ and $offset + 1 < n$ and $arr[offset + 1] == target$, return $offset + 1$.
   Otherwise, target is not present; return $-1$.

## G. Mathematical Foundation
1. **Golden Ratio Relation:**
   The ratio between successive Fibonacci numbers converges to the Golden Ratio $\phi$:
   $$\lim_{m \to \infty} \frac{F_m}{F_{m-1}} = \phi = \frac{1 + \sqrt{5}}{2} \approx 1.6180339887...$$
   $$\lim_{m \to \infty} \frac{F_{m-1}}{F_m} = \frac{1}{\phi} \approx 0.6180339887...$$
   $$\lim_{m \to \infty} \frac{F_{m-2}}{F_m} = \frac{1}{\phi^2} \approx 0.3819660112...$$
   Notice that $\frac{1}{\phi} + \frac{1}{\phi^2} = 0.618 + 0.382 = 1.0$.
   Thus, Fibonacci Search splits the search space into approximately $61.8\%$ and $38.2\%$ proportions!

2. **Binet's Formula and Search Step Bound:**
   By Binet's Formula:
   $$F_m = \frac{\phi^m - \psi^m}{\sqrt{5}} \approx \frac{\phi^m}{\sqrt{5}}, \quad \text{where } \psi = -\frac{1}{\phi}$$
   For an array of size $n$, the smallest $F_m \ge n$ satisfies:
   $$\frac{\phi^m}{\sqrt{5}} \approx n \implies \phi^m \approx n \sqrt{5}$$
   $$m \approx \log_{\phi}(n \sqrt{5}) = \frac{\ln(n \sqrt{5})}{\ln \phi} \approx \frac{\ln n + 0.8047}{0.4812} \approx 2.078 \ln n \approx 1.4404 \log_2 n$$
   Since each comparison either decrements $m$ by 1 (when $arr[i] < target$) or decrements $m$ by 2 (when $arr[i] > target$), the maximum number of comparisons in the worst case is:
   $$T_{\text{worst}}(n) \approx 1.44 \log_2 n$$
   The average number of comparisons is approximately $1.04 \log_2 n$.

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity:**
  - **Best Case: $O(1)$**
    Occurs when the target element is located at the first probe index $i = F_{m-2} - 1$.
  - **Average Case: $O(\log n)$**
    Averages approximately $1.04 \log_2 n$ comparisons.
  - **Worst Case: $O(\log n)$**
    At most $\approx 1.44 \log_2 n$ comparisons (occurs when the search consistently branches into the larger $F_{m-1}$ partition).
- **Space Complexity:**
  - **Iterative: $O(1)$ auxiliary space.** Requires only four integer scalar variables (`fibM`, `fib1`, `fib2`, `offset`).
  - **With Precomputed Table: $O(1)$ auxiliary space.** A small table of 48 Fibonacci numbers fits in under 200 bytes of ROM/flash and can index arrays up to $2.97 \times 10^{10}$ elements.
- **Hardware Instruction & CPU Cycle Profile:**
  - **Binary Search Loop:** 1 addition, 1 subtraction, 1 bit-shift (or division), 1 comparison.
  - **Fibonacci Search Loop:** 1 addition, 1 subtraction, 0 divisions, 0 bit-shifts, 1 comparison.
  - On processors where division requires software emulation (e.g. 50+ clock cycles), Fibonacci Search outperforms Binary Search in total CPU cycles, even though it executes slightly more comparisons on average.

## I. Common Mistakes & Pitfalls
1. **Missing the Clamping Bound:**
   Computing `i = offset + fib2` without `min(offset + fib2, n - 1)`.
   If the array length $n$ is not strictly equal to $F_m - 1$, $offset + fib2$ can exceed $n - 1$, raising an immediate `IndexError: list index out of range`.
2. **Inverting the Fibonacci Reductions:**
   Confusing which branch drops 1 Fibonacci step vs. 2 Fibonacci steps:
   - When $arr[i] < target$: The target is in the larger right subarray. Drop **1 step** ($F_m \leftarrow F_{m-1}$) and advance `offset = i`.
   - When $arr[i] > target$: The target is in the smaller left subarray. Drop **2 steps** ($F_m \leftarrow F_{m-2}$) and DO NOT advance `offset`.
   Swapping these causes the search window to misalign, creating an infinite loop or missing targets.
3. **Omitting the Residual Boundary Check:**
   When the main loop terminates ($F_m \le 1$), the candidate element at $offset + 1$ has NOT yet been compared! Failing to check `arr[offset + 1] == target` causes the search to fail whenever the target happens to be at the boundary or remaining singleton index.
4. **Incorrect Initial Offset:**
   Initializing `offset = 0` instead of `offset = -1`.
   Because array indexing is 0-based, if $offset = 0$ and $fib2 = 1$, the first probe checks index $1$, completely skipping index $0$!

## J. Common Confusions
- **Fibonacci Search vs. Binary Search:**
  Binary Search divides symmetric 50/50 intervals using midpoint division/shifts. Fibonacci Search divides asymmetric 61.8/38.2 intervals using only addition and subtraction. Binary Search has fewer worst-case comparisons ($1.0 \log_2 n$ vs. $1.44 \log_2 n$), but Fibonacci Search has zero division instructions.
- **Fibonacci Search vs. Golden Section Search:**
  Fibonacci Search operates on discrete sorted integer arrays. Golden Section Search operates on continuous functions $f(x)$ over an interval $[a, b]$ to find local extrema (minima or maxima). The Golden Section Search is the continuous limit of Fibonacci Search as $m \to \infty$.
- **Fibonacci Search vs. Ternary Search:**
  Ternary search divides the interval into three equal parts ($1/3, 1/3, 1/3$) and performs two comparisons per iteration ($2 \log_3 n \approx 1.26 \log_2 n$ comparisons). Fibonacci search performs only one comparison per step on average and requires no division by 3.

## K. When To Use It
- Embedded systems, microcontrollers (AVR, PIC, STM32 low-end, 8051), or DSPs where hardware integer division is missing and software division is costly.
- Real-time safety-critical systems where instruction cycle counts must be strictly deterministic and addition/subtraction guarantees uniform cycle execution times.
- Magnetic tape storage, flash page blocks, or sequential streams where forward seeks are physically faster than backward seeks.
- Algorithmic study of division-free computing and Golden Ratio optimization paradigms.

## L. When NOT To Use It
- Modern high-performance desktop or server CPUs (x86-64, modern ARM) where bit-shift `(low + high) >> 1` executes in 1 cycle, and the branch predictor favors binary search's symmetric splits.
- Unsorted data (requires sorted order).
- Linked lists or data structures lacking $O(1)$ random-access indexing.
- Very small arrays ($n < 10$), where simple linear search is faster due to lower setup overhead.

## M. Trade-offs
- **Pros:**
  - Strictly division-free: uses only addition and subtraction.
  - Guaranteed $O(\log n)$ worst-case time complexity.
  - $O(1)$ auxiliary memory space.
  - Asymmetric partition can benefit forward-seeking memory hardware.
- **Cons:**
  - Slightly more comparisons than Binary Search ($1.44 \log_2 n$ vs. $1.0 \log_2 n$ worst case).
  - More complex state management ($F_m, F_{m-1}, F_{m-2}, offset$) than Binary Search ($low, high$).

## N. Debugging Tips
1. Trace the four key state variables at every iteration: `(fibM, fib1, fib2, offset, i, arr[i])`.
2. Always assert the Fibonacci invariant: `assert fib2 + fib1 == fibM` at the start of each iteration.
3. Check the edge case where $n = 1$ and $n = 2$ to ensure the while loop and residual checks terminate cleanly.
4. Verify that `offset` monotonically increases or stays constant, never decreases.

## O. Memory Hook (Spaced repetition anchor)
"Fibonacci skips division:
Step forward? Drop one Fib, update offset.
Step backward? Drop two Fibs, keep offset.
End of the line? Check offset plus one!"

## P. Active Recall Questions
1. Why does `offset` start at `-1` instead of `0`?
2. Why is the probe index clamped with `min(offset + fib2, n - 1)`?
3. How does Fibonacci search step down the Fibonacci sequence without recomputing or using an array?
4. What is the worst-case number of comparisons in Fibonacci Search relative to $\log_2 n$?
5. What residual condition must be tested after the main while loop terminates?

## Q. Interview Questions & Answers
- **Q: Why would anyone use Fibonacci Search over Binary Search on a modern 64-bit computer?**
  *A:* On a modern desktop CPU with hardware branch prediction and fast bit-shifts, Binary Search is generally preferred. However, Fibonacci Search is celebrated in computer architecture and embedded systems where hardware dividers are absent. Additionally, on magnetic tape or non-uniform memory architectures where seeking forward is faster than seeking backward, Fibonacci search's asymmetric stepping provides a physical advantage.
- **Q: How does Fibonacci Search avoid division when stepping down Fibonacci levels?**
  *A:* Since $F_m = F_{m-1} + F_{m-2}$, we have $F_{m-2} = F_m - F_{m-1}$. When stepping down 1 level, the new $(F_m, F_{m-1}, F_{m-2})$ becomes $(F_{m-1}, F_{m-2}, F_{m-1} - F_{m-2})$. When stepping down 2 levels, the new $(F_m, F_{m-1}, F_{m-2})$ becomes $(F_{m-2}, F_{m-1} - F_{m-2}, F_{m-2} - (F_{m-1} - F_{m-2}))$. Every transition is accomplished solely by simple subtractions!
- **Q: Can Fibonacci Search be adapted to optimize a continuous unimodal function?**
  *A:* Yes! That is Kiefer's original 1953 algorithm: Fibonacci Search for unimodal optimization. When the number of function evaluations $N$ is known in advance, Fibonacci search achieves the minimax optimal contraction of the uncertainty interval. When $N$ is not known in advance, the continuous Golden Section Search is used.

## R. Project Connections (Where is this used in real systems?)
- **Automotive Electronic Control Units (ECU):** Bare-metal engine firmware running on low-cost microcontrollers (e.g. Renesas RH850 or NXP S32K without hardware floating-point or division coprocessors) uses Fibonacci search to perform real-time fuel-injection lookup table queries.
- **Digital Signal Processors (DSP):** High-cadence audio filters searching frequency-response lookup tables under strict single-cycle instruction budgets.
- **Tape Archive Retrieval Systems:** Archival storage libraries (e.g., LTO tape systems) where physical tape movement in the forward direction is faster than rewinding, matching the asymmetric step structure of Fibonacci search.

## S. Comparative Analysis & Alternatives
| Algorithm | Best Time | Average Time | Worst Time | Space | Operations in Loop | Division Needed? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | Increment, Compare | No |
| **Binary Search** | $O(1)$ | $O(\log_2 n)$ | $O(\log_2 n)$ | $O(1)$ | Add, Shift/Divide, Compare | Yes (or bit-shift) |
| **Fibonacci Search**| $O(1)$ | $\approx 1.04 \log_2 n$| $\approx 1.44 \log_2 n$| $O(1)$ | Add, Subtract, Compare | **NO (Zero Division)**|
| **Interpolation** | $O(1)$ | $O(\log \log n)$| $O(n)$ | $O(1)$ | Multiply, Divide, Sub | Yes (Heavy Division) |

## T. Edge Cases & Boundary Conditions
1. **Empty Array (`arr = []`):** Returns `-1` immediately.
2. **Single-Element Array (`arr = [x]`):** $F_m = 1$, loop does not run; residual check evaluates $offset + 1 = 0$ and correctly identifies match or mismatch.
3. **Array size is $F_m - 1$ exactly:** The probe index never needs clamping; full Fibonacci tree is utilized.
4. **Array size is NOT a Fibonacci number:** Clamping `min(offset + fib2, n - 1)` prevents index overflow.
5. **Target at Index 0:** Handled either on the first left-branch traversal or by the final residual check.
6. **Target at Index $n - 1$:** Handled by the rightmost boundary updates.
7. **Negative Numbers:** Handles arbitrary integers cleanly since comparisons are strictly relational (`<`, `>`, `==`).

## U. Practice Exercises & Problem Variants
1. **Unimodal Peak Finding:** Implement Fibonacci search to find the peak of a unimodal array (an array that strictly increases then strictly decreases) without division.
2. **Precomputed ROM Table:** Implement an embedded C/Python equivalent using a 32-entry static array of Fibonacci numbers.
3. **Continuous Golden Section Search:** Implement Golden Section Search to find the minimum of $f(x) = x^2 - 4x + 4$ on $[0, 5]$.

## V. Visual Step-by-Step Trace Walkthrough
Searching for `target = 85` in `arr = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100]`:
- Array length $n = 11$.
- Smallest Fibonacci $\ge 11$ is $F_7 = 13$.
- Fib sequence: $F_5 = 5$, $F_6 = 8$, $F_7 = 13$.
- `fibM = 13, fib1 = 8, fib2 = 5, offset = -1`
- **Iteration 1:**
  - $i = \min(-1 + 5, 10) = 4$.
  - $arr[4] = 45 < 85 \implies$ Target is in right subarray!
  - `offset = 4`.
  - Drop 1 Fib: `fibM = 8, fib1 = 5, fib2 = 3`.
- **Iteration 2:**
  - $i = \min(4 + 3, 10) = 7$.
  - $arr[7] = 82 < 85 \implies$ Target is in right subarray!
  - `offset = 7`.
  - Drop 1 Fib: `fibM = 5, fib1 = 3, fib2 = 2`.
- **Iteration 3:**
  - $i = \min(7 + 2, 10) = 9$.
  - $arr[9] = 90 > 85 \implies$ Target is in left subarray!
  - `offset` stays `7`.
  - Drop 2 Fibs: `fibM = 2, fib1 = 1, fib2 = 1`.
- **Iteration 4:**
  - $i = \min(7 + 1, 10) = 8$.
  - $arr[8] = 85 == 85 \implies$ **MATCH FOUND AT INDEX 8!**

## W. Verification & Quality Checklist
- [x] Division-free inner loop: only addition and subtraction operations used.
- [x] Clamping `min(offset + fib2, n - 1)` prevents index errors on non-Fibonacci sizes.
- [x] Residual check at $offset + 1$ covers boundary targets when $F_m = 1$.
- [x] Embedded precomputed lookup table variant included.
- [x] Continuous Golden Section Search optimization bridge implemented.
- [x] Deliberately buggy version with debugging commentary included.
- [x] Comprehensive unit tests testing all branches, edge cases, and sizes.

## X. Project Connection & Real-World Case Study
In automotive electronic control units (ECUs) controlling internal combustion timing, sensor lookups (e.g. mass airflow vs. throttle angle calibration tables) run inside microsecond-bounded interrupt service routines (ISRs). These chips often lack hardware floating-point and integer division units. Compilers substituting software division routines introduce unpredictable multi-cycle jitter that violates automotive timing safety standards (ISO 26262 ASIL-D). By implementing calibration table searches using Fibonacci Search with a precomputed Fibonacci lookup table in ROM, engine calibration engineers guarantee deterministic execution times with zero division latency, meeting stringent hard real-time deadlines.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
import math
import bisect


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (STANDARD ITERATIVE)
# ==============================================================================

def fibonacci_search(arr: Sequence[int], target: int) -> int:
    """
    Perform Fibonacci Search on a sorted sequence of integers.
    
    Operates strictly via addition and subtraction without division.
    Guarantees O(1) auxiliary space and O(log n) time complexity.
    
    Args:
        arr: Sorted sequence of integers.
        target: The key to find.
        
    Returns:
        0-based index of target if found; otherwise -1.
        
    Complexity:
        Time: Best O(1), Average O(log n), Worst O(log n) [at most ~1.44 log2(n)].
        Space: O(1) auxiliary memory.
    """
    if not arr:
        return -1

    n: int = len(arr)

    # Step 1: Initialize Fibonacci numbers
    # fib2 is (m - 2)-th Fibonacci number
    # fib1 is (m - 1)-th Fibonacci number
    # fibM is m-th Fibonacci number
    fib2: int = 0  # F_{m-2}
    fib1: int = 1  # F_{m-1}
    fibM: int = fib2 + fib1  # F_m

    # Find the smallest Fibonacci number greater than or equal to n
    while fibM < n:
        fib2 = fib1
        fib1 = fibM
        fibM = fib2 + fib1

    # offset marks the highest index eliminated from the left side of the array
    # Initialized to -1 because array is 0-indexed
    offset: int = -1

    # Step 2: Search loop while there are elements to inspect (fibM > 1)
    while fibM > 1:
        # Check if fib2 is a valid index; clamp to n - 1 to prevent IndexError
        i: int = min(offset + fib2, n - 1)

        # Target is greater than current value: search right subarray
        if arr[i] < target:
            # Drop 1 Fibonacci step: search space becomes F_{m-1}
            fibM = fib1
            fib1 = fib2
            fib2 = fibM - fib1
            offset = i

        # Target is smaller than current value: search left subarray
        elif arr[i] > target:
            # Drop 2 Fibonacci steps: search space becomes F_{m-2}
            fibM = fib2
            fib1 = fib1 - fib2
            fib2 = fibM - fib1
            # offset remains unchanged

        # Target found
        else:
            return i

    # Step 3: Residual check
    # When fibM == 1, fib1 == 1 and fib2 == 0. Exactly one candidate element
    # remains at offset + 1. Check if it matches target.
    if fib1 == 1 and (offset + 1) < n and arr[offset + 1] == target:
        return offset + 1

    return -1


# ==============================================================================
# 2. EMBEDDED-STYLE PRECOMPUTED LOOKUP TABLE IMPLEMENTATION
# ==============================================================================

# Static precomputed Fibonacci lookup table up to F_47
# F_46 = 1,836,311,903 (fits comfortably in signed 32-bit integer)
# Allows searching arrays of up to 1.8 billion elements with zero runtime generation.
FIBONACCI_TABLE: Tuple[int, ...] = (
    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597,
    2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418,
    317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465,
    14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296,
    433494437, 701408733, 1134903170, 1836311903
)

def fibonacci_search_precomputed(arr: Sequence[int], target: int) -> int:
    """
    Embedded microcontroller-style Fibonacci Search using precomputed ROM table.
    
    Eliminates the initial Fibonacci generation loop entirely, reducing startup latency.
    
    Args:
        arr: Sorted sequence.
        target: Element to find.
        
    Returns:
        Index of target if found, else -1.
    """
    n = len(arr)
    if n == 0:
        return -1

    # Find the smallest Fibonacci index m such that FIBONACCI_TABLE[m] >= n
    # In C/assembly, this is a tiny unrolled scan or binary search over 47 elements
    m = 0
    while m < len(FIBONACCI_TABLE) and FIBONACCI_TABLE[m] < n:
        m += 1

    if m >= len(FIBONACCI_TABLE):
        raise ValueError(f"Array size {n} exceeds precomputed Fibonacci table capacity.")

    offset = -1

    while m > 1:
        # Probe index uses F_{m-2}
        fib2 = FIBONACCI_TABLE[m - 2]
        i = min(offset + fib2, n - 1)

        if arr[i] < target:
            # Drop 1 Fibonacci level
            m -= 1
            offset = i
        elif arr[i] > target:
            # Drop 2 Fibonacci levels
            m -= 2
        else:
            return i

    # Residual check
    if m == 1 and (offset + 1) < n and arr[offset + 1] == target:
        return offset + 1

    return -1


# ==============================================================================
# 3. INSTRUMENTED IMPLEMENTATION (EDUCATIONAL METRICS & TRACE)
# ==============================================================================

def fibonacci_search_instrumented(
    arr: Sequence[int],
    target: int
) -> Tuple[int, List[Dict[str, Any]]]:
    """
    Instrumented Fibonacci Search recording detailed operational traces.
    
    Returns:
        Tuple of (found_index, history_list_of_dictionaries).
    """
    history: List[Dict[str, Any]] = []
    if not arr:
        return -1, history

    n = len(arr)
    fib2 = 0
    fib1 = 1
    fibM = fib2 + fib1

    while fibM < n:
        fib2 = fib1
        fib1 = fibM
        fibM = fib2 + fib1

    offset = -1
    step = 1

    while fibM > 1:
        i = min(offset + fib2, n - 1)
        record = {
            "step": step,
            "fibM": fibM,
            "fib1": fib1,
            "fib2": fib2,
            "offset": offset,
            "probe_idx": i,
            "probe_val": arr[i],
            "action": ""
        }

        if arr[i] < target:
            record["action"] = f"arr[{i}]={arr[i]} < {target} -> offset={i}, drop 1 Fib"
            fibM = fib1
            fib1 = fib2
            fib2 = fibM - fib1
            offset = i
        elif arr[i] > target:
            record["action"] = f"arr[{i}]={arr[i]} > {target} -> keep offset, drop 2 Fibs"
            fibM = fib2
            fib1 = fib1 - fib2
            fib2 = fibM - fib1
        else:
            record["action"] = f"arr[{i}]={arr[i]} == {target} -> MATCH FOUND!"
            history.append(record)
            return i, history

        history.append(record)
        step += 1

    # Residual check
    if fib1 == 1 and (offset + 1) < n:
        is_match = (arr[offset + 1] == target)
        history.append({
            "step": step,
            "fibM": fibM,
            "fib1": fib1,
            "fib2": fib2,
            "offset": offset,
            "probe_idx": offset + 1,
            "probe_val": arr[offset + 1],
            "action": f"Residual check at index {offset + 1}: match={is_match}"
        })
        if is_match:
            return offset + 1, history

    return -1, history


# ==============================================================================
# 4. CONTINUOUS DOMAIN ANALOGUE: GOLDEN SECTION SEARCH
# ==============================================================================

def continuous_golden_section_search(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-6
) -> float:
    """
    Continuous counterpart to Fibonacci Search (Golden Section Search).
    
    Finds the minimum of a unimodal continuous function f on the interval [a, b].
    Demonstrates the Golden Ratio contraction principle in continuous optimization.
    
    Args:
        f: A unimodal scalar function.
        a: Lower bound of search interval.
        b: Upper bound of search interval.
        tol: Convergence tolerance.
        
    Returns:
        The x-coordinate approximating the function minimum.
    """
    invphi = (math.sqrt(5.0) - 1.0) / 2.0  # 1 / phi ≈ 0.6180339887
    invphi2 = (3.0 - math.sqrt(5.0)) / 2.0  # 1 / phi^2 ≈ 0.3819660112

    (a, b) = (min(a, b), max(a, b))
    h = b - a
    if h <= tol:
        return (a + b) / 2.0

    # Required steps
    n = int(math.ceil(math.log(tol / h) / math.log(invphi)))

    c = a + invphi2 * h
    d = a + invphi * h
    yc = f(c)
    yd = f(d)

    for _ in range(n):
        if yc < yd:
            b = d
            d = c
            yd = yc
            h = invphi * h
            c = a + invphi2 * h
            yc = f(c)
        else:
            a = c
            c = d
            yc = yd
            h = invphi * h
            d = a + invphi * h
            yd = f(d)

    return (a + b) / 2.0


# ==============================================================================
# 5. DELIBERATELY BUGGY IMPLEMENTATION (EDUCATIONAL ANTI-PATTERN)
# ==============================================================================

def fibonacci_search_buggy(arr: List[int], target: int) -> int:
    """
    DELIBERATELY BUGGY IMPLEMENTATION FOR PEDAGOGICAL DEBUGGING.
    
    Contains 3 classic engineering blunders:
    
    Bug 1 (Unclamped Probe Index):
      Uses `i = offset + fib2` WITHOUT `min(..., n - 1)`.
      When n is not a Fibonacci number minus 1, `offset + fib2` can exceed
      `len(arr) - 1`, triggering an immediate `IndexError: list index out of range`!
      
    Bug 2 (Swapped Fibonacci Reductions):
      Inverts the branch step-down logic: drops 2 steps for `<` and 1 step for `>`.
      This corrupts the search intervals and throws the search into wrong partitions.
      
    Bug 3 (Missing Residual Boundary Check):
      Omits the final residual check `if fib1 and offset + 1 < n and arr[offset + 1] == target:`.
      This causes the algorithm to return -1 for targets located at the last checked position!
    """
    if not arr:
        return -1

    n = len(arr)
    fib2 = 0
    fib1 = 1
    fibM = fib2 + fib1

    while fibM < n:
        fib2 = fib1
        fib1 = fibM
        fibM = fib2 + fib1

    offset = -1

    while fibM > 1:
        # BUG 1: Missing `min(offset + fib2, n - 1)`
        # Directly accesses arr[offset + fib2], which will trigger native IndexError when offset + fib2 >= n!
        i = offset + fib2

        if arr[i] < target:
            # BUG 2: Inverted update logic! Should drop 1 step, but drops 2!
            fibM = fib2
            fib1 = fib1 - fib2
            fib2 = fibM - fib1
            offset = i
        elif arr[i] > target:
            # BUG 2: Inverted update logic! Should drop 2 steps, but drops 1!
            fibM = fib1
            fib1 = fib2
            fib2 = fibM - fib1
        else:
            return i

    # BUG 3: Omits residual check `arr[offset + 1] == target`!
    return -1


# ==============================================================================
# 6. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite covering standard, edge, negative, and varying-size arrays.
    """
    algorithms = [
        ("Iterative Fibonacci Search", fibonacci_search),
        ("Precomputed Lookup Fibonacci Search", fibonacci_search_precomputed),
    ]

    print("=" * 70)
    print("RUNNING COMPREHENSIVE FIBONACCI SEARCH TEST SUITE")
    print("=" * 70)

    # 1. Standard Sorted Array Test
    test_arr = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100, 235]
    for name, func in algorithms:
        # Test every single element present
        for expected_idx, val in enumerate(test_arr):
            actual_idx = func(test_arr, val)
            assert actual_idx == expected_idx, (
                f"{name} failed on present value {val}: expected {expected_idx}, got {actual_idx}"
            )
        # Test absent elements
        assert func(test_arr, 5) == -1, f"{name} failed on target below min"
        assert func(test_arr, 300) == -1, f"{name} failed on target above max"
        assert func(test_arr, 42) == -1, f"{name} failed on missing interior value"

    # 2. Empty Array & Single Element Array
    for name, func in algorithms:
        assert func([], 10) == -1, f"{name} failed on empty array"
        assert func([42], 42) == 0, f"{name} failed on matching single element"
        assert func([42], 99) == -1, f"{name} failed on non-matching single element"

    # 3. Two Elements Array
    two_elem = [100, 200]
    for name, func in algorithms:
        assert func(two_elem, 100) == 0, f"{name} failed on 1st of two elements"
        assert func(two_elem, 200) == 1, f"{name} failed on 2nd of two elements"
        assert func(two_elem, 150) == -1, f"{name} failed on missing between two elements"

    # 4. Three Elements Array
    three_elem = [1, 2, 3]
    for name, func in algorithms:
        assert func(three_elem, 1) == 0
        assert func(three_elem, 2) == 1
        assert func(three_elem, 3) == 2
        assert func(three_elem, 0) == -1
        assert func(three_elem, 4) == -1

    # 5. Arrays of Arbitrary Sizes (Checking non-Fibonacci sizes)
    # Test lengths from 1 to 65 to ensure clamping works across all boundary transitions
    for length in range(1, 65):
        arr = list(range(10, 10 + length * 2, 2))  # [10, 12, 14, ...]
        for name, func in algorithms:
            # First element
            assert func(arr, arr[0]) == 0, f"{name} failed on length {length} first element"
            # Middle element
            mid_idx = length // 2
            assert func(arr, arr[mid_idx]) == mid_idx, f"{name} failed on length {length} mid element"
            # Last element
            assert func(arr, arr[-1]) == length - 1, f"{name} failed on length {length} last element"
            # Missing element
            assert func(arr, arr[0] - 1) == -1, f"{name} failed on length {length} absent"

    # 6. Negative Integers
    neg_arr = [-50, -30, -20, -10, 0, 10, 25, 45, 60]
    for name, func in algorithms:
        assert func(neg_arr, -50) == 0
        assert func(neg_arr, -20) == 2
        assert func(neg_arr, 0) == 4
        assert func(neg_arr, 60) == 8
        assert func(neg_arr, -99) == -1

    # 7. Duplicate Elements
    dup_arr = [5, 5, 5, 5, 5, 5, 5]
    for name, func in algorithms:
        res = func(dup_arr, 5)
        assert 0 <= res < len(dup_arr) and dup_arr[res] == 5, f"{name} failed on duplicate array"
        assert func(dup_arr, 6) == -1

    # 8. Continuous Golden Section Search Test
    # Find minimum of f(x) = (x - 3)^2 + 5, which has a minimum at x = 3.0
    parabola = lambda x: (x - 3.0) ** 2 + 5.0
    min_x = continuous_golden_section_search(parabola, 0.0, 5.0, tol=1e-5)
    assert abs(min_x - 3.0) < 1e-4, f"Golden Section Search failed: expected ~3.0, got {min_x}"
    print(f"  [Verified] Continuous Golden Section Search found minimum at x = {min_x:.6f}")

    # 9. Test Deliberately Buggy Implementation to Confirm Diagnosed Failures
    print("Testing deliberate bugs in fibonacci_search_buggy()...")
    try:
        # Bug 1: Array of length 11: F_7 = 13. Searching for 120 causes offset + fib2 = 11 >= 11 (IndexError)
        fibonacci_search_buggy([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110], 120)
        print("  [Note] Buggy search did not crash on this input.")
    except IndexError as e:
        print(f"  [Verified] Buggy implementation failed as expected with native IndexError: {e}")

    # Bug 3: Target 30 in [10, 20, 30] is at index 2 (residual offset + 1). Buggy returns -1!
    buggy_res = fibonacci_search_buggy([10, 20, 30], 30)
    assert buggy_res == -1, f"Expected buggy implementation to return -1 due to Bug 3, got {buggy_res}"
    print(f"  [Verified] Buggy implementation missed residual target as expected: returned {buggy_res} (correct is 2)")

    print("\nALL FIBONACCI SEARCH TEST CASES PASSED SUCCESSFULLY!")
    print("=" * 70)


# ==============================================================================
# 7. MAIN DEMONSTRATION & EDUCATIONAL VISUALIZATION
# ==============================================================================

def main() -> None:
    """
    Main demonstration routine displaying step-by-step traces,
    Fibonacci window contraction, and division-free operation verification.
    """
    # Execute the comprehensive test suite
    run_tests()

    print("\n" + "=" * 70)
    print("FIBONACCI SEARCH: STEP-BY-STEP TRACE DEMONSTRATION")
    print("=" * 70)

    sample_arr = [10, 22, 35, 40, 45, 50, 80, 82, 85, 90, 100]
    target = 85

    print(f"Sorted Array: {sample_arr}")
    print(f"Array Size n: {len(sample_arr)}")
    print(f"Target Value: {target}\n")

    result_idx, history = fibonacci_search_instrumented(sample_arr, target)

    print(f"{'Step':<6}{'F_m':<6}{'F_{m-1}':<10}{'F_{m-2}':<10}{'Offset':<8}{'Probe_i':<10}{'arr[i]':<10}{'Action'}")
    print("-" * 80)
    for record in history:
        print(
            f"{record['step']:<6}"
            f"{record['fibM']:<6}"
            f"{record['fib1']:<10}"
            f"{record['fib2']:<10}"
            f"{record['offset']:<8}"
            f"{record['probe_idx']:<10}"
            f"{record['probe_val']:<10}"
            f"{record['action']}"
        )

    print("-" * 80)
    print(f"Result: Target {target} found at index {result_idx} in {len(history)} step(s)!\n")

    # Division-Free Hardware Analysis
    print("=" * 70)
    print("OPERATION PROFILE: FIBONACCI SEARCH VS BINARY SEARCH")
    print("=" * 70)
    print("Inner Loop Operations Comparison:")
    print("  Binary Search:")
    print("    - 1 Subtraction  (high - low)")
    print("    - 1 Division / Bit-Shift ((high - low) // 2)")
    print("    - 1 Addition     (low + half)")
    print("    - 1 Comparison   (arr[mid] vs target)")
    print("  Fibonacci Search:")
    print("    - 1 Addition     (offset + fib2)")
    print("    - 1 Subtraction  (fibM - fib1 or fib1 - fib2)")
    print("    - 0 Divisions / Multiplications! (Strictly zero)")
    print("    - 1 Comparison   (arr[i] vs target)")
    print("=" * 70)


if __name__ == "__main__":
    main()
