"""
Bellman-Ford Algorithm

Learning Objectives:
1. Understand Bellman-Ford for Single-Source Shortest Path.
2. Detect negative weight cycles.

Concept Explanation:
Computes shortest paths from a single source node to all other nodes in a weighted digraph. Slower than Dijkstra's but can handle negative weights and detect negative weight cycles.

Performance Analysis:
- Time Complexity: O(V * E)
- Space Complexity: O(V)

Edge Cases:
- Graph with negative weight cycles.
"""

from typing import Dict, List, Tuple, Any
import unittest

def bellman_ford(vertices: List[Any], edges: List[Tuple[Any, Any, float]], start: Any) -> Tuple[Dict[Any, float], bool]:
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                
    # Detect negative cycle
    has_negative_cycle = False
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            has_negative_cycle = True
            break
            
    return distances, has_negative_cycle

class TestBellmanFord(unittest.TestCase):
    def test_bellman_ford(self):
        vertices = ['A', 'B', 'C', 'D', 'E']
        edges = [
            ('A', 'B', -1), ('A', 'C', 4),
            ('B', 'C', 3), ('B', 'D', 2), ('B', 'E', 2),
            ('D', 'B', 1), ('D', 'C', 5),
            ('E', 'D', -3)
        ]
        dist, has_cycle = bellman_ford(vertices, edges, 'A')
        self.assertFalse(has_cycle)
        self.assertEqual(dist['E'], 1)
        
    def test_negative_cycle(self):
        vertices = ['A', 'B', 'C']
        edges = [('A', 'B', 1), ('B', 'C', -1), ('C', 'A', -1)]
        dist, has_cycle = bellman_ford(vertices, edges, 'A')
        self.assertTrue(has_cycle)

if __name__ == '__main__':
    unittest.main()
