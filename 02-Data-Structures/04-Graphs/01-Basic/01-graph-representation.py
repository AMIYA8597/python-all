"""
# ==============================================================================
# LABORATORY: GRAPH REPRESENTATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Tree is just a highly restricted Graph (a graph with no cycles, where every 
# node has exactly one parent). Graphs are the ultimate data structure for modeling 
# the real world: Social Networks (Facebook friends), Maps (Google Maps routing), 
# the Internet (routers connecting), and recommendation engines (Users -> Products).
# Before you can traverse or find the shortest path in a graph, you must know 
# how to represent it in RAM. The two primary ways are Adjacency Matrices and 
# Adjacency Lists.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Terminology: Vertices (V), Edges (E), Directed vs Undirected, Weighted.
# - Implement an Adjacency Matrix and understand its O(V^2) space complexity.
# - Implement an Adjacency List using a Python Dictionary (`defaultdict`).
# - Implement an Object-Oriented Graph.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List, Dict, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ADJACENCY MATRIX (DENSE GRAPHS)
# ==============================================================================
class AdjacencyMatrixGraph:
    """
    An Adjacency Matrix is a 2D array of size V x V (where V is the number of vertices).
    If there is an edge from Vertex A to Vertex B, matrix[A][B] = 1 (or the weight).
    Otherwise, it is 0.
    
    PROS: Checking if an edge exists between A and B takes O(1) time.
    CONS: It takes O(V^2) memory. A social network with 1 Billion users would 
          require an array of 1 Billion x 1 Billion elements (Exabytes of RAM!), 
          even though most users only have 300 friends (mostly zeros/sparse).
    """
    def __init__(self, num_vertices: int, directed: bool = False):
        self.V = num_vertices
        self.directed = directed
        # Initialize a V x V matrix filled with 0s
        self.matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        
    def add_edge(self, u: int, v: int, weight: int = 1):
        # Edge from u to v
        self.matrix[u][v] = weight
        if not self.directed:
            # If undirected, an edge from u->v implies an edge from v->u
            self.matrix[v][u] = weight
            
    def display(self):
        print("Adjacency Matrix:")
        for row in self.matrix:
            print("  ", row)

def demonstrate_matrix():
    section_header("Adjacency Matrix Representation")
    
    # 4 Vertices: 0, 1, 2, 3
    graph = AdjacencyMatrixGraph(4, directed=False)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    
    graph.display()
    
    print("\nChecking if edge exists between 0 and 2:")
    print(f"  matrix[0][2] == 1 -> {graph.matrix[0][2] == 1}")


# ==============================================================================
# 4. ADJACENCY LIST (SPARSE GRAPHS)
# ==============================================================================
class AdjacencyListGraph:
    """
    An Adjacency List uses a Dictionary (Hash Map). The Keys are the Vertices, 
    and the Values are Lists of neighbors.
    
    PROS: It takes O(V + E) memory. If 1 Billion users only have 300 friends each, 
          it only stores 300 Billion edges, which fits in modern server RAM.
    CONS: Checking if A is friends with B requires scanning A's list of friends, 
          taking O(Degree(A)) time instead of O(1).
          
    Note: 99% of FAANG interviews expect you to use an Adjacency List because 
    real-world graphs are "Sparse" (most nodes are NOT connected to most other nodes).
    """
    def __init__(self, directed: bool = False):
        self.directed = directed
        # defaultdict automatically creates an empty list if a key doesn't exist
        self.adj: Dict[Any, List[Tuple[Any, int]]] = defaultdict(list)
        
    def add_edge(self, u: str, v: str, weight: int = 1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))
            
    def display(self):
        print("Adjacency List:")
        for node, neighbors in self.adj.items():
            print(f"  {node} -> {neighbors}")

def demonstrate_adj_list():
    section_header("Adjacency List Representation")
    
    graph = AdjacencyListGraph(directed=True) # Directed Graph!
    
    # Let's map airport flights (Weighted Directed Graph)
    graph.add_edge("JFK", "LAX", weight=450)
    graph.add_edge("JFK", "SFO", weight=500)
    graph.add_edge("LAX", "ORD", weight=200)
    graph.add_edge("ORD", "JFK", weight=150)
    
    graph.display()
    
    print("\nNotice this is Directed. JFK goes to LAX, but LAX does not go to JFK!")
    print("Memory used is proportional to the number of flights (Edges), NOT")
    print("the total number of airports squared.")


# ==============================================================================
# 5. OBJECT-ORIENTED GRAPH
# ==============================================================================
class GraphNode:
    """
    Sometimes it's useful to represent a graph as actual objects in memory, 
    similar to TreeNodes.
    """
    def __init__(self, val: str):
        self.val = val
        self.neighbors: List['GraphNode'] = []
        
def demonstrate_oo_graph():
    section_header("Object-Oriented Graph Representation")
    
    nodeA = GraphNode("Alice")
    nodeB = GraphNode("Bob")
    nodeC = GraphNode("Charlie")
    
    nodeA.neighbors.append(nodeB)
    nodeB.neighbors.append(nodeC)
    nodeC.neighbors.append(nodeA) # Creates a cycle! A -> B -> C -> A
    
    print("Created A -> B -> C -> A")
    print(f"Alice's first neighbor is: {nodeA.neighbors[0].val}")
    print(f"That neighbor's first neighbor is: {nodeA.neighbors[0].neighbors[0].val}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When should you use an Adjacency Matrix instead of an Adjacency List?
   Answer: You should use a Matrix when the graph is highly "Dense" (almost every node connects to almost every other node), OR when the total number of vertices (V) is very small (e.g., V < 1,000) and you need to perform millions of O(1) edge existence checks.

2. What is the Space Complexity of an Adjacency List?
   Answer: O(V + E), where V is the number of vertices and E is the number of edges. This is because we must store an entry for every vertex, and across all lists, we store every edge.

3. Why is `defaultdict(list)` the preferred way to build a graph in Python?
   Answer: Because if you just use a standard dictionary `{}`, writing `adj[u].append(v)` will throw a `KeyError` if `u` hasn't been added yet. `defaultdict` automatically instantiates an empty list for `u` before appending, saving you from writing `if u not in adj: adj[u] = []` every time.
"""

if __name__ == "__main__":
    demonstrate_matrix()
    demonstrate_adj_list()
    demonstrate_oo_graph()
    print("\n[SUCCESS] Laboratory: Graph Representation Completed.")
