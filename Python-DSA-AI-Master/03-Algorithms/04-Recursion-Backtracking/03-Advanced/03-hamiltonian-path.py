"""
Hamiltonian Path and Cycle

Learning Objectives:
1. Differentiate between Hamiltonian Path and Hamiltonian Cycle.
2. Apply backtracking to find a path visiting every vertex exactly once.
3. Understand the NP-Complete nature of the problem.

Concept Explanation:
A Hamiltonian path in an undirected graph is a path that visits every vertex exactly once.
A Hamiltonian cycle is a Hamiltonian path that is a cycle (an edge exists between the last and first vertex).

Performance Analysis:
- Time Complexity: O(N!) where N is the number of vertices.
- Space Complexity: O(N) for recursion stack.
"""

from typing import List, Optional

class HamiltonianCycle:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def is_safe(self, v: int, pos: int, path: List[int]) -> bool:
        """Check if vertex v can be added to the path."""
        if self.graph[path[pos - 1]][v] == 0:
            return False
        if v in path:
            return False
        return True

    def ham_cycle_util(self, path: List[int], pos: int) -> bool:
        """Recursive utility to find a Hamiltonian Cycle."""
        if pos == self.V:
            # Check if there is an edge from last to first
            return self.graph[path[pos - 1]][path[0]] == 1

        for v in range(1, self.V):
            if self.is_safe(v, pos, path):
                path[pos] = v
                if self.ham_cycle_util(path, pos + 1):
                    return True
                path[pos] = -1
        return False

    def solve(self) -> Optional[List[int]]:
        """Basic Implementation: Solve Hamiltonian Cycle problem."""
        path = [-1] * self.V
        path[0] = 0 # Start at vertex 0

        if not self.ham_cycle_util(path, 1):
            return None
        return path

def run_tests():
    print("Testing Hamiltonian Path/Cycle...")
    hc = HamiltonianCycle(5)
    hc.graph = [
        [0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ]
    result = hc.solve()
    assert result is not None
    print("Hamiltonian Cycle test passed! Path:", result)

if __name__ == "__main__":
    run_tests()
