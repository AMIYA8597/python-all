"""
## A. Concept Name
Advanced Computational Geometry

## B. One-Sentence Definition
Advanced Computational Geometry deals with algorithmic solutions to complex geometric problems, such as finding the convex hull or closest pair of points, while carefully managing edge cases and floating-point precision.

## C. Why Does This Exist?
To solve spatial and geometric problems efficiently (often in O(N log N) or better) in competitive programming, computer graphics, and robotics, where naive O(N^2) or O(N^3) approaches are too slow.

## D. Intuition
Imagine stretching a rubber band around a set of pegs on a board (Convex Hull), or recursively dividing points into left and right halves to find the closest two pegs (Divide and Conquer).

## E. Real-Life Analogy
Convex Hull is like wrapping a gift with a single piece of wrapping paper pulled tight over the outermost points. Closest Pair is like trying to find the two nearest cell towers in a state by dividing the state into smaller regions.

## F. Mental Model
- Convex Hull: Sort points, then sweep left-to-right building a "lower" boundary, and right-to-left building an "upper" boundary. Remove inner points that make "concave" turns.
- Closest Pair: Divide points by X-coordinate, find the closest pair in each half, then check a narrow strip along the dividing line for a closer pair crossing the halves.

## G. Visual Explanation
```
Convex Hull (Monotone Chain):
Sort points by X.
Add P1, P2.
If P3 makes a "right turn" (clockwise), pop P2.
Keep doing this to form the lower hull.
Repeat backwards for the upper hull.
```

## H. Formal Explanation
Computational geometry algorithms heavily rely on the 2D cross product to determine the orientation of ordered triplets of points (collinear, clockwise, counter-clockwise). The Graham Scan or Monotone Chain algorithms compute the Convex Hull in O(N log N) time by sorting and maintaining a stack of hull vertices. The closest pair of points problem uses a divide-and-conquer approach in O(N log N) time by recursively finding the minimum distance in two halves and merging them by checking a boundary strip.

## I. Mathematical Foundation (if applicable)
The 2D cross product of vectors OA and OB: 
cross_product = (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x)
- > 0: Counter-clockwise turn
- < 0: Clockwise turn
- == 0: Collinear

## J. From-Scratch Implementation (if applicable)
See the implementations of `convex_hull_monotone_chain` and `closest_pair_of_points` below.

## K. Library / Production Implementation (if applicable)
In production Python, libraries like `scipy.spatial` (e.g., `ConvexHull`) and `shapely` are heavily optimized in C/C++ and handle advanced geometric operations.

## L. Trace (walk through example)
Convex Hull for [(0,0), (3,0), (1,1), (0,3)]:
1. Sort: (0,0), (0,3), (1,1), (3,0).
2. Lower hull adds (0,0), (0,3). Adding (1,1) makes a right turn, so (0,3) is popped.
3. Continues until the lower and upper bounds are formed.

## M. Complexity
- Convex Hull (Monotone Chain): Time O(N log N) for sorting, O(N) for hull construction. Space O(N) to store hull points.
- Closest Pair: Time O(N log N) due to dividing and bounding strip checks to O(1) per point. Space O(N).

## N. Common Mistakes
- Using floating-point division to calculate slopes instead of integer cross products.
- Failing to handle collinear points correctly (e.g., whether to include or exclude points on the edges of the hull).
- Forgetting to handle base cases in recursive geometry algorithms (like N < 3).

## O. Common Confusions
- "Why use cross product instead of slope (y2-y1)/(x2-x1)?" 
  Because slope can lead to Division by Zero and floating-point inaccuracies. Cross product stays exact with integers.

## P. When To Use
- Collision detection in game development.
- Calculating the perimeter or area enclosing a set of data points.
- Analyzing geographic data and spatial proximity.

## Q. When NOT To Use
- When dealing with purely topological or graph-based problems where coordinate geometry doesn't apply.
- In higher dimensions (3D+), where these specific 2D algorithms (like Monotone Chain) do not directly translate.

## R. Trade-offs
- Writing robust geometry code is error-prone. Integer arithmetic is safe but can overflow in languages without arbitrary-precision integers (Python handles arbitrarily large integers, which is a major advantage).

## S. Debugging
- Plot your points! Using `matplotlib` to visualize the points and the resulting lines/hulls is the fastest way to spot errors.
- Test with collinear points and duplicate points.

## T. Memory Hook
"Cross product saves the day, keeps the floating point away."

## U. Active Recall
1. How does the cross product tell us if a turn is left or right?
2. What is the time complexity of the Monotone Chain algorithm and what dominates it?
3. In the closest pair divide-and-conquer algorithm, how many points do we check in the boundary strip per point?

## V. Practice
Modify the Convex Hull algorithm to strictly include collinear points that lie on the edges of the polygon.

## W. Interview Question
Given a set of points, write a function to determine if they form a strictly convex polygon in the given order. How would you handle collinearity?

## X. Project Connection
Used in the collision detection engine of our physics simulation module to compute bounding volumes for complex shapes.
"""

