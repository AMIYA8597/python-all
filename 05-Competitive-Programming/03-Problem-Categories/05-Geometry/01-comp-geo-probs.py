"""
## A. Concept Name
Computational Geometry - Competitive Programming

## B. What is it?
Computational Geometry involves designing algorithms and data structures to solve geometric problems efficiently. It deals with points, lines, polygons, circles, and intersections in 2D and 3D space.

## C. Why it exists?
Many applications require manipulating and querying spatial data. Floating-point precision issues and edge cases (like collinear points) make geometry problems notoriously difficult. Dedicated algorithms exist to handle these robustly using integer arithmetic where possible.

## D. Industry Use Cases
- Computer Graphics: Rendering pipelines, clipping, collision detection.
- GIS (Geographic Information Systems): Spatial queries, map routing, geofencing.
- Robotics: Path planning, obstacle avoidance.
- CAD (Computer-Aided Design): 3D modeling, structural analysis.

## E. Learning Objectives
1. Master vector operations for geometric calculations (cross product, dot product).
2. Understand robust orientation tests to avoid floating-point errors.
3. Solve common geometry problems: Line Intersection, Point in Polygon, and Polygon Area.

## F. Core Math: Cross Product
The cross product helps in determining the orientation of three points (clockwise, counter-clockwise, or collinear), which is foundational for most 2D geometric algorithms.

## G. Orientation Principles
Using integer cross products guarantees exact results without the inaccuracies of floating-point division.

## H. Line Intersection
Determines if two line segments cross each other by checking the orientations of the endpoints of one segment relative to the other.

## I. Polygon Area
The Shoelace formula computes the area of a simple polygon using the coordinates of its vertices.

## J. Point in Polygon
The Ray Casting algorithm checks how many times a ray starting from the point intersects the polygon's edges to determine if it is inside.

## K. Floating-Point Pitfalls
Floating-point arithmetic has rounding errors which can cause collinear points to be mistakenly identified as non-collinear.

## L. Time Complexity
Most fundamental tests like orientation and intersection are O(1). Polygon operations are typically O(N) where N is the number of vertices.

## M. Space Complexity
Usually O(1) auxiliary space, as algorithms process coordinate pairs without needing complex data structures.

## N. Edge Cases
Collinear segments overlapping, point on the polygon boundary, and degenerate polygons (less than 3 vertices).

## O. Robustness
Always use integer arithmetic for orientation tests if the input coordinates are integers.

## P. Common Pitfalls
Using division (slopes) instead of cross products for checking parallelism or collinearity.

## Q. Data Representation
Points are best represented as tuples of integers or simple objects with x and y properties.

## R. Interview Challenge
How does floating-point imprecision affect geometric algorithms, and how do techniques like cross product help? (Answer: Integer cross products avoid decimal rounding errors entirely).

## S. Related Concepts
Convex Hull (Graham Scan, Jarvis March), Line Sweep algorithms.

## T. Code Readability
Modularizing operations like `orientation` and `on_segment` keeps complex logic manageable.

## U. Scalability
Efficient O(N log N) algorithms are required for processing millions of points, building on these basic O(1) tests.

## V. Testing & Verification
Verify with simple convex and concave polygons, as well as extreme points and collinear edge cases.

## W. Future Exploration
3D geometry, Voronoi diagrams, and Delaunay triangulations.

## X. Project Connection
These core primitives are used in building larger spatial engines, rendering systems, and competitive programming templates where geometric robustness is required.
"""
from typing import Tuple, List, Optional
import math

# Point representation
Point = Tuple[int, int]

# =============================================================================
# 1. Core Concept: Cross Product & Orientation
# =============================================================================
def orientation(p: Point, q: Point, r: Point) -> int:
    """
    Finds the orientation of an ordered triplet (p, q, r).
    Uses the cross product of vectors pq and qr.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Returns:
        0 if p, q, and r are collinear
        1 if clockwise (CW)
        2 if counter-clockwise (CCW)
    """
    # Cross product formula: (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise if > 0, Counter-clockwise if < 0


def on_segment(p: Point, q: Point, r: Point) -> bool:
    """
    Given three collinear points p, q, r, checks if point q lies on line segment 'pr'.
    """
    if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
        return True
    return False


# =============================================================================
# 2. Line Intersection
# =============================================================================
def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """
    Returns True if line segment 'p1q1' and 'p2q2' intersect.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases (Collinear intersections)
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False


# =============================================================================
# 3. Polygon Area (Shoelace Formula)
# =============================================================================
def polygon_area(points: List[Point]) -> float:
    """
    Calculates the area of a simple polygon given its vertices in order.
    Uses the Shoelace Formula.
    
    Time Complexity: O(N) where N is the number of vertices.
    Space Complexity: O(1)
    """
    n = len(points)
    if n < 3:
        return 0.0
        
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        # (x_i * y_i+1) - (x_i+1 * y_i)
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
        
    return abs(area) / 2.0


# =============================================================================
# 4. Point in Polygon (Ray Casting Algorithm)
# =============================================================================
def is_point_in_polygon(points: List[Point], p: Point) -> bool:
    """
    Checks whether a point 'p' lies inside a polygon defined by 'points'.
    Uses the ray-casting algorithm.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    n = len(points)
    if n < 3:
        return False

    # Create a point for ray segment from p to infinity
    extreme = (10**9, p[1])
    
    count = 0
    i = 0
    while True:
        next_i = (i + 1) % n
        
        # Check if segment from p to extreme intersects with polygon edge
        if do_intersect(points[i], points[next_i], p, extreme):
            # If the point is collinear with edge, check if it's on segment
            if orientation(points[i], p, points[next_i]) == 0:
                return on_segment(points[i], p, points[next_i])
            count += 1
            
        i = next_i
        if i == 0:
            break
            
    # Return true if count is odd
    return (count % 2 == 1)


# =============================================================================
# Interview Challenge
# =============================================================================
# Question: How does floating-point imprecision affect geometric algorithms, 
# and how do techniques like cross product help?
# Answer: Floating-point arithmetic has rounding errors which can cause 
# collinear points to be mistakenly identified as non-collinear (or vice versa),
# breaking the logic of intersections or hull constructions. Cross product using
# integers operates precisely without decimals, completely avoiding these bugs.


if __name__ == "__main__":
    print("Testing Computational Geometry algorithms...")
    
    p1 = (1, 1)
    q1 = (10, 1)
    p2 = (1, 2)
    q2 = (10, 2)
    assert do_intersect(p1, q1, p2, q2) == False
    
    p3 = (10, 0)
    q3 = (0, 10)
    p4 = (0, 0)
    q4 = (10, 10)
    assert do_intersect(p3, q3, p4, q4) == True
    
    polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
    assert polygon_area(polygon) == 100.0
    
    assert is_point_in_polygon(polygon, (5, 5)) == True
    assert is_point_in_polygon(polygon, (20, 20)) == False
    
    print("All tests passed!")
