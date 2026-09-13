"""
# ==============================================================================
# LABORATORY: BORŮVKA'S ALGORITHM (DISTRIBUTED MST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Kruskal's algorithm (1956) and Prim's algorithm (1957) are famous.
# But 30 years earlier, in 1926, Otakar Borůvka invented the very first MST 
# algorithm to build the most efficient electrical grid for the country of Moravia.
#
# Borůvka's Algorithm is a hybrid of Kruskal and Prim!
# - Like Kruskal, it starts with V completely disjoint islands.
# - Like Prim, islands look outward to find the cheapest wire connecting to a neighbor.
#
# The Magic Loop:
# 1. EVERY SINGLE ISLAND simultaneously looks at all its outward-facing wires.
# 2. EVERY ISLAND simultaneously picks its absolute cheapest outgoing wire.
# 3. We buy all those wires at once, instantly merging many islands together!
# 4. Repeat until only 1 island remains.
#
# Because every island buys a wire, the total number of islands cuts in HALF 
# (at minimum) every single iteration! Therefore, the outer loop runs a maximum 
# of O(log V) times. Finding the cheapest wires takes O(E).
# Total Time: O(E log V).
#
# So why use Borůvka's today if it's the same speed as Kruskal's?
# PARALLEL COMPUTING! 
# Kruskal's sorting step is sequential. Prim's Priority Queue is sequential. 
# You cannot easily divide them across 1,000 servers.
# In Borůvka, if you have 1,000 islands, you can assign 1 island to each CPU core! 
# Every core independently calculates its cheapest outgoing edge simultaneously.
# This makes it the algorithm of choice for Distributed Graph Processing (Hadoop MapReduce).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Multi-Source Simultaneous Greedy approach.
# - Implement the O(log V) outer reduction loop.
# - Reuse the Disjoint Set Union (DSU) engine to track island merges.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DSU ENGINE (Recycled from Kruskal's)
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
        if root_i == root_j:
            return False
        # Simplified union for Boruvka
        self.parent[root_i] = root_j
        return True


# ==============================================================================
# 4. BORŮVKA'S ALGORITHM ENGINE (O(E log V))
# ==============================================================================
def boruvkas_mst(vertices: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Time Complexity: O(E log V)
    Space Complexity: O(V)
    """
    dsu = DSU(vertices)
    
    mst_cost = 0
    mst_edges = []
    
    num_islands = vertices
    
    # Outer loop runs at most O(log V) times!
    while num_islands > 1:
        
        # Array to store the absolute cheapest outgoing edge for EVERY island.
        # Initialize with -1 to indicate "no edge found yet".
        cheapest_edges = [-1] * vertices
        
        # ----------------------------------------------------------------------
        # PHASE 1: FIND CHEAPEST OUTGOING EDGES (Massively Parallelizable)
        # ----------------------------------------------------------------------
        for edge_idx, (u, v, weight) in enumerate(edges):
            # Find which island node u and node v currently belong to
            island_u = dsu.find(u)
            island_v = dsu.find(v)
            
            # If they are on the SAME island, this is an internal wire (cycle). Ignore!
            if island_u == island_v:
                continue
                
            # For Island U, is this new wire cheaper than its currently known cheapest?
            # In a distributed system, this logic runs concurrently on separate threads!
            if cheapest_edges[island_u] == -1 or weight < edges[cheapest_edges[island_u]][2]:
                cheapest_edges[island_u] = edge_idx
                
            # For Island V, is this new wire cheaper?
            if cheapest_edges[island_v] == -1 or weight < edges[cheapest_edges[island_v]][2]:
                cheapest_edges[island_v] = edge_idx
                
        # ----------------------------------------------------------------------
        # PHASE 2: BUY THE CABLES AND MERGE ISLANDS
        # ----------------------------------------------------------------------
        # Flag to detect if the graph is disconnected
        edges_bought_this_round = False
        
        for island in range(vertices):
            # If this island successfully found a cheapest outgoing wire...
            edge_idx = cheapest_edges[island]
            if edge_idx != -1:
                u, v, weight = edges[edge_idx]
                
                # Try to merge the two islands!
                # (We must check because another island might have ALREADY bought 
                # this exact same wire from the other side during this loop!)
                if dsu.union(u, v):
                    mst_cost += weight
                    mst_edges.append((u, v))
                    num_islands -= 1
                    edges_bought_this_round = True
                    
        # If we went through a whole round and bought ZERO edges, but we still 
        # have >1 island, it means the graph is physically disconnected!
        if not edges_bought_this_round:
            raise ValueError("Graph is disconnected. No valid MST exists.")
            
    return mst_cost, mst_edges


def demonstrate_boruvka():
    section_header("Algorithm: Boruvka's Minimum Spanning Tree")
    
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
        
    print("\nExecuting Boruvka's Distributed Greedy Algorithm...")
    cost, mst = boruvkas_mst(vertices, edges)
    
    print(f"\nMinimum Cost to connect all cities: ${cost}")
    print("Cables purchased:")
    for u, v in mst:
        print(f" -> Connect {u} and {v}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the number of islands cut in half at every iteration?
   Answer: Imagine 8 completely separate islands. In Phase 1, EVERY island picks an outgoing edge. This results in 8 edges being selected. In the worst-case configuration, they all pair up with each other perfectly (1 pairs with 2, 3 pairs with 4...). This results in exactly 4 new larger islands. Therefore, the total number of islands drops by a factor of 2. An algorithm that divides its problem size by 2 at every step has an execution bound of $O(\\log N)$.

2. Why must we check `dsu.union(u, v)` again in Phase 2? Didn't we already ensure they were separate in Phase 1?
   Answer: In Phase 1, Island A selects edge (A->B) because it's cheap. Simultaneously, Island B selects the EXACT SAME edge (B->A) because it's also B's cheapest edge! In Phase 2, when we loop through the islands, Island A will successfully buy the edge and merge A and B. When the loop reaches Island B, it tries to buy the exact same edge again! The `dsu.union(u, v)` instantly returns False because A and B were already merged by A's purchase, preventing us from double-charging the cost.

3. Why is this algorithm so important for Google/Facebook?
   Answer: Modern graphs (like the Facebook social network or the Google web-link graph) contain Billions of vertices and Trillions of edges. You cannot load this into the RAM of a single server. You MUST use a distributed framework (like Apache Spark or Google Pregel). Borůvka's algorithm allows the graph to be partitioned across 1,000 servers. Each server runs Phase 1 independently on its local subset of edges. They send their chosen edges to a master server which runs Phase 2. This architecture is physically impossible with Dijkstra/Prim.
"""

if __name__ == "__main__":
    demonstrate_boruvka()
    print("\n[SUCCESS] Laboratory: Boruvka's Algorithm Completed.")
