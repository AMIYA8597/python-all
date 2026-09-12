"""
## A. Concept Name
Kruskal's Algorithm

## B. Learning Objectives
Understand Kruskal's algorithm, Disjoint Set Union (DSU)

## C. Concept Explanation
Kruskal's finds the Minimum Spanning Tree (MST) by sorting edges and adding them using DSU to avoid cycles.

## D. Basic Implementation Details
Implementation of the Disjoint Set Union (DSU) with path compression and union by rank.

## E. Intermediate Implementation Details
Kruskal's algorithm implementation to find the total weight of the MST.

## F. Advanced Implementation Details
Kruskal's algorithm modification to return the specific edges that make up the MST.

## G. Performance Analysis
- Time Complexity: O(E log E) due to sorting edges.
- Space Complexity: O(V) for DSU.

## H. Edge Cases
Disconnected graph, empty graph, single-node graph.

## I. Interview Challenge
Find the second minimum spanning tree.

## J. Real-World Applications
Network design (laying cables, designing routing protocols), clustering.

## K. Common Pitfalls
Forgetting to sort the edges by weight before processing; inefficient DSU without path compression.

## L. Alternatives
Prim's Algorithm, Borůvka's algorithm.

## M. Best Practices
Use Path Compression and Union by Rank to achieve nearly O(1) time complexity for DSU operations.

## N. Memory Management
The DSU rank and parent arrays require O(V) space. The edge list requires O(E) space.

## O. Scaling Strategies
For very large dense graphs, Prim's may be more efficient. Parallel edge sorting can speed up Kruskal's.

## P. Debugging Tips
Verify the parent array structure if cycles are failing to be detected.

## Q. Related Data Structures
Union-Find / Disjoint Set Union.

## R. Related Algorithms
Prim's Algorithm, Cycle Detection Algorithms.

## S. Standard Library Equivalents
`networkx.algorithms.tree.mst.minimum_spanning_tree` in the NetworkX library.

## T. Coding Patterns
Greedy algorithmic pattern.

## U. Test Design
Write tests for cyclic graphs, trees, disconnected components, and graphs with negative weights.

## V. Version Control History
Initial implementation of Kruskal's algorithm and DSU.

## W. Code Review Checklist
Ensure path compression correctly updates parents up to the root.

## X. Project Connection
Useful for building the core logic of a network routing or optimization project.
"""

import unittest
from typing import List, Tuple, Set

# Basic Implementation: DSU
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

# Intermediate: Kruskal's Algorithm
def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> int:
    dsu = DSU(n)
    edges.sort(key=lambda item: item[2])
    mst_weight = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
    return mst_weight

# Advanced: Return edges of MST
def kruskal_edges(n: int, edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    dsu = DSU(n)
    edges.sort(key=lambda item: item[2])
    mst = []
    for u, v, w in edges:
        if dsu.union(u, v):
            mst.append((u, v, w))
    return mst

class TestKruskal(unittest.TestCase):
    def test_kruskal(self):
        n = 4
        edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
        self.assertEqual(kruskal(n, edges), 19)

if __name__ == '__main__':
    unittest.main()
