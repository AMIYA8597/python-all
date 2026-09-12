"""
Tarjan's Strongly Connected Components (SCC) Algorithm

Learning Objectives:
1. Understand the concept of Strongly Connected Components in directed graphs.
2. Grasp the use of DFS to determine reachability and structure.
3. Master the calculation of discovery times and low-link values.
4. Learn how a stack helps track current component members.

Concept Explanation:
A Strongly Connected Component (SCC) is a maximal subset of vertices in a directed graph where every vertex is reachable from every other vertex in the subset.
Tarjan's algorithm uses a single Depth First Search (DFS) pass to find all SCCs. It maintains:
- `disc`: The discovery time of a node.
- `low`: The lowest discovery time reachable from the node.
- A stack to keep track of nodes currently being explored that haven't been assigned to an SCC.
When a node finishes exploring and its `low` equals its `disc`, it is the root of an SCC.

Imports:
"""
from typing import List, Dict
from collections import defaultdict
import sys
import unittest

sys.setrecursionlimit(2000)

class TarjanGraph:
    """Basic Implementation of Tarjan's SCC Algorithm"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.time = 0

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)

    def _scc_util(self, u: int, low: List[int], disc: List[int], 
                  stack_member: List[bool], st: List[int], result: List[List[int]]) -> None:
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        stack_member[u] = True
        st.append(u)

        for v in self.graph[u]:
            if disc[v] == -1:
                self._scc_util(v, low, disc, stack_member, st, result)
                low[u] = min(low[u], low[v])
            elif stack_member[v]:
                low[u] = min(low[u], disc[v])

        if low[u] == disc[u]:
            component = []
            w = -1
            while w != u:
                w = st.pop()
                component.append(w)
                stack_member[w] = False
            result.append(component)

    def get_sccs(self) -> List[List[int]]:
        """
        Performance Analysis:
        - Time Complexity: O(V + E) where V is vertices, E is edges. Each node and edge is processed once.
        - Space Complexity: O(V) for the recursive call stack, low, disc, and st arrays.
        """
        disc = [-1] * self.V
        low = [-1] * self.V
        stack_member = [False] * self.V
        st: List[int] = []
        result: List[List[int]] = []

        for i in range(self.V):
            if disc[i] == -1:
                self._scc_util(i, low, disc, stack_member, st, result)
                
        return result

"""
Edge Cases Handled:
1. Disconnected graphs: The outer loop ensures all vertices are checked.
2. Single node: Handled correctly as its own SCC.
3. Trees/DAGs: Handled correctly (every node is its own SCC).

Interview Challenge:
Problem: Given a directed graph representing a network of computers, find the minimum number of computers that need to receive a software update directly from the server so that every computer eventually receives it (via directed connections).
Hint: Find SCCs, contract them into a DAG, and count nodes in the DAG with in-degree 0.
"""

class TestTarjanSCC(unittest.TestCase):
    def test_basic_scc(self):
        g = TarjanGraph(5)
        g.add_edge(1, 0)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(0, 3)
        g.add_edge(3, 4)
        sccs = g.get_sccs()
        # [4], [3], [0,1,2] -> Note: order within SCC might vary
        self.assertEqual(len(sccs), 3)
        sizes = sorted([len(c) for c in sccs])
        self.assertEqual(sizes, [1, 1, 3])

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
