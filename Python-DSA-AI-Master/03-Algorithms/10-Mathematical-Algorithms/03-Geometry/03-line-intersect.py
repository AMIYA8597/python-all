"""
Module: Line Intersection Algorithms

Learning Objectives:
1. Learn how to check if two line segments intersect.
2. Calculate the exact intersection point of two lines.
3. Understand orientation and its use in intersection.

Concept Explanation:
- Two segments (p1, q1) and (p2, q2) intersect if they straddle each other.
- The intersection point can be found using Cramer's rule on line equations (Ax + By = C).

Performance Analysis:
- Intersection check: O(1) time.
- Exact intersection: O(1) time.

Edge Cases:
- Parallel lines (no intersection).
- Collinear, overlapping segments.
"""

from typing import Tuple, Optional

Point = Tuple[float, float]

# --- Basic Implementation ---
def on_segment(p: Point, q: Point, r: Point) -> bool:
    """Given three collinear points p, q, r, checks if q lies on segment pr."""
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and \
           min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

def orientation(p: Point, q: Point, r: Point) -> int:
    """0 -> Collinear, 1 -> Clockwise, 2 -> Counterclockwise"""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """Returns True if segment p1q1 intersects with segment p2q2."""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    # General case
    if o1 != o2 and o3 != o4:
        return True
        
    # Special cases: collinear and overlapping
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    
    return False

# --- Intermediate/Advanced Implementation ---
def line_intersection(A: Point, B: Point, C: Point, D: Point) -> Optional[Point]:
    """
    Returns the exact intersection point of the lines defined by AB and CD.
    Returns None if lines are parallel.
    Uses determinants (Cramer's rule).
    """
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1 * A[0] + b1 * A[1]
    
    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2 * C[0] + b2 * C[1]
    
    determinant = a1 * b2 - a2 * b1
    
    if determinant == 0:
        return None # Parallel lines
        
    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return (x, y)

# --- Interview Challenge ---
# Problem: Check if a point is inside a polygon
# See 04-polygon-algo.py for Ray Casting algorithm which relies on segment intersection.

# --- Tests ---
def run_tests():
    # Crossing segments
    assert do_intersect((0, 0), (2, 2), (0, 2), (2, 0)) == True
    # Parallel segments
    assert do_intersect((0, 0), (0, 2), (1, 0), (1, 2)) == False
    
    # Intersection point
    pt = line_intersection((0, 0), (2, 2), (0, 2), (2, 0))
    assert pt is not None
    assert abs(pt[0] - 1.0) < 1e-9 and abs(pt[1] - 1.0) < 1e-9
    
    # Parallel lines intersection point
    assert line_intersection((0, 0), (0, 2), (1, 0), (1, 2)) is None
    print("All tests passed for 03-line-intersect.py!")

if __name__ == "__main__":
    run_tests()
