"""
Johnson's Algorithm

Learning Objectives:
1. Understand Johnson's Algorithm for All-Pairs Shortest Path (APSP).
2. Learn how it combines Bellman-Ford and Dijkstra's.

Concept Explanation:
Johnson's algorithm finds shortest paths between all pairs of vertices in a sparse, edge-weighted, directed graph. It handles negative weights by first using Bellman-Ford to reweight edges to be non-negative, and then applies Dijkstra's algorithm from each vertex.

Performance Analysis:
- Time Complexity: O(V^2 log V + VE)
- Space Complexity: O(V^2)

Edge Cases:
- Graphs with negative weight cycles (detected during Bellman-Ford step).
"""

import heapq
from typing import Dict, List, Tuple, Any
import unittest

def bellman_ford_johnson(vertices: List[Any], edges: List[Tuple[Any, Any, float]], start: Any) -> Dict[Any, float]:
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0
    
    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative weight cycle")
            
    return distances

def dijkstra_johnson(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> Dict[Any, float]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances

def johnson(vertices: List[Any], edges: List[Tuple[Any, Any, float]]) -> Dict[Any, Dict[Any, float]]:
    # Step 1: Add new node 'S' and zero-weight edges to all other nodes
    s_edges = edges + [('S', v, 0) for v in vertices]
    s_vertices = vertices + ['S']
    
    # Step 2: Run Bellman-Ford from 'S' to get vertex weights (h)
    h = bellman_ford_johnson(s_vertices, s_edges, 'S')
    
    # Step 3: Reweight original edges
    reweighted_edges = [(u, v, w + h[u] - h[v]) for u, v, w in edges]
    
    # Build reweighted graph representation
    adj = {v: [] for v in vertices}
    for u, v, w in reweighted_edges:
        adj[u].append((v, w))
        
    # Step 4: Run Dijkstra from each vertex
    all_pairs_shortest_paths = {}
    for u in vertices:
        d_dist = dijkstra_johnson(adj, u)
        # Revert weights back to original scale
        all_pairs_shortest_paths[u] = {v: d_dist[v] + h[v] - h[u] if d_dist[v] != float('inf') else float('inf') for v in vertices}
        
    return all_pairs_shortest_paths

class TestJohnson(unittest.TestCase):
    def test_johnson(self):
        vertices = ['A', 'B', 'C', 'D']
        edges = [
            ('A', 'B', -2),
            ('B', 'C', -1),
            ('A', 'C', 4),
            ('C', 'A', 2),
            ('C', 'D', 2),
            ('B', 'D', 1)
        ]
        dist = johnson(vertices, edges)
        self.assertEqual(dist['A']['C'], -3)
        self.assertEqual(dist['A']['D'], -1)

if __name__ == '__main__':
    unittest.main()
