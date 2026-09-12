"""
Module: Dinic's Algorithm
"""
# Learning objectives: Dinic's algorithm for Maximum Flow.
# Concept explanation: Faster max flow algorithm using Level Graphs and Blocking Flows.

import unittest
from typing import List, Dict
import collections

# Basic/Intermediate: Dinic's Algorithm
class Edge:
    def __init__(self, v: int, flow: int, C: int, rev: int):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev

class Dinic:
    def __init__(self, V: int):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.level = [0] * V
        
    def add_edge(self, u: int, v: int, C: int):
        a = Edge(v, 0, C, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)
        
    def bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.V
        self.level[s] = 0
        queue = collections.deque([s])
        
        while queue:
            u = queue.popleft()
            for edge in self.adj[u]:
                if self.level[edge.v] < 0 and edge.flow < edge.C:
                    self.level[edge.v] = self.level[u] + 1
                    queue.append(edge.v)
        return self.level[t] >= 0
        
    def dfs(self, u: int, flow: int, t: int, start: List[int]) -> int:
        if u == t:
            return flow
            
        for i in range(start[u], len(self.adj[u])):
            edge = self.adj[u][i]
            if self.level[edge.v] == self.level[u] + 1 and edge.flow < edge.C:
                curr_flow = min(flow, edge.C - edge.flow)
                temp_flow = self.dfs(edge.v, curr_flow, t, start)
                if temp_flow > 0:
                    edge.flow += temp_flow
                    self.adj[edge.v][edge.rev].flow -= temp_flow
                    return temp_flow
            start[u] += 1
        return 0
        
    def max_flow(self, s: int, t: int) -> int:
        if s == t:
            return -1
        total_flow = 0
        while self.bfs(s, t):
            start = [0] * self.V
            while True:
                flow = self.dfs(s, float('inf'), t, start)
                if not flow:
                    break
                total_flow += flow
        return total_flow

# Performance analysis:
# Time Complexity: O(V^2 E)
# Space Complexity: O(V + E)
# Edge cases: Unreachable sink.
# Interview challenge: Maximum Bipartite Matching with Dinic's.

class TestDinic(unittest.TestCase):
    def test_dinic(self):
        g = Dinic(6)
        g.add_edge(0, 1, 16)
        g.add_edge(0, 2, 13)
        g.add_edge(1, 2, 10)
        g.add_edge(1, 3, 12)
        g.add_edge(2, 1, 4)
        g.add_edge(2, 4, 14)
        g.add_edge(3, 2, 9)
        g.add_edge(3, 5, 20)
        g.add_edge(4, 3, 7)
        g.add_edge(4, 5, 4)
        self.assertEqual(g.max_flow(0, 5), 23)

if __name__ == '__main__':
    unittest.main()
