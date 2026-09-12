"""
## A. Concept Name
Graph Representation using Adjacency Matrix

## B. Learning Objectives
1. Understand how to represent a graph using a 2D array.
2. Analyze the trade-offs between Adjacency Matrix and Adjacency List.
3. Implement matrix-based graph operations.
4. Grasp space complexity implications for dense vs sparse graphs.

## C. Concept Explanation
An Adjacency Matrix is a 2D array of size V x V where V is the number of vertices.
Matrix[i][j] is 1 (or the edge weight) if there is an edge from vertex i to vertex j, 
and 0 (or infinity) otherwise. It allows O(1) edge lookups but consumes O(V^2) space.

## D. Performance Analysis
- Space Complexity: O(V^2) - bad for sparse graphs, fine for dense.
- Add Vertex: O(V^2) if dynamic resizing array, O(1) if pre-allocated.
- Add Edge: O(1)
- Check Edge (u, v): O(1)
- Find all Neighbors: O(V)

## E. Edge Cases
- Large sparse graphs leading to OutOfMemory.
- Self-loops (diagonal elements matrix[i][i] = 1).

## F. Interview Challenge
"Given an adjacency matrix representing a graph, write an algorithm to find the number of connected components."

## X. Project Connection
Used in various projects involving dense graphs, pathfinding algorithms (like Floyd-Warshall), and network connectivity matrix operations.
"""

from typing import List, Optional

class MatrixGraphBasic:
    """Basic undirected unweighted graph using Adjacency Matrix."""
    
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]
        
    def add_edge(self, u: int, v: int) -> None:
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.matrix[u][v] = 1
            self.matrix[v][u] = 1
            
    def has_edge(self, u: int, v: int) -> bool:
        return self.matrix[u][v] == 1

class MatrixGraphIntermediate:
    """Directed graph with dynamic resizing (conceptual logic)."""
    
    def __init__(self):
        self.matrix: List[List[int]] = []
        self.vertex_map = {} # Maps vertex name to index
        self.index_map = {}  # Maps index to vertex name
        self.count = 0
        
    def add_vertex(self, vertex: str) -> None:
        if vertex not in self.vertex_map:
            self.vertex_map[vertex] = self.count
            self.index_map[self.count] = vertex
            self.count += 1
            # Expand matrix
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0] * self.count)
            
    def add_edge(self, u: str, v: str) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        u_idx = self.vertex_map[u]
        v_idx = self.vertex_map[v]
        self.matrix[u_idx][v_idx] = 1
        
    def get_neighbors(self, u: str) -> List[str]:
        if u not in self.vertex_map: return []
        u_idx = self.vertex_map[u]
        neighbors = []
        for v_idx, val in enumerate(self.matrix[u_idx]):
            if val == 1:
                neighbors.append(self.index_map[v_idx])
        return neighbors

class MatrixGraphAdvanced:
    """Weighted graph using Adjacency Matrix."""
    
    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed
        # Using float('inf') for no edge
        self.matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.matrix[i][i] = 0 # Distance to self is 0
            
    def add_edge(self, u: int, v: int, weight: float) -> None:
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight


def test_basic_matrix():
    g = MatrixGraphBasic(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    assert g.has_edge(0, 1)
    assert g.has_edge(1, 0)
    assert not g.has_edge(1, 2)
    print("Basic Matrix tests passed.")

def test_intermediate_matrix():
    g = MatrixGraphIntermediate()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    neighbors = g.get_neighbors('A')
    assert 'B' in neighbors and 'C' in neighbors
    assert 'A' not in g.get_neighbors('B')
    print("Intermediate Matrix tests passed.")

def test_advanced_matrix():
    g = MatrixGraphAdvanced(3, directed=True)
    g.add_edge(0, 1, 5.5)
    assert g.matrix[0][1] == 5.5
    assert g.matrix[1][0] == float('inf')
    print("Advanced Matrix tests passed.")

if __name__ == "__main__":
    print("Running Adjacency Matrix tests...")
    test_basic_matrix()
    test_intermediate_matrix()
    test_advanced_matrix()
    print("All tests passed!")
