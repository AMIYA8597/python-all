"""
Merge Intervals Pattern - Comprehensive Guide

Learning Objectives:
- Understand how to solve problems involving overlapping intervals
- Learn to sort intervals and traverse them to find overlaps
- Analyze time and space complexity
- Solve problems like merging intervals, inserting intervals, finding intersections

Concept Explanation:
This pattern describes an efficient technique to deal with overlapping intervals. In a lot of problems involving intervals, you either need to find overlapping intervals or merge intervals if they overlap. Given two intervals (a, b) and (c, d), there are 6 permutations of how they can interact, but they can be generalized to:
1. 'a' and 'b' do not overlap
2. 'a' and 'b' overlap, 'b' ends after 'a'
3. 'a' completely overlaps 'b'
4. 'b' completely overlaps 'a'

When to use:
- You're asked to produce a list with only mutually exclusive intervals
- Dealing with overlapping events, schedules, or time frames
"""

from typing import List

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __repr__(self):
        return f"[{self.start}, {self.end}]"

# Basic: Merge Intervals
def merge_intervals(intervals: List[Interval]) -> List[Interval]:
    """
    Given a list of intervals, merge all the overlapping intervals to produce a list 
    that has only mutually exclusive intervals.
    Time Complexity: O(N*logN) - for sorting
    Space Complexity: O(N) - for output
    """
    if len(intervals) < 2:
        return intervals

    intervals.sort(key=lambda x: x.start)
    merged = []
    
    start = intervals[0].start
    end = intervals[0].end
    
    for i in range(1, len(intervals)):
        interval = intervals[i]
        if interval.start <= end:  # overlapping
            end = max(end, interval.end)
        else:  # non-overlapping
            merged.append(Interval(start, end))
            start = interval.start
            end = interval.end
            
    # Add the last interval
    merged.append(Interval(start, end))
    return merged


# Intermediate: Insert Interval
def insert_interval(intervals: List[Interval], new_interval: Interval) -> List[Interval]:
    """
    Given a list of non-overlapping intervals sorted by their start time, insert a given interval 
    at the correct position and merge all necessary intervals to produce a list that has only mutually exclusive intervals.
    Time Complexity: O(N)
    Space Complexity: O(N)
    """
    merged = []
    i, n = 0, len(intervals)

    # skip all intervals that come before the 'new_interval'
    while i < n and intervals[i].end < new_interval.start:
        merged.append(intervals[i])
        i += 1

    # merge all intervals that overlap with 'new_interval'
    while i < n and intervals[i].start <= new_interval.end:
        new_interval.start = min(intervals[i].start, new_interval.start)
        new_interval.end = max(intervals[i].end, new_interval.end)
        i += 1
        
    merged.append(new_interval)

    # add all the remaining intervals
    while i < n:
        merged.append(intervals[i])
        i += 1

    return merged


def run_tests():
    print("Testing Merge Intervals...")
    intervals = [Interval(1, 4), Interval(2, 5), Interval(7, 9)]
    merged = merge_intervals(intervals)
    assert merged == [Interval(1, 5), Interval(7, 9)]
    
    intervals2 = [Interval(1, 3), Interval(5, 7), Interval(8, 12)]
    new_merged = insert_interval(intervals2, Interval(4, 6))
    assert new_merged == [Interval(1, 3), Interval(4, 7), Interval(8, 12)]
    
    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
