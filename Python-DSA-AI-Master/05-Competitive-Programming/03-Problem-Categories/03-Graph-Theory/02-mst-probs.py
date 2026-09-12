"""
## A. Concept Name
Minimum Spanning Tree (MST) Problems

## B. Overview
A Minimum Spanning Tree (MST) of an edge-weighted undirected graph is a spanning tree 
whose weight (the sum of the weights of its edges) is no larger than the weight of any other spanning tree.
This file explores standard MST algorithms (Kruskal's and Prim's) and their applications in competitive programming.

## C. Learning Objectives
1. Understand the properties of Spanning Trees and Minimum Spanning Trees.
2. Implement Kruskal's Algorithm using a Disjoint Set Union (DSU) data structure.
3. Implement Prim's Algorithm using a Priority Queue.
4. Solve practical variations of MST problems, such as finding the 'Min Cost to Connect All Points'
   or variations like the 'Second Best MST'.

## D. Concept Explanations

Kruskal's Algorithm:
- Follows a greedy approach.
- Sorts all edges in non-decreasing order of their weight.
- Picks the smallest edge. Checks if it forms a cycle with the spanning tree formed so far 
  (using a Disjoint Set / Union-Find data structure). If a cycle is not formed, includes this edge.
- Time Complexity: O(E log E) or O(E log V)
- Space Complexity: O(V) for the Union-Find structure.

Prim's Algorithm:
- Also a greedy algorithm.
- Starts with an empty spanning tree and maintains two sets of vertices: vertices included in MST 
  and vertices not yet included.
- At every step, it considers all the edges that connect the two sets, and picks the minimum weight edge.
- Implemented optimally using a Min-Heap.
- Time Complexity: O(E log V)
- Space Complexity: O(V + E) for graph representation and heap.

## X. Project Connection
- Network design (telecommunication, electrical grids).
- Approximation algorithms for NP-hard problems (like Traveling Salesperson Problem).
- Cluster analysis in machine learning.
"""

from typing import List, Tuple, Dict, Set
import heapq


class UnionFind:
    """
    Disjoint Set Union (DSU) or Union-Find data structure with 
    path compression and union by rank.
    """
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Unions the sets containing i and j.
        Returns True if a successful union occurred, False if they are already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False

        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
            
        return True


def kruskal_mst(vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Computes the Minimum Spanning Tree using Kruskal's Algorithm.
    
    Args:
        vertices: The number of vertices (0 to vertices-1).
        edges: A list of edges represented as (weight, u, v).
        
    Returns:
        A tuple containing the total weight of the MST and a list of the edges in the MST.
        Returns (-1, []) if no MST exists (graph is disconnected).
    """
    # Sort edges by weight
    edges.sort()
    
    uf = UnionFind(vertices)
    mst_weight = 0
    mst_edges = []
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst_weight += weight
            mst_edges.append((weight, u, v))
            if len(mst_edges) == vertices - 1:
                break
                
    if len(mst_edges) != vertices - 1:
        return -1, []  # Disconnected graph
        
    return mst_weight, mst_edges


def prim_mst(vertices: int, graph: List[List[Tuple[int, int]]]) -> int:
    """
    Computes the cost of the Minimum Spanning Tree using Prim's Algorithm.
    
    Args:
        vertices: The number of vertices.
        graph: Adjacency list representing the graph `graph[u] = [(weight, v), ...]`.
        
    Returns:
        The total weight of the MST, or -1 if the graph is disconnected.
    """
    if vertices == 0: return 0
    
    # Priority queue stores (weight, vertex)
    pq = [(0, 0)]
    visited = [False] * vertices
    mst_weight = 0
    edges_used = 0
    
    while pq and edges_used < vertices:
        weight, u = heapq.heappop(pq)
        
        if visited[u]:
            continue
            
        visited[u] = True
        mst_weight += weight
        edges_used += 1
        
        for edge_weight, v in graph[u]:
            if not visited[v]:
                heapq.heappush(pq, (edge_weight, v))
                
    if edges_used != vertices:
        return -1
        
    return mst_weight


def min_cost_connect_points(points: List[List[int]]) -> int:
    """
    Problem: Min Cost to Connect All Points (LeetCode 1584)
    You are given an array points representing integer coordinates of some points on a 2D-plane, 
    where points[i] = [xi, yi].
    
    The cost of connecting two points [xi, yi] and [xj, yj] is the Manhattan distance between them.
    Return the minimum cost to make all points connected.
    
    This is effectively finding the MST of a complete graph.
    """
    n = len(points)
    
    # Using Prim's algorithm for dense graph (Complete Graph)
    # We can optimize space by not building the full adjacency list.
    
    visited = [False] * n
    # min_dist array acts like our priority queue but is optimized for dense graphs. O(V^2) Prim's.
    min_dist = [float('inf')] * n
    min_dist[0] = 0
    
    total_cost = 0
    
    for _ in range(n):
        # Find the unvisited vertex with the minimum distance
        u = -1
        min_val = float('inf')
        for i in range(n):
            if not visited[i] and min_dist[i] < min_val:
                min_val = min_dist[i]
                u = i
                
        visited[u] = True
        total_cost += min_val
        
        # Update distances to all other unvisited vertices
        for v in range(n):
            if not visited[v]:
                dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if dist < min_dist[v]:
                    min_dist[v] = dist
                    
    return total_cost


def _run_tests():
    """Execute tests to ensure correctness."""
    
    # 1. Kruskal's Test
    v = 4
    edges = [
        (10, 0, 1),
        (6, 0, 2),
        (5, 0, 3),
        (15, 1, 3),
        (4, 2, 3)
    ]
    cost, mst_e = kruskal_mst(v, edges)
    assert cost == 19
    
    # 2. Prim's Test
    graph = [
        [(10, 1), (6, 2), (5, 3)],
        [(10, 0), (15, 3)],
        [(6, 0), (4, 3)],
        [(5, 0), (15, 1), (4, 2)]
    ]
    cost = prim_mst(v, graph)
    assert cost == 19
    
    # 3. Min Cost Connect Points Test
    points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
    assert min_cost_connect_points(points) == 20

if __name__ == '__main__':
    print("Running MST algorithm tests...")
    _run_tests()
    print("All tests passed!")
