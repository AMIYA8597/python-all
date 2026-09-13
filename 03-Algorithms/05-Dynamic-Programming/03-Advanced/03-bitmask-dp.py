"""
# ==============================================================================
# LABORATORY: BITMASK DP (THE TRAVELING SALESPERSON)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Traveling Salesperson Problem (TSP) is arguably the most famous algorithm 
# problem in human history.
# Given a list of cities and the distances between them, find the absolute 
# shortest route that visits EVERY city and returns to the starting city.
#
# It is NP-Hard.
# If you use naive Backtracking, you explore every permutation of paths. 
# Time Complexity: O(N!).
# If N = 20 cities, 20! is 2.4 Quintillion operations. Your computer will take 
# 77,000 years to find the shortest route.
#
# But using Dynamic Programming, we can optimize it using the Held-Karp Algorithm.
# How do we represent the DP State of "Which cities have we visited so far?"
# We could use an Array `visited = [True, False, True]`, but arrays cannot be 
# used as Dictionary Keys for Memoization!
#
# We use a **Bitmask**. 
# An integer where each binary bit represents a city. 
# `5` in binary is `101`. This perfectly represents "City 0 is visited, City 1 
# is NOT visited, City 2 is visited."
# By using integers as the state, DP can shatter the O(N!) barrier down to 
# O(N^2 * 2^N). A 77,000-year problem suddenly solves in 0.4 seconds!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Bitwise operators (`<<`, `&`, `|`) for state management.
# - Implement the Held-Karp TSP Algorithm.
# - Understand how DP transforms Factorial time to Exponential time.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HELD-KARP BITMASK DP
# ==============================================================================
def solve_tsp(graph: List[List[int]]) -> int:
    """
    Time Complexity: O(N^2 * 2^N)
    Space Complexity: O(N * 2^N) for the Memoization cache.
    """
    n = len(graph)
    
    # The final goal state where EVERY city is visited.
    # If N = 4, `1 << 4` is 16 (Binary 10000). Subtract 1 = 15 (Binary 1111).
    # `1111` means cities 0, 1, 2, and 3 are ALL visited!
    ALL_VISITED_MASK = (1 << n) - 1
    
    # Memoization Cache
    # Key: (mask, current_city)
    memo = {}
    
    def dp(mask: int, pos: int) -> int:
        # 1. BASE CASE (SUCCESS)
        # We have visited every single city.
        if mask == ALL_VISITED_MASK:
            # We must return to the STARTING city (City 0) to complete the loop!
            # Return the distance from our current `pos` back to `0`.
            return graph[pos][0]
            
        # 2. MEMOIZATION CHECK
        state = (mask, pos)
        if state in memo:
            return memo[state]
            
        ans = math.inf
        
        # 3. EXPLORE CHOICES
        # We are currently at city `pos`. Where can we go next?
        # Try going to every city `nxt` from 0 to N-1.
        for nxt in range(n):
            
            # --- THE BITMASK CHECK ---
            # Check if we have ALREADY visited city `nxt`.
            # We left-shift a 1 into the `nxt` position (e.g. if nxt=2, `1<<2` = 100).
            # We perform a Bitwise AND (`&`) with the mask.
            # If the mask was `101`, `101 & 100` = 100 (Not Zero!). It was visited.
            # If the mask was `001`, `001 & 100` = 000 (Zero!). It is unvisited.
            if (mask & (1 << nxt)) == 0:
                
                # We haven't visited it! Let's go there.
                
                # --- UPDATE THE MASK ---
                # We use Bitwise OR (`|`) to flip the bit to 1.
                # `001 | 100` = `101`.
                new_mask = mask | (1 << nxt)
                
                # --- STATE TRANSITION ---
                # The total cost of this path is the distance from `pos` to `nxt`, 
                # PLUS the optimal distance to finish the rest of the tour!
                cost = graph[pos][nxt] + dp(new_mask, nxt)
                
                # Keep track of the absolute shortest path
                ans = min(ans, cost)
                
        # 4. CACHE AND RETURN
        memo[state] = ans
        return ans

    # Start at City 0.
    # Initial Mask: City 0 is visited. (1 << 0) = 1 (Binary: 001).
    return dp(1, 0)


def demonstrate_tsp():
    section_header("Algorithm: TSP (Held-Karp Bitmask DP)")
    
    # 4 Cities (0, 1, 2, 3)
    # The matrix represents the distance between them.
    # e.g. graph[0][1] = 10 (Distance from 0 to 1 is 10)
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    print("Distance Matrix:")
    for row in graph:
        print(" " + str(row))
        
    print("\nExecuting Held-Karp Algorithm...")
    ans = solve_tsp(graph)
    
    print(f"Shortest Hamiltonian Cycle (TSP): {ans}")
    print("Optimal Path: 0 -> 1 -> 3 -> 2 -> 0")
    print("Math: 10 + 25 + 30 + 15 = 80")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does DP optimize TSP from $O(N!)$ to $O(N^2 \\times 2^N)$?
   Answer: Overlapping Subproblems! Imagine you start at City 0. 
   Path 1: 0 -> A -> B -> C. 
   Path 2: 0 -> B -> A -> C. 
   In naive backtracking, these are treated as completely different execution trees and are evaluated separately. But notice: in BOTH paths, you are currently at City C, and the exact same set of cities {A, B} has been visited. The optimal path to finish the remaining unvisited cities is mathematically identical! By caching the state `(mask=0111, pos=C)`, DP instantly skips re-evaluating the permutations.

2. Why do we use Bitmasks instead of Python Tuples `(True, False, True)` for the state?
   Answer: Bitmasks are raw Integers. Creating a new integer via `mask | (1 << nxt)` takes 1 CPU clock cycle. Hashing an integer for a dictionary lookup takes $O(1)$ time. If we used Tuples, every state transition would require allocating a brand new Tuple in RAM, and hashing a tuple requires iterating through every element inside it $O(N)$, causing massive memory and CPU overhead.

3. Is $O(N^2 \\times 2^N)$ considered fast?
   Answer: It is "fast" relative to the astronomical $O(N!)$. But it is still Exponential time! While $N=20$ solves in less than a second, $N=40$ will crash any supercomputer on Earth. For large scale logistics (like UPS routing 1,000 trucks), companies do NOT use this algorithm. They use Heuristics (like Simulated Annealing or Ant Colony Optimization) to find a "Good Enough" approximate answer, rather than calculating the mathematically perfect shortest path.
"""

if __name__ == "__main__":
    demonstrate_tsp()
    print("\n[SUCCESS] Laboratory: Bitmask DP Completed.")
