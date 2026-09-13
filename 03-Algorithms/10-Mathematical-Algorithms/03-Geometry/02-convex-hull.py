"""
# ==============================================================================
# LABORATORY: CONVEX HULL (MONOTONE CHAIN ALGORITHM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine a piece of wood with 1,000 nails hammered into it at random coordinates. 
# You take an elastic rubber band, stretch it completely open, and drop it around 
# the cluster of nails. It snaps tight.
# 
# The specific subset of nails that the rubber band touches forms a polygon. 
# This polygon is the Convex Hull. It mathematically bounds the entire set of points 
# within the smallest possible convex perimeter.
#
# Why is this useful?
# - Collision Detection: In video games, calculating collisions between complex 
#   character models is extremely slow. Engines first wrap the characters in a 
#   Convex Hull and check if the hulls intersect. (If the hulls don't touch, 
#   the complex models inside cannot possibly touch!).
# - Town Planning & Fencing: What is the shortest possible fence required to 
#   enclose all trees in an orchard?
# - Image Processing & AI object bounding boxes.
#
# Algorithms:
# 1. Jarvis March (Gift Wrapping): $O(N \times H)$ (where $H$ is the number of 
#    points actually on the hull). Similar to Selection Sort. Too slow if $H$ is large.
# 2. Graham Scan: $O(N \log N)$. Sorts points by Polar Angle using trigonometry. 
#    Very prone to floating point errors.
# 3. Monotone Chain (Andrew's Algorithm): $O(N \log N)$. The absolute gold standard. 
#    Sorts points normally by X-coordinate. It builds the "Upper Half" and "Lower Half" 
#    of the hull independently using the Cross Product! No trigonometry required!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the "Rubber Band" geometry analogy.
# - Re-use the Cross Product to enforce "Right Turns".
# - Implement Andrew's Monotone Chain Algorithm $O(N \log N)$.
#
# ==============================================================================
"""

from typing import Tuple, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Define a Point Type ---
Point = Tuple[int, int]
# -----------------------------------


# ==============================================================================
# 3. MONOTONE CHAIN ENGINE (ANDREW'S ALGORITHM)
# ==============================================================================
def cross_product(o: Point, a: Point, b: Point) -> int:
    """
    Returns the 2D cross product of OA and OB vectors.
    Math: (A_x - O_x) * (B_y - O_y) - (A_y - O_y) * (B_x - O_x)
    
    A positive cross product means O -> A -> B is a COUNTER-CLOCKWISE turn (Left).
    A negative cross product means O -> A -> B is a CLOCKWISE turn (Right).
    Zero means they are perfectly collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull_monotone_chain(points: List[Point]) -> List[Point]:
    """
    Builds the Convex Hull in O(N log N) time.
    Returns the points forming the perimeter of the hull in Counter-Clockwise order.
    """
    # 1. BASE CASES & SORTING
    # A hull requires at least 3 points to form a polygon!
    if len(points) <= 3:
        return points
        
    # Sort the points lexicographically (Primary by X-coordinate, Secondary by Y-coordinate).
    # This naturally sequences the points from left to right across the 2D plane!
    # Python's `.sort()` natively sorts tuples exactly like this.
    points = sorted(points)
    
    # 2. BUILD THE LOWER HULL
    # We walk from left to right, building the "bottom" curve of the rubber band.
    lower_hull = []
    for p in points:
        # The Monotone Chain Rule:
        # The rubber band must ALWAYS curve in the same direction!
        # If we take a "Right Turn" (Clockwise), it means our rubber band just 
        # caved INWARDS. This violates the property of convexity!
        # We must pop the offending points off the stack until we restore a Left Turn!
        
        # While the stack has at least 2 points AND the new point `p` does NOT 
        # make a Counter-Clockwise (Left) turn with the last two points...
        while len(lower_hull) >= 2 and cross_product(lower_hull[-2], lower_hull[-1], p) <= 0:
            lower_hull.pop() # Rip the invalid nail out!
            
        lower_hull.append(p)
        
    # 3. BUILD THE UPPER HULL
    # We walk BACKWARDS from right to left, building the "top" curve.
    upper_hull = []
    for p in reversed(points):
        while len(upper_hull) >= 2 and cross_product(upper_hull[-2], upper_hull[-1], p) <= 0:
            upper_hull.pop()
            
        upper_hull.append(p)
        
    # 4. GLUE THEM TOGETHER
    # Both hulls include the extreme left and right endpoints!
    # For example, `lower_hull` ends at the far-right point, and `upper_hull` 
    # begins at that exact same far-right point.
    # We slice off the last point `[:-1]` from both arrays to prevent duplicating 
    # the anchors, then combine them!
    
    return lower_hull[:-1] + upper_hull[:-1]


def demonstrate_convex_hull():
    section_header("Algorithm: Monotone Chain Convex Hull")
    
    # A cluster of 8 points
    points = [
        (0, 3), (1, 1), (2, 2), (4, 4),
        (0, 0), (1, 2), (3, 1), (3, 3)
    ]
    
    print("Initial Cluster of 2D Points:")
    print(points)
    
    hull = convex_hull_monotone_chain(points)
    
    print("\nCalculated Convex Hull Perimeter (Counter-Clockwise):")
    for pt in hull:
        print(f" -> {pt}")
        
    print("\nVerification:")
    print("Notice how inner points like (1, 1), (1, 2), and (2, 2) were entirely")
    print("skipped! They were swallowed inside the rubber band.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Andrew's Monotone Chain sort by X-coordinate instead of Polar Angle?
   Answer: Graham Scan sorts by Polar Angle using trigonometric functions like `atan2`. Calculating floating-point arcsines is mathematically expensive, slow, and highly prone to rounding errors (two points might evaluate to the same angle due to precision loss). Sorting by strict Integer X/Y coordinates is blindingly fast and 100% mathematically stable. By splitting the logic into an Upper and Lower sequence, Andrew's algorithm perfectly simulates the angular wrap-around without ever using a single trigonometric function.

2. Why do we `pop()` points off the stack when the Cross Product $\le 0$?
   Answer: The stack represents the current perimeter of the rubber band. A Cross Product $\le 0$ means the last three points form a Clockwise turn (or a flat line). If the perimeter turns clockwise, it means the boundary just dented INWARD towards the center of the shape! A Convex Polygon is mathematically defined as a shape with NO inward dents (all internal angles $< 180^{\circ}$). To fix the dent, we literally rip the offending nail (the middle point) out of the board by popping it, allowing the rubber band to snap tightly against the outer boundary.

3. Why is the time complexity $O(N \log N)$?
   Answer: The Cross Product evaluation and Stack `push/pop` operations run in strictly amortized $O(N)$ time. Why? Because every single point in the dataset can be pushed onto the stack exactly once, and popped off the stack at most once. $2N$ operations is mathematically $O(N)$. Therefore, the absolute bottleneck of the entire algorithm is the very first step: sorting the $N$ points lexicographically. The sorting step dominates at $O(N \log N)$.
"""

if __name__ == "__main__":
    demonstrate_convex_hull()
    print("\n[SUCCESS] Laboratory: Convex Hull Completed.")
