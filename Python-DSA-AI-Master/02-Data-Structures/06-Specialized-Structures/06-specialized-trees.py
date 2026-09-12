"""
## A. Concept Name
Specialized Trees (Segment Trees)

## B. Motivation
Efficiently process range queries (sum, min, max) and point updates dynamically on an array.

## C. Real-World Analogy
Like an index in a book where each chapter summarizes its pages, and the book summarizes the chapters, allowing fast lookups of total words without recounting everything.

## D. Core Mechanics
A Segment Tree is a binary tree where each node represents an interval of the array. The root represents the entire array, and the leaves represent individual elements. It supports O(log N) range queries and point updates.

## E. Time & Space Complexity
- Build: O(N) Time
- Query: O(log N) Time
- Update: O(log N) Time
- Space Complexity: O(N) auxiliary space

## F. Common Operations
Build, Update, Range Query.

## G. Edge Cases
- Completely outside range queries.
- Modifying leaf nodes correctly bubbling up.

## H. Common Pitfalls
- Not allocating enough space for the tree array (usually 4*N is needed).
- Off-by-one errors in interval indexing.

## I. Best Practices
Use 0-based indexing carefully. Clear boundary logic (`start`, `end`, `L`, `R`).

## J. Typical Use Cases
- Range Sum Query (RSQ).
- Range Minimum Query (RMQ).
- Computational Geometry.

## K. Variations
- Lazy Propagation Segment Tree.
- Persistent Segment Tree.
- 2D Segment Tree.

## L. Related Concepts
- Fenwick Tree (Binary Indexed Tree).
- Prefix Sums (static).
- Sparse Table.

## M. Interview Patterns
Often appears when dynamic updates are mixed with range queries.

## N. System Design
Used in metrics aggregation, analytics dashboards, and real-time monitoring.

## O. Advanced Optimizations
Iterative Segment Tree can reduce space and overhead.

## P. Debugging Tips
Print the tree array and check if parent nodes correctly combine their children.

## Q. Testing Strategy
Test with small ranges, entire ranges, point updates, and out-of-bound edge logic.

## R. Language Specifics
In Python, lists are used, but integer arrays or NumPy could optimize space.

## S. Code Readability
Modularize `_build`, `_update`, and `_query` helper methods.

## T. Performance Tuning
Use bitwise operations `2*i+1` -> `(i<<1)+1` if micro-optimizing.

## U. Security/Robustness
Validate bounds to prevent out-of-index errors.

## V. Visualization
Root: [0, N-1], Left: [0, mid], Right: [mid+1, N-1].

## W. Learning Checklist
[x] Build, [x] Point Update, [x] Range Query, [ ] Lazy Propagation.

## X. Project Connection
Essential in AI search environments for fast state or reward aggregation over specific ranges.
"""

from typing import List

class SegmentTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        # Tree array size needs to be at most 4 * N
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            self._build(arr, left_child, start, mid)
            self._build(arr, right_child, mid + 1, end)
            
            # Combine
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update(self, idx: int, val: int) -> None:
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
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
        return self._query(0, 0, self.n - 1, L, R)

    def _query(self, node: int, start: int, end: int, L: int, R: int) -> int:
        if R < start or L > end:
            return 0 # Outside range, return identity for sum
        
        if L <= start and end <= R:
            return self.tree[node] # Completely inside range
            
        mid = (start + end) // 2
        p1 = self._query(2 * node + 1, start, mid, L, R)
        p2 = self._query(2 * node + 2, mid + 1, end, L, R)
        return p1 + p2

# Performance Analysis:
# - Time Complexity: Build O(N). Update O(log N). Query O(log N).
# - Space Complexity: O(N) auxiliary space.

# Edge Cases:
# - Completely outside range queries.
# - Modifying leaf nodes correctly bubbling up.

# Interview Challenge:
# Implement Lazy Propagation on a Segment Tree to support O(log N) Range Updates.

# Tests
def test_segment_tree():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    
    assert st.query(1, 3) == 15 # 3 + 5 + 7
    st.update(1, 10) # arr becomes [1, 10, 5, 7, 9, 11]
    assert st.query(1, 3) == 22 # 10 + 5 + 7

if __name__ == "__main__":
    test_segment_tree()
    print("06-specialized-trees.py tests passed successfully!")
