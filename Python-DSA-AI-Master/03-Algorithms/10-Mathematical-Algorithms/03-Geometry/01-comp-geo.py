"""
Module: Basic Computational Geometry

Learning Objectives:
1. Model geometric objects like Points and Lines in Python.
2. Implement distance, dot product, and cross product.
3. Understand orientation (collinear, clockwise, counterclockwise).

Concept Explanation:
- Points are often represented as tuples (x, y) or classes.
- Cross product of 2D vectors A and B: A.x * B.y - A.y * B.x.
- The sign of the cross product determines the orientation of three points.

Performance Analysis:
- Point operations are O(1).
- Polygon area via Shoelace is O(N) where N is number of vertices.

Edge Cases:
- Coincident points.
- Collinear points in geometric checks.
"""

import math
from typing import Tuple, List

# --- Basic Implementation ---
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

def euclidean_distance(p1: Point, p2: Point) -> float:
    """Returns Euclidean distance between two points."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

# --- Intermediate Implementation ---
def cross_product(p1: Point, p2: Point, p3: Point) -> float:
    """
    Returns cross product of vectors (p2-p1) and (p3-p2).
    Positive if counter-clockwise, negative if clockwise, 0 if collinear.
    """
    return (p2.x - p1.x) * (p3.y - p2.y) - (p2.y - p1.y) * (p3.x - p2.x)

def orientation(p1: Point, p2: Point, p3: Point) -> int:
    """
    0 -> Collinear
    1 -> Clockwise
    2 -> Counterclockwise
    """
    val = (p2.y - p1.y) * (p3.x - p2.x) - (p2.x - p1.x) * (p3.y - p2.y)
    if val == 0: return 0
    return 1 if val > 0 else 2

# --- Advanced Implementation ---
def polygon_area(points: List[Point]) -> float:
    """
    Computes the area of a simple polygon using the Shoelace formula.
    Vertices must be given in order (CW or CCW).
    """
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += (points[i].x * points[j].y) - (points[j].x * points[i].y)
    return abs(area) / 2.0

# --- Interview Challenge ---
# Problem: Check if 4 points form a rectangle
def is_rectangle(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """Returns True if the 4 points form a rectangle."""
    def dist_sq(a, b):
        return (a.x - b.x)**2 + (a.y - b.y)**2
    
    # Calculate all pair distances
    pts = [p1, p2, p3, p4]
    dists = []
    for i in range(4):
        for j in range(i + 1, 4):
            dists.append(dist_sq(pts[i], pts[j]))
    dists.sort()
    
    # A rectangle has 4 equal sides (if square) or 2 pairs of equal sides,
    # but more importantly: 4 equal sides (dists[0..3]) or 2 pairs of equal sides (dists[0]==dists[1], dists[2]==dists[3]),
    # AND 2 equal diagonals (dists[4]==dists[5]).
    if dists[0] == 0: return False # overlapping points
    return dists[0] == dists[1] and dists[2] == dists[3] and dists[4] == dists[5]

# --- Tests ---
def run_tests():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert euclidean_distance(p1, p2) == 5.0
    
    # Collinear
    assert orientation(Point(0,0), Point(1,1), Point(2,2)) == 0
    # CCW
    assert orientation(Point(0,0), Point(1,0), Point(0,1)) == 2
    
    rect = [Point(0,0), Point(0,2), Point(2,2), Point(2,0)]
    assert polygon_area(rect) == 4.0
    assert is_rectangle(Point(0,0), Point(0,2), Point(2,2), Point(2,0)) == True
    print("All tests passed for 01-comp-geo.py!")

if __name__ == "__main__":
    run_tests()
