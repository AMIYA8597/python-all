"""
## A. Concept Name
Simulation Problems (Ad-Hoc)

## B. One-Sentence Definition
Simulation problems require building a step-by-step model of a process over time, tracking explicit state transitions based on specific rules without relying on advanced algorithms.

## C. Why Does This Exist?
Many real-world systems (like physics engines, queueing systems, or cellular automata) require exact replication of logical steps over time to predict an outcome, rather than optimizing for a single metric.

## D. Intuition
Imagine Conway's Game of Life. You can't usually skip to step 1,000 instantly. You have to write a loop that calculates step 1, then step 2, etc., up to step 1,000, managing the "current" and "next" states carefully.

## E. Real-Life Analogy
Think of a turn-based board game. Every turn, players make moves that change the state of the board. To find out what the board looks like at turn 50, you literally have to play through or "simulate" all 50 turns following the game's exact rules.

## F. Mental Model
Treat the simulation as a state machine inside a loop. The core pattern is: `Read Current State -> Apply Rules -> Write Next State -> Update Current State`. Always keep reads and writes strictly separated to avoid corrupting the simulation mid-step.

## G. Visual Explanation
```
Time T:      [State 0]
Rule Engine:   |  (Apply Direction Vectors / Conditionals)
Time T+1:    [State 1]
```

## H. Formal Explanation
In ad-hoc simulation problems, you iterate over discrete time steps or specific events. Data structures usually involve 2D grids (matrices), lists, or queues. Key techniques include using direction vectors for spatial movement and utilizing modular arithmetic for cyclic boundaries.

## I. Mathematical Foundation (if applicable)
Often relies on 2D coordinate geometry and modular arithmetic for wraparound conditions, rather than advanced mathematical theories.

## J. From-Scratch Implementation (if applicable)
N/A - the exact implementation is completely defined by the problem statement (e.g., Game of Life, Spiral Matrix).

## K. Library / Production Implementation (if applicable)
Used in specialized libraries for event-driven simulation (like `simpy` in Python) or 2D game frameworks (like `pygame`).

## L. Trace (walk through example)
Game of Life (one step):
1. Grid cell (0,0) is Alive.
2. Check 8 neighbors using direction vectors: `[(-1,-1), (-1,0), ...]`.
3. Count = 1 live neighbor.
4. Rule applied: < 2 live neighbors -> Cell dies.
5. Save "Dead" to the *next* state matrix.
6. Swap matrices after all cells are evaluated.

## M. Complexity
- Time Complexity: Typically O(S * N) where S is the number of steps and N is the size of the state (e.g., matrix cells).
- Space Complexity: O(N) to store the next state, though in-place bitwise tricks can reduce it to O(1).

## N. Common Mistakes
1. Mutating the state while reading it. In Game of Life, if you change a cell to 0, its neighbor might incorrectly read it as 0 instead of 1.
2. Missing boundary checks. `IndexError` is extremely common. Always verify `0 <= r < ROWS`.
3. Hardcoding nested `if` statements for directions instead of using a direction array.

## O. Common Confusions
"Can't I optimize this with dynamic programming?" Not always. If the problem asks for the exact state at step K, and state transitions depend on the entire board, you often must simulate all K steps. 

## P. When To Use
- When the problem explicitly says "simulate this process".
- When asked to traverse a matrix in a specific pattern (e.g., Spiral Matrix).

## Q. When NOT To Use
- When the problem asks for the shortest path or optimal choice (use BFS/DFS/DP instead).
- When K (number of steps) is astronomically large (e.g., 10^9) - this usually implies a cycle or math trick exists.

## R. Trade-offs
In-place state modification (using bits) saves O(N) space but makes the code harder to read and debug. For interviews, allocating a new matrix for the next state is often safer unless space is constrained.

## S. Debugging
- Print the state after *every* step for a small test case.
- Check if your direction vectors are correct.
- Ensure your boundary checks are inclusive/exclusive in the right ways.

## T. Memory Hook (a short memorable principle)
"Read from old, write to new. Never mix the two."

## U. Active Recall (questions before answers)
1. Why do we need an array of direction vectors in grid simulations?
2. How do you prevent state corruption when updating a grid?
3. What does an `IndexError` usually indicate in a simulation?

## V. Practice (exercises)
1. Simulate the movement of a robot on a grid given a string of commands ("U", "D", "L", "R").
2. Implement a 1D cellular automaton.

## W. Interview Question
"Design a function to simulate Conway's Game of Life in-place without allocating a new 2D matrix."

## X. Project Connection
This concept connects to any larger project requiring step-by-step state simulation, such as writing a game engine, physics simulator, or algorithmic trading backtester.
"""

from typing import List

def game_of_life(board: List[List[int]]) -> None:
    """
    Simulates one step of Conway's Game of Life IN-PLACE.
    
    Rules:
    1. Any live cell with fewer than two live neighbors dies (under-population).
    2. Any live cell with two or three live neighbors lives.
    3. Any live cell with more than three live neighbors dies (over-population).
    4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).
    
    Time Complexity: O(M * N) where M and N are grid dimensions.
    Space Complexity: O(1) utilizing bitwise encoding for state.
    """
    if not board or not board[0]:
        return

    rows = len(board)
    cols = len(board[0])
    
    # Direction vectors for 8 neighbors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # We will use bit 0 for the original state, and bit 1 for the next state.
    # original dead, next dead -> 00 (0)
    # original live, next dead -> 01 (1)
    # original dead, next live -> 10 (2)
    # original live, next live -> 11 (3)
    
    for r in range(rows):
        for c in range(cols):
            live_neighbors = 0
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    # check if originally alive (bit 0 is 1)
                    if board[nr][nc] & 1:
                        live_neighbors += 1
                        
            # Apply rules
            if board[r][c] == 1:
                if live_neighbors in (2, 3):
                    # Next state is live, set bit 1 (add 2)
                    board[r][c] = 3 
            else:
                if live_neighbors == 3:
                    # Next state is live, set bit 1 (add 2)
                    board[r][c] = 2

    # Shift all states to the right to get the next state
    for r in range(rows):
        for c in range(cols):
            board[r][c] >>= 1


def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Simulate walking a matrix in a spiral order.
    
    Time Complexity: O(M * N)
    Space Complexity: O(1) excluding output array.
    """
    if not matrix:
        return []
        
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse from left to right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Traverse from top to bottom
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        if top <= bottom:
            # Traverse from right to left
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
            
        if left <= right:
            # Traverse from bottom to top
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
            
    return result

if __name__ == "__main__":
    # Test Game of Life
    board = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
    expected_next = [
        [0, 0, 0],
        [1, 0, 1],
        [0, 1, 1],
        [0, 1, 0]
    ]
    game_of_life(board)
    assert board == expected_next, f"Expected {expected_next}, got {board}"

    # Test Spiral Order
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    assert spiral_order(matrix) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    
    print("All simulation problems tests passed successfully!")
