"""
Module: Convex Hull Algorithms

Learning Objectives:
1. Understand what a convex hull is.
2. Implement the Monotone Chain algorithm.
3. Handle collinear points gracefully.

Concept Explanation:
- The convex hull of a set of points is the smallest convex polygon that contains all points.
- Monotone Chain builds the lower and upper hulls separately after sorting points lexicographically.

Performance Analysis:
- Sorting takes O(N log N).
- Hull construction takes O(N).
- Overall time complexity: O(N log N).

Edge Cases:
- Fewer than 3 points (convex hull is the points themselves).
- All points are collinear.
- Duplicate points.
"""

from typing import List, Tuple

# --- Basic / Intermediate Implementation ---
# Using Tuple[float, float] for points (x, y)
Point = Tuple[float, float]

def cross_product(o: Point, a: Point, b: Point) -> float:
    """Returns 2D cross product of OA and OB vectors."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# --- Advanced Implementation ---
def convex_hull(points: List[Point]) -> List[Point]:
    """Computes the convex hull using the Monotone Chain algorithm."""
    # Remove duplicates and sort lexicographically
    points = sorted(list(set(points)))
    
    if len(points) <= 1:
        return points
        
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
        
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
        
    # Concatenate lower and upper hull. The last point of each is the first of the other.
    return lower[:-1] + upper[:-1]

# --- Interview Challenge ---
# Problem: Maximum area triangle from a set of points.
# The vertices of the maximum area triangle must lie on the convex hull.
def max_area_triangle(points: List[Point]) -> float:
    """O(H^3) naive check on convex hull vertices, where H is hull size."""
    hull = convex_hull(points)
    n = len(hull)
    max_area = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                # Area = 0.5 * abs(cross_product(A, B, C))
                area = abs(cross_product(hull[i], hull[j], hull[k])) / 2.0
                max_area = max(max_area, area)
    return max_area

# --- Tests ---
def run_tests():
    pts = [(0, 0), (0, 2), (2, 2), (2, 0), (1, 1)]
    hull = convex_hull(pts)
    # The convex hull of the square with a center point is the square itself
    assert len(hull) == 4
    assert (1, 1) not in hull
    
    assert max_area_triangle(pts) == 2.0 # Triangle with base 2, height 2 -> area 2
    print("All tests passed for 02-convex-hull.py!")

if __name__ == "__main__":
    run_tests()
