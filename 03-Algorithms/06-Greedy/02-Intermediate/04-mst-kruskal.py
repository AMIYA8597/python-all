"""
# ==============================================================================
# LABORATORY: KRUSKAL'S MST (GREEDY DISJOINT SET)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are laying fiber optic cables to connect 100 cities. 
# Cable costs money. You want to connect every single city using the absolute 
# minimum total length of cable.
#
# This is the "Minimum Spanning Tree" (MST) problem.
# - "Tree": A graph with no cycles. (If there's a cycle, you bought redundant cable!)
# - "Spanning": It connects EVERY vertex in the graph.
#
# In 1956, Joseph Kruskal invented a beautiful, pure Greedy algorithm:
# 1. Look at EVERY possible cable you could buy.
# 2. Sort them all by price (cheapest first).
# 3. Buy the absolute cheapest cable available. 
# 4. If buying a cable forms a closed Loop (Cycle) between cities that are 
#    ALREADY connected, throw it in the trash!
# 5. Stop when you have V-1 cables (which perfectly connects V cities).
#
# How do you instantly detect a Cycle?
# By using the legendary "Disjoint Set" (Union-Find) data structure!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Greedy Edge-Picking Heuristic.
# - Master the Disjoint Set (Union-Find) with Path Compression.
# - Understand why an MST requires exactly V-1 edges.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DISJOINT SET UNION (UNION-FIND)
# ==============================================================================
class DisjointSet:
    def __init__(self, vertices: int):
        # Initially, every vertex is its own "parent" (its own independent island).
        self.parent = {i: i for i in range(vertices)}
        # Rank is used to keep the tree flat when merging.
        self.rank = {i: 0 for i in range(vertices)}
        
    def find(self, i: int) -> int:
        """
        Finds the absolute "Root" of the island this vertex belongs to.
        Uses PATH COMPRESSION to flatten the tree for O(alpha N) amortized time!
        """
        if self.parent[i] == i:
            return i
            
        # Point this node DIRECTLY to the root to speed up all future queries!
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, u: int, v: int) -> bool:
        """
        Attempts to merge two islands. 
        Returns True if successful. 
        Returns False if they were ALREADY connected (A CYCLE!)
        """
        root_u = self.find(u)
        root_v = self.find(v)
        
        # If they share the exact same root, they are already connected!
        if root_u == root_v:
            return False
            
        # Merge the smaller island into the larger island (Union by Rank).
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            # If they are exactly the same size, pick one and promote it.
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
            
        return True


# ==============================================================================
# 4. KRUSKAL'S GREEDY ALGORITHM
# ==============================================================================
def kruskal_mst(vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    edges: List of (weight, node_u, node_v)
    
    Time Complexity: O(E log E) for the sorting. DSU is effectively O(1).
    Space Complexity: O(V) for the Disjoint Set.
    """
    
    # 1. THE GREEDY HEURISTIC
    # Sort all edges strictly by their Weight (Cheapest first!)
    # Python's `sort` automatically sorts Tuples by their first element (Weight).
    edges.sort()
    
    dsu = DisjointSet(vertices)
    mst_edges = []
    total_cost = 0
    
    # 2. THE GREEDY LOOP
    for edge in edges:
        weight, u, v = edge
        
        # --- CYCLE DETECTION ---
        # Can we connect node `u` and node `v`?
        # `dsu.union` will return False if they are already connected!
        if dsu.union(u, v):
            
            # We successfully connected two separate islands!
            # Lock the cable in.
            mst_edges.append(edge)
            total_cost += weight
            
            # 3. TERMINATION CONDITION
            # A Spanning Tree of V vertices is mathematically guaranteed to have 
            # EXACTLY V - 1 edges. Once we hit it, we can terminate early!
            if len(mst_edges) == vertices - 1:
                break
                
    return total_cost, mst_edges


def demonstrate_kruskal():
    section_header("Algorithm: Kruskal's Minimum Spanning Tree")
    
    vertices = 6
    # Edges format: (weight, node_u, node_v)
    # The nodes are 0-indexed (0 to 5)
    edges = [
        (4, 0, 1), (4, 0, 2), (2, 1, 2),
        (3, 1, 3), (2, 2, 3), (4, 2, 4),
        (2, 2, 5), (3, 3, 4), (3, 4, 5)
    ]
    
    print(f"Graph with {vertices} Vertices and {len(edges)} Edges.")
    print("Unsorted Edges:")
    for e in edges:
        print(f" Node {e[1]} <-> Node {e[2]} (Cost: ${e[0]})")
        
    print("\nExecuting Kruskal's Greedy DSU Algorithm...")
    total_cost, mst = kruskal_mst(vertices, edges.copy())
    
    print(f"\nMinimum Spanning Tree Cost: ${total_cost}")
    print(f"Edges Used: {len(mst)} (Mathematically V-1, which is {vertices-1})")
    
    for e in mst:
        print(f" -> Connect Node {e[1]} and {e[2]} (Cost: ${e[0]})")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Kruskal's Algorithm use a Disjoint Set instead of DFS for cycle detection?
   Answer: Running a DFS to check for cycles takes $O(V + E)$ time. If you run a DFS inside a loop of $E$ edges, your total time becomes $O(E \\times (V+E))$, which is incredibly slow ($O(V^3)$ for dense graphs). The Disjoint Set (Union-Find) with Path Compression performs cycle checks in Inverse Ackermann time $\\alpha(N)$, which is mathematically indistinguishable from $O(1)$. This drops the loop time to $O(E)$, making the Sorting step $O(E \\log E)$ the only bottleneck.

2. What is "Path Compression" in the Disjoint Set?
   Answer: Look at `self.parent[i] = self.find(self.parent[i])`. If node 5 points to 4, 4 points to 3, and 3 points to the Root 1, calling `find(5)` requires 3 hops. But as the recursion returns, it overwrites the parent pointer so 5 points DIRECTLY to 1, and 4 points DIRECTLY to 1. The tree is permanently flattened. The next time you call `find(5)`, it takes 1 single hop!

3. Kruskal's vs Prim's Algorithm. When to use which?
   Answer: Both are Greedy MST algorithms. Kruskal's sorts all edges globally ($O(E \\log E)$), making it phenomenal for "Sparse Graphs" (lots of nodes, very few edges). Prim's Algorithm grows a single tree locally using a Min-Heap ($O(E \\log V)$). Prim's is vastly superior for "Dense Graphs" (where every node is connected to almost every other node) because it doesn't have to sort the massive global edge list.
"""

if __name__ == "__main__":
    demonstrate_kruskal()
    print("\n[SUCCESS] Laboratory: Kruskal's Algorithm Completed.")
