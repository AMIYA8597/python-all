"""
# ==============================================================================
# LABORATORY: HAMILTONIAN CYCLES & TRAVELING SALESPERSON (TSP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that an Eulerian Path (visiting every EDGE exactly once) is easy 
# to solve in O(V + E) time using Hierholzer's Algorithm.
#
# But what if you want to visit every NODE exactly once, and return to the start? 
# This is a "Hamiltonian Cycle". If the graph is weighted, finding the CHEAPEST 
# Hamiltonian Cycle is known as the "Traveling Salesperson Problem" (TSP).
#
# TSP is NP-Hard. There is no known polynomial-time algorithm for it. If you have 
# 20 cities, checking every permutation takes 20! (2.4 quintillion) operations.
# However, using Dynamic Programming with Bitmasking (Bellman-Held-Karp Algorithm), 
# we can reduce the time from O(N!) to O(N^2 * 2^N), making it solvable for ~20 cities.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Eulerian and Hamiltonian problems.
# - Understand how to represent sets of visited cities using Bitmasks.
# - Implement the Bellman-Held-Karp Algorithm for TSP.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BITMASKING FOR SET REPRESENTATION
# ==============================================================================
def explain_bitmasking():
    section_header("Concept: Bitmasks for State Tracking")
    print("""
In DP, we need to memorize the state: "Which cities have we visited?"
Using a Python Set `visited = {0, 2, 3}` as a dictionary key is slow and memory heavy.
Instead, we use a single Integer as a Bitmask!

If we have 4 cities:
City 0 visited? -> 1st bit (2^0 = 1)
City 1 visited? -> 2nd bit (2^1 = 2)
City 2 visited? -> 3rd bit (2^2 = 4)
City 3 visited? -> 4th bit (2^3 = 8)

If we visited cities 0, 2, and 3:
Binary: 1101
Decimal: 8 + 4 + 0 + 1 = 13.

The integer 13 instantly and perfectly represents the set {0, 2, 3}.
We can check if City `i` is visited using Bitwise AND: `mask & (1 << i)`
We can add City `i` to the set using Bitwise OR: `mask | (1 << i)`
    """)


# ==============================================================================
# 4. BELLMAN-HELD-KARP ALGORITHM (TSP)
# ==============================================================================
def tsp(graph: List[List[int]]) -> int:
    """
    Solves the Traveling Salesperson Problem using DP + Bitmasking.
    Time Complexity: O(N^2 * 2^N)
    Space Complexity: O(N * 2^N)
    
    `graph` is an N x N adjacency matrix where graph[i][j] is the cost.
    """
    n = len(graph)
    
    # Memoization table.
    # memo[mask][i] = The minimum cost to visit all cities in `mask`, ending at city `i`.
    memo = {}
    
    # Start at City 0. The mask is 0001 (Decimal 1), meaning only City 0 is visited.
    def dp(mask: int, current_city: int) -> int:
        # Base Case: Have we visited all cities?
        # If n=4, all cities visited is 1111 (Decimal 15, which is 2^4 - 1)
        if mask == (1 << n) - 1:
            # We must return to the starting city (0) to complete the cycle!
            return graph[current_city][0]
            
        # Check memoization cache
        state = (mask, current_city)
        if state in memo:
            return memo[state]
            
        min_cost = float('inf')
        
        # Try traveling to every other city...
        for next_city in range(n):
            # If the next_city has NOT been visited yet...
            if not (mask & (1 << next_city)):
                # Calculate the cost: 
                # (Cost from current to next) + (Optimal cost for the remaining journey)
                new_mask = mask | (1 << next_city)
                cost = graph[current_city][next_city] + dp(new_mask, next_city)
                
                min_cost = min(min_cost, cost)
                
        # Cache and return
        memo[state] = min_cost
        return min_cost

    # Start at mask 1 (City 0 visited), current city 0.
    return dp(1, 0)

def demonstrate_tsp():
    section_header("Algorithm: Traveling Salesperson (DP + Bitmasking)")
    
    # Let's map 4 cities: 0, 1, 2, 3
    # Distances are symmetric for this example, but they don't have to be.
    # Distance from i to i is 0.
    graph = [
        [0,  10, 15, 20],  # From 0 to 0, 1, 2, 3
        [10, 0,  35, 25],  # From 1 to 0, 1, 2, 3
        [15, 35, 0,  30],  # From 2 to 0, 1, 2, 3
        [20, 25, 30, 0 ]   # From 3 to 0, 1, 2, 3
    ]
    
    print("Graph (Distance Matrix):")
    for row in graph:
        print(f"  {row}")
        
    print("\nCalculating Optimal TSP Tour...")
    min_cost = tsp(graph)
    
    print(f"Absolute Minimum Cost to visit all cities and return: {min_cost}")
    print("Optimal Path: 0 -> 1 -> 3 -> 2 -> 0")
    print("Math: 10 + 25 + 30 + 15 = 80")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is TSP so hard compared to Minimum Spanning Tree (MST)?
   Answer: MST just wants to connect all nodes as cheaply as possible, often forming branches. It can be solved greedily (Prim's/Kruskal's) in polynomial time. TSP strictly requires a continuous CYCLE visiting every node exactly once. Because of this strict structural constraint, greedy algorithms fail, and you must evaluate massive numbers of permutations (NP-Hard).

2. How much faster is Bellman-Held-Karp compared to Brute Force for 20 cities?
   Answer: Brute force evaluates `20!` permutations, which is ~2,432,902,000,000,000,000 operations (would take hundreds of years). BHK takes `O(20^2 * 2^20)`, which is `400 * 1,048,576 = 419,430,400` operations (takes less than a second in C++ or a few seconds in Python).

3. Can DP + Bitmasking solve TSP for 100 cities?
   Answer: No. `2^100` is astronomically huge. For 100 cities, it is mathematically impossible to find the *perfect* optimal route. Instead, routing software (like UPS or FedEx) uses Heuristics and Approximation Algorithms (like Simulated Annealing or Genetic Algorithms) to find a route that is "good enough" (e.g., within 2% of the optimal).
"""

if __name__ == "__main__":
    explain_bitmasking()
    demonstrate_tsp()
    print("\n[SUCCESS] Laboratory: Advanced Graphs (TSP & Bitmasking) Completed.")
