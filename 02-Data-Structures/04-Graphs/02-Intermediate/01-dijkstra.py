"""
# ==============================================================================
# LABORATORY: DIJKSTRA'S ALGORITHM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Breadth-First Search (BFS) finds the shortest path, but ONLY if every road has 
# a distance of 1 (unweighted). What if you are building Google Maps, and driving 
# from Node A to Node B takes 5 minutes, but A to C takes 50 minutes? BFS would 
# treat them equally.
# Dijkstra's Algorithm is the foundational algorithm for routing in Weighted Graphs. 
# It guarantees the shortest path from a starting node to ALL other nodes, as long 
# as there are NO negative weights (no time travel!).
# It achieves this by aggressively picking the closest known node using a Min-Heap 
# (Priority Queue).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why a Priority Queue (Min-Heap) is required.
# - Implement Dijkstra's Algorithm in O(E log V) time.
# - Reconstruct the exact path taken to the destination.
#
# ==============================================================================
"""

import heapq
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIJKSTRA'S ALGORITHM IMPLEMENTATION
# ==============================================================================
class WeightedGraph:
    def __init__(self):
        # adj[u] = [(v, weight), ...]
        self.adj = defaultdict(list)
        
    def add_edge(self, u: str, v: str, weight: int):
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight)) # Undirected for this example

def dijkstra(graph: WeightedGraph, start: str, end: str) -> Tuple[int, Optional[List[str]]]:
    """
    Finds the shortest path and distance from `start` to `end`.
    Time Complexity: O(E log V)
    Space Complexity: O(V + E)
    """
    # 1. Initialize distances to all nodes as Infinity
    distances = {node: float('inf') for node in graph.adj}
    distances[start] = 0
    
    # Track the parent node to reconstruct the path later
    parents = {start: None}
    
    # 2. Initialize the Priority Queue (Min-Heap)
    # The heap stores tuples of (current_distance_from_start, node_name)
    # Python's heapq sorts by the first element of the tuple!
    pq = [(0, start)]
    
    # Track nodes we have completely finalized (locked in their shortest path)
    visited = set()
    
    while pq:
        # Pop the node with the absolute SHORTEST known distance
        current_dist, current_node = heapq.heappop(pq)
        
        # If we reached the destination, we can stop early!
        if current_node == end:
            break
            
        # Optimization: Because we push multiple times to the heap when finding 
        # better paths, we might pop an old, outdated tuple. Ignore it.
        if current_node in visited:
            continue
            
        # Mark this node's shortest path as officially "Locked In"
        visited.add(current_node)
        
        # 3. Relax edges (Check all neighbors)
        for neighbor, weight in graph.adj[current_node]:
            # If the neighbor is already finalized, skip it
            if neighbor in visited:
                continue
                
            # Calculate the new distance to reach the neighbor THROUGH current_node
            new_dist = current_dist + weight
            
            # If this new path is faster than the previously known path...
            if new_dist < distances.get(neighbor, float('inf')):
                # Update the distance
                distances[neighbor] = new_dist
                # Update the parent for path reconstruction
                parents[neighbor] = current_node
                # Push the new, better distance onto the priority queue
                heapq.heappush(pq, (new_dist, neighbor))
                
    # Path Reconstruction
    if distances.get(end, float('inf')) == float('inf'):
        return -1, None # Unreachable
        
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parents[curr]
    path.reverse()
    
    return distances[end], path


# ==============================================================================
# 4. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_dijkstra():
    section_header("Algorithm: Dijkstra's Shortest Path")
    
    g = WeightedGraph()
    # A graph representing travel times between cities
    # A --10--> B --50--> C
    # |         |         ^
    # 20        10        |
    # v         v         |
    # D --20--> E --10----+
    
    g.add_edge('A', 'B', 10)
    g.add_edge('A', 'D', 20)
    g.add_edge('B', 'C', 50)
    g.add_edge('B', 'E', 10)
    g.add_edge('D', 'E', 20)
    g.add_edge('E', 'C', 10)
    
    print("Finding shortest route from A to C...")
    print("Notice that visually, A -> B -> C is the fewest 'jumps' (DFS/BFS path).")
    print("But taking that route takes 10 + 50 = 60 minutes.\n")
    
    distance, path = dijkstra(g, 'A', 'C')
    
    print(f"Shortest Distance Found: {distance} minutes")
    print(f"Optimal Path: {' -> '.join(path)}")
    print("\nDijkstra correctly ignored the fewest jumps and found the mathematically shortest time (10+10+10=30)!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Dijkstra's Algorithm use a Min-Heap (Priority Queue) instead of a standard Queue?
   Answer: A standard BFS Queue processes nodes in the exact order they were discovered. If you use it on weighted edges, it might explore a path that takes 100 minutes before exploring a path that takes 5 minutes. The Min-Heap guarantees that the algorithm ALWAYS explores the node that is mathematically closest to the start first (Greedy choice).

2. Why does Dijkstra's Algorithm fail if the graph has Negative Weights?
   Answer: Dijkstra assumes that once a node is popped from the Min-Heap, its shortest path is absolutely finalized. It assumes adding more edges to a path can only INCREASE the total distance. If negative weights exist, taking a longer, winding path might suddenly DECREASE the total distance, completely violating Dijkstra's core assumption.

3. Why do we push `(new_dist, neighbor)` to the heap instead of updating an existing node in the heap?
   Answer: In computer science, finding and updating a specific element inside a standard Binary Heap takes O(N) time. It is much faster to just push a duplicate, better tuple onto the heap (O(log N)). Because it has a smaller distance, the better tuple will pop off first. When the old, worse tuple pops off later, our `if current_node in visited` check safely ignores it.
"""

if __name__ == "__main__":
    demonstrate_dijkstra()
    print("\n[SUCCESS] Laboratory: Dijkstra's Algorithm Completed.")
