#!/usr/bin/env python3
"""
Graph Data Structure Implementations and Representations
=======================================================

This module demonstrates comprehensive graph implementations including different
representations, traversal algorithms, and fundamental graph operations.

Graph Properties:
- Vertices (nodes) and edges (connections)
- Directed vs undirected graphs
- Weighted vs unweighted graphs
- Dense vs sparse graphs
- Connected vs disconnected components

Topics Covered:
- Adjacency list representation
- Adjacency matrix representation
- Edge list representation
- Graph traversals (DFS, BFS)
- Graph properties and analysis
- Weighted graph implementations
- Performance comparisons
- Real-world applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
from typing import List, Dict, Set, Tuple, Optional, Deque, Any
from collections import defaultdict, deque
import random
import time
from dataclasses import dataclass


# ============================================================================
# SECTION 1: ADJACENCY LIST GRAPH IMPLEMENTATION
# ============================================================================

class GraphAdjacencyList:
    """
    Graph implementation using adjacency list representation.
    
    Advantages:
    - Space efficient for sparse graphs: O(V + E)
    - Fast edge iteration for a vertex
    - Dynamic size
    
    Disadvantages:
    - Slower edge lookup: O(degree)
    """
    
    def __init__(self, directed: bool = False):
        """Initialize graph with adjacency list."""
        self.directed = directed
        self.adjacency_list: Dict[int, List[int]] = defaultdict(list)
        self.num_vertices = 0
        self.num_edges = 0
    
    def add_vertex(self, vertex: int) -> None:
        """
        Add vertex to graph.
        
        Time Complexity: O(1)
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.num_vertices += 1
    
    def add_edge(self, source: int, destination: int) -> None:
        """
        Add edge between source and destination vertices.
        
        Time Complexity: O(1) average case
        """
        # Add vertices if they don't exist
        self.add_vertex(source)
        self.add_vertex(destination)
        
        # Add edge
        if destination not in self.adjacency_list[source]:
            self.adjacency_list[source].append(destination)
            self.num_edges += 1
            
            # For undirected graph, add reverse edge
            if not self.directed and source not in self.adjacency_list[destination]:
                self.adjacency_list[destination].append(source)
    
    def remove_edge(self, source: int, destination: int) -> bool:
        """
        Remove edge between source and destination.
        
        Time Complexity: O(degree)
        """
        if source in self.adjacency_list and destination in self.adjacency_list[source]:
            self.adjacency_list[source].remove(destination)
            self.num_edges -= 1
            
            # For undirected graph, remove reverse edge
            if not self.directed and source in self.adjacency_list[destination]:
                self.adjacency_list[destination].remove(source)
            
            return True
        return False
    
    def remove_vertex(self, vertex: int) -> bool:
        """
        Remove vertex and all its edges.
        
        Time Complexity: O(V + degree)
        """
        if vertex not in self.adjacency_list:
            return False
        
        # Remove all edges pointing to this vertex
        for v in self.adjacency_list:
            if vertex in self.adjacency_list[v]:
                self.adjacency_list[v].remove(vertex)
                if not self.directed:
                    self.num_edges -= 1
        
        # Remove edges from this vertex
        self.num_edges -= len(self.adjacency_list[vertex])
        
        # Remove vertex
        del self.adjacency_list[vertex]
        self.num_vertices -= 1
        
        return True
    
    def has_edge(self, source: int, destination: int) -> bool:
        """
        Check if edge exists between source and destination.
        
        Time Complexity: O(degree)
        """
        return (source in self.adjacency_list and 
                destination in self.adjacency_list[source])
    
    def get_vertices(self) -> List[int]:
        """Get all vertices in graph."""
        return list(self.adjacency_list.keys())
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Get all neighbors of a vertex."""
        return self.adjacency_list.get(vertex, []).copy()
    
    def get_degree(self, vertex: int) -> int:
        """Get degree of a vertex."""
        if vertex not in self.adjacency_list:
            return 0
        
        degree = len(self.adjacency_list[vertex])
        
        # For undirected graph, count incoming edges too
        if not self.directed:
            return degree
        
        # For directed graph, this is out-degree
        return degree
    
    def get_in_degree(self, vertex: int) -> int:
        """Get in-degree of a vertex (directed graphs)."""
        if not self.directed:
            return self.get_degree(vertex)
        
        in_degree = 0
        for v in self.adjacency_list:
            if vertex in self.adjacency_list[v]:
                in_degree += 1
        return in_degree
    
    def display(self) -> None:
        """Display graph structure."""
        print(f"Graph ({'Directed' if self.directed else 'Undirected'}):")
        print(f"Vertices: {self.num_vertices}, Edges: {self.num_edges}")
        
        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = self.adjacency_list[vertex]
            print(f"  {vertex}: {neighbors}")
    
    def __str__(self) -> str:
        """String representation of graph."""
        return f"GraphAdjList(V={self.num_vertices}, E={self.num_edges}, directed={self.directed})"


# ============================================================================
# SECTION 2: ADJACENCY MATRIX GRAPH IMPLEMENTATION
# ============================================================================

class GraphAdjacencyMatrix:
    """
    Graph implementation using adjacency matrix representation.
    
    Advantages:
    - Fast edge lookup: O(1)
    - Simple representation
    - Good for dense graphs
    
    Disadvantages:
    - Space inefficient for sparse graphs: O(V²)
    - Adding vertices is expensive
    """
    
    def __init__(self, max_vertices: int = 100, directed: bool = False):
        """Initialize graph with adjacency matrix."""
        self.directed = directed
        self.max_vertices = max_vertices
        self.num_vertices = 0
        self.num_edges = 0
        
        # Initialize matrix with zeros
        self.matrix = [[0 for _ in range(max_vertices)] for _ in range(max_vertices)]
        
        # Map vertex labels to indices
        self.vertex_to_index: Dict[int, int] = {}
        self.index_to_vertex: Dict[int, int] = {}
    
    def add_vertex(self, vertex: int) -> bool:
        """
        Add vertex to graph.
        
        Time Complexity: O(1)
        """
        if vertex in self.vertex_to_index:
            return False
        
        if self.num_vertices >= self.max_vertices:
            raise ValueError("Maximum vertices exceeded")
        
        # Add vertex mapping
        index = self.num_vertices
        self.vertex_to_index[vertex] = index
        self.index_to_vertex[index] = vertex
        self.num_vertices += 1
        
        return True
    
    def add_edge(self, source: int, destination: int, weight: int = 1) -> bool:
        """
        Add edge between source and destination vertices.
        
        Time Complexity: O(1)
        """
        # Add vertices if they don't exist
        self.add_vertex(source)
        self.add_vertex(destination)
        
        source_idx = self.vertex_to_index[source]
        dest_idx = self.vertex_to_index[destination]
        
        # Add edge if it doesn't exist
        if self.matrix[source_idx][dest_idx] == 0:
            self.matrix[source_idx][dest_idx] = weight
            self.num_edges += 1
            
            # For undirected graph, add reverse edge
            if not self.directed and self.matrix[dest_idx][source_idx] == 0:
                self.matrix[dest_idx][source_idx] = weight
            
            return True
        
        return False
    
    def remove_edge(self, source: int, destination: int) -> bool:
        """
        Remove edge between source and destination.
        
        Time Complexity: O(1)
        """
        if (source not in self.vertex_to_index or 
            destination not in self.vertex_to_index):
            return False
        
        source_idx = self.vertex_to_index[source]
        dest_idx = self.vertex_to_index[destination]
        
        if self.matrix[source_idx][dest_idx] != 0:
            self.matrix[source_idx][dest_idx] = 0
            self.num_edges -= 1
            
            # For undirected graph, remove reverse edge
            if not self.directed and self.matrix[dest_idx][source_idx] != 0:
                self.matrix[dest_idx][source_idx] = 0
            
            return True
        
        return False
    
    def has_edge(self, source: int, destination: int) -> bool:
        """
        Check if edge exists between source and destination.
        
        Time Complexity: O(1)
        """
        if (source not in self.vertex_to_index or 
            destination not in self.vertex_to_index):
            return False
        
        source_idx = self.vertex_to_index[source]
        dest_idx = self.vertex_to_index[destination]
        
        return self.matrix[source_idx][dest_idx] != 0
    
    def get_edge_weight(self, source: int, destination: int) -> Optional[int]:
        """Get weight of edge between source and destination."""
        if not self.has_edge(source, destination):
            return None
        
        source_idx = self.vertex_to_index[source]
        dest_idx = self.vertex_to_index[destination]
        
        return self.matrix[source_idx][dest_idx]
    
    def get_vertices(self) -> List[int]:
        """Get all vertices in graph."""
        return list(self.vertex_to_index.keys())
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Get all neighbors of a vertex."""
        if vertex not in self.vertex_to_index:
            return []
        
        neighbors = []
        vertex_idx = self.vertex_to_index[vertex]
        
        for i in range(self.num_vertices):
            if self.matrix[vertex_idx][i] != 0:
                neighbors.append(self.index_to_vertex[i])
        
        return neighbors
    
    def get_degree(self, vertex: int) -> int:
        """Get degree of a vertex."""
        return len(self.get_neighbors(vertex))
    
    def display(self) -> None:
        """Display adjacency matrix."""
        print(f"Graph ({'Directed' if self.directed else 'Undirected'}):")
        print(f"Vertices: {self.num_vertices}, Edges: {self.num_edges}")
        print("\nAdjacency Matrix:")
        
        # Print header
        vertices = sorted(self.vertex_to_index.keys())
        print("     ", end="")
        for v in vertices:
            print(f"{v:4}", end="")
        print()
        
        # Print matrix
        for v1 in vertices:
            print(f"{v1:4}: ", end="")
            v1_idx = self.vertex_to_index[v1]
            for v2 in vertices:
                v2_idx = self.vertex_to_index[v2]
                print(f"{self.matrix[v1_idx][v2_idx]:4}", end="")
            print()
    
    def __str__(self) -> str:
        """String representation of graph."""
        return f"GraphAdjMatrix(V={self.num_vertices}, E={self.num_edges}, directed={self.directed})"


