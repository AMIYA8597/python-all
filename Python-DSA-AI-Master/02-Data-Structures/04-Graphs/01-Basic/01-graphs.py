"""
## A. Concept Name
Graphs

## B. One-Sentence Definition
A graph is a non-linear data structure consisting of nodes (vertices) connected by edges.

## C. Why Does This Exist?
To model pairwise relationships between objects, enabling the representation of complex networks like social connections, maps, and the internet.

## D. Intuition
Imagine cities connected by roads. The cities are the points, and the roads are the connections between them. A graph simply records "what is connected to what".

## E. Real-Life Analogy
A social network. You are a node, and your friends are nodes. The friendship between you and a friend is an edge. If the friendship is mutual, it's an undirected edge. If you follow a celebrity but they don't follow you, it's a directed edge.

## F. Mental Model
Think of a graph as a set of circles (vertices) with lines (edges) drawn between some pairs of circles. Some lines might have arrows (direction) or numbers on them (weights).

## G. Visual Explanation
Vertices: {A, B, C, D}
Edges: {(A,B), (B,C), (C,D), (D,A)}
A --- B
|     |
D --- C

## H. Formal Explanation
A graph G is an ordered pair G = (V, E), where V is a set of vertices (or nodes) and E is a set of edges (links), which are 2-element subsets of V.

## I. Mathematical Foundation
- |V| = Number of vertices (order)
- |E| = Number of edges (size)
- Degree of v: Number of edges incident to vertex v.
- Max edges in simple undirected graph: |V|(|V|-1)/2

## J. From-Scratch Implementation
(See code below for the implementation using an Adjacency List)

## K. Library / Production Implementation
Python's `networkx` is the standard library for complex graph algorithms in production. For simple cases, a standard dictionary `dict[node] = list[nodes]` or `collections.defaultdict(list)` is universally used.

## L. Trace (walk through example)
1. Add Vertex A. Graph: {'A': []}
2. Add Vertex B. Graph: {'A': [], 'B': []}
3. Add Edge A-B. Graph: {'A': ['B'], 'B': ['A']}
4. Add Vertex C. Graph: {'A': ['B'], 'B': ['A'], 'C': []}
5. Add Edge B-C. Graph: {'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}

## M. Complexity
Time Complexity:
- Add Vertex: O(1)
- Add Edge: O(1)
- Remove Vertex: O(|V| + |E|) for Adjacency List
- Remove Edge: O(|E|) worst case for a specific node in Adjacency List
- Query Edge: O(|V|) worst case for Adjacency List

Space Complexity:
- Adjacency List: O(|V| + |E|)
- Adjacency Matrix: O(|V|^2)

## N. Common Mistakes
- Confusing Directed vs. Undirected graphs when adding edges (forgetting to add the reverse edge in an undirected graph).
- Using an Adjacency Matrix for sparse graphs (wastes huge amounts of memory).
- Getting stuck in infinite loops during traversal because visited nodes weren't tracked.

## O. Common Confusions
- "Is a tree a graph?" Yes, a tree is a special type of graph (a connected, acyclic, undirected graph).
- "Difference between Adjacency List and Matrix?" Matrix is a 2D array (good for dense graphs, O(1) edge lookup), List is a dict of lists (good for sparse graphs, efficient space).

## P. When To Use
- Modeling networks (social, computer, transportation).
- Finding shortest paths (GPS, routing).
- Dependency resolution (package managers, build systems).

## Q. When NOT To Use
- When relationships are strictly hierarchical (use a Tree).
- When data is simply sequential (use an Array or Linked List).
- When you just need key-value lookups (use a Hash Map).

## R. Trade-offs
- Adjacency List vs Adjacency Matrix: Adjacency List saves space for sparse graphs but makes edge lookup slower O(N) vs O(1) in Matrix. Matrix wastes O(V^2) space if edges are few.

## S. Debugging
- Print the adjacency list (dictionary) to verify connections.
- Draw the graph on paper if the number of nodes is small.
- Check if the graph has cycles when dealing with algorithms like topological sort.

## T. Memory Hook
"Dots and Lines". V for Vertices (dots), E for Edges (lines).

## U. Active Recall
1. What is the difference between a directed and undirected graph?
2. How do you represent a weighted edge in an Adjacency List?
3. What is the time complexity to find if an edge exists in an Adjacency Matrix vs Adjacency List?

## V. Practice
- Implement BFS and DFS traversal on a graph.
- Count the number of connected components in an undirected graph.
- Find the shortest path between two nodes using Dijkstra's Algorithm.

## W. Interview Question
"Clone a Graph" - Return a deep copy (clone) of a given connected undirected graph.
"Course Schedule" - Given a list of courses and prerequisites, can you finish all courses? (Cycle detection in directed graph).

## X. Project Connection
In an AI project, graphs are used in Knowledge Graphs to represent entities and their relationships, or in Pathfinding algorithms for NPCs in games.
"""

class Graph:
    """
    A foundational implementation of an Undirected Graph using an Adjacency List.
    """
    def __init__(self):
        # Using a dictionary to represent the adjacency list
        self.adj_list = {}

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, v1, v2):
        """Add an undirected edge between v1 and v2."""
        # Ensure both vertices exist
        if v1 not in self.adj_list:
            self.add_vertex(v1)
        if v2 not in self.adj_list:
            self.add_vertex(v2)
        
        # Add edge from v1 to v2
        self.adj_list[v1].append(v2)
        # Add edge from v2 to v1 (since it's undirected)
        self.adj_list[v2].append(v1)

    def remove_edge(self, v1, v2):
        """Remove the undirected edge between v1 and v2."""
        if v1 in self.adj_list and v2 in self.adj_list:
            try:
                self.adj_list[v1].remove(v2)
                self.adj_list[v2].remove(v1)
            except ValueError:
                pass # Edge doesn't exist

    def remove_vertex(self, vertex):
        """Remove a vertex and all its connected edges."""
        if vertex in self.adj_list:
            # First, remove all edges connected to this vertex from other vertices
            for adjacent_vertex in self.adj_list[vertex]:
                self.adj_list[adjacent_vertex].remove(vertex)
            # Finally, remove the vertex itself
            del self.adj_list[vertex]

    def display(self):
        """Print the graph's adjacency list."""
        for vertex in self.adj_list:
            print(f"{vertex} -> {self.adj_list[vertex]}")


if __name__ == "__main__":
    # ## L. Trace (walk through example) Execution
    print("Creating Graph...")
    g = Graph()
    
    print("\\nAdding Vertices A, B, C, D...")
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_vertex("D")
    
    print("\\nAdding Edges...")
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "A")
    
    print("\\nCurrent Graph:")
    g.display()
    
    print("\\nRemoving Edge A-B...")
    g.remove_edge("A", "B")
    g.display()
    
    print("\\nRemoving Vertex C...")
    g.remove_vertex("C")
    g.display()
