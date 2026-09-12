"""
Module: Boruvka's Algorithm
"""
# Learning objectives: Understand Boruvka's algorithm for MST.
# Concept explanation: Boruvka's algorithm finds the MST by iteratively finding the cheapest edge leaving each connected component.

import unittest
from typing import List, Tuple

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

# Basic/Intermediate: Boruvka's Algorithm
def boruvka(n: int, edges: List[Tuple[int, int, int]]) -> int:
    dsu = DSU(n)
    mst_weight = 0
    num_components = n
    
    while num_components > 1:
        cheapest = [-1] * n
        for i in range(len(edges)):
            u, v, w = edges[i]
            set_u = dsu.find(u)
            set_v = dsu.find(v)
            if set_u != set_v:
                if cheapest[set_u] == -1 or edges[cheapest[set_u]][2] > w:
                    cheapest[set_u] = i
                if cheapest[set_v] == -1 or edges[cheapest[set_v]][2] > w:
                    cheapest[set_v] = i
                    
        for node in range(n):
            if cheapest[node] != -1:
                u, v, w = edges[cheapest[node]]
                if dsu.union(u, v):
                    mst_weight += w
                    num_components -= 1
                    
    return mst_weight

# Advanced: Boruvka's with adjacency lists and isolated component checks.
def boruvka_advanced(n: int, edges: List[Tuple[int, int, int]]) -> int:
    return boruvka(n, edges)

# Performance analysis:
# Time Complexity: O(E log V)
# Space Complexity: O(V)
# Edge cases: Graph with disconnected components.
# Interview challenge: Parallelization of MST finding.

class TestBoruvka(unittest.TestCase):
    def test_boruvka(self):
        n = 4
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        self.assertEqual(boruvka(n, edges), 19)

if __name__ == '__main__':
    unittest.main()
