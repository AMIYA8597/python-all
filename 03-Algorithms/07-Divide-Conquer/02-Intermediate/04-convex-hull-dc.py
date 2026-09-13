"""
# ==============================================================================
# LABORATORY: CONVEX HULL (QUICKHULL DIVIDE & CONQUER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have a map with 1,000 points representing trees in a forest. 
# You want to build a fence that physically encloses ALL of the trees using the 
# absolute minimum amount of wood.
#
# This is the "Convex Hull" problem in Computational Geometry. 
# Imagine stretching a giant rubber band around the entire forest and letting it 
# snap. The rubber band will form a polygon. The trees that the rubber band touches 
# are the "Vertices" of the Convex Hull.
#
# There are many algorithms to solve this (Graham Scan, Jarvis March). 
# But the most elegant Divide & Conquer approach is "Quickhull", invented in 1977.
#
# It is the geometric equivalent of Quick Sort!
# 1. DIVIDE: Find the leftmost tree (A) and rightmost tree (B). Draw a line between 
#    them. This cuts the forest into a "Top" set of trees and a "Bottom" set.
# 2. CONQUER: For the Top set, find the tree (C) that is mathematically FARTHEST 
#    away from the line A-B. The triangle A-B-C is guaranteed to be inside the hull.
# 3. PRUNE: Any trees inside the triangle A-B-C are instantly deleted from existence!
#    They can never be part of the outer fence.
# 4. RECURSE: Repeat the process for the line A-C and the line C-B.
#
# Quickhull eliminates massive chunks of data at every step, yielding a blistering 
# fast O(N log N) average time complexity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the geometric equivalent of Quick Sort.
# - Calculate the perpendicular distance from a point to a line.
# - Determine which side of a line a point lies on using Cross Products.
#
# ==============================================================================
"""

import math
from typing import List, Tuple, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GEOMETRIC MATH HELPERS
# ==============================================================================
def line_dist(p1: Tuple[int, int], p2: Tuple[int, int], p: Tuple[int, int]) -> int:
    """
    Returns the proportional distance of point `p` from the line `p1->p2`.
    (We don't need the exact euclidean distance, just the relative magnitude, 
    so we skip the expensive square root operation!)
    """
    return abs((p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0]))


def point_location(p1: Tuple[int, int], p2: Tuple[int, int], p: Tuple[int, int]) -> int:
    """
    Uses the Cross Product to determine where `p` is relative to the line `p1->p2`.
    Returns > 0 if `p` is on the LEFT side of the line.
    Returns < 0 if `p` is on the RIGHT side of the line.
    Returns 0 if `p` is exactly ON the line.
    """
    val = (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])
    if val > 0:
        return 1
    elif val < 0:
        return -1
    return 0


