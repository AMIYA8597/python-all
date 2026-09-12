"""
## A. Concept Name
Graph Representation using Adjacency List

## B. Learning Objectives
1. Understand how graphs represent relationships between objects.
2. Learn the differences between directed and undirected graphs.
3. Implement a graph using an Adjacency List.
4. Understand the time and space complexity of graph operations.

## C. Concept Explanation
A graph G = (V, E) is a non-linear data structure consisting of nodes (vertices, V) and edges (E) that connect them.
In an Adjacency List representation, we use a dictionary (or an array of lists) where each key is a vertex, 
and the value is a list of its neighboring vertices. This is highly efficient for sparse graphs.

## D. Performance Analysis (Adjacency List)
- Space Complexity: O(V + E)
- Add Vertex: O(1)
- Add Edge: O(1)
- Check Edge (u, v): O(degree(u))
- Remove Edge: O(degree(u))

## E. Edge Cases
- Self-loops: A vertex with an edge to itself.
- Parallel edges (multigraphs): Multiple edges between the same pair of vertices. Not supported directly in sets/dicts unless weight list is used.
- Disconnected graphs: Some vertices have no edges.

## F. Interview Challenge
"Given an undirected graph, write a function to find the degree of each vertex and identify if it's a complete graph."

## X. Project Connection
Graphs are the foundation of social networks, routing algorithms (like Google Maps), and recommendation systems. Adjacency lists are typically the preferred representation for real-world (sparse) graphs.
"""

from typing import Dict, List, Set, Any, Optional

class GraphBasic:
    """Basic implementation of an unweighted, undirected graph."""
    
    def __init__(self):
        self.graph: Dict[Any, List[Any]] = {}
        
    def add_vertex(self, vertex: Any) -> None:
        if vertex not in self.graph:
            self.graph[vertex] = []
            
    def add_edge(self, u: Any, v: Any) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.graph[u].append(v)
        self.graph[v].append(u) # For undirected graph

    def get_neighbors(self, vertex: Any) -> List[Any]:
        return self.graph.get(vertex, [])

class GraphIntermediate:
    """Intermediate implementation supporting directed and undirected graphs."""
    
    def __init__(self, directed: bool = False):
        self.graph: Dict[Any, Set[Any]] = {}
        self.directed = directed
        
    def add_vertex(self, vertex: Any) -> None:
        if vertex not in self.graph:
            self.graph[vertex] = set()
            
    def add_edge(self, u: Any, v: Any) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.graph[u].add(v)
        if not self.directed:
            self.graph[v].add(u)
            
    def remove_edge(self, u: Any, v: Any) -> None:
        if u in self.graph and v in self.graph[u]:
            self.graph[u].remove(v)
        if not self.directed and v in self.graph and u in self.graph[v]:
            self.graph[v].remove(u)

class GraphAdvanced:
    """Advanced implementation supporting weighted, directed/undirected graphs."""
    
    def __init__(self, directed: bool = False):
        # Dictionary mapping vertex to a dictionary of neighbors and their edge weights
        self.graph: Dict[Any, Dict[Any, float]] = {}
        self.directed = directed
        
    def add_vertex(self, vertex: Any) -> None:
        if vertex not in self.graph:
            self.graph[vertex] = {}
            
    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        self.graph[u][v] = weight
        if not self.directed:
            self.graph[v][u] = weight
            
    def get_weight(self, u: Any, v: Any) -> Optional[float]:
        return self.graph.get(u, {}).get(v)

def test_basic_graph():
    g = GraphBasic()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    assert 2 in g.get_neighbors(1)
    assert 3 in g.get_neighbors(1)
    assert 1 in g.get_neighbors(2)
    print("Basic Graph tests passed.")

def test_intermediate_graph():
    g = GraphIntermediate(directed=True)
    g.add_edge('A', 'B')
    assert 'B' in g.graph['A']
    assert 'A' not in g.graph['B']
    g.remove_edge('A', 'B')
    assert 'B' not in g.graph['A']
    print("Intermediate Graph tests passed.")

def test_advanced_graph():
    g = GraphAdvanced(directed=False)
    g.add_edge("NYC", "LA", 2800)
    assert g.get_weight("NYC", "LA") == 2800
    assert g.get_weight("LA", "NYC") == 2800
    print("Advanced Graph tests passed.")

if __name__ == "__main__":
    print("Running Graph Representation tests...")
    test_basic_graph()
    test_intermediate_graph()
    test_advanced_graph()
    print("All tests passed!")
