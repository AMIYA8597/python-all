"""
Dijkstra's Shortest Path Algorithm

Learning Objectives:
1. Understand shortest path finding in weighted graphs.
2. Implement Dijkstra using a priority queue.
3. Compare Dijkstra's greedy approach to other pathfinding algorithms.

Concept Explanation:
Dijkstra's algorithm finds the shortest path from a single source node to all other nodes in a graph with 
non-negative edge weights. It greedily selects the unvisited node with the smallest tentative distance, 
then explores its neighbors to update their tentative distances.

Performance Analysis:
- Time Complexity: O((V + E) log V) with a priority queue (min-heap).
- Space Complexity: O(V) for distances and queue.

Edge Cases:
- Disconnected graphs.
- Graphs with negative weights (Dijkstra may fail, Bellman-Ford should be used).
- Target node not reachable.

Interview Challenge:
"Find the shortest distance between two nodes in a network with non-negative delays."
"""

import heapq
from typing import Dict, List, Tuple
import unittest

def dijkstra_basic(graph: Dict[str, Dict[str, int]], start: str) -> Dict[str, int]:
    """Basic implementation returning shortest distances from start."""
    distances = {node: float('inf') for node in graph}
    if start not in graph:
        return {}
    distances[start] = 0
    
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances

def dijkstra_intermediate(graph: Dict[str, List[Tuple[str, int]]], start: str, end: str) -> Tuple[int, List[str]]:
    """Intermediate implementation returning distance and the path to a specific target."""
    if start not in graph:
        return float('inf'), []
        
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        if current_node == end:
            break
            
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    if distances.get(end, float('inf')) == float('inf'):
        return float('inf'), []
        
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path.reverse()
    
    return distances[end], path

class Graph:
    def __init__(self):
        self.adj = {}
        
    def add_edge(self, u: str, v: str, w: int):
        if u not in self.adj: self.adj[u] = {}
        if v not in self.adj: self.adj[v] = {}
        self.adj[u][v] = w
        self.adj[v][u] = w # Assuming undirected for advanced example

def dijkstra_advanced(g: Graph, start: str) -> Dict[str, int]:
    """Advanced implementation using a custom Graph class."""
    return dijkstra_basic(g.adj, start)

class TestDijkstra(unittest.TestCase):
    def test_basic(self):
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }
        distances = dijkstra_basic(graph, 'A')
        self.assertEqual(distances['D'], 4)
        
    def test_intermediate(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }
        dist, path = dijkstra_intermediate(graph, 'A', 'D')
        self.assertEqual(dist, 4)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])

if __name__ == "__main__":
    unittest.main()
