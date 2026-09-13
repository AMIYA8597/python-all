"""
# ==============================================================================
# LABORATORY: PROBABILITY DP (EXPECTED VALUE & MARKOV CHAINS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Thus far, Dynamic Programming has been used to find MAX profits, MIN costs, 
# or BOOLEAN validity.
# But DP is also the foundation of Quantitative Finance, Machine Learning 
# (Reinforcement Learning), and advanced Statistics.
#
# We use DP to calculate Mathematical Probability and Expected Value.
# 
# Classic Problem: "Knight Probability in Chessboard".
# A Knight starts at `(start_row, start_col)` on an NxN chessboard. It makes 
# exactly `K` random legal moves. If it moves off the board, it dies. 
# What is the exact mathematical probability that it remains on the board after 
# `K` moves?
#
# A naive simulation (Monte Carlo) would run 10 Million random walks and divide 
# the survivals by 10 Million. It would be slow and mathematically imprecise.
# Probability DP computes the exact mathematical fraction in O(K * N^2) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Probability State Transitions.
# - Model a Markov Chain Process using DP.
# - Implement Space Optimization for 3D State grids.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PROBABILITY TABULATION (3D DP -> 2D OPTIMIZED)
# ==============================================================================
def knight_probability(n: int, k: int, start_row: int, start_column: int) -> float:
    """
    Time Complexity: O(K * N^2)
    Space Complexity: O(N^2) (Space optimized from 3D O(K * N^2)).
    """
    
    # 1. STATE DEFINITION
    # Normally, we would need a 3D matrix `dp[step][row][col]`.
    # But because step 5 ONLY cares about the probabilities in step 4, we only 
    # need TWO 2D grids: `current_dp` and `next_dp`!
    
    # Initialize the starting grid (Step 0)
    # The Knight is 100% guaranteed to be on the starting square!
    current_dp = [[0.0 for _ in range(n)] for _ in range(n)]
    current_dp[start_row][start_column] = 1.0
    
    # The 8 possible L-shaped moves for a Knight
    moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    # 2. THE MARKOV CHAIN LOOP
    # We step time forward exactly `k` times.
    for step in range(k):
        
        # Create a blank grid for the new probabilities in this next step
        next_dp = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Scan every square on the board to see if the Knight could be there
        for r in range(n):
            for c in range(n):
                
                # If there is a non-zero probability the Knight is currently here...
                if current_dp[r][c] > 0:
                    
                    # The Knight will randomly pick one of 8 moves.
                    # Each move has a 1/8 (0.125) probability of occurring.
                    move_prob = current_dp[r][c] / 8.0
                    
                    for r_offset, c_offset in moves:
                        next_r, next_c = r + r_offset, c + c_offset
                        
                        # --- STATE TRANSITION ---
                        # If the move lands SAFELY on the board...
                        if 0 <= next_r < n and 0 <= next_c < n:
                            # We ADD the fractional probability to that new square!
                            # (We use ADD because multiple different Knight paths 
                            # could converge on the exact same square simultaneously).
                            next_dp[next_r][next_c] += move_prob
                            
        # The step is over. The new grid becomes the current grid.
        current_dp = next_dp
        
    # 3. FINAL AGGREGATION
    # After `k` steps, the `current_dp` grid holds the exact fractional 
    # probabilities of the Knight being on every single square.
    # To find the total probability of survival, we just sum up the whole grid!
    total_survival_probability = 0.0
    for r in range(n):
        for c in range(n):
            total_survival_probability += current_dp[r][c]
            
    return total_survival_probability


def demonstrate_probability_dp():
    section_header("Algorithm: Probability DP (Knight's Survival)")
    
    n = 3
    k = 2
    start_row = 0
    start_col = 0
    
    print(f"Board Size: {n}x{n}")
    print(f"Start Position: ({start_row}, {start_col}) -> Top-Left Corner")
    print(f"Number of Moves: {k}\n")
    
    ans = knight_probability(n, k, start_row, start_col)
    
    print(f"Mathematical Probability of Survival: {ans:.6f}")
    print("Explanation:")
    print("Step 1: The knight has 2 safe moves out of 8 (lands on 1,2 or 2,1). Prob = 2/8 = 0.25")
    print("Step 2: From 1,2, it has 2 safe moves. From 2,1 it has 2 safe moves.")
    print("Total safe branches = 4. Total possible branches = 64.")
    print("4 / 64 = 0.0625")
    
    n = 8
    k = 10
    print(f"\nScaling up: 8x8 Board, 10 Moves from Center (4,4).")
    ans2 = knight_probability(n, k, 4, 4)
    print(f"Mathematical Probability of Survival: {ans2:.6f}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is this called a "Markov Chain Process"?
   Answer: A Markov Process is a mathematical system that transitions from one state to another, under the strict rule that the FUTURE state depends ONLY on the CURRENT state, and not on the sequence of events that preceded it (Memorylessness). Because step `k` only reads the probabilities of step `k-1`, it perfectly models a Markov Chain.

2. Why do we ADD probabilities together at the target square `next_dp[next_r][next_c] += move_prob`?
   Answer: The Law of Total Probability! If you want to know the probability of the Knight being on square `(2,2)` at step 5, you must sum up the mutually exclusive probabilities of every possible way it could have arrived there. It could have jumped from `(0,1)` OR from `(1,0)`. In probability theory, "OR" translates to Addition.

3. How does this differ from Monte Carlo simulation?
   Answer: Monte Carlo uses a Random Number Generator to physically simulate 1 million L-shaped paths. It is an "Approximation" algorithm. Probability DP does not use any randomness; it calculates the exhaustive mathematical permutations and divides by the state space, resulting in the mathematically perfect exact fraction, instantly.
"""

if __name__ == "__main__":
    demonstrate_probability_dp()
    print("\n[SUCCESS] Laboratory: Probability DP Completed.")
