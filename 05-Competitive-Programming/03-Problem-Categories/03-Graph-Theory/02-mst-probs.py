"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (MINIMUM SPANNING TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are an engineer at AT&T. You need to connect 100 cities with fiber-optic 
# cables so they all share the same internet network.
# Laying cable costs money. The cost depends on the distance between cities.
#
# You do NOT want to connect every city to every other city (too expensive).
# You just need a "Tree" (no cycles) that "Spans" (connects) all 100 cities, 
# ensuring the total cost of all the cables is the mathematically lowest 
# possible amount.
#
# This is the Minimum Spanning Tree (MST) problem.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Kruskal's Algorithm (Greedy Edge Sorting + DSU).
# - Understand Prim's Algorithm (Node Expansion + Priority Queue).
#
# ==============================================================================
"""

import heapq

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KRUSKAL'S ALGORITHM (O(E log E))
# ==============================================================================
class DSU:
    """Helper class for Kruskal's Algorithm"""
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.size = [1] * size
        
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]
        
    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False # Cycle detected!
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        return True

def kruskal(n: int, edges: list[list[int]]) -> int:
    """
    Finds the cost of the Minimum Spanning Tree using Kruskal's.
    Time Complexity: O(E log E) because of sorting the edges!
    """
    # 1. Sort all edges from Cheapest to Most Expensive! (Greedy choice)
    edges.sort(key=lambda x: x[2])
    
    dsu = DSU(n)
    mst_cost = 0
    edges_used = 0
    
    # 2. Iterate through the cheapest edges
    for u, v, weight in edges:
        # If joining U and V does NOT create a Cycle (DSU checks this in O(1)!):
        if dsu.union(u, v):
            mst_cost += weight
            edges_used += 1
            
            # A Spanning Tree on N nodes always has exactly (N - 1) edges.
            # Once we hit N - 1, we can mathematically stop early!
            if edges_used == n - 1:
                break
                
    return mst_cost if edges_used == n - 1 else -1

def demonstrate_kruskal():
    section_header("Kruskal's Algorithm (Edge-Based)")
    
    # 4 Nodes: 0, 1, 2, 3
    # Edges: [u, v, weight]
    edges = [
        [0, 1, 1], # Cheap!
        [1, 3, 3],
        [0, 2, 4],
        [2, 3, 1], # Cheap!
        [1, 2, 2]
    ]
    
    cost = kruskal(4, edges)
    print(f"Kruskal's Minimum Spanning Tree Cost: {cost}")
    print("\nWhy it works: It blindly picks the absolute cheapest cables in the world, ")
    print("and relies on the DSU to reject any cable that forms a redundant cycle!")


# ==============================================================================
# 4. PRIM'S ALGORITHM (O(E log V))
# ==============================================================================
from collections import defaultdict

def prim(n: int, edges: list[list[int]]) -> int:
    """
    Finds the cost of the Minimum Spanning Tree using Prim's.
    Time Complexity: O(E log V) because of the Priority Queue.
    """
    # 1. Build Adjacency List
    adj = defaultdict(list)
    for u, v, weight in edges:
        adj[u].append((weight, v))
        adj[v].append((weight, u)) # Undirected Graph!
        
    # 2. Initialize Data Structures
    visited = set()
    mst_cost = 0
    
    # Priority Queue stores (weight, node)
    # Start arbitrarily from Node 0 with cost 0
    pq = [(0, 0)]
    
    # 3. Expand the Tree
    while pq and len(visited) < n:
        weight, u = heapq.heappop(pq)
        
        # If we already connected this node to our network, skip it!
        if u in visited:
            continue
            
        # Officially add it to the network!
        visited.add(u)
        mst_cost += weight
        
        # Look at all possible cables leaving this new node
        for edge_weight, v in adj[u]:
            # If the neighbor is NOT yet in our network, add the cable to the heap!
            if v not in visited:
                heapq.heappush(pq, (edge_weight, v))
                
    return mst_cost if len(visited) == n else -1

def demonstrate_prim():
    section_header("Prim's Algorithm (Node-Based)")
    
    edges = [
        [0, 1, 1],
        [1, 3, 3],
        [0, 2, 4],
        [2, 3, 1],
        [1, 2, 2]
    ]
    
    cost = prim(4, edges)
    print(f"Prim's Minimum Spanning Tree Cost: {cost}")
    print("\nWhy it works: It starts at Node 0, and slowly expands its territory ")
    print("like a mold, always choosing the cheapest adjacent cable to eat next.")


def run_all_labs():
    demonstrate_kruskal()
    demonstrate_prim()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the philosophical difference in the Greedy choice between Kruskal's Algorithm and Prim's Algorithm.
   Answer: Kruskal is "Edge-Centric". It looks at the global graph, completely shatters it into individual edges, sorts all edges by weight, and blindly pulls the absolute cheapest edge from anywhere in the world, slowly gluing the graph back together using a DSU to prevent cycles. Prim is "Node-Centric". It acts like an infection. It starts at a single root node and evaluates only the edges directly touching its currently infected territory. It uses a Min-Heap to select the absolute cheapest adjacent edge, expanding its territory organically into a single contiguous tree.

2. Why is the Disjoint Set Union (DSU) strictly mandatory for implementing Kruskal's algorithm, but not needed for Prim's?
   Answer: Kruskal picks edges randomly from anywhere in the global graph. It might pick an edge in New York, then an edge in California. Because the components are disjoint and floating everywhere, it needs a lightning-fast mathematical way to check "If I connect these two cities, does it form a redundant circle (Cycle)?" DSU answers this in $O(1)$ time. Prim starts at one central node and expands outward contiguously. It mathematically guarantees it never forms a cycle simply by keeping a `visited` set of nodes already inside the territory. If the Min-Heap suggests a cable that points to a `visited` node, Prim trivially discards it.

3. Which algorithm should you choose: Kruskal or Prim?
   Answer: In competitive programming, **Kruskal** is the undisputed king. Why? Because the DSU template is usually pre-written in a competitive programmer's snippet library, making Kruskal incredibly short and bug-free to type (literally just `sort()` + a loop). Furthermore, if the graph is Sparse (very few edges, $E \approx V$), sorting the edges takes almost zero time. Prim is generally only preferred in extremely Dense graphs ($E \approx V^2$), where sorting $V^2$ edges would be computationally punishing, and Prim's array-based implementation mathematically outperforms it.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Minimum Spanning Trees Completed.")
