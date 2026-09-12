"""
## A. Concept Name
Dijkstra's Algorithm (Single-Source Shortest Path)

## B. Real-World Analogy
Think of a GPS navigation system finding the quickest route to your destination. It evaluates different roads, avoiding long detours and prioritizing the shortest travel times, iteratively updating its best guess as it "explores" intersections.

## C. Theoretical Background
Dijkstra's algorithm is a greedy algorithm that solves the single-source shortest path problem for a graph with non-negative edge weights. It iteratively selects the unvisited node with the lowest distance, calculates the distance through it to each unvisited neighbor, and updates the neighbor's distance if a shorter path is found.

## D. Time & Space Complexity
- Time Complexity: O((V + E) log V) when using a Priority Queue (min-heap).
- Space Complexity: O(V) for storing the distance map and priority queue.

## X. Project Connection
In AI applications, Dijkstra's algorithm is foundational for pathfinding (e.g., in robotics, autonomous vehicles, or game AI) and routing problems. It serves as the baseline for more advanced, heuristic-based algorithms like A* (A-Star), which are widely used for navigating intelligent agents through complex environments.
"""

import heapq

def dijkstra(graph, start):
    """
    Finds the shortest paths from a starting node to all other nodes in a weighted graph.
    
    Args:
        graph (dict): An adjacency list representation of the graph.
                      Format: {node: {neighbor: weight, ...}, ...}
        start (str/int): The starting node.
        
    Returns:
        dict: A dictionary of the shortest distances from the start node to all other nodes.
    """
    # Initialize distances with infinity, except for the start node (distance 0)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Priority queue to hold (distance, node) tuples
    # This ensures we always process the unvisited node with the smallest known distance
    pq = [(0, start)]
    
    # Track visited nodes to prevent redundant processing
    visited = set()
    
    while pq:
        # Extract the node with the smallest tentative distance
        current_distance, current_node = heapq.heappop(pq)
        
        # If node is already fully processed, skip it
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Check all neighboring nodes
        for neighbor, weight in graph[current_node].items():
            if neighbor in visited:
                continue
                
            # Calculate the distance to the neighbor through the current node
            distance = current_distance + weight
            
            # If a shorter path is found, update it and push to the priority queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances


if __name__ == "__main__":
    # Example usage:
    # Graph representation: A dictionary where each key is a node, 
    # and the value is another dictionary of neighboring nodes and their edge weights.
    example_graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
        'E': {'C': 10, 'D': 2, 'Z': 3},
        'Z': {'D': 6, 'E': 3}
    }
    
    start_node = 'A'
    shortest_paths = dijkstra(example_graph, start_node)
    
    print(f"Shortest paths from node '{start_node}':")
    for node, distance in shortest_paths.items():
        print(f"  -> Distance to {node}: {distance}")
