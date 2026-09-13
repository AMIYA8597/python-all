"""
# ==============================================================================
# LABORATORY: EXACT INTERSECTIONS & POINT-IN-POLYGON (RAY CASTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the first geometry lab, you learned how to check IF two lines intersect 
# using the Cross Product orientation (returning a boolean).
#
# But what if you are programming a physics engine and a bullet hits a wall? 
# You need to know exactly WHERE it hit! You need the exact (x, y) floating-point 
# coordinate of the intersection.
#
# We can find this by modeling the lines in General Form (Ax + By = C) and 
# solving the system of linear equations using Cramer's Rule (Determinants)! 
# This avoids the dreaded DivisionByZero slope errors.
#
# Application: Point-in-Polygon
# You are building a GPS geofencing application. You have a complex polygon 
# representing the city borders of Chicago. A user is standing at (Lat, Long). 
# Are they inside or outside the city?
#
# The legendary Ray Casting Algorithm solves this. You draw a horizontal "laser" 
# pointing strictly to the right from the user's location. You mathematically 
# count how many times the laser intersects the walls of the polygon.
# - If it crosses the walls an ODD number of times, they are INSIDE!
# - If it crosses an EVEN number of times, they are OUTSIDE!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Convert Coordinate lines to General Form (Ax + By = C).
# - Use Cramer's Rule to find exact intersection coordinates.
# - Implement the Ray Casting algorithm for complex polygons.
#
# ==============================================================================
"""

from typing import Tuple, List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Define a Point Type ---
Point = Tuple[float, float]
# -----------------------------------


# ==============================================================================
# 3. EXACT LINE INTERSECTION (CRAMER'S RULE)
# ==============================================================================
def get_intersection_coordinate(p1: Point, q1: Point, p2: Point, q2: Point) -> Optional[Point]:
    """
    Finds the exact floating point intersection coordinate of two infinite lines 
    (not just line segments, but the infinite lines passing through them).
    
    If the lines are perfectly parallel, returns None.
    """
    # 1. CONVERT TO GENERAL FORM: Ax + By = C
    # To find A, B, and C from two points (X1, Y1) and (X2, Y2):
    # A = Y2 - Y1
    # B = X1 - X2
    # C = A*X1 + B*Y1
    
    A1 = q1[1] - p1[1]
    B1 = p1[0] - q1[0]
    C1 = A1 * p1[0] + B1 * p1[1]
    
    A2 = q2[1] - p2[1]
    B2 = p2[0] - q2[0]
    C2 = A2 * p2[0] + B2 * p2[1]
    
    # 2. CRAMER'S RULE (Determinant calculation)
    # The determinant of the coefficient matrix:
    # | A1  B1 |
    # | A2  B2 |
    det = A1 * B2 - A2 * B1
    
    # If the determinant is 0, the lines are mathematically PARALLEL!
    # They will never intersect (or they are the exact same line).
    if det == 0:
        return None
        
    # 3. SOLVE FOR X AND Y
    # X = Det(C, B) / Det
    # Y = Det(A, C) / Det
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det
    
    return (x, y)


# ==============================================================================
# 4. POINT-IN-POLYGON (RAY CASTING ALGORITHM)
# ==============================================================================
# We re-use the boolean orientation logic from Lab 1 to check segment intersection!
def orientation(p1: Point, p2: Point, p3: Point) -> int:
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0])
    if val == 0: return 0
    return 1 if val > 0 else -1

def on_segment(p: Point, q: Point, r: Point) -> bool:
    if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
        return True
    return False

def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point) -> bool:
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    
    if (o1 != o2) and (o3 != o4): return True
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    return False


