"""
# ==============================================================================
# LABORATORY: CLOSEST PAIR OF POINTS (DIVIDE & CONQUER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Problem: You are designing an Air Traffic Control system. You have 100,000 
# airplanes flying in a 2D sector. You must instantly sound an alarm if ANY two 
# planes get dangerously close to each other.
#
# How do you find the two closest planes?
# - Naive Approach: Check Plane 1 against all 99,999 others. Then Plane 2... 
#   This takes O(N^2) time. 10 Billion operations. By the time your computer 
#   finishes calculating, the planes will have crashed.
#
# In 1975, Michael Shamos proved that this problem can be mathematically 
# solved in strict O(N log N) time using Divide and Conquer!
#
# The Architecture:
# 1. Sort all planes by their X-coordinate.
# 2. Draw a vertical line down the middle of the sky, splitting the planes 
#    into a Left Half and a Right Half.
# 3. Recursively find the closest pair in the Left Half (distance = dL), and 
#    the closest pair in the Right Half (distance = dR).
# 4. Let `d` = min(dL, dR). 
#    Is it possible that a plane in the Left Half and a plane in the Right Half 
#    are closer than `d`? Yes! But ONLY if they are both flying within a distance 
#    `d` of the vertical center line!
#
# The Magic Trick:
# We gather all planes in that narrow "Middle Strip" and sort them by Y-coordinate. 
# Do we have to check every plane in the strip against every other plane? 
# NO! Mathematical geometry proves that a plane only needs to check its next 
# 6 closest neighbors in the Y-axis. The 7th neighbor is mathematically guaranteed 
# to be further than `d`. 
# This drops the merge step to strict O(N), cementing the O(N log N) runtime!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Euclidean Distance without floating-point `sqrt` inaccuracies.
# - Implement the Recursive Divide and Conquer architecture.
# - Understand the Geometric "6-Neighbor" Proof in the middle strip.
#
# ==============================================================================
"""

import math
from typing import Tuple, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Define a Point Type ---
Point = Tuple[float, float]
# -----------------------------------


