"""
## A. Concept Name
Disjoint Set Union (DSU)

## B. Learning Objectives
1. Understand the Disjoint Set (Union-Find) data structure.
2. Implement path compression for efficient 'find' operations.
3. Implement union by rank/size for efficient 'union' operations.

## C. Concept Explanation
DSU tracks a set of elements partitioned into a number of disjoint (non-overlapping) subsets. It supports two useful operations:
1. Find: Determine which subset a particular element is in.
2. Union: Join two subsets into a single subset.
With path compression and union by rank, both operations take nearly O(1) amortized time (inverse Ackermann function).

## D. Code Implementation
See the `DSU` class and `count_components` function below.

## E. Performance Analysis
- Time Complexity: O(alpha(N)) amortized per operation, where alpha is the inverse Ackermann function. Effectively O(1).
- Space Complexity: O(N) to store parent and rank arrays.

## F. Edge Cases
- Attempting to union elements already in the same set.
- Out of bounds element queries (needs manual checks).

## G. Interview Challenge
Number of Connected Components
Given an undirected graph, find the number of connected components using DSU.

## X. Project Connection
DSU is essential in AI for clustering algorithms, evaluating network connectivity, image segmentation (e.g., merging connected pixels), and finding connected components in knowledge graphs.
"""

class DSU:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        # Path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i == root_j:
            return False
            
        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
            
        return True

def count_components(n: int, edges: list[list[int]]) -> int:
    dsu = DSU(n)
    components = n
    for u, v in edges:
        if dsu.union(u, v):
            components -= 1
    return components

# Tests
def test_dsu():
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(1, 2)
    assert dsu.find(0) == dsu.find(2)
    assert dsu.find(0) != dsu.find(3)

def test_components():
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(4, [[0, 1], [2, 3]]) == 2

if __name__ == "__main__":
    test_dsu()
    test_components()
    print("01-disjoint-set-union.py tests passed successfully!")
