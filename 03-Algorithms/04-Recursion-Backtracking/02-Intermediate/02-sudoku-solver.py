"""
# ==============================================================================
# LABORATORY: SUDOKU SOLVER (BACKTRACKING WITH EARLY EXIT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen Backtracking generate ALL solutions (like finding all N-Queens 
# configurations). 
# 
# But what if you only want ONE solution? (Like solving a Sudoku puzzle).
# If the algorithm finds the solution deep inside the recursion tree, how do you 
# stop the other 4 Billion branches from continuing to execute?
#
# You use an **Early Exit (Boolean Propagation)**.
# Instead of `def backtrack():`, you write `def backtrack() -> bool:`.
# If a branch hits the success state, it returns `True`. Every parent function 
# checks the return value, and if it sees `True`, it instantly returns `True` 
# itself! The `True` cascades all the way to the top of the Call Stack in 
# microseconds, instantly terminating the entire algorithm.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Early Exit (Boolean Propagation).
# - Understand 2D Grid Traversal.
# - Master the mathematics of 3x3 Subgrids: `(row // 3) * 3`.
#
# ==============================================================================
"""

from typing import List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STATE VALIDATION (PRUNING)
# ==============================================================================
def is_valid(board: List[List[str]], row: int, col: int, char: str) -> bool:
    """
    Checks if placing `char` at board[row][col] is mathematically legal.
    Time Complexity: O(9) -> O(1) Constant time.
    """
    # 1. Check Row and Column simultaneously
    for i in range(9):
        # Is the number already in this row?
        if board[row][i] == char:
            return False
        # Is the number already in this column?
        if board[i][col] == char:
            return False
            
    # 2. Check the 3x3 Subgrid
    # MATH TRICK: How do we find the top-left corner of the subgrid?
    # If row=5, (5 // 3) = 1. 1 * 3 = 3. The subgrid starts at row 3!
    # If col=7, (7 // 3) = 2. 2 * 3 = 6. The subgrid starts at col 6!
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == char:
                return False
                
    return True


# ==============================================================================
# 4. THE EARLY EXIT ENGINE
# ==============================================================================
def solve_sudoku(board: List[List[str]]) -> bool:
    """
    Modifies the board In-Place.
    Returns True the microsecond it finds a valid solution.
    Time Complexity: O(9^(Empty Cells)) Worst Case.
    Space Complexity: O(Empty Cells) Call Stack.
    """
    
    # 1. Find the next empty cell (represented by '.')
    for row in range(9):
        for col in range(9):
            
            if board[row][col] == '.':
                
                # 2. We found an empty cell! Try numbers 1 through 9.
                for num in range(1, 10):
                    char = str(num)
                    
                    if is_valid(board, row, col, char):
                        
                        # --- CHOOSE ---
                        board[row][col] = char
                        
                        # --- EXPLORE ---
                        # If this recursive path eventually leads to a solved board, 
                        # it will return True.
                        if solve_sudoku(board) is True:
                            # --- THE EARLY EXIT ---
                            # Do NOT keep looping. Do NOT backtrack.
                            # Instantly pass the True upwards!
                            return True
                            
                        # --- UNCHOOSE ---
                        # The path failed (it returned False).
                        # Revert the cell to empty and try the next number.
                        board[row][col] = '.'
                        
                # 3. FATAL DEAD END
                # We tried 1 through 9. NONE of them were valid.
                # This means a previous decision higher up in the tree was wrong!
                # We must return False to tell the parent function to backtrack.
                return False
                
    # 4. BASE CASE (SUCCESS)
    # The nested for-loops finished without finding a single '.' empty cell!
    # The board is completely full and completely valid!
    return True


# ==============================================================================
# 5. VISUALIZATION
# ==============================================================================
def print_board(board: List[List[str]]) -> None:
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        row_str = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            row_str += board[i][j] + " "
        print(row_str)

def demonstrate_sudoku():
    section_header("Algorithm: Sudoku Solver (Early Exit)")
    
    # Unsolved Sudoku Board
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
    
    print("Initial Board:\n")
    print_board(board)
    
    print("\nExecuting Backtracking Engine...\n")
    solve_sudoku(board)
    
    print("Solved Board:\n")
    print_board(board)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `solve_sudoku` return `bool` instead of just returning the solved board?
   Answer: To trigger the "Early Exit" cascade. The Call Stack might be 50 layers deep. When layer 50 successfully fills the final square, it returns `True`. Layer 49 sees `if solve_sudoku() is True: return True`, so it instantly returns `True`. This cascades up to Layer 1 in microseconds, halting the algorithm and freezing the globally shared `board` array in its solved state.

2. Why is the time complexity exactly $O(9^E)$ where E is empty cells?
   Answer: The branching factor is 9 (we try numbers 1 through 9). The maximum depth of the recursion tree is the number of empty cells (E). In a Decision Tree, the worst-case number of nodes explored is $BranchingFactor^{Depth}$.

3. Can we optimize this algorithm further?
   Answer: Yes! Right now, the algorithm scans from Top-Left to Bottom-Right sequentially. This is naive. A human plays Sudoku by looking for the square that has the FEWEST possible options remaining. This is called the "Minimum Remaining Values (MRV)" Heuristic. If we change step 1 to scan the board and find the empty cell with the most constraints, the branching factor drops from 9 to 1 or 2, massively speeding up the algorithm!
"""

if __name__ == "__main__":
    demonstrate_sudoku()
    print("\n[SUCCESS] Laboratory: Sudoku Solver Completed.")
