"""
Module: Sudoku Solver (Advanced Backtracking)

================================================================================
1. INTUITION & REAL-WORLD ANALOGY
================================================================================
Imagine you are assigning desks in a large corporate office space.
Constraints:
1. No two people from the same department can sit in the same row.
2. No two people from the same department can sit in the same column.
3. No two people from the same department can sit in the same 3x3 isolated pod.

You start assigning seats one by one. Eventually, you might reach a desk where 
every possible department assignment violates one of the rules. What do you do? 
You undo the previous assignment (maybe even a few) and try a different department 
for that person. This process of systematic trial, error, and undoing is the 
heart of BACKTRACKING. 

Sudoku is the ultimate backtracking problem:
- Try a number (1-9) in an empty cell.
- Check if it violates any row, column, or 3x3 box constraints.
- If it works, recursively proceed to the next empty cell.
- If we get stuck, backtrack! Wipe the cell clean and try the next valid number.

================================================================================
2. FORMAL EXPLANATION
================================================================================
Sudoku is a constraint satisfaction problem (CSP). We explore a decision tree where:
- Each level of the tree represents an empty cell on the board.
- Each branch represents placing a digit (1-9) in that cell.
- Pruning happens when a digit violates Sudoku constraints (Row, Col, Box).

State Space Reduction:
A naive approach would generate 9^(number of empty cells) configurations and 
check each. By checking constraints BEFORE making a recursive call, we prune 
massive branches of the decision tree, converting an impossibly slow algorithm 
into one that solves most boards in milliseconds.

For O(1) constraint checking, we use Hash Sets (or boolean arrays) to keep 
track of the digits currently placed in each row, column, and 3x3 sub-box.

Sub-box Indexing Formula:
A 9x9 board has 9 sub-boxes (0 to 8). Given a cell at (r, c), which box is it in?
box_index = (r // 3) * 3 + (c // 3)
- (r // 3) gives the row of the box (0, 1, or 2).
- (c // 3) gives the col of the box (0, 1, or 2).
- Multiplying the box row by 3 flattens this 2D box grid into a 1D index (0-8).

================================================================================
3. IMPLEMENTATION
================================================================================
"""
from typing import List

def solveSudoku(board: List[List[str]]) -> None:
    """
    Solves a Sudoku puzzle in-place using backtracking.
    
    Args:
        board (List[List[str]]): A 9x9 grid representing the Sudoku board.
                                 Empty cells are denoted by '.'.
    """
    # Hash sets to keep track of seen numbers in rows, cols, and boxes
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    # Store empty cells to avoid scanning the board repeatedly
    empty_cells = []
    
    # 1. Initialization phase: Populate constraints and empty cells
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                empty_cells.append((r, c))
            else:
                val = board[r][c]
                rows[r].add(val)
                cols[c].add(val)
                box_idx = (r // 3) * 3 + (c // 3)
                boxes[box_idx].add(val)
                
    def backtrack(idx: int) -> bool:
        # BASE CASE: If we've successfully filled all empty cells, we're done!
        if idx == len(empty_cells):
            return True
        
        # Current cell to fill
        r, c = empty_cells[idx]
        box_idx = (r // 3) * 3 + (c // 3)
        
        # Explore all possibilities: Digits 1 through 9
        for val in map(str, range(1, 10)):
            # Constraint check: Is it safe to place `val` here?
            if val not in rows[r] and val not in cols[c] and val not in boxes[box_idx]:
                
                # 1. MAKE A CHOICE (Place the digit)
                board[r][c] = val
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_idx].add(val)
                
                # 2. EXPLORE (Recurse to the next cell)
                # If this path leads to a solution, propagate the success upward
                if backtrack(idx + 1):
                    return True
                
                # 3. BACKTRACK (Undo the choice)
                # If we are here, the current path failed down the line. Clean up!
                board[r][c] = '.'
                rows[r].remove(val)
                cols[c].remove(val)
                boxes[box_idx].remove(val)
                
        # If no digit from 1-9 works, this path is a dead end. Return False.
        return False
        
    # Kick off the backtracking starting from the first empty cell
    backtrack(0)


"""
================================================================================
4. COMPLEXITY ANALYSIS
================================================================================
Time Complexity: O(9^(Empty Cells))
- In the worst case, we might have to try 9 possibilities for each empty cell.
- The maximum number of empty cells is 81, making the upper bound O(9^81).
- However, because we constantly prune invalid choices using our O(1) set lookups, 
  the actual time taken is significantly less.

Space Complexity: O(1) or O(81) -> O(1)
- The board is always 9x9.
- We use 3 arrays of 9 hash sets. At most, each set stores 9 digits. 
- Maximum empty cells list size is 81.
- Recursion call stack max depth is 81.
- Because the grid size is fixed (9x9), space is technically O(1).

================================================================================
5. DEBUGGING & COMMON MISTAKES
================================================================================
Common Mistake 1: Forgetting to undo the choice (Backtrack step).
- If you don't remove `val` from `rows`, `cols`, and `boxes`, your constraints
  will permanently block valid numbers in completely unrelated branches.

Common Mistake 2: Returning early from the recursion loop without checking all.
- Remember, backtracking means iterating through ALL possible valid candidates.
- You must return False ONLY AFTER trying digits 1-9 and failing for all.

Common Mistake 3: Modifying the board incorrectly.
- Sudoku cells contain strings (e.g., "5"), not integers. Using integers might 
  cause type mismatch errors depending on the language/platform constraints.

Debugging Tip:
- If your solver fails, print the cell coordinates (r, c) when it returns False.
- The highest index it reaches before collapsing backward shows exactly where the 
  impossible state occurred!

================================================================================
6. ACTIVE RECALL & MEMORY ANCHORS
================================================================================
- **Memory Anchor**: "Choose, Recurse, Undo." This is the Holy Trinity of 
  Backtracking algorithms.
- **Active Recall**: What is the mathematical formula to map a 2D coordinate 
  (r, c) into a 1D Sub-Box index for a 9x9 board?
  -> (r // 3) * 3 + (c // 3)
- **Active Recall**: Why use an array of Sets instead of scanning the board?
  -> Scanning takes O(9). HashSet lookup takes O(1). Across millions of 
     recursive calls, this transforms the algorithm from practically unusable 
     to lightning fast.
"""

def run_tests():
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    
    print("Initial Board:")
    for row in board:
        print(" ".join(row))
        
    solveSudoku(board)
    
    print("\nSolved Board:")
    for row in board:
        print(" ".join(row))
        
    # Verify a few cells
    assert board[0][0] == "5"
    assert board[0][2] == "4" # It should fill 4 here
    assert board[8][8] == "9"
    print("\n[SUCCESS] All tests passed.")

if __name__ == "__main__":
    run_tests()
