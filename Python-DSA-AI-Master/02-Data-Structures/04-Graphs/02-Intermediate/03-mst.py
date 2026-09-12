"""
## A. Concept Name
Minimum Spanning Trees (MST)

## B. Real-World Analogy
Imagine laying down a fiber-optic network connecting several cities. You want every city to be connected to the network, but fiber-optic cables are expensive. The Minimum Spanning Tree represents the exact set of cable routes that connects all the cities with the absolute minimum total cost of cable used, without creating any unnecessary redundant loops.

## C. Learning Objectives
1. Understand the concept of Spanning Trees and Minimum Spanning Trees.
2. Implement Kruskal's Algorithm using Disjoint Set Union (DSU).
3. Implement Prim's Algorithm using a Priority Queue.
4. Analyze the complexities and appropriate use cases for both algorithms.

## D. Concept Explanation
A Minimum Spanning Tree is a subset of the edges of a connected, edge-weighted undirected graph that connects all the vertices together, without any cycles, and with the minimum possible total edge weight.
- Kruskal's Algorithm: Sort all edges and greedily pick the smallest edge that doesn't form a cycle (using DSU).
- Prim's Algorithm: Start with a single vertex and greedily grow the tree by adding the smallest edge connecting the tree to a new vertex (using a Priority Queue).

## E. Memory Hooks/Mnemonics
- **Kruskal's = Kables (Edges)**: Focuses on sorting and picking the smallest *edges* globally.
- **Prim's = Points (Vertices)**: Focuses on starting from a single *vertex* (point) and expanding outward.

## F. Step-by-Step Breakdown
**Kruskal's**:
1. Sort all edges in non-decreasing order of their weight.
2. Pick the smallest edge. Check if it forms a cycle with the spanning tree formed so far (using DSU).
3. If no cycle is formed, include this edge. Else, discard it.
4. Repeat step 2 until there are (V-1) edges in the spanning tree.

**Prim's**:
1. Initialize a tree with a single vertex.
2. Maintain a set of all edges that connect the tree to vertices not yet in the tree.
3. Pick the smallest edge from this set and add its destination vertex to the tree.
4. Repeat until all vertices are in the tree.

## G. Base Implementation
- **Disjoint Set Union (DSU)** class to support Kruskal's algorithm with path compression and union by rank.

## H. Intermediate Implementation
- **Kruskal's Algorithm** utilizing the DSU to efficiently build an MST from a list of edges.

## I. Advanced Implementation
- **Prim's Algorithm** utilizing a min-heap (Priority Queue) and an adjacency list graph representation.

## J. Performance Analysis
- **Kruskal's**: Time Complexity O(E log E) or O(E log V) dominating due to edge sorting. Space Complexity O(V) for DSU.
- **Prim's**: Time Complexity O(E log V) with an adjacency list and binary heap. Space Complexity O(V + E) to store the graph and priority queue.

## K. Edge Cases & Gotchas
- **Disconnected Graph**: A full MST doesn't exist. These algorithms will find a minimum spanning forest instead.
- **Identical Edge Weights**: Handled naturally, but means the MST might not be unique.
- **Negative Weights**: Both algorithms work perfectly fine with negative edge weights (unlike Dijkstra's).

## L. Common Pitfalls
- Forgetting to use Path Compression and Union by Rank in DSU, leading to O(V) operations instead of O(α(V)).
- Adding a vertex to the visited set in Prim's *before* popping it from the heap, leading to sub-optimal edges or cycles.

## M. Practical Application
- Designing network topologies (telecommunications, water supply networks, electrical grids).
- Approximation algorithms for NP-hard problems like the Traveling Salesperson Problem (TSP).

## N. System Design Context
In a distributed system, MSTs are used to broadcast messages efficiently. A spanning tree protocol (STP) prevents broadcast storms in local area networks (LANs) by disabling redundant links while ensuring all switches remain connected.

## O. Interview Patterns
- **Find minimum cost to connect all nodes**: A classic MST indicator.
- **Can all nodes be reached given some constraint?**: Might involve Kruskal's to incrementally add edges.
- **Maximum Spanning Tree**: Just negate all edge weights or sort descending in Kruskal's.

## P. Best Practices
- Use Prim's algorithm for dense graphs (E ≈ V²).
- Use Kruskal's algorithm for sparse graphs (E ≈ V).

## Q. Testing Strategies
- Test with known minimum total weights.
- Test with disconnected components.
- Test with linear chains and star graphs.

## R. Debugging Tips
- If Kruskal's returns a tree with cycles, your DSU logic is flawed.
- If Prim's skips nodes, check if the graph dictionary encompasses all vertices properly.

## S. Comparative Analysis
| Feature | Kruskal's | Prim's |
|---------|-----------|--------|
| Approach | Edge-centric | Vertex-centric |
| Dense Graphs | Slower | Faster |
| Sparse Graphs | Faster | Slower |
| Core Data Structure | DSU | Priority Queue |

## T. Common Misconceptions
- **Misconception**: MST is the same as the shortest path tree.
- **Fact**: Dijkstra's algorithm finds the shortest path from a single source to all nodes. MST minimizes the total weight of *all* edges, not the path from a source.

## U. Vocabulary & Terminology
- **Spanning Tree**: A subgraph that includes all vertices of the original graph and is a tree.
- **Weight**: The cost associated with an edge.
- **Forest**: A disjoint set of trees.

## V. Related Concepts
- Disjoint Set Union (Union-Find)
- Dijkstra's Algorithm
- Greedy Algorithms

## W. Code Review Guide
- Ensure DSU `find` implements path compression (`parent[x] = find(parent[x])`).
- Verify the priority queue in Prim's pushes `(weight, u, v)` correctly.

## X. Project Connection
Understanding MSTs directly enables building efficient routing algorithms for our simulated network topology planner project, guaranteeing minimal cable costs.
"""

