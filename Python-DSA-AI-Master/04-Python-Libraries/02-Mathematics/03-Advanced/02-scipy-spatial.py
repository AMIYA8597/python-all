"""
Module: scipy.spatial Masterclass
Description: A textbook-grade interactive lesson on the `scipy.spatial` module.

===========================================================================
THEORY & MATHEMATICAL BACKGROUND: scipy.spatial
===========================================================================
The `scipy.spatial` module provides a comprehensive suite of algorithms for 
spatial data structures and operations. It allows you to analyze data points 
in n-dimensional space. The major components include:

1. Distance Computations (`scipy.spatial.distance`):
   - Computes distances between collections of points.
   - Core functions: `pdist` (pairwise distances), `cdist` (distances between 
     two collections), and `squareform` (converts between vector and matrix 
     forms of distance matrices).
   - Time Complexity: O(N^2 * D) for N points in D dimensions. Space: O(N^2).

2. Spatial Data Structures (`KDTree` and `cKDTree`):
   - A KD-Tree (K-Dimensional Tree) is a space-partitioning data structure 
     useful for organizing points in a k-dimensional space.
   - It allows for extremely fast nearest-neighbor queries.
   - Construction Time: O(N log N). Space: O(N).
   - Query Time (Nearest Neighbor): O(log N) on average, O(N) worst case (in high dimensions).

3. Computational Geometry (Convex Hull, Delaunay, Voronoi):
   - Convex Hull: The smallest convex shape enclosing a set of points.
     - Algorithm: Quickhull. Time Complexity: O(N log N) for 2D/3D.
   - Delaunay Triangulation: Triangulates a set of points such that no point 
     is strictly inside the circumcircle of any triangle.
     - Time Complexity: O(N log N) in 2D.
   - Voronoi Diagrams: Partitions space into regions based on distance to 
     a specified set of points. Dual graph of Delaunay triangulation.
     - Time Complexity: O(N log N) in 2D.

===========================================================================
REAL-WORLD APPLICATIONS:
===========================================================================
- Machine Learning (K-Nearest Neighbors, Clustering)
- Geographic Information Systems (GIS) - nearest facilities, bounding boxes.
- Computer Graphics and Physics Engines (collision detection, mesh generation).
- Bioinformatics (protein folding, molecular similarity).

This lesson explores these concepts interactively, robustly handling edge 
cases and demonstrating best practices for high-performance computing.
"""

import time
import math
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import scipy.spatial as spatial
from scipy.spatial import distance
import warnings


def demo_distance_metrics() -> None:
    """
    Demonstrates computing various distance metrics using `pdist` and `cdist`.
    
    Why pdist and cdist?
    - `pdist` calculates all unique pairwise distances between points in an N x D array.
      It returns a condensed distance matrix (1D array) of size N*(N-1)/2, saving space.
    - `cdist` calculates distances between each pair from two collections.
    """
    print("=" * 60)
    print("1. SPATIAL DISTANCE METRICS (pdist, cdist, squareform)")
    print("=" * 60)

    # Consider 4 points in a 2-dimensional space (e.g., coordinates on a map)
    # Shape: (4, 2)
    points_A = np.array([
        [0, 0],
        [3, 4],
        [6, 8],
        [3, 0]
    ], dtype=np.float64)

    print("Points Array A:")
    print(points_A)
    print()

    # 1.1 Pairwise Distances (pdist)
    # Using Euclidean distance (straight-line distance)
    # Time Complexity: O(N^2 * D), where N is number of points, D is dimensions.
    condensed_euclidean = distance.pdist(points_A, metric='euclidean')
    
    print("Condensed Pairwise Euclidean Distances (1D Array):")
    print(np.round(condensed_euclidean, 2))
    print(f"Shape of condensed array: {condensed_euclidean.shape} (N*(N-1)/2 elements)\n")

    # The condensed matrix is often hard to read. We convert it to a symmetric square matrix.
    # squareform toggles between the condensed and square formats.
    square_euclidean = distance.squareform(condensed_euclidean)
    print("Squareform Distance Matrix (Symmetric N x N):")
    print(np.round(square_euclidean, 2))
    print()

    # 1.2 Distances between two different sets of points (cdist)
    points_B = np.array([
        [0, 4],
        [6, 0]
    ], dtype=np.float64)

    # Calculate Manhattan distance (City Block distance) between points_A and points_B
    # Distance between (x1, y1) and (x2, y2) = |x1 - x2| + |y1 - y2|
    dist_ab_manhattan = distance.cdist(points_A, points_B, metric='cityblock')
    
    print("Manhattan Distances between A (4x2) and B (2x2) -> Result (4x2):")
    print(dist_ab_manhattan)
    print("Interpretation: Row `i`, Column `j` represents distance from A[i] to B[j]\n")


