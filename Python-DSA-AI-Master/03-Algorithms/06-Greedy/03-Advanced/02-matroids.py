"""
Matroids and Greedy Algorithms

Learning Objectives:
1. Understand the mathematical framework of Matroids.
2. Formulate greedy algorithms using Matroid structure.
3. Solve scheduling problems modeled as Matroids.

Concept Explanation:
A Matroid is a mathematical structure that generalizes the notion of linear independence.
If an optimization problem can be formulated as finding a maximum-weight independent set 
in a Matroid, then the standard greedy algorithm is guaranteed to find the optimal solution.
Components of a Matroid:
- A finite ground set E.
- A family of subsets I of E, called independent sets.
Satisfying hereditary and exchange properties.

Performance Analysis:
- Time Complexity: Dominated by sorting elements O(N log N) + independence checks O(N * C).
- Space Complexity: O(N) to store independent sets.

Edge Cases:
- Empty ground set.
- All elements have zero/negative weights.

Interview Challenge:
"Implement a generic Matroid greedy algorithm and apply it to a scheduling task."
"""

from typing import List, Tuple, Callable
import unittest

def matroid_greedy_basic(elements: List[Tuple[Any, int]], is_independent: Callable[[List[Any]], bool]) -> List[Any]:
    """
    Basic greedy algorithm for matroids.
    elements: List of (item, weight)
    is_independent: Function checking if a set of items is independent.
    """
    # Sort elements by weight descending
    elements.sort(key=lambda x: x[1], reverse=True)
    
    independent_set = []
    
    for item, weight in elements:
        # Check if adding current item maintains independence
        temp_set = independent_set + [item]
        if is_independent(temp_set):
            independent_set.append(item)
            
    return independent_set

# Example application: Task scheduling with deadlines (Unit-time tasks)
# A set of tasks is independent if there exists a valid schedule for them.
def is_valid_schedule(tasks: List[Tuple[int, int]]) -> bool:
    """
    Check if tasks (deadline, id) can all be scheduled.
    For unit-time tasks, if we sort by deadline, time slot 'i' must be <= deadline[i].
    """
    tasks.sort(key=lambda x: x[0])
    for i, (deadline, _) in enumerate(tasks):
        if i + 1 > deadline:
            return False
    return True

def schedule_tasks_matroid(deadlines: List[int], penalties: List[int]) -> Tuple[List[int], int]:
    """Schedule tasks to minimize penalty (maximize saved penalty)."""
    n = len(deadlines)
    # elements are ((deadline, index), penalty)
    elements = [((deadlines[i], i), penalties[i]) for i in range(n)]
    
    selected_tasks = matroid_greedy_basic(elements, is_valid_schedule)
    
    # Calculate total penalty (sum of all penalties - sum of selected penalties)
    total_penalty = sum(penalties)
    saved_penalty = sum(elements[i][1] for i in range(n) if elements[i][0] in selected_tasks)
    
    return [task[1] for task in selected_tasks], total_penalty - saved_penalty

class TestMatroid(unittest.TestCase):
    def test_matroid_greedy(self):
        deadlines = [4, 2, 4, 3, 1, 4, 6]
        penalties = [70, 60, 50, 40, 30, 20, 10]
        # Maximize saved penalties: sort by penalty -> 70(d:4), 60(d:2), 50(d:4), 40(d:3), 30(d:1), 20(d:4), 10(d:6)
        # 70 ok, 60 ok, 50 ok, 40 ok, 30 rejected, 20 rejected, 10 ok
        # Selected: 70, 60, 50, 40, 10. Saved: 230. Penalty: 280 - 230 = 50.
        selected, min_penalty = schedule_tasks_matroid(deadlines, penalties)
        self.assertEqual(min_penalty, 50)
        self.assertEqual(len(selected), 5)

if __name__ == "__main__":
    unittest.main()
