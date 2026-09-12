"""
## A. Concept Name
Graph Algorithms Template for Competitive Programming

## B. Description
Graphs are one of the most frequently tested data structures in competitive programming and technical interviews. This module provides a complete template for representing graphs and executing standard graph algorithms like Traversal (BFS/DFS), Shortest Path (Dijkstra), Connectivity (Disjoint Set Union), and Topological Sorting.

## C. Learning Objectives
1. Understand Adjacency List representation of graphs.
2. Master Graph Traversals: Breadth-First Search (BFS) and Depth-First Search (DFS).
3. Implement Dijkstra's Algorithm for Single Source Shortest Path.
4. Utilize Disjoint Set Union (DSU) for cycle detection and dynamic connectivity.
5. Apply Topological Sorting for Directed Acyclic Graphs (DAGs).

## D. Concept Explanation
- Adjacency List: The most efficient way to store a sparse graph. O(V + E) space.
- BFS: Uses a queue. Explores neighbors layer by layer. Great for unweighted shortest paths.
- DFS: Uses a stack (or recursion). Explores deep into a path before backtracking.
- Dijkstra: Uses a priority queue (min-heap). Finds the shortest path in a weighted graph without negative edges.
- DSU (Union-Find): Tracks elements partitioned into disjoint subsets. Uses Path Compression and Union by Rank.
- Topological Sort: Orders nodes such that for every directed edge U->V, U comes before V. Uses indegrees (Kahn's Algorithm).

## E. Use Cases
- Network routing and mapping.
- Dependency resolution (e.g., package managers, task scheduling).
- Social network connections and friend suggestions.

## F. Intuition
Think of a graph like a map of a country. The cities are the vertices (nodes) and the roads connecting them are the edges. Algorithms like BFS help you find the city with the fewest stopovers, while Dijkstra's finds the path with the shortest physical distance.

## G. Visual Explanation
```text
      (1)
    0 --- 1
   /      | \
(4)      (2) (1)
 /        |   \
2 ------- 3 --- 4
   (1)
```
- Nodes (Vertices): 0, 1, 2, 3, 4
- Edges: (0,1), (0,2), (1,3), (1,4), (2,3)
- Weights are in parentheses.

## H. Formal Explanation
A graph G = (V, E) is defined by a set of vertices V and a set of edges E. Each edge connects a pair of vertices. In directed graphs, edges have a direction (u -> v). In weighted graphs, edges have a numerical weight.

## I. Data Structures / Memory Foundation
Adjacency List: A list (or array) of lists. `adj[u]` contains a list of tuples `(v, weight)` representing an edge from u to v. This requires O(V + E) memory, which is optimal for sparse graphs compared to an Adjacency Matrix (O(V^2)).

## J. Implementation & Examples
Below we provide highly optimized, class-based implementations with typing.

## K. Edge Cases
- Disconnected graphs: Some nodes cannot be reached from the starting node.
- Cycles: Directed or undirected cycles can cause infinite loops if nodes are not marked as visited.
- Negative weights: Dijkstra's algorithm will fail if the graph has negative edge weights (use Bellman-Ford instead).

## L. Trace (Step-by-Step)
BFS on graph: 0-1, 1-2, 1-3
1. Queue: [0], Visited: {0}
2. Pop 0, append neighbors 1. Queue: [1], Visited: {0, 1}
3. Pop 1, append neighbors 2, 3. Queue: [2, 3], Visited: {0, 1, 2, 3}
4. Pop 2, no unvisited neighbors. Queue: [3]
5. Pop 3, no unvisited neighbors. Queue: []

## M. Complexity Analysis
- BFS/DFS: Time O(V + E), Space O(V)
- Dijkstra: Time O((V + E) log V), Space O(V + E)
- Topological Sort: Time O(V + E), Space O(V)
- DSU: Find/Union Time Amortized O(α(V)) ≈ O(1), Space O(V)

## N. Common Mistakes
- Forgetting to mark a node as visited when using BFS/DFS.
- Initializing distances with 0 instead of infinity in Dijkstra's.
- Not checking for cycles before performing Topological Sorting.

## O. Common Confusions
- BFS vs DFS: Use BFS for shortest path in unweighted graphs. Use DFS for exploring all paths or topological sorting.
- Adjacency Matrix vs List: Always default to Adjacency List unless the graph is extremely dense (E ≈ V^2) and V is small (e.g., V ≤ 1000).

## P. When To Use
- BFS: Shortest path (unweighted), level-order traversal.
- DFS: Cycle detection, backtracking, strongly connected components.
- Dijkstra: Shortest path (weighted, non-negative).
- DSU: Kruskal's MST, dynamic connectivity, cycle detection in undirected graphs.
- Topological Sort: Task scheduling, dependency resolution in DAGs.

## Q. Alternatives
- Bellman-Ford: For shortest paths with negative weights (O(V*E)).
- Floyd-Warshall: All-pairs shortest path (O(V^3)).

## R. Best Practices
- Always use `sys.setrecursionlimit` for DFS in Python.
- Use `collections.deque` for queues instead of lists for O(1) popleft.
- Use `heapq` for the priority queue in Dijkstra's.

## S. Debugging
- Print the adjacency list to verify the graph was built correctly.
- Ensure 0-indexed vs 1-indexed nodes are handled properly based on the problem input.

## T. Memory Hook
- BFS = Broad (layer by layer).
- DFS = Deep (plunge to the bottom).
- DSU = Union of Sets.
- Dijkstra = Shortest Path (Priority Queue).

## U. Active Recall
1. What is the time complexity of Dijkstra's algorithm?
2. How does Kahn's algorithm detect cycles?
3. What is the purpose of path compression in DSU?

## V. Practice
- Implement cycle detection using BFS.
- Write a function to find the shortest path from a start node to an end node, returning the path itself (not just the distance).

## W. Interview Challenge
1. Explain why Dijkstra's algorithm fails when the graph contains negative edge weights. What algorithm should be used instead?
2. Modify the DSU implementation to keep track of the size of each disjoint component dynamically.
3. How can Topological Sorting be used to find the shortest path in a Directed Acyclic Graph (DAG) in O(V + E) time?

## X. Project Connection
In Machine Learning, graphs represent everything from neural network architectures (computation graphs) to social network interactions. Frameworks like PyTorch Geometric rely heavily on efficient graph representations (Adjacency Lists/Edge Lists) for Graph Neural Networks (GNNs).
"""