# ============================================================================
# SECTION 3: WEIGHTED GRAPH IMPLEMENTATION
# ============================================================================

@dataclass
class Edge:
    """Represents a weighted edge in a graph."""
    source: int
    destination: int
    weight: float
    
    def __lt__(self, other):
        """Compare edges by weight."""
        return self.weight < other.weight
    
    def __str__(self):
        return f"({self.source} -> {self.destination}, w={self.weight})"


class WeightedGraph:
    """
    Weighted graph implementation using adjacency list with edge weights.
    
    Supports both directed and undirected weighted graphs.
    """
    
    def __init__(self, directed: bool = False):
        """Initialize weighted graph."""
        self.directed = directed
        self.adjacency_list: Dict[int, Dict[int, float]] = defaultdict(dict)
        self.num_vertices = 0
        self.num_edges = 0
    
    def add_vertex(self, vertex: int) -> None:
        """Add vertex to graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}
            self.num_vertices += 1
    
    def add_edge(self, source: int, destination: int, weight: float) -> None:
        """Add weighted edge between vertices."""
        # Add vertices if they don't exist
        self.add_vertex(source)
        self.add_vertex(destination)
        
        # Add edge with weight
        if destination not in self.adjacency_list[source]:
            self.num_edges += 1
        
        self.adjacency_list[source][destination] = weight
        
        # For undirected graph, add reverse edge
        if not self.directed:
            self.adjacency_list[destination][source] = weight
    
    def remove_edge(self, source: int, destination: int) -> bool:
        """Remove edge between vertices."""
        if (source in self.adjacency_list and 
            destination in self.adjacency_list[source]):
            
            del self.adjacency_list[source][destination]
            self.num_edges -= 1
            
            # For undirected graph, remove reverse edge
            if not self.directed:
                if source in self.adjacency_list[destination]:
                    del self.adjacency_list[destination][source]
            
            return True
        return False
    
    def get_edge_weight(self, source: int, destination: int) -> Optional[float]:
        """Get weight of edge between vertices."""
        if (source in self.adjacency_list and 
            destination in self.adjacency_list[source]):
            return self.adjacency_list[source][destination]
        return None
    
    def get_vertices(self) -> List[int]:
        """Get all vertices in graph."""
        return list(self.adjacency_list.keys())
    
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """Get neighbors with their edge weights."""
        if vertex not in self.adjacency_list:
            return []
        
        return [(neighbor, weight) for neighbor, weight in self.adjacency_list[vertex].items()]
    
    def get_all_edges(self) -> List[Edge]:
        """Get all edges in the graph."""
        edges = []
        
        for source in self.adjacency_list:
            for destination, weight in self.adjacency_list[source].items():
                if self.directed or source <= destination:  # Avoid duplicates in undirected
                    edges.append(Edge(source, destination, weight))
        
        return edges
    
    def display(self) -> None:
        """Display weighted graph structure."""
        print(f"Weighted Graph ({'Directed' if self.directed else 'Undirected'}):")
        print(f"Vertices: {self.num_vertices}, Edges: {self.num_edges}")
        
        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = self.adjacency_list[vertex]
            neighbor_str = [f"{neighbor}(w={weight})" for neighbor, weight in neighbors.items()]
            print(f"  {vertex}: {neighbor_str}")


# ============================================================================
# SECTION 4: GRAPH TRAVERSAL ALGORITHMS
# ============================================================================

class GraphTraversal:
    """Collection of graph traversal algorithms."""
    
    @staticmethod
    def depth_first_search(graph: GraphAdjacencyList, start_vertex: int) -> List[int]:
        """
        Depth-First Search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Uses stack (recursion) to explore as far as possible before backtracking.
        """
        visited = set()
        result = []
        
        def dfs_recursive(vertex: int) -> None:
            visited.add(vertex)
            result.append(vertex)
            
            # Visit all neighbors
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        if start_vertex in graph.adjacency_list:
            dfs_recursive(start_vertex)
        
        return result
    
    @staticmethod
    def depth_first_search_iterative(graph: GraphAdjacencyList, start_vertex: int) -> List[int]:
        """
        Iterative DFS using explicit stack.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_vertex not in graph.adjacency_list:
            return []
        
        visited = set()
        result = []
        stack = [start_vertex]
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors to stack (reverse order for consistent traversal)
                neighbors = graph.get_neighbors(vertex)
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    @staticmethod
    def breadth_first_search(graph: GraphAdjacencyList, start_vertex: int) -> List[int]:
        """
        Breadth-First Search traversal.
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Uses queue to explore all neighbors before going deeper.
        """
        if start_vertex not in graph.adjacency_list:
            return []
        
        visited = set()
        result = []
        queue = deque([start_vertex])
        
        visited.add(start_vertex)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            # Add unvisited neighbors to queue
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    @staticmethod
    def find_path_dfs(graph: GraphAdjacencyList, start: int, end: int) -> Optional[List[int]]:
        """
        Find path between two vertices using DFS.
        
        Returns first path found (not necessarily shortest).
        """
        visited = set()
        path = []
        
        def dfs_path(vertex: int) -> bool:
            visited.add(vertex)
            path.append(vertex)
            
            if vertex == end:
                return True
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    if dfs_path(neighbor):
                        return True
            
            path.pop()  # Backtrack
            return False
        
        if start in graph.adjacency_list and dfs_path(start):
            return path
        
        return None
    
    @staticmethod
    def find_shortest_path_bfs(graph: GraphAdjacencyList, start: int, end: int) -> Optional[List[int]]:
        """
        Find shortest path between two vertices using BFS.
        
        Returns shortest path in unweighted graph.
        """
        if start not in graph.adjacency_list:
            return None
        
        if start == end:
            return [start]
        
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)
        
        while queue:
            vertex, path = queue.popleft()
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    @staticmethod
    def is_connected(graph: GraphAdjacencyList) -> bool:
        """
        Check if undirected graph is connected.
        
        A graph is connected if there's a path between every pair of vertices.
        """
        if graph.directed:
            raise ValueError("Connection check only valid for undirected graphs")
        
        vertices = graph.get_vertices()
        if not vertices:
            return True
        
        # Perform DFS from first vertex
        visited = set()
        
        def dfs(vertex: int) -> None:
            visited.add(vertex)
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs(neighbor)
        
        dfs(vertices[0])
        
        # Check if all vertices were visited
        return len(visited) == len(vertices)
    
    @staticmethod
    def find_connected_components(graph: GraphAdjacencyList) -> List[List[int]]:
        """
        Find all connected components in undirected graph.
        
        Returns list of components, each component is a list of vertices.
        """
        if graph.directed:
            raise ValueError("Connected components only valid for undirected graphs")
        
        visited = set()
        components = []
        
        def dfs_component(vertex: int, component: List[int]) -> None:
            visited.add(vertex)
            component.append(vertex)
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    dfs_component(neighbor, component)
        
        for vertex in graph.get_vertices():
            if vertex not in visited:
                component = []
                dfs_component(vertex, component)
                components.append(component)
        
        return components


