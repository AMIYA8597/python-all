"""
## A. Concept Name
Convex Hull & Rotating Calipers

## B. Concept Explanation
The Convex Hull of a set of points is the smallest convex polygon that encloses all the points. Imagine snapping a rubber band around a set of pegs on a board; the shape of the rubber band is the convex hull. Finding the convex hull is a fundamental problem in computational geometry. It acts as a preprocessing step for many other algorithms, reducing the problem size from all points to just the boundary points. It is heavily used in pattern recognition, collision detection, and clustering.

## C. Problem Statement
1. Given a set of 2D points, find the points that form its convex hull in counter-clockwise order.
2. Given a set of 2D points, find the maximum distance (diameter) between any two points in the set.

## D. Logic/Approach
1. **Convex Hull (Monotone Chain)**: Sort points lexicographically. Build the lower hull by adding points one by one, removing any that make a clockwise turn (using the cross product). Repeat the process in reverse order to build the upper hull. Concatenate both halves.
2. **Rotating Calipers (Diameter)**: First, compute the convex hull (since the furthest points must lie on the hull). Then iterate through all edges of the hull. For each edge, find the point furthest from it by checking triangle areas. Move the "calipers" around the polygon, recording the maximum distance found.

## E. Time & Space Complexity
- Convex Hull: Time O(N log N) for sorting, O(N) for building the hull. Space O(N).
- Polygon Diameter: Time O(N log N) to find the hull, O(H) for calipers where H is hull size. Space O(N).

## F. Edge Cases
- Less than 3 points (already forms its own hull).
- Collinear points (handled by cross product condition <= 0).
- Only one point in the dataset (diameter is 0.0).

## G. Related/Similar Problems
- Graham Scan (alternative Convex Hull algorithm)
- Closest Pair of Points (Divide & Conquer)
- Minimum Enclosing Circle

## X. Project Connection
- Computer Vision: Object boundary detection, hand gesture recognition.
- Game Development: Fast 2D/3D collision detection using bounding boxes/hulls.
- Data Science: Finding enclosing geometries for data clustering and support vector machines (SVM).
"""
from typing import List, Tuple
import math

Point = Tuple[int, int]

def cross_product(o: Point, a: Point, b: Point) -> int:
    """
    2D cross product of OA and OB vectors.
    Returns a positive value if O, A, B form a counter-clockwise turn,
    negative for clockwise, and zero if collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


# =============================================================================
# 1. Convex Hull: Monotone Chain Algorithm
# =============================================================================
def convex_hull(points: List[Point]) -> List[Point]:
    """
    Computes the convex hull of a set of 2D points using the Monotone Chain algorithm.
    
    Time Complexity: O(N log N) for sorting, O(N) for building the hull. Total: O(N log N).
    Space Complexity: O(N) for the hull storage.
    
    Args:
        points: A list of 2D points (x, y).
        
    Returns:
        List of points in the convex hull in counter-clockwise order.
    """
    n = len(points)
    if n <= 3:
        # Sort to maintain consistent order, but a triangle or line is its own hull.
        return sorted(points)

    # Sort points lexicographically (by x, then by y)
    sorted_points = sorted(points)

    # Build the lower hull
    lower: List[Point] = []
    for p in sorted_points:
        # Remove points that make a clockwise turn
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build the upper hull
    upper: List[Point] = []
    for p in reversed(sorted_points):
        # Remove points that make a clockwise turn
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull. The last point of each half is omitted
    # because it is repeated at the beginning of the other half.
    return lower[:-1] + upper[:-1]


# =============================================================================
# 2. Polygon Diameter: Rotating Calipers
# =============================================================================
def dist_sq(p1: Point, p2: Point) -> int:
    """Returns the squared Euclidean distance between two points."""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def polygon_diameter(points: List[Point]) -> float:
    """
    Finds the maximum distance between any two points in the set.
    First finds the convex hull, then uses Rotating Calipers.
    
    Time Complexity: O(N log N) for hull, O(H) for calipers where H is hull size.
    Space Complexity: O(N)
    
    Args:
        points: List of points.
        
    Returns:
        Maximum distance between any two points.
    """
    hull = convex_hull(points)
    n = len(hull)
    
    if n == 1:
        return 0.0
    if n == 2:
        return math.sqrt(dist_sq(hull[0], hull[1]))

    max_dist_sq = 0
    j = 1
    
    # Iterate through all edges of the hull
    for i in range(n):
        # Find the point j that is furthest from the edge i to i+1
        # using the area of the triangle formed by (i, i+1, j) as a proxy for distance
        next_i = (i + 1) % n
        
        while True:
            next_j = (j + 1) % n
            # If moving to next_j increases the triangle area, keep moving j
            area_j = abs(cross_product(hull[i], hull[next_i], hull[j]))
            area_next_j = abs(cross_product(hull[i], hull[next_i], hull[next_j]))
            
            if area_next_j > area_j:
                j = next_j
            else:
                break
                
        # Check distance between point i and point j
        max_dist_sq = max(max_dist_sq, dist_sq(hull[i], hull[j]))
        max_dist_sq = max(max_dist_sq, dist_sq(hull[next_i], hull[j]))

    return math.sqrt(max_dist_sq)


# =============================================================================
# Interview Challenge
# =============================================================================
# Question: Why do we use the cross product condition `<= 0` when popping points 
# from our hull stack?
# Answer: The condition `cross_product(A, B, C) <= 0` means that the sequence 
# of points A -> B -> C forms a clockwise turn or is perfectly straight.
# In a true strictly convex hull, all internal angles must be less than 180 degrees 
# (counter-clockwise turns). Popping points that fail this ensures the boundary remains convex.


if __name__ == "__main__":
    print("Testing Convex Hull & Rotating Calipers...")
    
    points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
    expected_hull = [(0, 0), (3, 0), (3, 3), (0, 3)]
    
    hull = convex_hull(points)
    # The starting point may vary depending on tie-breakers, but the set is the same.
    assert set(hull) == set(expected_hull)
    print("Convex Hull Test: PASS")
    
    # Distance between (0, 0) and (3, 3) is sqrt(18) = 4.2426...
    diam = polygon_diameter(points)
    assert abs(diam - math.sqrt(18)) < 1e-6
    print("Polygon Diameter Test: PASS")
    
    print("All tests passed!")
