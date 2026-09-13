"""
# ==============================================================================
# LABORATORY: KNIGHT'S TOUR & WARNSDORFF'S HEURISTIC
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The "Knight's Tour" is an ancient mathematical problem: Can a Knight start on 
# an empty chessboard and make valid L-shaped moves to visit EVERY single square 
# exactly once?
#
# If you use naive Backtracking, the Knight has up to 8 possible moves at every 
# step. For an 8x8 board (64 squares), the depth of the recursion tree is 64.
# The Time Complexity is roughly O(8^64). 
# Your computer will crash before it even finishes a fraction of a percent.
#
# How do we solve it? We use a **Heuristic**. 
# A Heuristic is a "Rule of Thumb" that makes the Backtracking algorithm artificially 
# smarter. Instead of trying the 8 moves randomly, we sort the moves based on 
# how "good" they are.
#
# **Warnsdorff's Rule (1823):** "Always choose the next square that has the FEWEST 
# valid onward moves."
# Why? Because if a square has only 1 valid exit left, and you don't go there 
# immediately, you will get trapped later. By targeting the most restricted 
# squares first, the algorithm magically avoids dead ends and solves the board 
# in near-linear time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 8 Directional Vectors for 2D Grid movement.
# - Understand how a Heuristic guides the `for` loop in Backtracking.
# - Implement Warnsdorff's Rule to shatter the O(8^64) time barrier.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIRECTIONAL VECTORS (THE L-SHAPE)
# ==============================================================================
# The 8 mathematical offsets to generate a Knight's L-shaped moves on a grid.
# e.g. Up 2, Right 1 -> (-2, 1)
MOVES = [
    (-2, 1), (-1, 2), (1, 2), (2, 1),
    (2, -1), (1, -2), (-1, -2), (-2, -1)
]

def is_safe(board: List[List[int]], row: int, col: int, n: int) -> bool:
    """Checks if the square is on the board and hasn't been visited yet."""
    return 0 <= row < n and 0 <= col < n and board[row][col] == -1


# ==============================================================================
# 4. WARNSDORFF'S HEURISTIC ENGINE
# ==============================================================================
def count_onward_moves(board: List[List[int]], row: int, col: int, n: int) -> int:
    """
    Counts how many valid exits exist from a specific square.
    Used exclusively to rank the choices for Warnsdorff's Heuristic.
    """
    count = 0
    for r_offset, c_offset in MOVES:
        next_r, next_c = row + r_offset, col + c_offset
        if is_safe(board, next_r, next_c, n):
            count += 1
    return count

def get_warnsdorff_sorted_moves(board: List[List[int]], row: int, col: int, n: int) -> List[Tuple[int, int]]:
    """
    Returns the valid next moves, SORTED by Warnsdorff's Rule (Fewest exits first).
    """
    valid_moves = []
    
    for r_offset, c_offset in MOVES:
        next_r, next_c = row + r_offset, col + c_offset
        if is_safe(board, next_r, next_c, n):
            # Calculate the degree (number of onward exits)
            degree = count_onward_moves(board, next_r, next_c, n)
            valid_moves.append((degree, next_r, next_c))
            
    # Sort by the degree (the first element in the tuple)
    valid_moves.sort()
    
    # Strip the degree out and just return the coordinates
    return [(r, c) for _, r, c in valid_moves]


# ==============================================================================
# 5. THE BACKTRACKING ALGORITHM
# ==============================================================================
def solve_knight_tour(n: int) -> None:
    # Initialize board with -1 (Unvisited)
    board = [[-1 for _ in range(n)] for _ in range(n)]
    
    # Start the Knight at (0, 0)
    start_row, start_col = 0, 0
    board[start_row][start_col] = 0 # Step 0
    
    # Target number of steps to fill the board (N^2)
    target_steps = n * n
    
    def backtrack(row: int, col: int, step_num: int) -> bool:
        # 1. BASE CASE (SUCCESS)
        if step_num == target_steps:
            return True
            
        # 2. THE CHOICES (GUIDED BY HEURISTIC)
        # Instead of a hardcoded loop `for offset in MOVES:`, we dynamically 
        # generate and SORT the choices using Warnsdorff's Rule!
        best_moves = get_warnsdorff_sorted_moves(board, row, col, n)
        
        for next_r, next_c in best_moves:
            # --- CHOOSE ---
            board[next_r][next_c] = step_num
            
            # --- EXPLORE ---
            if backtrack(next_r, next_c, step_num + 1) is True:
                return True
                
            # --- UNCHOOSE ---
            board[next_r][next_c] = -1
            
        # 3. DEAD END
        return False

    # Execute
    if backtrack(start_row, start_col, 1):
        print(f" SUCCESS! Knight's Tour solved for {n}x{n} board.")
        for row in board:
            # Format the numbers to have 2 digits spacing for clean grids
            print(" ".join(f"{str(cell).zfill(2)}" for cell in row))
    else:
        print(" FAILED to find a solution.")


def demonstrate_knights_tour():
    section_header("Algorithm: Knight's Tour (Warnsdorff's Heuristic)")
    
    # We will use a 6x6 board to keep console output clean. 
    # An 8x8 board solves in milliseconds too, thanks to the Heuristic!
    n = 6
    print(f"Attempting to solve the Knight's Tour for a {n}x{n} board...")
    solve_knight_tour(n)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Warnsdorff's Heuristic work?
   Answer: It acts as an aggressive "Look-Ahead" pruning mechanism. If a square in the corner of the board only has 1 valid exit remaining, and we choose to jump somewhere else instead, that corner square becomes a permanent mathematical trap that we can never escape from later. By forcing the Knight to immediately clear out the most restricted squares first, it naturally spirals inwards/outwards, leaving the wide-open center squares for the very end.

2. Does Warnsdorff's Heuristic change the Big-O Time Complexity?
   Answer: Mathematically, NO. It is still a Backtracking algorithm that could theoretically hit $O(8^{N^2})$ in the absolute worst-case if the heuristic ties repeatedly. But practically, it reduces the effective branching factor to nearly 1, allowing it to solve massive boards in linear $O(N^2)$ time.

3. How do we model movement on a 2D Array?
   Answer: Using Directional Vectors! Instead of writing 8 massive nested `if` statements, you create an array of `(row_offset, col_offset)` tuples. You loop over them `for r, c in MOVES:` and mathematically add them to your current coordinate: `next_row = curr_row + r`.
"""

if __name__ == "__main__":
    demonstrate_knights_tour()
    print("\n[SUCCESS] Laboratory: Knight's Tour Completed.")
