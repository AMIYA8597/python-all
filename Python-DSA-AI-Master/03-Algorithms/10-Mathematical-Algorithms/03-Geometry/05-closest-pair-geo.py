"""
Module: Closest Pair of Points

Learning Objectives:
1. Understand the Divide and Conquer approach in geometry.
2. Implement an O(N log N) algorithm for finding the closest pair of points.
3. Compare brute-force and optimized approaches.

Concept Explanation:
- The problem is to find two points in an array with the minimum Euclidean distance.
- Divide and Conquer: Sort points by x-coordinate. Recursively find minimum distance in left and right halves.
- The 'strip' problem: Check points near the dividing line. Sort by y-coordinate and check only the next 7 points.

Performance Analysis:
- Brute Force: O(N^2)
- Divide and Conquer: O(N log N) time, O(N) space.

Edge Cases:
- Less than 2 points (return infinity).
- Points with identical coordinates (distance is 0).
"""

import math
from typing import List, Tuple

Point = Tuple[float, float]

# --- Basic Implementation ---
def distance(p1: Point, p2: Point) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def closest_pair_bruteforce(points: List[Point]) -> float:
    """O(N^2) time approach to find the minimum distance."""
    n = len(points)
    min_dist = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
    return min_dist

# --- Intermediate / Advanced Implementation ---
def closest_pair_recursive(points_x: List[Point], points_y: List[Point]) -> float:
    """Recursive step for Divide and Conquer."""
    n = len(points_x)
    if n <= 3:
        return closest_pair_bruteforce(points_x)
        
    mid = n // 2
    mid_point = points_x[mid]
    
    P_y_left = []
    P_y_right = []
    
    # Split y-sorted points into left and right while maintaining y-order
    for p in points_y:
        if p[0] <= mid_point[0]:
            P_y_left.append(p)
        else:
            P_y_right.append(p)
            
    dl = closest_pair_recursive(points_x[:mid], P_y_left)
    dr = closest_pair_recursive(points_x[mid:], P_y_right)
    d = min(dl, dr)
    
    # Build strip array
    strip = [p for p in points_y if abs(p[0] - mid_point[0]) < d]
    
    # Check points in the strip
    min_a = d
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):
            min_a = min(min_a, distance(strip[i], strip[j]))
            
    return min_a

def closest_pair(points: List[Point]) -> float:
    """O(N log N) algorithm for closest pair of points."""
    points_x = sorted(points, key=lambda p: p[0])
    points_y = sorted(points, key=lambda p: p[1])
    return closest_pair_recursive(points_x, points_y)

# --- Interview Challenge ---
# Problem: Closest Pair Index
# Modify the algorithm to return the indices or actual points of the closest pair.
# (Left as an exercise to extend the return tuple)

# --- Tests ---
def run_tests():
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    
    dist_bf = closest_pair_bruteforce(pts)
    dist_dc = closest_pair(pts)
    
    # closest are (2,3) and (3,4) with distance sqrt(1^2 + 1^2) = 1.414...
    assert abs(dist_bf - math.sqrt(2)) < 1e-9
    assert abs(dist_dc - dist_bf) < 1e-9
    print("All tests passed for 05-closest-pair-geo.py!")

if __name__ == "__main__":
    run_tests()
