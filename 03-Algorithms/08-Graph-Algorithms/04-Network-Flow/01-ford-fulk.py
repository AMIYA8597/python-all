"""
# ==============================================================================
# LABORATORY: NETWORK FLOW (FORD-FULKERSON & RESIDUAL GRAPHS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You manage a city's water infrastructure. You have a Water Treatment Plant 
# (the Source, `S`) and a major Downtown Hub (the Sink, `T`). 
# Between them is a massive, complex network of pipes. Every pipe has a physical 
# Maximum Capacity (e.g., 10 gallons per minute).
# 
# What is the absolute MAXIMUM amount of water you can pump from S to T?
#
# A naive Greedy algorithm fails instantly. If you greedily pump 10 gallons down 
# the widest pipe, that water might get "stuck" in a bottleneck later on, while 
# simultaneously blocking a different route from being used!
#
# In 1956, L.R. Ford and D.R. Fulkerson invented the solution: The Residual Graph.
#
# Every time you push water down a pipe, you MUST magically create a "Phantom Pipe" 
# facing the exact opposite direction. 
# If I push 5 gallons from A -> B, I create a phantom pipe from B -> A with a 
# capacity of 5. 
# 
# Why? Because later in the algorithm, if we find a better route, we can literally 
# pump water BACKWARDS through the phantom pipe. Mathematically, pumping water 
# backward perfectly cancels out the previous water, effectively "undoing" our 
# previous bad greedy decision!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Max-Flow Min-Cut Theorem.
# - Build the Adjacency Matrix Residual Graph.
# - Implement the DFS Augmenting Path search.
# - Understand the "Phantom Pipe" backward flow algebra.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FORD-FULKERSON ENGINE (DFS & RESIDUAL GRAPHS)
# ==============================================================================
def dfs_augmenting_path(residual_graph: List[List[int]], source: int, sink: int, parent_map: List[int], visited: List[bool]) -> bool:
    """
    Standard DFS that searches for ANY valid path from Source to Sink 
    where the pipe capacities are strictly > 0.
    Updates `parent_map` so we can trace the path backward later.
    """
    visited[source] = True
    
    # Base case: We hit the sink!
    if source == sink:
        return True
        
    for neighbor, capacity in enumerate(residual_graph[source]):
        # If we haven't visited this node, AND the pipe can physically hold more water!
        if not visited[neighbor] and capacity > 0:
            parent_map[neighbor] = source
            
            # Recurse deeper!
            if dfs_augmenting_path(residual_graph, neighbor, sink, parent_map, visited):
                return True
                
    return False


def ford_fulkerson(vertices: int, graph: List[List[int]], source: int, sink: int) -> int:
    """
    Time Complexity: O(E * MaxFlow). This is "Pseudo-Polynomial".
    If the Max Flow is 1 Billion, the DFS might run 1 Billion times!
    Space Complexity: O(V^2) for the Adjacency Matrix Residual Graph.
    """
    
    # 1. CREATE THE RESIDUAL GRAPH
    # At the very beginning, the Residual Graph is an exact copy of the Original Graph.
    residual_graph = [[graph[i][j] for j in range(vertices)] for i in range(vertices)]
    
    # Array to track how we reached each node during the DFS
    parent_map = [-1] * vertices
    
    max_flow = 0
    
    # 2. THE INFINITE PUMPING LOOP
    # We keep running DFS until there are literally NO MORE paths from S to T 
    # that have a capacity > 0.
    while True:
        
        visited = [False] * vertices
        
        # Fire the DFS! Did it find a path?
        if not dfs_augmenting_path(residual_graph, source, sink, parent_map, visited):
            # No path found? We have mathematically reached absolute maximum capacity!
            break
            
        # 3. TRACE THE PATH BACKWARD TO FIND THE BOTTLENECK
        # We found a path! But how much water can we actually push through it?
        # A chain is only as strong as its weakest link. We must find the 
        # lowest capacity pipe in this specific path!
        path_flow = math.inf
        curr = sink
        
        while curr != source:
            prev = parent_map[curr]
            # Update the bottleneck if this pipe is smaller
            path_flow = min(path_flow, residual_graph[prev][curr])
            curr = prev
            
        # 4. PUSH THE WATER & CREATE PHANTOM PIPES
        # We now push `path_flow` gallons of water down the path!
        max_flow += path_flow
        
        curr = sink
        while curr != source:
            prev = parent_map[curr]
            
            # A. Subtract the capacity from the Forward Pipe (it's filling up!)
            residual_graph[prev][curr] -= path_flow
            
            # B. Add the capacity to the Phantom Backward Pipe!
            # This allows future DFS runs to "undo" this flow by pumping backward!
            residual_graph[curr][prev] += path_flow
            
            curr = prev
            
    return max_flow


def demonstrate_ford_fulkerson():
    section_header("Algorithm: Ford-Fulkerson (Max Flow)")
    
    vertices = 6
    # 2D Adjacency Matrix Capacities
    # Nodes: 0=Source, 1, 2, 3, 4, 5=Sink
    graph = [
        [0, 16, 13, 0,  0,  0 ], # S (0) -> 1 (16), S -> 2 (13)
        [0, 0,  10, 12, 0,  0 ], # 1 -> 2 (10), 1 -> 3 (12)
        [0, 4,  0,  0,  14, 0 ], # 2 -> 1 (4), 2 -> 4 (14)
        [0, 0,  9,  0,  0,  20], # 3 -> 2 (9), 3 -> T (20)
        [0, 0,  0,  7,  0,  4 ], # 4 -> 3 (7), 4 -> T (4)
        [0, 0,  0,  0,  0,  0 ]  # T (5)
    ]
    
    source = 0
    sink = 5
    
    print("Graph Capacities Matrix:")
    for row in graph: print(row)
        
    print(f"\nExecuting Ford-Fulkerson (S={source} -> T={sink})...")
    max_flow = ford_fulkerson(vertices, graph, source, sink)
    
    print(f"\nAbsolute Maximum Water Flow: {max_flow} gallons/sec")
    print("(Expected: 23)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does it physically mean to "pump water backward" through a phantom pipe?
   Answer: Imagine A -> B has a capacity of 10. We pumped 10 gallons through it. The forward pipe is now 0. We create a phantom pipe B -> A with capacity 10. Later, the algorithm finds a route that enters B, and decides to pump 4 gallons down the B -> A phantom pipe. Physically, water isn't flowing backwards. What we actually did was REDUCE the forward flow of A -> B from 10 down to 6! We intercepted the 4 gallons at B and re-routed them somewhere else! The phantom pipe is just an algebraic trick to "undo" bad flow assignments.

2. What is the "Max-Flow Min-Cut Theorem"?
   Answer: This is one of the most profound theorems in graph theory. It states that the Maximum Flow of the entire network is mathematically identical to the "Minimum Cut". A Cut is a physical line you draw through the graph that separates S from T. If you calculate the capacity of all the pipes your line sliced through, the smallest possible slice capacity is EXACTLY EQUAL to the maximum flow of the network! The network is physically bottlenecked by its smallest cross-section.

3. Why is $O(E \\times MaxFlow)$ considered a dangerous "Pseudo-Polynomial" bound?
   Answer: Imagine a graph with only 4 nodes. S -> A (Cap: 1 Billion), S -> B (Cap: 1 Billion), A -> T (Cap: 1 Billion), B -> T (Cap: 1 Billion), and a middle pipe A -> B (Cap: 1). 
   If the DFS is unlucky, it routes 1 gallon through S -> A -> B -> T. Then it routes 1 gallon S -> B -> A -> T. Because the DFS only finds paths of 1 gallon at a time, it will run 2 Billion times to fill the pipes! The time complexity depends on the ACTUAL DATA VALUES, not just the number of nodes! This is a catastrophic flaw.
"""

if __name__ == "__main__":
    demonstrate_ford_fulkerson()
    print("\n[SUCCESS] Laboratory: Ford-Fulkerson Algorithm Completed.")
