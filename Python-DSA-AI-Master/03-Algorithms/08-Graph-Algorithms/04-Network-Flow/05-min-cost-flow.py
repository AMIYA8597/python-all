"""
Module: Min Cost Max Flow Algorithm
"""
# Learning objectives: Successive shortest path algorithm.
# Concept explanation: Finds the maximum flow while minimizing the total cost. Uses Bellman-Ford or SPFA to find shortest paths in terms of cost.

import unittest
from typing import List, Tuple
import collections

# Basic/Intermediate: Successive Shortest Path with SPFA
class MinCostMaxFlow:
    def __init__(self, V: int):
        self.V = V
        self.edges = []
        self.adj = [[] for _ in range(V)]
        
    def add_edge(self, u: int, v: int, capacity: int, cost: int):
        self.edges.append([u, v, capacity, cost, 0])
        self.edges.append([v, u, 0, -cost, 0])
        self.adj[u].append(len(self.edges) - 2)
        self.adj[v].append(len(self.edges) - 1)
        
    def min_cost_flow(self, s: int, t: int) -> Tuple[int, int]:
        total_flow = 0
        total_cost = 0
        
        while True:
            dist = [float('inf')] * self.V
            parent_edge = [-1] * self.V
            in_queue = [False] * self.V
            
            queue = collections.deque([s])
            dist[s] = 0
            in_queue[s] = True
            
            while queue:
                u = queue.popleft()
                in_queue[u] = False
                
                for e_idx in self.adj[u]:
                    u, v, cap, cost, flow = self.edges[e_idx]
                    if cap - flow > 0 and dist[v] > dist[u] + cost:
                        dist[v] = dist[u] + cost
                        parent_edge[v] = e_idx
                        if not in_queue[v]:
                            queue.append(v)
                            in_queue[v] = True
                            
            if dist[t] == float('inf'):
                break
                
            push_flow = float('inf')
            curr = t
            while curr != s:
                e_idx = parent_edge[curr]
                _, _, cap, _, flow = self.edges[e_idx]
                push_flow = min(push_flow, cap - flow)
                curr = self.edges[e_idx][0]
                
            total_flow += push_flow
            total_cost += push_flow * dist[t]
            
            curr = t
            while curr != s:
                e_idx = parent_edge[curr]
                self.edges[e_idx][4] += push_flow
                self.edges[e_idx ^ 1][4] -= push_flow
                curr = self.edges[e_idx][0]
                
        return total_flow, total_cost

# Performance analysis:
# Time Complexity: Depends on shortest path algorithm, generally O(F * VE) where F is max flow.
# Space Complexity: O(V + E)
# Edge cases: Negative cost cycles (requires cycle canceling).
# Interview challenge: Transportation problem.

class TestMinCostMaxFlow(unittest.TestCase):
    def test_mcmf(self):
        g = MinCostMaxFlow(4)
        g.add_edge(0, 1, 2, 1)
        g.add_edge(0, 2, 2, 2)
        g.add_edge(1, 2, 1, 1)
        g.add_edge(1, 3, 2, 3)
        g.add_edge(2, 3, 2, 1)
        flow, cost = g.min_cost_flow(0, 3)
        self.assertEqual(flow, 4)
        self.assertEqual(cost, 12)

if __name__ == '__main__':
    unittest.main()
