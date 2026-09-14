"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (EXPERT GEOMETRY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given 100,000 points on a 2D map. You need to find the two points 
# that are mathematically CLOSEST to each other.
#
# Unlike finding the farthest points (where we can just use the Convex Hull), 
# the closest points could be anywhere—deep inside the swarm or on the edge.
# A double `for` loop takes $O(N^2)$ time (Time Limit Exceeded).
#
# You must use a brilliant Divide and Conquer algorithm that sorts the points, 
# physically slices the map in half, recursively finds the closest points in 
# the left and right halves, and then miraculously stitches the boundary back 
# together in exactly $O(N \log N)$ time!
#
# Second, how do we actually find the maximum diameter of a Convex Hull in O(N)?
# We use Rotating Calipers.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Divide & Conquer approach for Closest Pair of Points.
# - Understand the Boundary Strip geometric proof.
# - Understand Rotating Calipers for Convex Polygons.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CLOSEST PAIR OF POINTS (DIVIDE AND CONQUER)
# ==============================================================================
def distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def closest_pair(points: list[tuple[int, int]]) -> float:
    """
    Finds the shortest distance between any two points in the array.
    Time Complexity: O(N log N)
    """
    # Base Case: Brute force for very small subsets (<= 3 points)
    if len(points) <= 3:
        min_dist = float('inf')
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                min_dist = min(min_dist, distance(points[i], points[j]))
        return min_dist
        
    # 1. DIVIDE
    # Sort points by X-coordinate (assuming they aren't pre-sorted for this recursion)
    points.sort(key=lambda p: p[0])
    
    mid = len(points) // 2
    mid_point = points[mid]
    
    # 2. CONQUER
    # Recursively find the smallest distance strictly in the Left Half, 
    # and strictly in the Right Half!
    dl = closest_pair(points[:mid])
    dr = closest_pair(points[mid:])
    
    # The absolute smallest distance found so far:
    d = min(dl, dr)
    
    # 3. STITCHING THE BOUNDARY (The Magic)
    # What if the closest pair consists of one point on the Left, and one point 
    # on the Right, crossing the exact middle border?
    # We create a "Strip" array of all points whose X-distance to the mid_point 
    # is strictly less than `d`. If a point is further than `d` on the X-axis, 
    # it is mathematically impossible for it to be closer than `d` total!
    strip = [p for p in points if abs(p[0] - mid_point[0]) < d]
    
    # Sort the Strip by Y-coordinate!
    strip.sort(key=lambda p: p[1])
    
    min_dist = d
    
    # Geometric Proof: Inside this strip, we only ever need to check the next 
    # 7 points! (Because if you pack points into a d-by-2d rectangle, you can 
    # mathematically only fit 8 points before they become closer than `d`!).
    for i in range(len(strip)):
        j = i + 1
        # Only check points whose Y-distance is less than our current minimum!
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
            min_dist = min(min_dist, distance(strip[i], strip[j]))
            j += 1
            
    return min_dist

def demonstrate_closest_pair():
    section_header("Closest Pair of Points (Divide & Conquer)")
    
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    
    print(f"Points: {points}")
    print("\nExecuting O(N log N) recursive division...")
    
    ans = closest_pair(points)
    
    print(f"Shortest Distance: {ans:.4f}")
    print("Expected: 1.4142 (Distance between (2,3) and (3,4))")


# ==============================================================================
# 4. ROTATING CALIPERS (POLYGON DIAMETER)
# ==============================================================================
def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def polygon_diameter(hull: list[tuple[int, int]]) -> float:
    """
    Finds the maximum distance between any two points on a Convex Hull.
    Uses the Rotating Calipers method.
    Time Complexity: O(N) where N is points on the hull.
    """
    n = len(hull)
    if n <= 1: return 0.0
    if n == 2: return distance(hull[0], hull[1])
    
    # To avoid dealing with floats in loops, we check squared distances!
    def dist_sq(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
        
    max_dist_sq = 0
    
    # We maintain two pointers: `i` walks along the edges of the polygon.
    # `j` represents the vertex on the absolute OPPOSITE side of the polygon.
    j = 1
    
    for i in range(n):
        # Let's define the current edge of the polygon as `hull[i]` to `hull[i+1]`
        next_i = (i + 1) % n
        
        # We advance `j` around the perimeter as long as the triangle formed by 
        # (i, next_i, j+1) is mathematically LARGER (has more area) than the 
        # triangle formed by (i, next_i, j). 
        # The Area is exactly equal to 0.5 * absolute(Cross Product)!
        while True:
            next_j = (j + 1) % n
            
            # Area of triangle (i, next_i, j)
            area_j = abs(cross_product(hull[i], hull[next_i], hull[j]))
            
            # Area of triangle (i, next_i, next_j)
            area_next_j = abs(cross_product(hull[i], hull[next_i], hull[next_j]))
            
            # If advancing `j` makes the triangle smaller, it means `j` has passed 
            # the mathematical peak (the furthest opposing vertex). We stop advancing!
            if area_next_j <= area_j:
                break
            j = next_j
            
        # The diameter could be formed by `i` and `j`, or `next_i` and `j`
        max_dist_sq = max(max_dist_sq, dist_sq(hull[i], hull[j]), dist_sq(hull[next_i], hull[j]))
        
    return math.sqrt(max_dist_sq)

def demonstrate_rotating_calipers():
    section_header("Rotating Calipers (Polygon Diameter)")
    
    # A convex polygon
    hull = [(0, 0), (4, 0), (5, 3), (2, 5), (0, 4)]
    
    print(f"Convex Hull Points: {hull}")
    
    diameter = polygon_diameter(hull)
    print(f"\nMaximum Diameter: {diameter:.4f}")
    
    print("Notice how the pointers iterate through the perimeter exactly once, ")
    print("yielding a blazingly fast O(N) execution time!")


def run_all_labs():
    demonstrate_closest_pair()
    demonstrate_rotating_calipers()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the Closest Pair of Points algorithm, why is the inner loop mathematically guaranteed to execute at most 7 times, making the stitching phase $O(N)$?
   Answer: This is a famous geometric proof. In the "stitching" phase, we are checking points inside a narrow vertical strip of width $2d$. We only check points whose Y-coordinate distance is strictly less than $d$. This forms a bounding box of size $2d \times d$. We already mathematically proved during the recursive phase that any two points on the exact same side of the partition are at least distance $d$ apart. If you attempt to pack points into a $2d \times d$ rectangle such that *no two points on the same side are closer than $d$*, geometry strictly dictates you can only fit a maximum of 8 points! Therefore, the inner `while` loop checks a maximum of 7 neighbors before the Y-distance exceeds $d$, resulting in an $O(N)$ linear pass.

2. Explain the intuition behind the "Rotating Calipers" algorithm. How does it simulate rotating a physical clamp without using trigonometry or angles?
   Answer: Imagine placing a polygon inside a physical vise clamp. The two jaws of the clamp touch two parallel tangents of the shape. To find the diameter, you rotate the clamp 360 degrees and track the widest opening. To simulate this without using trigonometry (sines/cosines), we use the Area of a Triangle! A triangle's area is $\frac{1}{2} \times \text{Base} \times \text{Height}$. If we lock the Base to a specific edge of the polygon (`i` to `next_i`), the Height of the triangle is exactly the perpendicular distance to the opposite vertex (`j`). By using the Cross Product to calculate the Area, we simply advance `j` around the perimeter until the Area (and thus the Height) stops growing. This perfectly finds the furthest opposing vertex without calculating a single angle!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Expert Geometry Completed.")