def is_inside_polygon(polygon: List[Point], target: Point) -> bool:
    """
    Determines if the `target` point lies strictly inside the given 2D polygon.
    Uses the Ray Casting Algorithm.
    Time Complexity: O(N) where N is the number of vertices in the polygon.
    """
    n = len(polygon)
    
    # A polygon mathematically requires at least 3 vertices (Triangle).
    if n < 3:
        return False
        
    # 1. CREATE THE INFINITE LASER
    # We create a point infinitely far to the right of our target!
    # Mathematically, "infinity" just needs to be larger than the max X coordinate 
    # of the polygon.
    extreme_right: Point = (1000000000, target[1])
    
    intersect_count = 0
    
    # 2. CHECK EVERY SINGLE WALL IN THE POLYGON
    for i in range(n):
        # The wall connects Vertex i to Vertex i+1
        wall_start = polygon[i]
        wall_end = polygon[(i + 1) % n]
        
        # Did our laser physically hit this wall?
        if do_intersect(wall_start, wall_end, target, extreme_right):
            
            # SPECIAL EDGE CASE: What if the target point physically lies exactly 
            # ON the wall border?
            # In most geofencing rules, standing on the border = Inside.
            if orientation(wall_start, target, wall_end) == 0:
                return on_segment(wall_start, target, wall_end)
                
            intersect_count += 1
            
    # 3. THE ODD/EVEN RULE
    # If the laser crossed an odd number of walls (1, 3, 5...), we are INSIDE!
    # If it crossed an even number (0, 2, 4...), we are OUTSIDE!
    return (intersect_count % 2 == 1)


def demonstrate_intersections():
    section_header("Algorithm: Exact Line Intersection (Cramer's Rule)")
    
    L1_start, L1_end = (0, 0), (10, 10) # Diagonal line /
    L2_start, L2_end = (0, 10), (10, 0) # Diagonal line \
    
    print(f"Line 1: {L1_start} to {L1_end}")
    print(f"Line 2: {L2_start} to {L2_end}")
    
    coord = get_intersection_coordinate(L1_start, L1_end, L2_start, L2_end)
    print(f"Exact intersection point: {coord}")
    
    section_header("Algorithm: Ray Casting (Point in Polygon)")
    
    # A standard 10x10 square
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    
    point_inside = (5, 5)
    point_outside = (20, 20)
    point_on_edge = (10, 5)
    
    print(f"Polygon Bounds: {square}")
    
    print(f"\nTarget {point_inside}: Inside? {is_inside_polygon(square, point_inside)}")
    print(f"Target {point_outside}: Inside? {is_inside_polygon(square, point_outside)}")
    print(f"Target {point_on_edge}: Inside? {is_inside_polygon(square, point_on_edge)}")
    
    print("\nImagine the Ray Casting for (5, 5).")
    print("A laser shoots to the right towards (Infinity, 5).")
    print("It pierces exactly ONE wall: The right border (10, 0) to (10, 10).")
    print("1 is an odd number. Therefore, it is inside!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Cramer's Rule prevent $DivisionByZero$ errors on vertical lines?
   Answer: The standard slope formula $m = \frac{Y_2 - Y_1}{X_2 - X_1}$ crashes if the line is vertical (denominator is 0). By converting the line to General Form $Ax + By = C$, the "slopes" are transformed into coefficients! A vertical line simply has $B = 0$. The Determinant calculation $\det = A_1 B_2 - A_2 B_1$ involves NO division whatsoever! Division is only executed at the absolute final step to calculate $X$ and $Y$, and the denominator is the Determinant itself. If the Determinant is 0, it means the lines are Parallel, which mathematically validates why division is impossible!

2. How does Ray Casting definitively prove a point is inside a polygon?
   Answer: Think of a polygon as a balloon. If you stand completely OUTSIDE the balloon and shoot a laser through it, the laser must pierce the front wall to enter, and pierce the back wall to exit. Total piercings: 2 (Even). It will ALWAYS be even. 
   If you are standing INSIDE the balloon, the laser only needs to pierce the back wall to exit. Total piercings: 1 (Odd). 
   No matter how complex, star-shaped, or jagged the polygon is, crossing a wall flips your state from Inside $\to$ Outside, or Outside $\to$ Inside. The odd/even parity is mathematically flawless.

3. Are there edge cases in Ray Casting?
   Answer: Yes! What if your laser perfectly hits a VERTEX of the polygon instead of the flat wall? Depending on how the loop executes, it might count the vertex twice (once for the wall ending there, once for the wall starting there), falsely flipping the odd/even count! In production-grade geometry engines, you must implement specific logic to handle vertex piercings, usually by considering a vertex intersection only if the adjacent walls cross the laser line vertically.
"""

if __name__ == "__main__":
    demonstrate_intersections()
    print("\n[SUCCESS] Laboratory: Exact Intersections & Ray Casting Completed.")
