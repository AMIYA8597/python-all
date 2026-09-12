"""
Module: Push-Relabel Algorithm
"""
# Learning objectives: Preflow-push / Push-Relabel algorithm.
# Concept explanation: Works locally by maintaining a preflow and pushing excess flow towards the sink, relabeling heights when blocked.

import unittest
from typing import List

# Basic/Intermediate: Push-Relabel
class Edge:
    def __init__(self, u, v, capacity, flow=0):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow

class PushRelabel:
    def __init__(self, V: int):
        self.V = V
        self.edges = []
        self.adj = [[] for _ in range(V)]
        
    def add_edge(self, u: int, v: int, capacity: int):
        self.edges.append(Edge(u, v, capacity))
        self.edges.append(Edge(v, u, 0)) # residual
        self.adj[u].append(len(self.edges) - 2)
        self.adj[v].append(len(self.edges) - 1)
        
    def max_flow(self, s: int, t: int) -> int:
        height = [0] * self.V
        excess = [0] * self.V
        height[s] = self.V
        
        for e_idx in self.adj[s]:
            edge = self.edges[e_idx]
            edge.flow = edge.capacity
            self.edges[e_idx ^ 1].flow -= edge.flow
            excess[edge.v] += edge.flow
            excess[s] -= edge.flow
            
        def push(u: int):
            for e_idx in self.adj[u]:
                edge = self.edges[e_idx]
                if height[u] > height[edge.v] and edge.flow < edge.capacity:
                    df = min(excess[u], edge.capacity - edge.flow)
                    edge.flow += df
                    self.edges[e_idx ^ 1].flow -= df
                    excess[u] -= df
                    excess[edge.v] += df
                    if excess[u] == 0:
                        return True
            return False
            
        def relabel(u: int):
            min_h = float('inf')
            for e_idx in self.adj[u]:
                edge = self.edges[e_idx]
                if edge.capacity > edge.flow:
                    min_h = min(min_h, height[edge.v])
            if min_h < float('inf'):
                height[u] = min_h + 1
                
        while True:
            u = -1
            for i in range(self.V):
                if i != s and i != t and excess[i] > 0:
                    u = i
                    break
            if u == -1:
                break
                
            if not push(u):
                relabel(u)
                
        return excess[t]

# Performance analysis:
# Time Complexity: O(V^2 E) basic, O(V^3) with relabel-to-front.
# Space Complexity: O(V + E)
# Edge cases: Dense graphs.
# Interview challenge: Image segmentation problem.

class TestPushRelabel(unittest.TestCase):
    def test_pr(self):
        g = PushRelabel(6)
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
