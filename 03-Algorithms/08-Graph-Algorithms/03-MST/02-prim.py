"""
# ==============================================================================
# LABORATORY: PRIM'S ALGORITHM (GROWING THE MST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Kruskal's Algorithm builds a Minimum Spanning Tree (MST) by looking at the 
# entire world globally. It sorts every wire on Earth, buys the cheapest one, 
# and creates dozens of disconnected mini-islands that slowly merge together.
#
# Prim's Algorithm (developed by Vojtěch Jarník in 1930, and Robert Prim in 1957) 
# takes a completely different philosophical approach.
# It grows a single, unified, contiguous island.
#
# It starts at one random city. It looks at all the wires connected to that city, 
# picks the cheapest one, and absorbs the new city into its empire. Then it looks 
# at all the wires connected to the EMPIRE, picks the cheapest one, and absorbs 
# the next city.
#
# If this sounds suspiciously like Dijkstra's Shortest Path Algorithm, you are right!
# Prim's is the exact same code architecture as Dijkstra (using a Min-Heap).
#
# THE ONE DIFFERENCE:
# - Dijkstra's PQ tracks: "Total accumulated distance from the Start Node".
# - Prim's PQ tracks: "The physical cost of this specific single wire".
# 
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Global Greedy (Kruskal) and Local Greedy (Prim).
# - Adapt Dijkstra's Min-Heap engine to solve MST.
# - Analyze the Density Tradeoff (Sparse vs Dense graphs).
#
# ==============================================================================
"""

import heapq
from typing import Dict, List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PRIM'S MST ENGINE (O((V+E) log V))
# ==============================================================================
def prims_mst(vertices: int, graph: Dict[int, List[Tuple[int, float]]]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Time Complexity: O((V+E) log V) using a standard binary heap.
    Space Complexity: O(V + E) for the graph, visited set, and Priority Queue.
    """
    
    mst_cost = 0
    mst_edges = []
    
    # Track nodes that have already been absorbed into the Empire
    visited = set()
    
    # The Priority Queue stores: (edge_weight, destination_node, source_node)
    # We include `source_node` purely so we can print out which wire we bought!
    # Start at Node 0. It costs $0 to teleport to the start node.
    pq = [(0, 0, -1)] 
    
    while pq:
        # Pop the cheapest available wire connected to the Empire
        weight, current_node, source_node = heapq.heappop(pq)
        
        # If this node is ALREADY in the Empire, buying this wire would 
        # mathematically create a cycle! Discard it instantly!
        if current_node in visited:
            continue
            
        # 1. ABSORB THE NODE INTO THE EMPIRE
        visited.add(current_node)
        mst_cost += weight
        
        # Record the wire we bought (ignore the imaginary teleport to the start node)
        if source_node != -1:
            mst_edges.append((source_node, current_node))
            
        # Optimization: A spanning tree for V nodes has exactly V-1 edges.
        # If we have absorbed all V nodes, we are done!
        if len(visited) == vertices:
            break
            
        # 2. SURVEY THE NEW FRONTIER
        # Look at all wires emanating from this newly conquered node
        for neighbor, edge_cost in graph.get(current_node, []):
            # Only push wires that lead to UNCONQUERED territory!
            if neighbor not in visited:
                # NOTICE: We push ONLY `edge_cost`. 
                # In Dijkstra, we would push `total_accumulated_distance + edge_cost`!
                heapq.heappush(pq, (edge_cost, neighbor, current_node))
                
    # Edge case verification
    if len(visited) != vertices:
        raise ValueError("Graph is disconnected. No valid MST exists.")
        
    return mst_cost, mst_edges


def demonstrate_prim():
    section_header("Algorithm: Prim's Minimum Spanning Tree")
    
    vertices = 4
    # Adjacency List: {Node: [(Neighbor, Cost)]}
    # Note: MST applies to UNDIRECTED graphs, so every edge must exist in both directions!
    graph = {
        0: [(1, 10), (2, 6), (3, 5)],
        1: [(0, 10), (3, 15)],
        2: [(0, 6), (3, 4)],
        3: [(0, 5), (1, 15), (2, 4)]
    }
    
    print("Graph Adjacency List:")
    for node, edges in graph.items():
        print(f" Node {node} connections: {edges}")
        
    print("\nExecuting Prim's Local Greedy Algorithm (Min-Heap)...")
    cost, mst = prims_mst(vertices, graph)
    
    print(f"\nMinimum Cost to connect all cities: ${cost}")
    print("Cables purchased:")
    for u, v in mst:
        print(f" -> Connect {u} and {v}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference in the code between Dijkstra and Prim?
   Answer: It is literally one single line of code. When exploring neighbors, Dijkstra pushes `(current_distance + edge_weight)` to the Min-Heap. Prim pushes ONLY `(edge_weight)`. Dijkstra optimizes for the global route from the starting point. Prim optimizes purely for the absolute cheapest local wire attached to the current structure.

2. When should you use Kruskal's vs Prim's algorithm?
   Answer: "Graph Density". 
   - A "Sparse" graph has very few edges (e.g., $E \approx V$). Kruskal's sorting step takes $O(E \\log E) \\approx O(V \\log V)$. It is blazing fast and easier to implement with a DSU.
   - A "Dense" graph has maximum edges (e.g., $E \approx V^2$). Kruskal's sorting step takes $O(V^2 \\log V^2) = O(V^2 \\log V)$. Prim's algorithm, if optimized with a Fibonacci Heap, runs in $O(E + V \\log V) = O(V^2 + V \\log V) = O(V^2)$. Thus, Prim's is mathematically superior for massively dense networks!

3. Can Prim's handle Disconnected Graphs?
   Answer: By default, no. Prim's algorithm grows a single contiguous island. If a node is completely isolated with no edges, the Priority Queue will empty out before the `visited` set reaches the total number of vertices. Kruskal's algorithm handles it naturally because it evaluates edges globally, but it will still fail to return a full $V-1$ spanning tree. If you want a "Minimum Spanning FOREST" (multiple disjoint MSTs), you must wrap Prim's in a global loop over all unvisited vertices, exactly like computing Disconnected Components in DFS.
"""

if __name__ == "__main__":
    demonstrate_prim()
    print("\n[SUCCESS] Laboratory: Prim's Algorithm Completed.")
