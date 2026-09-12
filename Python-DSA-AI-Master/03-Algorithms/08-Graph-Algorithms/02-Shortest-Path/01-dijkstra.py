"""
## A. Concept Name
Dijkstra's Algorithm (Shortest Path)

## B. Introduction & Learning Objectives
What is Dijkstra's Algorithm?
Dijkstra's algorithm is a greedy algorithm used to find the shortest path from a 
single source node to all other nodes in a graph with non-negative edge weights.

Learning Objectives:
- Understand the greedy strategy and relaxation step of Dijkstra's algorithm.
- Implement the algorithm using a priority queue (min-heap) for optimal efficiency.
- Reconstruct the shortest path from a source to a destination.
- Understand its limitations (cannot handle negative edge weights).

## C. Concept Explanation
Algorithm Steps:
1. Initialize distances from the start node to all other nodes as infinity, 
   except the start node itself (distance 0).
2. Use a priority queue to always process the unvisited node with the smallest 
   known distance.
3. For the current node, iterate over all its neighbors. If the known distance 
   to a neighbor is greater than the distance to the current node plus the 
   edge weight, update (relax) the distance.
4. Mark the current node as visited.
5. Repeat until all reachable nodes are visited.

## D. Industry Use Cases
- GPS Navigation: Finding the fastest route between two locations.
- Network Routing protocols: OSPF (Open Shortest Path First) uses Dijkstra's.
- Transportation networks: Flight routing, train schedules.

## E. Implementation & Advanced Concepts
We use Python's built-in `heapq` module to maintain the priority queue.

## F. Complexity Analysis
- Time Complexity: O((V + E) log V), where V is vertices and E is edges. 
  Extracting the minimum from the heap takes O(log V) and happens V times.
  Decreasing the key (pushing a new distance) takes O(log V) and happens E times.
- Space Complexity: O(V + E) for the adjacency list graph representation, and 
  O(V) for distances, predecessors dictionaries, and the priority queue.

## G. Common Mistakes & Interview Questions
Mistake: Using Dijkstra's on graphs with negative weights. 
Dijkstra's algorithm relies on the assumption that once a node is popped from 
the min-heap, its shortest distance is finalized. A negative weight edge could 
provide a shorter path later, breaking this assumption. (Use Bellman-Ford instead).

Interview Challenge:
"Given a 2D grid representing a terrain with different movement costs, find the 
minimum cost to travel from the top-left to the bottom-right corner."
(This is a classic variation where the grid acts as a graph and Dijkstra's 
can be applied directly).

## X. Project Connection
This fundamental graph traversal algorithm will be utilized in our core pathfinding
module to power the network routing visualizer in our final project.
"""

import heapq
from typing import Dict, List, Tuple, Optional

class WeightedGraph:
    """
    Directed weighted graph using an adjacency list.
    """
    def __init__(self) -> None:
        # Dictionary mapping a node to a list of tuples: (neighbor, weight)
        self.adj_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Adds a directed, weighted edge from u to v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append((v, weight))


def dijkstra(graph: WeightedGraph, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Computes shortest paths from `start` to all other nodes.

    Args:
        graph: The weighted graph.
        start: The starting node.

    Returns:
        A tuple containing:
        1. A dictionary mapping each node to its shortest distance from `start`.
        2. A dictionary mapping each node to its predecessor on the shortest path.
    """
    # 1. Initialization
    distances: Dict[str, float] = {node: float('inf') for node in graph.adj_list}
    distances[start] = 0
    
    # Store predecessors to reconstruct the path
    predecessors: Dict[str, Optional[str]] = {node: None for node in graph.adj_list}

    # Priority queue stores tuples of (distance, node)
    # By default, heapq in Python is a min-heap prioritizing the first element
    pq: List[Tuple[float, str]] = [(0, start)]

    # Keep track of nodes that have had their minimum distance finalized
    visited = set()

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # Skip if already fully processed (can happen if multiple updates were pushed)
        if current_node in visited:
            continue
            
        visited.add(current_node)

        # 3. Relaxation Step
        for neighbor, weight in graph.adj_list.get(current_node, []):
            if neighbor in visited:
                continue
                
            distance = current_dist + weight

            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def get_shortest_path(predecessors: Dict[str, Optional[str]], start: str, target: str) -> List[str]:
    """
    Reconstructs the shortest path from start to target.
    """
    path = []
    curr: Optional[str] = target
    
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = predecessors[curr]
        
    path.reverse()
    
    # If the first node in path is not start, it means target is unreachable
    if path and path[0] == start:
        return path
    return []


if __name__ == "__main__":
    g = WeightedGraph()
    # Graph based on a classic example
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 5)
    g.add_edge('B', 'D', 10)
    g.add_edge('C', 'E', 3)
    g.add_edge('E', 'D', 4)
    g.add_edge('D', 'Z', 11)
    
    start_node = 'A'
    dists, preds = dijkstra(g, start_node)
    
    print(f"Shortest distances from {start_node}:")
    for node, d in dists.items():
        print(f"  to {node}: {d}")
        
    assert dists['B'] == 4
    assert dists['C'] == 2
    assert dists['E'] == 5
    assert dists['D'] == 9
    assert dists['Z'] == 20
    
    target_node = 'Z'
    path = get_shortest_path(preds, start_node, target_node)
    print(f"Shortest path from {start_node} to {target_node}: {' -> '.join(path)}")
    assert path == ['A', 'C', 'E', 'D', 'Z']
    
    print("All Dijkstra's algorithm tests passed!")