def demo_kdtree_for_nearest_neighbors() -> None:
    """
    Demonstrates KDTree (and cKDTree, the C-optimized version) for rapid 
    spatial queries like Nearest Neighbor search and Range Queries.
    
    Why KD-Trees?
    If you need to find the closest point to a query out of millions of points,
    calculating all distances takes O(N). A KDTree pre-processes the points in
    O(N log N) time, reducing query time to O(log N).
    """
    print("=" * 60)
    print("2. FAST SPATIAL QUERIES WITH KD-TREE")
    print("=" * 60)

    # Generate 100,000 random 3D points
    np.random.seed(42)
    N_points = 100_000
    points = np.random.rand(N_points, 3) * 100.0  # Points in a 100x100x100 cube

    # Build the KD-Tree (We use cKDTree for maximum performance)
    print(f"Building KDTree for {N_points} points in 3D...")
    start_build = time.time()
    # leafsize controls the number of points at which the tree switches to brute-force.
    # Default is 16, which is generally optimal.
    tree = spatial.cKDTree(points, leafsize=16)
    build_time = time.time() - start_build
    print(f"KDTree built in {build_time:.4f} seconds.\n")

    # 2.1 Single Nearest Neighbor Query
    query_point = np.array([50.0, 50.0, 50.0])
    
    start_query = time.time()
    # k=1 means we want the 1 nearest neighbor
    distance_nn, index_nn = tree.query(query_point, k=1)
    query_time = time.time() - start_query

    print("--- Nearest Neighbor Search ---")
    print(f"Query Point: {query_point}")
    print(f"Nearest Neighbor (Index {index_nn}): {points[index_nn]}")
    print(f"Distance: {distance_nn:.4f}")
    print(f"Query executed in {query_time:.6f} seconds (O(log N)).\n")

    # 2.2 Range Query (Ball Tree / Points within radius)
    # Find all points within a distance of 2.0 from the query point
    radius = 2.0
    start_range = time.time()
    indices_within_radius = tree.query_ball_point(query_point, r=radius)
    range_time = time.time() - start_range

    print("--- Range Query ---")
    print(f"Found {len(indices_within_radius)} points within radius {radius}.")
    print(f"Query executed in {range_time:.6f} seconds.\n")


def demo_computational_geometry() -> None:
    """
    Demonstrates Convex Hulls, Delaunay Triangulation, and Voronoi Diagrams.
    
    These structures are fundamental in graphics, pathfinding, and modeling.
    """
    print("=" * 60)
    print("3. COMPUTATIONAL GEOMETRY")
    print("=" * 60)

    # Let's create a small set of random 2D points
    np.random.seed(99)
    points = np.random.rand(15, 2)

    # 3.1 Convex Hull
    # Finds the smallest convex polygon containing all points.
    # Edge case: All points collinear. `scipy.spatial.ConvexHull` uses Qhull, 
    # which robustly handles or errors appropriately on degenerate inputs.
    try:
        hull = spatial.ConvexHull(points)
        print("--- Convex Hull ---")
        print(f"Number of points forming the hull (vertices): {len(hull.vertices)}")
        print(f"Hull Area (Volume in 2D): {hull.volume:.4f}")
        print(f"Hull Perimeter (Area in 2D): {hull.area:.4f}")
        print("Vertices indices (counterclockwise):", hull.vertices)
        print()
    except spatial.qhull.QhullError as e:
        print(f"Failed to compute Convex Hull: {e}")

    # 3.2 Delaunay Triangulation
    # Connects points into a mesh of triangles maximizing the minimum angle.
    print("--- Delaunay Triangulation ---")
    triangulation = spatial.Delaunay(points)
    print(f"Created {triangulation.simplices.shape[0]} triangles (simplices).")
    
    # We can use the Delaunay object to test if points are inside the hull
    test_points = np.array([[0.5, 0.5], [1.5, 1.5]])  # One likely inside, one clearly outside
    
    # find_simplex returns the index of the triangle containing the point, or -1 if outside
    simplex_indices = triangulation.find_simplex(test_points)
    for p, sim_idx in zip(test_points, simplex_indices):
        status = "Inside" if sim_idx != -1 else "Outside"
        print(f"Point {p} is {status} the triangulation (Simplex index: {sim_idx}).")
    print()

    # 3.3 Voronoi Diagrams
    # Divides space into regions based on the nearest seed point.
    print("--- Voronoi Diagram ---")
    vor = spatial.Voronoi(points)
    print(f"Number of Voronoi regions generated: {len(vor.regions)}")
    print(f"Number of finite and infinite Voronoi vertices: {len(vor.vertices)}")
    print("Note: Regions containing '-1' in their vertex list extend to infinity.\n")


