"""
# ==============================================================================
# LABORATORY: DIJKSTRA'S ALGORITHM (WEIGHTED SHORTEST PATH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Breadth-First Search (BFS) finds the shortest path perfectly, BUT only if 
# every edge has the exact same distance (unweighted).
# If you are mapping a GPS route, the road from A to B might be 5 miles, 
# but the road from A to C is 50 miles. BFS would treat them as equal "1 step", 
# giving you a terribly incorrect driving route.
#
# Enter Edsger W. Dijkstra (1956).
# Dijkstra's Algorithm is essentially BFS, but instead of using a standard FIFO 
# Queue, it uses a Priority Queue (Min-Heap).
#
# It doesn't expand in uniform concentric rings. It expands greedily along the 
# absolute shortest physical distance mathematically available at any given moment.
#
# This perfectly powers Google Maps, Internet Routing (OSPF), and AI pathfinding.
#
# The One Fatal Flaw: Dijkstra blindly trusts that taking a longer path will 
# never somehow magically reduce your total distance. Therefore, it mathematically 
# breaks if the graph has "Negative Weight Edges" (e.g., a time-travel wormhole 
# that subtracts 50 miles from your odometer).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Min-Heap (Priority Queue) in Python (`heapq`).
# - Maintain a global `distances` dictionary initialized to Infinity.
# - Reconstruct the optimal weighted path.
# - Prove why Negative Edges shatter the algorithm.
#
# ==============================================================================
"""

import heapq
import math
from typing import Dict, List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIJKSTRA'S SHORTEST PATH ENGINE (O((V+E) log V))
# ==============================================================================
def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Tuple[Dict[int, float], Dict[int, int]]:
    """
    Computes the shortest path from the `start` node to ALL OTHER NODES in the graph!
    Graph format: {node: [(neighbor, edge_weight), ...]}
    Returns: (distances_dict, parent_map)
    """
    
    # 1. INITIALIZE DISTANCES TO INFINITY
    # At the start, we assume every node in the world is infinitely far away.
    distances = {node: math.inf for node in graph}
    # Except the start node, which is 0 miles away from itself!
    distances[start] = 0
    
    # We track parents to reconstruct the actual GPS driving route later
    parent_map = {start: None}
    
    # 2. THE MIN-HEAP (Priority Queue)
    # Python's `heapq` sorts tuples by their FIRST element.
    # Therefore, we push (current_distance, node)
    pq = [(0, start)]
    
    # 3. THE GREEDY LOOP
    while pq:
        # Pop the mathematically closest un-finalized node in the entire graph
        current_dist, current_node = heapq.heappop(pq)
        
        # STALE RECORD OPTIMIZATION
        # Because we push things to the heap without manually updating existing 
        # records (which is O(N) slow in Python), the heap might contain "stale" 
        # copies of nodes with worse distances. We instantly ignore them!
        if current_dist > distances[current_node]:
            continue
            
        # 4. EXPLORE NEIGHBORS (Edge Relaxation)
        for neighbor, weight in graph.get(current_node, []):
            # Calculate the total distance to reach this neighbor VIA the current node
            distance_via_current = current_dist + weight
            
            # If this new path is strictly FASTER than the current known record...
            if distance_via_current < distances[neighbor]:
                # UPDATE THE RECORD!
                distances[neighbor] = distance_via_current
                parent_map[neighbor] = current_node
                
                # Push the new, better route into the Priority Queue
                heapq.heappush(pq, (distance_via_current, neighbor))
                
    return distances, parent_map


def get_shortest_path(parent_map: Dict[int, int], target: int) -> List[int]:
    """Reconstructs the path by walking backward from Target to Start."""
    if target not in parent_map:
        return [] # Unreachable
        
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent_map[curr]
        
    return path[::-1]


def demonstrate_dijkstra():
    section_header("Algorithm: Dijkstra's Shortest Path")
    
    # Adjacency List: {Node: [(Neighbor, Weight)]}
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 5), ('D', 10)],
        'C': [('E', 3)],
        'E': [('D', 4)],
        'D': []
    }
    
    start = 'A'
    target = 'D'
    
    print(f"Executing Dijkstra from Node {start}...")
    distances, parents = dijkstra(graph, start)
    
    print(f"\nFinal Distances from {start}:")
    for node, dist in distances.items():
        print(f" -> to {node}: {dist} miles")
        
    route = get_shortest_path(parents, target)
    print(f"\nOptimal Route {start} -> {target}: {' -> '.join(route)}")
    print(f"Total Mileage: {distances[target]}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Dijkstra break if there is a Negative Edge?
   Answer: Dijkstra is fundamentally a Greedy algorithm. The moment it pops a node from the Priority Queue, it firmly declares: "I have found the absolute shortest path to this node. I will NEVER evaluate this node again." If a negative edge exists somewhere deep in the graph that loops back and provides a shorter path to this "finalized" node, Dijkstra will completely ignore it, returning an incorrect mathematically impossible route.

2. Why is the time complexity $O((V+E) \\log V)$?
   Answer: We explore every vertex $V$ and every edge $E$. For every single edge relaxation, we push a new tuple into the Min-Heap. The heap can physically grow to a size of $V$ (or $E$ if using lazy stale-record pushes). Pushing/popping from a heap takes $O(\\log N)$ time. Therefore, processing $V+E$ elements through a $\\log V$ heap yields $O((V+E) \\log V)$.

3. How does the "Stale Record" optimization `if current_dist > distances[current_node]` work?
   Answer: In theoretical computer science, a Priority Queue has a `decrease_key` function to update a node's distance in $O(\\log V)$ time. Python's `heapq` module DOES NOT have this! Instead of updating, we just lazily push a duplicate tuple with the new better distance. When the better tuple pops, it finalizes the node. Later, the old "worse" tuple will pop. The `if` check instantly detects that the popped distance is worse than the finalized distance in the dictionary, and safely discards it in $O(1)$ time!
"""

if __name__ == "__main__":
    demonstrate_dijkstra()
    print("\n[SUCCESS] Laboratory: Dijkstra's Algorithm Completed.")
