"""
CodeChef Long Challenge Practice
================================

Overview
--------
CodeChef Long Challenges typically run for several days. Problems range from basic
implementations to extremely complex algorithmic and mathematical puzzles. Because
time is ample during the contest, solutions often require optimizing time complexity
from O(N^2) to O(N log N) or O(N), implementing advanced data structures (like 
Segment Trees, Fenwick Trees, Suffix Automata), or optimizing constant factors.

Learning Objectives:
1. Master segment trees for range queries and point updates.
2. Understand lazy propagation for range updates.
3. Write robust, clean, and well-typed data structure implementations.
4. Analyze the space-time tradeoffs of advanced tree structures.

Concept Explanation
-------------------
A Segment Tree is a binary tree used for storing information about intervals or segments.
It allows querying which of the stored segments contain a given point, or answering
range queries (like sum, minimum, maximum) over an array in O(log N) time.

In a Long Challenge, you might need a segment tree to keep track of dynamic arrays
where both updates and queries are frequent.

Basic to Professional Implementation
------------------------------------
Below is a professional-grade implementation of a Segment Tree for Range Minimum Queries (RMQ).
"""

from typing import List, Union

class SegmentTree:
    """
    A professional-grade Segment Tree for Range Minimum Queries (RMQ).
    """
    def __init__(self, data: List[int]):
        self.n = len(data)
        # Tree size is at most 4*N
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            self.tree[node] = min(self.tree[left_child], self.tree[right_child])

    def query(self, L: int, R: int) -> Union[int, float]:
        """
        Query the minimum value in the range [L, R].
        """
        if L < 0 or R >= self.n or L > R:
            raise ValueError("Invalid query range")
        return self._query(0, 0, self.n - 1, L, R)

    def _query(self, node: int, start: int, end: int, L: int, R: int) -> Union[int, float]:
        # Complete overlap
        if L <= start and end <= R:
            return self.tree[node]
        
        # No overlap
        if end < L or start > R:
            return float('inf')
            
        # Partial overlap
        mid = (start + end) // 2
        left_min = self._query(2 * node + 1, start, mid, L, R)
        right_min = self._query(2 * node + 2, mid + 1, end, L, R)
        return min(left_min, right_min)

    def update(self, idx: int, value: int) -> None:
        """
        Update the value at index `idx` to `value`.
        """
        if idx < 0 or idx >= self.n:
            raise IndexError("Index out of bounds")
        self._update(0, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, value: int) -> None:
        if start == end:
            self.tree[node] = value
        else:
            mid = (start + end) // 2
            if start <= idx <= mid:
                self._update(2 * node + 1, start, mid, idx, value)
            else:
                self._update(2 * node + 2, mid + 1, end, idx, value)
            self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])


if __name__ == "__main__":
    # Tests and Assertions
    print("Testing SegmentTree for CodeChef Long Challenge...")
    arr = [1, 3, 2, 7, 9, 11]
    st = SegmentTree(arr)
    
    # Query min in [1, 4] -> min(3, 2, 7, 9) = 2
    assert st.query(1, 4) == 2, f"Expected 2, got {st.query(1, 4)}"
    
    # Query min in [0, 5] -> min(1, 3, 2, 7, 9, 11) = 1
    assert st.query(0, 5) == 1, f"Expected 1, got {st.query(0, 5)}"
    
    # Update index 2 from 2 to 10
    st.update(2, 10)
    # Array is now [1, 3, 10, 7, 9, 11]
    
    # Query min in [1, 4] -> min(3, 10, 7, 9) = 3
    assert st.query(1, 4) == 3, f"Expected 3, got {st.query(1, 4)}"
    
    print("All tests passed!")

"""
Complexity Analysis:
- Building the tree: O(N) time, O(N) space.
- Querying a range: O(log N) time.
- Point update: O(log N) time.

Common Mistakes:
- Off-by-one errors when defining segment boundaries or child indices.
- Not allocating enough space for the segment tree array (should be 4 * N).
- Forgetting to update parent nodes after updating child nodes in the `update` function.

Interview Challenge:
Modify the SegmentTree class to support Range Updates (e.g., add X to all elements in range [L, R])
using Lazy Propagation in O(log N) time.
"""
