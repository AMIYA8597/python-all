"""
# ==============================================================================
# LABORATORY: MIN-COST MAX-FLOW (MCMF)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You work for FedEx. You have 100 packages (Capacity) that must travel from 
# New York (S) to Los Angeles (T).
# 
# Standard Max Flow (Dinic's, Edmonds-Karp) will successfully route all 100 
# packages using the available trucks. BUT it ignores money. It might put 90 
# packages on a Private Jet, and 10 on a train. 
# You will go bankrupt.
#
# In the real world, every pipe/truck has TWO properties:
# 1. Capacity (e.g., max 10 packages).
# 2. Cost (e.g., $50 per package).
#
# The goal of Min-Cost Max-Flow (MCMF) is to push the maximum possible volume 
# through the network, but strictly prioritizing the CHEAPEST routes first!
#
# THE ALGORITHM (Successive Shortest Path):
# We use the Edmonds-Karp architecture. But instead of using BFS to find the 
# path with the fewest edges, we use an algorithm to find the path with the 
# LOWEST COST.
#
# Wait, can we just use Dijkstra?
# NO! Remember the Phantom Pipes from Ford-Fulkerson? If you push a package 
# down a $50 pipe, the Phantom Backward pipe allows you to "undo" that flow. 
# Therefore, the Phantom Pipe has a cost of -$50 (a REFUND!).
# 
# Dijkstra crashes on Negative Edges! So we must use Bellman-Ford (or the 
# highly optimized Shortest Path Faster Algorithm - SPFA) to find the cheapest 
# path through the residual graph!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Capacity and Cost.
# - Understand why Phantom Pipes have negative costs (Refunds).
# - Implement the SPFA-based Min-Cost Max-Flow engine.
#
# ==============================================================================
"""

import math
from collections import deque
from typing import List, Tuple, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MCMF ENGINE (SUCCESSIVE SHORTEST PATH VIA SPFA)
# ==============================================================================
def spfa_shortest_path(vertices: int, capacity: List[List[int]], cost: List[List[float]], source: int, sink: int, parent_map: List[int]) -> bool:
    """
    Shortest Path Faster Algorithm (SPFA).
    An optimized queue-based version of Bellman-Ford that safely handles 
    Negative Edges without hitting O(V*E) on average.
    Finds the absolute CHEAPEST path from Source to Sink where Capacity > 0.
    """
    # 1. INITIALIZE DISTANCES
    distances = [math.inf] * vertices
    distances[source] = 0
    
    # We use a Queue to track which nodes need their outgoing edges relaxed
    queue = deque([source])
    
    # Boolean array to track if a node is CURRENTLY physically inside the queue
    in_queue = [False] * vertices
    in_queue[source] = True
    
    while queue:
        u = queue.popleft()
        in_queue[u] = False # We took it out!
        
        # Look at all neighbors
        for v in range(vertices):
            # If the pipe has physical space for more packages...
            if capacity[u][v] > 0:
                # If routing through `u` is CHEAPER than the current known cost to `v`...
                if distances[u] + cost[u][v] < distances[v]:
                    # Update the record!
                    distances[v] = distances[u] + cost[u][v]
                    parent_map[v] = u
                    
                    # If `v` isn't already waiting in the queue, put it in so it 
                    # can update its own downstream neighbors!
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
                        
    # If the sink's distance is no longer infinity, we found a valid path!
    return distances[sink] != math.inf


def min_cost_max_flow(vertices: int, capacity: List[List[int]], cost: List[List[float]], source: int, sink: int) -> Tuple[int, float]:
    """
    Computes both the Max Flow and the Minimum Cost required to achieve it.
    """
    max_flow = 0
    total_cost = 0.0
    
    parent_map = [-1] * vertices
    
    # 1. THE INFINITE PUMPING LOOP
    # We keep running SPFA to find the absolute cheapest path available.
    while spfa_shortest_path(vertices, capacity, cost, source, sink, parent_map):
        
        # 2. FIND THE BOTTLENECK (CAPACITY)
        path_flow = math.inf
        curr = sink
        
        while curr != source:
            prev = parent_map[curr]
            path_flow = min(path_flow, capacity[prev][curr])
            curr = prev
            
        # 3. PUSH FLOW, PAY THE BILL, AND CREATE PHANTOM PIPES
        max_flow += path_flow
        
        curr = sink
        while curr != source:
            prev = parent_map[curr]
            
            # Forward pipe loses capacity
            capacity[prev][curr] -= path_flow
            
            # Phantom backward pipe gains capacity!
            capacity[curr][prev] += path_flow
            
            # We must PAY for the packages we just moved!
            # Total Cost += (Number of Packages) * (Cost per Package)
            total_cost += path_flow * cost[prev][curr]
            
            curr = prev
            
    return max_flow, total_cost


