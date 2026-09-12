"""
Module: MST Variations
"""
# Learning objectives: Understand variations like Maximum Spanning Tree, Euclidean MST.
# Concept explanation: Adapting MST algorithms for different use cases.

import unittest
from typing import List, Tuple
import math

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
    def find(self, i: int) -> int:
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i: int, j: int) -> bool:
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

# Basic: Maximum Spanning Tree
def maximum_spanning_tree(n: int, edges: List[Tuple[int, int, int]]) -> int:
    dsu = DSU(n)
    # Sort edges descending by weight
    edges.sort(key=lambda item: item[2], reverse=True)
    mst_weight = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
    return mst_weight

# Intermediate: Euclidean MST (Points in 2D)
def euclidean_mst(points: List[Tuple[int, int]]) -> float:
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dist = math.sqrt((points[i][0]-points[j][0])**2 + (points[i][1]-points[j][1])**2)
            edges.append((i, j, dist))
    
    dsu = DSU(n)
    edges.sort(key=lambda item: item[2])
    mst_weight = 0.0
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
    return mst_weight

# Advanced: Second Best MST (O(VE))
# Omitted for brevity

# Performance analysis:
# Time Complexity: O(E log E) for Max Spanning Tree
# Space Complexity: O(V)
# Edge cases: Empty graph.
# Interview challenge: Connect points to minimize maximum edge.

class TestMSTVar(unittest.TestCase):
    def test_max_spanning_tree(self):
        n = 4
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        self.assertEqual(maximum_spanning_tree(n, edges), 31) # 15 + 10 + 6 = 31

if __name__ == '__main__':
    unittest.main()
