"""
AtCoder Regular Contest (ARC) Practice

This module dives into advanced topics frequently encountered in AtCoder Regular Contests.
ARC problems demand high mathematical maturity, ad-hoc problem-solving skills,
and proficiency with advanced graph theory (e.g., Strongly Connected Components,
Max Flow) and combinatorial mathematics.

Learning Objectives:
1. Develop ad-hoc thinking and mathematical problem-solving skills.
2. Implement advanced graph algorithms like SCC (Kosaraju's/Tarjan's).
3. Utilize modular arithmetic effectively in combinatorial problems.

Industry Use Cases:
Advanced graph algorithms are used in compiler optimization, network flow analysis,
circuit design, and social network analysis.
"""

from typing import List, Set
from collections import defaultdict

class GraphSCC:
    """
    Finding Strongly Connected Components (SCC) using Kosaraju's Algorithm.
    """
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph = defaultdict(list)
        self.rev_graph = defaultdict(list)
        
    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.rev_graph[v].append(u)
        
    def _dfs_1(self, v: int, visited: List[bool], stack: List[int]) -> None:
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self._dfs_1(neighbor, visited, stack)
        stack.append(v)
        
    def _dfs_2(self, v: int, visited: List[bool], scc: List[int]) -> None:
        visited[v] = True
        scc.append(v)
        for neighbor in self.rev_graph[v]:
            if not visited[neighbor]:
                self._dfs_2(neighbor, visited, scc)
                
    def find_sccs(self) -> List[List[int]]:
        stack = []
        visited = [False] * self.V
        
        for i in range(self.V):
            if not visited[i]:
                self._dfs_1(i, visited, stack)
                
        visited = [False] * self.V
        sccs = []
        
        while stack:
            v = stack.pop()
            if not visited[v]:
                scc = []
                self._dfs_2(v, visited, scc)
                sccs.append(scc)
                
        return sccs

def test_scc():
    g = GraphSCC(5)
    g.add_edge(1, 0)
    g.add_edge(0, 2)
    g.add_edge(2, 1)
    g.add_edge(0, 3)
    g.add_edge(3, 4)
    
    sccs = g.find_sccs()
    # Component sets
    scc_sets = [set(c) for c in sccs]
    assert {0, 1, 2} in scc_sets
    assert {3} in scc_sets
    assert {4} in scc_sets

if __name__ == "__main__":
    test_scc()
    print("AtCoder Regular tests passed.")
