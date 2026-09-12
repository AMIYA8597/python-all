"""
## A. Concept Name
Maximum Flow (Ford-Fulkerson / Edmonds-Karp) - Advanced Graph Data Structures

## B. Learning Objectives
1. Understand Network Flow and the Max-Flow Min-Cut theorem.
2. Implement Ford-Fulkerson using DFS.
3. Implement Edmonds-Karp using BFS for better time complexity.
4. Model real-world problems as maximum flow (e.g., bipartite matching).

## C. Concept Explanation
Maximum Flow algorithms find the maximum possible flow from a source node to a sink node in a flow network.
Each edge has a capacity. Flow conservation holds for all nodes except source and sink.
Ford-Fulkerson uses augmenting paths. Edmonds-Karp is an implementation of Ford-Fulkerson that uses BFS to find the shortest augmenting path.

## D. Performance Analysis
- Time Complexity (Edmonds-Karp): O(V * E^2).
- Space Complexity: O(V^2) or O(V + E) depending on graph representation.

## E. Edge Cases
1. Source and sink are the same.
2. No path exists between source and sink.
3. Disconnected graph.
4. Infinite capacities (if modeled).

## F. Interview Challenge
Q: "How do you find the Min-Cut using the residual graph after finding Max Flow?"
A: "Perform a BFS/DFS from the source on the residual graph. All reachable nodes are in the source set (S), unreachable nodes are in the sink set (T). Edges crossing from S to T in the original graph form the Min-Cut."

## X. Project Connection
Understanding Max Flow is critical for AI Resource Allocator tasks where we map compute nodes to workload tasks to maximize network throughput and handle bottleneck identification.
"""

from typing import List, Dict, Tuple
from collections import deque

# Basic Implementation: DFS for augmenting path (Ford-Fulkerson)
def dfs(graph: List[List[int]], u: int, sink: int, flow: int, visited: List[bool]) -> int:
    if u == sink: return flow
    visited[u] = True
    for v in range(len(graph)):
        if not visited[v] and graph[u][v] > 0:
            pushed = dfs(graph, v, sink, min(flow, graph[u][v]), visited)
            if pushed > 0:
                graph[u][v] -= pushed
                graph[v][u] += pushed
                return pushed
    return 0

def ford_fulkerson(graph: List[List[int]], source: int, sink: int) -> int:
    # Creating residual graph
    V = len(graph)
    res_graph = [row[:] for row in graph]
    max_flow = 0
    
    while True:
        visited = [False] * V
        pushed = dfs(res_graph, source, sink, float('inf'), visited)
        if pushed == 0:
            break
        max_flow += pushed
    return max_flow

# Intermediate/Advanced Implementation: Edmonds-Karp (BFS)
def bfs(res_graph: List[List[int]], source: int, sink: int, parent: List[int]) -> bool:
    V = len(res_graph)
    visited = [False] * V
    queue = deque([source])
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        for v in range(V):
            if not visited[v] and res_graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    return False

def edmonds_karp(graph: List[List[int]], source: int, sink: int) -> int:
    V = len(graph)
    res_graph = [row[:] for row in graph]
    parent = [-1] * V
    max_flow = 0
    
    while bfs(res_graph, source, sink, parent):
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, res_graph[parent[s]][s])
            s = parent[s]
            
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            res_graph[u][v] -= path_flow
            res_graph[v][u] += path_flow
            v = u
            
    return max_flow

def test_max_flow():
    graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    assert ford_fulkerson(graph, 0, 5) == 23
    assert edmonds_karp(graph, 0, 5) == 23
    print("All tests passed for Max Flow algorithms.")

if __name__ == "__main__":
    test_max_flow()
