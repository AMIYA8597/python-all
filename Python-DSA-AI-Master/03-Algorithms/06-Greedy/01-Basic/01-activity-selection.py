"""
Activity Selection Problem

Learning Objectives:
1. Understand the greedy choice property in interval scheduling.
2. Implement activity selection efficiently using sorting.
3. Handle overlapping constraints in greedy algorithms.

Concept Explanation:
The Activity Selection Problem is a classic greedy algorithm problem. Given a set of activities, 
each with a start time and a finish time, the goal is to select the maximum number of mutually 
compatible activities. Two activities are compatible if they don't overlap in time.
The greedy strategy is to always pick the next available activity that ends the earliest.

Performance Analysis:
- Time Complexity: O(N log N) if the activities are not sorted (due to sorting). O(N) if already sorted.
- Space Complexity: O(N) or O(1) depending on whether we create a new list for sorted items.

Edge Cases:
- Empty list of activities.
- All activities overlap.
- No activities overlap.

Interview Challenge:
"Given a list of meetings with start and end times, find the maximum number of meetings you can attend."
"""

from typing import List, Tuple
import unittest

def activity_selection_basic(start: List[int], finish: List[int]) -> List[int]:
    """Basic implementation assuming activities are already sorted by finish time."""
    if not start or not finish or len(start) != len(finish):
        return []
    
    selected = [0]
    last_finish_time = finish[0]
    
    for i in range(1, len(start)):
        if start[i] >= last_finish_time:
            selected.append(i)
            last_finish_time = finish[i]
            
    return selected

def activity_selection_intermediate(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Intermediate implementation taking a list of (start, finish) tuples and sorting them."""
    if not activities:
        return []
        
    sorted_activities = sorted(activities, key=lambda x: x[1])
    selected = [sorted_activities[0]]
    last_finish_time = sorted_activities[0][1]
    
    for i in range(1, len(sorted_activities)):
        if sorted_activities[i][0] >= last_finish_time:
            selected.append(sorted_activities[i])
            last_finish_time = sorted_activities[i][1]
            
    return selected

def activity_selection_advanced(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:
    """Advanced implementation handling named activities and tracking total time."""
    if not activities:
        return []
        
    sorted_activities = sorted(activities, key=lambda x: x[2])
    selected = [sorted_activities[0]]
    last_finish_time = sorted_activities[0][2]
    
    for i in range(1, len(sorted_activities)):
        if sorted_activities[i][1] >= last_finish_time:
            selected.append(sorted_activities[i])
            last_finish_time = sorted_activities[i][2]
            
    return selected

class TestActivitySelection(unittest.TestCase):
    def test_basic(self):
        start = [1, 3, 0, 5, 8, 5]
        finish = [2, 4, 6, 7, 9, 9]
        # These need to be sorted by finish time for basic to work correctly in our strict formulation,
        # but the problem typically assumes sorted or we must sort them. 
        # Let's pass sorted ones for basic test.
        start_sorted = [1, 3, 0, 5, 5, 8]
        finish_sorted = [2, 4, 6, 7, 9, 9]
        self.assertEqual(activity_selection_basic(start_sorted, finish_sorted), [0, 1, 3, 5])
        
    def test_intermediate(self):
        activities = [(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)]
        self.assertEqual(activity_selection_intermediate(activities), [(1, 2), (3, 4), (5, 7), (8, 9)])
        
    def test_advanced(self):
        activities = [('A1', 1, 2), ('A2', 3, 4), ('A3', 0, 6), ('A4', 5, 7), ('A5', 8, 9), ('A6', 5, 9)]
        self.assertEqual(activity_selection_advanced(activities), [('A1', 1, 2), ('A2', 3, 4), ('A4', 5, 7), ('A5', 8, 9)])

if __name__ == "__main__":
    unittest.main()
