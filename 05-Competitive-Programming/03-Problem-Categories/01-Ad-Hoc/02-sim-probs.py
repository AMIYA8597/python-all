"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (COMPLEX SIMULATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive portion of interviews (especially at companies like Amazon and 
# Bloomberg) involve simulating a physical system. 
#
# E.g., "Design a parking lot", "Simulate a game of Tic-Tac-Toe", or 
# "Implement Conway's Game of Life on a 2D grid".
#
# These are not Math puzzles. You actually DO have to write the $O(N^2)$ loops 
# to simulate the game rules exactly as stated. The challenge is keeping your 
# code completely decoupled, modular, and bug-free when dealing with massive 
# 2D arrays (Matrices) and out-of-bounds boundary conditions.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Safely traverse a 2D matrix (The 8-Directional Array Trick).
# - Simulate Conway's Game of Life (In-Place Matrix Modification).
# - Rotate a 2D Matrix (Transposition).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE 8-DIRECTIONAL ARRAY TRICK
# ==============================================================================
def demonstrate_directions():
    section_header("The 8-Directional Matrix Trick")
    
    print("If you need to check all 8 neighbors of a cell in a 2D Grid, ")
    print("DO NOT write 8 separate `if` statements! That is extremely buggy.")
    print("Use a Directional Array.\n")
    
    # Delta (row, col) for all 8 directions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-Left, Top, Top-Right
        ( 0, -1),          ( 0, 1),  # Left, Right
        ( 1, -1), ( 1, 0), ( 1, 1)   # Bottom-Left, Bottom, Bottom-Right
    ]
    
    print("Directions Array:")
    for dr, dc in directions:
        print(f"Row offset: {dr:2}, Col offset: {dc:2}")
        
    print("\nIn your code, you just use a single loop:")
    print("for dr, dc in directions:")
    print("    nr, nc = r + dr, c + dc")
    print("    if 0 <= nr < ROWS and 0 <= nc < COLS:")
    print("        # Safely process neighbor without IndexError!")


# ==============================================================================
# 4. CONWAY'S GAME OF LIFE (IN-PLACE SIMULATION)
# ==============================================================================
def game_of_life(board: list[list[int]]) -> None:
    """
    Simulates one step of Conway's Game of Life IN-PLACE.
    1 = Live cell, 0 = Dead cell.
    Rules:
    - Live cell with < 2 live neighbors dies.
    - Live cell with 2 or 3 live neighbors lives.
    - Live cell with > 3 live neighbors dies.
    - Dead cell with exactly 3 live neighbors becomes a live cell.
    
    TRAP: If you modify the board directly, you corrupt the state for the next cells!
    SOLUTION: Use bit-manipulation or dummy states!
    0 = Dead (stays dead)
    1 = Live (stays live)
    2 = Dead (becomes Live)
    3 = Live (becomes Dead)
    """
    ROWS = len(board)
    COLS = len(board[0])
    
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    for r in range(ROWS):
        for c in range(COLS):
            live_neighbors = 0
            
            # Check 8 neighbors safely
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    # If neighbor is 1 (Live) or 3 (Live becoming Dead), it counts as currently alive!
                    if board[nr][nc] == 1 or board[nr][nc] == 3:
                        live_neighbors += 1
                        
            # Apply Game Rules using Dummy States
            if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                # Rule 1 & 3: Dies
                board[r][c] = 3
            elif board[r][c] == 0 and live_neighbors == 3:
                # Rule 4: Reproduction
                board[r][c] = 2
                
    # Final Pass: Convert Dummy States to actual 0s and 1s
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 2:
                board[r][c] = 1
            elif board[r][c] == 3:
                board[r][c] = 0

def demonstrate_game_of_life():
    section_header("Game of Life (In-Place Dummy States)")
    
    board = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
    
    print("Initial Board:")
    for row in board: print(row)
    
    # Simulates exactly 1 step
    game_of_life(board)
    
    print("\nBoard after 1 Step:")
    for row in board: print(row)


# ==============================================================================
# 5. MATRIX ROTATION (TRANSPOSE + REVERSE)
# ==============================================================================
def rotate_matrix(matrix: list[list[int]]) -> None:
    """
    Rotates a square 2D matrix 90 degrees clockwise IN-PLACE.
    Time Complexity: O(N^2), Space Complexity: O(1)
    
    The Mathematical Trick:
    1. Transpose the matrix (swap row and col).
    2. Reverse every row.
    """
    N = len(matrix)
    
    # 1. Transpose
    for i in range(N):
        for j in range(i, N):
            # Swap [i][j] with [j][i]
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # 2. Reverse every row
    for i in range(N):
        matrix[i].reverse()

def demonstrate_rotation():
    section_header("In-Place 2D Matrix Rotation")
    
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("Original Matrix:")
    for row in matrix: print(row)
    
    rotate_matrix(matrix)
    
    print("\nRotated 90 Degrees Clockwise:")
    for row in matrix: print(row)


def run_all_labs():
    demonstrate_directions()
    demonstrate_game_of_life()
    demonstrate_rotation()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When navigating a 2D Matrix, why is it considered a catastrophic anti-pattern to write 4 or 8 separate `if` statements to check the neighboring cells?
   Answer: Writing `if row > 0: check(up)` and `if row < ROWS-1: check(down)` creates massive code bloat, violates the DRY (Don't Repeat Yourself) principle, and drastically increases the surface area for copy-paste typos (e.g., typing `row` instead of `col`). The industry standard is to define a static list of tuple offsets (`directions = [(0,1), (1,0), (0,-1), (-1,0)]`) and use a single `for dr, dc in directions:` loop. This abstracts the boundary-checking logic into exactly two lines of code (`0 <= r + dr < ROWS`), mathematically guaranteeing flawless boundary safety.

2. In Conway's Game of Life (or any cellular automata), why does updating the board "in-place" directly corrupt the algorithm, and how do we solve it using $O(1)$ space?
   Answer: Cellular automata rules require all cells to update *simultaneously* based on the exact state of the board at Time $T$. If you physically flip Cell A from 1 to 0 during the loop, when the loop reaches Cell B, Cell B will read Cell A's *new* state (Time $T+1$) instead of its old state (Time $T$), corrupting the neighbor count calculation. To solve this without allocating an entire duplicate $O(N^2)$ board in memory, we invent "Dummy States". We set the cell to `3` (meaning "Was Alive, Now Dead"). When calculating neighbors for other cells, if they see a `3`, they mathematically count it as a `1` (Alive). After the entire board is processed, a second pass trivially converts all `3`s to `0`s in $O(1)$ extra space.

3. How do you rotate a 2D Square Matrix 90 degrees clockwise completely in-place?
   Answer: You use a mathematical shortcut combining two simple linear algebra operations. First, you Transpose the matrix by swapping elements across the main diagonal (`matrix[i][j] swapped with matrix[j][i]`). Second, you iterate through every row and Reverse it (`matrix[i].reverse()`). Because transposition and array reversal both use $O(1)$ in-place swapping mechanics, the entire 2D matrix is perfectly rotated without requiring a secondary $O(N^2)$ matrix buffer.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Complex Simulation Completed.")
