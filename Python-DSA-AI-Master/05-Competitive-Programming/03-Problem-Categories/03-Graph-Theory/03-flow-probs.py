"""
## A. Concept Name
Network Flow Problems (Max Flow, Edmonds-Karp, Dinic's Algorithm)

## B. Overview
Network flow problems involve directing a flow of commodities, data, or physical items 
through a network of nodes, bounded by edge capacities. 
The canonical problem is Maximum Flow, which asks for the maximum total flow from a 
source node to a sink node.

## C. Learning Objectives
1. Understand Flow Networks, Capacity, Residual Graphs, and Augmenting Paths.
2. Master the Max-Flow Min-Cut Theorem.
3. Implement the Ford-Fulkerson method and Edmonds-Karp algorithm.
4. Implement Dinic's Algorithm for high-performance competitive programming.
5. Apply Maximum Flow to solve Maximum Bipartite Matching problems.

## D. Concept Explanations
Max-Flow Min-Cut Theorem:
- The maximum amount of flow passing from the source to the sink is equal to the total weight 
  of the edges in the minimum cut, i.e., the smallest total capacity of edges which if removed 
  would disconnect the source from the sink.

Edmonds-Karp Algorithm:
- An implementation of the Ford-Fulkerson method that uses Breadth-First Search (BFS) 
  to find augmenting paths.
- Guarantees the shortest augmenting path (in terms of number of edges).
- Time Complexity: O(V * E^2).

Dinic's Algorithm:
- A faster algorithm that uses Level Graphs (via BFS) and Blocking Flows (via DFS).
- Much faster in practice and essential for dense graphs or strict time limits.
- Time Complexity: O(V^2 * E).
- For unit capacity networks (like Bipartite Matching), it runs in O(E * sqrt(V)).

## E. Industry Use Cases
- Traffic and transportation routing.
- Liquid flow in pipes.
- Job assignments (Maximum Bipartite Matching).
- Image segmentation in computer vision (min-cut).

## X. Project Connection
These flow algorithms are utilized in optimization modules of the Python-DSA-AI-Master project to solve routing, matching, and allocation problems efficiently.
"""

from typing import List
from collections import deque


class EdmondsKarp:
    """
    Computes Max Flow using the Edmonds-Karp algorithm (BFS based Ford-Fulkerson).
    """
    def __init__(self, n: int):
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int):
        if self.capacity[u][v] == 0 and self.capacity[v][u] == 0:
            self.graph[u].append(v)
            self.graph[v].append(u)
        self.capacity[u][v] += cap

    def bfs(self, s: int, t: int, parent: List[int]) -> int:
        parent[:] = [-1] * self.n
        parent[s] = -2
        queue = deque([(s, float('inf'))])

        while queue:
            cur, flow = queue.popleft()

            for next_node in self.graph[cur]:
                if parent[next_node] == -1 and self.capacity[cur][next_node] > 0:
                    parent[next_node] = cur
                    new_flow = min(flow, self.capacity[cur][next_node])
                    if next_node == t:
                        return new_flow
                    queue.append((next_node, new_flow))
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        parent = [-1] * self.n
        
        while True:
            new_flow = self.bfs(s, t, parent)
            if new_flow == 0:
                break
            
            flow += new_flow
            cur = t
            while cur != s:
                prev = parent[cur]
                self.capacity[prev][cur] -= new_flow
                self.capacity[cur][prev] += new_flow
                cur = prev
                
        return flow


class Dinic:
    """
    Computes Max Flow using Dinic's algorithm (Level Graph + Blocking Flow).
    O(V^2 E) in general, O(E sqrt(V)) for bipartite matching.
    """
    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = [-1] * n

    def add_edge(self, u: int, v: int, cap: int):
        # Forward edge: [target, cap, flow, reverse_edge_index]
        self.graph[u].append([v, cap, 0, len(self.graph[v])])
        # Reverse edge
        self.graph[v].append([u, 0, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])
        
        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                v, cap, flow, _ = edge
                if cap - flow > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
                    
        return self.level[t] != -1

    def _dfs(self, u: int, t: int, push: int, ptr: List[int]) -> int:
        if push == 0:
            return 0
        if u == t:
            return push
            
        for cid in range(ptr[u], len(self.graph[u])):
            ptr[u] = cid
            v, cap, flow, rev_idx = self.graph[u][cid]
            
            if self.level[u] + 1 != self.level[v] or cap - flow == 0:
                continue
                
            pushed = self._dfs(v, t, min(push, cap - flow), ptr)
            
            if pushed == 0:
                continue
                
            self.graph[u][cid][2] += pushed
            self.graph[v][rev_idx][2] -= pushed
            return pushed
            
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self._bfs(s, t):
            ptr = [0] * self.n
            while True:
                pushed = self._dfs(s, t, float('inf'), ptr)
                if not pushed:
                    break
                flow += pushed
        return flow


def _run_tests():
    """Execute tests to ensure correctness."""
    
    # 1. Edmonds-Karp Test
    ek = EdmondsKarp(6)
    ek.add_edge(0, 1, 16)
    ek.add_edge(0, 2, 13)
    ek.add_edge(1, 2, 10)
    ek.add_edge(1, 3, 12)
    ek.add_edge(2, 1, 4)
    ek.add_edge(2, 4, 14)
    ek.add_edge(3, 2, 9)
    ek.add_edge(3, 5, 20)
    ek.add_edge(4, 3, 7)
    ek.add_edge(4, 5, 4)
    
    assert ek.max_flow(0, 5) == 23

    # 2. Dinic's Test
    dn = Dinic(6)
    dn.add_edge(0, 1, 16)
    dn.add_edge(0, 2, 13)
    dn.add_edge(1, 2, 10)
    dn.add_edge(1, 3, 12)
    dn.add_edge(2, 1, 4)
    dn.add_edge(2, 4, 14)
    dn.add_edge(3, 2, 9)
    dn.add_edge(3, 5, 20)
    dn.add_edge(4, 3, 7)
    dn.add_edge(4, 5, 4)
    
    assert dn.max_flow(0, 5) == 23


if __name__ == '__main__':
    print("Running Flow algorithm tests...")
    _run_tests()
    print("All tests passed!")