# ============================================================================
# SECTION 5: GRAPH ANALYSIS AND PROPERTIES
# ============================================================================

def analyze_graph(graph: GraphAdjacencyList) -> Dict[str, Any]:
    """
    Analyze graph properties and return statistics.
    
    Returns dictionary with various graph metrics.
    """
    vertices = graph.get_vertices()
    analysis = {
        'num_vertices': graph.num_vertices,
        'num_edges': graph.num_edges,
        'is_directed': graph.directed,
        'density': 0.0,
        'average_degree': 0.0,
        'max_degree': 0,
        'min_degree': float('inf'),
        'degree_sequence': [],
        'is_connected': False,
        'num_components': 0,
        'diameter': -1
    }
    
    if not vertices:
        return analysis
    
    # Calculate degree statistics
    degrees = []
    for vertex in vertices:
        degree = graph.get_degree(vertex)
        degrees.append(degree)
        analysis['max_degree'] = max(analysis['max_degree'], degree)
        analysis['min_degree'] = min(analysis['min_degree'], degree)
    
    analysis['degree_sequence'] = sorted(degrees, reverse=True)
    analysis['average_degree'] = sum(degrees) / len(degrees) if degrees else 0
    
    # Calculate density
    max_edges = graph.num_vertices * (graph.num_vertices - 1)
    if not graph.directed:
        max_edges //= 2
    
    if max_edges > 0:
        analysis['density'] = graph.num_edges / max_edges
    
    # Analyze connectivity (for undirected graphs)
    if not graph.directed:
        analysis['is_connected'] = GraphTraversal.is_connected(graph)
        components = GraphTraversal.find_connected_components(graph)
        analysis['num_components'] = len(components)
        
        # Calculate diameter (longest shortest path in largest component)
        if components:
            largest_component = max(components, key=len)
            if len(largest_component) > 1:
                analysis['diameter'] = calculate_diameter(graph, largest_component)
    
    return analysis


