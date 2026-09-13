"""
# ==============================================================================
# LABORATORY: MINIMUM PATH SUM (2D GRID DP & IN-PLACE OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a 2D grid filled with non-negative numbers representing "costs".
# You start at the top-left corner `(0, 0)` and want to reach the bottom-right 
# corner `(M-1, N-1)`. You can ONLY move Down or Right.
# What is the path that yields the absolute Minimum Sum?
#
# If you use DFS/Backtracking, you will explore every possible path. In an 
# 18x18 grid, there are 2.3 Billion paths. It will take minutes to run.
#
# But notice the Overlapping Subproblems: If you reach cell `(5, 5)`, it doesn't 
# matter HOW you got there. The optimal path FROM `(5, 5)` to the end is exactly 
# the same regardless of your past.
# 
# Using 2D Dynamic Programming, we can calculate the absolute optimal path in 
# exactly 1 pass over the grid, taking O(M * N) time.
# And incredibly, we can do it in O(1) Extra Space by mutating the input grid!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand 2D Grid DP State Transitions.
# - Master Grid Boundary Conditions (The Top Row & Left Column).
# - Implement O(1) Space In-Place mutation.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. 2D TABULATION (IN-PLACE)
# ==============================================================================
def min_path_sum(grid: List[List[int]]) -> int:
    """
    Time Complexity: O(M * N) (Exactly one pass through the grid).
    Space Complexity: O(1) (We overwrite the input grid to save RAM!).
    """
    if not grid or not grid[0]:
        return 0
        
    rows = len(grid)
    cols = len(grid[0])
    
    # 1. STATE DEFINITION
    # Normally we would create `dp = [[0]*cols for _ in range(rows)]`.
    # But because we only ever look at the cell ABOVE us or the cell LEFT of us, 
    # we can just OVERWRITE the `grid` cells with their DP values!
    # After a cell is processed, its original value is never needed again.
    
    # 2. INITIALIZATION (BOUNDARY CONDITIONS)
    
    # A. The Top Row (Row 0)
    # If you are in the top row, you CANNOT come from above. 
    # You MUST have come from the Left.
    for c in range(1, cols):
        grid[0][c] += grid[0][c - 1]
        
    # B. The Left Column (Col 0)
    # If you are in the left column, you CANNOT come from the left.
    # You MUST have come from Above.
    for r in range(1, rows):
        grid[r][0] += grid[r - 1][0]
        
    # 3. THE TABULATION LOOP (THE INTERIOR)
    # Now we loop through the rest of the grid (Starting at Row 1, Col 1).
    for r in range(1, rows):
        for c in range(1, cols):
            
            # --- STATE TRANSITION EQUATION ---
            # To reach `(r, c)`, we either stepped DOWN from `(r-1, c)` 
            # or stepped RIGHT from `(r, c-1)`.
            # Which one was cheaper? Take the minimum, and add the current cell's cost!
            
            cost_from_above = grid[r - 1][c]
            cost_from_left = grid[r][c - 1]
            
            grid[r][c] += min(cost_from_above, cost_from_left)
            
    # The final answer is the accumulated cost at the bottom-right corner.
    return grid[rows - 1][cols - 1]


def print_grid(grid: List[List[int]], title: str):
    print(f"\n{title}:")
    for row in grid:
        # Format strings to align columns beautifully
        print(" ".join(f"{num:3d}" for num in row))


def demonstrate_min_path_sum():
    section_header("Algorithm: Minimum Path Sum")
    
    # Let's use a copy because the algorithm destroys the input grid!
    import copy
    
    grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]
    
    grid_copy = copy.deepcopy(grid)
    
    print_grid(grid, "Original Cost Grid")
    
    ans = min_path_sum(grid_copy)
    
    print_grid(grid_copy, "Mutated DP Grid (Final State)")
    
    print(f"\nMinimum Path Sum: {ans} (Expected: 7)")
    print("Path: 1 -> 3 -> 1 -> 1 -> 1")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is In-Place mutation considered $O(1)$ Space, and is it safe for Production?
   Answer: It is $O(1)$ "Auxiliary Space" because we allocate zero extra arrays; we just reuse the memory the caller gave us. However, in a real Production environment (like a web server backend), mutating input parameters is highly dangerous (Side Effects). If another thread tries to read that grid, it will read garbage DP data instead of the original costs! In Production, you should allocate a new $O(N)$ 1D array to act as the "previous row" buffer, achieving $O(N)$ space safely without destroying the input.

2. Why did we isolate the Top Row and Left Column in separate `for` loops?
   Answer: To avoid `if` statements inside the main nested loop! If we just started at `0,0`, we would have to check `if r > 0` and `if c > 0` billions of times. By pre-calculating the boundary conditions first, the interior loop can run with zero branching logic, allowing the CPU to execute it at maximum speed.

3. Can this algorithm handle negative numbers in the grid?
   Answer: YES! Unlike Dijkstra's Graph Algorithm (which catastrophically fails on negative weights because it uses a Greedy Priority Queue), DP on a grid evaluates ALL valid paths mathematically. It will correctly incorporate negative numbers into the minimum sum.
"""

if __name__ == "__main__":
    demonstrate_min_path_sum()
    print("\n[SUCCESS] Laboratory: Min Path Sum Completed.")
