"""
Hamiltonian Path and Circuit

Learning Objectives:
1. Understand Hamiltonian Paths (visits every vertex exactly once) and Circuits.
2. Grasp why Hamiltonian problems are NP-Complete.
3. Implement Backtracking to solve Hamiltonian Cycle problem for small graphs.

Concept Explanation:
Unlike Eulerian paths which traverse all edges, Hamiltonian paths traverse all vertices. There are no easy sufficient and necessary conditions (like degree counts) to determine existence in polynomial time for general graphs. We use backtracking.

Imports:
"""
from typing import List
import unittest

class HamiltonianGraph:
    """Implementation of Hamiltonian Cycle using Backtracking"""
    def __init__(self, vertices: int):
        self.V = vertices
        # Adjacency matrix for easier edge checking
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def is_safe(self, v: int, pos: int, path: List[int]) -> bool:
        # Check if current vertex and last vertex in path are adjacent
        if self.graph[path[pos-1]][v] == 0:
            return False
        # Check if vertex is already in path
        if v in path:
            return False
        return True

    def _ham_cycle_util(self, path: List[int], pos: int) -> bool:
        # Base case: all vertices are in the path
        if pos == self.V:
            # Check if there is an edge from the last included vertex to the first
            if self.graph[path[pos-1]][path[0]] == 1:
                return True
            else:
                return False

        for v in range(1, self.V):
            if self.is_safe(v, pos, path):
                path[pos] = v
                if self._ham_cycle_util(path, pos + 1):
                    return True
                path[pos] = -1

        return False

    def get_hamiltonian_cycle(self) -> List[int]:
        """
        Performance Analysis:
        - Time Complexity: O(N!) in worst case where N is vertices. NP-Complete.
        - Space Complexity: O(N) for recursion stack and path array.
        """
        path = [-1] * self.V
        # Start at vertex 0
        path[0] = 0

        if not self._ham_cycle_util(path, 1):
            return []
        
        # Include closing edge back to start for the circuit
        return path + [path[0]]

class TestHamiltonian(unittest.TestCase):
    def test_cycle_exists(self):
        g1 = HamiltonianGraph(5)
        g1.graph = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 1, 0]
        ]
        cycle = g1.get_hamiltonian_cycle()
        self.assertTrue(len(cycle) > 0)

    def test_no_cycle(self):
        g2 = HamiltonianGraph(5)
        g2.graph = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0], # Disconnect
            [0, 1, 1, 0, 0]
        ]
        cycle = g2.get_hamiltonian_cycle()
        self.assertEqual(len(cycle), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
