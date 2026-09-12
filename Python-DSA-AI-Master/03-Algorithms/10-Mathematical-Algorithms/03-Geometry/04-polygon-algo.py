"""
Module: Polygon Algorithms

Learning Objectives:
1. Implement algorithms to check if a point is inside a polygon.
2. Calculate polygon properties (perimeter, area, convexity).
3. Apply Ray Casting algorithm.

Concept Explanation:
- Ray Casting algorithm determines if a point is inside a polygon by drawing a horizontal ray from the point and counting intersections with polygon edges. Odd = inside, Even = outside.
- Convex polygon check: All interior angles must be < 180 degrees (same orientation for all adjacent edges).

Performance Analysis:
- Ray casting: O(N) where N is the number of vertices.
- Convex check: O(N).

Edge Cases:
- Point lies exactly on the boundary of the polygon.
- Ray passes exactly through a vertex.
"""

from typing import List, Tuple

Point = Tuple[float, float]

# --- Basic Implementation ---
def polygon_perimeter(polygon: List[Point]) -> float:
    """Calculates the perimeter of a polygon."""
    import math
    perimeter = 0.0
    n = len(polygon)
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        perimeter += math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    return perimeter

# --- Intermediate Implementation ---
def is_convex(polygon: List[Point]) -> bool:
    """Checks if a polygon is convex."""
    n = len(polygon)
    if n < 3: return False
    
    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
        
    got_positive = False
    got_negative = False
    
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        p3 = polygon[(i + 2) % n]
        cp = cross_product(p1, p2, p3)
        if cp > 0: got_positive = True
        elif cp < 0: got_negative = True
        
        if got_positive and got_negative:
            return False
    return True

# --- Advanced Implementation ---
def point_in_polygon(pt: Point, polygon: List[Point]) -> bool:
    """
    Ray casting algorithm. Returns True if pt is strictly inside the polygon.
    Returns False if outside. If on boundary, behavior can be customized (we return False).
    """
    n = len(polygon)
    inside = False
    x, y = pt
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        
        # Check horizontal ray intersection
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= x_intersection:
                            inside = not inside
        p1x, p1y = p2x, p2y
        
    return inside

# --- Interview Challenge ---
# Problem: Largest Triangle Area
# Given points, find the area of the largest triangle.
def largest_triangle_area(points: List[Point]) -> float:
    """O(N^3) area check, can be improved using convex hull."""
    n = len(points)
    max_area = 0.0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                xA, yA = points[i]
                xB, yB = points[j]
                xC, yC = points[k]
                area = abs(xA*(yB - yC) + xB*(yC - yA) + xC*(yA - yB)) / 2.0
                max_area = max(max_area, area)
    return max_area

# --- Tests ---
def run_tests():
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert polygon_perimeter(square) == 8.0
    assert is_convex(square) == True
    
    concave = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]
    assert is_convex(concave) == False
    
    assert point_in_polygon((1, 1), square) == True
    assert point_in_polygon((3, 3), square) == False
    print("All tests passed for 04-polygon-algo.py!")

if __name__ == "__main__":
    run_tests()
