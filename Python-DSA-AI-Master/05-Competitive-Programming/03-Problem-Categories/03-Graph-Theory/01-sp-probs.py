"""
===========================================================================
CHAPTER 5, SECTION 3.1: GRAPH THEORY - SHORTEST PATH ALGORITHMS
===========================================================================

## A. Concept Name
Shortest Path Algorithms in Graph Theory

## B. Concept Explanation
Graph theory problems often require finding the shortest path between nodes. 
Depending on the properties of the graph (directed/undirected, positive/negative weights, 
dense/sparse), different algorithms are optimal. This chapter explores four fundamental 
algorithms for Shortest Path problems:
1. **Dijkstra's Algorithm**: Single-Source Shortest Path (SSSP) for graphs with non-negative edge weights.
2. **Bellman-Ford Algorithm**: SSSP for graphs that may contain negative weight edges. It can also detect negative-weight cycles.
3. **SPFA (Shortest Path Faster Algorithm)**: An optimization of Bellman-Ford using a queue.
4. **Floyd-Warshall Algorithm**: All-Pairs Shortest Path (APSP) using Dynamic Programming.

### The Mathematics of Shortest Paths
Let G = (V, E) be a directed or undirected graph where V is the set of vertices and E is the set of edges.
Let w(u, v) be the weight (or cost/distance) of the edge from u to v.
A path p = <v_0, v_1, ..., v_k> is a sequence of vertices such that (v_{i-1}, v_i) ∈ E for i = 1, 2, ..., k.
The weight of a path w(p) is the sum of the weights of its constituent edges:
    w(p) = Σ (from i=1 to k) w(v_{i-1}, v_i)

The shortest-path weight δ(u, v) from u to v is defined as:
    δ(u, v) = min { w(p) : p is a path from u to v } if there is a path from u to v
    δ(u, v) = ∞ if no path exists.
    δ(u, v) = -∞ if the path goes through a negative weight cycle.

### The Relaxation Property
The fundamental operation in SSSP algorithms is "relaxation". 
For an edge (u, v) with weight w:
    if distance[v] > distance[u] + w:
        distance[v] = distance[u] + w
        predecessor[v] = u
By systematically relaxing edges in different orders, different algorithms guarantee finding δ(s, v).

## C. Learning Objectives
1. Implement Dijkstra's algorithm using an adjacency list and Min-Heap.
2. Implement Bellman-Ford and extract negative weight cycles.
3. Master the Floyd-Warshall DP matrix formulation and path reconstruction.
4. Understand SPFA and when its average-case speedup is useful.
5. Apply these algorithms to classic problems (e.g., Network Delay Time, Currency Arbitrage).

## D. Complexity Analysis
| Algorithm      | Use Case                           | Time Complexity | Space Complexity |
|----------------|------------------------------------|-----------------|------------------|
| Dijkstra       | Non-negative SSSP                  | O((V+E) log V)  | O(V + E)         |
| Bellman-Ford   | Negative weights, Cycle detection  | O(V × E)        | O(V)             |
| SPFA           | Average case faster Bellman-Ford   | O(E) to O(V×E)  | O(V)             |
| Floyd-Warshall | All-Pairs Shortest Path (APSP)     | O(V³)           | O(V²)            |

## E. Real-world Applications
1. **Network Routing Protocols**: 
   - OSPF (Open Shortest Path First) uses Dijkstra's algorithm.
   - RIP (Routing Information Protocol) uses a variant of distance-vector routing akin to Bellman-Ford.
2. **Navigation Systems**: Google Maps, GPS routing (using A*, which is guided Dijkstra).
3. **Financial Arbitrage**: Finding negative cycles in a currency exchange graph identifies risk-free arbitrage opportunities.
4. **Operations Research**: Critical Path Method (CPM) and PERT analysis in project scheduling.

"""

import heapq
from collections import deque
from typing import List, Dict, Tuple, Optional
import math


