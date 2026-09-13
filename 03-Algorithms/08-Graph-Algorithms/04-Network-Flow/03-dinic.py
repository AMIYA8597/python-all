"""
# ==============================================================================
# LABORATORY: DINIC'S ALGORITHM (FAANG-GRADE MAX FLOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Edmonds-Karp uses BFS to guarantee O(V * E^2) time.
# But it has a fatal inefficiency: Every time it runs BFS, it finds ONE single 
# path, pushes water through it, and immediately throws the BFS map away.
# If there are 10 valid paths of the exact same length, Edmonds-Karp will 
# wastefully run BFS 10 separate times!
#
# In 1970, the Soviet computer scientist Yefim Dinitz invented a masterpiece 
# algorithm that combined BFS and DFS into an unstoppable engine.
#
# PHASE 1 (BFS):
# Dinic's runs a BFS. But instead of stopping at the sink, it creates a "Level Graph". 
# It assigns an integer to every single node representing its exact distance from 
# the source. (Source=0, A=1, B=1, Sink=2).
#
# PHASE 2 (DFS):
# Now, we unleash a DFS. But this DFS is mathematically constrained: It is ONLY 
# allowed to travel to nodes whose Level is exactly +1 higher than its current node.
# Water is ONLY allowed to flow strictly downhill!
#
# The DFS aggressively pumps water down EVERY single path it can find in the 
# Level Graph until the entire graph is completely dry. 
#
# Because the DFS is blocked from going backward or sideways, it is blistering fast. 
# Total Time Complexity: O(V^2 * E). 
# This completely crushes Edmonds-Karp on dense graphs. It is the absolute 
# standard for Competitive Programming and Production AI routing.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the BFS Level Graph.
# - Implement the Constrained DFS.
# - Master the `ptr` (Dead End) Optimization for DFS.
#
# ==============================================================================
"""

import math
from collections import deque
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DINIC'S HYBRID ENGINE (O(V^2 * E))
# ==============================================================================
def build_level_graph(residual_graph: List[List[int]], source: int, sink: int, levels: List[int]) -> bool:
    """
    PHASE 1 (BFS): Builds the exact distance layers from the Source.
    Returns True if the Sink is reachable.
    """
    vertices = len(residual_graph)
    
    # Reset all levels to -1 (unreached)
    for i in range(vertices):
        levels[i] = -1
        
    levels[source] = 0
    queue = deque([source])
    
    while queue:
        current = queue.popleft()
        
        for neighbor, capacity in enumerate(residual_graph[current]):
            # If unvisited AND pipe has capacity!
            if levels[neighbor] < 0 and capacity > 0:
                # The neighbor is strictly 1 level deeper than the current node!
                levels[neighbor] = levels[current] + 1
                queue.append(neighbor)
                
    # If the sink's level is still -1, it means the graph is completely blocked!
    return levels[sink] >= 0


def push_flow_dfs(residual_graph: List[List[int]], current: int, sink: int, flow_in: int, levels: List[int], ptr: List[int]) -> int:
    """
    PHASE 2 (DFS): Aggressively pushes flow through the Level Graph.
    Uses `ptr` to remember Dead Ends and avoid checking them twice!
    """
    if current == sink or flow_in == 0:
        return flow_in
        
    # The `ptr` array is the secret weapon!
    # If Node 2 has 5 neighbors, and we already checked neighbors 0, 1, and 2 
    # and found them blocked, `ptr[2]` will be 3. 
    # Next time DFS visits Node 2, it instantly skips the blocked pipes!
    for i in range(ptr[current], len(residual_graph[current])):
        ptr[current] = i # Save our progress!
        
        neighbor = i
        capacity = residual_graph[current][neighbor]
        
        # CONSTRAINED MOVEMENT!
        # The DFS is ONLY allowed to move strictly to a node exactly +1 level deeper.
        if levels[neighbor] == levels[current] + 1 and capacity > 0:
            
            # Recurse deeper! The bottleneck is the MINIMUM of the flow coming in 
            # and the physical capacity of this pipe!
            bottleneck = min(flow_in, capacity)
            pushed_flow = push_flow_dfs(residual_graph, neighbor, sink, bottleneck, levels, ptr)
            
            if pushed_flow > 0:
                # 1. Forward pipe loses capacity
                residual_graph[current][neighbor] -= pushed_flow
                # 2. Phantom backward pipe gains capacity
                residual_graph[neighbor][current] += pushed_flow
                
                return pushed_flow
                
    # If we check every neighbor and find nothing, this node is a DEAD END!
    return 0


