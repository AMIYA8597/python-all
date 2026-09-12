"""
Module: Edmonds-Karp Algorithm
"""
# Learning objectives: Edmonds-Karp algorithm for max flow.
# Concept explanation: An implementation of Ford-Fulkerson that uses BFS to find the shortest augmenting path.

import unittest
from typing import List
import collections

# Basic/Intermediate: Edmonds-Karp
class GraphEK:
    def __init__(self, vertices: int):
        self.graph = [[0]*vertices for _ in range(vertices)]
        self.ROW = vertices
    
    def add_edge(self, u: int, v: int, w: int):
        self.graph[u][v] = w
        
    def bfs(self, s: int, t: int, parent: List[int]) -> bool:
        visited = [False]*(self.ROW)
        queue = collections.deque([s])
        visited[s] = True
        
        while queue:
            u = queue.popleft()
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False
        
    def edmonds_karp(self, source: int, sink: int) -> int:
        parent = [-1]*(self.ROW)
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
                
            max_flow += path_flow
            
            v = sink
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
                
        return int(max_flow)

# Advanced: Adjacency list representation
# Performance analysis:
# Time Complexity: O(V * E^2)
# Space Complexity: O(V^2) or O(V+E) with adj list.
# Edge cases: Empty graph.
# Interview challenge: Finding minimum cut edges.

class TestEdmondsKarp(unittest.TestCase):
    def test_ek(self):
        g = GraphEK(6)
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
        self.assertEqual(g.edmonds_karp(0, 5), 23)

if __name__ == '__main__':
    unittest.main()
