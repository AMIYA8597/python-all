"""
Breadth-First Search (BFS) Variations

Learning Objectives:
1. Understand the core concept of Breadth-First Search in graphs.
2. Implement BFS using a queue.
3. Apply BFS for shortest path in unweighted graphs.

Concept Explanation:
Breadth-First Search (BFS) explores the neighbor nodes first, before moving to the next level neighbors. It uses a queue to keep track of nodes to visit next.

Performance Analysis:
- Time Complexity: O(V + E)
- Space Complexity: O(V) for the queue and visited set.

Edge Cases:
- Disconnected graphs.
- Graphs with cycles.
"""

from typing import Dict, List, Set, Any
from collections import deque
import unittest

# Basic: Simple BFS Traversal
def bfs_basic(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    visited = set([start])
    queue = deque([start])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return result

# Intermediate: Shortest Path in Unweighted Graph
def bfs_shortest_path(graph: Dict[Any, List[Any]], start: Any, target: Any) -> List[Any]:
    if start == target:
        return [start]
        
    visited = set([start])
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        vertex = path[-1]
        
        for neighbor in graph.get(vertex, []):
            if neighbor == target:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
                
    return []

# Advanced: Multi-source BFS (e.g., rotten oranges problem)
def multi_source_bfs(graph: Dict[Any, List[Any]], sources: List[Any]) -> Dict[Any, int]:
    distances = {s: 0 for s in sources}
    queue = deque(sources)
    
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.get(vertex, []):
            if neighbor not in distances:
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
                
    return distances

class TestBFS(unittest.TestCase):
    def setUp(self):
        self.graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
        
    def test_bfs_basic(self):
        res = bfs_basic(self.graph, 'A')
        self.assertEqual(res[:3], ['A', 'B', 'C'])
        
    def test_bfs_shortest_path(self):
        self.assertEqual(bfs_shortest_path(self.graph, 'A', 'F'), ['A', 'C', 'F'])
        
if __name__ == '__main__':
    unittest.main()
