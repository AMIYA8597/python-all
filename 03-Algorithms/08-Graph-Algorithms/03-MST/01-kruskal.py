"""
# ==============================================================================
# LABORATORY: KRUSKAL'S MST & UNION-FIND (DISJOINT SET UNION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Minimum Spanning Tree (MST) is a subset of a graph that connects all the 
# vertices together without any cycles, using the absolute minimum total edge weight.
# If you are laying fiber-optic internet cables between 10 cities, you want them 
# all connected using the least amount of copper wire.
#
# Kruskal's algorithm is a Greedy algorithm. 
# 1. Sort all the edges in the world from cheapest to most expensive.
# 2. Iterate through them. If an edge connects two cities that aren't already 
#    connected, buy the cable!
# 3. If an edge creates a CYCLE (e.g., A is already connected to B through C, 
#    so buying a direct cable from A to B is a waste of money), discard it!
#
# But how do you mathematically detect a cycle in O(1) time? 
# If you run a DFS every time you evaluate a wire, the algorithm degrades to O(E * V).
#
# The solution is one of the most beautiful data structures in Computer Science:
# The Disjoint Set Union (DSU), also known as Union-Find.
#
# DSU tracks who belongs to which "Island". 
# By using "Path Compression" and "Union by Size", checking if two cities are 
# on the same island takes O(α(V)) time. `α` is the Inverse Ackermann Function, 
# which grows so inconceivably slowly that for all physical numbers in the universe, 
# it evaluates to $\le 4$. It is effectively O(1).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a professional-grade DSU class (Union-Find).
# - Master Path Compression (the O(α) optimization).
# - Assemble Kruskal's algorithm on top of the DSU engine.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DISJOINT SET UNION (UNION-FIND ENGINE)
# ==============================================================================
class DSU:
    def __init__(self, size: int):
        # Initially, every node is its own boss (parent is itself)
        self.parent = list(range(size))
        # We track the "size" of each island to keep trees shallow
        self.size = [1] * size
        
    def find(self, i: int) -> int:
        """
        Finds the absolute Supreme Leader (Root) of node `i`.
        Includes PATH COMPRESSION optimization.
        """
        # If the node is NOT its own boss...
        if self.parent[i] != i:
            # We recursively find the true boss.
            # PATH COMPRESSION: We instantly update this node's parent to point 
            # DIRECTLY to the Supreme Leader! This flattens the tree completely, 
            # ensuring all future lookups are O(1).
            self.parent[i] = self.find(self.parent[i])
            
        return self.parent[i]
        
    def union(self, i: int, j: int) -> bool:
        """
        Connects the islands containing `i` and `j`.
        Returns False if they were ALREADY on the same island (Cycle Detected!).
        Includes UNION BY SIZE optimization.
        """
        # Find the Supreme Leaders of both islands
        root_i = self.find(i)
        root_j = self.find(j)
        
        # If they share the exact same boss, they are already connected!
        if root_i == root_j:
            return False # CYCLE! Do not buy this cable!
            
        # UNION BY SIZE
        # We always attach the smaller island to the larger island. 
        # This prevents the tree from becoming a long, spindly linked list, 
        # guaranteeing O(log N) depth even without Path Compression.
        if self.size[root_i] < self.size[root_j]:
            # Island J is bigger. J absorbs I.
            self.parent[root_i] = root_j
            self.size[root_j] += self.size[root_i]
        else:
            # Island I is bigger (or equal). I absorbs J.
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            
        return True


# ==============================================================================
# 4. KRUSKAL'S ALGORITHM (O(E log E))
# ==============================================================================
def kruskals_mst(vertices: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Time Complexity: O(E log E) for the sorting step. The DSU operations are O(1).
    Space Complexity: O(V) for the DSU arrays.
    """
    # 1. SORT ALL EDGES (The Greedy Step)
    # Sort strictly by the edge weight (the 3rd element in the tuple)
    edges.sort(key=lambda x: x[2])
    
    dsu = DSU(vertices)
    mst_cost = 0
    mst_edges = []
    
    # 2. ITERATE AND UNION
    for u, v, weight in edges:
        # If union() returns True, it means they were on different islands.
        # We successfully bought the cable and merged the islands!
        if dsu.union(u, v):
            mst_cost += weight
            mst_edges.append((u, v))
            
            # Optimization: A spanning tree for V nodes has exactly V-1 edges.
            # We can break early!
            if len(mst_edges) == vertices - 1:
                break
                
    # Edge case: If we finished the loop but we don't have V-1 edges, 
    # the graph was physically disconnected! A full spanning tree is impossible.
    if len(mst_edges) != vertices - 1:
        raise ValueError("Graph is disconnected. No valid MST exists.")
        
    return mst_cost, mst_edges


def demonstrate_kruskal():
    section_header("Algorithm: Kruskal's Minimum Spanning Tree")
    
    vertices = 4
    # (u, v, weight)
    edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    
    print("Available Cables to buy:")
    for u, v, w in edges: print(f" {u} <-> {v} (Cost: ${w})")
        
    print("\nExecuting Kruskal's Greedy Algorithm with DSU...")
    cost, mst = kruskals_mst(vertices, edges)
    
    print(f"\nMinimum Cost to connect all cities: ${cost}")
    print("Cables purchased:")
    for u, v in mst:
        print(f" -> Connect {u} and {v}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Path Compression" in a Disjoint Set Union?
   Answer: When you call `find(x)`, you traverse up the tree: $x \\to parent(x) \\to grandparent(x) \\to Root$. Without path compression, the next time you call `find(x)`, you have to do the exact same traversal. With path compression, on the way back down the recursion, you set `parent[x] = Root` for EVERY node in the chain. The tree instantly flattens to a depth of 1. Future lookups take strictly $O(1)$ time!

2. Why is the time complexity $O(E \\log E)$?
   Answer: The absolute bottleneck of Kruskal's Algorithm is Step 1: Sorting the edge list. Sorting an array of $E$ elements takes $O(E \\log E)$ time. The subsequent loop runs $E$ times, but because the DSU `find` and `union` operations run in $O(\\alpha(V))$ practically $O(1)$ time, the entire loop takes $O(E)$. Since $E \\log E$ is mathematically larger than $E$, the sorting step dominates the Big-O bound.

3. Can Kruskal's handle Negative Edge Weights?
   Answer: YES! Unlike Dijkstra's shortest path, Kruskal's is building a Spanning Tree, not a directional route. The Greedy logic holds perfectly true: sorting the edges from cheapest to most expensive will naturally place the most negative edges at the absolute front of the array. Kruskal's will greedily buy all the negative edges first, effectively "getting paid" to connect the cities, perfectly minimizing the global cost.
"""

if __name__ == "__main__":
    demonstrate_kruskal()
    print("\n[SUCCESS] Laboratory: Kruskal's MST & DSU Completed.")
