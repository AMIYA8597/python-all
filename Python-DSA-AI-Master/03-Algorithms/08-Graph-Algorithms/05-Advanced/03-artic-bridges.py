"""
Articulation Points and Bridges

Learning Objectives:
1. Understand what articulation points (cut vertices) and bridges (cut edges) are.
2. Learn how removing these affects graph connectivity.
3. Master the DFS-based discovery and low-link approach to identify them in O(V+E) time.

Concept Explanation:
- Articulation Point: A vertex whose removal increases the number of connected components.
- Bridge: An edge whose removal increases the number of connected components.
Both are critical in network design for identifying single points of failure.
We use DFS:
- `disc[u]`: Discovery time of `u`.
- `low[u]`: Lowest discovery time reachable from `u` without going through the parent.
Condition for Articulation Point `u`:
- `u` is root of DFS tree and has >= 2 children.
- `u` is not root, and for some child `v`, `low[v] >= disc[u]`.
Condition for Bridge `u-v`:
- For child `v`, `low[v] > disc[u]`.

Imports:
"""
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import unittest

class ArticBridgesGraph:
    """Basic/Intermediate Implementation of Articulation Points and Bridges"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)
        self.time = 0

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def _dfs(self, u: int, visited: List[bool], parent: List[int], low: List[int], disc: List[int], 
             ap: List[bool], bridges: List[Tuple[int, int]]) -> None:
        children = 0
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                self._dfs(v, visited, parent, low, disc, ap, bridges)

                low[u] = min(low[u], low[v])

                # Bridge condition
                if low[v] > disc[u]:
                    bridges.append((u, v))

                # Articulation Point conditions
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True

            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def find_ap_and_bridges(self) -> Tuple[List[int], List[Tuple[int, int]]]:
        """
        Performance Analysis:
        - Time Complexity: O(V + E) for undirected graphs using one DFS.
        - Space Complexity: O(V) for arrays and recursion stack.
        """
        visited = [False] * self.V
        disc = [float("Inf")] * self.V
        low = [float("Inf")] * self.V
        parent = [-1] * self.V
        ap = [False] * self.V
        bridges: List[Tuple[int, int]] = []

        for i in range(self.V):
            if not visited[i]:
                self._dfs(i, visited, parent, low, disc, ap, bridges)

        ap_list = [i for i, is_ap in enumerate(ap) if is_ap]
        return ap_list, bridges

"""
Edge Cases:
1. Graph with multiple disconnected components.
2. Cycles vs Trees: Bridges are edges not in any cycle.
"""

class TestArticBridges(unittest.TestCase):
    def test_ap_bridges(self):
        g = ArticBridgesGraph(5)
        g.add_edge(1, 0)
        g.add_edge(0, 2)
        g.add_edge(2, 1)
        g.add_edge(0, 3)
        g.add_edge(3, 4)
        aps, bridges = g.find_ap_and_bridges()
        self.assertIn(0, aps)
        self.assertIn(3, aps)
        
        # normalize bridges for comparison
        norm_bridges = set(tuple(sorted(b)) for b in bridges)
        self.assertIn((0, 3), norm_bridges)
        self.assertIn((3, 4), norm_bridges)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
