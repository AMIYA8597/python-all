"""
Codeforces Div 2 Contest Practice
==================================

What is this?
This module tackles Codeforces Division 2 problems. These problems are significantly 
harder than Div 3, requiring strong knowledge of algorithms like Graph Theory (BFS/DFS, 
Shortest Paths), advanced Dynamic Programming, Binary Search on Answers, and Number Theory.

Why does it exist?
Div 2 problems test the ability to construct complex algorithms under pressure. 
They frequently appear in advanced coding assessments for Quantitative Finance (Quant) 
roles and Senior Software Engineering positions.

Industry Use Cases:
- Network routing and latency optimization (Graph algorithms).
- Capacity planning and resource bounds (Binary Search on Answer).
- Cryptography and hashing (Number Theory).

Learning Objectives:
- Master Binary Search on a monotonic function (Binary Search on Answer).
- Implement efficient Graph traversal algorithms avoiding recursive limits.
- Understand state transitions in multi-dimensional Dynamic Programming.

Concept Explanation:
Beginner: You know binary search finds an element in a sorted array. "Binary Search on Answer" 
extends this: if you can check if a given answer 'X' is valid in O(N) time, and the validity 
is monotonic (e.g., if X is possible, X+1 is also possible), you can binary search the answer in O(N log(Max)).

Advanced: For graphs, Python's recursion limit (1000) often causes RecursionError in deep DFS. 
Professional CP in Python requires iterative DFS or artificially raising `sys.setrecursionlimit`. 
However, iterative is preferred to avoid memory overhead.

Example Problem: Minimum Capacity to Ship Packages Within D Days
"""

import sys
from typing import List

# ---------------------------------------------------------------------------
# BASIC IMPLEMENTATION (Linear Search - O(N * Max_Cap))
# ---------------------------------------------------------------------------
def ship_packages_basic(weights: List[int], days: int) -> int:
    """
    Finds the minimum capacity by testing every capacity starting from the max weight.
    Time Complexity: O(N * Sum(weights)) - Very Slow
    Space Complexity: O(1)
    """
    def can_ship(capacity: int) -> bool:
        current_weight = 0
        days_needed = 1
        for w in weights:
            if current_weight + w > capacity:
                days_needed += 1
                current_weight = w
            else:
                current_weight += w
        return days_needed <= days

    max_w = max(weights)
    sum_w = sum(weights)
    
    for cap in range(max_w, sum_w + 1):
        if can_ship(cap):
            return cap
    return sum_w

# ---------------------------------------------------------------------------
# PROFESSIONAL IMPLEMENTATION (Binary Search on Answer - O(N log(Sum)))
# ---------------------------------------------------------------------------
def ship_packages_optimized(weights: List[int], days: int) -> int:
    """
    Uses Binary Search on the Answer.
    The minimum possible capacity is max(weights) (must carry the heaviest item).
    The maximum possible capacity is sum(weights) (carry everything in 1 day).
    
    Time Complexity: O(N * log(Sum(weights) - max(weights)))
    Space Complexity: O(1)
    """
    def can_ship(capacity: int) -> bool:
        current_weight = 0
        days_needed = 1
        for w in weights:
            if current_weight + w > capacity:
                days_needed += 1
                current_weight = w
                if days_needed > days: # Early exit
                    return False
            else:
                current_weight += w
        return True

    left, right = max(weights), sum(weights)
    ans = right
    
    while left <= right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            ans = mid
            right = mid - 1 # Try to find a smaller capacity
        else:
            left = mid + 1  # Capacity too small, increase it
            
    return ans

# ---------------------------------------------------------------------------
# COMMON MISTAKES & PERFORMANCE CONSIDERATIONS
# ---------------------------------------------------------------------------
# 1. Binary Search Bounds: Setting the initial `left` and `right` bounds incorrectly 
#    is the #1 cause of bugs in BS on Answer.
# 2. Infinite Loops: Ensure your `left <= right` and mid calculations update 
#    correctly to prevent the search space from stalling. `mid = left + (right - left) // 2` 
#    prevents integer overflow in languages like Java/C++, though Python handles it.
# 3. Graph DFS in Python: Always use `sys.setrecursionlimit(200000)` if you must use 
#    recursive DFS in a Codeforces Div 2 problem, as tree depths can reach 10^5.

# ---------------------------------------------------------------------------
# INTERVIEW QUESTIONS & EXERCISES
# ---------------------------------------------------------------------------
# Q1: How do you identify a problem can be solved with "Binary Search on Answer"?
# A1: Look for keywords like "minimize the maximum" or "maximize the minimum". 
#     Also, check if the condition is monotonic: if 'X' works, does every value > 'X' 
#     also work? If so, you can binary search the threshold.
#
# Exercise: Write an iterative Depth First Search (DFS) for a generic tree represented
# as an adjacency list to find the diameter of the tree.

if __name__ == "__main__":
    weights = [1,2,3,4,5,6,7,8,9,10]
    days = 5
    # The capacity should be 15:
    # Day 1: 1, 2, 3, 4, 5 (sum: 15)
    # Day 2: 6, 7 (sum: 13)
    # Day 3: 8
    # Day 4: 9
    # Day 5: 10
    assert ship_packages_basic(weights, days) == 15, "Basic implementation failed"
    assert ship_packages_optimized(weights, days) == 15, "Optimized implementation failed"
    
    print("All Codeforces Div 2 tests passed successfully.")
