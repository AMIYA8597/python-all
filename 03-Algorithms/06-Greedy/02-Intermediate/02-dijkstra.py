"""
# ==============================================================================
# LABORATORY: DIJKSTRA'S ALGORITHM (GREEDY GRAPH TRAVERSAL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are using Google Maps. You want the fastest route from New York to LA.
# How does Google calculate it instantly among millions of roads?
#
# In 1956, Edsger W. Dijkstra invented a brilliant algorithm to find the 
# Shortest Path in a graph.
# It is fundamentally a Greedy Algorithm!
# 
# How? At every single step, the algorithm asks: "Of all the cities I know 
# exist right now, which one has the absolute SHORTEST total distance from 
# the start?" It greedily locks in that city, and then explores its neighbors.
#
# Because it always explores the absolutely closest nodes first (using a Min-Heap 
# Priority Queue), by the time it reaches your destination, it is mathematically 
# guaranteed to have found the shortest possible path.
#
# However, because it is Greedy, it has a fatal flaw: Negative Weights.
# If a road gives you "negative distance" (a time-travel wormhole), the Greedy 
# assumption shatters, and Dijkstra will return the wrong answer. (You must use 
# Bellman-Ford DP instead).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Dijkstra is a Greedy Algorithm.
# - Implement O((V+E) log V) Traversal using `heapq`.
# - Understand the "Relaxation" of edges.
#
# ==============================================================================
"""

import heapq
import math
from typing import List, Dict, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIJKSTRA'S SHORTEST PATH (O((V+E) log V))
# ==============================================================================
def dijkstra(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> Dict[str, int]:
    """
    Finds the shortest distance from `start_node` to EVERY other node in the graph.
    `graph` is an Adjacency List: {'A': [('B', 4), ('C', 1)]}
    
    Time Complexity: O((V + E) log V) where V=Vertices, E=Edges
    Space Complexity: O(V) for distances and heap.
    """
    
    # 1. INITIALIZATION
    # We assume the distance to every node is INFINITY.
    distances = {node: math.inf for node in graph}
    # The distance to the start node is always 0!
    distances[start_node] = 0
    
    # The Priority Queue (Min-Heap). 
    # Stores tuples of (current_shortest_distance, node)
    pq = [(0, start_node)]
    
    # 2. THE GREEDY TRAVERSAL LOOP
    while pq:
        
        # --- THE GREEDY CHOICE ---
        # Pop the node with the absolute smallest distance from the heap.
        # This is an O(log V) operation!
        current_dist, current_node = heapq.heappop(pq)
        
        # Optimization (Lazy Deletion):
        # Because we can't easily update values inside Python's `heapq`, we just 
        # push duplicate nodes with better distances. If we pop an older, worse 
        # distance, we just ignore it!
        if current_dist > distances[current_node]:
            continue
            
        # 3. EXPLORE NEIGHBORS
        for neighbor, weight in graph[current_node]:
            
            # Calculate the total distance to reach this neighbor THROUGH the current node.
            distance_through_current = current_dist + weight
            
            # --- EDGE RELAXATION ---
            # Is this new path strictly faster than the neighbor's current known path?
            if distance_through_current < distances[neighbor]:
                
                # YES! We "relax" the edge. We overwrite the distance.
                distances[neighbor] = distance_through_current
                
                # Push this better path into the priority queue so it can be evaluated!
                heapq.heappush(pq, (distance_through_current, neighbor))
                
    return distances


def demonstrate_dijkstra():
    section_header("Algorithm: Dijkstra's Shortest Path")
    
    # Adjacency List (Directed Graph)
    # A -> B costs 4. A -> C costs 1.
    graph = {
        'A': [('B', 4), ('C', 1)],
        'B': [('D', 1)],
        'C': [('B', 2), ('D', 5)],
        'D': []
    }
    
    print("Graph Structure:")
    for node, edges in graph.items():
        print(f" {node} -> {edges}")
        
    start = 'A'
    print(f"\nExecuting Dijkstra starting from {start}...")
    shortest_paths = dijkstra(graph, start)
    
    print("\nShortest Distances:")
    for node, dist in shortest_paths.items():
        print(f" {start} to {node}: {dist}")
        
    print("\nExplanation of C to B:")
    print("A direct path from A to B is 4.")
    print("But A -> C (1) -> B (2) is 3! Dijkstra correctly 'Relaxed' the B edge.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does "Edge Relaxation" mean?
   Answer: "Relaxation" is the mathematical process of testing if a new path to a node is strictly better than the currently known path. If `current_dist + weight < known_dist`, the tension of the edge is "relaxed", and the distance is overwritten. 

2. Why exactly does Dijkstra fail on negative weights?
   Answer: Dijkstra is a GREEDY algorithm. It assumes that once a node is popped from the Min-Heap, its shortest path is permanently, irreversibly locked in. It assumes that ANY future path to it would only increase the distance (because weights are positive). If you have a negative weight edge later in the graph, a path could magically become shorter! But Dijkstra has already locked the node and will never re-process it, resulting in the wrong answer.

3. Why is the Time Complexity $O((V+E) \\log V)$ instead of just $O(E \\log V)$?
   Answer: In the worst-case scenario (a dense graph), you might push a new updated distance into the Priority Queue every single time you evaluate an edge. That's $E$ pushes. A Heap push/pop takes $O(\\log V)$ time. Therefore, the heap operations take $O(E \\log V)$. Popping all $V$ vertices takes $O(V \\log V)$. Combined, it is mathematically written as $O((V+E) \\log V)$.
"""

if __name__ == "__main__":
    demonstrate_dijkstra()
    print("\n[SUCCESS] Laboratory: Dijkstra's Algorithm Completed.")
