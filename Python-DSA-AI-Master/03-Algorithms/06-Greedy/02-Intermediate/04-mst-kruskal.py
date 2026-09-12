"""
Minimum Spanning Tree - Kruskal's Algorithm

Learning Objectives:
1. Understand Minimum Spanning Trees (MST).
2. Implement Disjoint Set Union (Union-Find) data structure.
3. Apply greedy strategy to edge selection.

Concept Explanation:
Kruskal's algorithm finds a Minimum Spanning Tree for a connected weighted graph. 
It sorts all edges in non-decreasing order of their weight and iteratively adds the 
smallest edge to the MST, provided it doesn't form a cycle. 
Cycle detection is efficiently handled using a Disjoint Set data structure.

Performance Analysis:
- Time Complexity: O(E log E) or O(E log V) due to sorting edges. Union-Find operations take nearly O(1).
- Space Complexity: O(V + E) for storing the graph and disjoint set.

Edge Cases:
- Disconnected graph (will output a Minimum Spanning Forest).
- Graph with single vertex.

Interview Challenge:
"Find the minimum cost to connect all cities in a network."
"""

from typing import List, Tuple
import unittest

class DisjointSet:
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
        
        if root_i == root_j:
            return False
            
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

def kruskal_basic(n_vertices: int, edges: List[Tuple[int, int, int]]) -> int:
    """Basic implementation returning min cost."""
    ds = DisjointSet(n_vertices)
    edges.sort(key=lambda x: x[2])
    
    mst_cost = 0
    edges_used = 0
    
    for u, v, weight in edges:
        if ds.union(u, v):
            mst_cost += weight
            edges_used += 1
            if edges_used == n_vertices - 1:
                break
                
    return mst_cost

def kruskal_intermediate(n_vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """Intermediate implementation returning min cost and MST edges."""
    ds = DisjointSet(n_vertices)
    edges.sort(key=lambda x: x[2])
    
    mst_cost = 0
    mst_edges = []
    
    for u, v, weight in edges:
        if ds.union(u, v):
            mst_cost += weight
            mst_edges.append((u, v, weight))
            if len(mst_edges) == n_vertices - 1:
                break
                
    return mst_cost, mst_edges

class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = []
        
    def add_edge(self, u: int, v: int, w: int):
        self.graph.append([u, v, w])
        
    def kruskal(self):
        return kruskal_intermediate(self.V, self.graph)

class TestKruskal(unittest.TestCase):
    def test_basic(self):
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        self.assertEqual(kruskal_basic(4, edges), 19) # (2,3,4), (0,3,5), (0,1,10)
        
    def test_intermediate(self):
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        cost, mst = kruskal_intermediate(4, edges)
        self.assertEqual(cost, 19)
        self.assertEqual(len(mst), 3)

if __name__ == "__main__":
    unittest.main()
