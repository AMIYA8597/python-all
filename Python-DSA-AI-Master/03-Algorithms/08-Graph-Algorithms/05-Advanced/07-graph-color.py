"""
Graph Coloring

Learning Objectives:
1. Understand graph coloring and the chromatic number.
2. Implement a greedy graph coloring algorithm.
3. Understand backtracking for m-coloring problem.

Concept Explanation:
Graph coloring assigns colors to vertices such that no two adjacent vertices share a color. 
Finding the minimum number of colors (chromatic number) is NP-Complete. 
However, Greedy Coloring provides an upper bound and is fast (O(V+E)). 
Alternatively, Backtracking determines if the graph can be colored with at most `m` colors.

Imports:
"""
from typing import List, Dict
from collections import defaultdict
import unittest

class GraphColoring:
    """Greedy and Backtracking Implementations for Graph Coloring"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: Dict[int, List[int]] = defaultdict(list)

    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def greedy_coloring(self) -> List[int]:
        """
        Greedy Algorithm
        Performance: O(V + E) time, O(V) space.
        Note: Doesn't guarantee minimum colors (chromatic number), but fast.
        """
        result = [-1] * self.V
        result[0] = 0

        available = [True] * self.V

        for u in range(1, self.V):
            for i in self.graph[u]:
                if result[i] != -1:
                    available[result[i]] = False

            cr = 0
            while cr < self.V:
                if available[cr]:
                    break
                cr += 1
                
            result[u] = cr

            for i in self.graph[u]:
                if result[i] != -1:
                    available[result[i]] = True

        return result

    def _is_safe(self, v: int, color: List[int], c: int) -> bool:
        for i in self.graph[v]:
            if color[i] == c:
                return False
        return True

    def _graph_color_util(self, m: int, color: List[int], v: int) -> bool:
        if v == self.V:
            return True

        for c in range(1, m + 1):
            if self._is_safe(v, color, c):
                color[v] = c
                if self._graph_color_util(m, color, v + 1):
                    return True
                color[v] = 0

        return False

    def can_color(self, m: int) -> bool:
        """
        Backtracking to check if m colors are sufficient.
        Performance: O(m^V) time in worst case, O(V) space.
        """
        color = [0] * self.V
        return self._graph_color_util(m, color, 0)

class TestGraphColoring(unittest.TestCase):
    def test_greedy(self):
        g = GraphColoring(5)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        colors = g.greedy_coloring()
        self.assertEqual(len(colors), 5)
        self.assertNotEqual(colors[0], colors[1])
        
    def test_can_color(self):
        g = GraphColoring(4)
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(0, 3)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        # Complete graph K4 requires 4 colors, here it's short 1 edge so 3 is enough
        self.assertTrue(g.can_color(3))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
