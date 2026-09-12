"""
Module: Tower of Hanoi using Recursion

Learning Objectives:
1. Understand the classic divide and conquer recursive problem.
2. Visualize state space and recursive call tree.
3. Understand the mathematical minimum number of moves: 2^n - 1.
4. Implement a step-by-step solution tracer.

Concept Explanation:
Tower of Hanoi consists of 3 pegs and n disks of different sizes.
Goal: Move all disks from the source peg to the destination peg.
Rules:
1. Move only one disk at a time.
2. A larger disk cannot be placed on top of a smaller disk.
3. Disks can only be moved from the top of a stack.

Imports:
"""
from typing import List, Tuple

def hanoi_basic(n: int, source: str, destination: str, auxiliary: str) -> None:
    """Basic implementation: Prints the steps to solve the puzzle."""
    if n < 0:
        raise ValueError("Number of disks cannot be negative")
    if n == 0:
        return
    if n == 1:
        print(f"Move disk 1 from {source} to {destination}")
        return
        
    hanoi_basic(n - 1, source, auxiliary, destination)
    print(f"Move disk {n} from {source} to {destination}")
    hanoi_basic(n - 1, auxiliary, destination, source)

def hanoi_moves(n: int, source: str, destination: str, auxiliary: str) -> List[Tuple[int, str, str]]:
    """Intermediate implementation: Return the list of moves."""
    moves = []
    
    def solve(disk, src, dst, aux):
        if disk == 0:
            return
        solve(disk - 1, src, aux, dst)
        moves.append((disk, src, dst))
        solve(disk - 1, aux, dst, src)
        
    solve(n, source, destination, auxiliary)
    return moves

class HanoiState:
    """Advanced implementation: Object-oriented approach tracking state."""
    def __init__(self, n: int):
        self.pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
        self.moves = 0
        
    def move(self, src: str, dst: str):
        if not self.pegs[src]:
            raise ValueError(f"Peg {src} is empty")
        if self.pegs[dst] and self.pegs[src][-1] > self.pegs[dst][-1]:
            raise ValueError("Invalid move: larger disk on smaller disk")
            
        disk = self.pegs[src].pop()
        self.pegs[dst].append(disk)
        self.moves += 1
        
    def solve(self, n: int, src: str, dst: str, aux: str):
        if n > 0:
            self.solve(n - 1, src, aux, dst)
            self.move(src, dst)
            self.solve(n - 1, aux, dst, src)

def performance_analysis():
    """Analyze the number of moves required."""
    print("Performance Analysis (Number of moves):")
    for i in range(1, 6):
        moves = len(hanoi_moves(i, 'A', 'C', 'B'))
        print(f"n = {i} | Moves = {moves} | Expected = {2**i - 1}")

def edge_cases():
    """Handle edge cases like 0 disks."""
    print("\nEdge Cases:")
    print("Solving for 0 disks:")
    hanoi_basic(0, 'A', 'C', 'B')
    print("(No output means correct handling)")

def interview_challenge():
    """
    Challenge: Find the state of the pegs after k moves.
    """
    print("\nInterview Challenge: Calculate total moves for 10 disks:")
    print(f"Total moves = {2**10 - 1}")

def run_tests():
    """Unit tests."""
    moves = hanoi_moves(3, 'A', 'C', 'B')
    assert len(moves) == 7
    assert moves[0] == (1, 'A', 'C')
    assert moves[-1] == (1, 'A', 'C')
    
    state = HanoiState(3)
    state.solve(3, 'A', 'C', 'B')
    assert len(state.pegs['C']) == 3
    assert state.moves == 7
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Tower of Hanoi ---\n")
    print("Solving for 3 disks:")
    hanoi_basic(3, 'A', 'C', 'B')
    print("")
    performance_analysis()
    edge_cases()
    interview_challenge()
    run_tests()