import heapq
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import unittest

# Basic Implementation: Disjoint Set Union
class DSU:
    def __init__(self, vertices: List[Any]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item: Any) -> Any:
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])  # Path compression
        return self.parent[item]

    def union(self, set1: Any, set2: Any) -> bool:
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            # Union by rank
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False

# Intermediate Implementation: Kruskal's Algorithm
def kruskal(vertices: List[Any], edges: List[Tuple[float, Any, Any]]) -> List[Tuple[float, Any, Any]]:
    mst = []
    dsu = DSU(vertices)
    edges.sort()  # Sort edges by weight

    for weight, u, v in edges:
        if dsu.union(u, v):
            mst.append((weight, u, v))
            
    return mst

# Advanced Implementation: Prim's Algorithm
def prim(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> List[Tuple[float, Any, Any]]:
    mst = []
    visited = set([start])
    edges = [
        (weight, start, to)
        for to, weight in graph.get(start, [])
    ]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.append((weight, frm, to))
            for next_to, next_weight in graph.get(to, []):
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))

    return mst

# Interview Challenge
def minimum_cost_to_connect_cities(n: int, connections: List[List[int]]) -> int:
    """
    Given n cities and connections = [[city1, city2, cost], ...].
    Find minimum cost to connect all cities. Return -1 if not possible.
    """
    vertices = list(range(1, n + 1))
    edges = [(cost, u, v) for u, v, cost in connections]
    mst = kruskal(vertices, edges)
    
    if len(mst) == n - 1:
        return sum(weight for weight, _, _ in mst)
    return -1

# Tests
class TestMST(unittest.TestCase):
    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [
            (1, 'A', 'B'),
            (4, 'A', 'C'),
            (2, 'B', 'C'),
            (5, 'B', 'D'),
            (1, 'C', 'D')
        ]
        self.graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }

    def test_kruskal(self):
        mst = kruskal(self.vertices, self.edges)
        self.assertEqual(sum(w for w, u, v in mst), 4)

    def test_prim(self):
        mst = prim(self.graph, 'A')
        self.assertEqual(sum(w for w, u, v in mst), 4)

    def test_connect_cities(self):
        conns = [[1,2,5], [1,3,6], [2,3,1]]
        self.assertEqual(minimum_cost_to_connect_cities(3, conns), 6)

if __name__ == '__main__':
    unittest.main()
