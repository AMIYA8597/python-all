"""
## A. Concept Name
Disjoint Set Union (DSU) / Union-Find

## B. Core Intent
Provide a highly efficient data structure to track elements partitioned into disjoint subsets, supporting near-constant-time Find and Union operations.

## C. Key Takeaways
- DSU is used to group elements and determine if they belong to the same group.
- Path Compression flattens the tree during Find.
- Union by Size/Rank keeps the tree shallow.
- Time complexity is O(α(N)), where α is the inverse Ackermann function (effectively O(1)).

## D. Real-World Context
- Network connectivity (e.g., routing protocols, social networks).
- Image processing (finding connected components / regions).
- Minimum Spanning Trees (Kruskal's algorithm for cost-effective wiring).

## E. Technical Vocabulary
- Disjoint Sets, Union-Find, Root Node, Path Compression, Union by Rank/Size, Connected Components, Inverse Ackermann Function.

## F. Common Pitfalls
- Forgetting to initialize the parent array correctly (each node points to itself).
- Omitting Path Compression or Union by Size, leading to O(N) operations.
- Using `root_i` instead of `self.parent[root_i]` during union when path compression isn't fully propagated.

## G. Setup & Prerequisites
- Python basics, understanding of trees and arrays.

## H. Step-by-Step Walkthrough
1. Initialize an array where `parent[i] = i`.
2. Find operation: Recursively traverse up to the root, setting `parent[node] = root` on the way back (Path Compression).
3. Union operation: Find the roots of both elements. If different, attach the smaller tree's root to the larger tree's root (Union by Size).

## I. Best Practices
- Always use both Path Compression and Union by Size/Rank for optimal O(α(N)) complexity.
- Encapsulate the DSU logic within a class for reusability.

## J. Debugging Tips
- If elements aren't correctly grouping, ensure `find()` is used to get roots during `union()` rather than using elements directly.
- Print the `parent` array to trace component formations.

## K. Performance Tuning
- In competitive programming, a flat array or list for `parent` and `size` is much faster than object-oriented node representations.

## L. Testing Strategy
- Test with entirely disconnected nodes, fully connected nodes, and linear chains.
- Assert component counts match expected values.

## M. Code Organization
- Keep `BasicDSU` and `ProfessionalDSU` classes separate to illustrate optimizations.

## N. Security Considerations
- Malicious inputs forming deep trees can cause stack overflow if recursion limit is low (Path Compression). Use iterative Find if recursion depth is a concern.

## O. Deployment Considerations
- Wrap DSU in libraries as a standard disjoint-set collection.

## P. Maintenance & Scalability
- Array-based DSU scales well up to memory limits, though dynamic adding of nodes might require a hash map instead of a list.

## Q. Data Handling
- Inputs are typically 0-indexed or 1-indexed integers. Map arbitrary objects to integers if needed.

## R. Related Patterns
- Graph traversals (DFS/BFS) for connected components.
- Kruskal's Minimum Spanning Tree.

## S. Alternatives
- DFS/BFS can find connected components but cannot efficiently handle dynamic edge additions (online connectivity).

## T. External References
- CP-Algorithms: Disjoint Set Union.

## U. Further Reading
- Tarjan's analysis of the inverse Ackermann function.

## V. Exercises
- Implement a DSU that supports rollbacks (undoing the last union).
- Solve "Number of Provinces" and "Redundant Connection".

## W. FAQ
- Q: What is the inverse Ackermann function? A: A function that grows so slowly it is <= 4 for all practically applicable values of N.

## X. Project Connection
DSU is essential for graph algorithms in AI pathfinding, clustering operations, and dynamic connectivity problems in complex network simulations.
"""

from typing import List, Dict

class BasicDSU:
    """Basic Disjoint Set without optimizations."""
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        return self.find(self.parent[i])

    def union(self, i: int, j: int) -> None:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j

class ProfessionalDSU:
    """Optimized Disjoint Set Union with Path Compression and Union by Size."""
    def __init__(self, size: int):
        # Initialize each element as its own parent.
        self.parent = list(range(size))
        # Keep track of the size of each component.
        self.size = [1] * size
        # Number of connected components
        self.components = size

    def find(self, i: int) -> int:
        """Find the root of the set containing i, with path compression."""
        if self.parent[i] != i:
            # Path compression: update parent to the root directly
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Union the sets containing i and j by size.
        Returns True if a union was performed, False if they were already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False  # Already in the same component, forms a cycle

        # Union by size: attach smaller component to larger one
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i

        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        self.components -= 1
        return True

    def get_size(self, i: int) -> int:
        """Get the size of the component containing element i."""
        return self.size[self.find(i)]

def count_provinces(isConnected: List[List[int]]) -> int:
    """
    Problem: Find the number of connected provinces.
    A province is a group of directly or indirectly connected cities.
    isConnected[i][j] = 1 if i and j are directly connected.
    """
    n = len(isConnected)
    dsu = ProfessionalDSU(n)
    
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                dsu.union(i, j)
                
    return dsu.components

def redundant_connection(edges: List[List[int]]) -> List[int]:
    """
    Problem: Redundant Connection.
    Given an undirected graph that started as a tree with N nodes, one additional edge was added.
    Find the edge that can be removed so the resulting graph is a tree.
    """
    n = len(edges)
    dsu = ProfessionalDSU(n + 1)
    
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
            
    return []

if __name__ == "__main__":
    # Test Count Provinces
    provinces = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1]
    ]
    assert count_provinces(provinces) == 2, "Test case 1 failed"
    print("Count Provinces tests passed.")
    
    # Test Redundant Connection
    edges = [[1, 2], [1, 3], [2, 3]]
    assert redundant_connection(edges) == [2, 3], "Test case 2 failed"
    
    edges2 = [[1,2], [2,3], [3,4], [1,4], [1,5]]
    assert redundant_connection(edges2) == [1, 4], "Test case 3 failed"
    print("Redundant Connection tests passed.")

    """
    Complexity Analysis:
    Time Complexity:
    - O(V^2) for count_provinces to traverse the matrix, but O(V^2 * α(V)) for unions.
    - O(E * α(V)) for redundant_connection where E is the number of edges.
    
    Space Complexity:
    - O(V) for the DSU internal arrays (`parent` and `size`).
    
    Interview Challenge:
    Modify the DSU to handle dynamically adding nodes, or implement an algorithm 
    to answer offline connectivity queries.
    """
