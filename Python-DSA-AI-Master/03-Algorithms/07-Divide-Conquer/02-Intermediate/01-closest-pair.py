"""
Closest Pair of Points Problem using Divide and Conquer.

Learning Objectives:
1. Apply divide and conquer to a geometric problem.
2. Understand the merging step in 2D space.
3. Optimize the minimum distance calculation.

Concept Explanation:
Given n points in a 2D plane, find the pair with the smallest Euclidean distance.
The D&C approach divides the points by a vertical line, finds min distance recursively
in left and right halves, and then checks a 'strip' near the dividing line for a closer pair.
"""

import math
from typing import List, Tuple

Point = Tuple[float, float]

def dist(p1: Point, p2: Point) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force(points: List[Point]) -> float:
    min_val = float('inf')
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            if dist(points[i], points[j]) < min_val:
                min_val = dist(points[i], points[j])
    return min_val

def closest_split_pair(p_x: List[Point], p_y: List[Point], delta: float, best_pair: Tuple[Point, Point]) -> Tuple[float, Tuple[Point, Point]]:
    mid_x = p_x[len(p_x) // 2][0]
    s_y = [p for p in p_y if mid_x - delta <= p[0] <= mid_x + delta]
    
    best_sq = delta
    n_y = len(s_y)
    
    for i in range(n_y - 1):
        for j in range(i + 1, min(i + 8, n_y)):
            p, q = s_y[i], s_y[j]
            d = dist(p, q)
            if d < best_sq:
                best_sq = d
                best_pair = (p, q)
                
    return best_sq, best_pair

def closest_pair_rec(p_x: List[Point], p_y: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    if len(p_x) <= 3:
        n = len(p_x)
        min_d = float('inf')
        best_pair = None
        for i in range(n):
            for j in range(i + 1, n):
                d = dist(p_x[i], p_x[j])
                if d < min_d:
                    min_d = d
                    best_pair = (p_x[i], p_x[j])
        return min_d, best_pair

    mid = len(p_x) // 2
    Q_x = p_x[:mid]
    R_x = p_x[mid:]
    
    midpoint = p_x[mid][0]  
    Q_y = list(filter(lambda x: x[0] <= midpoint, p_y))
    R_y = list(filter(lambda x: x[0] > midpoint, p_y))

    d1, pair1 = closest_pair_rec(Q_x, Q_y)
    d2, pair2 = closest_pair_rec(R_x, R_y)

    if d1 < d2:
        delta = d1
        best_pair = pair1
    else:
        delta = d2
        best_pair = pair2

    d3, pair3 = closest_split_pair(p_x, p_y, delta, best_pair)

    if d3 < delta:
        return d3, pair3
    return delta, best_pair

def closest_pair(points: List[Point]) -> float:
    """Advanced entry point for O(N log N) algorithm."""
    p_x = sorted(points, key=lambda x: x[0])
    p_y = sorted(points, key=lambda x: x[1])
    return closest_pair_rec(p_x, p_y)[0]

"""
Performance Analysis:
- Time Complexity: O(n log n).
- Space Complexity: O(n) for sorted arrays.

Edge Cases:
- Less than 2 points (error or infinity).
- Points with same coordinates.

Interview Challenge:
Extend this algorithm to find the closest pair in 3D space.
"""

def test_closest_pair():
    P = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    assert math.isclose(closest_pair(P), 1.41421356, rel_tol=1e-5)
    print("All tests passed.")

if __name__ == "__main__":
    test_closest_pair()
