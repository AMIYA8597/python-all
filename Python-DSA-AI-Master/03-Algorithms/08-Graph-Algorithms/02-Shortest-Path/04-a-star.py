"""
A* Search Algorithm

Learning Objectives:
1. Understand informed search vs uninformed search.
2. Implement A* with a heuristic.

Concept Explanation:
A* uses a best-first search and finds the least-cost path from a given initial node to one goal node. It uses a heuristic function to estimate the cost to the goal. 
f(n) = g(n) + h(n) where g is the cost from start and h is the estimated cost to goal.

Performance Analysis:
- Time Complexity: O(E) in worst case, heavily depends on the heuristic.
- Space Complexity: O(V)

Edge Cases:
- Inadmissible heuristic (overestimates cost) can lead to suboptimal paths.
"""

import heapq
from typing import Dict, List, Tuple, Callable, Any
import unittest

def a_star(graph: Dict[Any, List[Tuple[Any, float]]], start: Any, target: Any, heuristic: Callable[[Any, Any], float]) -> List[Any]:
    open_set = [(0, start)]
    came_from = {}
    
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, target)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == target:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
            
        for neighbor, weight in graph.get(current, []):
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return []

class TestAStar(unittest.TestCase):
    def test_a_star(self):
        graph = {
            'A': [('B', 1), ('C', 3)],
            'B': [('D', 1)],
            'C': [('D', 1)],
            'D': []
        }
        
        def h(node, target):
            h_vals = {'A': 2, 'B': 1, 'C': 1, 'D': 0}
            return h_vals[node]
            
        path = a_star(graph, 'A', 'D', h)
        self.assertEqual(path, ['A', 'B', 'D'])

if __name__ == '__main__':
    unittest.main()
