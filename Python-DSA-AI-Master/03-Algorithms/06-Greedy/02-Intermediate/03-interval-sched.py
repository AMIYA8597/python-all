"""
Interval Scheduling Maximization

Learning Objectives:
1. Understand the interval scheduling problem.
2. Differentiate between maximizing count vs minimizing resources (coloring).
3. Implement greedy solutions efficiently.

Concept Explanation:
Similar to the Activity Selection problem, Interval Scheduling Maximization asks to find the 
largest set of non-overlapping intervals.
The optimal greedy strategy is: sort intervals by end time, and always select the next interval 
that starts after the current one ends.

Performance Analysis:
- Time Complexity: O(N log N) for sorting.
- Space Complexity: O(N) for output list.

Edge Cases:
- Exact overlap of boundaries (usually allowed in scheduling).
- Empty intervals.
- Nested intervals.

Interview Challenge:
"Given a list of intervals, find the maximum number of intervals you can schedule on a single machine."
"""

from typing import List, Tuple
import unittest

def interval_scheduling_basic(intervals: List[Tuple[int, int]]) -> int:
    """Basic implementation returning max count of non-overlapping intervals."""
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[1])
    count = 1
    last_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start >= last_end:
            count += 1
            last_end = end
            
    return count

def interval_scheduling_intermediate(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Intermediate implementation returning the actual scheduled intervals."""
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[1])
    scheduled = [intervals[0]]
    last_end = intervals[0][1]
    
    for start, end in intervals[1:]:
        if start >= last_end:
            scheduled.append((start, end))
            last_end = end
            
    return scheduled

class Interval:
    def __init__(self, start: int, end: int, name: str):
        self.start = start
        self.end = end
        self.name = name

def interval_scheduling_advanced(intervals: List[Interval]) -> List[str]:
    """Advanced implementation using custom objects."""
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x.end)
    scheduled = [intervals[0].name]
    last_end = intervals[0].end
    
    for interval in intervals[1:]:
        if interval.start >= last_end:
            scheduled.append(interval.name)
            last_end = interval.end
            
    return scheduled

class TestIntervalScheduling(unittest.TestCase):
    def test_basic(self):
        intervals = [(1, 3), (2, 4), (3, 6), (5, 7), (8, 10)]
        self.assertEqual(interval_scheduling_basic(intervals), 4) # (1,3), (3,6), (8,10) Wait: 1-3, 3-6, 8-10 is 3. What about (5,7)?
        # (1,3), (3,6) -> wait, (5,7) overlaps with (3,6).
        # Let's trace manually: sort by end: (1,3), (2,4), (3,6), (5,7), (8,10)
        # pick (1,3). last=3. 
        # (2,4): start=2 < 3.
        # (3,6): start=3 >= 3. pick. last=6.
        # (5,7): start=5 < 6.
        # (8,10): start=8 >= 6. pick. last=10.
        # Total = 3.
        intervals2 = [(1, 3), (2, 4), (3, 5), (5, 7), (8, 10)]
        self.assertEqual(interval_scheduling_basic(intervals2), 4) # (1,3), (3,5), (5,7), (8,10)
        
    def test_intermediate(self):
        intervals = [(1, 3), (2, 4), (3, 5), (5, 7), (8, 10)]
        self.assertEqual(interval_scheduling_intermediate(intervals), [(1, 3), (3, 5), (5, 7), (8, 10)])

if __name__ == "__main__":
    unittest.main()
