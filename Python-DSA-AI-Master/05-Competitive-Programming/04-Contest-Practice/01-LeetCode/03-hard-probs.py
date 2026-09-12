"""
LeetCode Hard Problems - Comprehensive Guide
=============================================

What is this?
This module covers advanced problem-solving techniques commonly encountered in LeetCode Hard problems.
It provides a deep dive into algorithm design, covering topics like complex Dynamic Programming, 
Advanced Graph Algorithms, and clever Data Structure combinations.

Why does it exist?
In competitive programming and top-tier tech interviews (FAANG), "Hard" problems are used to 
distinguish candidates who can write code from those who can engineer highly optimized, 
scalable algorithms under time and space constraints.

Industry Use Cases:
- Optimization engines (e.g., route planning, resource allocation)
- High-performance text search and natural language processing engines
- Network flow optimization and state-space search in AI

Learning Objectives:
- Master advanced Dynamic Programming with state reduction.
- Implement complex backtracking with pruning.
- Understand how to leverage multiple data structures simultaneously.
- Analyze time and space complexity rigorously.

Concept Explanation:
Beginner: Hard problems often seem impossible at first glance. They usually require breaking down 
the problem into smaller, manageable subproblems (DP) or systematically exploring all possibilities 
while quickly abandoning dead ends (Backtracking/Pruning).

Advanced: Solving hard problems requires recognizing the underlying mathematical structure or graph 
topology. It involves optimizing time complexity from O(N^2) to O(N log N) or O(N) using techniques 
like Monotonic Stacks, Sliding Windows, or specialized trees (Segment Trees, Tries).

Example Problem: Trapping Rain Water
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it can trap after raining.
"""

from typing import List

# ---------------------------------------------------------------------------
# BASIC IMPLEMENTATION (O(N) Time, O(N) Space using prefix arrays)
# ---------------------------------------------------------------------------
def trap_water_basic(height: List[int]) -> int:
    """
    Computes the trapped water using left and right max arrays.
    
    Time Complexity: O(N) where N is the length of height.
    Space Complexity: O(N) for storing left_max and right_max arrays.
    """
    if not height:
        return 0
    
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(height[i], left_max[i - 1])
        
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(height[i], right_max[i + 1])
        
    trapped_water = 0
    for i in range(n):
        trapped_water += min(left_max[i], right_max[i]) - height[i]
        
    return trapped_water

# ---------------------------------------------------------------------------
# PROFESSIONAL IMPLEMENTATION (O(N) Time, O(1) Space using two pointers)
# ---------------------------------------------------------------------------
def trap_water_optimized(height: List[int]) -> int:
    """
    Computes the trapped water using a highly optimized two-pointer approach.
    
    This avoids the O(N) auxiliary space by maintaining the maximums on the fly
    from both the left and right ends.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not height:
        return 0
        
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    trapped_water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            trapped_water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            trapped_water += right_max - height[right]
            
    return trapped_water


# ---------------------------------------------------------------------------
# ADVANCED CONCEPT: N-Queens Problem (Backtracking)
# ---------------------------------------------------------------------------
class NQueensSolver:
    """
    Solves the N-Queens problem using optimized backtracking.
    Places N queens on an NxN chessboard such that no two queens attack each other.
    """
    
    def solveNQueens(self, n: int) -> List[List[str]]:
        def backtrack(row: int, diagonals: set, anti_diagonals: set, cols: set, state: List[List[str]]):
            if row == n:
                ans.append(["".join(row) for row in state])
                return
            
            for col in range(n):
                curr_diagonal = row - col
                curr_anti_diagonal = row + col
                
                if col in cols or curr_diagonal in diagonals or curr_anti_diagonal in anti_diagonals:
                    continue
                    
                cols.add(col)
                diagonals.add(curr_diagonal)
                anti_diagonals.add(curr_anti_diagonal)
                state[row][col] = 'Q'
                
                backtrack(row + 1, diagonals, anti_diagonals, cols, state)
                
                cols.remove(col)
                diagonals.remove(curr_diagonal)
                anti_diagonals.remove(curr_anti_diagonal)
                state[row][col] = '.'

        ans = []
        empty_board = [["."] * n for _ in range(n)]
        backtrack(0, set(), set(), set(), empty_board)
        return ans


# ---------------------------------------------------------------------------
# COMMON MISTAKES & PERFORMANCE CONSIDERATIONS
# ---------------------------------------------------------------------------
# 1. Memory Leaks in Recursion: When passing large data structures in recursion,
#    ensure you are passing by reference and backtracking correctly, rather than 
#    creating deep copies at each stack frame, which blows up time and space.
# 2. String Concatenation: In Python, strings are immutable. Repeatedly adding 
#    to a string in a loop takes O(N^2) time. Use lists and "".join() instead.
# 3. Security: In competitive programming, security is rarely a concern, but in 
#    production, recursive backtracking must be bounded (e.g., maximum depth limit)
#    to prevent stack overflow attacks or Denial of Service (DoS).

# ---------------------------------------------------------------------------
# INTERVIEW QUESTIONS & EXERCISES
# ---------------------------------------------------------------------------
# Q1: How does the two-pointer approach for Trapping Rain Water guarantee correctness?
# A1: By maintaining `left_max` and `right_max`, the bottleneck is always the smaller 
#     of the two. If `left_max < right_max`, we know the water column above `left` 
#     is strictly bounded by `left_max`, regardless of what happens in the middle.
# 
# Exercise: Modify the Trapping Rain Water problem to 3D (Trapping Rain Water II).
# Hint: You will need a Min-Heap (Priority Queue) to process the boundary cells first.

if __name__ == "__main__":
    # Test Trapping Rain Water
    heights = [0,1,0,2,1,0,1,3,2,1,2,1]
    assert trap_water_basic(heights) == 6, "Basic Trapping Water Failed"
    assert trap_water_optimized(heights) == 6, "Optimized Trapping Water Failed"
    
    # Test N-Queens
    solver = NQueensSolver()
    solutions = solver.solveNQueens(4)
    assert len(solutions) == 2, "4-Queens should have exactly 2 distinct solutions"
    
    print("All LeetCode Hard tests passed successfully.")
