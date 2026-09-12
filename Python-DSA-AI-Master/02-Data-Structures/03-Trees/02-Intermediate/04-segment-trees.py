"""
## A. Concept Name
Segment Trees

## B. Concept Explanation
A Segment Tree is a binary tree used for storing intervals or segments. It allows querying
which of the stored segments contain a given point, but it's most famous for answering Range
Queries (like finding the sum of array elements from index L to R) and updating elements in O(log n) time.

## C. Learning Objectives
1. Understand when to use Segment Trees (range queries and point updates)
2. Build a segment tree from an array
3. Perform range queries (like sum, min, max) and point updates efficiently

## D. Common Pitfalls
- Forgetting to allocate enough space (4 * n is a safe bound).
- Off-by-one errors when managing segment bounds in recursion.
- Failing to return a neutral element (like 0 for sum, inf for min) for out-of-bounds queries.

## E. Real-world Application
- Fast range queries in databases (e.g., retrieving aggregate statistics for a time range).
- Finding minimum, maximum, or sum in intervals in game development or graphics algorithms.

## F. Time and Space Complexity
- Build: O(n)
- Query: O(log n)
- Update: O(log n)
- Space Complexity: O(n), specifically an array of size 4 * n.

## G. Edge Cases
- Empty input array.
- Out of bounds queries (handled by returning neutral element, e.g., 0 for sum).
- Point updates vs Range updates (range updates require Lazy Propagation).

## H. Implementation Steps
1. Determine the size of the array and allocate 4*n size for the tree.
2. Recursively build the tree by splitting ranges into halves.
3. Implement query and update operations using recursive traversal.

## I. Example Walkthrough
Given array [1, 3, 5, 7, 9, 11], the tree stores sums of segments.
To query sum(1, 3), we visit nodes covering indices 1 to 3 and sum them (3+5+7=15).

## J. Advanced Techniques
- Lazy Propagation for efficient range updates.
- 2D Segment Trees for grid-based spatial queries.

## K. Practice Exercises
- Implement a Range Minimum Query (RMQ) Segment Tree.
- Adapt the Segment Tree to find the number of zeros in a given range.

## L. Additional Resources
- CP-Algorithms Segment Tree guide.
- Introduction to Algorithms (CLRS).

## M. Interview Questions
- How do you handle range updates efficiently?
- Why do we allocate 4*N space instead of 2*N?

## N. AI / Machine Learning Application
- Efficient feature aggregations and running statistics over sliding windows in time-series forecasting.

## O. System Design Context
- Segment trees are used in specialized in-memory time-series databases to accelerate interval data aggregations.

## P. Optimization Strategies
- Iterative Segment Trees: Can be implemented iteratively to avoid recursion overhead and reduce space to exactly 2*N.

## Q. Testing Strategies
- Test with empty arrays, single-element arrays, and very large inputs.
- Cross-validate results with a naive O(n) loop approach.

## R. Mathematical Foundation
- Relies on the associativity of operations (like sum, min, max). If (A+B)+C = A+(B+C), the property can be efficiently cached.

## S. Historical Context
- Originally proposed in computational geometry by Jon Bentley in 1977 for solving interval problems.

## T. Language-Specific Details
- In Python, recursion limits might be hit for very deep trees, though segment trees have depth O(log n), so it is rarely an issue for reasonable n.

## U. Debugging Tips
- Print the flat tree array. The root element `tree[0]` should reflect the combined result of the whole array.

## V. Comparative Analysis
- Segment Tree vs Fenwick Tree (Binary Indexed Tree): Fenwick is simpler to code and uses less memory, but Segment Tree is more versatile (handles non-invertible operations like min/max).

## W. Code Walkthrough
- `__init__`: Allocates space and triggers `_build`.
- `_build`: Recursively halves range, assigning values from leaves up.
- `_query`: Returns exact range matches or splits the query down to children.

## X. Project Connection
This data structure serves as the underlying analytical engine for fast metric aggregation in dashboard or trading algorithms.
"""

from typing import List

class SegmentTree:
    """Implementation of a Segment Tree for Range Sum Queries."""
    
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            
            # Combine
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, idx: int, val: int):
        if self.n > 0:
            self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            if start <= idx <= mid:
                self._update(left_child, start, mid, idx, val)
            else:
                self._update(right_child, mid + 1, end, idx, val)
                
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query(self, L: int, R: int) -> int:
        if self.n == 0:
            return 0
        return self._query(0, 0, self.n - 1, L, R)

    def _query(self, node: int, start: int, end: int, L: int, R: int) -> int:
        # Outside range
        if R < start or end < L:
            return 0
        
        # Fully inside range
        if L <= start and end <= R:
            return self.tree[node]
            
        # Partially inside range
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        p1 = self._query(left_child, start, mid, L, R)
        p2 = self._query(right_child, mid + 1, end, L, R)
        
        return p1 + p2

def test_segment_tree():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    
    assert st.query(1, 3) == 15  # 3 + 5 + 7
    st.update(1, 10)             # array becomes [1, 10, 5, 7, 9, 11]
    assert st.query(1, 3) == 22  # 10 + 5 + 7
    
    print("Segment Tree basic tests passed!")

if __name__ == "__main__":
    test_segment_tree()
