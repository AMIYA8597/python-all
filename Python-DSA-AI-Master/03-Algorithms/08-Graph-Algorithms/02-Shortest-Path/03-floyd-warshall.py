"""
Floyd-Warshall Algorithm (All-Pairs Shortest Path)

===============================================================================
1. INTRODUCTION & LEARNING OBJECTIVES
===============================================================================
What is the Floyd-Warshall Algorithm?
Floyd-Warshall is a dynamic programming algorithm for finding shortest paths in 
a directed or undirected weighted graph with positive or negative edge weights. 
Unlike Dijkstra's (single source), Floyd-Warshall finds the shortest path 
between ALL pairs of vertices.

Learning Objectives:
- Understand the DP formulation of the all-pairs shortest path problem.
- Implement the Floyd-Warshall algorithm using an adjacency matrix.
- Detect negative weight cycles in a graph.
- Analyze the O(V^3) time complexity and trade-offs compared to running 
  Dijkstra's from every node.

===============================================================================
2. CONCEPT EXPLANATION & INDUSTRY USE CASES
===============================================================================
Core Concept:
The algorithm considers all possible paths between every pair of vertices `u` 
and `v`. It iteratively considers each vertex `k` as an intermediate point.
If the path from `u` to `k` plus the path from `k` to `v` is shorter than the 
currently known direct path from `u` to `v`, it updates the shortest path.

Recurrence Relation:
distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

Industry Use Cases:
- Arbitrage Detection: Finding negative cycles in foreign exchange markets.
- Network Analysis: Calculating the diameter or centralities of a network.
- Game AI: Precomputing all distances in a small map for instant lookup.

===============================================================================
3. IMPLEMENTATION & ADVANCED CONCEPTS
===============================================================================
We represent the graph as an adjacency matrix where `matrix[i][j]` is the weight 
of the edge from `i` to `j`. If there is no edge, it is `infinity`.
"""

from typing import List, Optional

def floyd_warshall(graph_matrix: List[List[float]]) -> Optional[List[List[float]]]:
    """
    Computes all-pairs shortest paths using the Floyd-Warshall algorithm.

    Args:
        graph_matrix: A 2D list representing the adjacency matrix of the graph.
                      graph_matrix[i][j] is the weight from i to j.
                      Use float('inf') for missing edges.

    Returns:
        A 2D list representing the shortest distance between all pairs.
        Returns None if a negative-weight cycle is detected.
    """
    V = len(graph_matrix)
    
    # Initialize the distance matrix by copying the input matrix
    dist = [[graph_matrix[i][j] for j in range(V)] for i in range(V)]
    
    # Ensure distance from a node to itself is 0
    for i in range(V):
        dist[i][i] = 0

    # Core Algorithm: DP approach
    # k acts as the intermediate vertex
    for k in range(V):
        # i acts as the source vertex
        for i in range(V):
            # j acts as the destination vertex
            for j in range(V):
                # Update the shortest path if passing through k is cheaper
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

    # Negative Cycle Detection
    # If the distance from a node to itself becomes negative, there's a negative cycle
    for i in range(V):
        if dist[i][i] < 0:
            print("Negative weight cycle detected!")
            return None

    return dist


def reconstruct_path_fw(next_node_matrix: List[List[Optional[int]]], u: int, v: int) -> List[int]:
    """
    (Advanced) Reconstructs path. Requires a modified FW that stores the 'next' node.
    """
    if next_node_matrix[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = next_node_matrix[u][v]
        path.append(u)
    return path


===============================================================================
4. COMPLEXITY ANALYSIS
===============================================================================
- Time Complexity: O(V^3) where V is the number of vertices. Three nested loops, 
  each iterating V times.
- Space Complexity: O(V^2) for the 2D distance matrix.

Comparison:
Running Dijkstra V times takes O(V * (V + E) log V). For dense graphs (E ≈ V^2), 
this is O(V^3 log V), making Floyd-Warshall slightly faster and much simpler to 
implement. However, for sparse graphs, V*Dijkstra's is usually faster.

===============================================================================
5. COMMON MISTAKES & INTERVIEW QUESTIONS
===============================================================================
Mistake: Incorrect loop ordering. 
The outer loop MUST be `k` (the intermediate vertex). If `k` is the inner loop, 
the algorithm will fail to find shortest paths that require multiple intermediate 
nodes because it won't properly build upon previously calculated multi-hop paths.

Interview Challenge:
"Given a list of currency exchange rates, find out if it's possible to start 
with 1 unit of a currency and end up with more than 1 unit through a series of 
trades (Arbitrage)."
(Hint: Transform weights using -log(rate) and use Floyd-Warshall or Bellman-Ford 
to find negative cycles).

===============================================================================
6. TESTS & ASSERTIONS
===============================================================================
if __name__ == "__main__":
    INF = float('inf')
    
    # Example Graph (4 vertices)
    # (0)---5--->(1)
    #  |         / |
    #  |        /  |
    #  10    -3    3
    #  |    /      |
    #  v   v       v
    # (3)<---1---(2)
    
    graph = [
        [0,   5,   INF, 10],
        [INF, 0,   3,   INF],
        [INF, INF, 0,   1],
        [INF, -3,  INF, 0]
    ]

    shortest_paths = floyd_warshall(graph)
    
    print("All-Pairs Shortest Paths Matrix:")
    if shortest_paths:
        for row in shortest_paths:
            print(["INF" if x == INF else x for x in row])
            
        assert shortest_paths[0][0] == 0
        assert shortest_paths[0][1] == 5
        assert shortest_paths[0][2] == 8
        assert shortest_paths[0][3] == 9
        assert shortest_paths[3][1] == -3
        assert shortest_paths[3][2] == 0
        assert shortest_paths[3][3] == 0

    # Test Negative Cycle Detection
    graph_neg_cycle = [
        [0,   1,   INF],
        [INF, 0,   -1],
        [-1,  INF, 0]
    ]
    
    result = floyd_warshall(graph_neg_cycle)
    assert result is None, "Should detect negative cycle"

    print("All Floyd-Warshall tests passed!")