import math
from typing import List, Tuple

# Type aliases for readability
Point = Tuple[int, int]


def cross_product(o: Point, a: Point, b: Point) -> int:
    """
    Computes the 2D cross product of vectors OA and OB.
    
    A positive cross product indicates a counter-clockwise turn.
    A negative cross product indicates a clockwise turn.
    Zero indicates collinearity.
    
    Args:
        o: Origin point (x, y)
        a: Point A (x, y)
        b: Point B (x, y)
        
    Returns:
        Integer representing the magnitude and direction of the cross product.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull_monotone_chain(points: List[Point]) -> List[Point]:
    """
    Computes the convex hull of a set of 2D points using the Monotone Chain algorithm.
    
    Time Complexity: O(N log N) where N is the number of points (due to sorting).
    Space Complexity: O(N) to store the hull.
    
    Args:
        points: A list of 2D points (x, y).
        
    Returns:
        A list of points representing the convex hull in counter-clockwise order.
    """
    # Remove duplicates and sort lexicographically (by x, then y)
    points = sorted(list(set(points)))
    
    if len(points) <= 1:
        return points

    # Build the lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build the upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull. The last point of each list is omitted 
    # because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]


def dist_sq(p1: Point, p2: Point) -> int:
    """Calculates squared Euclidean distance between two points."""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def closest_pair_of_points(points: List[Point]) -> float:
    """
    Finds the minimum distance between any two points in the set.
    Uses a divide and conquer approach.
    
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    
    Args:
        points: A list of 2D points (x, y).
        
    Returns:
        The minimum Euclidean distance.
    """
    def recurse(px: List[Point], py: List[Point]) -> float:
        n = len(px)
        if n <= 3:
            # Base case: brute force for small sets
            min_d = float('inf')
            for i in range(n):
                for j in range(i + 1, n):
                    d = math.sqrt(dist_sq(px[i], px[j]))
                    if d < min_d:
                        min_d = d
            return min_d

        mid = n // 2
        mid_point = px[mid]
        
        # Divide
        pyl = [p for p in py if p[0] <= mid_point[0]]
        pyr = [p for p in py if p[0] > mid_point[0]]
        
        # In case of multiple points with the same x-coordinate, ensure we don't end up with empty lists
        if not pyl:
            pyl, pyr = py[:mid], py[mid:]
        if not pyr:
            pyl, pyr = py[:mid], py[mid:]
            
        dl = recurse(px[:mid], pyl)
        dr = recurse(px[mid:], pyr)
        
        d = min(dl, dr)
        
        # Strip area processing
        strip = [p for p in py if abs(p[0] - mid_point[0]) < d]
        
        min_d = d
        # Check points in the strip
        for i in range(len(strip)):
            # Inner loop runs at most 7 times due to geometric constraints
            for j in range(i + 1, min(i + 8, len(strip))):
                dist = math.sqrt(dist_sq(strip[i], strip[j]))
                if dist < min_d:
                    min_d = dist
                    
        return min_d

    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return recurse(px, py)


# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. Precision Issues: Avoid division and floats if possible. Use cross products instead of slopes.
# 2. Collinear Points: In Convex Hull, be precise about whether strictly greater than or >= is needed depending on whether you want all collinear boundary points.
# 3. Base Cases: Don't forget handling N < 3 gracefully.

# ==========================================
# Interview Challenge
# ==========================================
# Given a set of points, write a function to determine if they form a strictly convex polygon 
# in the given order. How would you handle collinearity?

if __name__ == "__main__":
    print("Testing Convex Hull (Monotone Chain)")
    pts = [(0, 0), (0, 3), (3, 3), (3, 0), (1, 1), (2, 2), (1, 2)]
    hull = convex_hull_monotone_chain(pts)
    print("Points:", pts)
    print("Hull:", hull)
    assert set(hull) == {(0, 0), (3, 0), (3, 3), (0, 3)}

    print("\nTesting Closest Pair of Points")
    pts2 = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    min_dist = closest_pair_of_points(pts2)
    print("Points:", pts2)
    print("Minimum Distance:", min_dist)
    # distance between (2,3) and (3,4) is sqrt(1^2 + 1^2) = 1.414...
    assert math.isclose(min_dist, math.sqrt(2), rel_tol=1e-5)
    
    print("\nAll tests passed successfully.")