from collections import deque
import heapq
from typing import List, Tuple, Dict, Set, Optional

class Graph:
    def __init__(self, vertices: int, directed: bool = False):
        self.V = vertices
        self.directed = directed
        self.adj: List[List[Tuple[int, int]]] = [[] for _ in range(vertices)]
        
    def add_edge(self, u: int, v: int, weight: int = 1):
        """Adds an edge from u to v. For undirected, adds v to u as well."""
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def bfs(self, start: int) -> List[int]:
        """Breadth-First Search. Returns the order of visited nodes. Time: O(V + E)"""
        visited = [False] * self.V
        queue = deque([start])
        visited[start] = True
        traversal = []

        while queue:
            node = queue.popleft()
            traversal.append(node)

            for neighbor, _ in self.adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return traversal

    def dfs(self, start: int) -> List[int]:
        """Depth-First Search (Iterative). Returns the order of visited nodes. Time: O(V + E)"""
        visited = [False] * self.V
        stack = [start]
        traversal = []

        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                traversal.append(node)
                # Push neighbors (reversed for standard left-to-right visit order)
                for neighbor, _ in reversed(self.adj[node]):
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return traversal

    def dijkstra(self, start: int) -> List[int]:
        """
        Dijkstra's Algorithm for Shortest Path.
        Returns a list of shortest distances from 'start'. 
        Time: O((V + E) log V)
        """
        distances = [float('inf')] * self.V
        distances[start] = 0
        # Priority queue stores tuples of (distance, vertex)
        pq = [(0, start)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            # Optimization: If we found a shorter path already, skip
            if current_dist > distances[u]:
                continue

            for v, weight in self.adj[u]:
                distance = current_dist + weight
                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(pq, (distance, v))
                    
        return distances

    def topological_sort(self) -> List[int]:
        """
        Kahn's Algorithm for Topological Sorting (Requires DAG).
        Returns the sorted order, or empty list if a cycle exists.
        Time: O(V + E)
        """
        if not self.directed:
            raise ValueError("Topological sort is only for directed graphs.")
            
        in_degree = [0] * self.V
        for u in range(self.V):
            for v, _ in self.adj[u]:
                in_degree[v] += 1
                
        queue = deque([i for i in range(self.V) if in_degree[i] == 0])
        topo_order = []

        while queue:
            u = queue.popleft()
            topo_order.append(u)
            
            for v, _ in self.adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        if len(topo_order) != self.V:
            return [] # Cycle detected
        return topo_order

class DSU:
    """
    Disjoint Set Union (Union-Find) with Path Compression and Union by Rank.
    Time Complexity: Amortized O(alpha(V)) ~ O(1) per operation.
    """
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # Union by rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            self.components -= 1
            return True
        return False


# --- Example Usage and Tests ---
if __name__ == "__main__":
    # Test Graph Traversals
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    
    assert g.bfs(0) == [0, 1, 2, 3, 4]
    assert g.dfs(0) == [0, 1, 3, 4, 2]

    # Test Dijkstra
    g_weight = Graph(4)
    g_weight.add_edge(0, 1, 1)
    g_weight.add_edge(1, 2, 2)
    g_weight.add_edge(0, 2, 4)
    g_weight.add_edge(2, 3, 1)
    assert g_weight.dijkstra(0) == [0, 1, 3, 4]

    # Test Topological Sort
    g_dir = Graph(6, directed=True)
    g_dir.add_edge(5, 2)
    g_dir.add_edge(5, 0)
    g_dir.add_edge(4, 0)
    g_dir.add_edge(4, 1)
    g_dir.add_edge(2, 3)
    g_dir.add_edge(3, 1)
    topo = g_dir.topological_sort()
    assert len(topo) == 6
    
    # Test DSU
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(1, 2)
    assert dsu.find(0) == dsu.find(2)
    assert dsu.find(0) != dsu.find(3)
    assert dsu.components == 3

    print("All Graph algorithm tests passed!")
