"""
## A. Concept Name
Weighted Graphs

## B. One-Sentence Definition
A weighted graph is a graph where each edge has an associated numerical value, known as a weight or cost.

## C. Why Does This Exist?
To model real-world networks where connections have varying costs, distances, or capacities (like road distances between cities, latency in computer networks, or transaction costs).

## D. Intuition
Think of a regular graph as a map showing which cities have roads between them. A weighted graph adds the exact distance in miles for each road, allowing you to find the shortest or cheapest path, not just any path.

## E. Real-Life Analogy
- Flight Routes: Cities are vertices, flights are edges, and ticket prices are weights.
- Google Maps: Intersections are vertices, roads are edges, and the time it takes to drive on them are the weights.

## F. Mental Model
Imagine a set of points connected by strings. In an unweighted graph, all strings are the same length. In a weighted graph, some strings are long and elastic, while others are short and taut, representing different "costs" to traverse.

## G. Visual Explanation
Vertices: (A, B, C)
A --(5)--> B
A --(3)--> C
B --(20)-> C
The numbers in parentheses are the weights. Going A->C directly costs 3. Going A->B->C costs 5 + 20 = 25.

## H. Formal Explanation
A weighted graph G = (V, E, W) consists of a set of vertices V, a set of edges E, and a weight function W: E -> R that maps each edge to a real number. Can be directed or undirected. Can be represented via an Adjacency Matrix (a 2D array where `matrix[u][v] = weight`) or an Adjacency List (where `list[u]` stores `(v, weight)` pairs).

## I. Mathematical Foundation (if applicable)
Graph G = (V, E)
Weight function w(e) for e ∈ E.
Shortest path from s to t minimizes the sum of w(e) for all edges e in the path.

## J. From-Scratch Implementation (if applicable)
(See code below for Adjacency List and Matrix implementations).

## K. Library / Production Implementation (if applicable)
Python's `networkx` library represents weighted graphs where edge attributes store the weights: `G.add_edge(u, v, weight=5.0)`.

## L. Trace (walk through example)
For Adjacency Matrix with vertices A(0) and B(1):
1. Initialize a 2x2 matrix with infinity `inf`.
2. Add edge A->B with weight 5.0.
3. Update `matrix[0][1] = 5.0`.

## M. Complexity
- Space Complexity: Adjacency List O(V + E), Adjacency Matrix O(V^2).
- Time Complexity (Adding Edge): O(1) for both.
- Time Complexity (Query Edge): Adjacency List O(V) (or O(E/V) average), Adjacency Matrix O(1).

## N. Common Mistakes
- Using an Adjacency Matrix for a sparse graph (wastes O(V^2) memory).
- Forgetting to initialize the matrix diagonal to 0 or unreachables to infinity.

## O. Common Confusions
- "Why use Adjacency Lists if Matrix is faster to query?" Adjacency lists save massive amounts of memory in real-world sparse networks and are faster for iterating over neighbors.

## P. When To Use
- Routing, scheduling, or network flow problems.
- Finding shortest paths (Dijkstra's Algorithm) or minimum spanning trees (Kruskal/Prim).

## Q. When NOT To Use
- When connections have no "cost" or variation (use unweighted graphs).
- If just finding if a path exists regardless of distance.

## R. Trade-offs
- Adjacency List vs Matrix: Memory vs Fast Edge Lookup.

## S. Debugging
- Check if negative weights exist (this breaks algorithms like Dijkstra).
- Ensure undirected edges are added in both directions (u->v and v->u).

## T. Memory Hook (a short memorable principle)
Matrix for Dense (O(1) lookups), List for Sparse (O(V+E) memory).

## U. Active Recall (questions before answers)
1. How are weights stored in an Adjacency List? (As a tuple of (neighbor, weight) in the neighbor list).
2. What is the space complexity of an Adjacency Matrix? (O(V^2)).

## V. Practice (exercises)
1. Implement a method to remove an edge.
2. Implement Dijkstra's algorithm using the `SimpleWeightedGraph` class.

## W. Interview Question
"How do you represent a weighted graph in memory? What are the tradeoffs?"
(Answer: Adjacency Matrix for dense graphs offering O(1) edge lookups, Adjacency List for sparse graphs saving space O(V+E)).

## X. Project Connection
Used in GPS mapping software, delivery routing systems, and networking protocols (OSPF) to find optimal paths.
"""

from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
import unittest

# Basic Implementation
class SimpleWeightedGraph:
    def __init__(self, directed: bool = False):
        self.graph: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)
        self.directed = directed

    def add_edge(self, u: Any, v: Any, weight: float) -> None:
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))

    def get_neighbors(self, u: Any) -> List[Tuple[Any, float]]:
        return self.graph.get(u, [])


# Intermediate Implementation
class AdjacencyMatrixGraph:
    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.matrix[i][i] = 0.0

    def add_edge(self, u: int, v: int, weight: float) -> None:
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.matrix[u][v] = weight
            if not self.directed:
                self.matrix[v][u] = weight


# Advanced Implementation
class Edge:
    def __init__(self, src: 'Vertex', dest: 'Vertex', weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

class Vertex:
    def __init__(self, key: Any):
        self.key = key
        self.edges: List[Edge] = []

    def add_neighbor(self, neighbor: 'Vertex', weight: float):
        self.edges.append(Edge(self, neighbor, weight))

class ObjectOrientedGraph:
    def __init__(self, directed: bool = False):
        self.vertices: Dict[Any, Vertex] = {}
        self.directed = directed

    def add_vertex(self, key: Any) -> Vertex:
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)
        return self.vertices[key]

    def add_edge(self, u_key: Any, v_key: Any, weight: float) -> None:
        u = self.add_vertex(u_key)
        v = self.add_vertex(v_key)
        u.add_neighbor(v, weight)
        if not self.directed:
            v.add_neighbor(u, weight)

# Interview Challenge
def find_heaviest_edge(graph: SimpleWeightedGraph) -> Optional[Tuple[Any, Any, float]]:
    """
    Find the edge with the maximum weight in a given graph.
    """
    max_weight = float('-inf')
    heaviest_edge = None
    for u in graph.graph:
        for v, weight in graph.graph[u]:
            if weight > max_weight:
                max_weight = weight
                heaviest_edge = (u, v, weight)
    return heaviest_edge

# Tests
class TestWeightedGraphs(unittest.TestCase):
    def test_simple_weighted_graph(self):
        g = SimpleWeightedGraph(directed=False)
        g.add_edge('A', 'B', 5.0)
        g.add_edge('A', 'C', 3.0)
        self.assertIn(('B', 5.0), g.get_neighbors('A'))
        self.assertIn(('A', 5.0), g.get_neighbors('B'))

    def test_adjacency_matrix(self):
        g = AdjacencyMatrixGraph(3, directed=True)
        g.add_edge(0, 1, 2.5)
        self.assertEqual(g.matrix[0][1], 2.5)
        self.assertEqual(g.matrix[1][0], float('inf'))

    def test_heaviest_edge(self):
        g = SimpleWeightedGraph(directed=True)
        g.add_edge('A', 'B', 10)
        g.add_edge('B', 'C', 20)
        self.assertEqual(find_heaviest_edge(g), ('B', 'C', 20.0))

if __name__ == '__main__':
    unittest.main()
