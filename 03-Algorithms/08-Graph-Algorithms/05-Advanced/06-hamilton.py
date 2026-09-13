"""
# ==============================================================================
# LABORATORY: HAMILTONIAN PATHS (DP WITH BITMASKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you solved the Eulerian Path (visiting every EDGE exactly 
# once) in blazing fast O(V+E) time.
#
# What if we change the rule? What if you are a FedEx delivery driver, and you 
# must visit every CITY (VERTEX) exactly once?
#
# Welcome to the Hamiltonian Path (and its famous weighted sibling, the 
# Traveling Salesperson Problem). 
# This problem is NP-Complete. There is no known mathematical trick to solve 
# it in polynomial time.
#
# A naive algorithm uses Backtracking. It tries every possible permutation of 
# cities. Time Complexity: O(V!). 
# If you have 20 cities, V! is 2,432,902,008,176,640,000 operations. 
# A supercomputer would take decades to calculate the route.
#
# Can we do better? Yes.
# In 1962, Richard Bellman, Michael Held, and Richard Karp applied Dynamic 
# Programming (DP) to this problem.
#
# They realized that if you have already visited Cities {A, B, C} and you are 
# currently standing in City C, IT DOES NOT MATTER if you took the route 
# A->B->C or B->A->C. The future of the route only depends on two things:
# 1. The exact set of cities you have visited so far.
# 2. The exact city you are currently standing in.
#
# By caching this state using a "Bitmask" (an integer where the bits represent 
# visited cities), the time complexity drops from O(V!) to O(V^2 * 2^V).
# For 20 cities, this is 419,000,000 operations. It executes in milliseconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the horrific scale of O(V!).
# - Master Bitmasking for state representation (`1 << i`).
# - Implement the Bellman-Held-Karp Top-Down DP algorithm.
#
# ==============================================================================
"""

import math
from typing import List, Tuple, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BELLMAN-HELD-KARP DP ENGINE (O(V^2 * 2^V))
# ==============================================================================
class HamiltonianTSP:
    def __init__(self, vertices: int, graph: List[List[float]]):
        self.V = vertices
        self.graph = graph
        
        # The DP Memoization Cache.
        # Key: (bitmask, current_city) -> Value: Shortest remaining distance
        self.memo = {}
        
        # To reconstruct the path!
        # Key: (bitmask, current_city) -> Value: Next City to visit
        self.parent_map = {}
        
    def _tsp_dp(self, bitmask: int, current_city: int) -> float:
        """
        Top-Down Dynamic Programming with Bitmasking.
        Returns the absolute shortest distance to visit all REMAINING unvisited cities 
        and return to the Start (City 0).
        """
        # 1. BASE CASE: All cities have been visited!
        # If V = 4, the target bitmask is 1111 in binary (which is 2^4 - 1 = 15).
        if bitmask == (1 << self.V) - 1:
            # We must return to the Start (City 0) to complete the Hamiltonian Cycle!
            return self.graph[current_city][0]
            
        # 2. MEMOIZATION CHECK
        if (bitmask, current_city) in self.memo:
            return self.memo[(bitmask, current_city)]
            
        ans = math.inf
        best_next_city = -1
        
        # 3. EXPLORE ALL UNVISITED CITIES
        for next_city in range(self.V):
            
            # Use bitwise AND to check if `next_city` is ALREADY in the bitmask!
            # If the bit is 0, it means it is unvisited!
            if (bitmask & (1 << next_city)) == 0:
                
                # We can physically travel there (edge exists)
                if self.graph[current_city][next_city] != math.inf:
                    
                    # Create the NEW bitmask by turning on the bit for `next_city` (Bitwise OR)
                    new_bitmask = bitmask | (1 << next_city)
                    
                    # Recurse to find the cost of the remaining journey!
                    cost_of_remaining_journey = self._tsp_dp(new_bitmask, next_city)
                    
                    total_cost = self.graph[current_city][next_city] + cost_of_remaining_journey
                    
                    if total_cost < ans:
                        ans = total_cost
                        best_next_city = next_city
                        
        # 4. CACHE THE RESULT
        self.memo[(bitmask, current_city)] = ans
        if best_next_city != -1:
            self.parent_map[(bitmask, current_city)] = best_next_city
            
        return ans

    def solve(self) -> Tuple[float, List[int]]:
        # Start at City 0. 
        # The bitmask is 1 (which is 0001 in binary), meaning City 0 is visited.
        initial_bitmask = 1
        start_city = 0
        
        min_cost = self._tsp_dp(initial_bitmask, start_city)
        
        # Path Reconstruction
        path = [start_city]
        curr_mask = initial_bitmask
        curr_city = start_city
        
        while True:
            if (curr_mask, curr_city) not in self.parent_map:
                break
            next_city = self.parent_map[(curr_mask, curr_city)]
            path.append(next_city)
            curr_mask = curr_mask | (1 << next_city)
            curr_city = next_city
            
        # Add the return to start!
        path.append(start_city)
        
        return min_cost, path


def demonstrate_tsp():
    section_header("Algorithm: Traveling Salesperson Problem (TSP DP)")
    
    vertices = 4
    INF = math.inf
    # Complete Graph Adjacency Matrix
    graph = [
        [0,  10, 15, 20],
        [10, 0,  35, 25],
        [15, 35, 0,  30],
        [20, 25, 30, 0 ]
    ]
    
    print("Graph Edge Matrix (Costs):")
    for row in graph: print(row)
        
    print("\nExecuting Bellman-Held-Karp DP with Bitmasking...")
    tsp = HamiltonianTSP(vertices, graph)
    cost, route = tsp.solve()
    
    print(f"\nAbsolute Minimum Cost for Hamiltonian Cycle: ${cost}")
    print(f"Optimal Route: {' -> '.join(map(str, route))}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Bitmasking reduce the time complexity so drastically?
   Answer: In brute-force backtracking, $A \\to B \\to C$ and $B \\to A \\to C$ are completely separate branches of the DFS tree. The recursion will blindly re-calculate the exact same subproblem (visiting $D, E, F$ starting from $C$) twice! Bitmasking realizes that the SET $\{A, B, C\}$ is represented by the exact same integer `0111` in binary. When the second branch hits City C with the bitmask `0111`, it instantly returns the cached $O(1)$ answer from the DP Memo, pruning Trillions of redundant recursive branches!

2. Why use integers for bitmasking instead of a Python `Set` or `List`?
   Answer: Memory and Speed! A Python Set or List is a massive, heavy object in memory. You cannot use a mutable List as a Dictionary Key for memoization. An integer is a microscopic, immutable primitive type. Checking if a city is visited takes 1 CPU clock cycle using Bitwise AND `(mask & (1 << city))`. Adding a city takes 1 clock cycle using Bitwise OR `(mask | (1 << city))`. It is the fastest possible way to manage state.

3. Is $O(V^2 2^V)$ fast enough for large graphs?
   Answer: No. It works flawlessly up to $V = 22$. Beyond 22 cities, the $2^V$ exponential growth term causes the RAM cache to explode (out of memory) and CPU time to spike into minutes/hours. For a 100-city TSP, no known exact polynomial algorithm exists. You must abandon exactness and use "Heuristic/Approximation Algorithms" (Simulated Annealing, Genetic Algorithms, Ant Colony Optimization, or Christofides' 1.5-Approximation) which return a "pretty good" route in polynomial time.
"""

if __name__ == "__main__":
    demonstrate_tsp()
    print("\n[SUCCESS] Laboratory: Hamiltonian Paths & TSP Completed.")