def demonstrate_mcmf():
    section_header("Algorithm: Min-Cost Max-Flow (MCMF)")
    
    vertices = 4
    # Nodes: 0=Source, 1, 2, 3=Sink
    
    # ---------------------------------------------------------
    # CAPACITY MATRIX
    # ---------------------------------------------------------
    capacity = [
        [0, 10, 10, 0],  # S -> 1 (Cap 10), S -> 2 (Cap 10)
        [0, 0,  0,  15], # 1 -> T (Cap 15)
        [0, 0,  0,  15], # 2 -> T (Cap 15)
        [0, 0,  0,  0]   # T
    ]
    
    # ---------------------------------------------------------
    # COST MATRIX
    # ---------------------------------------------------------
    # S -> 1 is a Private Jet (Cost: $50)
    # S -> 2 is a Cargo Train (Cost: $5)
    # Both paths from 1 and 2 to the Sink cost $0 (just for simplicity).
    # Remember: Phantom backward pipes must have NEGATIVE costs!
    cost = [
        [0,   50,  5,   0],
        [-50, 0,   0,   0],  # Phantom S->1 Refund
        [-5,  0,   0,   0],  # Phantom S->2 Refund
        [0,   0,   0,   0]
    ]
    
    source = 0
    sink = 3
    
    print("Executing Min-Cost Max-Flow Engine...")
    flow, total_money = min_cost_max_flow(vertices, capacity, cost, source, sink)
    
    print(f"\nResults:")
    print(f"Max Flow (Packages Delivered): {flow}")
    print(f"Total Cost to FedEx: ${total_money}")
    
    print("\nExplanation:")
    print("Max Flow is 20 (10 down the Train, 10 down the Jet).")
    print("The SPFA found the Train ($5) first! It maxed it out (10 * $5 = $50).")
    print("Then it was forced to use the Jet ($50) to max out the flow (10 * $50 = $500).")
    print("Total Bill = $550.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must the backward phantom pipe have a NEGATIVE cost?
   Answer: The entire point of the residual graph is to allow the algorithm to mathematically "undo" a previous greedy decision if a better global route is found later. If we pushed a package down a $50 pipe, we were billed $50. If we later find a better route and decide to push that package backward out of the pipe to route it elsewhere, we MUST receive our $50 back! The -$50 phantom pipe represents the refund.

2. Why can't we use Dijkstra's Algorithm instead of SPFA/Bellman-Ford?
   Answer: Dijkstra's Algorithm absolutely crashes the moment it encounters a negative edge. Because every forward flow in MCMF physically creates a negative phantom pipe in the residual graph, the graph is mathematically guaranteed to be flooded with negative edges during the while loop. Dijkstra's Greedy assumption fails, and you must use a Bellman-Ford variant.

3. Is it possible to use Dijkstra for MCMF?
   Answer: YES, but it requires a massive mathematical trick! Similar to Johnson's Algorithm (from the Shortest Path module), you can use "Node Potentials" to algebraically shift all costs in the graph so they are strictly $\ge 0$. You run Bellman-Ford exactly ONCE at the beginning to establish the potentials, and then you can safely use Dijkstra inside the `while` loop! This optimization achieves $O(F \cdot E \\log V)$, which is heavily used in FAANG competitive programming.
"""

if __name__ == "__main__":
    demonstrate_mcmf()
    print("\n[SUCCESS] Laboratory: Min-Cost Max-Flow Completed.")
