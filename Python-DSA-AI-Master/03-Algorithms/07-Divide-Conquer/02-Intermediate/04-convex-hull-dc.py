"""
Convex Hull (QuickHull Algorithm using Divide and Conquer).

Learning Objectives:
1. Understand the Convex Hull geometric problem.
2. Implement QuickHull algorithm based on D&C.
3. Determine geometric distances and orientation.

Concept Explanation:
The Convex Hull of a set of points is the smallest convex polygon that contains all points.
QuickHull finds the hull by finding the points with min/max x coordinates, forming a line,
and recursively finding the points furthest from this line on both sides.
"""

from typing import List, Tuple

Point = Tuple[int, int]

def find_side(p1: Point, p2: Point, p: Point) -> int:
    """Returns side of p with respect to line p1-p2."""
    val = (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0

def line_dist(p1: Point, p2: Point, p: Point) -> int:
    """Proportional distance of p from line p1-p2."""
    return abs((p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0]))

def quickhull(points: List[Point], n: int, p1: Point, p2: Point, side: int, hull: set):
    ind = -1
    max_dist = 0

    for i in range(n):
        temp = line_dist(p1, p2, points[i])
        if find_side(p1, p2, points[i]) == side and temp > max_dist:
            ind = i
            max_dist = temp

    if ind == -1:
        hull.add(p1)
        hull.add(p2)
        return

    quickhull(points, n, points[ind], p1, -find_side(points[ind], p1, p2), hull)
    quickhull(points, n, points[ind], p2, -find_side(points[ind], p2, p1), hull)

def print_hull(points: List[Point]) -> List[Point]:
    """Entry point for QuickHull."""
    n = len(points)
    if n < 3:
        return points

    min_x = 0
    max_x = 0
    for i in range(1, n):
        if points[i][0] < points[min_x][0]:
            min_x = i
        if points[i][0] > points[max_x][0]:
            max_x = i

    hull = set()
    quickhull(points, n, points[min_x], points[max_x], 1, hull)
    quickhull(points, n, points[min_x], points[max_x], -1, hull)

    return sorted(list(hull))

"""
Performance Analysis:
- Time Complexity: Best O(n log n). Worst O(n^2) when points lie on boundary.
- Space Complexity: O(n) for recursion stack.

Edge Cases:
- Less than 3 points.
- Collinear points.
- Duplicate points.

Interview Challenge:
Compare QuickHull with Graham Scan algorithm.
"""

def test_quickhull():
    points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    hull = print_hull(points)
    # Expected hull points (could vary slightly in order but set matches)
    expected = [(0, 0), (0, 3), (3, 1), (4, 4)]
    assert sorted(hull) == expected
    print("All tests passed.")

if __name__ == "__main__":
    test_quickhull()
