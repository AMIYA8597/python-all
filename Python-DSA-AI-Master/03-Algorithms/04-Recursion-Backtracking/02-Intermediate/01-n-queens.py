"""
Module: N-Queens Problem

Learning Objectives:
- Understand backtracking as a problem-solving strategy.
- Implement the N-Queens problem efficiently.
- Learn to manage states and prune search spaces.

Concept Explanation:
The N-Queens problem asks how to place N chess queens on an N×N chessboard so that no two queens threaten each other. Thus, a solution requires that no two queens share the same row, column, or diagonal. Backtracking builds candidates incrementally and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution.
"""
import time
from typing import List

# Basic Implementation
def solveNQueens_basic(n: int) -> List[List[str]]:
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def backtrack(row, board):
        if row == n:
            res.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board.append(col)
                backtrack(row + 1, board)
                board.pop()

    res = []
    backtrack(0, [])
    
    # Format the output
    formatted_res = []
    for board in res:
        formatted_board = ["." * col + "Q" + "." * (n - col - 1) for col in board]
        formatted_res.append(formatted_board)
    return formatted_res

# Intermediate Implementation (Optimized with Sets)
def solveNQueens_intermediate(n: int) -> List[List[str]]:
    cols = set()
    pos_diag = set() # row + col
    neg_diag = set() # row - col
    
    res = []
    board = [["."] * n for _ in range(n)]
    
    def backtrack(row):
        if row == n:
            copy = ["".join(r) for r in board]
            res.append(copy)
            return
        
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = "Q"
            
            backtrack(row + 1)
            
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)
            board[row][col] = "."
            
    backtrack(0)
    return res

# Advanced Implementation (Bitmasking)
def solveNQueens_advanced(n: int) -> int:
    # Returns count of solutions for performance
    count = 0
    def solve(row, cols, pos_diag, neg_diag):
        nonlocal count
        if row == n:
            count += 1
            return
        
        available_positions = ((1 << n) - 1) & ~(cols | pos_diag | neg_diag)
        while available_positions:
            pos = available_positions & -available_positions
            available_positions -= pos
            solve(row + 1, cols | pos, (pos_diag | pos) << 1, (neg_diag | pos) >> 1)
            
    solve(0, 0, 0, 0)
    return count

def run_tests():
    print("Testing Basic Implementation...")
    assert len(solveNQueens_basic(4)) == 2
    print("Testing Intermediate Implementation...")
    assert len(solveNQueens_intermediate(4)) == 2
    print("Testing Advanced Implementation...")
    assert solveNQueens_advanced(8) == 92
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
