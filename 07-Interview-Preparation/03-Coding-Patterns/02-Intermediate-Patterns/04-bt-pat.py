"""
Backtracking Pattern

Learning Objectives:
1. Understand the core concept of Backtracking (explore all paths and backtrack if not valid).
2. Learn the common template for backtracking problems.
3. Master solving Permutations, Combinations, and Subsets.
4. Analyze time and space complexity.
5. Learn state restoration.

Concept Explanation:
Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, removing those solutions that fail to satisfy the constraints of the problem at any point of time. It's essentially an exhaustive search (DFS) with pruning.
"""

from typing import List

# Basic Implementation: Subsets
def subsets(nums: List[int]) -> List[List[int]]:
    """Time: O(N * 2^N), Space: O(N)"""
    res = []
    
    def backtrack(start: int, path: List[int]):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop() # Restore state (Backtrack)
            
    backtrack(0, [])
    return res

# Intermediate Implementation: Permutations
def permutations(nums: List[int]) -> List[List[int]]:
    """Time: O(N * N!), Space: O(N)"""
    res = []
    
    def backtrack(path: List[int]):
        if len(path) == len(nums):
            res.append(path[:])
            return
            
        for i in range(len(nums)):
            if nums[i] in path:
                continue
            path.append(nums[i])
            backtrack(path)
            path.pop()
            
    backtrack([])
    return res

# Advanced Implementation: N-Queens
def solveNQueens(n: int) -> List[List[str]]:
    """Time: O(N!), Space: O(N^2)"""
    col = set()
    posDiag = set() # (r + c)
    negDiag = set() # (r - c)
    
    res = []
    board = [["."] * n for _ in range(n)]
    
    def backtrack(r: int):
        if r == n:
            copy = ["".join(row) for row in board]
            res.append(copy)
            return
            
        for c in range(n):
            if c in col or (r + c) in posDiag or (r - c) in negDiag:
                continue
                
            col.add(c)
            posDiag.add(r + c)
            negDiag.add(r - c)
            board[r][c] = "Q"
            
            backtrack(r + 1)
            
            col.remove(c)
            posDiag.remove(r + c)
            negDiag.remove(r - c)
            board[r][c] = "."
            
    backtrack(0)
    return res

# Edge Cases to Handle:
# 1. Duplicate elements in input (need sorting and skip condition).
# 2. Empty input arrays.

# Interview Challenge: Combination Sum
def combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    res = []
    
    def backtrack(start: int, path: List[int], total: int):
        if total == target:
            res.append(path[:])
            return
        if total > target:
            return
            
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, total + candidates[i])
            path.pop()
            
    backtrack(0, [], 0)
    return res

def run_tests():
    assert [1] in subsets([1])
    assert len(subsets([1, 2, 3])) == 8
    
    assert len(permutations([1, 2, 3])) == 6
    
    assert len(solveNQueens(4)) == 2
    
    c_sum = combination_sum([2, 3, 6, 7], 7)
    assert [7] in c_sum and [2, 2, 3] in c_sum
    
    print("All Backtracking tests passed!")

if __name__ == "__main__":
    run_tests()
