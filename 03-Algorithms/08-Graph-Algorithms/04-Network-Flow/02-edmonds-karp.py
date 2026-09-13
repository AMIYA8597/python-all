"""
# ==============================================================================
# LABORATORY: EDMONDS-KARP (STRONGLY POLYNOMIAL MAX FLOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned the fatal flaw of Ford-Fulkerson.
# It uses Depth-First Search (DFS) to find paths. If there is a massive 1-Billion 
# gallon pipe network, but the DFS gets unlucky and finds a path that routes 
# exactly 1 gallon of water back and forth across the middle, the `while` loop 
# will literally execute 2 Billion times!
#
# The time complexity $O(E \\times MaxFlow)$ is "Pseudo-Polynomial", meaning the 
# algorithm's speed depends on the SIZE of the numbers in the data, not just 
# the number of nodes!
#
# In 1972, Jack Edmonds and Richard Karp published a 1-line fix to this algorithm.
# 
# Do not use DFS. Use Breadth-First Search (BFS).
#
# By using BFS (a Queue instead of a Stack), the algorithm is mathematically 
# forced to always pick the absolute SHORTEST physical path (fewest edges) from 
# the Source to the Sink.
# It becomes physically impossible to enter pathological zig-zag 1-gallon loops!
#
# The time complexity instantly becomes $O(V \\times E^2)$. 
# It is completely independent of the pipe capacities! Even if the pipes hold 
# 10 Trillion gallons, it runs in the exact same amount of time. This is called 
# "Strongly Polynomial".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Replace DFS with a `collections.deque` BFS.
# - Understand the difference between Pseudo-Polynomial and Strongly Polynomial.
# - Master the ultimate production-grade Max Flow implementation.
#
# ==============================================================================
"""

import math
from collections import deque
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EDMONDS-KARP ENGINE (BFS MAX FLOW)
# ==============================================================================
def bfs_augmenting_path(residual_graph: List[List[int]], source: int, sink: int, parent_map: List[int]) -> bool:
    """
    Standard BFS that finds the SHORTEST path (fewest edges) from Source to Sink.
    Time Complexity: O(V + E)
    """
    vertices = len(residual_graph)
    visited = [False] * vertices
    
    # 1. THE QUEUE (Breadth-First Expansion)
    queue = deque([source])
    visited[source] = True
    
    while queue:
        current = queue.popleft()
        
        # 2. EXPLORE NEIGHBORS (Concentric Rings)
        for neighbor, capacity in enumerate(residual_graph[current]):
            
            # If unvisited AND pipe is not full...
            if not visited[neighbor] and capacity > 0:
                # Record exactly how we reached this neighbor
                parent_map[neighbor] = current
                visited[neighbor] = True
                
                # If we hit the sink, we immediately halt the BFS!
                # We are mathematically guaranteed this is the shortest path!
                if neighbor == sink:
                    return True
                    
                queue.append(neighbor)
                
    return False


def edmonds_karp(vertices: int, graph: List[List[int]], source: int, sink: int) -> int:
    """
    Time Complexity: O(V * E^2). Strongly Polynomial!
    Space Complexity: O(V^2) for the Adjacency Matrix.
    """
    
    # 1. CREATE RESIDUAL GRAPH
    residual_graph = [[graph[i][j] for j in range(vertices)] for i in range(vertices)]
    parent_map = [-1] * vertices
    max_flow = 0
    
    # 2. THE BFS PUMPING LOOP
    # We keep running BFS until no path exists!
    while bfs_augmenting_path(residual_graph, source, sink, parent_map):
        
        # 3. FIND THE BOTTLENECK
        path_flow = math.inf
        curr = sink
        
        while curr != source:
            prev = parent_map[curr]
            path_flow = min(path_flow, residual_graph[prev][curr])
            curr = prev
            
        # 4. PUSH WATER & CREATE PHANTOM PIPES
        max_flow += path_flow
        
        curr = sink
        while curr != source:
            prev = parent_map[curr]
            
            # Forward pipe loses capacity
            residual_graph[prev][curr] -= path_flow
            
            # Phantom backward pipe gains capacity
            residual_graph[curr][prev] += path_flow
            
            curr = prev
            
    return max_flow


def demonstrate_edmonds_karp():
    section_header("Algorithm: Edmonds-Karp (Strongly Polynomial)")
    
    vertices = 6
    # Same graph as previous lab!
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
        
    print(f"\nExecuting Edmonds-Karp BFS Algorithm (S={source} -> T={sink})...")
    max_flow = edmonds_karp(vertices, graph, source, sink)
    
    print(f"\nAbsolute Maximum Water Flow: {max_flow} gallons/sec")
    print("(Expected: 23)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does replacing DFS with BFS fix the Pseudo-Polynomial flaw?
   Answer: In the catastrophic failure case, the graph has a middle pipe with 1 capacity connecting two massive 1-Billion capacity pipes. DFS is a stack. It dives deep and randomly zig-zags across that middle pipe, finding a 3-edge path that only holds 1 gallon. BFS explores in concentric rings. It will naturally discover the direct 2-edge paths (e.g., S -> A -> T) and fill them to 1-Billion capacity IMMEDIATELY on the very first iterations! The 1-capacity middle pipe is mathematically pushed to the back of the queue and ignored until the massive pipes are full.

2. Why is the time complexity $O(V \\times E^2)$?
   Answer: A single run of BFS takes $O(E)$ time. Edmonds and Karp published a mathematical proof in 1972 demonstrating that if you strictly use BFS, the absolute maximum number of times the BFS can possibly execute before the network is completely saturated is bounded by $O(V \\times E)$. Therefore, multiplying the number of runs by the time of a single run yields $O(V \\times E^2)$. 

3. Is Edmonds-Karp the absolute fastest Max Flow algorithm?
   Answer: No! While $O(V E^2)$ is standard for most textbooks, modern FAANG applications use Dinic's Algorithm. Dinic's runs multiple BFS layers to create a "Level Graph", and then runs a massive parallelized DFS on that specific level graph. Dinic's achieves $O(V^2 E)$, which completely crushes Edmonds-Karp on dense graphs. Further advanced algorithms like Push-Relabel achieve $O(V^3)$.
"""

if __name__ == "__main__":
    demonstrate_edmonds_karp()
    print("\n[SUCCESS] Laboratory: Edmonds-Karp Algorithm Completed.")
