"""
Bipartite Matching - Advanced Graph Data Structures

Learning Objectives:
1. Understand Bipartite Graphs and Maximum Bipartite Matching (MBM).
2. Implement MBM using DFS-based augmenting paths.
3. Formulate assignment problems (e.g., jobs to applicants) as MBM.

Concept Explanation:
A bipartite graph's vertices can be divided into two disjoint sets U and V such that every edge connects a vertex in U to one in V.
Maximum Bipartite Matching finds the largest set of edges without common vertices.
It can be solved using max-flow (Hopcroft-Karp or Ford-Fulkerson) or a simpler DFS approach.

Performance Analysis:
- Time Complexity: O(V * E) for the DFS approach.
- Space Complexity: O(V) for visited arrays and matching state.
"""

from typing import List

class BipartiteMatcher:
    def __init__(self, applicants: int, jobs: int):
        self.applicants = applicants
        self.jobs = jobs
        # graph[u][v] is 1 if applicant u is interested in job v
        self.graph = [[0] * jobs for _ in range(applicants)]
        
    def add_interest(self, applicant: int, job: int):
        self.graph[applicant][job] = 1
        
    def _bpm(self, u: int, matchR: List[int], seen: List[bool]) -> bool:
        for v in range(self.jobs):
            if self.graph[u][v] and not seen[v]:
                seen[v] = True
                
                # If job 'v' is not assigned to an applicant OR
                # previously assigned applicant for job 'v' has an alternate job available
                if matchR[v] == -1 or self._bpm(matchR[v], matchR, seen):
                    matchR[v] = u
                    return True
        return False
        
    def max_bipartite_matching(self) -> int:
        matchR = [-1] * self.jobs
        result = 0
        
        for i in range(self.applicants):
            seen = [False] * self.jobs
            if self._bpm(i, matchR, seen):
                result += 1
                
        return result

# Advanced: Checking if a graph is Bipartite using BFS (Graph Coloring)
def is_bipartite(graph: List[List[int]], start: int) -> bool:
    V = len(graph)
    color = [-1] * V
    
    from collections import deque
    queue = deque([start])
    color[start] = 1
    
    while queue:
        u = queue.popleft()
        
        # Self loop implies not bipartite
        if graph[u][u] == 1:
            return False
            
        for v in range(V):
            if graph[u][v] == 1 and color[v] == -1:
                color[v] = 1 - color[u]
                queue.append(v)
            elif graph[u][v] == 1 and color[v] == color[u]:
                return False
                
    return True

# Edge Cases:
# 1. No edges (0 matching).
# 2. Perfect matching possible.
# 3. Disconnected components.

# Interview Challenge:
# Q: "How does Hopcroft-Karp improve upon the basic DFS MBM algorithm?"
# A: "Hopcroft-Karp uses BFS to find multiple shortest augmenting paths simultaneously, reducing time complexity to O(E * sqrt(V))."

def test_bipartite_matching():
    bpGraph = BipartiteMatcher(6, 6)
    interests = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 2), (3, 2), (3, 3), (4, 5), (5, 5)]
    for u, v in interests:
        bpGraph.add_interest(u, v)
        
    assert bpGraph.max_bipartite_matching() == 5
    
    adj = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ]
    assert is_bipartite(adj, 0) == True
    
    print("All tests passed for Bipartite Matching.")

if __name__ == "__main__":
    test_bipartite_matching()
