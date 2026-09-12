"""
## A. Concept Name
Shortest Paths in Graphs

## B. Learning Objectives
1. Understand the Shortest Path problem in graphs.
2. Implement Dijkstra's algorithm using a Priority Queue.
3. Handle graph traversal optimally to find the minimum distance from a source to all vertices.
4. Analyze time and space complexity of Dijkstra's algorithm.

## C. Concept Explanation
Dijkstra's Algorithm finds the shortest path from a starting vertex to all other vertices in a graph
with non-negative edge weights. It greedily selects the unvisited vertex with the smallest known distance
and updates the distances of its adjacent vertices.

## D. Implementations
Basic Implementation: Dijkstra without priority queue (O(V^2)).
Intermediate Implementation: Dijkstra with priority queue (O(E log V)).
Advanced Implementation: Dijkstra recovering the actual shortest path.

## E. Performance Analysis
- Time Complexity: O((V + E) log V) with a binary heap priority queue.
- Space Complexity: O(V) for the distance dictionary and priority queue.

## F. Edge Cases
- Disconnected graphs: Unreachable nodes will have an infinite distance.
- Cyclic graphs: Handled gracefully as long as weights are non-negative.
- Negative weights: Dijkstra's fails here (requires Bellman-Ford).

## X. Project Connection
Shortest paths algorithms are heavily used in real-world applications like GPS mapping, network routing, and AI pathfinding projects where you must minimize costs to reach a destination.
"""

import heapq
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
import unittest

# Basic Implementation (O(V^2))
def dijkstra_basic(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> Dict[Any, float]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()

    for _ in range(len(graph)):
        # Find minimum distance unvisited node
        min_node = None
        min_dist = float('inf')
        for node in graph:
            if node not in visited and distances[node] < min_dist:
                min_dist = distances[node]
                min_node = node
        
        if min_node is None:
            break
            
        visited.add(min_node)
        for neighbor, weight in graph[min_node]:
            if neighbor not in distances:
                distances[neighbor] = float('inf')
            new_dist = distances[min_node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                
    return distances


# Intermediate Implementation (O(E log V))
def dijkstra_pq(graph: Dict[Any, List[Tuple[Any, float]]], start: Any) -> Dict[Any, float]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)] # (distance, node)
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Optimization: skip if we found a shorter path already
        if current_distance > distances.get(current_node, float('inf')):
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in distances:
                distances[neighbor] = float('inf')
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances


# Advanced Implementation
def dijkstra_path(graph: Dict[Any, List[Tuple[Any, float]]], start: Any, end: Any) -> Tuple[float, List[Any]]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous_nodes = {node: None for node in graph}
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node == end:
            break
            
        if current_distance > distances.get(current_node, float('inf')):
            continue
            
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in distances:
                distances[neighbor] = float('inf')
                previous_nodes[neighbor] = None
                
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    # Reconstruct path
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = previous_nodes.get(curr)
    path.reverse()
    
    if path and path[0] == start:
        return distances[end], path
    return float('inf'), []

# Interview Challenge
def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Given a network of n nodes, labeled from 1 to n. 
    times[i] = (u, v, w), the time it takes for a signal to travel from node u to node v.
    Return the time it takes for all nodes to receive the signal starting from k.
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
        if v not in graph:
            graph[v] = [] # ensure vertex exists
    if k not in graph:
        graph[k] = []
        
    distances = dijkstra_pq(graph, k)
    if len(distances) < n:
        return -1
    max_dist = max(distances.values())
    return max_dist if max_dist != float('inf') else -1

# Tests
class TestShortestPaths(unittest.TestCase):
    def setUp(self):
        self.graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }

    def test_dijkstra_basic(self):
        dists = dijkstra_basic(self.graph, 'A')
        self.assertEqual(dists['D'], 4)

    def test_dijkstra_pq(self):
        dists = dijkstra_pq(self.graph, 'A')
        self.assertEqual(dists['C'], 3)
        self.assertEqual(dists['D'], 4)

    def test_dijkstra_path(self):
        dist, path = dijkstra_path(self.graph, 'A', 'D')
        self.assertEqual(dist, 4)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])

    def test_network_delay(self):
        times = [[2,1,1],[2,3,1],[3,4,1]]
        self.assertEqual(network_delay_time(times, 4, 2), 2)

if __name__ == '__main__':
    unittest.main()
