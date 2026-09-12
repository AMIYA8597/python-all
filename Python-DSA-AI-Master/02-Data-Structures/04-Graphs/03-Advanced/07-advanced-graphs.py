"""
## A. Concept Name
Advanced Graph Algorithms: A* Search and Travelling Salesperson Problem (TSP)

## B. Problem Statement
How can we efficiently find the shortest path in a graph with heuristics, and how do we solve complex combinatorial optimization problems like the TSP?

## C. Real-World Applications
1. A*: GPS Navigation, Pathfinding in Video Games (AI character movement).
2. TSP: Logistics and delivery route planning, printed circuit board manufacturing.

## D. Core Logic
- A*: Extends Dijkstra's algorithm by using a heuristic function to guide the search towards the goal more quickly.
- TSP (Held-Karp): Uses bitmask dynamic programming to record visited nodes and calculate minimum cost Hamiltonian cycles.

## E. Pseudocode
A*:
f_score = g_score + h_score
Use Min-Heap to evaluate node with lowest f_score.
Explore neighbors, update scores if a better path is found.

## F. Step-by-Step Implementation
1. Initialize structures for tracking costs.
2. Push start node to Priority Queue.
3. While PQ is not empty, pop and evaluate.
4. If goal, reconstruct path.
5. Else, iterate neighbors and update distances.

## G. Time and Space Complexity
- A* Time: O(E + V log V) worst-case. Space: O(V).
- TSP Time: O(n^2 * 2^n). Space: O(n * 2^n).

## H. Edge Cases
Disconnected components, Unreachable goals, Graphs with 1 or 2 nodes for TSP.

## I. Common Pitfalls
- A*: Using a non-admissible heuristic which leads to suboptimal paths.
- TSP: Running pure recursion (O(n!)) instead of DP.

## J. Interview Strategy
Mention that A* needs an admissible and consistent heuristic for optimality. For TSP, bring up exact vs approximate solutions.

## K. Walkthrough
Trace the heuristic evaluation for A* as it bypasses nodes moving away from the goal.

## L. Dry Run
A* finds shorter path with minimal expansion compared to standard BFS.

## M. Alternate Approaches
TSP: Approximate solutions like Christofides algorithm, Genetic Algorithms.

## N. Quick Reference
A*: `heapq.heappush(pq, (f_score_val, neighbor))`

## O. Glossary
- Admissible Heuristic: A heuristic that never overestimates the true cost.
- Bitmask: Using integers to represent subsets of a set.

## P. Visual Representation
A* searches in a directed cone shape toward the goal rather than a perfect circle like Dijkstra.

## Q. Code Structure
`a_star()` function for search and `tsp_held_karp()` for dynamic programming.

## R. Test Cases
Test basic paths for A* and small square grids for TSP.

## S. FAQ
Q: Can A* be slower than Dijkstra?
A: No, with heuristic = 0, A* behaves exactly like Dijkstra.

## T. Common Errors
Forgetting to bitwise OR `|` when marking a node visited in TSP DP.

## U. Further Reading
Introduction to Algorithms (CLRS) - Graph theory.

## V. Recommended Next Steps
Learn Flow Networks (Ford-Fulkerson).

## W. Exercise
Modify the A* implementation to work on a 2D grid with Manhattan distance.

## X. Project Connection
Integrate A* into a simple maze-solving application.
"""

import heapq
from typing import List, Tuple, Dict, Callable
import math

# 1. A* Search Algorithm
def a_star(graph: Dict[int, List[Tuple[int, float]]], start: int, goal: int, heuristic: Callable[[int, int], float]) -> Tuple[List[int], float]:
    """
    graph: Adjacency list mapping node -> list of (neighbor, edge_cost)
    heuristic: Function h(n, goal) estimating cost from n to goal
    """
    pq = [(0.0, start)] # (f_score, node)
    
    g_score = {start: 0.0}
    f_score = {start: heuristic(start, goal)}
    came_from = {}
    
    while pq:
        current_f, current = heapq.heappop(pq)
        
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g_score[goal]
            
        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score_val = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f_score_val
                heapq.heappush(pq, (f_score_val, neighbor))
                
    return [], math.inf # No path found

# 2. Travelling Salesperson Problem (TSP) using DP with Bitmask
def tsp_held_karp(dist: List[List[float]]) -> float:
    n = len(dist)
    # memo[(mask, last_node)]
    memo = {}
    
    def dp(mask: int, last: int) -> float:
        if mask == (1 << n) - 1:
            return dist[last][0] # return to start
            
        if (mask, last) in memo:
            return memo[(mask, last)]
            
        ans = math.inf
        for city in range(n):
            if (mask & (1 << city)) == 0: # Not visited
                ans = min(ans, dist[last][city] + dp(mask | (1 << city), city))
                
        memo[(mask, last)] = ans
        return ans
        
    return dp(1, 0) # Start from city 0, mask = 1 (city 0 visited)

def test_advanced_graphs():
    # Test A*
    graph = {
        0: [(1, 1), (2, 4)],
        1: [(2, 2), (3, 5)],
        2: [(3, 1)],
        3: []
    }
    # Dummy heuristic: 0 for all (makes it pure Dijkstra)
    path, cost = a_star(graph, 0, 3, lambda u, v: 0)
    assert path == [0, 1, 2, 3]
    assert cost == 4
    
    # Test TSP
    tsp_graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    min_cost = tsp_held_karp(tsp_graph)
    assert min_cost == 80 # 0 -> 1 -> 3 -> 2 -> 0 (10 + 25 + 30 + 15)
    
    print("All tests passed for Advanced Graph topics.")

if __name__ == "__main__":
    test_advanced_graphs()
