r"""
# Ternary Search: Complete Algorithmic & Mathematical Guide

## A. Concept Name
Ternary Search (Discrete Array Search & Continuous Unimodal Optimization)

## B. One-Sentence Definition
Ternary Search is a divide-and-conquer algorithm that divides a search space into three equal segments using two partition points (mid1 and mid2), enabling logarithmic item lookup in sorted arrays or derivative-free extremum localization in unimodal functions.

## C. Why Does This Exist? (What problem does it solve?)
In discrete searching, students often ask: "If binary search halves the search space in O(log2 N) time, does dividing into three parts yield O(log3 N) and run faster?" Ternary search exists to explore this theoretical limit, proving that fewer iterations does NOT necessarily mean fewer comparisons or faster runtime.

More importantly, Ternary Search solves a fundamental continuous optimization problem where Binary Search fails: finding the global maximum or minimum of a unimodal function without computing derivatives. Binary search requires knowing whether an evaluation is higher or lower than a known target, or requires gradient information (f'(x) = 0). Ternary search compares two interior probe points, f(mid1) and f(mid2), discarding an entire third of the domain where the extremum provably cannot exist, even when the function is non-differentiable.

## D. Intuition & Real-Life Analogy
- **Discrete Array Analogy (The Two-Question Game):**
  Suppose you are guessing a secret number between 1 and 99. In binary search, you ask 1 question: "Is the number > 50?" (cutting the candidates to 50). In ternary search, you ask 2 questions: "Is it <= 33?" and if not, "Is it > 66?". You cut the candidates down to 33, but you spent two questions to do so. In the end, asking 2 questions per round across fewer rounds costs more total questions than asking 1 question per round across slightly more rounds.
  
- **Continuous Peak Finding Analogy (The Mountain in the Fog):**
  Imagine you are hiking on a mountain ridge shrouded in thick fog. You know the ridge rises to a single summit (unimodal) and then descends on the other side. You cannot see the summit, and you do not have an altimeter gradient map. You send two scouts forward along your path: Scout 1 stands at position `mid1` and Scout 2 stands at position `mid2` (with `mid1 < mid2`). 
  - If Scout 1 measures an altitude higher than Scout 2 (`f(mid1) > f(mid2)`), the peak CANNOT be beyond Scout 2 on the right slope (since moving past mid1 to mid2 already dropped in elevation). Thus, you discard the entire right third of the mountain!
  - If Scout 2 is higher (`f(mid1) < f(mid2)`), the peak cannot be before Scout 1. You discard the left third!

## E. Mental Model
```text
Discrete Array Partitioning:
Index Range: [ left .......................................... right ]
                       mid1                    mid2
[ left ... mid1 - 1 ] | mid1 | [ mid1 + 1 ... mid2 - 1 ] | mid2 | [ mid2 + 1 ... right ]
      Part 1                        Part 2                         Part 3

Unimodal Function Peak Finding (Maximization):
f(x)
 ^                 Peak
 |                  /\
 |                 /  \
 |         mid1   /    \   mid2
 |          *    /      \   *
 |         / \  /        \ / \
 |        /   \/          V   \
 |       /                     \
 +------+-----------------------+---------> x
       left                   right

Case 1: f(mid1) < f(mid2)  ==> Peak CANNOT be in [left, mid1]. Discard left 1/3!
Case 2: f(mid1) > f(mid2)  ==> Peak CANNOT be in [mid2, right]. Discard right 1/3!
Case 3: f(mid1) == f(mid2) ==> Peak is in [mid1, mid2]. Discard both outer thirds!
```

## F. Formal Technical Explanation
Ternary search operates over an interval `[left, right]`:
1. **Trisection:** It determines two intermediate points:
   - `mid1 = left + (right - left) / 3`
   - `mid2 = right - (right - left) / 3`
2. **Discrete Array Search:**
   - Evaluates `arr[mid1]` and `arr[mid2]` against `target`.
   - If `target == arr[mid1]`, return `mid1`.
   - If `target == arr[mid2]`, return `mid2`.
   - If `target < arr[mid1]`, search space becomes `[left, mid1 - 1]`.
   - Else if `target > arr[mid2]`, search space becomes `[mid2 + 1, right]`.
   - Else search space becomes `[mid1 + 1, mid2 - 1]`.
3. **Continuous Unimodal Optimization:**
   - Evaluates `f(mid1)` and `f(mid2)`.
   - For maximization:
     - If `f(mid1) < f(mid2)`: the global maximum cannot reside in `[left, mid1]`. Update `left = mid1`.
     - Else: the global maximum cannot reside in `[mid2, right]`. Update `right = mid2`.
   - Iterates until `right - left < epsilon` or for a fixed number of iterations (e.g., 80-100 iterations achieves floating-point machine precision).

## G. Mathematical Foundation
1. **Discrete Search Comparison Count:**
   - Binary search recurrence: `T(N) = T(N/2) + 1` (or 2 comparisons in practice).
     Max comparisons: `2 * log2(N) = 2 * (ln N / ln 2) ≈ 2.885 * ln N`.
   - Ternary search recurrence: `T(N) = T(N/3) + 2` (or up to 4 comparisons in practice).
     Max comparisons: `4 * log3(N) = 4 * (ln N / ln 3) ≈ 3.641 * ln N`.
   - Since `3.641 * ln N > 2.885 * ln N`, ternary search performs approximately **26% MORE comparisons** than binary search in the worst case!

2. **Continuous Domain Reduction:**
   - At each step of continuous ternary search, the domain shrinks to `2/3` of its previous length.
   - After `k` iterations, the remaining interval length is:
     `L_k = (right_0 - left_0) * (2/3)^k`
   - To achieve precision `epsilon`:
     `(2/3)^k <= epsilon / (right_0 - left_0)  ==>  k >= log_{1.5}((right_0 - left_0) / epsilon)`
   - For an initial interval of length 1,000,000 and `epsilon = 10^-7`:
     `k = log_{1.5}(10^13) ≈ ln(10^13) / ln(1.5) ≈ 29.93 / 0.4055 ≈ 74 iterations`.

## H. Complexity Analysis
- **Discrete Array Search:**
  - Best-Case Time Complexity: `O(1)` (Target is at `mid1` or `mid2` on the first check).
  - Worst-Case Time Complexity: `O(log3 N)` iterations, which is asymptotically `O(log N)`.
  - Average-Case Time Complexity: `O(log N)`.
  - Space Complexity: `O(1)` auxiliary memory for iterative; `O(log3 N)` stack space for recursive.
- **Continuous Unimodal Optimization:**
  - Time Complexity: `O(log_{1.5}((right - left) / epsilon) * cost(f))` where `cost(f)` is function evaluation time.
  - Space Complexity: `O(1)` auxiliary space.

## I. Common Mistakes & Pitfalls
1. **Integer Midpoint Truncation:**
   Writing `mid2 = (left + right) * 2 // 3` or `mid2 = mid1 + (right - left) // 3`. When `right - left` is small, rounding errors can cause `mid1 == mid2` or make boundaries exceed limits.
   Always use: `mid1 = left + (right - left) // 3` and `mid2 = right - (right - left) // 3`.
2. **Floating-Point Infinite Loop with Epsilon:**
   Writing `while right - left > 1e-15:` can loop forever if machine precision limits `(right - left)` from shrinking further. It is much safer to run a fixed loop: `for _ in range(100):`.
3. **Applying to Non-Unimodal Functions:**
   If a function has multiple peaks, ternary search can discard the subsegment containing the global peak and settle on a suboptimal local extremum.
4. **Plateaus (f(mid1) == f(mid2)):**
   If the function contains flat horizontal regions, discarding either outer third might accidentally discard the extremum if the plateau is wide.

## J. Common Confusions
- **Ternary Search vs Binary Search:** Binary search is strictly faster for array lookup due to fewer branch comparisons and better branch prediction. Ternary search is primarily useful for *unimodal function extremum finding* where binary search cannot be directly applied without derivatives.
- **Ternary Search vs Golden Section Search:** Golden Section Search also optimizes unimodal continuous functions, but it partitions by the golden ratio `phi ≈ 0.618`. This allows reusing one probe evaluation from the previous iteration, reducing evaluations from 2 per step to 1 per step (a ~50% speedup).

## K. When To Use It
- Finding the minimum or maximum of a unimodal (or concave/convex) function when derivatives are unknown, difficult, or expensive to calculate.
- Geometry and physics problems: Finding the minimum distance between moving objects over time.
- Competitive programming problems featuring "Peak Index in a Mountain Array" or convex cost optimization.

## L. When NOT To Use It
- Standard lookup in a sorted array (use `bisect` / Binary Search instead).
- Multimodal functions with many local extrema (use Grid Search, Gradient Descent with restarts, Simulated Annealing, or Bayesian Optimization).
- Smooth differentiable functions where Newton-Raphson or Brent's method converges quadratically.

## M. Trade-offs
- **Pros:**
  - Derivative-free optimization.
  - Guaranteed linear convergence `O(log(1/eps))` on any strictly unimodal function.
  - Simple to implement without external numerical libraries.
- **Cons:**
  - Discrete version is slower than binary search in practice.
  - Slower than Golden Section Search (evaluates `f` twice per iteration instead of once).
  - Strictly requires the unimodality property.

## N. Debugging Tips
- Print `(left, mid1, mid2, right, f(mid1), f(mid2))` per step to verify that the interval monotonically shrinks by a factor of `2/3`.
- Verify unimodality by plotting the function or evaluating samples along the domain before running ternary search.
- For integer ternary search, check termination conditions when `right - left <= 2` to prevent infinite oscillation.

## O. Memory Hook
"Three parts, two scouts: where the scouts climb down, throw that third out!"

## P. Active Recall Questions
1. Why does Ternary Search require more comparisons than Binary Search when searching an array of size N?
2. What mathematical property must function `f(x)` satisfy for continuous ternary search to locate its maximum?
3. In continuous optimization, by what exact fraction does the search interval shrink after each iteration?
4. How does Golden Section Search optimize the number of function evaluations compared to Ternary Search?

## Q. Interview Questions & Answers
- **Q: How would you find the peak element in a strictly increasing then strictly decreasing array (Bitonic Array)?**
  *A:* You can use either Binary Search (comparing `arr[mid]` with `arr[mid + 1]`) or Ternary Search (comparing `arr[mid1]` with `arr[mid2]`). Binary search is preferred in interviews due to `O(log2 N)` comparisons.
- **Q: Can Ternary Search find the minimum of a convex parabola `f(x) = ax^2 + bx + c`?**
  *A:* Yes, every parabola with `a > 0` is strictly convex and unimodal. Ternary search will locate the vertex `x = -b / (2a)` within any desired epsilon.

## R. Real-World Failure Stories & Engineering Lessons
In high-frequency trading (HFT), an algorithmic routing engine used ternary search to find the optimal order batch size that minimized round-trip transaction latency. The developers assumed network latency as a function of batch size was unimodal (decreasing due to amortization, then increasing due to packet fragmentation). However, operating system socket buffers caused periodic discontinuous latency cliffs (bimodal behavior), trapping ternary search in an artificially high latency bucket and causing millions in delayed order fills.
*Lesson:* Never assume unimodality without rigorous empirical testing across boundary regions.

## S. Comparative Benchmark & Empirical Behavior
| Algorithm | Domain | Evaluations / Iteration | Domain Reduction / Iteration | Total Work for 10^-6 Precision |
| :--- | :--- | :--- | :--- | :--- |
| **Binary Search** | Monotonic discrete/continuous | 1 | 0.500 | ~20 evaluations |
| **Ternary Search** | Unimodal continuous | 2 | 0.667 | ~70 evaluations |
| **Golden Section Search** | Unimodal continuous | 1 (after step 1) | 0.618 | ~35 evaluations |
| **Brent's Method** | Smooth unimodal | 1 (parabolic interpolation) | Superlinear | ~8-12 evaluations |

## T. Edge Cases & Boundary Conditions
1. Target is at the exact boundary (`left == 0` or `right == len(arr) - 1`).
2. Array with 0, 1, or 2 elements.
3. Completely flat functions (`f(x) = c` everywhere): extremum is not unique.
4. Function with peak on the boundary point (`left` or `right`).

## U. Recommended Practice Problems
- LeetCode 852: Peak Index in a Mountain Array
- LeetCode 162: Find Peak Element
- LeetCode 1095: Find in Mountain Array
- Codeforces 578C: Weakness and Poorness (Ternary Search on Real Values)

## V. Verification & Edge-Case Checklist
- [x] Handled empty list (`arr = []`).
- [x] Handled 1-element and 2-element arrays.
- [x] Avoided integer overflow using `left + (right - left) // 3`.
- [x] Fixed-iteration loop used for float optimization to prevent epsilon underflow.
- [x] Verified exact equality matches on both `mid1` and `mid2`.

## W. Core Takeaways & Summary
- Ternary search splits a space into 3 segments using 2 pivots.
- For sorted arrays, it is an educational curiosity: `log3 N` iterations sounds superior, but `4 * log3 N` comparisons makes it slower than binary search.
- For unimodal function optimization, ternary search is a robust, derivative-free workhorse that reduces domain uncertainty by `(2/3)^k`.

## X. Project Connection
- **Game Engine & Graphics:** Finding the point of closest approach between two curved 3D trajectories (parametric splines).
- **Robotics & Motion Planning:** Optimizing traversal speed or throttle along a curve under non-linear friction constraints.
- **Machine Learning:** Derivative-free 1D hyperparameter tuning (e.g., optimal regularizer lambda or learning rate threshold).
"""

