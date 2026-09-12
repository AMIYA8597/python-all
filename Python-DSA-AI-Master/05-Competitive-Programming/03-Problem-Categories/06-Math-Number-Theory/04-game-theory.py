"""
## A. Concept Name
Game Theory in Competitive Programming (Combinatorial Game Theory)

## B. Core Problem
Solving impartial games where two players take turns, and the winner is determined by the last move or the state of the game (e.g., Nim). The challenge is determining the winning strategy optimally without simulating every possibility.

## C. Key Principles
- **Impartial Games:** Games where the allowable moves depend only on the position and not on which player is currently moving.
- **Nim and Nim-Sum:** The game of Nim is solved using the XOR sum (Nim-Sum) of the heap sizes.
- **Sprague-Grundy Theorem:** Every impartial game under normal play convention is equivalent to a Nim heap of a certain size (its Grundy value).
- **Winning/Losing States:** A state with a Nim-Sum or Grundy value of 0 is a losing state (P-position). Any non-zero value is a winning state (N-position).

## D. Implementation Details
- Calculate XOR sums for Nim variations.
- Use Memoization/Dynamic Programming to calculate Grundy values (MEX - Minimum Excluded value) for custom game rules.

## E. Real-world Examples
- **Cryptography and Economics:** Strategic decision making.
- **AI and Game Trees:** Evaluating game states (Minimax, Alpha-Beta pruning) often stems from game theory foundations.
- **Resource Allocation:** Bidding mechanisms and auction theory.

## X. Project Connection
Understanding Game Theory is crucial for optimal decision-making modules in the overarching AI systems, allowing the AI to perfectly evaluate state spaces and guarantee winning moves when available.
"""

def solve_nim(heaps: list[int]) -> bool:
    """
    Solves the standard game of Nim.
    Returns True if the first player can force a win, False otherwise.
    """
    nim_sum = 0
    for heap in heaps:
        nim_sum ^= heap
    return nim_sum != 0

def calculate_mex(s: set[int]) -> int:
    """
    Calculates the Minimum Excluded (MEX) value of a set.
    """
    mex = 0
    while mex in s:
        mex += 1
    return mex

def grundy_values(n: int, allowed_moves: list[int]) -> list[int]:
    """
    Calculates the Grundy values (or nim-values) for a simple subtraction game.
    n: the size of the initial state.
    allowed_moves: a list of allowed subtraction moves.
    """
    g = [0] * (n + 1)
    for i in range(1, n + 1):
        reachable = set()
        for move in allowed_moves:
            if i >= move:
                reachable.add(g[i - move])
        g[i] = calculate_mex(reachable)
    return g

if __name__ == "__main__":
    heaps = [3, 4, 5]
    print(f"Standard Nim with heaps {heaps}: First player wins? {solve_nim(heaps)}")
    
    allowed = [1, 2, 3]
    n_stones = 10
    g_vals = grundy_values(n_stones, allowed)
    print(f"Subtraction game (moves {allowed}) up to {n_stones} stones: {g_vals}")
    print(f"First player wins starting with {n_stones} stones? {g_vals[n_stones] != 0}")
