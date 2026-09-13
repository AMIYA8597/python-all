"""
# ==============================================================================
# LABORATORY: JOHNSON'S ALGORITHM (GRAPH REWEIGHTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You need the All-Pairs Shortest Path (APSP) for a massive GPS graph.
# - Floyd-Warshall handles negative edges, but takes exactly O(V^3) time. For 
#   100,000 cities, V^3 takes 1000 Trillion operations. It's too slow.
# - Running Dijkstra from every city takes O(V * E log V). If the graph is 
#   sparse (like a road network where E ~ V), this is O(V^2 log V). 
#   That's billions of times faster!
#
# But there's a fatal problem: The graph has Negative Toll Roads. 
# Dijkstra mathematically crashes if it touches a negative edge.
# 
# In 1977, Donald Johnson invented a mathematical miracle to solve this.
# He asked: "Can we just add +100 to every edge to make them all positive, 
# and then run Dijkstra?"
# No! If you add a flat +100, a path with 5 short hops gets unfairly penalized 
# (+500) compared to a path with 1 long hop (+100). It physically breaks the 
# true optimal route.
#
# Johnson's Algorithm uses "Node Potentials" (calculated via a single run of 
# Bellman-Ford) to reweight the edges. The math guarantees that every edge 
# becomes strictly POSITIVE, but the global optimal path is perfectly preserved!
#
# Once reweighted, you can safely run the blazing-fast Dijkstra V times!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the failure of flat reweighting.
# - Execute the Bellman-Ford potential calculation.
# - Apply the algebraic shift: `w' = w + h(u) - h(v)`.
#
# ==============================================================================
"""

import heapq
import math
from typing import Dict, List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HELPER ALGORITHMS (BELLMAN-FORD & DIJKSTRA)
# ==============================================================================
def bellman_ford_potential(vertices: int, edges: List[Tuple[int, int, int]]) -> List[float]:
    """Runs Bellman-Ford from a 'phantom' node to calculate node potentials."""
    # We add a phantom node (let's call it node V) that has a 0-weight edge to ALL 
    # other nodes. This guarantees the algorithm can reach every disconnected island.
    distances = [0] * (vertices + 1) # V is the phantom node
    
    # We only need V-1 sweeps for the real nodes, but V sweeps to include the phantom.
    for _ in range(vertices):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                
    # One final sweep to detect negative cycles
    for u, v, w in edges:
        if distances[u] + w < distances[v]:
            raise ValueError("Graph contains a Negative Weight Cycle. APSP is impossible.")
            
    # Return the potentials for the real nodes (0 to V-1)
    return distances[:vertices]


def dijkstra_reweighted(graph: Dict[int, List[Tuple[int, int]]], start: int, num_vertices: int) -> List[float]:
    """Standard Dijkstra, but operating on the magically positive edges."""
    distances = [math.inf] * num_vertices
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, u = heapq.heappop(pq)
        
        if curr_dist > distances[u]:
            continue
            
        for v, weight in graph.get(u, []):
            if curr_dist + weight < distances[v]:
                distances[v] = curr_dist + weight
                heapq.heappush(pq, (distances[v], v))
                
    return distances


# ==============================================================================
# 4. JOHNSON'S ALGORITHM ENGINE (O(V E log V))
# ==============================================================================
def johnsons_algorithm(vertices: int, edges: List[Tuple[int, int, int]]) -> List[List[float]]:
    # 1. CALCULATE NODE POTENTIALS (O(V * E))
    # `h` is an array representing the mathematical "elevation" of each node.
    h = bellman_ford_potential(vertices, edges)
    
    # 2. REWEIGHT THE GRAPH (O(E))
    # We alter every edge using the magic formula: w' = w + h(u) - h(v)
    # The math guarantees that `w'` will ALWAYS be >= 0.
    reweighted_graph = {i: [] for i in range(vertices)}
    for u, v, w in edges:
        w_prime = w + h[u] - h[v]
        reweighted_graph[u].append((v, w_prime))
        
    # 3. RUN DIJKSTRA FROM EVERY NODE (O(V * E log V))
    all_pairs_shortest_paths = []
    
    for start_node in range(vertices):
        # Run Dijkstra on the strictly positive `w_prime` edges!
        dist_prime = dijkstra_reweighted(reweighted_graph, start_node, vertices)
        
        # 4. REVERSE THE ALGEBRAIC SHIFT
        # The distances returned by Dijkstra are based on `w_prime`.
        # To get the true original mileage, we reverse the math: True Dist = D_prime - h(u) + h(v)
        true_distances = []
        for v in range(vertices):
            if dist_prime[v] == math.inf:
                true_distances.append(math.inf)
            else:
                true_distances.append(dist_prime[v] - h[start_node] + h[v])
                
        all_pairs_shortest_paths.append(true_distances)
        
    return all_pairs_shortest_paths


def demonstrate_johnson():
    section_header("Algorithm: Johnson's APSP")
    
    vertices = 4
    # Include negative edges!
    edges = [
        (0, 1, -5),
        (0, 2, 2),
        (1, 2, 4),
        (2, 3, 1),
        (3, 0, 3) # Loop back, but overall cycle weight is -5+4+1+3 = 3 (Positive cycle, so it's safe!)
    ]
    
    print("Executing Bellman-Ford to calculate potentials...")
    print("Reweighting graph algebraically...")
    print("Executing Dijkstra V times on positive edges...")
    
    apsp = johnsons_algorithm(vertices, edges)
    
    print("\nAll Pairs Shortest Paths Matrix:")
    for i, row in enumerate(apsp):
        print(f" From {i}: {row}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does adding $h(u) - h(v)$ preserve the shortest path?
   Answer: This is "Telescoping Math". If you travel from A -> B -> C, the new cost is: 
   $(Cost(A, B) + h(A) - h(B)) + (Cost(B, C) + h(B) - h(C))$.
   Notice how $-h(B)$ and $+h(B)$ perfectly cancel each other out! The intermediate nodes vanish completely from the equation. The total shift for ANY path from A to C is purely $+ h(A) - h(C)$. Because every single possible path between A and C is penalized by the exact same mathematical constant, the shortest path remains identically the shortest path!

2. How does the math guarantee the new edges will be strictly $\ge 0$?
   Answer: The potentials $h(u)$ were calculated using Bellman-Ford. Bellman-Ford guarantees that for any edge $u \\to v$, the triangle inequality holds: $h(v) \le h(u) + w$. 
   If we rearrange that algebra: $0 \le w + h(u) - h(v)$.
   This perfectly matches our reweighting formula! Thus, the new edge weight is mathematically guaranteed to be $\ge 0$, rendering it 100% safe for Dijkstra!

3. Could we just use Dijkstra if we ensure our graph has no negative cycles?
   Answer: No! Dijkstra crashes on ANY negative edge, even if it isn't part of a cycle. Dijkstra is fundamentally greedy. Once it finalizes a node, it never looks back. If a negative edge later in the graph provides a shorter route, Dijkstra will ignore it. You MUST use Johnson's reweighting trick to eliminate the negative edge entirely before invoking Dijkstra.
"""

if __name__ == "__main__":
    demonstrate_johnson()
    print("\n[SUCCESS] Laboratory: Johnson's Algorithm Completed.")
