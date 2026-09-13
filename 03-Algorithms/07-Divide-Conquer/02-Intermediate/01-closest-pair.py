"""
# ==============================================================================
# LABORATORY: CLOSEST PAIR OF POINTS (COMPUTATIONAL GEOMETRY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building an Air Traffic Control radar system. You have 10,000 airplanes 
# in the sky, represented as (X, Y) coordinates. 
# You must instantly detect the TWO planes that are physically closest to each 
# other to prevent a collision.
#
# A naive algorithm calculates the distance between EVERY possible pair of planes.
# That requires O(N^2) time. For 10,000 planes, that's 100,000,000 calculations. 
# The radar frame will freeze. Planes will crash.
#
# We must use Divide and Conquer to solve this in O(N log N) time!
#
# 1. DIVIDE: Draw a vertical line perfectly down the middle of the sky.
# 2. CONQUER: Recursively find the closest pair strictly in the Left Half (d1), 
#    and strictly in the Right Half (d2). Let `d = min(d1, d2)`.
# 3. COMBINE (The Boundary Problem): 
#    What if the closest two planes are 1 millimeter apart, but one is in the 
#    Left Half, and the other is in the Right Half? 
#    We create a "Strip" around the vertical boundary of width `2d`.
#    We ONLY check planes inside this strip.
# 
# The Mathematical Miracle (Pigeonhole Principle):
# Inside that boundary strip, for any given plane, we only need to check a 
# MAXIMUM of 7 other planes! Because if 8 planes were packed that tightly, 
# their internal distances would be less than `d`, which violates our recursive 
# proof!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Computational Geometry Divide & Conquer.
# - Understand the O(N) Strip crossing validation.
# - Apply the Pigeonhole Principle to algorithm optimization.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIVIDE & CONQUER (CLOSEST PAIR O(N log^2 N))
# ==============================================================================
def calculate_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Standard Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def closest_pair_recursive(points_sorted_x: List[Tuple[int, int]]) -> float:
    """
    Time Complexity: O(N log N) per level, log N levels = O(N log^2 N).
    (Can be optimized to O(N log N) by pre-sorting Y).
    """
    n = len(points_sorted_x)
    
    # 1. BASE CASE (Brute Force for tiny subproblems)
    # If there are 3 or fewer points, it's faster to just check them manually.
    if n <= 3:
        min_dist = math.inf
        for i in range(n):
            for j in range(i + 1, n):
                dist = calculate_distance(points_sorted_x[i], points_sorted_x[j])
                min_dist = min(min_dist, dist)
        return min_dist
        
    # 2. DIVIDE (Split by X coordinate)
    mid = n // 2
    mid_point = points_sorted_x[mid]
    
    left_half = points_sorted_x[:mid]
    right_half = points_sorted_x[mid:]
    
    # 3. CONQUER (Recursive Calls)
    # Find the shortest distance purely on the left side, and purely on the right.
    dist_left = closest_pair_recursive(left_half)
    dist_right = closest_pair_recursive(right_half)
    
    # The current known absolute minimum distance!
    d = min(dist_left, dist_right)
    
    # 4. COMBINE (The Boundary Strip)
    # We must check if there is a pair ACROSS the middle line closer than `d`.
    # We filter out any points that are further than `d` horizontally from the 
    # vertical midline.
    strip = []
    for point in points_sorted_x:
        if abs(point[0] - mid_point[0]) < d:
            strip.append(point)
            
    # Sort the strip by their Y coordinates. (This is what makes it O(N log N) per level)
    strip.sort(key=lambda p: p[1])
    
    # Check the points in the strip!
    min_dist_strip = d
    for i in range(len(strip)):
        # THE MAGIC 7 TRICK:
        # We only need to check the next few points. Mathematically, the inner 
        # loop will run AT MOST 7 times before the Y-distance exceeds `d` and breaks!
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist_strip:
            dist = calculate_distance(strip[i], strip[j])
            min_dist_strip = min(min_dist_strip, dist)
            j += 1
            
    return min(d, min_dist_strip)


def closest_pair(points: List[Tuple[int, int]]) -> float:
    # Initial trigger function. Sorts by X once.
    points.sort(key=lambda p: p[0])
    return closest_pair_recursive(points)


def demonstrate_closest_pair():
    section_header("Algorithm: Closest Pair of Points (2D Plane)")
    
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    
    print("Radar Coordinates:")
    for p in points:
        print(f" Airplane at (X={p[0]}, Y={p[1]})")
        
    print("\nExecuting O(N log^2 N) Divide & Conquer...")
    min_dist = closest_pair(points)
    
    print(f"\nMinimum Distance Found: {min_dist:.4f}")
    
    # Let's verify with brute force
    brute_dist = math.inf
    p1_best, p2_best = None, None
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = calculate_distance(points[i], points[j])
            if dist < brute_dist:
                brute_dist = dist
                p1_best, p2_best = points[i], points[j]
                
    print(f"Brute Force Verification: {brute_dist:.4f} between {p1_best} and {p2_best}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the inner loop in the boundary strip run at most 7 times?
   Answer: This is proven by the Pigeonhole Principle. Consider a rectangle in the strip of width $2d$ and height $d$. We already proved recursively that NO two points on the same side can be closer than $d$. If you try to pack points into this rectangle such that they maintain a distance of at least $d$ from each other, geometry physically limits you to placing a maximum of 8 points! Therefore, any given point only needs to check the next 7 points in the Y-sorted array.

2. How can you optimize this from $O(N \\log^2 N)$ to strictly $O(N \\log N)$?
   Answer: The bottleneck is sorting the `strip` by Y-coordinates at every single level of recursion! Instead of doing `.sort(key=y)` inside the recursion, you can pass TWO globally pre-sorted arrays into the function (`points_sorted_x` and `points_sorted_y`). During the Divide step, you manually filter the Y-array into `left_y` and `right_y` in $O(N)$ time, maintaining the sort order. This removes the logarithmic sorting overhead from the recurrence relation.

3. Why can't we use a simple Grid/Hash Map to solve this in $O(N)$?
   Answer: You can! There is a Randomized Algorithm (using a Hash Map with a grid size of $d$) that solves Closest Pair in Expected $O(N)$ time. However, it requires a lot of bit-manipulation and spatial hashing. The Divide & Conquer approach is the mathematically pure, deterministic $O(N \\log N)$ standard taught in algorithm courses.
"""

if __name__ == "__main__":
    demonstrate_closest_pair()
    print("\n[SUCCESS] Laboratory: Closest Pair D&C Completed.")
