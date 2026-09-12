"""
## A. Concept Name
Articulation Points and Bridges - Advanced Graph Data Structures

## B. Motivation / Why it matters
Identifying vulnerabilities in a network, such as single points of failure (Articulation Points / Cut Vertices) and critical connections (Bridges), is essential for designing robust systems in networking, power grids, and transportation.

## C. Core Mechanics
- An Articulation Point is a vertex whose removal increases the number of connected components.
- A Bridge is an edge whose removal increases the number of connected components.
- Both can be found efficiently using a single DFS traversal tracking `discovery_time` and `lowest_reachable_time`.

## D. Real-World Analogy
Imagine a map of islands connected by bridges. An articulation point is an island that, if submerged, disconnects other islands. A bridge (in the graph sense) is a literal bridge that, if collapsed, separates groups of islands.

## E. Implementation Details
- Uses DFS to compute `disc` (discovery time) and `low` (lowest reachable time).
- A node `u` is an articulation point if:
  1. It's the root of the DFS tree and has more than 1 child.
  2. It's not the root and has a child `v` such that `low[v] >= disc[u]`.
- An edge `(u, v)` is a bridge if `low[v] > disc[u]`.

## F. Complexity Analysis
- Time Complexity: O(V + E) for undirected graphs.
- Space Complexity: O(V) for the call stack and metadata arrays.

## G. Edge Cases
1. Complete graphs (no APs or bridges).
2. Tree structures (all internal nodes are APs, all edges are bridges).
3. Disconnected graphs.

## H. Common Interview Questions
Q: "What's the relationship between Articulation Points and Bridges?"
A: "The endpoints of a bridge are often articulation points, but not always (e.g., if the bridge connects a single node leaf). Conversely, a graph can have articulation points but no bridges (e.g., two triangles joined at a single vertex)."

## X. Project Connection
Critical for analyzing network topologies in distributed systems, preventing network partitions, and building fault-tolerant infrastructure.
"""

from typing import List, Set, Tuple
from collections import defaultdict

class NetworkAnalyzer:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        self.time = 0
        
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
        self.graph[v].append(u)
        
    def _dfs_ap(self, u: int, visited: List[bool], disc: List[int], low: List[int], parent: List[int], ap: Set[int]):
        children = 0
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        
        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                children += 1
                self._dfs_ap(v, visited, disc, low, parent, ap)
                
                low[u] = min(low[u], low[v])
                
                # Root node is AP if it has > 1 children in DFS tree
                if parent[u] == -1 and children > 1:
                    ap.add(u)
                # Non-root node is AP if no back-edge from subtree reaches above u
                elif parent[u] != -1 and low[v] >= disc[u]:
                    ap.add(u)
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def find_articulation_points(self) -> List[int]:
        visited = [False] * self.V
        disc = [float('inf')] * self.V
        low = [float('inf')] * self.V
        parent = [-1] * self.V
        ap = set()
        
        self.time = 0
        for i in range(self.V):
            if not visited[i]:
                self._dfs_ap(i, visited, disc, low, parent, ap)
                
        return list(ap)
        
    def _dfs_bridges(self, u: int, visited: List[bool], disc: List[int], low: List[int], parent: List[int], bridges: List[Tuple[int, int]]):
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        
        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                self._dfs_bridges(v, visited, disc, low, parent, bridges)
                low[u] = min(low[u], low[v])
                
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def find_bridges(self) -> List[Tuple[int, int]]:
        visited = [False] * self.V
        disc = [float('inf')] * self.V
        low = [float('inf')] * self.V
        parent = [-1] * self.V
        bridges = []
        
        self.time = 0
        for i in range(self.V):
            if not visited[i]:
                self._dfs_bridges(i, visited, disc, low, parent, bridges)
                
        return bridges

def test_ap_and_bridges():
    g1 = NetworkAnalyzer(5)
    g1.add_edge(1, 0)
    g1.add_edge(0, 2)
    g1.add_edge(2, 1)
    g1.add_edge(0, 3)
    g1.add_edge(3, 4)
    
    aps = g1.find_articulation_points()
    bridges = g1.find_bridges()
    
    assert set(aps) == {0, 3}
    assert set(bridges) == {(3, 4), (0, 3)}
    
    print("All tests passed for Articulation Points and Bridges.")

if __name__ == "__main__":
    test_ap_and_bridges()
