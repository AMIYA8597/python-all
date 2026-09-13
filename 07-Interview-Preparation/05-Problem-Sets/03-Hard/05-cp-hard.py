"""
Competitive Programming Hard Problems - Interview Preparation

Learning Objectives:
1. Master advanced algorithms used in CP (e.g., Fast I/O, Advanced Graph Theory, Math).
2. Learn to write optimal code for strict time limits.
3. Understand combinatorics and modular arithmetic.

This module features implementations commonly used in competitive programming.
"""

from typing import List

# 1. Modular Exponentiation
def power_mod(base: int, exp: int, mod: int) -> int:
    """
    Computes (base^exp) % mod efficiently using binary exponentiation.
    Time Complexity: O(log(exp))
    """
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return res

# 2. Maximum Bipartite Matching (Hopcroft-Karp / DFS based)
class BipartiteGraph:
    """
    Finds the maximum matching in a bipartite graph.
    """
    def __init__(self, u_nodes: int, v_nodes: int):
        self.u_nodes = u_nodes
        self.v_nodes = v_nodes
        self.graph = [[] for _ in range(u_nodes)]

    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)

    def bpm(self, u: int, matchR: List[int], seen: List[bool]) -> bool:
        for v in self.graph[u]:
            if not seen[v]:
                seen[v] = True
                if matchR[v] == -1 or self.bpm(matchR[v], matchR, seen):
                    matchR[v] = u
                    return True
        return False

    def max_bipartite_matching(self) -> int:
        matchR = [-1] * self.v_nodes
        result = 0
        for i in range(self.u_nodes):
            seen = [False] * self.v_nodes
            if self.bpm(i, matchR, seen):
                result += 1
        return result

def test_cp_algorithms():
    print("Testing Modular Exponentiation:")
    assert power_mod(2, 10, 1000) == 24
    assert power_mod(5, 3, 100) == 25
    print("Modular Exponentiation tests passed!")
    
    print("\nTesting Maximum Bipartite Matching:")
    bg = BipartiteGraph(4, 4)
    bg.add_edge(0, 1)
    bg.add_edge(0, 2)
    bg.add_edge(1, 0)
    bg.add_edge(2, 2)
    bg.add_edge(3, 2)
    bg.add_edge(3, 3)
    matches = bg.max_bipartite_matching()
    print(f"Max matching: {matches}")
    assert matches == 4
    print("BPM tests passed!")

if __name__ == "__main__":
    test_cp_algorithms()
    print("\nAll CP tests passed!")
