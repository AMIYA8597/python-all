"""
# ==============================================================================
# LABORATORY: COMPUTATIONAL GEOMETRY (CROSS PRODUCT & INTERSECTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a collision detection engine for a video game. You have two 
# Line Segments (a laser beam and a wall). Do they intersect?
#
# The naive approach: Use $y = mx + b$ algebra to find the intersection point, 
# and then check if the point lies on both segments. 
# Problem: What if the line is perfectly vertical? The slope $m$ is infinity. 
# Your program will instantly crash with a DivisionByZero error. Floating point 
# inaccuracies will also cause "near misses" to incorrectly register as hits.
#
# Computational Geometry completely abandons high school algebra slopes!
# Instead, we use the Vector Cross Product.
#
# The Cross Product provides one magical piece of information: ORIENTATION.
# If I walk from Point A to Point B, and then to Point C... did I turn LEFT, 
# did I turn RIGHT, or did I walk perfectly STRAIGHT?
#
# This single $O(1)$ multiplication operation solves almost every 2D geometry 
# problem in computer science without EVER using division or floating point math!
# - Line Intersection? Check if the endpoints of Line 1 straddle Line 2 using Orientation!
# - Polygon Area? The Cross Product is exactly twice the area of a triangle!
# - Convex Hull? Sort points and only accept "Right Turns"!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Vector Orientation via the Cross Product.
# - Implement robust $O(1)$ Line Segment Intersection (immune to vertical slopes).
# - Calculate the area of any polygon using the Shoelace Formula.
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
# 3. THE CROSS PRODUCT ENGINE (ORIENTATION)
# ==============================================================================
def orientation(p1: Point, p2: Point, p3: Point) -> int:
    """
    Returns the Orientation of the ordered triplet (p1, p2, p3).
    Math: Cross Product of vectors (p2-p1) and (p3-p2).
    
    Returns:
       0 : Collinear (The points form a straight line)
       1 : Clockwise (Right Turn)
      -1 : Counter-Clockwise (Left Turn)
    """
    # Cross Product Formula: (y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0])
    
    if val == 0: return 0
    return 1 if val > 0 else -1


def on_segment(p: Point, q: Point, r: Point) -> bool:
    """
    Given three COLLINEAR points p, q, and r, this checks if point `q` lies 
    physically on the line segment bounded by `p` and `r`.
    """
    # Check bounding box constraints!
    if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
        return True
    return False


# ==============================================================================
# 4. ROBUST LINE INTERSECTION
# ==============================================================================
def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    """
    Checks if Line Segment 1 (p1-q1) intersects Line Segment 2 (p2-q2).
    Completely immune to vertical slopes and floating point errors!
    """
    # 1. Calculate the orientations required for the General Case
    # Does Line 2 straddle Line 1?
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    
    # Does Line 1 straddle Line 2?
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    # GENERAL CASE: 
    # If p2 and q2 are on OPPOSITE sides of Line 1, AND p1 and q1 are on 
    # OPPOSITE sides of Line 2, they mathematically must intersect!
    if (o1 != o2) and (o3 != o4):
        return True
        
    # SPECIAL CASES (Collinear / Touching)
    # What if the endpoints physically touch the other line?
    
    # p1, q1, p2 are collinear, and p2 lies on segment p1-q1
    if o1 == 0 and on_segment(p1, p2, q1): return True
    
    # p1, q1, q2 are collinear, and q2 lies on segment p1-q1
    if o2 == 0 and on_segment(p1, q2, q1): return True
    
    # p2, q2, p1 are collinear, and p1 lies on segment p2-q2
    if o3 == 0 and on_segment(p2, p1, q2): return True
    
    # p2, q2, q1 are collinear, and q1 lies on segment p2-q2
    if o4 == 0 and on_segment(p2, q1, q2): return True
    
    return False


# ==============================================================================
# 5. THE SHOELACE FORMULA (POLYGON AREA)
# ==============================================================================
def polygon_area(points: List[Point]) -> float:
    """
    Calculates the exact area of ANY simple polygon (convex or concave).
    Uses the Shoelace Formula (which is derived directly from the Cross Product!).
    """
    n = len(points)
    area = 0.0
    
    for i in range(n):
        # We take the cross product of the current point and the NEXT point.
        # We use modulo `n` to perfectly wrap the final point back to the first point!
        j = (i + 1) % n
        
        # Shoelace math: (x_i * y_{i+1}) - (y_i * x_{i+1})
        area += (points[i][0] * points[j][1]) - (points[i][1] * points[j][0])
        
    # The total sum of cross products is EXACTLY twice the area of the polygon.
    # We take the absolute value (in case the points were ordered clockwise) and halve it.
    return abs(area) / 2.0


def demonstrate_geometry():
    section_header("Algorithm: Cross Product Orientation")
    
    p1 = (0, 0)
    p2 = (4, 4)
    p3 = (1, 2)
    print(f"Path: {p1} -> {p2} -> {p3}")
    o = orientation(p1, p2, p3)
    
    if o == 0: print("Result: Collinear (Straight)")
    elif o == 1: print("Result: Clockwise (Right Turn)")
    else: print("Result: Counter-Clockwise (Left Turn)")
    
    section_header("Algorithm: Line Intersection")
    
    # A standard "X" intersection
    seg1_p, seg1_q = (1, 1), (10, 1)
    seg2_p, seg2_q = (1, 2), (10, 2) # Parallel, won't intersect
    
    print(f"Segment 1: {seg1_p} to {seg1_q}")
    print(f"Segment 2: {seg2_p} to {seg2_q}")
    print(f"Do they intersect? {do_intersect(seg1_p, seg1_q, seg2_p, seg2_q)}")
    
    seg3_p, seg3_q = (5, 0), (5, 5) # Vertical line crossing Segment 1!
    print(f"\nSegment 1: {seg1_p} to {seg1_q}")
    print(f"Segment 3 (Vertical): {seg3_p} to {seg3_q}")
    print(f"Do they intersect? {do_intersect(seg1_p, seg1_q, seg3_p, seg3_q)}")
    
    section_header("Algorithm: Shoelace Formula (Area)")
    
    # A standard 2x2 Square (Area should be 4)
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    print(f"Polygon Points: {square}")
    print(f"Calculated Area: {polygon_area(square)}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Cross Product mathematically superior to $y = mx + b$ slope algebra?
   Answer: Slope algebra $m = (y_2 - y_1) / (x_2 - x_1)$ fundamentally requires division. In computing, division is dangerous. If the line is perfectly vertical, $x_2 - x_1 = 0$, triggering a fatal `DivisionByZero` crash. Furthermore, floating point division introduces micro-inaccuracies. The Cross Product $(y_2 - y_1) \times (x_3 - x_2) - (y_3 - y_2) \times (x_2 - x_1)$ uses ONLY integer multiplication and subtraction. It is 100% mathematically stable, never crashes on vertical lines, and never loses precision.

2. How does checking "straddling" prove intersection?
   Answer: Imagine a river (Line 1). You have two cities (p2 and q2) forming Line 2. If City A is on the North bank (Left turn from the river) and City B is on the South bank (Right turn from the river), then the road connecting them MUST cross the river! By verifying that the endpoints of Line 2 possess opposite Orientations relative to Line 1, AND vice versa, we perfectly mathematically prove intersection without ever physically calculating the exact coordinate of the crash.

3. Why is it called the "Shoelace" formula?
   Answer: If you write the $X$ coordinates in a vertical column, and the $Y$ coordinates in a vertical column next to it, the math requires you to multiply $X_1 \times Y_2$, then $Y_1 \times X_2$. When you draw lines connecting these terms on paper, they criss-cross repeatedly all the way down the columns, perfectly resembling the physical laces of a shoe!
"""

if __name__ == "__main__":
    demonstrate_geometry()
    print("\n[SUCCESS] Laboratory: Computational Geometry Completed.")
