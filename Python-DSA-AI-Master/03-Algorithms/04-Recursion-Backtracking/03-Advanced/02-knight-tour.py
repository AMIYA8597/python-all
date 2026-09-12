"""
Knight's Tour Problem - Advanced Backtracking & Heuristics

================================================================================
1. INTUITION & REAL-WORLD ANALOGY
================================================================================
Imagine a delivery drone that can only jump specific distances (like a chess knight) 
and needs to visit every neighborhood (cell) on a grid-like map exactly once before
running out of battery. How do you find a path? 

In graph theory, finding a path that visits every vertex exactly once is called 
finding a "Hamiltonian Path." The Knight's Tour is a classic example of this on a 
graph where nodes are chessboard squares and edges represent valid knight moves.

================================================================================
2. FORMAL EXPLANATION
================================================================================
The Knight's Tour problem asks if a knight can visit every square on an N x N 
chessboard exactly once.
- The board has N * N squares.
- A knight can make up to 8 moves from any square (L-shapes: ±1 on one axis, 
  ±2 on the other).
- We place the knight at an initial position (usually (0, 0)) and try to find a 
  sequence of N^2 - 1 valid moves.

Approaches:
1. Naive Backtracking: 
   Try every possible move. If a path leads to a dead end before visiting all squares,
   backtrack and try the next move.
2. Warnsdorff's Rule (Heuristic):
   Always move to the adjacent, unvisited square with the **fewest** onward moves. 
   This greedy strategy drastically reduces the search space by avoiding dead ends 
   early. It effectively finds a path for much larger N in near linear time.

================================================================================
3. COMPLEXITY ANALYSIS
================================================================================
Naive Backtracking:
- Time Complexity: O(8^(N^2)) worst case. From each square, there are at most 8 moves.
  For N >= 8, this is practically unsolvable in reasonable time.
- Space Complexity: O(N^2) for the N x N board state and maximum recursion stack.

Warnsdorff's Rule (Greedy + Backtracking):
- Time Complexity: O(N^2) typical/average case. The heuristic guides the knight to a 
  solution almost directly, minimizing backtracking.
- Space Complexity: O(N^2) for board state and recursion stack.

================================================================================
4. COMMON MISTAKES & DEBUGGING
================================================================================
- Mistake: Not marking the starting square as visited (step 0).
  Fix: Always initialize board[startX][startY] = 0 before entering recursion.
- Mistake: Incorrect bounds checking.
  Fix: Ensure 0 <= x < N and 0 <= y < N.
- Mistake: Using Warnsdorff's blindly without fallback.
  Fix: Warnsdorff's rule is a heuristic; sometimes multiple neighbors have the 
  same degree. Breaking ties randomly or systematically is important, and 
  backtracking might still be needed if a dead end is reached.

================================================================================
5. ACTIVE RECALL & MEMORY ANCHORS
================================================================================
- Q: Why is Warnsdorff's Rule so effective?
- A: It leaves squares with fewer exits for later, ensuring we don't get "trapped" 
     early by consuming the only exits for isolated squares.
- Anchor: "Eat the crust first" — visit the most restricted edges/corners of the board
          early, leaving the flexible center for last.

================================================================================
"""

from typing import List, Tuple, Optional
import time

class KnightTour:
    def __init__(self, n: int):
        self.n = n
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    def is_safe(self, x: int, y: int, board: List[List[int]]) -> bool:
        """Check if x, y are valid and unvisited."""
        return 0 <= x < self.n and 0 <= y < self.n and board[x][y] == -1

    def solve_naive(self, start_x: int = 0, start_y: int = 0) -> Optional[List[List[int]]]:
        """
        Solves the Knight's Tour using purely naive backtracking.
        Warning: Very slow for N >= 6.
        """
        board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        board[start_x][start_y] = 0
        
        if self._solve_kt_util(start_x, start_y, 1, board):
            return board
        return None

    def _solve_kt_util(self, x: int, y: int, move_i: int, board: List[List[int]]) -> bool:
        """Recursive backtracking utility."""
        if move_i == self.n ** 2:
            return True

        for move in self.moves:
            next_x, next_y = x + move[0], y + move[1]
            if self.is_safe(next_x, next_y, board):
                board[next_x][next_y] = move_i
                if self._solve_kt_util(next_x, next_y, move_i + 1, board):
                    return True
                # Backtrack
                board[next_x][next_y] = -1
                
        return False

    # =========================================================================
    # PROFESSIONAL IMPLEMENTATION: Warnsdorff's Rule
    # =========================================================================
    
    def get_degree(self, x: int, y: int, board: List[List[int]]) -> int:
        """Counts how many unvisited neighbors an (x, y) square has."""
        count = 0
        for move in self.moves:
            nx, ny = x + move[0], y + move[1]
            if self.is_safe(nx, ny, board):
                count += 1
        return count

    def solve_warnsdorff(self, start_x: int = 0, start_y: int = 0) -> Optional[List[List[int]]]:
        """
        Solves using Warnsdorff's heuristic for O(N^2) typical performance.
        Can easily solve N=8 or even much larger boards.
        """
        board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        board[start_x][start_y] = 0
        
        if self._solve_warnsdorff_util(start_x, start_y, 1, board):
            return board
        return None

    def _solve_warnsdorff_util(self, x: int, y: int, move_i: int, board: List[List[int]]) -> bool:
        """Recursive backtracking with Warnsdorff's heuristic."""
        if move_i == self.n ** 2:
            return True
            
        # Get all valid next moves
        valid_moves = []
        for move in self.moves:
            nx, ny = x + move[0], y + move[1]
            if self.is_safe(nx, ny, board):
                degree = self.get_degree(nx, ny, board)
                valid_moves.append((degree, nx, ny))
                
        # Sort moves by degree (fewest onward moves first) - THIS is Warnsdorff's Rule
        valid_moves.sort(key=lambda item: item[0])
        
        # Try sorted moves
        for _, nx, ny in valid_moves:
            board[nx][ny] = move_i
            if self._solve_warnsdorff_util(nx, ny, move_i + 1, board):
                return True
            # Backtrack
            board[nx][ny] = -1
            
        return False


def print_board(board: List[List[int]]):
    """Utility to print the board beautifully."""
    if not board:
        print("No solution found.")
        return
    n = len(board)
    for row in board:
        print(" ".join(f"{str(cell).rjust(2, '0')}" for cell in row))
    print()


def run_tests():
    print("=== Testing Naive Backtracking ===")
    n_small = 5
    kt_small = KnightTour(n_small)
    
    start_time = time.time()
    res_naive = kt_small.solve_naive()
    print(f"Naive solution for {n_small}x{n_small} found in {time.time() - start_time:.4f}s")
    if res_naive:
        print_board(res_naive)
    
    print("\n=== Testing Warnsdorff's Heuristic ===")
    # N=8 is standard chessboard. Naive would hang forever, but Warnsdorff solves it instantly.
    n_large = 8
    kt_large = KnightTour(n_large)
    
    start_time = time.time()
    res_warnsdorff = kt_large.solve_warnsdorff()
    print(f"Warnsdorff solution for {n_large}x{n_large} found in {time.time() - start_time:.4f}s")
    if res_warnsdorff:
        print_board(res_warnsdorff)
    
    assert res_naive is not None
    assert res_warnsdorff is not None
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
