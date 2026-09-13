"""
# ==============================================================================
# LABORATORY: ADVANCED SHORTEST PATHS (FLOYD-WARSHALL & A*)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dijkstra and Bellman-Ford are "Single-Source" algorithms. They find the shortest 
# path from ONE specific starting node to all other nodes. 
# But what if you are building an airline ticketing system, and you need to precompute 
# the cheapest flight between EVERY pair of cities in the world? 
# Running Dijkstra V times takes O(V * E log V). Running Bellman-Ford V times 
# takes O(V^2 * E).
#
# The Floyd-Warshall Algorithm uses Dynamic Programming to elegantly find the 
# shortest path between EVERY pair of nodes simultaneously in exactly O(V^3) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Dynamic Programming core of Floyd-Warshall (Adjacency Matrix).
# - Implement Floyd-Warshall in 5 lines of code.
# - Understand how A* (A-Star) optimizes Dijkstra using a Heuristic.
#
# ==============================================================================
"""

from typing import List
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FLOYD-WARSHALL ALGORITHM (ALL-PAIRS SHORTEST PATH)
# ==============================================================================
def floyd_warshall(num_vertices: int, edges: List[List[int]]) -> List[List[float]]:
    """
    Time Complexity: exactly O(V^3)
    Space Complexity: O(V^2)
    
    The algorithm operates directly on an Adjacency Matrix.
    """
    # 1. Initialize the Distance Matrix
    # Distances to self are 0. All other initial distances are Infinity.
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        dist[i][i] = 0
        
    # Apply direct edges
    for u, v, weight in edges:
        dist[u][v] = weight
        # If undirected, also add dist[v][u] = weight
        
    # 2. The Core Dynamic Programming Loop
    # We test every possible node `k` to see if it acts as a faster "shortcut" 
    # between node `i` and node `j`.
    for k in range(num_vertices):       # The intermediate "shortcut" node
        for i in range(num_vertices):   # The starting node
            for j in range(num_vertices): # The destination node
                
                # If path [i -> k] + [k -> j] is faster than the current known 
                # path [i -> j], update the matrix!
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    # Note: If dist[i][i] ever becomes less than 0, a Negative Cycle exists!
    return dist

def demonstrate_floyd_warshall():
    section_header("Algorithm: Floyd-Warshall (All-Pairs)")
    
    # Let's map 4 cities: 0, 1, 2, 3
    num_cities = 4
    edges = [
        (0, 1, 3), # 0 to 1 costs 3
        (0, 2, 8), # 0 to 2 costs 8
        (1, 2, 4), # 1 to 2 costs 4
        (1, 3, 2), # 1 to 3 costs 2
        (2, 3, 1), # 2 to 3 costs 1
        (3, 0, 2)  # 3 to 0 costs 2
    ]
    
    print("Finding shortest paths between ALL pairs of cities...")
    all_pairs_matrix = floyd_warshall(num_cities, edges)
    
    print("\nShortest Distance Matrix:")
    print("       To 0   To 1   To 2   To 3")
    print("      -------------------------")
    for i in range(num_cities):
        row_str = " ".join([f"{all_pairs_matrix[i][j]:4}" for j in range(num_cities)])
        print(f"From {i} | {row_str}")
        
    print("\nObserve Matrix[0][2].")
    print("Direct edge from 0 to 2 costs 8.")
    print(f"Matrix calculated shortest path is {all_pairs_matrix[0][2]} (which is 0 -> 1 -> 2: 3 + 4 = 7).")


# ==============================================================================
# 4. A-STAR (A*) SEARCH OVERVIEW
# ==============================================================================
def explain_a_star():
    section_header("Concept: A* (A-Star) Search Algorithm")
    print("""
Dijkstra's Algorithm is perfectly accurate, but it is "Blind". 
If you use Dijkstra to navigate from New York to Los Angeles, the algorithm will 
explore roads leading to Florida and Maine with equal priority, simply because 
they are close to New York. It expands uniformly in a circle.

A* (A-Star) is Dijkstra + a "Heuristic".
Instead of the Priority Queue sorting purely by `distance_from_start`, A* sorts 
the queue by: `distance_from_start + estimated_distance_to_target`.

For geographic routing, the heuristic is usually the "Straight-Line (Euclidean) 
Distance". 
If a road leads towards Florida, the straight-line distance to LA increases, 
dropping its priority in the queue. 
If a road leads West (towards LA), the straight-line distance decreases, putting 
it at the front of the queue.

This forces the search algorithm to aggressively target the destination, often 
finding the shortest path while exploring 90% fewer nodes than Dijkstra!
    """)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Floyd-Warshall use 3 nested loops (O(V^3))?
   Answer: It systematically checks if routing traffic through an intermediate node `k` provides a shorter path between starting node `i` and destination node `j`. It loops over `k`, `i`, and `j` to test every possible combination.

2. Does Floyd-Warshall work with negative edge weights?
   Answer: Yes, because it is essentially a Dynamic Programming approach (like Bellman-Ford) that evaluates paths rather than locking in greedy choices (like Dijkstra). Furthermore, it can detect negative cycles if the diagonal `dist[i][i]` ever drops below 0 (meaning a node can reach itself in negative time).

3. Why use Dijkstra instead of Floyd-Warshall if Floyd-Warshall gives you the answer for ALL pairs at once?
   Answer: Time Complexity! O(V^3) is astronomically slow for large graphs. If a graph has 10,000 nodes, Floyd-Warshall requires 1 Trillion operations (takes minutes/hours). If you only need the path between ONE pair, Dijkstra requires less than 1 million operations (milliseconds). You only use Floyd-Warshall on very small, dense graphs.
"""

if __name__ == "__main__":
    demonstrate_floyd_warshall()
    explain_a_star()
    print("\n[SUCCESS] Laboratory: Advanced Shortest Paths Completed.")