def spatial_interview_challenge(locations: np.ndarray, threshold_distance: float) -> List[Tuple[int, int]]:
    """
    Common Spatial Interview Challenge:
    Given a list of (x, y) coordinates representing delivery hubs, find all pairs of 
    hubs that are dangerously close to each other (distance < threshold_distance).
    
    Constraints: 
    - The number of hubs can be up to 10,000.
    - Return a list of tuples containing the indices of the hub pairs (i, j) where i < j.
    
    Naive Approach: O(N^2) pairwise distance calculation.
    Optimized Approach: Use a KDTree which efficiently prunes the search space.
    
    Args:
        locations (np.ndarray): Shape (N, 2) array of coordinates.
        threshold_distance (float): The maximum distance to be considered "dangerously close".
        
    Returns:
        List[Tuple[int, int]]: List of index pairs.
    """
    print("=" * 60)
    print("4. INTERVIEW CHALLENGE: Close Facilities (KDTree Pairs)")
    print("=" * 60)
    
    if len(locations) < 2:
        return []
        
    # Build KDTree for O(N log N) processing
    tree = spatial.cKDTree(locations)
    
    # query_pairs finds all pairs of points within the specified distance r.
    # It directly returns a set of tuples (i, j) where i < j, which is highly optimized in C.
    start = time.time()
    close_pairs = tree.query_pairs(r=threshold_distance)
    elapsed = time.time() - start
    
    print(f"Found {len(close_pairs)} close pairs in {elapsed:.6f} seconds using cKDTree.")
    
    # Convert set to sorted list for deterministic output
    return sorted(list(close_pairs))


def run_benchmarks_and_tests() -> None:
    """
    Benchmarks standard loops vs scipy spatial optimized operations to 
    prove why using this library is critical for performance.
    """
    print("=" * 60)
    print("5. PERFORMANCE BENCHMARKS & TESTS")
    print("=" * 60)

    np.random.seed(7)
    test_points = np.random.rand(2000, 2) * 100
    
    print("Task: Find all unique pairs within a distance of 2.0 (for 2,000 points)")
    
    # 1. Pure Python approach (Brute Force O(N^2))
    start_py = time.time()
    py_pairs = []
    n = len(test_points)
    for i in range(n):
        for j in range(i + 1, n):
            dx = test_points[i, 0] - test_points[j, 0]
            dy = test_points[i, 1] - test_points[j, 1]
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 2.0:
                py_pairs.append((i, j))
    py_time = time.time() - start_py
    print(f"Pure Python Brute Force: {py_time:.4f} sec | Pairs found: {len(py_pairs)}")
    
    # 2. Scipy cKDTree optimized O(N log N + K)
    start_scipy = time.time()
    tree = spatial.cKDTree(test_points)
    scipy_pairs = tree.query_pairs(r=2.0)
    scipy_time = time.time() - start_scipy
    print(f"Scipy cKDTree Approach:  {scipy_time:.4f} sec | Pairs found: {len(scipy_pairs)}")
    
    # Assert correctness
    assert len(py_pairs) == len(scipy_pairs), "Mismatch in number of pairs found!"
    print(f"\nSPEEDUP: The cKDTree is {py_time / scipy_time:.2f}x faster on just 2k points!")
    print("For N=100,000, pure Python would take hours; cKDTree takes milliseconds.")
    print("\nAll tests passed successfully.")


if __name__ == "__main__":
    print("=" * 80)
    print(f"SCIPY SPATIAL MASTERCLASS".center(80))
    print("=" * 80 + "\n")
    
    # 1. Distance Metrics
    demo_distance_metrics()
    
    # 2. KD Trees
    demo_kdtree_for_nearest_neighbors()
    
    # 3. Geometry (Hull, Delaunay, Voronoi)
    demo_computational_geometry()
    
    # 4. Challenge
    np.random.seed(0)
    hubs = np.random.rand(5000, 2) * 1000  # 5000 hubs in a 1000x1000 area
    close_hubs = spatial_interview_challenge(hubs, threshold_distance=5.0)
    print(f"Sample of close pairs: {close_hubs[:5]}...")
    print()
    
    # 5. Benchmarks
    run_benchmarks_and_tests()
    
    print("=" * 80)
    print(f"END OF SCIPY SPATIAL MASTERCLASS".center(80))
    print("=" * 80 + "\n")