import math
from typing import Callable, List, Optional, Tuple


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (DISCRETE ARRAY SEARCH)
# ==============================================================================

def ternary_search_iterative(arr: List[int], target: int) -> int:
    """
    Searches for target in a sorted list using iterative Ternary Search.
    
    Args:
        arr: Sorted list of integers.
        target: Value to locate.
        
    Returns:
        Index of target if found, else -1.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        # Divide into 3 parts
        partition_size = (right - left) // 3
        mid1 = left + partition_size
        mid2 = right - partition_size

        # Check if target is at either probe point
        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        # Narrow down the search space
        if target < arr[mid1]:
            # Target is in the first third: [left, mid1 - 1]
            right = mid1 - 1
        elif target > arr[mid2]:
            # Target is in the third third: [mid2 + 1, right]
            left = mid2 + 1
        else:
            # Target is in the middle third: [mid1 + 1, mid2 - 1]
            left = mid1 + 1
            right = mid2 - 1

    return -1


def ternary_search_recursive(
    arr: List[int], target: int, left: int, right: int
) -> int:
    """
    Searches for target in a sorted list using recursive Ternary Search.
    
    Args:
        arr: Sorted list of integers.
        target: Value to locate.
        left: Left boundary index.
        right: Right boundary index.
        
    Returns:
        Index of target if found, else -1.
    """
    if left > right:
        return -1

    partition_size = (right - left) // 3
    mid1 = left + partition_size
    mid2 = right - partition_size

    if arr[mid1] == target:
        return mid1
    if arr[mid2] == target:
        return mid2

    if target < arr[mid1]:
        return ternary_search_recursive(arr, target, left, mid1 - 1)
    elif target > arr[mid2]:
        return ternary_search_recursive(arr, target, mid2 + 1, right)
    else:
        return ternary_search_recursive(arr, target, mid1 + 1, mid2 - 1)


# ==============================================================================
# 2. CONTINUOUS UNIMODAL FUNCTION OPTIMIZATION (PEAK / TROUGH FINDING)
# ==============================================================================

def ternary_search_maximum(
    func: Callable[[float], float],
    left: float,
    right: float,
    iterations: int = 100
) -> Tuple[float, float]:
    """
    Finds the input x in [left, right] that maximizes a unimodal function func(x).
    
    Uses a fixed iteration count to avoid floating-point epsilon underflow.
    Each iteration reduces the search interval to exactly 2/3 of its previous size.
    100 iterations achieves (2/3)^100 ≈ 2.45e-18 precision.
    
    Args:
        func: A unimodal mathematical function to maximize.
        left: Left bound of domain.
        right: Right bound of domain.
        iterations: Number of trisection iterations.
        
    Returns:
        Tuple of (optimal_x, maximum_y).
    """
    for _ in range(iterations):
        delta = (right - left) / 3.0
        mid1 = left + delta
        mid2 = right - delta

        # If mid1 is strictly less than mid2, peak cannot be in [left, mid1]
        if func(mid1) < func(mid2):
            left = mid1
        else:
            right = mid2

    best_x = (left + right) / 2.0
    return best_x, func(best_x)


def ternary_search_minimum(
    func: Callable[[float], float],
    left: float,
    right: float,
    iterations: int = 100
) -> Tuple[float, float]:
    """
    Finds the input x in [left, right] that minimizes a convex unimodal function func(x).
    
    Args:
        func: A unimodal function to minimize.
        left: Left bound of domain.
        right: Right bound of domain.
        iterations: Number of trisection iterations.
        
    Returns:
        Tuple of (optimal_x, minimum_y).
    """
    for _ in range(iterations):
        delta = (right - left) / 3.0
        mid1 = left + delta
        mid2 = right - delta

        # For minimization: if f(mid1) is GREATER than f(mid2),
        # minimum cannot be in [left, mid1]. Discard left third!
        if func(mid1) > func(mid2):
            left = mid1
        else:
            right = mid2

    best_x = (left + right) / 2.0
    return best_x, func(best_x)


# ==============================================================================
# 3. INDUSTRY-STANDARD / PRODUCTION EQUIVALENT (GOLDEN SECTION OPTIMIZATION)
# ==============================================================================

def golden_section_search_min(
    func: Callable[[float], float],
    left: float,
    right: float,
    tolerance: float = 1e-9
) -> Tuple[float, float]:
    """
    Production-standard derivative-free 1D scalar minimizer (Golden Section Search).
    
    Equivalent to scipy.optimize.minimize_scalar(method='golden').
    Unlike ternary search which evaluates func twice per iteration,
    Golden Section Search only evaluates func ONCE per iteration after initialization
    by reusing the previous probe point!
    """
    invphi = (math.sqrt(5) - 1) / 2  # 1 / phi ≈ 0.6180339887...
    invphi2 = (3 - math.sqrt(5)) / 2 # 1 / phi^2 ≈ 0.3819660112...

    h = right - left
    if h <= tolerance:
        mid = (left + right) / 2
        return mid, func(mid)

    c = left + invphi2 * h
    d = left + invphi * h
    yc = func(c)
    yd = func(d)

    while (right - left) > tolerance:
        if yc < yd:
            right = d
            d = c
            yd = yc
            h = invphi * h
            c = left + invphi2 * h
            yc = func(c)
        else:
            left = c
            c = d
            yc = yd
            h = invphi * h
            d = left + invphi * h
            yd = func(d)

    best_x = (left + right) / 2
    return best_x, func(best_x)


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATION WITH DEBUGGING COMMENTARY
# ==============================================================================

def ternary_search_buggy(arr: List[int], target: int) -> int:
    """
    Deliberately buggy implementation demonstrating common real-world flaws.
    
    Can you spot the bugs below?
    """
    left = 0
    right = len(arr) - 1

    # BUG 1: Using strict `<` instead of `<=`.
    # If the array has a single element (e.g. arr=[42], target=42),
    # left=0, right=0, 0 < 0 is False! The loop never runs and returns -1.
    while left < right:
        # BUG 2: Integer division without preserving boundaries.
        # Writing `(left + right) // 3` instead of `left + (right - left) // 3`
        # causes mid1 to be calculated relative to 0 instead of relative to `left`!
        # When left=6 and right=9, mid1 becomes (6+9)//3 = 5, which is OUTSIDE [left, right]!
        mid1 = (left + right) // 3
        mid2 = (left + right) * 2 // 3

        if arr[mid1] == target:
            return mid1
        if arr[mid2] == target:
            return mid2

        if target < arr[mid1]:
            # BUG 3: Off-by-one by not excluding mid1: `right = mid1`
            # Can cause an infinite loop when right - left == 1.
            right = mid1
        elif target > arr[mid2]:
            left = mid2
        else:
            left = mid1
            right = mid2

    return -1


# ==============================================================================
# 5. ADVANCED INTERVIEW VARIANT: FIND PEAK IN MOUNTAIN ARRAY (LEETCODE 852 / 162)
# ==============================================================================

def find_peak_in_mountain_array(arr: List[int]) -> int:
    """
    Finds the index of the peak element in a mountain array.
    A mountain array satisfies:
      arr[0] < arr[1] < ... < arr[peak] > arr[peak + 1] > ... > arr[-1]
      
    Solved using discrete Ternary Search in O(log3 N) time and O(1) space.
    """
    left = 0
    right = len(arr) - 1

    while right - left > 2:
        m1 = left + (right - left) // 3
        m2 = right - (right - left) // 3

        if arr[m1] < arr[m2]:
            # Peak cannot be in [left, m1]
            left = m1
        else:
            # Peak cannot be in [m2, right]
            right = m2

    # Linear scan across the remaining 3 or fewer elements
    peak_idx = left
    for i in range(left + 1, right + 1):
        if arr[i] > arr[peak_idx]:
            peak_idx = i

    return peak_idx


# ==============================================================================
# 6. TESTING & VALIDATION
# ==============================================================================

def run_tests() -> None:
    """Comprehensive test suite validating all implementations."""
    print("--- Running Ternary Search Test Suite ---")

    # 1. Discrete Array Tests (Iterative & Recursive)
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
    for idx, val in enumerate(sorted_array):
        assert ternary_search_iterative(sorted_array, val) == idx, f"Iterative failed for {val}"
        assert ternary_search_recursive(sorted_array, val, 0, len(sorted_array) - 1) == idx, f"Recursive failed for {val}"

    # Missing elements
    assert ternary_search_iterative(sorted_array, 1) == -1, "Found non-existent element 1"
    assert ternary_search_iterative(sorted_array, 50) == -1, "Found non-existent element 50"
    assert ternary_search_iterative(sorted_array, 100) == -1, "Found non-existent element 100"
    assert ternary_search_iterative([], 5) == -1, "Failed on empty list"
    assert ternary_search_iterative([42], 42) == 0, "Failed on single-element match"
    assert ternary_search_iterative([42], 99) == -1, "Failed on single-element mismatch"

    # 2. Continuous Maximization: f(x) = -(x - 3.5)^2 + 10  (Peak at x = 3.5, y = 10.0)
    parabola_max = lambda x: -((x - 3.5) ** 2) + 10.0
    opt_x, max_y = ternary_search_maximum(parabola_max, left=0.0, right=10.0)
    assert abs(opt_x - 3.5) < 1e-6, f"Maximization x error: got {opt_x}"
    assert abs(max_y - 10.0) < 1e-6, f"Maximization y error: got {max_y}"

    # 3. Continuous Minimization: f(x) = (x - 7.25)^2 + 4.0  (Minimum at x = 7.25, y = 4.0)
    parabola_min = lambda x: ((x - 7.25) ** 2) + 4.0
    opt_min_x, min_y = ternary_search_minimum(parabola_min, left=-5.0, right=20.0)
    assert abs(opt_min_x - 7.25) < 1e-6, f"Minimization x error: got {opt_min_x}"
    assert abs(min_y - 4.0) < 1e-6, f"Minimization y error: got {min_y}"

    # 4. Golden Section Search Comparison
    gs_x, gs_y = golden_section_search_min(parabola_min, left=-5.0, right=20.0)
    assert abs(gs_x - 7.25) < 1e-6, f"Golden Section Search x error: got {gs_x}"
    assert abs(gs_y - 4.0) < 1e-6, f"Golden Section Search y error: got {gs_y}"

    # 5. Mountain Array Peak Finding
    mountain = [0, 2, 5, 8, 14, 25, 20, 15, 7, 3, 1]
    peak_index = find_peak_in_mountain_array(mountain)
    assert peak_index == 5, f"Peak detection failed: expected 5, got {peak_index}"
    assert mountain[peak_index] == 25, "Peak value mismatch"

    # Smallest valid mountain array
    small_mountain = [1, 10, 2]
    assert find_peak_in_mountain_array(small_mountain) == 1

    print("[+] All Ternary Search unit tests passed successfully!")


# ==============================================================================
# 7. MAIN EDUCATIONAL TRACE & DEMO
# ==============================================================================

def main() -> None:
    """Executes test suite and prints educational step-by-step traces."""
    run_tests()

    print("\n" + "=" * 70)
    print("EDUCATIONAL TRACE: Continuous Ternary Search Maximization")
    print("Function: f(x) = -x^2 + 6x + 5 = -(x - 3)^2 + 14 (Global Peak at x = 3, y = 14)")
    print("Initial Search Domain: [-10.0, 10.0]")
    print("=" * 70)

    f = lambda x: -(x**2) + 6 * x + 5
    left = -10.0
    right = 10.0

    print(f"{'Step':<6} | {'Left':<10} | {'Mid1':<10} | {'Mid2':<10} | {'Right':<10} | {'f(Mid1)':<10} | {'f(Mid2)':<10} | {'Action'}")
    print("-" * 92)

    for step in range(1, 11):
        delta = (right - left) / 3.0
        m1 = left + delta
        m2 = right - delta
        y1 = f(m1)
        y2 = f(m2)

        if y1 < y2:
            action = "Discard Left 1/3 (left = mid1)"
            left_next = m1
            right_next = right
        else:
            action = "Discard Right 1/3 (right = mid2)"
            left_next = left
            right_next = m2

        print(f"{step:<6} | {left:<10.4f} | {m1:<10.4f} | {m2:<10.4f} | {right:<10.4f} | {y1:<10.4f} | {y2:<10.4f} | {action}")
        left, right = left_next, right_next

    est_peak = (left + right) / 2.0
    print("-" * 92)
    print(f"After 10 trisection steps, Estimated Peak: x ~= {est_peak:.6f}, f(x) ~= {f(est_peak):.6f}")
    print(f"True Analytical Peak: x = 3.000000, f(x) = 14.000000 (Error: {abs(est_peak - 3.0):.2e})")
    print("=" * 70)


if __name__ == "__main__":
    main()
