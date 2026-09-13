"""
# ==============================================================================
# LABORATORY: MINIMUM SPANNING TREES (MST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dijkstra's Algorithm finds the cheapest path from Node A to Node B. 
# But what if you are the government, and you need to build a power grid that 
# connects ALL 50 cities in your state? You don't care about the fastest route 
# between two specific cities; you care about the absolute CHEAPEST total cost 
# to ensure every city is connected to the network.
# 
# This is the "Minimum Spanning Tree" (MST) problem. 
# A Spanning Tree is a subset of edges that connects all vertices without any 
# cycles. The *Minimum* Spanning Tree is the one with the lowest total edge weight.
# There are two legendary algorithms to solve this: Prim's and Kruskal's.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Shortest Path (Dijkstra) and MST.
# - Implement Prim's Algorithm using a Min-Heap (O(E log V)).
# - Implement Kruskal's Algorithm using Union-Find (O(E log E)).
#
# ==============================================================================
"""

import heapq
from typing import List, Tuple, Dict
from collections import defaultdict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PRIM'S ALGORITHM
# ==============================================================================
def prims_algorithm(num_vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Prim's algorithm builds the MST starting from a single node and growing outwards.
    It uses a Min-Heap to always select the absolute cheapest edge that connects 
    a "known" node to an "unknown" node.
    """
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
        
    # Track which nodes are already in our MST
    visited = set()
    mst_edges = []
    total_cost = 0
    
    # Priority Queue: (weight, current_node, parent_node)
    # We start arbitrarily at Node 0. It has no parent (-1) and cost 0.
    pq = [(0, 0, -1)]
    
    while pq and len(visited) < num_vertices:
        weight, node, parent = heapq.heappop(pq)
        
        # If this node is already in the MST, this edge is useless (creates a cycle)
        if node in visited:
            continue
            
        # Officially add this node and edge to the MST
        visited.add(node)
        total_cost += weight
        if parent != -1: # Ignore the initial artificial edge
            mst_edges.append((parent, node, weight))
            
        # Discover all outgoing edges from this newly added node
        for next_weight, neighbor in adj[node]:
            if neighbor not in visited:
                # Push them to the priority queue
                heapq.heappush(pq, (next_weight, neighbor, node))
                
    # If the graph was disconnected, we can't build a full MST
    if len(visited) != num_vertices:
        return -1, []
        
    return total_cost, mst_edges

def demonstrate_prims():
    section_header("Algorithm: Prim's Algorithm (Min-Heap)")
    
    # Square with a diagonal
    # 0 --(1)-- 1
    # |       / |
    # (4)  (2) (5)
    # |   /     |
    # 3 --(3)-- 2
    
    edges = [
        (0, 1, 1),
        (0, 3, 4),
        (1, 2, 5),
        (1, 3, 2),
        (2, 3, 3)
    ]
    
    cost, mst = prims_algorithm(4, edges)
    
    print(f"Total Minimum Cost to connect all cities: {cost}")
    print("Edges used in the Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"  City {u} <--> City {v} (Cost: {w})")


# ==============================================================================
# 4. KRUSKAL'S ALGORITHM
# ==============================================================================
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False # Cycle detected!
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

def kruskals_algorithm(num_vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Kruskal's algorithm doesn't grow outward from a single point. 
    It sorts ALL edges globally by weight, and aggressively adds the absolute 
    cheapest edges anywhere in the graph, as long as they don't create a cycle!
    It uses Union-Find to instantly detect cycles.
    """
    # 1. Sort all edges globally by weight (O(E log E))
    edges.sort(key=lambda x: x[2])
    
    uf = UnionFind(num_vertices)
    mst_edges = []
    total_cost = 0
    
    # 2. Iterate through the sorted edges
    for u, v, weight in edges:
        # 3. Use Union-Find to see if adding this edge creates a cycle
        if uf.union(u, v):
            # If it doesn't create a cycle, add it to the MST!
            mst_edges.append((u, v, weight))
            total_cost += weight
            
            # Optimization: The MST is complete when we have exactly V - 1 edges
            if len(mst_edges) == num_vertices - 1:
                break
                
    if len(mst_edges) != num_vertices - 1:
        return -1, []
        
    return total_cost, mst_edges

def demonstrate_kruskals():
    section_header("Algorithm: Kruskal's Algorithm (Union-Find)")
    
    # Same graph as before
    edges = [
        (0, 1, 1),
        (0, 3, 4),
        (1, 2, 5),
        (1, 3, 2),
        (2, 3, 3)
    ]
    
    print("Kruskal sorts all edges globally first:")
    edges_sorted = sorted(edges, key=lambda x: x[2])
    for u, v, w in edges_sorted:
        print(f"  Edge ({u}, {v}) Cost: {w}")
        
    print("\nThen it tries to add them in order, skipping any that cause cycles using Union-Find.\n")
    
    cost, mst = kruskals_algorithm(4, edges)
    
    print(f"Total Minimum Cost to connect all cities: {cost}")
    print("Edges used in the Minimum Spanning Tree:")
    for u, v, w in mst:
        print(f"  City {u} <--> City {v} (Cost: {w})")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Dijkstra and Prim's algorithm?
   Answer: Structurally, they are almost identical (both use a Min-Heap). However, Dijkstra sorts the heap by the TOTAL distance from the start node. Prim's sorts the heap purely by the LOCAL weight of the edge itself. Dijkstra optimizes routing; Prim's optimizes global network cost.

2. When should you use Kruskal's vs Prim's algorithm?
   Answer: Kruskal's requires sorting all edges globally taking O(E log E) time. Prim's takes O(E log V) using a heap. If the graph is sparse (very few edges), Kruskal's is often simpler and faster in practice. If the graph is extremely dense (e.g., E approaches V^2), Prim's is mathematically faster.

3. Why do we stop Kruskal's algorithm early when we reach V - 1 edges?
   Answer: A mathematical property of trees states that a fully connected tree with V vertices ALWAYS contains exactly V - 1 edges. Any additional edge would mathematically guarantee the creation of a cycle.
"""

if __name__ == "__main__":
    demonstrate_prims()
    demonstrate_kruskals()
    print("\n[SUCCESS] Laboratory: Minimum Spanning Trees Completed.")
