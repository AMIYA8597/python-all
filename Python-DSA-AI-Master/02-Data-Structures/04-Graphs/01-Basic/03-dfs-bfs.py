"""
## A. Concept Name
Graph Traversal: Depth First Search (DFS) and Breadth First Search (BFS)

## B. Learning Objectives
1. Understand the core concepts behind DFS (stack/recursion) and BFS (queue).
2. Implement DFS using both recursive and iterative approaches.
3. Implement BFS and use it to find the shortest path in unweighted graphs.
4. Analyze the time and space complexity of graph traversals.

## C. Concept Explanation
- DFS explores as far as possible along each branch before backtracking. Useful for topological sorting, cycle detection.
- BFS explores all neighbor nodes at the present depth prior to moving on to nodes at the next depth level. Useful for finding shortest paths.

## D. Performance Analysis
- Time Complexity: O(V + E) for both DFS and BFS (using Adjacency List).
- Space Complexity: O(V) for the visited set, plus O(V) for call stack (DFS) or queue (BFS) in the worst case.

## E. Edge Cases
- Disconnected graphs: If the graph is disconnected, starting from one node won't visit all nodes. Must loop over all vertices.
- Cycles: Must keep track of 'visited' nodes to prevent infinite loops.

## F. Interview Challenge
"Given a 2D grid of 0s and 1s, use DFS or BFS to find the number of islands (connected components of 1s)."

## X. Project Connection
Understanding graph traversals is fundamental for various applications such as web crawlers, solving mazes, social network analysis, and AI search algorithms.
"""

from typing import Dict, List, Set, Any
from collections import deque

class GraphTraversal:
    def __init__(self):
        self.graph: Dict[Any, List[Any]] = {}
        
    def add_edge(self, u: Any, v: Any) -> None:
        if u not in self.graph: self.graph[u] = []
        if v not in self.graph: self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    # --- BASIC: Recursive DFS ---
    def dfs_recursive(self, start: Any, visited: Set[Any] = None) -> List[Any]:
        if visited is None:
            visited = set()
        visited.add(start)
        result = [start]
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                result.extend(self.dfs_recursive(neighbor, visited))
        return result

    # --- INTERMEDIATE: Iterative DFS & BFS ---
    def dfs_iterative(self, start: Any) -> List[Any]:
        visited = set()
        stack = [start]
        result = []
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                # Reverse to maintain similar order to recursive DFS
                stack.extend(reversed(self.graph.get(vertex, [])))
        return result

    def bfs(self, start: Any) -> List[Any]:
        visited = set([start])
        queue = deque([start])
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            for neighbor in self.graph.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    # --- ADVANCED: Shortest Path using BFS ---
    def bfs_shortest_path(self, start: Any, target: Any) -> List[Any]:
        """Finds the shortest path between start and target in an unweighted graph."""
        if start == target:
            return [start]
            
        visited = set([start])
        queue = deque([[start]]) # Queue of paths
        
        while queue:
            path = queue.popleft()
            vertex = path[-1]
            
            for neighbor in self.graph.get(vertex, []):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return []

def setup_test_graph() -> GraphTraversal:
    g = GraphTraversal()
    # Graph: A-B, A-C, B-D, B-E, C-F
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
    for u, v in edges:
        g.add_edge(u, v)
    return g

def test_traversals():
    g = setup_test_graph()
    
    dfs_rec = g.dfs_recursive('A')
    assert len(dfs_rec) == 6
    assert set(dfs_rec) == {'A', 'B', 'C', 'D', 'E', 'F'}
    
    dfs_iter = g.dfs_iterative('A')
    assert len(dfs_iter) == 6
    assert set(dfs_iter) == {'A', 'B', 'C', 'D', 'E', 'F'}
    
    bfs_res = g.bfs('A')
    assert bfs_res[0] == 'A'
    assert set(bfs_res[1:3]) == {'B', 'C'} # Next level
    
    path = g.bfs_shortest_path('A', 'E')
    assert path == ['A', 'B', 'E']
    print("Traversal tests passed.")

if __name__ == "__main__":
    print("Running DFS/BFS tests...")
    test_traversals()
    print("All tests passed!")
