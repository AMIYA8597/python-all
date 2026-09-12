"""
Eulerian Path and Circuit

Learning Objectives:
1. Understand Eulerian Paths (visits every edge exactly once) and Circuits (path that starts and ends on same vertex).
2. Learn the conditions for existence of Eulerian Paths/Circuits in undirected and directed graphs.
3. Master Hierholzer's Algorithm to reconstruct the path/circuit.

Concept Explanation:
- An undirected connected graph has an Eulerian cycle if every vertex has an even degree.
- It has an Eulerian path if zero or exactly two vertices have an odd degree.
Hierholzer's Algorithm builds the circuit in O(E) time by maintaining a current path and recursively merging sub-tours.

Imports:
"""
from typing import List, Dict, Optional
from collections import defaultdict
import unittest

class EulerianGraph:
    """Implementation of Hierholzer's Algorithm for Undirected Eulerian Path/Circuit"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def _is_connected(self) -> bool:
        visited = [False] * self.V
        node = -1
        for i in range(self.V):
            if len(self.graph[i]) > 0:
                node = i
                break
        if node == -1:
            return True
        
        self._dfs(node, visited)
        
        for i in range(self.V):
            if visited[i] == False and len(self.graph[i]) > 0:
                return False
        return True

    def _dfs(self, v: int, visited: List[bool]) -> None:
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self._dfs(i, visited)

    def check_eulerian(self) -> int:
        """Returns 0 if not Eulerian, 1 if has an Euler path, 2 if has an Euler cycle"""
        if not self._is_connected():
            return 0
        odd = sum(1 for i in range(self.V) if len(self.graph[i]) % 2 != 0)
        
        if odd == 0:
            return 2
        elif odd == 2:
            return 1
        return 0

    def get_euler_path(self) -> Optional[List[int]]:
        """
        Hierholzer's algorithm to find the path.
        Performance: O(V + E) time, O(V + E) space.
        """
        euler_type = self.check_eulerian()
        if euler_type == 0:
            return None
        
        adj = {u: list(v) for u, v in self.graph.items()}
        
        # Start node
        curr_v = 0
        if euler_type == 1:
            for i in range(self.V):
                if len(self.graph[i]) % 2 != 0:
                    curr_v = i
                    break

        curr_path = [curr_v]
        circuit = []

        while curr_path:
            curr_v = curr_path[-1]
            if adj[curr_v]:
                next_v = adj[curr_v].pop()
                adj[next_v].remove(curr_v) # Since undirected
                curr_path.append(next_v)
            else:
                circuit.append(curr_path.pop())
                
        return circuit[::-1]

class TestEulerian(unittest.TestCase):
    def test_eulerian(self):
        g = EulerianGraph(5)
        g.add_edge(1, 0)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(0, 3)
        g.add_edge(3, 4)
        # Not Eulerian, degrees are 0:3, 1:2, 2:2, 3:2, 4:1 => 2 odds
        self.assertEqual(g.check_eulerian(), 1)
        path = g.get_euler_path()
        self.assertIsNotNone(path)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
