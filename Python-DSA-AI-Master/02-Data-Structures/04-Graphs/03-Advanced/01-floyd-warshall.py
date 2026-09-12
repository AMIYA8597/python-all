"""
## A. Concept Name
Floyd-Warshall Algorithm

## B. Problem Statement
Find the shortest paths between all pairs of vertices in a weighted graph.

## C. Real-World Applications
Network routing protocols, urban traffic planning, social network connectivity, arbitrage detection in currency exchange.

## D. Core Mechanism
Dynamic programming approach that incrementally updates the shortest paths between all pairs of vertices by considering all vertices as intermediate nodes one by one.

## E. Time & Space Complexity
Time Complexity: O(V^3) where V is the number of vertices.
Space Complexity: O(V^2) for the distance matrix.

## F. Step-by-Step Explanation
1. Initialize the distance matrix with direct edge weights between nodes. Set non-adjacent nodes to infinity, and self-loops to 0.
2. Iterate through all possible intermediate vertices (k).
3. For each intermediate vertex, iterate through all pairs of nodes (i, j).
4. Update the shortest path from i to j to be the minimum of the current shortest path and the path through k.

## G. Implementation Variations
Basic matrix implementation, path reconstruction extension (using a 'next' matrix), and transitive closure (using boolean operations).

## H. Common Pitfalls & Anti-Patterns
Forgetting to initialize self-loops to 0 or missing the order of loops (the intermediate vertex loop must be the outermost loop).

## I. Interview & System Design Questions
Q: How can you use Floyd-Warshall to detect negative cycles?
A: Check the diagonal of the final distance matrix. If any distance from a node to itself is less than 0, there is a negative weight cycle.

## J. Alternative Approaches
Johnson's algorithm for sparse graphs (O(V^2 log V + VE) using Bellman-Ford and Dijkstra). Running Dijkstra V times.

## K. Memory & Performance Implications
Requires O(V^2) memory which can be prohibitive for graphs with millions of nodes. High cache locality if arrays are packed properly.

## L. Edge Cases & Constraints
Empty graphs, single-node graphs, disconnected components, and graphs with negative weight cycles.

## M. Distributed/Scalable System Considerations
For extremely large graphs, block-based Floyd-Warshall (Kleene's algorithm) or distributed frameworks (like Pregel or Apache Giraph) are preferred over single-node implementations.

## N. Monitoring & Telemetry
In real systems, monitor execution time and memory usage for large graphs.

## O. Clean Code & Design Principles
Use clear variable naming (e.g., `dist`, `nxt`). Keep cycle detection and path reconstruction modular if possible.

## P. Testing Strategies
Test with simple positive weight graphs, disconnected graphs, graphs with negative edges, and graphs with negative cycles.

## Q. Debugging Tactics
Print the matrix after each k-iteration for small graphs to verify updates.

## R. Code Review Checklist
Check the loop order (k, i, j). Ensure infinity is used correctly. Validate initialization logic.

## S. Algorithmic Trade-offs
O(V^3) limits use to small/dense graphs. Dijkstra V times is better for sparse graphs.

## T. Security & Failure Modes
Out-of-memory errors on large graphs. Unhandled infinity values in additions leading to overflow if not using float('inf').

## U. Asynchronous/Concurrency Patterns
Can be parallelized, but synchronization between iterations is required.

## V. Future Extensions
Optimizing with SIMD instructions for matrix operations.

## W. Maintenance & Refactoring
Keep the algorithm implementations isolated from business logic.

## X. Project Connection
Used in the core routing engine for mapping services to precompute paths between key landmarks.
"""

from typing import List, Tuple, Dict, Optional
import math

# Basic Implementation: Adjacency Matrix
def floyd_warshall_basic(graph: List[List[float]]) -> List[List[float]]:
    V = len(graph)
    dist = [[graph[i][j] for j in range(V)] for i in range(V)]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Intermediate Implementation: With Path Reconstruction
def floyd_warshall_path(graph: List[List[float]]) -> Tuple[List[List[float]], List[List[int]]]:
    V = len(graph)
    dist = [[graph[i][j] for j in range(V)] for i in range(V)]
    nxt = [[j if graph[i][j] != math.inf and i != j else -1 for j in range(V)] for i in range(V)]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt

def get_path(u: int, v: int, nxt: List[List[int]]) -> List[int]:
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path

# Advanced Implementation: Negative Cycle Detection
def floyd_warshall_advanced(graph: List[List[float]]) -> Tuple[List[List[float]], bool]:
    V = len(graph)
    dist = [[graph[i][j] for j in range(V)] for i in range(V)]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    # Check negative cycle
    has_neg_cycle = False
    for i in range(V):
        if dist[i][i] < 0:
            has_neg_cycle = True
            break
            
    return dist, has_neg_cycle

# Edge Cases:
# 1. Empty graph
# 2. Graph with single node
# 3. Disconnected graph components
# 4. Negative weight cycles

# Interview Challenge:
# Q: "How can you use Floyd-Warshall to find the transitive closure of a graph?"
# A: "Initialize dist with 1 if there's an edge, 0 otherwise. Use OR/AND logical operations instead of +/min: dist[i][j] = dist[i][j] or (dist[i][k] and dist[k][j])."

def test_floyd_warshall():
    INF = math.inf
    graph = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0]
    ]
    
    # Basic
    dist = floyd_warshall_basic(graph)
    assert dist[0][2] == 5
    assert dist[1][3] == 3
    
    # Advanced
    dist_adv, neg_cyc = floyd_warshall_advanced(graph)
    assert not neg_cyc
    
    graph_neg_cycle = [
        [0, 1, INF],
        [INF, 0, -1],
        [-1, INF, 0]
    ]
    _, neg_cyc_true = floyd_warshall_advanced(graph_neg_cycle)
    assert neg_cyc_true
    
    print("All tests passed for Floyd-Warshall.")

if __name__ == "__main__":
    test_floyd_warshall()
