"""
Minimum Spanning Tree - Prim's Algorithm

Learning Objectives:
1. Understand the concept of Minimum Spanning Tree (MST).
2. Learn how Prim's algorithm builds an MST by greedily picking the cheapest edge.
3. Implement Prim's algorithm using a priority queue (min-heap) for optimal performance.
4. Analyze the time and space complexity of Prim's algorithm.

Concept Explanation:
A Minimum Spanning Tree (MST) or minimum weight spanning tree is a subset of the edges of a 
connected, edge-weighted undirected graph that connects all the vertices together, without any cycles 
and with the minimum possible total edge weight.

Prim's algorithm operates by building this tree one vertex at a time, from an arbitrary starting vertex,
at each step adding the cheapest possible connection from the tree to another vertex.

Industry Use Cases:
- Network design (e.g., telecommunications, computer networks, electrical grids).
- Approximation algorithms for NP-hard problems like the Traveling Salesperson Problem (TSP).
- Cluster analysis.

Common Mistakes:
- Forgetting that the graph must be undirected and connected.
- Not keeping track of visited nodes properly, leading to cycles.
- Pushing all adjacent edges into the heap without checking if the destination is already visited, 
  which can lead to unnecessary heap operations (though still correct if handled upon popping).
"""

import heapq
from typing import Dict, List, Tuple, Set

def prim_basic(graph: Dict[int, List[Tuple[int, int]]], start_node: int) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Basic implementation of Prim's Algorithm using a priority queue.
    
    Args:
        graph: Adjacency list representation of the graph {node: [(neighbor, weight)]}
        start_node: The node to start the MST from.
        
    Returns:
        A tuple containing (total_cost, list_of_edges_in_mst)
        where list_of_edges_in_mst contains tuples of (u, v, weight).
    """
    mst_edges = []
    visited: Set[int] = set()
    min_heap: List[Tuple[int, int, int]] = []  # (weight, source, destination)
    total_cost = 0

    # Start with the initial node. Mark it as visited and add its edges.
    visited.add(start_node)
    for neighbor, weight in graph.get(start_node, []):
        heapq.heappush(min_heap, (weight, start_node, neighbor))

    while min_heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(min_heap)

        if v in visited:
            continue

        # Add the edge to MST
        visited.add(v)
        total_cost += weight
        mst_edges.append((u, v, weight))

        # Add adjacent edges of the newly added vertex
        for neighbor, edge_weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, v, neighbor))

    # Check if a spanning tree was possible
    if len(visited) != len(graph):
        return -1, []  # Graph is disconnected

    return total_cost, mst_edges


class PrimsAlgorithm:
    """
    Professional grade implementation of Prim's Algorithm.
    Supports generic node types and handles disconnected components elegantly.
    """
    def __init__(self, vertices: List[str]):
        self.vertices = vertices
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {v: [] for v in vertices}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Adds an undirected edge to the graph."""
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append((v, weight))
            self.adj_list[v].append((u, weight))
        else:
            raise ValueError("Vertices must exist in the graph.")

    def find_mst(self) -> Tuple[float, List[Tuple[str, str, float]]]:
        """
        Finds the Minimum Spanning Tree.
        Returns:
            Tuple of (total weight, list of edges).
        """
        if not self.vertices:
            return 0.0, []

        start_node = self.vertices[0]
        visited: Set[str] = {start_node}
        edges: List[Tuple[float, str, str]] = []
        mst: List[Tuple[str, str, float]] = []
        total_weight = 0.0

        for neighbor, weight in self.adj_list[start_node]:
            heapq.heappush(edges, (weight, start_node, neighbor))

        while edges and len(visited) < len(self.vertices):
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                visited.add(v)
                mst.append((u, v, weight))
                total_weight += weight
                for neighbor, next_weight in self.adj_list[v]:
                    if neighbor not in visited:
                        heapq.heappush(edges, (next_weight, v, neighbor))
                        
        if len(visited) < len(self.vertices):
            raise Exception("Graph is disconnected; no MST exists.")

        return total_weight, mst

"""
Complexity Analysis:
- Time Complexity: O(E log V) where E is the number of edges and V is the number of vertices.
  Each edge is pushed onto the priority queue at most once. Extracting from the min-heap takes O(log E) which is bounded by O(log V^2) = O(log V).
- Space Complexity: O(V + E) for the adjacency list and O(E) for the priority queue. Overall space complexity is O(V + E).

Interview Challenge:
Question: Can Prim's algorithm be modified to find the Maximum Spanning Tree?
Answer: Yes. We can simply negate the edge weights before running the standard Prim's algorithm, or use a max-heap instead of a min-heap to always greedily select the edge with the highest weight.
"""

if __name__ == "__main__":
    print("Testing Basic Prim's Algorithm...")
    # Graph representation: A(0), B(1), C(2), D(3)
    graph = {
        0: [(1, 10), (2, 6), (3, 5)],
        1: [(0, 10), (3, 15)],
        2: [(0, 6), (3, 4)],
        3: [(0, 5), (1, 15), (2, 4)]
    }
    cost, mst = prim_basic(graph, 0)
    assert cost == 19
    print(f"Basic Prim's cost: {cost}, edges: {mst}")

    print("Testing Professional Prim's Algorithm...")
    prim = PrimsAlgorithm(['A', 'B', 'C', 'D'])
    prim.add_edge('A', 'B', 10)
    prim.add_edge('A', 'C', 6)
    prim.add_edge('A', 'D', 5)
    prim.add_edge('B', 'D', 15)
    prim.add_edge('C', 'D', 4)
    
    prof_cost, prof_mst = prim.find_mst()
    assert prof_cost == 19.0
    print(f"Professional Prim's cost: {prof_cost}, edges: {prof_mst}")
    print("All tests passed successfully.")
