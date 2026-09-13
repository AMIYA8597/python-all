"""
# ==============================================================================
# LABORATORY: COMPUTATIONAL GEOMETRY (SCIPY.SPATIAL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you are building a video game, a GPS navigation system, or an autonomous 
# drone, you are constantly solving Spatial Mathematics.
# 
# Questions like:
# - "What is the closest enemy to the player?" (Nearest Neighbor)
# - "What is the outer physical perimeter of this swarm of drones?" (Convex Hull)
# - "How do I divide this city into delivery zones based on the closest warehouse?" (Voronoi)
#
# Doing this manually requires brutal $O(N^2)$ distance calculations and complex 
# trigonometry. `scipy.spatial` provides heavily optimized $C$ implementations 
# of world-class computational geometry algorithms.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Query exact Nearest Neighbors in $O(\log N)$ time using KD-Trees.
# - Calculate the boundary of a point cloud using Convex Hulls.
# - Understand the duality of Delaunay Triangulations and Voronoi Diagrams.
#
# ==============================================================================
"""

import numpy as np
from scipy import spatial

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. K-DIMENSIONAL TREES (NEAREST NEIGHBORS)
# ==============================================================================
def demonstrate_kdtree():
    section_header("Spatial Indexing (KD-Trees)")
    
    print("Imagine you are Uber. You have 100,000 drivers in a city.")
    print("A user requests a ride. Finding the closest driver using brute force ")
    print("requires calculating the Haversine distance 100,000 times! (O(N)).")
    
    # Generate 100,000 random driver coordinates (X, Y)
    np.random.seed(42)
    drivers = np.random.rand(100_000, 2) * 1000 # 1000x1000 grid
    
    # 1. BUILD THE KD-TREE
    # A KD-Tree recursively slices the map in half (Left/Right, then Top/Bottom).
    # Building it takes O(N log N), but querying it is blazingly fast!
    tree = spatial.KDTree(drivers)
    print("KD-Tree successfully built in memory.")
    
    # 2. QUERY THE KD-TREE
    # User's location
    user_location = [500.0, 500.0]
    
    # Query for the K=3 closest drivers
    # The search traverses the tree in O(log N) time!
    distances, indices = tree.query(user_location, k=3)
    
    print(f"\nUser Location: {user_location}")
    print("Top 3 Closest Drivers Found instantly:")
    for i in range(3):
        idx = indices[i]
        dist = distances[i]
        print(f" - Driver #{idx:<6} | Distance: {dist:.2f} | Coords: {np.round(drivers[idx], 1)}")


# ==============================================================================
# 4. CONVEX HULLS
# ==============================================================================
def demonstrate_convex_hull():
    section_header("Convex Hulls (Finding Perimeters)")
    
    print("A Convex Hull is the smallest convex polygon that completely encloses ")
    print("a set of points. Imagine wrapping a rubber band around a bunch of pegs!")
    
    # 20 random points
    points = np.random.rand(20, 2)
    
    # Calculate the Hull
    # SciPy uses the highly optimized Qhull C library.
    hull = spatial.ConvexHull(points)
    
    print(f"\nTotal Points: {len(points)}")
    print(f"Points that form the outer perimeter (Vertices): {len(hull.vertices)}")
    
    print("\nPerimeter Vertex Indices (in counter-clockwise order):")
    print(hull.vertices)
    
    print(f"\nEnclosed Area  : {hull.volume:.4f} (For 2D, volume means Area!)")
    print(f"Perimeter Size : {hull.area:.4f} (For 2D, area means Perimeter length!)")


# ==============================================================================
# 5. DELAUNAY TRIANGULATION & VORONOI DIAGRAMS
# ==============================================================================
def demonstrate_voronoi_delaunay():
    section_header("Delaunay Triangulations & Voronoi Diagrams")
    
    # 10 critical locations (e.g., Hospitals in a city)
    hospitals = np.random.rand(10, 2)
    
    # 1. DELAUNAY TRIANGULATION
    # This algorithm connects all points with triangles such that NO point is 
    # inside the circumcircle of any triangle! 
    # This maximizes the minimum angles of the triangles (avoiding sliver triangles).
    # It is universally used in 3D Graphics to create polygon meshes!
    triangulation = spatial.Delaunay(hospitals)
    print("Delaunay Triangulation computed.")
    print(f"Total Triangles (Simplices) formed: {len(triangulation.simplices)}")
    
    # 2. VORONOI DIAGRAM
    # Voronoi is the mathematical dual of Delaunay!
    # It divides the map into "Regions" (Polygons). Any point inside Region X 
    # is mathematically guaranteed to be closer to Hospital X than ANY other hospital!
    # This is exactly how you draw voting districts or delivery zones.
    voronoi = spatial.Voronoi(hospitals)
    
    print("\nVoronoi Diagram computed.")
    print(f"Total Regions formed: {len(voronoi.regions)}")
    
    print("\nNotice: Delaunay connects the hospitals to each other. ")
    print("Voronoi draws borders halfway BETWEEN the hospitals!")


def run_all_labs():
    demonstrate_kdtree()
    demonstrate_convex_hull()
    demonstrate_voronoi_delaunay()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a KD-Tree $O(\log N)$ for Nearest Neighbor searches?
   Answer: A KD-Tree (K-Dimensional Tree) is a binary search tree mapped to physical space. The Root node splits the map vertically into Left/Right halves. The child nodes split those halves horizontally into Top/Bottom. If a user is at $(10, 10)$, the algorithm instantly ignores the entire Right half of the map, immediately eliminating 50% of the drivers! At every depth of the tree, it eliminates half the remaining drivers. Halving a dataset iteratively requires exactly $\log_2(N)$ steps.

2. Why are Convex Hulls used in Collision Detection for video games?
   Answer: Checking if two highly complex 3D models (like characters with 10,000 polygons) are physically intersecting requires millions of mathematical checks per frame, which lags the game. A Convex Hull creates a simplified, "shrink-wrapped" invisible perimeter around the character containing maybe 12 polygons. The game engine only checks if the simple Convex Hulls collide. If they do, THEN it performs the expensive exact checks. It is an extreme optimization technique.

3. What is the mathematical relationship between Delaunay and Voronoi?
   Answer: They are mathematical Duals! If you calculate the Delaunay Triangulation of a set of points, you get a mesh of triangles. If you find the geometric center (circumcenter) of every single triangle, and draw lines connecting adjacent centers, you perfectly draw the borders of the Voronoi Diagram! Every line segment in a Voronoi diagram is perfectly perpendicular to an edge in the Delaunay triangulation.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Spatial Geometry Completed.")
