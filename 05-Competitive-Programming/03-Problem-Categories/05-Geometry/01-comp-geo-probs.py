"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (COMPUTATIONAL GEOMETRY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are programming the navigation software for an autonomous drone.
# You have a 2D map with coordinates. The drone is at point A, and the target 
# is at point B. Suddenly, a massive polygonal no-fly zone (a polygon) appears.
# 
# How does the drone mathematically calculate if a specific GPS coordinate is 
# physically inside or outside the forbidden polygon?
# How do you calculate the tightest bounding box (Convex Hull) around a swarm 
# of enemy drones?
#
# You cannot use floating-point math (e.g., calculating slopes with division, 
# `y2 - y1 / x2 - x1`) because floating-point inaccuracies will cause catastrophic 
# rounding errors, and division by zero will crash your software if the line 
# is perfectly vertical.
#
# You must use Computational Geometry based entirely on the 2D Cross Product, 
# which relies strictly on Integer Multiplication, mathematically guaranteeing 
# 100% precision with zero crashes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Vector Mathematics (Dot Product & Cross Product).
# - Master the Orientation (CCW) test.
# - Implement the Monotone Chain algorithm for the Convex Hull.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CROSS PRODUCT (ORIENTATION / CCW)
# ==============================================================================
def cross_product(p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> int:
    """
    Calculates the 2D Cross Product of vectors (p1->p2) and (p1->p3).
    This mathematically determines the ORIENTATION of the 3 points.
    
    Returns:
    > 0 : Counter-Clockwise (Left Turn)
    < 0 : Clockwise (Right Turn)
    == 0: Collinear (The 3 points form a perfectly straight line)
    
    Notice there is NO division! No floating points! Only integer math!
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    # Vector A = p1 -> p2 = (x2 - x1, y2 - y1)
    # Vector B = p1 -> p3 = (x3 - x1, y3 - y1)
    # Cross Product = Ax * By - Ay * Bx
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

def demonstrate_orientation():
    section_header("The Cross Product (Orientation Test)")
    
    p1 = (0, 0)
    p2 = (4, 4)
    
    # Let's test three different third points
    left_point = (2, 5)   # Above the diagonal line
    right_point = (5, 2)  # Below the diagonal line
    straight_point = (8, 8) # Exactly on the line
    
    print(f"Line Segment: {p1} to {p2}")
    
    cp_left = cross_product(p1, p2, left_point)
    print(f"To reach {left_point}: Cross Product is {cp_left} -> {'Left Turn (CCW)' if cp_left > 0 else 'Right'}")
    
    cp_right = cross_product(p1, p2, right_point)
    print(f"To reach {right_point}: Cross Product is {cp_right} -> {'Right Turn (CW)' if cp_right < 0 else 'Left'}")
    
    cp_straight = cross_product(p1, p2, straight_point)
    print(f"To reach {straight_point}: Cross Product is {cp_straight} -> {'Collinear' if cp_straight == 0 else 'Turn'}")


# ==============================================================================
# 4. THE CONVEX HULL (MONOTONE CHAIN ALGORITHM)
# ==============================================================================
def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Finds the Convex Hull (the tightest outer polygon encompassing all points).
    Algorithm: Monotone Chain.
    Time Complexity: O(N log N) for sorting, O(N) for building the hull.
    Space Complexity: O(N)
    """
    # 1. Sort the points lexicographically (by X-coordinate, then by Y-coordinate).
    points = sorted(points)
    
    # A polygon requires at least 3 points.
    if len(points) <= 3:
        return points
        
    def build_half_hull(pts: list[tuple[int, int]]) -> list[tuple[int, int]]:
        hull = []
        for p in pts:
            # While the last 3 points in our Hull form a "Right Turn" or are "Collinear",
            # the middle point is mathematically INSIDE the polygon, making it 
            # useless for the OUTER boundary. We pop it!
            while len(hull) >= 2 and cross_product(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull
        
    # 2. Build the Lower Boundary
    lower = build_half_hull(points)
    
    # 3. Build the Upper Boundary (by reversing the points)
    upper = build_half_hull(points[::-1])
    
    # 4. Merge them!
    # The last point of the lower hull is the first point of the upper hull,
    # and vice versa, so we slice off the last point of both to prevent duplicates.
    return lower[:-1] + upper[:-1]

def demonstrate_convex_hull():
    section_header("Convex Hull (Monotone Chain)")
    
    points = [
        (0, 0), (0, 4), (4, 0), (4, 4), # 4 Outer Corners
        (1, 1), (2, 2), (3, 1), (2, 3)  # 4 Inner Points
    ]
    
    print("A swarm of 8 drones is located at:")
    print(points)
    
    hull = convex_hull(points)
    
    print("\nThe Convex Hull (The bounding polygon) consists of:")
    print(hull)
    print("Notice how the 4 inner points were mathematically discarded in O(N log N) time!")


def run_all_labs():
    demonstrate_orientation()
    demonstrate_convex_hull()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When checking if three points form a left turn or a right turn, why is the Cross Product vastly superior to calculating the geometric slopes (`m1 = y2-y1 / x2-x1`)?
   Answer: Two reasons. First, Division by Zero. If points A and B form a perfectly vertical line (sharing the same X coordinate), `x2 - x1` becomes 0, and the slope calculation immediately crashes the program with a `ZeroDivisionError`. Second, Floating Point Precision. Computers cannot perfectly store irrational fractions (like 1/3) in binary. If you use division, the resulting float is mathematically imprecise. When checking if a point is perfectly collinear on a line, `slope1 == slope2` will return `False` due to rounding errors deep in the decimals. The Cross Product equation `(x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)` uses ONLY Integer Subtraction and Integer Multiplication. It mathematically guarantees 100% precision, zero float rounding errors, and zero risk of division crashes.

2. In the Monotone Chain algorithm for the Convex Hull, why do we use `while len(hull) >= 2 and cross_product(hull[-2], hull[-1], p) <= 0: hull.pop()`?
   Answer: A Convex polygon means every interior angle is strictly less than 180 degrees. If you trace the perimeter of the polygon, you must constantly make "Left Turns" (Counter-Clockwise). If you ever make a "Right Turn", or continue perfectly straight, it means the middle vertex is physically caving inward, creating a concave dent. A Convex Hull cannot have concave dents! The `cross_product <= 0` mathematically detects a Right Turn or a straight line. If detected, we aggressively `pop()` the offending middle vertex out of the stack, deleting the dent, and re-evaluating the new angle until it forms a perfect Left Turn. 

3. How does the sorting step (`sorted(points)`) enable the Monotone Chain algorithm to run in $O(N)$ time after the sort?
   Answer: By sorting lexicographically (left-to-right on the X-axis), we mathematically guarantee that as we iterate through the list, we are strictly moving horizontally across the 2D plane. This geometry allows us to sweep across the bottom of the points to build the "Lower Hull", and sweep backwards across the top to build the "Upper Hull". Because every point is added to the stack exactly once, and popped from the stack at most once, the amortized cost of the `while` loop is $O(1)$ per point, resulting in a lightning-fast $O(N)$ sweep phase!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Computational Geometry Completed.")