def dinics_algorithm(vertices: int, graph: List[List[int]], source: int, sink: int) -> int:
    """
    Time Complexity: O(V^2 * E).
    Space Complexity: O(V^2) for the Adjacency Matrix.
    """
    residual_graph = [[graph[i][j] for j in range(vertices)] for i in range(vertices)]
    levels = [-1] * vertices
    max_flow = 0
    
    # 1. THE INFINITE PUMPING LOOP
    # We keep building Level Graphs until the Sink is mathematically unreachable!
    while build_level_graph(residual_graph, source, sink, levels):
        
        # Reset the Dead End pointers for the new DFS Phase!
        ptr = [0] * vertices
        
        # 2. AGGRESSIVE DFS
        # We loop the DFS over and over until it literally cannot find a single 
        # drop of water to push through this specific Level Graph!
        while True:
            pushed = push_flow_dfs(residual_graph, source, sink, math.inf, levels, ptr)
            if pushed == 0:
                break # This Level Graph is utterly dry. Time to rebuild it via BFS!
            max_flow += pushed
            
    return max_flow


def demonstrate_dinic():
    section_header("Algorithm: Dinic's Algorithm (Max Flow)")
    
    vertices = 6
    # Same graph as previous labs for verification!
    graph = [
        [0, 16, 13, 0,  0,  0 ], 
        [0, 0,  10, 12, 0,  0 ], 
        [0, 4,  0,  0,  14, 0 ], 
        [0, 0,  9,  0,  0,  20], 
        [0, 0,  0,  7,  0,  4 ], 
        [0, 0,  0,  0,  0,  0 ]  
    ]
    
    source = 0
    sink = 5
    
    print("Graph Capacities Matrix:")
    for row in graph: print(row)
        
    print(f"\nExecuting Dinic's Hybrid BFS+DFS Algorithm (S={source} -> T={sink})...")
    max_flow = dinics_algorithm(vertices, graph, source, sink)
    
    print(f"\nAbsolute Maximum Water Flow: {max_flow} gallons/sec")
    print("(Expected: 23)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Dinic's use a Hybrid of BFS and DFS?
   Answer: BFS guarantees the absolute shortest paths, preventing infinite loops. DFS is insanely fast at aggressively pushing water down a fixed path. By having BFS pre-calculate a "Level Graph", it creates a safe playground for the DFS. The DFS can wildly explore the graph, but because it is mathematically constrained by the `level + 1` rule, it is physically impossible for the DFS to spiral into a loop or backtrack. It is the best of both worlds.

2. What is the `ptr` array (Dead End Optimization)?
   Answer: During the DFS phase, we might visit Node A and discover that paths 1, 2, and 3 are completely blocked/full. We backtrack. A microsecond later, a completely different path in the graph might lead the DFS back to Node A! Without `ptr`, the DFS would stupidly re-check paths 1, 2, and 3 again! The `ptr` array saves our exact index in the `for` loop. When the DFS returns to Node A, it instantly resumes at path 4. This optimization is mandatory to achieve the $O(V^2 E)$ time bound.

3. For Bipartite Matching (assigning 500 Uber drivers to 500 passengers), which Max Flow algorithm should you use?
   Answer: Dinic's Algorithm! In a special "Unit Capacity Network" (where every pipe capacity is exactly 1, which happens in Bipartite Matching), Dinic's time complexity mathematically drops from $O(V^2 E)$ down to a mind-blowing $O(E \\sqrt{V})$. It is the undisputed king of assignment algorithms (Hopcroft-Karp is essentially just Dinic's algorithm optimized for Bipartite graphs).
"""

if __name__ == "__main__":
    demonstrate_dinic()
    print("\n[SUCCESS] Laboratory: Dinic's Algorithm Completed.")
