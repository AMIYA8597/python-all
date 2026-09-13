"""
# ==============================================================================
# LABORATORY: MST VARIATIONS (SECOND-BEST & MAXIMUM SPANNING TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've mastered Kruskal, Prim, and Borůvka. They all output the absolute 
# mathematically perfect Minimum Spanning Tree (MST).
#
# But in real-world Engineering (like designing the physical backbone of the 
# internet for a country), relying on ONE single MST is a fatal flaw. 
# What happens if a backhoe physically cuts the primary fiber-optic line? 
# The country goes offline.
#
# You need Network Redundancy. You need to calculate the "Second-Best MST".
# 
# Theorem: The Second-Best MST must differ from the primary MST by exactly 
# ONE EDGE. 
# 
# Therefore, the algorithm is simple:
# 1. Compute the Primary MST.
# 2. Iterate through every wire in the Primary MST.
# 3. Temporarily ban that wire from existence.
# 4. Re-run Kruskal's algorithm on the remaining wires to find a "Backup Tree".
# 5. Keep track of all Backup Trees. The one with the lowest total cost is 
#    officially the Second-Best MST!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Maximum Spanning Trees (Max-ST).
# - Implement the Edge-Exclusion algorithm for the Second-Best MST.
# - Analyze the O(V * E) time complexity overhead.
#
# ==============================================================================
"""

from typing import List, Tuple
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DSU ENGINE (Recycled for Kruskal)
# ==============================================================================
class DSU:
    def __init__(self, size: int):
        self.parent = list(range(size))
    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j: return False
        self.parent[root_i] = root_j
        return True


# ==============================================================================
# 4. KRUSKAL WITH EDGE EXCLUSION
# ==============================================================================
def kruskal_excluding_edge(vertices: int, edges: List[Tuple[int, int, float]], excluded_edge: int) -> float:
    """
    Runs Kruskal's, but ignores the specific edge at index `excluded_edge`.
    Returns math.inf if a valid spanning tree cannot be formed.
    Note: Assumes `edges` is ALREADY SORTED (Optimization to prevent re-sorting).
    """
    dsu = DSU(vertices)
    mst_cost = 0
    edges_used = 0
    
    for i, (u, v, weight) in enumerate(edges):
        # BAN THIS SPECIFIC WIRE!
        if i == excluded_edge:
            continue
            
        if dsu.union(u, v):
            mst_cost += weight
            edges_used += 1
            if edges_used == vertices - 1:
                break
                
    # If we couldn't connect the graph without that wire, the backup fails!
    if edges_used != vertices - 1:
        return math.inf
        
    return mst_cost


# ==============================================================================
# 5. SECOND-BEST MST ENGINE (O(V * E log E))
# ==============================================================================
def second_best_mst(vertices: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, float]:
    """
    Finds the Primary MST and the Second-Best Backup MST.
    """
    # 1. Sort edges ONCE. (O(E log E))
    edges.sort(key=lambda x: x[2])
    
    # 2. Find the Primary MST and record WHICH edges we used!
    dsu = DSU(vertices)
    primary_cost = 0
    primary_edge_indices = []
    
    for i, (u, v, weight) in enumerate(edges):
        if dsu.union(u, v):
            primary_cost += weight
            primary_edge_indices.append(i)
            if len(primary_edge_indices) == vertices - 1:
                break
                
    # 3. Find the Second-Best MST
    # Loop over the exactly V-1 edges that form the Primary MST
    second_best_cost = math.inf
    
    for edge_index in primary_edge_indices:
        # Re-run Kruskal without this edge! (O(E) since it's already sorted)
        backup_cost = kruskal_excluding_edge(vertices, edges, edge_index)
        
        # Is this the cheapest backup tree we've seen so far?
        if backup_cost < second_best_cost:
            second_best_cost = backup_cost
            
    return primary_cost, second_best_cost


# ==============================================================================
# 6. MAXIMUM SPANNING TREE ENGINE
# ==============================================================================
def maximum_spanning_tree(vertices: int, edges: List[Tuple[int, int, float]]) -> float:
    """
    What if you want to find the MOST EXPENSIVE possible spanning tree?
    Just sort the edges in reverse (Descending)!
    """
    edges_descending = sorted(edges, key=lambda x: x[2], reverse=True)
    
    dsu = DSU(vertices)
    max_cost = 0
    edges_used = 0
    
    for u, v, weight in edges_descending:
        if dsu.union(u, v):
            max_cost += weight
            edges_used += 1
            if edges_used == vertices - 1:
                break
                
    return max_cost


def demonstrate_variations():
    section_header("Algorithm: MST Variations (Redundancy & Max)")
    
    vertices = 4
    edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    
    primary, secondary = second_best_mst(vertices, edges)
    
    print(f"Primary Minimum Spanning Tree Cost: ${primary}")
    print(f"Second-Best Backup MST Cost: ${secondary}")
    
    print("\nExecuting Maximum Spanning Tree...")
    max_st = maximum_spanning_tree(vertices, edges)
    print(f"Maximum Spanning Tree Cost: ${max_st}")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must the Second-Best MST differ from the Primary MST by exactly one edge?
   Answer: Graph theory dictates that if you take any spanning tree and add ONE new edge to it, you mathematically guarantee the creation of exactly one Cycle. To restore it to a spanning tree, you must remove exactly one edge from that newly formed cycle. Therefore, the transformation from the absolute best tree to the next-best tree always involves swapping exactly one old wire for exactly one new wire!

2. Why is the time complexity $O(V * E)$?
   Answer: We sort the edges once, which takes $O(E \\log E)$. The Primary MST uses exactly $V-1$ edges. In our loop, we temporarily delete one of those edges and re-run the Kruskal logic. Because the array is already sorted, re-running Kruskal takes strictly $O(E)$ time (assuming $O(1)$ DSU). Since we do this $V-1$ times, the loop takes $O(V \\times E)$. Total time: $O(E \\log E + VE)$.

3. Do MST algorithms work on Directed Graphs (One-Way streets)?
   Answer: NO. Kruskal, Prim, and Borůvka instantly crash and fail mathematically on Directed Graphs. A Spanning Tree on a Directed Graph is called an "Arborescence". Finding the Minimum Weight Arborescence requires a completely different, highly complex algorithm called "Edmonds' Algorithm" (or the Chu-Liu-Edmonds algorithm), which involves collapsing detected cycles into "super-nodes" and recursively modifying edge weights!
"""

if __name__ == "__main__":
    demonstrate_variations()
    print("\n[SUCCESS] Laboratory: MST Variations Completed.")
