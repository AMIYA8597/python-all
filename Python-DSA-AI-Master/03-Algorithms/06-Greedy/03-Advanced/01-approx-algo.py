"""
Approximation Algorithms using Greedy

Learning Objectives:
1. Understand NP-hard problems and why exact polynomial time algorithms don't exist (yet).
2. Use greedy strategies to find approximate solutions.
3. Analyze the approximation ratio of greedy algorithms.

Concept Explanation:
For many optimization problems (like Vertex Cover, Set Cover), finding the absolute optimal solution 
is NP-hard. Approximation algorithms guarantee a solution that is within a certain factor of the optimal.
Greedy algorithms often serve as simple and fast approximation algorithms.
For example, in Set Cover, the greedy approach is to repeatedly pick the set that covers the most 
uncovered elements.

Performance Analysis:
- Time Complexity: Varies by problem. For Greedy Set Cover: O(N * M) where N is subsets, M is universe.
- Space Complexity: O(M) for storing uncovered elements.

Edge Cases:
- Universe cannot be fully covered.
- Empty universe or empty sets.

Interview Challenge:
"Given a universe of elements and a collection of sets, find a small number of sets whose union covers the universe."
"""

from typing import List, Set, Dict
import unittest

def set_cover_basic(universe: Set[int], subsets: List[Set[int]]) -> List[int]:
    """Basic greedy set cover. Returns indices of chosen sets."""
    uncovered = set(universe)
    chosen_indices = []
    
    # Track available subsets and their original indices
    available_subsets = list(enumerate(subsets))
    
    while uncovered:
        best_index = -1
        max_covered = 0
        best_set = None
        
        for idx, subset in available_subsets:
            if idx in chosen_indices:
                continue
            cover = len(uncovered.intersection(subset))
            if cover > max_covered:
                max_covered = cover
                best_index = idx
                best_set = subset
                
        if max_covered == 0: # Cannot cover remaining elements
            break
            
        chosen_indices.append(best_index)
        uncovered -= best_set
        
    return chosen_indices if not uncovered else []

def set_cover_intermediate(universe: Set[str], subsets: Dict[str, Set[str]]) -> List[str]:
    """Intermediate implementation using named subsets."""
    uncovered = set(universe)
    chosen_sets = []
    
    while uncovered:
        best_name = None
        max_covered = 0
        best_set = None
        
        for name, subset in subsets.items():
            if name in chosen_sets:
                continue
            cover = len(uncovered.intersection(subset))
            if cover > max_covered:
                max_covered = cover
                best_name = name
                best_set = subset
                
        if max_covered == 0:
            break
            
        chosen_sets.append(best_name)
        uncovered -= best_set
        
    return chosen_sets if not uncovered else []

class TestApproximation(unittest.TestCase):
    def test_basic(self):
        universe = {1, 2, 3, 4, 5}
        subsets = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
        # Greedy will pick {1, 2, 3} (covers 3), then {4, 5} (covers 2) -> Total 2 sets
        res = set_cover_basic(universe, subsets)
        self.assertEqual(len(res), 2)
        self.assertTrue(0 in res and 3 in res)
        
    def test_intermediate(self):
        universe = {'a', 'b', 'c', 'd', 'e'}
        subsets = {
            'S1': {'a', 'b', 'c'},
            'S2': {'b', 'd'},
            'S3': {'c', 'd'},
            'S4': {'d', 'e'}
        }
        res = set_cover_intermediate(universe, subsets)
        self.assertEqual(len(res), 2)
        self.assertTrue('S1' in res and 'S4' in res)

if __name__ == "__main__":
    unittest.main()
