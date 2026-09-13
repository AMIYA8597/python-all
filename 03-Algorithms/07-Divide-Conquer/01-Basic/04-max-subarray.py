"""
# ==============================================================================
# LABORATORY: MAXIMUM SUBARRAY SUM (THE CROSSING SUBPROBLEM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The "Maximum Subarray Sum" problem asks you to find the contiguous subarray 
# within an array of numbers (containing negatives) that has the largest sum.
#
# You probably know Kadane's Algorithm, which solves this brilliantly in O(N) 
# time using a Greedy DP approach. So why do we care about a slower O(N log N) 
# Divide and Conquer approach?
#
# Because it teaches the "Crossing Subproblem"!
# In Merge Sort and Quick Sort, the subproblems were completely isolated. 
# But in some D&C algorithms, the optimal answer might literally STRADDLE the 
# boundary between the Left Half and the Right Half!
# 
# To solve this:
# 1. DIVIDE: Split the array in half.
# 2. CONQUER: Recursively find the Max Subarray purely in the Left Half, and 
#    purely in the Right Half.
# 3. COMBINE: Calculate the Max Subarray that physically CROSSES the midpoint.
#    Then, take the `max()` of all three!
#
# This exact "Crossing Midpoint" logic is the mathematical foundation for advanced 
# Computational Geometry algorithms like finding the "Closest Pair of Points" 
# in 2D space!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to mathematically analyze boundary-spanning data.
# - Implement the `find_max_crossing_subarray` function.
# - Combine 3 distinct sub-answers into 1 global answer.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIVIDE & CONQUER (CROSSING BOUNDARIES)
# ==============================================================================
def find_max_crossing_subarray(nums: List[int], low: int, mid: int, high: int) -> int:
    """
    Finds the maximum subarray that strictly crosses the `mid` index.
    Time Complexity: O(N) (Where N is high - low).
    """
    # 1. SCAN LEFT FROM MIDPOINT
    left_sum = -math.inf
    current_sum = 0
    # Loop from `mid` strictly backwards to `low`
    for i in range(mid, low - 1, -1):
        current_sum += nums[i]
        if current_sum > left_sum:
            left_sum = current_sum
            
    # 2. SCAN RIGHT FROM MIDPOINT
    right_sum = -math.inf
    current_sum = 0
    # Loop from `mid + 1` strictly forwards to `high`
    for j in range(mid + 1, high + 1):
        current_sum += nums[j]
        if current_sum > right_sum:
            right_sum = current_sum
            
    # The maximum subarray crossing the midpoint is simply the combination 
    # of the best left path and the best right path!
    return left_sum + right_sum


def max_subarray_dc(nums: List[int], low: int, high: int) -> int:
    """
    Time Complexity: O(N log N) (Proven via Master Theorem: T(n) = 2T(n/2) + O(n))
    Space Complexity: O(log N) for the recursion stack.
    """
    # 1. BASE CASE
    # If the array has only 1 element, that element IS the maximum subarray.
    if low == high:
        return nums[low]
        
    # 2. DIVIDE
    mid = low + (high - low) // 2
    
    # 3. CONQUER (Isolated Halves)
    # Find the max subarray purely on the left.
    left_max = max_subarray_dc(nums, low, mid)
    
    # Find the max subarray purely on the right.
    right_max = max_subarray_dc(nums, mid + 1, high)
    
    # 4. COMBINE (The Crossing Subproblem)
    # Find the max subarray that spans ACROSS the midpoint.
    cross_max = find_max_crossing_subarray(nums, low, mid, high)
    
    # The absolute largest of these three possibilities is mathematically 
    # guaranteed to be the global maximum subarray!
    return max(left_max, right_max, cross_max)


def demonstrate_max_subarray():
    section_header("Algorithm: Maximum Subarray Sum (D&C)")
    
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    
    print(f"Input Array: {nums}")
    print("\nExecuting Divide and Conquer Algorithm...")
    
    ans = max_subarray_dc(nums, 0, len(nums) - 1)
    
    print(f"\nMaximum Subarray Sum: {ans} (Expected: 6)")
    print("Explanation: The subarray [4, -1, 2, 1] sums to 6.")
    
    print("\nHow did the algorithm find this?")
    print("When the array was split at index 4 (Value -1):")
    print(" Left Max (-2, 1, -3, 4) -> 4")
    print(" Right Max (2, 1, -5, 4) -> 4")
    print(" Crossing Max (4, -1, 2, 1) -> 6")
    print(" max(4, 4, 6) returns 6!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the `find_max_crossing_subarray` scan OUTWARDS from the midpoint?
   Answer: Because a "crossing" subarray MUST physically contain the `mid` element and the `mid+1` element! If we started scanning from the edges `low` and `high` inwards, we wouldn't guarantee that the sums we find actually connect together in the middle. By starting at `mid` and radiating outwards, we ensure the left segment and right segment perfectly fuse into a single contiguous block.

2. Kadane's Algorithm is $O(N)$. D&C is $O(N \\log N)$. Why even learn D&C?
   Answer: Kadane's algorithm is a specific Greedy DP trick that only applies to 1D arrays. If you are asked to solve the "Maximum Submatrix Sum" in a 2D Grid, or the "Closest Pair of Points" in 2D space, the Greedy trick physically cannot map to 2D coordinates. You MUST use the Divide & Conquer "Crossing" logic (e.g., finding points that lie across the dividing plane).

3. Can this D&C approach be heavily parallelized?
   Answer: YES! And this is its secret superpower. Kadane's algorithm is $O(N)$, but it is strictly sequential; you cannot calculate step $i$ until step $i-1$ is finished. The Divide & Conquer approach allows you to send the `left_half` to CPU Core 1, and the `right_half` to CPU Core 2 simultaneously! In massive distributed systems (like Hadoop MapReduce), D&C algorithms can scale horizontally across thousands of servers, crushing sequential $O(N)$ algorithms in real-world time.
"""

if __name__ == "__main__":
    demonstrate_max_subarray()
    print("\n[SUCCESS] Laboratory: Max Subarray D&C Completed.")
