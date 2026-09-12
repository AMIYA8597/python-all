"""
Convex Hull Optimization

Learning Objectives:
1. Recognize DP formulations of the form dp[i] = min(dp[j] + m[j]*x[i] + c[j])
2. Understand the concept of maintaining a lower/upper envelope of lines.
3. Implement Convex Hull Trick (CHT) using a monotonic queue or dynamic CHT.

Concept Explanation:
Convex Hull Optimization speeds up DP transitions from O(N) to O(1) or O(log N)
when the transition cost can be represented as a set of linear functions y = mx + c.
If queries x[i] are monotonic, we can use a deque.

Basic:
- Concept of intersecting lines.
Intermediate:
- Monotonic CHT using deque.
Advanced:
- Dynamic CHT or Li Chao Tree (conceptually).

Type Hints:
Variables are often integers.

Performance Analysis:
Time Complexity: O(N) if slopes and queries are sorted, O(N log N) otherwise.
Space Complexity: O(N) for storing lines.
"""

from collections import deque
from typing import List, Tuple

class Line:
    def __init__(self, m: int, c: int):
        self.m = m
        self.c = c

    def eval(self, x: int) -> int:
        return self.m * x + self.c

    def intersect_x(self, other: 'Line') -> float:
        if self.m == other.m:
            return float('inf') if self.c > other.c else float('-inf')
        return (other.c - self.c) / (self.m - other.m)

class ConvexHullTrick:
    def __init__(self):
        self.lines = deque()

    def add(self, m: int, c: int):
        """Add line y = mx + c. Assumes slopes are added in strictly decreasing order for minimum."""
        line = Line(m, c)
        while len(self.lines) >= 2:
            l1, l2 = self.lines[-2], self.lines[-1]
            if l1.intersect_x(line) <= l1.intersect_x(l2):
                self.lines.pop()
            else:
                break
        self.lines.append(line)

    def query(self, x: int) -> int:
        """Query min value at x. Assumes query x are strictly increasing."""
        if not self.lines:
            return 0
        while len(self.lines) >= 2:
            if self.lines[0].eval(x) >= self.lines[1].eval(x):
                self.lines.popleft()
            else:
                break
        return self.lines[0].eval(x)

def basic_cht_example(slopes: List[int], intercepts: List[int], queries: List[int]) -> List[int]:
    cht = ConvexHullTrick()
    for m, c in zip(slopes, intercepts):
        cht.add(m, c)
    return [cht.query(x) for x in queries]

def test_functions():
    slopes = [-1, -2, -3]
    intercepts = [10, 12, 16]
    queries = [1, 2, 3]
    res = basic_cht_example(slopes, intercepts, queries)
    assert res == [9, 8, 7]
    print("All tests passed.")

if __name__ == "__main__":
    test_functions()
