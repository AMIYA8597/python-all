"""
Planar Graph Checks (Basic)

Learning Objectives:
1. Understand the definition of Planar Graphs (can be drawn on a plane without edge crossings).
2. Learn Euler's formula: V - E + F = 2.
3. Understand Kuratowski's Theorem and subgraphs K5 and K3,3.

Concept Explanation:
A strict linear-time planarity test (like Hopcroft-Tarjan) is highly complex. 
For educational purposes, we implement necessary condition checks using Euler's formula consequences:
For a connected planar graph with V >= 3:
1. E <= 3V - 6
2. If triangle-free, E <= 2V - 4

Imports:
"""
from typing import List, Dict, Set
from collections import defaultdict
import unittest

class PlanarChecker:
    """Basic structural checks for planarity"""
    def __init__(self, vertices: int):
        self.V = vertices
        self.edges = 0
        self.graph: Dict[int, Set[int]] = defaultdict(set)

    def add_edge(self, u: int, v: int) -> None:
        if v not in self.graph[u]:
            self.graph[u].add(v)
            self.graph[v].add(u)
            self.edges += 1

    def has_triangles(self) -> bool:
        # Check for any 3-cycle
        for u in range(self.V):
            for v in self.graph[u]:
                for w in self.graph[v]:
                    if w != u and w in self.graph[u]:
                        return True
        return False

    def is_planar_possible(self) -> bool:
        """
        Uses Euler's formula deductions.
        Note: This is a NECESSARY but not SUFFICIENT condition. 
        True means it MIGHT be planar. False means it is definitely NOT planar.
        """
        if self.V < 3:
            return True
            
        if self.edges > 3 * self.V - 6:
            return False
            
        if not self.has_triangles():
            if self.edges > 2 * self.V - 4:
                return False
                
        return True

"""
Edge Cases:
Small graphs (V < 3) are always planar.
Disconnected graphs need to be evaluated per component (assumed connected here).

Interview Challenge:
Why is K5 not planar? 
V=5, E=10. 3V-6 = 15-6 = 9. Since E > 9, K5 violates the necessary condition and is not planar.
"""

class TestPlanarity(unittest.TestCase):
    def test_k5(self):
        # K5 is non-planar
        g = PlanarChecker(5)
        for i in range(5):
            for j in range(i+1, 5):
                g.add_edge(i, j)
        self.assertFalse(g.is_planar_possible())
        
    def test_planar_graph(self):
        g = PlanarChecker(4)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 0)
        self.assertTrue(g.is_planar_possible())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
