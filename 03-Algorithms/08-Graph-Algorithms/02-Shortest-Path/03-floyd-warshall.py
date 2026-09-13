"""
# ==============================================================================
# LABORATORY: FLOYD-WARSHALL (ALL-PAIRS SHORTEST PATH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dijkstra and Bellman-Ford are Single-Source Shortest Path (SSSP) algorithms. 
# You give them ONE start node (e.g., New York), and they find the distance to 
# every other city.
#
# What if you are building an airline ticketing database, and you need a massive 
# lookup table containing the shortest flight time between EVERY possible pair 
# of cities on Earth simultaneously? 
# (This is the All-Pairs Shortest Path or APSP problem).
#
# You *could* just run Dijkstra $V$ times (once for every city). That works!
# But what if there are negative edges? Dijkstra crashes. 
# You *could* run Bellman-Ford $V$ times, but that takes O(V^4) time!
#
# Enter the Floyd-Warshall Algorithm (1962).
# It doesn't use Heaps. It doesn't sweep edge lists. 
# It uses an Adjacency Matrix and Dynamic Programming.
# With three beautifully simple nested `for` loops, it solves the APSP problem 
# in exactly O(V^3) time.
#
# The Core Idea: 
# To find the shortest path from $i$ to $j$, we check if routing THROUGH a 
# middleman node $k$ is faster than the direct path!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Adjacency Matrix representation of graphs.
# - Implement the 3-loop Floyd-Warshall DP engine.
# - Understand why the $k$ loop MUST be on the outside.
# - Detect Negative Cycles globally using the matrix diagonal.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FLOYD-WARSHALL DP ENGINE (O(V^3))
# ==============================================================================
def floyd_warshall(vertices: int, adjacency_matrix: List[List[float]]) -> List[List[float]]:
    """
    Computes the shortest path between all pairs of vertices.
    Expects an initialized Adjacency Matrix where matrix[i][j] is the edge weight.
    If no edge exists, matrix[i][j] should be math.inf.
    matrix[i][i] MUST be 0.
    """
    
    # Create a deep copy of the matrix so we don't mutate the original input
    dist = [[adjacency_matrix[i][j] for j in range(vertices)] for i in range(vertices)]
    
    # --------------------------------------------------------------------------
    # THE MAGICAL 3 LOOPS
    # --------------------------------------------------------------------------
    # k = The "middleman" node we are currently allowing paths to route through.
    # THIS MUST BE THE OUTER LOOP.
    for k in range(vertices):
        
        # i = The Start node
        for i in range(vertices):
            
            # j = The Target node
            for j in range(vertices):
                
                # The Dynamic Programming Recurrence Relation:
                # Is routing from [i -> k] and then [k -> j] strictly FASTER 
                # than the currently known path [i -> j]?
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    # --------------------------------------------------------------------------
    # NEGATIVE CYCLE DETECTION
    # --------------------------------------------------------------------------
    # The mathematical distance from a node to ITSELF is exactly 0.
    # If `dist[i][i]` ever drops BELOW zero, it physically proves that the node 
    # left itself, traveled through a negative time-travel loop, and arrived 
    # back at itself with negative distance!
    for i in range(vertices):
        if dist[i][i] < 0:
            raise ValueError(f"CRITICAL: Negative Cycle detected involving node {i}!")
            
    return dist


def demonstrate_floyd_warshall():
    section_header("Algorithm: Floyd-Warshall (APSP)")
    
    INF = math.inf
    vertices = 4
    
    # Adjacency Matrix for a 4-node graph
    # Row = Source, Col = Destination
    # E.g., graph[0][1] = 5 means edge from 0 to 1 has weight 5.
    graph = [
        [0,   5,  INF, 10],  # From Node 0
        [INF, 0,    3, INF],  # From Node 1
        [INF, INF,  0,   1],  # From Node 2
        [INF, INF, INF,  0]   # From Node 3
    ]
    
    print("Initial Adjacency Matrix (Direct Edges):")
    for row in graph: print(row)
        
    print("\nExecuting O(V^3) Dynamic Programming...")
    shortest_paths = floyd_warshall(vertices, graph)
    
    print("\nFinal All-Pairs Shortest Path Matrix:")
    for i, row in enumerate(shortest_paths): 
        print(f"From {i}: {row}")
        
    print("\nObservation:")
    print("Notice `graph[0][3]` was originally 10.")
    print("But the final matrix shows the shortest path is 9!")
    print("It routed through: 0 -> 1 -> 2 -> 3  (5 + 3 + 1 = 9).")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why MUST the $k$ loop be on the outside?
   Answer: Floyd-Warshall is fundamentally a Dynamic Programming algorithm. The state definition is $DP[k][i][j]$: "The shortest path from $i$ to $j$ using ONLY nodes $0$ to $k$ as middlemen". To calculate state $k$, you MUST have fully calculated the entire matrix for state $k-1$! If you put $i$ or $j$ on the outside, you would evaluate routes before the necessary intermediate middleman routes were finalized, destroying the DP overlapping subproblem guarantee.

2. Does Floyd-Warshall reconstruct the exact path?
   Answer: By default, no, it only gives the integer distance. However, you can initialize a secondary $V \\times V$ `NextNode` matrix. Whenever you execute the `if dist[i][k] + dist[k][j] < dist[i][j]` update block, you also update `NextNode[i][j] = NextNode[i][k]`. After the algorithm finishes, you can use the `NextNode` matrix to reconstruct the exact physical path array between any two nodes in $O(V)$ time!

3. When should I use Floyd-Warshall instead of Dijkstra?
   Answer: 
   - If the graph is sparse ($E \approx V$), running Dijkstra $V$ times yields $O(V^2 \\log V)$, which absolutely crushes Floyd-Warshall's rigid $O(V^3)$.
   - If the graph is insanely dense ($E \approx V^2$), running Dijkstra $V$ times yields $O(V^3 \\log V)$. In this case, Floyd-Warshall is strictly faster.
   - If the graph has Negative Edges, Dijkstra crashes. You must use Floyd-Warshall.
   - In FAANG interviews, if $V \le 400$, Floyd-Warshall is the safest and easiest algorithm to write, as the 3 nested loops are mathematically flawless and impossible to implement incorrectly under pressure.
"""

if __name__ == "__main__":
    demonstrate_floyd_warshall()
    print("\n[SUCCESS] Laboratory: Floyd-Warshall Algorithm Completed.")
