"""
Biconnected Components

Learning Objectives:
1. Understand biconnectivity in undirected graphs.
2. Relate biconnected components to articulation points.
3. Learn how to extract edges belonging to the same biconnected component.

Concept Explanation:
A biconnected graph is a connected graph that cannot be broken into disconnected pieces by deleting any single vertex (and its incident edges).
A Biconnected Component (BCC) is a maximal biconnected subgraph.
We use Tarjan's discovery time and low-link approach, pushing edges onto a stack. When an articulation point is found (or root is done), we pop edges to form a BCC.

Imports:
"""
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import unittest

class BiconnectedGraph:
    """Intermediate Implementation of Biconnected Components"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.time = 0

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def _bcc_util(self, u: int, parent: int, low: List[int], disc: List[int], 
                  st: List[Tuple[int, int]], result: List[List[Tuple[int, int]]]) -> None:
        children = 0
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if disc[v] == -1:
                children += 1
                st.append((u, v))
                self._bcc_util(v, u, low, disc, st, result)
                low[u] = min(low[u], low[v])

                if (parent == -1 and children > 1) or (parent != -1 and low[v] >= disc[u]):
                    comp = []
                    while st:
                        edge = st.pop()
                        comp.append(edge)
                        if edge == (u, v) or edge == (v, u):
                            break
                    if comp:
                        result.append(comp)

            elif v != parent and disc[v] < disc[u]:
                st.append((u, v))
                low[u] = min(low[u], disc[v])

    def get_bccs(self) -> List[List[Tuple[int, int]]]:
        """
        Performance Analysis:
        - Time Complexity: O(V + E)
        - Space Complexity: O(E) for stack storing edges, O(V) for recursion and tracking.
        """
        disc = [-1] * self.V
        low = [-1] * self.V
        st: List[Tuple[int, int]] = []
        result: List[List[Tuple[int, int]]] = []

        for i in range(self.V):
            if disc[i] == -1:
                self._bcc_util(i, -1, low, disc, st, result)
                comp = []
                while st:
                    comp.append(st.pop())
                if comp:
                    result.append(comp)

        return result

"""
Edge Cases:
1. Graphs with multiple connected components.
2. A graph with only 2 vertices connected by an edge.
"""

class TestBiconnected(unittest.TestCase):
    def test_bcc(self):
        g = BiconnectedGraph(5)
        g.add_edge(1, 0)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(0, 3)
        g.add_edge(3, 4)
        bccs = g.get_bccs()
        self.assertEqual(len(bccs), 3)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