def calculate_diameter(graph: GraphAdjacencyList, vertices: List[int]) -> int:
    """
    Calculate diameter of a connected component.
    
    Diameter is the longest shortest path between any two vertices.
    """
    max_distance = 0
    
    for start in vertices:
        # BFS to find shortest distances from start to all other vertices
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            
            for neighbor in graph.get_neighbors(vertex):
                if neighbor in vertices and neighbor not in distances:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
                    max_distance = max(max_distance, distances[neighbor])
    
    return max_distance


# ============================================================================
# SECTION 6: PERFORMANCE COMPARISON
# ============================================================================

def benchmark_graph_representations():
    """Compare performance of different graph representations."""
    print("\n=== GRAPH REPRESENTATION PERFORMANCE COMPARISON ===")
    
    sizes = [100, 500, 1000]
    
    for size in sizes:
        print(f"\nBenchmarking with {size} vertices:")
        
        # Create graphs
        adj_list = GraphAdjacencyList()
        adj_matrix = GraphAdjacencyMatrix(max_vertices=size)
        
        # Add vertices
        vertices = list(range(size))
        
        # Benchmark vertex addition
        start = time.perf_counter()
        for v in vertices:
            adj_list.add_vertex(v)
        list_vertex_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for v in vertices:
            adj_matrix.add_vertex(v)
        matrix_vertex_time = time.perf_counter() - start
        
        # Add random edges (10% density)
        edges = []
        num_edges = int(0.1 * size * (size - 1) / 2)
        
        for _ in range(num_edges):
            u = random.randint(0, size - 1)
            v = random.randint(0, size - 1)
            if u != v:
                edges.append((u, v))
        
        # Benchmark edge addition
        start = time.perf_counter()
        for u, v in edges:
            adj_list.add_edge(u, v)
        list_edge_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for u, v in edges:
            adj_matrix.add_edge(u, v)
        matrix_edge_time = time.perf_counter() - start
        
        # Benchmark edge lookup
        test_edges = random.sample(edges, min(100, len(edges)))
        
        start = time.perf_counter()
        for u, v in test_edges:
            adj_list.has_edge(u, v)
        list_lookup_time = time.perf_counter() - start
        
        start = time.perf_counter()
        for u, v in test_edges:
            adj_matrix.has_edge(u, v)
        matrix_lookup_time = time.perf_counter() - start
        
        print(f"  Vertex addition:")
        print(f"    Adjacency List:   {list_vertex_time:.6f}s")
        print(f"    Adjacency Matrix: {matrix_vertex_time:.6f}s")
        
        print(f"  Edge addition ({len(edges)} edges):")
        print(f"    Adjacency List:   {list_edge_time:.6f}s")
        print(f"    Adjacency Matrix: {matrix_edge_time:.6f}s")
        
        print(f"  Edge lookup ({len(test_edges)} lookups):")
        print(f"    Adjacency List:   {list_lookup_time:.6f}s")
        print(f"    Adjacency Matrix: {matrix_lookup_time:.6f}s")
        print(f"    Matrix speedup:   {list_lookup_time / matrix_lookup_time:.1f}x")


