"""
# ==============================================================================
# LABORATORY: BELLMAN-FORD (NEGATIVE EDGES & CYCLES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dijkstra's algorithm is blazing fast, but it is Greedy. It assumes that 
# taking an extra step will always ADD distance to your journey.
# 
# What if you are mapping Financial Arbitrage? You start with $100. 
# You convert USD -> EUR -> JPY -> USD. 
# Due to exchange rate discrepancies, you end up with $102! 
# In graph theory, this is a "Negative Edge" (the cost went down). 
# Even worse, this is a "Negative Weight Cycle". You can loop this cycle 
# endlessly to print infinite money!
#
# Dijkstra will instantly crash or infinite-loop if it hits a negative cycle.
#
# Enter Richard Bellman (the inventor of Dynamic Programming) and Lester Ford.
# The Bellman-Ford algorithm doesn't use a Min-Heap. It doesn't use Greed.
# It simply loops over EVERY SINGLE EDGE in the entire graph, and relaxes them.
# How many times does it do this? Exactly V - 1 times (where V is Vertices).
#
# Why V - 1? Because mathematically, the longest possible route between two nodes 
# that does NOT visit the same node twice (a simple path) contains exactly V-1 edges!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Bellman-Ford handles negative edges.
# - Implement the V-1 global relaxation sweep.
# - Execute the V-th sweep to detect Negative Cycles (Arbitrage).
#
# ==============================================================================
"""

import math
from typing import Dict, List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BELLMAN-FORD ENGINE (O(V * E))
# ==============================================================================
def bellman_ford(vertices: int, edges: List[Tuple[int, int, float]], start: int):
    """
    Computes shortest path from `start` to all nodes.
    Detects Negative Weight Cycles.
    Time Complexity: O(V * E)
    Space Complexity: O(V)
    """
    # 1. INITIALIZE DISTANCES
    distances = {i: math.inf for i in range(vertices)}
    distances[start] = 0
    parent_map = {start: None}
    
    # 2. THE V-1 RELAXATION SWEEP
    # We must sweep every single edge, V-1 times.
    for iteration in range(vertices - 1):
        # Optimization flag: If we do a full sweep and NOTHING changes, 
        # the graph is already perfectly optimized! We can break early!
        any_updates = False
        
        for u, v, weight in edges:
            # If the start node `u` has actually been reached...
            if distances[u] != math.inf:
                # If the path through `u` is strictly better than `v`'s current record...
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    parent_map[v] = u
                    any_updates = True
                    
        # If no edges were relaxed in this entire sweep, we are done!
        if not any_updates:
            break
            
    # 3. NEGATIVE CYCLE DETECTION (The V-th Sweep!)
    # We already mathematically proved that V-1 sweeps guarantees the shortest 
    # possible simple paths.
    # Therefore, if we sweep ONE MORE TIME, and we STILL find a shorter path, 
    # it is physically impossible unless there is an infinite negative loop!
    for u, v, weight in edges:
        if distances[u] != math.inf:
            if distances[u] + weight < distances[v]:
                raise ValueError(f"CRITICAL: Negative Weight Cycle Detected via edge {u}->{v}!")
                
    return distances, parent_map


def demonstrate_bellman_ford():
    section_header("Algorithm: Bellman-Ford")
    
    # Let's create a graph WITH a negative edge, but NO negative cycle.
    # 0 -> 1 (Weight 4)
    # 0 -> 2 (Weight 5)
    # 2 -> 1 (Weight -2)  <- Negative Edge!
    # 1 -> 3 (Weight 3)
    vertices = 4
    edges = [
        (0, 1, 4),
        (0, 2, 5),
        (2, 1, -2), 
        (1, 3, 3)
    ]
    
    start = 0
    print("Graph Edges:")
    for u, v, w in edges: print(f" Node {u} -> {v} (Cost: {w})")
        
    print("\nExecuting Bellman-Ford O(V*E)...")
    distances, parents = bellman_ford(vertices, edges, start)
    
    print("\nFinal Optimal Distances:")
    for node, dist in distances.items():
        print(f" -> Node {node}: {dist}")
        
    print("\n(Notice how Node 1 has a distance of 3, because the algorithm correctly routed 0 -> 2 -> 1 (5 - 2 = 3), ignoring the direct 0->1 path of 4!)")
    
    # ---------------------------------------------------------
    section_header("Arbitrage: Negative Cycle Detection")
    # Let's inject a cycle that prints infinite money.
    # 0 -> 1 (1)
    # 1 -> 2 (-1)
    # 2 -> 0 (-1)
    bad_edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 0, -1)
    ]
    print("Injecting Malicious Cycle (0->1->2->0)...")
    try:
        bellman_ford(3, bad_edges, 0)
    except ValueError as e:
        print(f"\nALGORITHM HALTED:\n{e}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Bellman-Ford run exactly $V - 1$ times?
   Answer: In any graph with $V$ vertices, the longest possible path that doesn't loop back on itself (a simple path) contains exactly $V - 1$ edges. Imagine a straight line graph: 1 -> 2 -> 3 -> 4. ($V=4$). The path from 1 to 4 takes 3 edges ($4 - 1$). In the absolute worst-case scenario, the edge list is perfectly backwards, meaning we only successfully relax 1 edge per sweep. Sweeping the entire edge list $V - 1$ times guarantees that the ripple effect has had enough mathematical time to propagate from one end of the graph to the other.

2. How does the V-th sweep detect a Negative Cycle?
   Answer: After $V - 1$ sweeps, the algorithm guarantees it has found the absolute shortest possible non-looping paths. If you sweep a $V$-th time, and a distance magically decreases AGAIN, it mathematically proves that taking a cycle (visiting a node twice) reduced your total distance! This is the definition of a Negative Weight Cycle.

3. Why not always use Bellman-Ford instead of Dijkstra?
   Answer: Time Complexity. Dijkstra runs in $O((V+E) \\log V)$, which is exceptionally fast. Bellman-Ford runs in $O(V \\times E)$. In a dense graph where every node connects to every other node, $E \approx V^2$. This means Bellman-Ford hits $O(V^3)$ time! Dijkstra would hit $O(V^2 \\log V)$. You should strictly use Dijkstra unless you absolutely know your data contains negative edges.
"""

if __name__ == "__main__":
    demonstrate_bellman_ford()
    print("\n[SUCCESS] Laboratory: Bellman-Ford Algorithm Completed.")
