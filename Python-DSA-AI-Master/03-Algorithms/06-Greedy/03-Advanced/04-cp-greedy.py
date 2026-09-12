"""
Competitive Programming Greedy Techniques

Learning Objectives:
1. Apply greedy strategies to complex CP problems.
2. Combine greedy with other techniques (sorting, binary search, priority queues).
3. Identify "greedy choice" properties under tight time constraints.

Concept Explanation:
In competitive programming, greedy algorithms are often used when problems require maximizing or 
minimizing a value under certain constraints, and a local optimal choice leads to a global optimum.
Typical patterns involve sorting the input and iterating, or maintaining a priority queue to always 
process the "best" available option.
Example problem: Meeting Rooms II (minimum number of conference rooms required).

Performance Analysis:
- Time Complexity: Typically O(N log N) due to sorting or priority queues.
- Space Complexity: O(N) for storing events or queues.

Edge Cases:
- Large inputs (10^5 elements), requires efficient O(N log N) solutions.
- Duplicate values.

Interview Challenge:
"Given an array of meeting time intervals consisting of start and end times, find the minimum number of conference rooms required."
"""

import heapq
from typing import List, Tuple
import unittest

def min_meeting_rooms_basic(intervals: List[Tuple[int, int]]) -> int:
    """Basic approach using line sweep (chronological ordering of events)."""
    if not intervals:
        return 0
        
    events = []
    for start, end in intervals:
        events.append((start, 1))  # 1 for room needed
        events.append((end, -1))   # -1 for room freed
        
    events.sort(key=lambda x: (x[0], x[1]))
    
    max_rooms = 0
    current_rooms = 0
    for _, diff in events:
        current_rooms += diff
        max_rooms = max(max_rooms, current_rooms)
        
    return max_rooms

def min_meeting_rooms_intermediate(intervals: List[Tuple[int, int]]) -> int:
    """Intermediate approach using a Priority Queue (Min-Heap)."""
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[0])
    free_rooms = []
    heapq.heappush(free_rooms, intervals[0][1])
    
    for i in range(1, len(intervals)):
        if free_rooms[0] <= intervals[i][0]:
            heapq.heappop(free_rooms)
        heapq.heappush(free_rooms, intervals[i][1])
            
    return len(free_rooms)

def gas_station_advanced(gas: List[int], cost: List[int]) -> int:
    """
    Advanced CP Problem: Gas Station.
    Find the starting gas station's index if you can travel around the circuit once, otherwise return -1.
    """
    if sum(gas) < sum(cost):
        return -1
        
    start_idx = 0
    current_gas = 0
    
    for i in range(len(gas)):
        current_gas += gas[i] - cost[i]
        if current_gas < 0:
            start_idx = i + 1
            current_gas = 0
            
    return start_idx

class TestCPGreedy(unittest.TestCase):
    def test_meeting_rooms_basic(self):
        intervals = [(0, 30), (5, 10), (15, 20)]
        self.assertEqual(min_meeting_rooms_basic(intervals), 2)
        
    def test_meeting_rooms_intermediate(self):
        intervals = [(7, 10), (2, 4)]
        self.assertEqual(min_meeting_rooms_intermediate(intervals), 1)
        
    def test_gas_station(self):
        gas = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
        self.assertEqual(gas_station_advanced(gas, cost), 3)

if __name__ == "__main__":
    unittest.main()
