"""
# ==============================================================================
# LABORATORY: ADVANCED POLYGONS (PICK'S THEOREM & CENTROIDS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Pick's Theorem:
# In 1899, Georg Alexander Pick discovered one of the most beautiful formulas 
# in all of integer geometry. 
# 
# Suppose you draw a polygon on a piece of graph paper where every vertex is 
# exactly on a grid intersection (integer coordinates). 
# You want to know the Area of the polygon.
# 
# You COULD use the Shoelace Formula. But Pick's Theorem states you can calculate 
# the EXACT area just by counting dots!
# Formula: Area = I + (B / 2) - 1
# - I: The number of grid points strictly INSIDE the polygon.
# - B: The number of grid points exactly ON THE BOUNDARY of the polygon.
#
# This theorem is heavily tested in competitive programming because problems 
# will give you the Area (via Shoelace) and B, and ask you to calculate I!
# 
# Polygon Centroid (Center of Mass):
# You are building a 2D physics engine. A polygonal asteroid is floating in space. 
# Gravity must pull it from its absolute Center of Mass. Where is that point?
# You cannot just average the X and Y coordinates! (That gives the geometric 
# center of the vertices, which is heavily biased if many vertices are clustered 
# on one side).
# 
# The True Centroid is calculated using the Cross Product! You break the polygon 
# into triangles, find the centroid of each triangle, and compute a weighted 
# average based on the Area of each triangle!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand and apply Pick's Theorem.
# - Use GCD to calculate Boundary points (B).
# - Calculate the True Centroid of a polygon.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Define a Point Type ---
Point = Tuple[float, float]
# -----------------------------------


# ==============================================================================
# 3. PICK'S THEOREM ENGINE
# ==============================================================================
def count_boundary_points(p1: Point, p2: Point) -> int:
    """
    How many integer grid points lie EXACTLY on the line segment between P1 and P2?
    Math: It is exactly the Greatest Common Divisor (GCD) of the X-distance and 
    Y-distance!
    """
    dx = abs(int(p1[0] - p2[0]))
    dy = abs(int(p1[1] - p2[1]))
    
    # We subtract 1 because we don't want to double-count the endpoints when 
    # we loop around the entire polygon!
    return math.gcd(dx, dy)

def calculate_interior_points(polygon: List[Point]) -> int:
    """
    Calculates `I` (Interior Points) using Pick's Theorem and the Shoelace Formula.
    Pick's Formula: Area = I + (B / 2) - 1
    Rearranged: I = Area - (B / 2) + 1
    """
    n = len(polygon)
    
    # 1. SHOELACE FORMULA (To find exact Area)
    area2 = 0 # We use 2*Area to avoid floating point division
    boundary_count = 0
    
    for i in range(n):
        j = (i + 1) % n
        
        # Cross product sum for Shoelace Area
        area2 += (polygon[i][0] * polygon[j][1]) - (polygon[i][1] * polygon[j][0])
        
        # GCD to count Boundary points
        boundary_count += count_boundary_points(polygon[i], polygon[j])
        
    area = abs(area2) / 2.0
    
    # 2. PICK'S THEOREM MATH
    # I = Area - B/2 + 1
    interior_points = area - (boundary_count / 2.0) + 1
    
    return int(interior_points)


# ==============================================================================
# 4. POLYGON CENTROID (CENTER OF MASS)
# ==============================================================================
def calculate_centroid(polygon: List[Point]) -> Point:
    """
    Calculates the True Center of Mass of a polygon using Cross Products.
    Assumes the polygon is non-self-intersecting.
    """
    n = len(polygon)
    cx = 0.0
    cy = 0.0
    area_sum = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        
        p1 = polygon[i]
        p2 = polygon[j]
        
        # The Cross Product of the current triangle slice!
        # (Technically, this is twice the signed area of the triangle formed by 
        # the origin (0,0), P1, and P2).
        cross_val = (p1[0] * p2[1]) - (p1[1] * p2[0])
        
        # Add to the total area sum
        area_sum += cross_val
        
        # Weighted accumulation of the X and Y coordinates
        cx += (p1[0] + p2[0]) * cross_val
        cy += (p1[1] + p2[1]) * cross_val
        
    # The final total area is area_sum / 2
    # The true centroid divides the weighted accumulation by (6 * Area)
    # (Since area_sum is already 2*Area, we divide by 3 * area_sum).
    
    if area_sum == 0:
        return (0.0, 0.0) # Degenerate polygon (flat line)
        
    cx /= (3.0 * area_sum)
    cy /= (3.0 * area_sum)
    
    return (cx, cy)


def demonstrate_advanced_polygons():
    section_header("Algorithm: Pick's Theorem (Integer Geometry)")
    
    # A massive triangle on a coordinate grid
    triangle = [(0, 0), (10, 0), (0, 10)]
    
    print(f"Polygon Grid Coordinates: {triangle}")
    
    interior = calculate_interior_points(triangle)
    print(f"How many dots are STRICTLY INSIDE this triangle? -> {interior}")
    
    print("\nVerification via Area:")
    # Base=10, Height=10. Area = 50.
    # Boundary points:
    # (0,0) to (10,0) -> 10 points
    # (0,0) to (0,10) -> 10 points
    # (10,0) to (0,10) -> GCD(10, 10) = 10 points
    # Total Boundary = 30.
    # Pick's Theorem: Area = I + B/2 - 1 -> 50 = 36 + 15 - 1 -> 50 = 50! Perfect!
    
    section_header("Algorithm: True Polygon Centroid")
    
    # Let's test a shape heavily biased to one side (L-Shape)
    l_shape = [
        (0, 0), (4, 0), (4, 1), 
        (1, 1), (1, 4), (0, 4)
    ]
    
    print(f"L-Shape Coordinates: {l_shape}")
    
    centroid = calculate_centroid(l_shape)
    print(f"Calculated Center of Mass: {centroid}")
    
    print("\nObservation:")
    print("If we just averaged the X and Y vertices, the center would be (1.66, 1.66).")
    print(f"The True Centroid is {centroid}. It shifted heavily towards the massive")
    print("corner cluster to correctly balance the physical weight of the shape!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `math.gcd(dx, dy)` perfectly calculate the number of boundary dots?
   Answer: Imagine a line segment from $(0, 0)$ to $(15, 10)$. The slope is $10/15$, which reduces to $2/3$. This mathematically proves that for every $3$ steps right, the line goes $2$ steps up, landing PERFECTLY on an integer grid intersection! How many times does this $3 \times 2$ "staircase" repeat over the $15 \times 10$ distance? Exactly 5 times! What is $\text{GCD}(15, 10)$? It is 5! The GCD extracts the exact mathematical frequency of the reduced slope.

2. Why do we divide by $(3 \times \text{area\_sum})$ when calculating the Centroid?
   Answer: Physics! The center of mass of a single Triangle is located exactly at the average of its three vertices: $(X_1 + X_2 + X_3) / 3$. 
   Our algorithm loops through the polygon, creating triangles anchored at the Origin $(0,0)$. 
   The centroid of one of these slice-triangles is $(0 + X_1 + X_2) / 3$. 
   We weight this centroid by the Area of the slice, which is $(X_1 \times Y_2 - Y_1 \times X_2) / 2$. 
   Because both formulas have denominators ($/3$ and $/2$), they multiply together to form a denominator of $/6$. Since `area_sum` is already $2 \times \text{Area}$, we divide the final accumulated value by $(3 \times \text{area\_sum})$ to mathematically satisfy the $/6$ denominator requirement!

3. Where is Pick's Theorem used in Computer Science?
   Answer: It is frequently used in Computer Graphics and Rasterization. When rendering a 3D polygon onto a 2D pixel grid (like a monitor screen), the engine needs to know exactly how many pixels lie strictly inside the polygon to execute shaders. Pick's Theorem mathematically computes this pixel count instantly without physically iterating through a massive 2D bounding-box array.
"""

if __name__ == "__main__":
    demonstrate_advanced_polygons()
    print("\n[SUCCESS] Laboratory: Advanced Polygons Completed.")