# ==============================================================================
# 3. DISTANCE ENGINE
# ==============================================================================
def distance_squared(p1: Point, p2: Point) -> float:
    """
    Calculates the Euclidean Distance SQUARED.
    We intentionally do NOT use math.sqrt() here!
    Square roots introduce microscopic floating point inaccuracies. Comparing 
    squared distances is mathematically identical to comparing real distances, 
    but 100% immune to precision loss.
    """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def brute_force_closest(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    """
    Standard O(N^2) brute force.
    Used exclusively as the Base Case for the recursion when N is very small (<= 3).
    """
    n = len(points)
    min_dist_sq = float('inf')
    best_pair = None
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance_squared(points[i], points[j])
            if dist < min_dist_sq:
                min_dist_sq = dist
                best_pair = (points[i], points[j])
                
    return min_dist_sq, best_pair


# ==============================================================================
# 4. DIVIDE AND CONQUER ENGINE (O(N LOG N))
# ==============================================================================
def closest_pair_recursive(points_sorted_x: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    """
    The recursive core of the algorithm. 
    Expects the points to ALREADY be sorted by X-coordinate!
    """
    n = len(points_sorted_x)
    
    # 1. BASE CASE (N <= 3)
    # If there are only 3 planes left in this sector, just check them all.
    if n <= 3:
        return brute_force_closest(points_sorted_x)
        
    # 2. DIVIDE
    # Draw a vertical line down the middle.
    mid = n // 2
    mid_point = points_sorted_x[mid]
    
    left_half = points_sorted_x[:mid]
    right_half = points_sorted_x[mid:]
    
    # Recursively conquer the halves!
    dist_l, pair_l = closest_pair_recursive(left_half)
    dist_r, pair_r = closest_pair_recursive(right_half)
    
    # 3. CONQUER (Find the minimum of the two isolated halves)
    if dist_l < dist_r:
        min_dist_sq = dist_l
        best_pair = pair_l
    else:
        min_dist_sq = dist_r
        best_pair = pair_r
        
    # 4. THE MIDDLE STRIP MERGE
    # What if the closest pair spans ACROSS the dividing line?
    # We only care about planes that are within `sqrt(min_dist_sq)` of the center line!
    # (We must calculate the true physical distance `d` for the X-axis coordinate boundary).
    min_dist = math.sqrt(min_dist_sq)
    
    strip = []
    for p in points_sorted_x:
        # If the plane's X-coordinate is within `min_dist` of the middle line...
        if abs(p[0] - mid_point[0]) < min_dist:
            strip.append(p)
            
    # Sort the planes in the strip by their Y-COORDINATE!
    # (In a hyper-optimized version, we would pre-sort by Y globally, but sorting 
    # here is acceptable since the strip is usually tiny).
    strip.sort(key=lambda p: p[1])
    
    # 5. THE MAGIC 6-NEIGHBOR LOOP
    # We check each plane against the planes above it in the strip.
    strip_len = len(strip)
    for i in range(strip_len):
        j = i + 1
        
        # We STOP checking mathematically as soon as the Y-distance between the 
        # two planes exceeds our current minimum distance `d`!
        # Because the strip is sorted by Y, we know for an absolute fact that 
        # ALL subsequent planes will be even further away!
        while j < strip_len and (strip[j][1] - strip[i][1]) < min_dist:
            dist = distance_squared(strip[i], strip[j])
            
            if dist < min_dist_sq:
                min_dist_sq = dist
                min_dist = math.sqrt(min_dist_sq) # Update the threshold!
                best_pair = (strip[i], strip[j])
                
            j += 1
            
    return min_dist_sq, best_pair


def find_closest_pair(points: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    """
    Wrapper function to handle the initial X-sorting.
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points!")
        
    # Crucial Step: Sort globally by X exactly ONCE to achieve O(N log N).
    points_sorted_x = sorted(points, key=lambda p: p[0])
    
    dist_sq, pair = closest_pair_recursive(points_sorted_x)
    
    # We return the TRUE physical distance at the very end
    return math.sqrt(dist_sq), pair


def demonstrate_closest_pair():
    section_header("Algorithm: Closest Pair of Points (O(N log N))")
    
    points = [
        (2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)
    ]
    
    print(f"Tracking {len(points)} airplanes.")
    print("Executing Divide and Conquer...")
    
    min_dist, best_pair = find_closest_pair(points)
    
    print(f"\nCRITICAL ALERT: Closest planes found!")
    print(f"Plane 1: {best_pair[0]}")
    print(f"Plane 2: {best_pair[1]}")
    print(f"Physical Distance: {min_dist:.4f} units")
    
    print("\nVerification:")
    print("Looking at the coordinates, (2,3) and (3,4) are right next to each other.")
    print("Distance: sqrt((3-2)^2 + (4-3)^2) = sqrt(1+1) = sqrt(2) = 1.4142. Perfect!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we intentionally NOT use `math.sqrt()` during the recursive search?
   Answer: Square root calculation is mathematically expensive and introduces floating-point truncation errors. If we are just comparing distances to see which is smaller, $A < B$ mathematically guarantees that $A^2 < B^2$ (for positive numbers). By exclusively passing and comparing the Squared Distance, we use $100\%$ pure integer math, guaranteeing maximum CPU speed and absolute immunity to precision loss! We only execute `sqrt()` at the absolute final wrapper return.

2. Why is the `while` loop in the middle strip guaranteed to be $O(N)$?
   Answer: The "6-Neighbor" Geometric Proof! We are analyzing a strip of width $2d$ (from $-d$ to $+d$ of the center line). We partitioned this area into squares of side length $d/2$. Mathematical geometry dictates that no more than 1 point can physically exist in a square of $d/2$ (because if 2 points existed in the same square, their distance would be LESS than $d$, meaning our recursive algorithm would have already caught them as the minimum in the Left or Right half!). Because of this spatial packing constraint, any point in the strip can have at maximum 6 other points within a radius of $d$. Therefore, the inner `while` loop mathematically can NEVER execute more than 6 times, meaning it runs in constant $O(1)$ time per point, making the strip merge strictly $O(N)$.

3. Where is this algorithm used in the real world?
   Answer: 
   - Air Traffic Control collision detection.
   - Boids/Flocking simulations in Video Games (finding the nearest neighbors to align movement).
   - Unsupervised Machine Learning (Agglomerative Hierarchical Clustering), where the closest two data clusters are continuously merged together.
"""

if __name__ == "__main__":
    demonstrate_closest_pair()
    print("\n[SUCCESS] Laboratory: Closest Pair of Points Completed.")
