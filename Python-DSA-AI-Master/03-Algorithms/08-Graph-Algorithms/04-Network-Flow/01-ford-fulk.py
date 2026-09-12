"""
Module: Ford-Fulkerson Algorithm
"""
# Learning objectives: Max Flow Min Cut theorem, Ford-Fulkerson algorithm.
# Concept explanation: Finds the maximum flow in a flow network using augmenting paths.

import unittest
from typing import List

# Basic/Intermediate: Ford-Fulkerson using DFS
class Graph:
    def __init__(self, vertices: int):
        self.graph = [[0]*vertices for _ in range(vertices)]
        self.ROW = vertices
    
    def add_edge(self, u: int, v: int, w: int):
        self.graph[u][v] = w
        
    def dfs(self, s: int, t: int, parent: List[int]) -> bool:
        visited = [False]*(self.ROW)
        stack = [s]
        visited[s] = True
        
        while stack:
            u = stack.pop()
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    stack.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
        return False
        
    def ford_fulkerson(self, source: int, sink: int) -> int:
        parent = [-1]*(self.ROW)
        max_flow = 0
        
        while self.dfs(source, sink, parent):
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

# Advanced: Capacity scaling Ford-Fulkerson
# Performance analysis:
# Time Complexity: O(E * max_flow)
# Space Complexity: O(V^2) for adjacency matrix.
# Edge cases: Graph with cycles, multiple sources/sinks.
# Interview challenge: Bipartite matching.

class TestFordFulkerson(unittest.TestCase):
    def test_ff(self):
        g = Graph(6)
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
        self.assertEqual(g.ford_fulkerson(0, 5), 23)

if __name__ == '__main__':
    unittest.main()