# ============================================================================
# SECTION 7: REAL-WORLD APPLICATIONS
# ============================================================================

def create_social_network_example():
    """Create example social network graph."""
    print("\n=== SOCIAL NETWORK GRAPH EXAMPLE ===")
    
    # Create undirected graph for social network
    social_network = GraphAdjacencyList(directed=False)
    
    # Add people (vertices)
    people = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace"]
    people_ids = {name: i for i, name in enumerate(people)}
    id_to_name = {i: name for name, i in people_ids.items()}
    
    # Add friendships (edges)
    friendships = [
        ("Alice", "Bob"), ("Alice", "Charlie"), ("Alice", "Diana"),
        ("Bob", "Charlie"), ("Bob", "Eve"),
        ("Charlie", "Diana"), ("Charlie", "Frank"),
        ("Diana", "Frank"), ("Diana", "Grace"),
        ("Eve", "Frank"),
        ("Frank", "Grace")
    ]
    
    for person1, person2 in friendships:
        social_network.add_edge(people_ids[person1], people_ids[person2])
    
    print("Social Network Graph:")
    for person_id, person_name in id_to_name.items():
        friends = social_network.get_neighbors(person_id)
        friend_names = [id_to_name[fid] for fid in friends]
        print(f"  {person_name}: friends with {friend_names}")
    
    # Analyze the network
    analysis = analyze_graph(social_network)
    print(f"\nNetwork Analysis:")
    print(f"  Total people: {analysis['num_vertices']}")
    print(f"  Total friendships: {analysis['num_edges']}")
    print(f"  Average friends per person: {analysis['average_degree']:.1f}")
    print(f"  Network density: {analysis['density']:.2f}")
    print(f"  Is fully connected: {analysis['is_connected']}")
    
    # Find path between two people
    alice_id = people_ids["Alice"]
    grace_id = people_ids["Grace"]
    
    path = GraphTraversal.find_shortest_path_bfs(social_network, alice_id, grace_id)
    if path:
        path_names = [id_to_name[pid] for pid in path]
        print(f"  Shortest connection from Alice to Grace: {' -> '.join(path_names)}")


