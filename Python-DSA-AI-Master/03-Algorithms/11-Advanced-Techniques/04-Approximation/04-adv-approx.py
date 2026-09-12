"""
Module: Advanced Approximation Algorithms
=========================================

Learning Objectives:
1. Implement approximation algorithms with guaranteed bounds.
2. Solve the Vertex Cover problem with a 2-approximation factor.
3. Solve the Set Cover problem with a greedy approximation.

Concept Explanation:
Some NP-Hard problems have algorithms that guarantee the solution will not be 
worse than a certain factor `c` times the optimal solution. 
For Vertex Cover, picking edges and adding both endpoints yields a 2-approximation.
For Set Cover, greedily picking the set that covers the most uncovered elements
yields a ln(n)-approximation.

Type Hints & Edge Cases:
- Empty graphs or sets.
- Already covered states.
"""

from typing import List, Set, Tuple

# Basic Implementation: Vertex Cover 2-Approximation
# Edges represented as pairs of nodes: (u, v)
def vertex_cover_approx(edges: List[Tuple[int, int]]) -> Set[int]:
    """
    Finds a vertex cover that is at most twice the optimal size.
    """
    cover = set()
    edges_copy = edges.copy()
    
    while edges_copy:
        u, v = edges_copy.pop()
        cover.add(u)
        cover.add(v)
        
        # Remove all edges incident to u or v
        edges_copy = [edge for edge in edges_copy if edge[0] not in (u, v) and edge[1] not in (u, v)]
        
    return cover

# Advanced Implementation: Greedy Set Cover
def set_cover_greedy(universe: Set[int], subsets: List[Set[int]]) -> List[Set[int]]:
    """
    Finds a set cover using greedy approach. Guarantees O(ln n) approximation.
    """
    uncovered = universe.copy()
    cover_sets = []
    
    while uncovered:
        # Find the subset that covers the most uncovered elements
        best_set = max(subsets, key=lambda s: len(s.intersection(uncovered)))
        
        # If no subset covers any remaining elements, cover is impossible
        if not best_set.intersection(uncovered):
            break
            
        cover_sets.append(best_set)
        uncovered -= best_set
        
    return cover_sets

# Interview Challenge
def challenge_is_vertex_cover(edges: List[Tuple[int, int]], cover: Set[int]) -> bool:
    """
    Challenge: Verify if a given set of vertices is a valid vertex cover.
    """
    for u, v in edges:
        if u not in cover and v not in cover:
            return False
    return True

def test_approx():
    # Test Vertex Cover
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
    cover = vertex_cover_approx(edges)
    assert challenge_is_vertex_cover(edges, cover), "Invalid vertex cover"
    assert len(cover) <= 2 * 3, "2-Approximation violated" # Opt is 2 or 3
    
    # Test Set Cover
    universe = {1, 2, 3, 4, 5}
    subsets = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
    sc = set_cover_greedy(universe, subsets)
    covered_elements = set().union(*sc)
    assert covered_elements == universe, "Set cover failed"
    
    print("All tests passed.")

if __name__ == "__main__":
    print("Advanced Approximation Execution\\n" + "-"*30)
    test_approx()
