"""
# ==============================================================================
# LABORATORY: BRANCH AND BOUND (TSP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Traveling Salesperson Problem (TSP) asks: "What is the shortest route 
# that visits every city exactly once and returns to the origin?"
#
# Algorithm 1: Pure Backtracking.
# Explores every single permutation. Time: $O(N!)$. 
# If $N=20$, $20! = 2.4 \times 10^{18}$. Your program will run for 300 years.
#
# Algorithm 2: Dynamic Programming (Held-Karp with Bitmasking).
# Time: $O(N^2 2^N)$. Space: $O(N 2^N)$. 
# If $N=20$, time is a few million operations (1 second). 
# But if $N=30$, the RAM requirement explodes to over 100 Gigabytes! DP crashes.
#
# Algorithm 3: Branch and Bound (BnB).
# Branch and Bound is an intelligent Backtracking search. 
# While exploring the decision tree, you maintain a global variable: 
# `best_solution_so_far`.
# 
# At EVERY step in the search, before you dive deeper, you calculate a 
# Mathematical Lower Bound. You ask: "Assuming absolute best-case miracles, 
# what is the minimum possible cost to finish this path?"
#
# If `current_cost + lower_bound >= best_solution_so_far`, you PRUNE THE BRANCH. 
# You instantly stop exploring. You just mathematically proved that even with a 
# miracle, this path will never beat your current record.
#
# By aggressively pruning branches early, BnB can solve massive NP-Hard problems 
# without the catastrophic memory limits of DP!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Branch and Bound search.
# - Calculate rigorous Mathematical Lower Bounds for TSP.
# - Witness the extreme pruning power of the algorithm.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BRANCH AND BOUND ENGINE
# ==============================================================================
class TSPBranchAndBound:
    def __init__(self, adjacency_matrix: List[List[int]]):
        self.adj = adjacency_matrix
        self.n = len(adjacency_matrix)
        
        self.best_cost = float('inf')
        self.best_path = []
        
        # Performance Tracking
        self.states_explored = 0
        self.branches_pruned = 0
        
    def _calculate_lower_bound(self, current_node: int, visited: List[bool]) -> int:
        """
        Calculates an optimistic Mathematical Lower Bound for the REMAINING path.
        We do this by finding the absolute minimum edge leaving every unvisited 
        node, and assuming (optimistically) that we can take all of them!
        """
        bound = 0
        
        # 1. We MUST leave the `current_node` eventually.
        # What is the cheapest edge leaving the current node to an unvisited node?
        min_leave_current = float('inf')
        for v in range(self.n):
            if not visited[v] and self.adj[current_node][v] != 0:
                min_leave_current = min(min_leave_current, self.adj[current_node][v])
                
        if min_leave_current != float('inf'):
            bound += min_leave_current
            
        # 2. For every OTHER unvisited node, it must be entered and exited.
        # We greedily assume we can take the absolute cheapest edge leaving it!
        for u in range(self.n):
            if not visited[u]:
                min_edge = float('inf')
                for v in range(self.n):
                    # We can't travel to ourselves, but we CAN travel back to 
                    # node 0 (since it's the final destination, and marked visited).
                    if u != v and self.adj[u][v] != 0:
                        min_edge = min(min_edge, self.adj[u][v])
                        
                if min_edge != float('inf'):
                    bound += min_edge
                    
        return bound
        
    def _branch_and_bound_search(
        self, 
        current_node: int, 
        visited_count: int, 
        current_cost: int, 
        current_path: List[int], 
        visited: List[bool]
    ):
        self.states_explored += 1
        
        # 1. BASE CASE: All nodes visited!
        if visited_count == self.n:
            # We must return to the start node (0)
            return_cost = self.adj[current_node][0]
            if return_cost != 0: # If an edge exists back to the start
                total_cost = current_cost + return_cost
                
                # Have we found a new global minimum?
                if total_cost < self.best_cost:
                    self.best_cost = total_cost
                    self.best_path = current_path.copy() + [0]
            return
            
        # 2. CALCULATE THE LOWER BOUND
        bound = self._calculate_lower_bound(current_node, visited)
        
        # 3. THE PRUNING RULE (The absolute core of Branch and Bound)
        # If our current cost + the absolute best-case miracle bound is STILL 
        # worse than the best answer we've already found... PRUNE THE BRANCH!
        if current_cost + bound >= self.best_cost:
            self.branches_pruned += 1
            return
            
        # 4. BRANCHING (Explore Neighbors)
        for v in range(self.n):
            if not visited[v] and self.adj[current_node][v] != 0:
                
                # DO: Mark state
                visited[v] = True
                current_path.append(v)
                
                # RECURSE
                self._branch_and_bound_search(
                    v, 
                    visited_count + 1, 
                    current_cost + self.adj[current_node][v], 
                    current_path, 
                    visited
                )
                
                # UNDO: Backtrack state
                visited[v] = False
                current_path.pop()


    def solve(self) -> Tuple[int, List[int]]:
        """
        Initializes the search from Node 0.
        """
        visited = [False] * self.n
        visited[0] = True # Start at node 0
        current_path = [0]
        
        # We need an initial `best_cost` to start pruning immediately!
        # A simple Greedy approach works well to get a fast, decent upper bound.
        self._greedy_initial_bound()
        
        self._branch_and_bound_search(0, 1, 0, current_path, visited)
        
        return self.best_cost, self.best_path
        
    def _greedy_initial_bound(self):
        """
        Executes a simple Nearest-Neighbor greedy search to establish a decent 
        baseline `best_cost`. The lower the baseline, the more branches we prune!
        """
        visited = [False] * self.n
        visited[0] = True
        curr = 0
        cost = 0
        
        for _ in range(self.n - 1):
            next_node = -1
            min_edge = float('inf')
            
            for v in range(self.n):
                if not visited[v] and self.adj[curr][v] != 0 and self.adj[curr][v] < min_edge:
                    min_edge = self.adj[curr][v]
                    next_node = v
                    
            if next_node == -1: return # Disconnected graph
            
            visited[next_node] = True
            cost += min_edge
            curr = next_node
            
        # Return to start
        if self.adj[curr][0] != 0:
            self.best_cost = cost + self.adj[curr][0]


def demonstrate_bnb():
    section_header("Algorithm: Branch and Bound (TSP)")
    
    # A fully connected 5-node graph with asymmetric weights
    adj_matrix = [
        [ 0, 10, 15, 20, 25],
        [10,  0, 35, 25, 30],
        [15, 35,  0, 30,  5],
        [20, 25, 30,  0, 15],
        [25, 30,  5, 15,  0]
    ]
    
    print("Graph Adjacency Matrix:")
    for row in adj_matrix: print(row)
    
    solver = TSPBranchAndBound(adj_matrix)
    best_cost, best_path = solver.solve()
    
    print("\nSearch Completed!")
    print(f"Optimal TSP Cost : {best_cost}")
    print(f"Optimal Route    : {' -> '.join(map(str, best_path))}")
    
    print("\nPerformance Metrics:")
    print(f"States Explored : {solver.states_explored}")
    print(f"Branches Pruned : {solver.branches_pruned}")
    
    # A 5-node graph has (5-1)! = 24 possible paths.
    # Notice how many branches were physically annihilated before they could 
    # even generate the bottom of the tree!


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Branch & Bound better than Dynamic Programming for TSP when $N=30$?
   Answer: DP uses a Bitmask to track visited states. The state space is $N \times 2^N$. For $N=30$, $30 \times 2^{30} \approx 32$ Billion states! Each state requires 4 bytes of memory, totaling $\approx 128$ Gigabytes of RAM. DP will physically crash your computer due to Out-Of-Memory errors. Branch & Bound is fundamentally a Depth-First Search (Backtracking). DFS only uses $O(N)$ memory for the call stack! BnB can run for days without ever crashing your RAM, and aggressively prunes the search space to finish quickly.

2. What makes a "Good" Lower Bound calculation?
   Answer: It must be mathematically optimistic (it can NEVER overestimate the cost, otherwise it might prune the true optimal answer). It must also be incredibly fast to calculate (e.g., $O(N)$). If calculating the bound takes $O(N^3)$ time, you will waste more CPU time calculating the bound than you would have spent just searching the branch! The greedy "minimum outgoing edge" logic is mathematically strict, never overestimates, and calculates extremely fast.

3. Why do we run a Greedy algorithm BEFORE starting the BnB search?
   Answer: If we initialize `best_cost = Infinity`, the pruning logic `current_cost + bound >= best_cost` will NEVER trigger during the early phases of the search! The algorithm will waste time exploring a ton of terrible branches just to establish the first valid `best_cost`. By running a millisecond Nearest-Neighbor greedy search first, we establish a decent realistic baseline (e.g., `best_cost = 140`). This allows the algorithm to start aggressively pruning terrible branches from the absolute very first step of the recursion!
"""

if __name__ == "__main__":
    demonstrate_bnb()
    print("\n[SUCCESS] Laboratory: Branch and Bound Completed.")
