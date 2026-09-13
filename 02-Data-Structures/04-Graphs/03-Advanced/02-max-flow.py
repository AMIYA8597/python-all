"""
# ==============================================================================
# LABORATORY: MAX FLOW (EDMONDS-KARP ALGORITHM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine a network of water pipes connecting a Water Treatment Plant (Source) 
# to a City (Sink). Every pipe has a maximum capacity (e.g., 10 gallons/sec). 
# What is the ABSOLUTE MAXIMUM amount of water you can pump through the entire 
# network simultaneously without bursting any pipes?
#
# This is the "Maximum Flow" problem. It is arguably the most important algorithm 
# in Operations Research, used for internet traffic routing, airline scheduling, 
# and bipartite matching.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Residual Graph and "Augmenting Paths".
# - Understand the crucial concept of "Pushing Flow Backwards" (Undo).
# - Implement the Edmonds-Karp algorithm (BFS-based Ford-Fulkerson).
#
# ==============================================================================
"""

from collections import deque, defaultdict
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MAX FLOW (EDMONDS-KARP IMPLEMENTATION)
# ==============================================================================
class FlowNetwork:
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        # We use an Adjacency Matrix for capacity to easily manage forward 
        # and backward edges in O(1) time. 
        self.capacity = [[0] * num_nodes for _ in range(num_nodes)]
        self.adj = defaultdict(list)
        
    def add_edge(self, u: int, v: int, cap: int):
        # A network flow edge is directed
        self.capacity[u][v] += cap
        
        # We must add the vertices to the adjacency list so BFS can traverse them.
        # CRUCIAL: We must also add the REVERSE edge to the adjacency list!
        # Even if the capacity of v -> u is 0, we need to be able to traverse it 
        # to "undo" flow later.
        self.adj[u].append(v)
        self.adj[v].append(u)

def bfs_augmenting_path(network: FlowNetwork, source: int, sink: int, parent: List[int]) -> int:
    """
    Finds ANY path from source to sink that still has available capacity.
    Because this is BFS (Edmonds-Karp), it finds the SHORTEST path (fewest edges).
    Returns the maximum flow that can be pushed through this specific path.
    """
    # Reset parent array
    for i in range(network.n):
        parent[i] = -1
        
    parent[source] = -2 # Mark source as visited
    
    # Queue stores (current_node, bottleneck_flow_so_far)
    queue = deque([(source, float('inf'))])
    
    while queue:
        u, current_flow = queue.popleft()
        
        for v in network.adj[u]:
            # If v is unvisited AND there is still available capacity in the pipe
            if parent[v] == -1 and network.capacity[u][v] > 0:
                parent[v] = u # Record the path
                
                # The flow we can push is limited by the smallest pipe in the path (bottleneck)
                new_flow = min(current_flow, network.capacity[u][v])
                
                if v == sink:
                    return new_flow
                    
                queue.append((v, new_flow))
                
    return 0 # No path found

def edmonds_karp(network: FlowNetwork, source: int, sink: int) -> int:
    """
    Computes the Maximum Flow from source to sink.
    Time Complexity: O(V * E^2)
    """
    max_flow = 0
    parent = [-1] * network.n
    
    while True:
        # 1. Find an augmenting path using BFS
        path_flow = bfs_augmenting_path(network, source, sink, parent)
        
        # 2. If no more paths exist, we have reached Maximum Flow!
        if path_flow == 0:
            break
            
        # 3. Add this path's flow to our total
        max_flow += path_flow
        
        # 4. Update the Residual Graph (The Magic Step)
        v = sink
        while v != source:
            u = parent[v]
            
            # Decrease the available capacity of the forward edge
            network.capacity[u][v] -= path_flow
            
            # INCREASE the capacity of the backward edge!
            # This allows future BFS searches to "undo" this flow by pushing 
            # flow backwards, essentially rerouting the water if a better path is found later.
            network.capacity[v][u] += path_flow
            
            v = u
            
    return max_flow

def demonstrate_max_flow():
    section_header("Algorithm: Edmonds-Karp (Max Flow)")
    
    # Build the classic diamond graph
    #      (10)
    #    /-----> Node 1
    #   /       /     \
    # S(0)    (2)     (10)
    #   \     /         \
    #    \-> Node 2 ----> Sink(3)
    #      (10)         (10)
    
    net = FlowNetwork(4)
    net.add_edge(0, 1, 10)
    net.add_edge(0, 2, 10)
    net.add_edge(1, 2, 2)
    net.add_edge(1, 3, 10)
    net.add_edge(2, 3, 10)
    
    print("Executing Max Flow from Source (0) to Sink (3)...")
    max_f = edmonds_karp(net, 0, 3)
    
    print(f"\nMaximum Flow achieved: {max_f}")
    print("(Expected: 20. 10 gallons through top, 10 gallons through bottom. The cross pipe (1->2) is useless here).")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we INCREASE the capacity of the REVERSE edge in the Residual Graph?
   Answer: This is the defining genius of the Ford-Fulkerson method. If we greedily push 10 gallons down a pipe, we might block a mathematically superior route that we didn't discover yet. By adding 10 gallons of capacity to the REVERSE edge, we give future BFS searches the ability to push water BACKWARDS. Pushing water backwards perfectly cancels out the previous flow, effectively "undoing" the bad greedy choice and allowing the water to be rerouted.

2. What is the difference between Ford-Fulkerson and Edmonds-Karp?
   Answer: Ford-Fulkerson is a general method that uses ANY search algorithm (often DFS) to find augmenting paths. If you use DFS, the algorithm can get trapped in a loop of tiny updates, taking O(Max_Flow * E) time (which can be infinite for irrational capacities). Edmonds-Karp specifies that you MUST use BFS. By always picking the shortest path, it mathematically guarantees termination in O(V * E^2) time.

3. What is the Min-Cut Max-Flow Theorem?
   Answer: The absolute maximum flow you can push through a network is EXACTLY EQUAL to the total capacity of the smallest set of edges that, if removed, would completely disconnect the source from the sink (the Minimum Cut).
"""

if __name__ == "__main__":
    demonstrate_max_flow()
    print("\n[SUCCESS] Laboratory: Max Flow (Edmonds-Karp) Completed.")
