"""
# ==============================================================================
# LABORATORY: N-QUEENS & BACKTRACKING PRUNING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The N-Queens problem asks: "Can you place N Queens on an NxN chessboard so 
# that none of them can attack each other?" (Queens can move horizontally, 
# vertically, and diagonally).
#
# If you try to brute-force this by placing N queens on N^2 squares randomly, 
# there are (N^2 choose N) combinations. For an 8x8 board, that is 4 Billion 
# combinations. Your program will crash.
#
# But Backtracking gives us a superpower: **Pruning**.
#
# When we place the 1st Queen at (0, 0), it instantly invalidates the entire 
# first row, first column, and main diagonal. If we attempt to place the 2nd Queen 
# at (0, 1), we check our rules first. It's invalid! We immediately abort that 
# branch. We "Pruned" millions of dead-end combinations in a single millisecond.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand State Validation (Pruning).
# - Understand Mathematical Diagonal tracking (O(1) lookups).
# - Implement the fully optimized N-Queens backtracking engine.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. N-QUEENS (O(1) VALIDATION SETS)
# ==============================================================================
def solve_n_queens(n: int) -> List[List[str]]:
    """
    Time Complexity: O(N!) Worst case (but practically much faster due to pruning).
    Space Complexity: O(N) for Call Stack and Sets.
    """
    
    # We need to quickly check if a column or diagonal is already under attack.
    # We could loop over the board O(N) every time, but Sets give us O(1) lookups!
    cols = set()
    
    # In a matrix, every square on a Positive Diagonal (/) has the exact same 
    # value for `row + col`.
    # e.g., (0,2), (1,1), (2,0) -> 0+2=2, 1+1=2, 2+0=2.
    pos_diagonals = set() 
    
    # Every square on a Negative Diagonal (\) has the exact same value for `row - col`.
    # e.g., (0,0), (1,1), (2,2) -> 0-0=0, 1-1=0, 2-2=0.
    neg_diagonals = set() 
    
    # We only need to store the COLUMN index of the Queen for each row.
    # board[row] = col
    board_state = []
    
    all_solutions = []
    
    def backtrack(row: int):
        # 1. BASE CASE (SUCCESS)
        # We successfully placed a queen on every row from 0 to N-1!
        if row == n:
            all_solutions.append(list(board_state))
            return
            
        # 2. THE CHOICES
        # We are on `row`. Try placing a queen in every `col` (0 to N-1).
        for col in range(n):
            
            # --- PRUNING (THE MAGIC) ---
            # Is this square under attack?
            if col in cols or (row + col) in pos_diagonals or (row - col) in neg_diagonals:
                # INVALID! Skip it entirely. Do not recurse.
                continue
                
            # --- CHOOSE ---
            # We found a safe square! Place the queen.
            cols.add(col)
            pos_diagonals.add(row + col)
            neg_diagonals.add(row - col)
            board_state.append(col)
            
            # --- EXPLORE ---
            # Move down to the next row and repeat!
            backtrack(row + 1)
            
            # --- UNCHOOSE ---
            # We returned. This path either succeeded or hit a dead end.
            # Lift the queen off the board so we can try the next `col`.
            cols.remove(col)
            pos_diagonals.remove(row + col)
            neg_diagonals.remove(row - col)
            board_state.pop()

    # Start placing queens at row 0
    backtrack(0)
    return all_solutions


# ==============================================================================
# 4. VISUALIZATION ENGINE
# ==============================================================================
def format_board(solution: List[int], n: int) -> List[str]:
    """Converts the internal list `[1, 3, 0, 2]` into an ASCII Chessboard."""
    board = []
    for col in solution:
        # Create a row of dots '.'
        row_str = ["."] * n
        # Place the Queen 'Q'
        row_str[col] = "Q"
        board.append(" ".join(row_str))
    return board

def demonstrate_n_queens():
    section_header("Algorithm: N-Queens")
    
    n = 4
    print(f"Solving the N-Queens problem for a {n}x{n} board...\n")
    
    solutions = solve_n_queens(n)
    
    print(f"Found {len(solutions)} valid solutions!\n")
    
    for idx, sol in enumerate(solutions):
        print(f"Solution {idx + 1}:")
        ascii_board = format_board(sol, n)
        for row in ascii_board:
            print(f"  {row}")
        print()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we only need a 1D Array `board_state` instead of a full 2D NxN Matrix?
   Answer: Because the rules of the game dictate that no two Queens can share the same Row. Therefore, our recursion automatically forces exactly 1 Queen per row. We don't need a matrix; we just need an array where `board[i] = col` means "The Queen on row `i` is located at column `col`". This saves massive amounts of RAM.

2. What is Pruning?
   Answer: Pruning is the act of checking if a State is mathematically valid *BEFORE* diving into the recursive `explore()` step. If the state is invalid, the `continue` statement aborts that entire branch of the Decision Tree, saving the CPU from doing millions of useless recursive calls.

3. Why do we use `(row + col)` and `(row - col)` to track diagonals?
   Answer: It is a mathematical property of 2D Grids. Imagine a matrix. If you step Diagonally Down-Right (e.g., from (1,1) to (2,2)), you added 1 to both `row` and `col`. Therefore, their difference `(row - col)` remains exactly the same! `2-2 == 0`, `1-1 == 0`. We can use this constant difference as a unique Hash Key in our Set to instantly check if any other Queen is sitting on that exact diagonal line.
"""

if __name__ == "__main__":
    demonstrate_n_queens()
    print("\n[SUCCESS] Laboratory: N-Queens Completed.")