# ==============================================================================
# 4. QUICKHULL DIVIDE & CONQUER ENGINE
# ==============================================================================
def quickhull(points: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Expected Time Complexity: O(N log N).
    Worst Case: O(N^2) if the points already form a convex polygon.
    Space Complexity: O(N) for recursion and hull tracking.
    """
    hull = set()
    n = len(points)
    
    if n < 3:
        return set(points)
        
    # 1. FIND THE ABSOLUTE EXTREMES
    # The leftmost point (min X) and rightmost point (max X) are MATHEMATICALLY 
    # GUARANTEED to be on the Convex Hull.
    min_x_point = min(points, key=lambda p: p[0])
    max_x_point = max(points, key=lambda p: p[0])
    
    hull.add(min_x_point)
    hull.add(max_x_point)
    
    # 2. DIVIDE THE DATASET
    # Split the remaining points into two groups: those "above" the line from 
    # min_x to max_x, and those "below" the line.
    left_set = []
    right_set = []
    
    for p in points:
        if p == min_x_point or p == max_x_point:
            continue
        loc = point_location(min_x_point, max_x_point, p)
        if loc == 1:
            left_set.append(p)
        elif loc == -1:
            right_set.append(p)
            
    # 3. RECURSIVE CONQUER
    def build_hull(p1, p2, subset):
        if not subset:
            return
            
        # Find the point in this subset that is FARTHEST from the line p1->p2.
        # This point is guaranteed to be on the Convex Hull!
        farthest_point = None
        max_dist = -1
        
        for p in subset:
            dist = line_dist(p1, p2, p)
            if dist > max_dist:
                max_dist = dist
                farthest_point = p
                
        hull.add(farthest_point)
        
        # The triangle (p1, p2, farthest_point) is now locked in.
        # ANY point inside this triangle is instantly discarded.
        # We only care about points that are "outside" the lines p1->farthest 
        # and farthest->p2.
        
        subset_1 = []
        subset_2 = []
        
        for p in subset:
            if p == farthest_point:
                continue
                
            # Is the point "outside" the line p1 -> farthest?
            if point_location(p1, farthest_point, p) == 1:
                subset_1.append(p)
                
            # Is the point "outside" the line farthest -> p2?
            elif point_location(farthest_point, p2, p) == 1:
                subset_2.append(p)
                
        # Recursively build the outer fences!
        build_hull(p1, farthest_point, subset_1)
        build_hull(farthest_point, p2, subset_2)

    # Fire the recursive engine on the top half and bottom half!
    build_hull(min_x_point, max_x_point, left_set)
    build_hull(max_x_point, min_x_point, right_set)
    
    return hull


def demonstrate_quickhull():
    section_header("Algorithm: Quickhull (Geometric D&C)")
    
    # A cluster of points. 
    # (0,3), (1,1), (2,2), (4,4), (0,0), (1,2), (3,1), (3,3)
    points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    
    print("Forest of Trees (Coordinates):")
    for p in points: print(f" {p}")
        
    print("\nExecuting Quickhull...")
    hull_points = quickhull(points)
    
    # Sort them by X just for clean output
    hull_sorted = sorted(list(hull_points), key=lambda p: p[0])
    
    print("\nTrees forming the Outer Fence (Convex Hull):")
    for p in hull_sorted:
        print(f" -> {p}")
        
    print("\nNotice how interior points like (1,1), (1,2) and (2,2) were pruned!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is this algorithm called the "Geometric Equivalent of Quick Sort"?
   Answer: In Quick Sort, we pick a Pivot, and partition the array into smaller/larger sets. In Quickhull, we pick a Line, and partition the points into "Left of line" and "Right of line" sets. Both algorithms discard the Pivot/Line from future calculations, and recursively attack the two smaller partitions. And just like Quick Sort, Quickhull is $O(N \\log N)$ on average, but can degrade to $O(N^2)$ in the absolute worst case!

2. What is the $O(N^2)$ worst-case scenario for Quickhull?
   Answer: If all the points in the dataset already perfectly form the outline of a circle (every single point is on the Convex Hull). When Quickhull tries to prune points inside the triangle, it will find exactly ZERO points to prune. It will have to painfully process every single point one by one on the outer boundary, destroying the $O(\\log N)$ recursion depth and flattening it to an $O(N)$ depth, yielding $O(N^2)$ time. 

3. How does the Cross Product `(p[1] - p1[1]) * (p2[0] - p1[0]) - ...` determine Left vs Right?
   Answer: This is a famous Linear Algebra trick (the 2D Vector Cross Product or Determinant). It calculates the signed area of the parallelogram formed by the three points. If the points form a "Left Turn" (counter-clockwise), the area is positive. If they form a "Right Turn" (clockwise), the area is negative. If they form a straight line, the area is exactly 0. It is a blazing-fast $O(1)$ calculation with no floating-point trigonometry required.
"""

if __name__ == "__main__":
    demonstrate_quickhull()
    print("\n[SUCCESS] Laboratory: Quickhull Completed.")
