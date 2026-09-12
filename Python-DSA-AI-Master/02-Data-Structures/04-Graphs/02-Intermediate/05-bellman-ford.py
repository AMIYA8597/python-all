"""
## A. Concept Name
Bellman-Ford Algorithm

## B. Problem Statement
Find the shortest path from a starting node to all other nodes in a graph, even when edge weights are negative.

## C. Learning Objectives
1. Understand how to compute single-source shortest paths with negative edge weights.
2. Implement Bellman-Ford algorithm to find shortest paths.
3. Detect negative weight cycles in a graph.
4. Compare Bellman-Ford with Dijkstra's algorithm.

## D. Concept Explanation
The Bellman-Ford algorithm finds the shortest paths from a starting node to all other nodes.
Unlike Dijkstra's algorithm, it correctly handles graphs with negative edge weights. 
It works by relaxing all edges |V| - 1 times. If distances can still be shortened after |V| - 1 iterations,
the graph contains a negative-weight cycle.

## E. Basic Implementation
Standard Bellman-Ford to find shortest paths.

## F. Intermediate Implementation
Bellman-Ford with early termination optimization.

## G. Advanced Implementation
Path reconstruction and returning the negative cycle if it exists.

## H. Performance Analysis
- Time Complexity: O(V * E) for relaxing all edges V-1 times.
- Space Complexity: O(V) for storing distances and predecessors.

## I. Edge Cases
- Disconnected components: Distances remain infinity.
- Negative weight cycles: The algorithm correctly identifies them.

## J. Interview Challenge
Network Delay Time using Bellman-Ford (calculating the maximum time for a signal to reach all nodes).

## X. Project Connection
Can be used in financial arbitrage detection systems where negative cycles in a currency exchange graph represent profitable arbitrage opportunities, or in network routing protocols like RIP (Routing Information Protocol).
"""

from typing import Dict, List, Tuple, Any, Optional
import unittest

# Basic Implementation
def bellman_ford_basic(vertices: List[Any], edges: List[Tuple[Any, Any, float]], start: Any) -> Dict[Any, float]:
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0

    # Relax all edges V-1 times
    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    # Check for negative weight cycles
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return distances

# Intermediate Implementation: Early Termination
def bellman_ford_optimized(vertices: List[Any], edges: List[Tuple[Any, Any, float]], start: Any) -> Dict[Any, float]:
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                updated = True
        
        # If no distance was updated in this pass, shortest paths are found
        if not updated:
            break

    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return distances

# Advanced Implementation: Path Reconstruction and Cycle Return
def bellman_ford_advanced(vertices: List[Any], edges: List[Tuple[Any, Any, float]], start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any], List[Any]]:
    distances = {v: float('inf') for v in vertices}
    predecessors = {v: None for v in vertices}
    distances[start] = 0
    cycle = []

    for _ in range(len(vertices) - 1):
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u

    # Check for cycle
    cycle_start = None
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            cycle_start = v
            break

    if cycle_start is not None:
        # We found a node that is part of a negative cycle or reachable from it.
        # Find a node that is actually in the cycle
        node = cycle_start
        for _ in range(len(vertices)):
            node = predecessors[node]

        # Extract cycle
        curr = node
        while True:
            cycle.append(curr)
            curr = predecessors[curr]
            if curr == node and len(cycle) > 1:
                break
        cycle.append(node)
        cycle.reverse()

    return distances, predecessors, cycle

# Interview Challenge
def network_delay_bf(times: List[List[int]], n: int, k: int) -> int:
    """
    Find network delay time using Bellman-Ford
    """
    vertices = list(range(1, n + 1))
    edges = [(u, v, float(w)) for u, v, w in times]
    try:
        dists = bellman_ford_optimized(vertices, edges, k)
        max_dist = max(dists.values())
        return int(max_dist) if max_dist != float('inf') else -1
    except ValueError:
        return -1

# Tests
class TestBellmanFord(unittest.TestCase):
    def setUp(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edges = [
            ('A', 'B', 4),
            ('A', 'C', 5),
            ('B', 'C', -2),
            ('C', 'D', 3),
            ('B', 'D', 4)
        ]

    def test_basic(self):
        dists = bellman_ford_basic(self.vertices, self.edges, 'A')
        self.assertEqual(dists['C'], 2)
        self.assertEqual(dists['D'], 5)

    def test_optimized(self):
        dists = bellman_ford_optimized(self.vertices, self.edges, 'A')
        self.assertEqual(dists['C'], 2)

    def test_negative_cycle(self):
        cycle_edges = [('A', 'B', 1), ('B', 'C', -1), ('C', 'A', -1)]
        with self.assertRaises(ValueError):
            bellman_ford_basic(['A', 'B', 'C'], cycle_edges, 'A')

    def test_advanced_cycle_detection(self):
        cycle_edges = [('A', 'B', 1), ('B', 'C', -1), ('C', 'D', -1), ('D', 'B', -1)]
        dists, preds, cycle = bellman_ford_advanced(['A', 'B', 'C', 'D'], cycle_edges, 'A')
        self.assertTrue(len(cycle) > 0)

if __name__ == '__main__':
    unittest.main()
