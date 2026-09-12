"""
Kosaraju's Strongly Connected Components Algorithm

Learning Objectives:
1. Understand the mathematical properties of graph transposition (reversing edges).
2. Learn the two-pass DFS approach to finding SCCs.
3. Compare Kosaraju's algorithm with Tarjan's in terms of simplicity and practical performance.

Concept Explanation:
Kosaraju's algorithm finds SCCs by executing two DFS passes:
1. Pass 1: Perform DFS on the original graph to compute the finishing times of each node. We push nodes to a stack as they finish.
2. Pass 2: Reverse all edges of the graph. Pop nodes from the stack; for each unvisited node, perform DFS on the reversed graph. All nodes reachable in this pass form an SCC.

Imports:
"""
from typing import List, Dict, Set
from collections import defaultdict
import unittest

class KosarajuGraph:
    """Basic/Intermediate Implementation of Kosaraju's Algorithm"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)

    def _fill_order(self, v: int, visited: List[bool], stack: List[int]) -> None:
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self._fill_order(i, visited, stack)
        stack.append(v)

    def _get_transpose(self) -> 'KosarajuGraph':
        g = KosarajuGraph(self.V)
        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    def _dfs_util(self, v: int, visited: List[bool], component: List[int]) -> None:
        visited[v] = True
        component.append(v)
        for i in self.graph[v]:
            if not visited[i]:
                self._dfs_util(i, visited, component)

    def get_sccs(self) -> List[List[int]]:
        """
        Performance Analysis:
        - Time Complexity: O(V + E) for two DFS passes and graph transposition.
        - Space Complexity: O(V + E) for storing the transposed graph and recursion stack.
        Kosaraju's generally requires more space and more passes than Tarjan's, but is easier to implement.
        """
        stack: List[int] = []
        visited = [False] * self.V

        # Pass 1
        for i in range(self.V):
            if not visited[i]:
                self._fill_order(i, visited, stack)

        # Transpose
        gr = self._get_transpose()

        # Pass 2
        visited = [False] * self.V
        result: List[List[int]] = []
        
        while stack:
            i = stack.pop()
            if not visited[i]:
                comp: List[int] = []
                gr._dfs_util(i, visited, comp)
                result.append(comp)

        return result

"""
Edge Cases:
1. Cyclic graphs with disconnected components.
2. Acyclic graphs (DAGs), where every vertex is its own SCC.

Interview Challenge:
Problem: Given a list of user transactions where a follows b, determine the isolated groups of users who only transact with each other.
"""

class TestKosaraju(unittest.TestCase):
    def test_kosaraju(self):
        g = KosarajuGraph(5)
        g.add_edge(1, 0)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(0, 3)
        g.add_edge(3, 4)
        sccs = g.get_sccs()
        self.assertEqual(len(sccs), 3)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