def create_city_road_network():
    """Create weighted graph representing city road network."""
    print("\n=== CITY ROAD NETWORK EXAMPLE ===")
    
    # Create weighted directed graph (one-way streets)
    road_network = WeightedGraph(directed=True)
    
    # Add intersections and roads with travel times (minutes)
    roads = [
        (1, 2, 5.0),   # Intersection 1 to 2: 5 minutes
        (1, 3, 8.0),   # Intersection 1 to 3: 8 minutes
        (2, 3, 2.0),   # Intersection 2 to 3: 2 minutes
        (2, 4, 7.0),   # Intersection 2 to 4: 7 minutes
        (3, 4, 3.0),   # Intersection 3 to 4: 3 minutes
        (3, 5, 6.0),   # Intersection 3 to 5: 6 minutes
        (4, 5, 1.0),   # Intersection 4 to 5: 1 minute
        (4, 6, 4.0),   # Intersection 4 to 6: 4 minutes
        (5, 6, 2.0),   # Intersection 5 to 6: 2 minutes
    ]
    
    for start, end, time in roads:
        road_network.add_edge(start, end, time)
    
    print("Road Network (travel times in minutes):")
    road_network.display()
    
    # Find all roads from intersection 3
    neighbors = road_network.get_neighbors(3)
    print(f"\nRoads from intersection 3:")
    for neighbor, time in neighbors:
        print(f"  To intersection {neighbor}: {time} minutes")
    
    return road_network


