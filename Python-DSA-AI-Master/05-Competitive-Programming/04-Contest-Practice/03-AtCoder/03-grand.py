"""
AtCoder Grand Contest (AGC) Practice
====================================

Overview
--------
AtCoder Grand Contests are known for their high difficulty, mathematically intensive
problems, and elegant ad-hoc or constructive solutions. Unlike standard algorithm
contests, AGC problems often require a deep understanding of underlying properties,
invariants, or combinatorial logic rather than just knowing complex data structures.

Learning Objectives:
1. Understand how to approach mathematically heavy and constructive problems.
2. Learn to identify invariants or parity properties in problem statements.
3. Master the implementation of efficient, clean solutions to complex logic.
4. Practice a classic AGC-style problem involving arrays and operations.

Concept Explanation
-------------------
Consider a common AGC-style problem: "You are given an array. In one operation, you can
choose an element, and do something to it and its neighbors. Can you reach a target state?"
To solve such problems, we often look for:
- Invariants: Things that do not change regardless of the operation.
- Reversibility: Can we work backwards from the target state?
- Greedy Choice: Is there a uniquely optimal move at each step?

Below, we simulate a typical AGC-style algorithmic challenge: finding the optimal
sequence of operations to balance an array using a greedy approach, often seen in
problems involving sliding windows or prefix sum invariants.

Basic to Professional Implementation
------------------------------------
We implement a solver for an array balancing problem. The problem requires us to
make all elements equal to the median using the minimum number of increment/decrement
operations, a classic mathematical property.
"""

from typing import List
import statistics

def solve_agc_median_balance_basic(arr: List[int]) -> int:
    """
    Basic implementation of finding minimum operations to make all elements equal.
    Each operation is an increment or decrement by 1.
    
    Time Complexity: O(N log N) due to sorting for the median.
    Space Complexity: O(1) beyond the input array.
    """
    if not arr:
        return 0
    arr.sort()
    median = arr[len(arr) // 2]
    
    operations = 0
    for num in arr:
        operations += abs(num - median)
    return operations

def solve_agc_median_balance_pro(arr: List[int]) -> int:
    """
    Professional implementation: Handles edge cases, uses type hints, and 
    optimizes readability and safety.
    
    In a real AGC context, this might be a sub-problem for a larger 2D grid
    or tree structure, but the core logic remains essential.
    """
    if not arr:
        return 0
        
    # Using quickselect (O(N)) for median finding would be optimal,
    # but for simplicity and robust standard library usage, we use sort.
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    median = sorted_arr[n // 2]
    
    # Calculate sum of absolute differences efficiently
    # Can also be done using prefix sums if multiple queries are needed
    return sum(abs(x - median) for x in sorted_arr)


# --- Advanced Concept: Constructive Algorithms ---
def solve_agc_constructive_permutation(n: int) -> List[int]:
    """
    Constructive problem: Construct a permutation of 1 to N such that 
    the absolute difference between adjacent elements is strictly alternating
    between large and small, a common AGC constructive pattern.
    
    Example for N=5: [1, 5, 2, 4, 3]
    """
    result = []
    left, right = 1, n
    
    while left <= right:
        result.append(left)
        left += 1
        if left > right:
            break
        result.append(right)
        right -= 1
        
    return result


if __name__ == "__main__":
    # Tests and Assertions
    print("Testing AGC Median Balance...")
    arr = [1, 5, 2, 9, 3]
    # Sorted: 1, 2, 3, 5, 9 -> Median is 3
    # Ops: |1-3| + |2-3| + |3-3| + |5-3| + |9-3| = 2 + 1 + 0 + 2 + 6 = 11
    assert solve_agc_median_balance_pro(arr) == 11, "Basic test failed"
    assert solve_agc_median_balance_pro([]) == 0, "Empty array test failed"
    
    print("Testing AGC Constructive Permutation...")
    perm = solve_agc_constructive_permutation(5)
    assert perm == [1, 5, 2, 4, 3], f"Expected [1, 5, 2, 4, 3], got {perm}"
    print("All tests passed!")

"""
Complexity Analysis:
- `solve_agc_median_balance_pro`: 
  Time Complexity: O(N log N) for sorting.
  Space Complexity: O(N) for the sorted copy.
- `solve_agc_constructive_permutation`:
  Time Complexity: O(N) to construct the array.
  Space Complexity: O(N) to store the result.

Common Mistakes:
- Choosing the mean instead of the median for minimizing absolute differences.
- In constructive algorithms, failing to verify parity constraints for odd/even N.

Interview Challenge:
How would you solve the median balance problem if you were only allowed to operate
on contiguous subsegments instead of individual elements? (Hint: Consider the difference array).
"""