class ShortestPathAlgorithms:
    """
    A comprehensive suite of shortest path algorithms.
    This class is designed as a namespace for standard textbook implementations.
    """

    @staticmethod
    def dijkstra(n: int, edges: List[Tuple[int, int, float]], source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Professional implementation of Dijkstra's Algorithm using an Adjacency List and a Min-Heap.
        Finds the shortest path from `source` to all other nodes.
        
        Constraints: No negative edge weights.
        
        Time Complexity: O((V + E) log V)
        Space Complexity: O(V + E) for the adjacency list and priority queue.
        
        Args:
            n (int): Number of nodes (nodes are 1-indexed to n).
            edges (List[Tuple[int, int, float]]): List of directed edges as (u, v, weight).
            source (int): The starting node.
            
        Returns:
            Tuple[Dict[int, float], Dict[int, Optional[int]]]:
                1. Dictionary mapping each node to its shortest distance from the source.
                2. Dictionary mapping each node to its predecessor (for path reconstruction).
        """
        # 1. Build Adjacency List
        # graph[u] = list of (v, weight)
        graph: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(1, n + 1)}
        for u, v, w in edges:
            if w < 0:
                raise ValueError("Dijkstra's Algorithm does not support negative edge weights.")
            graph[u].append((v, w))
            
        # 2. Initialize distances and predecessors
        distances = {i: float('inf') for i in range(1, n + 1)}
        predecessors: Dict[int, Optional[int]] = {i: None for i in range(1, n + 1)}
        distances[source] = 0.0
        
        # 3. Min-heap to process nodes greedy-style: stores tuples of (distance_from_source, node)
        pq = [(0.0, source)]
        
        while pq:
            # Extract the node with the minimum distance
            current_dist, u = heapq.heappop(pq)
            
            # Optimization: 
            # Because Python's heapq doesn't support decrease-key efficiently, we push duplicate nodes
            # with updated distances. If we pop a node and its distance is greater than the best known
            # distance, it's an outdated entry. We should skip it.
            if current_dist > distances[u]:
                continue
                
            # Explore neighbors
            for v, weight in graph[u]:
                new_distance = current_dist + weight
                
                # Relaxation step
                if new_distance < distances[v]:
                    distances[v] = new_distance
                    predecessors[v] = u
                    heapq.heappush(pq, (new_distance, v))
                    
        return distances, predecessors

    @staticmethod
    def bellman_ford(n: int, edges: List[Tuple[int, int, float]], source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Bellman-Ford Algorithm for finding SSSP in graphs that may contain negative weights.
        It also detects negative-weight cycles.
        
        Time Complexity: O(V * E)
        Space Complexity: O(V)
        
        Args:
            n (int): Number of nodes (1-indexed).
            edges (List[Tuple[int, int, float]]): List of directed edges as (u, v, weight).
            source (int): The starting node.
            
        Returns:
            Tuple[Dict[int, float], Dict[int, Optional[int]]]:
                1. Dictionary mapping nodes to their shortest distance (or empty if a negative cycle is reachable).
                2. Dictionary of predecessors.
        """
        distances = {i: float('inf') for i in range(1, n + 1)}
        predecessors: Dict[int, Optional[int]] = {i: None for i in range(1, n + 1)}
        distances[source] = 0.0
        
        # Step 1: Relax all edges |V| - 1 times.
        # A simple shortest path from source to any other vertex can have at most |V| - 1 edges.
        for _ in range(n - 1):
            relaxed_any = False
            for u, v, w in edges:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
                    relaxed_any = True
            
            # Optimization: If no distances were updated in this pass, we can early exit.
            if not relaxed_any:
                break
                
        # Step 2: Check for negative-weight cycles.
        # If we can still relax an edge, then a negative cycle exists.
        for u, v, w in edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                # Negative cycle detected!
                print(f"Warning: Graph contains a negative weight cycle involving edge {u}->{v}.")
                # In standard competitive programming problems, reaching a negative cycle
                # means distances are mathematically undefined (-inf). We return empty dicts to signal this.
                return {}, {}
                
        return distances, predecessors

    @staticmethod
    def spfa(n: int, edges: List[Tuple[int, int, float]], source: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Shortest Path Faster Algorithm (SPFA).
        An optimization of Bellman-Ford using a queue to only relax edges from nodes
        whose distance was updated in the previous step.
        
        Time Complexity: Average O(E), Worst case O(V * E)
        Space Complexity: O(V + E)
        """
        graph: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(1, n + 1)}
        for u, v, w in edges:
            graph[u].append((v, w))
            
        distances = {i: float('inf') for i in range(1, n + 1)}
        predecessors: Dict[int, Optional[int]] = {i: None for i in range(1, n + 1)}
        distances[source] = 0.0
        
        queue = deque([source])
        in_queue = {i: False for i in range(1, n + 1)}
        in_queue[source] = True
        
        # Array to count how many times a node is added to the queue
        # If a node is added more than V-1 times, a negative cycle exists.
        count = {i: 0 for i in range(1, n + 1)}
        count[source] = 1
        
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            
            for v, w in graph[u]:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
                    
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
                        count[v] += 1
                        
                        if count[v] > n:
                            # Node enqueued more than V times implies a negative cycle
                            return {}, {}
                            
        return distances, predecessors

    @staticmethod
    def floyd_warshall(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
        """
        Floyd-Warshall Algorithm for All-Pairs Shortest Path (APSP).
        Uses Dynamic Programming to find the shortest paths between all pairs of nodes.
        
        Time Complexity: O(V^3)
        Space Complexity: O(V^2) for the distance matrix and next_node matrix.
        
        Args:
            n (int): Number of nodes (1-indexed).
            edges (List[Tuple[int, int, float]]): List of directed edges.
            
        Returns:
            Tuple[List[List[float]], List[List[Optional[int]]]]:
                1. 2D array where dist[i][j] is the shortest distance from node i to node j.
                2. 2D array where next_node[i][j] is the next node to visit on the shortest path from i to j.
        """
        # We'll use 0-indexing internally and pad size to n+1 to keep 1-indexed usage simple.
        dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        next_node: List[List[Optional[int]]] = [[None] * (n + 1) for _ in range(n + 1)]
        
        # Diagonal is 0
        for i in range(1, n + 1):
            dist[i][i] = 0.0
            next_node[i][i] = i
            
        # Populate initial edges
        # Note: If there are multiple edges between u and v, we want the minimum one.
        for u, v, w in edges:
            if w < dist[u][v]:
                dist[u][v] = w
                next_node[u][v] = v
                
        # DP: k is the intermediate vertex
        # At step k, we consider paths from i to j that can use vertices 1..k as intermediate points.
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    # Relaxation step
                    if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                        if dist[i][k] + dist[k][j] < dist[i][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            # To go from i to j optimally, go from i to k first.
                            # So the next step from i is whatever the next step is to get to k.
                            next_node[i][j] = next_node[i][k]
                            
        # Check for negative cycles
        # If the distance from a node to itself becomes negative, a negative cycle exists.
        for i in range(1, n + 1):
            if dist[i][i] < 0:
                print(f"Warning: Negative cycle detected at node {i}")
                
        return dist, next_node


class PathReconstructor:
    """
    Utility class to reconstruct paths from the predecessors/next_node dictionaries
    generated by the shortest path algorithms.
    """
    
    @staticmethod
    def reconstruct_sssp_path(predecessors: Dict[int, Optional[int]], source: int, target: int) -> List[int]:
        """Reconstruct path from source to target using the predecessor dictionary."""
        if target not in predecessors or (predecessors[target] is None and target != source):
            return [] # No path exists
            
        path = []
        current: Optional[int] = target
        while current is not None:
            path.append(current)
            if current == source:
                break
            current = predecessors[current]
            
        if not path or path[-1] != source:
            return []
            
        path.reverse()
        return path

    @staticmethod
    def reconstruct_apsp_path(next_node: List[List[Optional[int]]], u: int, v: int) -> List[int]:
        """Reconstruct path from u to v using the next_node matrix from Floyd-Warshall."""
        if next_node[u][v] is None:
            return []
            
        path = [u]
        while u != v:
            u_next = next_node[u][v]
            if u_next is None:
                return []
            u = u_next
            path.append(u)
        return path


# ============================================================================
# PROBLEM APPLICATIONS
# ============================================================================

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Problem: Network Delay Time (LeetCode 743).
    Given a list of travel times as directed edges times[i] = [u, v, w].
    Find the time it takes for all nodes to receive the signal sent from node k.
    If it's impossible for all nodes to receive the signal, return -1.
    
    Approach: SSSP using Dijkstra. The answer is the max distance to any node.
    """
    # Convert list format for our algorithm
    edges = [(u, v, float(w)) for u, v, w in times]
    distances, _ = ShortestPathAlgorithms.dijkstra(n, edges, k)
    
    max_time = max(distances.values())
    if max_time == float('inf'):
        return -1
    return int(max_time)


def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    Problem: Cheapest Flights Within K Stops (LeetCode 787)
    There are n cities connected by some number of flights. flights[i] = [from, to, price].
    Find the cheapest price from src to dst with at most k stops.
    
    Approach: Modified Bellman-Ford or BFS. We can run exactly K+1 iterations of Bellman-Ford.
    This restricts the shortest path to use at most K+1 edges (K stops).
    """
    distances = {i: float('inf') for i in range(n)}
    distances[src] = 0.0
    
    # Run exactly k+1 relaxations (k stops means k+1 edges)
    for _ in range(k + 1):
        temp_distances = dict(distances) # Copy distances for synchronous update
        for u, v, w in flights:
            if distances[u] != float('inf') and distances[u] + w < temp_distances[v]:
                temp_distances[v] = distances[u] + w
        distances = temp_distances
        
    ans = distances[dst]
    return int(ans) if ans != float('inf') else -1


# ============================================================================
# EXHAUSTIVE TEST SUITE
# ============================================================================
if __name__ == "__main__":
    print("Running Tests for Shortest Path Algorithms...\n")
    
    # 1. Dijkstra Tests
    print("--- Testing Dijkstra's Algorithm ---")
    edges1 = [(1, 2, 2.0), (1, 3, 4.0), (2, 3, 1.0), (2, 4, 7.0), (3, 4, 3.0)]
    n1 = 4
    dists, preds = ShortestPathAlgorithms.dijkstra(n1, edges1, 1)
    
    assert dists[1] == 0.0
    assert dists[2] == 2.0
    assert dists[3] == 3.0 # 1->2->3 is shorter than 1->3
    assert dists[4] == 6.0 # 1->2->3->4
    
    path_1_to_4 = PathReconstructor.reconstruct_sssp_path(preds, 1, 4)
    assert path_1_to_4 == [1, 2, 3, 4]
    print("Dijkstra SSSP and Path Reconstruction: PASS")
    
    # Network Delay Time Test
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert network_delay_time(times, 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 1) == 1
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1
    print("LeetCode 743 Network Delay Time: PASS")


    # 2. Bellman-Ford Tests
    print("\n--- Testing Bellman-Ford Algorithm ---")
    # Graph with negative weight but NO negative cycle
    edges2 = [(1, 2, 4.0), (1, 3, 3.0), (2, 4, 2.0), (3, 2, -2.0), (3, 4, 1.0)]
    dists2, preds2 = ShortestPathAlgorithms.bellman_ford(4, edges2, 1)
    
    assert dists2[2] == 1.0 # 1->3->2 is 3 + (-2) = 1
    assert dists2[4] == 3.0 # 1->3->2->4 is 1 + 2 = 3
    path_bf = PathReconstructor.reconstruct_sssp_path(preds2, 1, 4)
    assert path_bf == [1, 3, 2, 4]
    
    # Graph with a negative cycle
    edges_nc = [(1, 2, 1.0), (2, 3, -1.0), (3, 4, -1.0), (4, 2, -1.0)]
    dists_nc, _ = ShortestPathAlgorithms.bellman_ford(4, edges_nc, 1)
    assert dists_nc == {}, "Failed to detect negative cycle in Bellman-Ford"
    print("Bellman-Ford SSSP and Negative Cycle Detection: PASS")


    # 3. SPFA Tests
    print("\n--- Testing SPFA ---")
    dists_spfa, preds_spfa = ShortestPathAlgorithms.spfa(4, edges2, 1)
    assert dists_spfa[2] == 1.0
    assert dists_spfa[4] == 3.0
    
    dists_spfa_nc, _ = ShortestPathAlgorithms.spfa(4, edges_nc, 1)
    assert dists_spfa_nc == {}, "Failed to detect negative cycle in SPFA"
    print("SPFA SSSP and Negative Cycle Detection: PASS")
    
    
    # 4. Floyd-Warshall Tests
    print("\n--- Testing Floyd-Warshall Algorithm ---")
    edges3 = [(1, 2, 3.0), (1, 4, 5.0), (2, 1, 2.0), (2, 4, 4.0), (3, 2, 1.0), (4, 3, 2.0)]
    n3 = 4
    matrix, next_node = ShortestPathAlgorithms.floyd_warshall(n3, edges3)
    
    # Check APSP results
    assert matrix[1][2] == 3.0
    assert matrix[1][3] == 7.0  # 1->4->3 (5 + 2 = 7)
    assert matrix[1][4] == 5.0
    
    assert matrix[3][1] == 3.0  # 3->2->1 (1 + 2 = 3)
    assert matrix[3][4] == 5.0  # 3->2->4 (1 + 4 = 5)
    
    # Reconstruct path from 1 to 3: 1 -> 4 -> 3
    path_fw_1_3 = PathReconstructor.reconstruct_apsp_path(next_node, 1, 3)
    assert path_fw_1_3 == [1, 4, 3]
    
    # Reconstruct path from 3 to 4: 3 -> 2 -> 4
    path_fw_3_4 = PathReconstructor.reconstruct_apsp_path(next_node, 3, 4)
    assert path_fw_3_4 == [3, 2, 4]
    print("Floyd-Warshall APSP and Path Reconstruction: PASS")
    
    
    # 5. Application Tests
    print("\n--- Testing Cheapest Flights Within K Stops ---")
    flights1 = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    assert find_cheapest_price(4, flights1, 0, 3, 1) == 700
    assert find_cheapest_price(4, flights1, 0, 3, 0) == -1
    
    flights2 = [[0,1,100],[1,2,100],[0,2,500]]
    assert find_cheapest_price(3, flights2, 0, 2, 1) == 200
    assert find_cheapest_price(3, flights2, 0, 2, 0) == 500
    print("LeetCode 787 Cheapest Flights: PASS")


    print("\n==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY! 🚀")
    print("==================================================")
