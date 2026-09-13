"""
# ==============================================================================
# LABORATORY: SPATIAL TREES (K-D TREES & K-NEAREST NEIGHBORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Binary Search Tree (BST) organizes 1-Dimensional data (e.g., numbers).
# But what if you have 2-Dimensional data? (e.g., GPS coordinates on a map).
# If a user opens Uber and requests a ride, Uber needs to find the "Nearest Driver" 
# out of 100,000 cars.
#
# Doing an O(N) linear scan to calculate the distance to every car is too slow.
# We need an O(log N) search. But a BST only sorts by X or Y, not both!
#
# The "K-Dimensional Tree" (K-D Tree) solves this. It is a Binary Tree that 
# alternates the sorting axis at every level! 
# Level 0: Sorts by X. (Left child has smaller X, Right child has larger X).
# Level 1: Sorts by Y. (Left child has smaller Y, Right child has larger Y).
# Level 2: Sorts by X again.
#
# This perfectly partitions 2D, 3D, or K-Dimensional space, allowing O(log N) 
# Nearest Neighbor Searches (crucial for Machine Learning KNN algorithms).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Spatial Partitioning.
# - Build a 2-D Tree.
# - Implement Nearest Neighbor Search with spatial pruning.
#
# ==============================================================================
"""

import math
from typing import List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. K-D TREE IMPLEMENTATION
# ==============================================================================
class KDNode:
    def __init__(self, point: Tuple[float, float]):
        self.point = point
        self.left: Optional['KDNode'] = None
        self.right: Optional['KDNode'] = None

class KDTree:
    def __init__(self, points: List[Tuple[float, float]]):
        """
        Builds a balanced 2-D Tree in O(N log N) time.
        We achieve balance by always picking the MEDIAN point of the current axis 
        to be the root of the subtree.
        """
        self.k = 2 # 2 Dimensions (X and Y)
        self.root = self._build(points, depth=0)

    def _build(self, points: List[Tuple[float, float]], depth: int) -> Optional[KDNode]:
        if not points:
            return None
            
        # Determine the axis to split on (0 for X, 1 for Y)
        axis = depth % self.k
        
        # Sort points by the chosen axis to find the median
        points.sort(key=lambda p: p[axis])
        median_idx = len(points) // 2
        
        # Create node and recursively build children
        node = KDNode(points[median_idx])
        node.left = self._build(points[:median_idx], depth + 1)
        node.right = self._build(points[median_idx + 1:], depth + 1)
        
        return node

    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Standard Euclidean distance squared (saves a math.sqrt call)."""
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    def nearest_neighbor(self, target: Tuple[float, float]) -> Tuple[Tuple[float, float], float]:
        """
        Finds the closest point to `target` in O(log N) time.
        Returns (Best_Point, Distance).
        """
        best_point = None
        best_dist = float('inf')
        
        def _search(node: KDNode, depth: int):
            nonlocal best_point, best_dist
            
            if node is None:
                return
                
            # 1. Update best if this node is closer
            dist = self._distance(node.point, target)
            if dist < best_dist:
                best_dist = dist
                best_point = node.point
                
            # 2. Determine which child to visit first (the one that naturally contains the target)
            axis = depth % self.k
            target_coord = target[axis]
            node_coord = node.point[axis]
            
            if target_coord < node_coord:
                first_child = node.left
                second_child = node.right
            else:
                first_child = node.right
                second_child = node.left
                
            # 3. Recursively search the promising half
            _search(first_child, depth + 1)
            
            # 4. PRUNING OPTIMIZATION: Do we even need to check the other half?
            # If the distance from the target to the SPLITTING LINE is GREATER than 
            # our current `best_dist`, then it is mathematically impossible for the 
            # other half of the tree to contain a closer point! We can completely skip it!
            # This pruning is what makes K-D Tree O(log N) instead of O(N).
            axis_distance = (target_coord - node_coord)**2
            
            if axis_distance < best_dist:
                # The hypersphere intersects the splitting line. We must check the other half.
                _search(second_child, depth + 1)

        _search(self.root, 0)
        return best_point, math.sqrt(best_dist) # Return actual distance now

def demonstrate_kd_tree():
    section_header("Algorithm: K-D Tree (Nearest Neighbor Search)")
    
    # A list of coordinates (X, Y)
    cars = [
        (2.0, 3.0),
        (5.0, 4.0),
        (9.0, 6.0),
        (4.0, 7.0),
        (8.0, 1.0),
        (7.0, 2.0)
    ]
    
    print(f"Driver Coordinates (Cars): {cars}")
    print("Building K-D Tree...")
    kdtree = KDTree(cars)
    
    user_location = (9.0, 2.0)
    print(f"\nUser is at location: {user_location}")
    print("Searching for the absolute closest car in O(log N) time...")
    
    best_car, distance = kdtree.nearest_neighbor(user_location)
    
    print(f"\nResult: The closest car is at {best_car}")
    print(f"Distance: {distance:.2f} units")
    
    # Verify manually
    print("\nManual Verification (O(N) linear scan):")
    for car in cars:
        dist = math.sqrt((car[0]-user_location[0])**2 + (car[1]-user_location[1])**2)
        print(f" Car {car} -> Distance {dist:.2f}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does K-D Tree construction sort the points and pick the Median at every step?
   Answer: To guarantee the tree is perfectly balanced. If we just inserted points randomly, a K-D tree could degenerate into a straight line (Linked List), making the search O(N). Picking the median ensures exactly half the points go left, and half go right, guaranteeing a depth of O(log N).

2. What is Spatial Pruning?
   Answer: When searching for the nearest neighbor, we keep track of the `best_distance` found so far. The K-D Tree divides space using straight lines (axis-aligned planes). If the perpendicular distance from our target point to the dividing line is LARGER than our `best_distance`, we know that the entire region on the other side of the line is too far away. We can safely prune (skip) that entire massive branch of the tree!

3. Are K-D Trees good for high dimensions (e.g. 1000-dimensional Machine Learning embeddings)?
   Answer: NO. This is called the "Curse of Dimensionality". In high dimensions, the pruning optimization completely fails because the distance to the splitting line is almost always smaller than the `best_distance`. The algorithm degrades into a slow O(N) brute-force search. For high dimensions, Approximate Nearest Neighbor (ANN) algorithms like HNSW (Hierarchical Navigable Small World graphs) or LSH (Locality Sensitive Hashing) are used instead.
"""

if __name__ == "__main__":
    demonstrate_kd_tree()
    print("\n[SUCCESS] Laboratory: K-D Trees Completed.")
