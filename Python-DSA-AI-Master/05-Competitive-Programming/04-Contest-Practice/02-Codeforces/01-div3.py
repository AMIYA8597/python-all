"""
Codeforces Div 3 Contest Practice
==================================

What is this?
This module focuses on problems commonly found in Codeforces Division 3 contests. 
Div 3 contests are designed for beginners and intermediate programmers, focusing on 
fundamental algorithms, basic math, greedy approaches, string manipulation, and ad-hoc logic.

Why does it exist?
Codeforces is the premier competitive programming platform. Div 3 helps build a strong 
foundation in translating mathematical and logical ideas into code rapidly and without bugs.
It teaches resilience against edge cases.

Industry Use Cases:
- Rapid prototyping of business logic
- Data parsing and sanitization (string manipulation)
- Basic optimization problems (greedy algorithms) in supply chain or scheduling

Learning Objectives:
- Master fast input/output in Python for competitive programming.
- Develop intuition for greedy algorithms and when they are optimal.
- Handle edge cases in ad-hoc problems effectively.
- Understand parity, basic number theory, and modular arithmetic.

Concept Explanation:
Beginner: Ad-hoc problems require simulating a process exactly as described. Greedy 
problems require finding a local optimum at each step that leads to a global optimum.

Advanced: Even in "simple" problems, performance matters. Python's default `input()` 
is slow. Using `sys.stdin.read` is crucial. Furthermore, identifying that a problem 
requires O(1) mathematical calculation instead of O(N) simulation separates the winners.

Example Problem: Maximize the Minimum
Given an array, we can perform operations to balance it. We want to maximize the minimum element.
"""

import sys
from typing import List

# ---------------------------------------------------------------------------
# BASIC IMPLEMENTATION (Simulation - may Time Out)
# ---------------------------------------------------------------------------
def solve_basic(arr: List[int], k: int) -> int:
    """
    Simulate adding 1 to the minimum element k times.
    Time Complexity: O(K * N) where K is operations, N is array size.
    Space Complexity: O(1)
    """
    if not arr:
        return 0
    arr_copy = arr.copy()
    for _ in range(k):
        min_idx = arr_copy.index(min(arr_copy))
        arr_copy[min_idx] += 1
    return min(arr_copy)

# ---------------------------------------------------------------------------
# PROFESSIONAL IMPLEMENTATION (Math / Greedy - O(N log N) or O(N))
# ---------------------------------------------------------------------------
def solve_optimized(arr: List[int], k: int) -> int:
    """
    Optimized approach using sorting and filling the 'valleys'.
    Time Complexity: O(N log N) due to sorting.
    Space Complexity: O(1) or O(N) depending on sort implementation.
    """
    if not arr:
        return 0
    n = len(arr)
    arr.sort()
    
    for i in range(1, n):
        # Number of elements at the current minimum level
        count = i 
        # Difference in height to the next level
        diff = arr[i] - arr[i-1] 
        
        if diff == 0:
            continue
            
        cost = count * diff
        
        if k >= cost:
            k -= cost
        else:
            # Cannot reach the next level, distribute remaining k evenly
            return arr[i-1] + k // count
            
    # If we leveled the whole array and still have k left
    return arr[-1] + k // n

# ---------------------------------------------------------------------------
# COMMON MISTAKES & PERFORMANCE CONSIDERATIONS
# ---------------------------------------------------------------------------
# 1. Fast I/O: Python's `input()` is too slow for 10^5 inputs. 
#    Use `sys.stdin.read().split()` to read all tokens into memory instantly.
# 2. Integer Overflow: Python handles arbitrarily large integers, but operations
#    on very large numbers take O(digits) time. However, in C++/Java, overflow
#    is a major bug source.
# 3. Off-by-one errors: Highly common in greedy and string manipulation.

# ---------------------------------------------------------------------------
# INTERVIEW QUESTIONS & EXERCISES
# ---------------------------------------------------------------------------
# Q1: Why is sorting the array useful in the optimized approach?
# A1: It groups the smallest elements together, allowing us to mathematically 
#     calculate how many operations it takes to level them up to the next smallest 
#     element, reducing O(K) steps into O(1) mathematical jumps.
#
# Exercise: Implement a solution using a Min-Heap (heapq). 
# Compare its performance to the sorting approach.

if __name__ == "__main__":
    arr = [1, 2, 4]
    k = 5
    # Basic: [1,2,4] -> min is 1. +1 -> [2,2,4]. min is 2. +2 -> [3,3,4]. min is 3. +2 -> [4,4,4]. Ans: 4.
    assert solve_basic(arr, k) == 4, "Basic implementation failed"
    assert solve_optimized(arr.copy(), k) == 4, "Optimized implementation failed"
    
    print("All Codeforces Div 3 tests passed successfully.")