# ============================================================================
# SECTION 8: TESTING AND VALIDATION
# ============================================================================

def test_graph_operations():
    """Comprehensive testing of graph implementations."""
    print("\n=== TESTING GRAPH OPERATIONS ===")
    
    # Test Adjacency List Graph
    print("Testing GraphAdjacencyList:")
    graph = GraphAdjacencyList(directed=False)
    
    # Test vertex and edge operations
    vertices = [1, 2, 3, 4, 5]
    for v in vertices:
        graph.add_vertex(v)
    
    edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    assert graph.num_vertices == 5, "Should have 5 vertices"
    assert graph.num_edges == 5, "Should have 5 edges"
    assert graph.has_edge(1, 2), "Should have edge 1-2"
    assert graph.has_edge(2, 1), "Should have edge 2-1 (undirected)"
    assert not graph.has_edge(1, 5), "Should not have direct edge 1-5"
    
    # Test neighbors
    neighbors_1 = graph.get_neighbors(1)
    assert set(neighbors_1) == {2, 3}, f"Neighbors of 1 should be {{2, 3}}, got {neighbors_1}"
    
    print("  GraphAdjacencyList: All tests passed!")
    
    # Test Adjacency Matrix Graph
    print("Testing GraphAdjacencyMatrix:")
    matrix_graph = GraphAdjacencyMatrix(max_vertices=10, directed=False)
    
    for v in vertices:
        matrix_graph.add_vertex(v)
    
    for u, v in edges:
        matrix_graph.add_edge(u, v)
    
    assert matrix_graph.num_vertices == 5, "Should have 5 vertices"
    assert matrix_graph.has_edge(1, 2), "Should have edge 1-2"
    assert matrix_graph.get_edge_weight(1, 2) == 1, "Default weight should be 1"
    
    print("  GraphAdjacencyMatrix: All tests passed!")
    
    # Test Weighted Graph
    print("Testing WeightedGraph:")
    weighted = WeightedGraph(directed=True)
    
    weighted.add_edge(1, 2, 5.5)
    weighted.add_edge(2, 3, 3.2)
    weighted.add_edge(1, 3, 8.1)
    
    assert weighted.get_edge_weight(1, 2) == 5.5, "Should have correct weight"
    assert weighted.get_edge_weight(2, 1) is None, "Directed graph shouldn't have reverse edge"
    
    print("  WeightedGraph: All tests passed!")
    
    # Test traversals
    print("Testing Graph Traversals:")
    
    # Create test graph for traversals
    test_graph = GraphAdjacencyList(directed=False)
    test_edges = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)]
    for u, v in test_edges:
        test_graph.add_edge(u, v)
    
    dfs_result = GraphTraversal.depth_first_search(test_graph, 1)
    bfs_result = GraphTraversal.breadth_first_search(test_graph, 1)
    
    assert len(dfs_result) == 6, "DFS should visit all 6 vertices"
    assert len(bfs_result) == 6, "BFS should visit all 6 vertices"
    assert dfs_result[0] == 1, "DFS should start with vertex 1"
    assert bfs_result[0] == 1, "BFS should start with vertex 1"
    
    # Test path finding
    path = GraphTraversal.find_shortest_path_bfs(test_graph, 1, 6)
    assert path is not None, "Should find path from 1 to 6"
    assert path[0] == 1 and path[-1] == 6, "Path should start at 1 and end at 6"
    
    print("  Graph Traversals: All tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Graph Data Structure Implementations and Analysis")
    print("=" * 55)
    
    try:
        # Basic graph demonstrations
        print("=== BASIC GRAPH DEMONSTRATIONS ===")
        
        # Adjacency List Graph
        print("\n1. Adjacency List Graph:")
        adj_list = GraphAdjacencyList(directed=False)
        
        # Add vertices and edges
        edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
        for u, v in edges:
            adj_list.add_edge(u, v)
        
        adj_list.display()
        
        # Adjacency Matrix Graph
        print("\n2. Adjacency Matrix Graph:")
        adj_matrix = GraphAdjacencyMatrix(max_vertices=10, directed=False)
        
        for u, v in edges:
            adj_matrix.add_edge(u, v)
        
        adj_matrix.display()
        
        # Weighted Graph
        print("\n3. Weighted Graph:")
        weighted = WeightedGraph(directed=True)
        
        weighted_edges = [(1, 2, 4.5), (1, 3, 2.1), (2, 3, 1.8), (2, 4, 3.7), (3, 4, 2.3)]
        for u, v, w in weighted_edges:
            weighted.add_edge(u, v, w)
        
        weighted.display()
        
        # Graph Traversals
        print("\n4. Graph Traversal Examples:")
        print(f"DFS from vertex 1: {GraphTraversal.depth_first_search(adj_list, 1)}")
        print(f"BFS from vertex 1: {GraphTraversal.breadth_first_search(adj_list, 1)}")
        
        path = GraphTraversal.find_shortest_path_bfs(adj_list, 1, 5)
        print(f"Shortest path from 1 to 5: {path}")
        
        # Graph Analysis
        print("\n5. Graph Analysis:")
        analysis = analyze_graph(adj_list)
        print(f"Vertices: {analysis['num_vertices']}, Edges: {analysis['num_edges']}")
        print(f"Density: {analysis['density']:.3f}")
        print(f"Average degree: {analysis['average_degree']:.1f}")
        print(f"Is connected: {analysis['is_connected']}")
        
        # Real-world applications
        create_social_network_example()
        create_city_road_network()
        
        # Performance benchmarks
        benchmark_graph_representations()
        
        # Run tests
        test_graph_operations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 55}")
        print("Graph implementation demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement graph using edge list representation.

2. Add graph coloring algorithms (vertex coloring, edge coloring).

3. Implement topological sorting for directed acyclic graphs.

4. Create cycle detection algorithms for directed and undirected graphs.

5. Implement bipartite graph detection algorithm.

6. Add shortest path algorithms (Dijkstra's, Bellman-Ford, Floyd-Warshall).

7. Implement minimum spanning tree algorithms (Kruskal's, Prim's).

8. Create strongly connected components algorithm (Kosaraju's, Tarjan's).

9. Implement graph isomorphism detection.

10. Add maximum flow algorithms (Ford-Fulkerson, Edmonds-Karp).

ADVANCED CHALLENGES:

1. Implement graph compression techniques
2. Create dynamic graph data structures
3. Build graph databases with query optimization
4. Implement graph neural network representations
5. Create distributed graph processing algorithms
6. Build graph visualization tools
7. Implement graph stream processing
8. Create graph pattern matching algorithms
9. Build graph clustering algorithms
10. Implement graph similarity measures

ALGORITHM APPLICATIONS:

1. Social network analysis and recommendations
2. Route planning and GPS navigation systems
3. Dependency resolution in package managers
4. Network flow and capacity planning
5. Circuit design and electronic systems
6. Compiler optimization and data flow analysis
7. Game AI pathfinding and decision trees
8. Web crawling and link analysis
9. Biological network analysis
10. Transportation and logistics optimization

SYSTEM DESIGN:

1. Design graph database system
2. Build recommendation engine using graphs
3. Create distributed graph processing framework
4. Design network monitoring system
5. Build fraud detection using graph analysis
"""
