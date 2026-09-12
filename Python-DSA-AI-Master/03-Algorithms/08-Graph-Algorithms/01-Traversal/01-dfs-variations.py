"""
Depth-First Search (DFS) Variations

Learning Objectives:
1. Understand the core concept of Depth-First Search in graphs.
2. Implement recursive and iterative DFS.
3. Apply DFS for cycle detection and topological sorting.

Concept Explanation:
Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking. It uses a stack (explicitly or via recursion) to keep track of the current path.

Performance Analysis:
- Time Complexity: O(V + E) where V is vertices and E is edges.
- Space Complexity: O(V) for the call stack or explicit stack and visited set.

Edge Cases:
- Disconnected graphs (need to iterate over all vertices).
- Cyclic graphs (must track visited nodes to avoid infinite loops).
"""

from typing import Dict, List, Set, Any
import unittest

# Basic: Recursive DFS
def dfs_recursive(graph: Dict[Any, List[Any]], start: Any, visited: Set[Any] = None) -> List[Any]:
    if visited is None:
        visited = set()
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
            
    return result

# Intermediate: Iterative DFS
def dfs_iterative(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            # Add reversed so left-most child is popped first for consistency with recursive
            stack.extend(reversed(graph.get(vertex, [])))
            
    return result

# Advanced: Topological Sort using DFS
def topological_sort(graph: Dict[Any, List[Any]]) -> List[Any]:
    visited = set()
    stack = []
    
    def dfs(vertex: Any):
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)
        
    for node in graph:
        if node not in visited:
            dfs(node)
            
    return stack[::-1]

class TestDFS(unittest.TestCase):
    def setUp(self):
        self.graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }
        
    def test_dfs_recursive(self):
        self.assertEqual(dfs_recursive(self.graph, 'A'), ['A', 'B', 'D', 'E', 'F', 'C'])
        
    def test_dfs_iterative(self):
        self.assertEqual(dfs_iterative(self.graph, 'A'), ['A', 'B', 'D', 'E', 'F', 'C'])
        
    def test_topological_sort(self):
        dag = {'A': ['C'], 'B': ['C', 'D'], 'C': ['E'], 'D': ['F'], 'E': [], 'F': []}
        result = topological_sort(dag)
        self.assertTrue(result.index('A') < result.index('C'))
        self.assertTrue(result.index('C') < result.index('E'))

if __name__ == '__main__':
    unittest.main()
