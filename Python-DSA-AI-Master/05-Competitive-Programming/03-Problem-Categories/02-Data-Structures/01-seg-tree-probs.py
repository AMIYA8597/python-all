"""
Competitive Programming Problems: Segment Trees
===============================================

Overview:
---------
A Segment Tree is a versatile and highly applicable data structure used to answer range queries 
(like finding the sum, minimum, or maximum in an array segment) in O(log N) time, while also 
allowing updates to the array elements in O(log N) time.

Learning Objectives:
--------------------
1. Understand the structure and memory layout of a Segment Tree.
2. Implement recursive Point Updates and Range Queries.
3. Master Lazy Propagation for efficiently handling Range Updates.

Industry Use Cases:
-------------------
- Game Development: Collision detection using spatial trees, or managing dynamic statistics 
  over ranges (e.g., team health in a zone).
- Financial Systems: Fast tracking of stock minimums/maximums over dynamic time windows.
- Database Engines: Used inside database indexing for multidimensional range queries.

Beginner to Advanced Explanations:
----------------------------------
- Basic: If we use a normal array for Range Sums, updating takes O(1) but querying takes O(N). 
  If we use Prefix Sums, querying takes O(1) but updating takes O(N). A Segment Tree balances 
  this by making BOTH operations O(log N). It achieves this by storing aggregated data 
  in a binary tree structure.
- Advanced: Lazy Propagation is required when we want to update a whole range (e.g., "Add 5 to 
  all elements from index L to R"). Updating them one-by-one takes O(N log N). With lazy 
  propagation, we delay the update to children nodes until they are actually queried, 
  reducing the range update complexity to O(log N).

Performance & Space Considerations:
-----------------------------------
- Segment Trees typically require an array of size 4 * N to represent a tree for an array of size N.
- Using flat arrays (0-indexed) is cache-friendly compared to Node-based object graphs.
"""

from typing import List, Callable, Union
import math

class SegmentTree:
    """
    A generic professional-grade Segment Tree supporting Lazy Propagation.
    Configurable with different associative operations (e.g., sum, min, max).
    
    Time Complexity:
    - Build: O(N)
    - Range Query: O(log N)
    - Range Update (Lazy): O(log N)
    """
    
    def __init__(self, data: List[int], op: str = 'sum'):
        self.n = len(data)
        # 4 * N is the safe upper bound for segment tree array size
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        
        self.op_type = op
        if self.op_type == 'sum':
            self.merge = lambda x, y: x + y
            self.default_val = 0
        elif self.op_type == 'min':
            self.merge = lambda x, y: min(x, y)
            self.default_val = float('inf')
        elif self.op_type == 'max':
            self.merge = lambda x, y: max(x, y)
            self.default_val = float('-inf')
        else:
            raise ValueError("Unsupported operation type. Use 'sum', 'min', or 'max'.")
            
        self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        """Recursively builds the segment tree."""
        if start == end:
            self.tree[node] = data[start]
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        
        self.tree[node] = self.merge(self.tree[left_child], self.tree[right_child])

    def _apply_lazy(self, node: int, start: int, end: int) -> None:
        """Applies pending lazy updates to the current node and passes them to children."""
        if self.lazy[node] != 0:
            # Apply the pending update
            if self.op_type == 'sum':
                # For sum, adding X to all elements in range means adding X * count to the total
                self.tree[node] += self.lazy[node] * (end - start + 1)
            else:
                # For min/max, adding X to all elements just adds X to the min/max value
                self.tree[node] += self.lazy[node]
                
            # If not a leaf node, propagate the lazy value downwards
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
                
            # Clear current node's lazy value
            self.lazy[node] = 0

    def update_range(self, l: int, r: int, val: int) -> None:
        """Adds 'val' to all elements in the range [l, r]."""
        self._update_range_util(0, 0, self.n - 1, l, r, val)

    def _update_range_util(self, node: int, start: int, end: int, l: int, r: int, val: int) -> None:
        # First, ensure all pending updates are applied
        self._apply_lazy(node, start, end)
        
        # No overlap
        if start > end or start > r or end < l:
            return
            
        # Complete overlap
        if start >= l and end <= r:
            self.lazy[node] += val
            self._apply_lazy(node, start, end)
            return
            
        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._update_range_util(left_child, start, mid, l, r, val)
        self._update_range_util(right_child, mid + 1, end, l, r, val)
        
        self.tree[node] = self.merge(self.tree[left_child], self.tree[right_child])

    def query(self, l: int, r: int) -> Union[int, float]:
        """Queries the aggregated value in the range [l, r]."""
        return self._query_util(0, 0, self.n - 1, l, r)

    def _query_util(self, node: int, start: int, end: int, l: int, r: int) -> Union[int, float]:
        # Always resolve lazy updates before querying
        self._apply_lazy(node, start, end)
        
        # No overlap
        if start > end or start > r or end < l:
            return self.default_val
            
        # Complete overlap
        if start >= l and end <= r:
            return self.tree[node]
            
        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_val = self._query_util(left_child, start, mid, l, r)
        right_val = self._query_util(right_child, mid + 1, end, l, r)
        
        return self.merge(left_val, right_val)


# =============================================================================
# Tests and Main Guard
# =============================================================================
if __name__ == "__main__":
    print("Running Tests for Segment Tree with Lazy Propagation...\n")
    
    # Initial array
    arr = [1, 3, 5, 7, 9, 11]
    print(f"Initial array: {arr}")
    
    # 1. Test Range Sum
    st_sum = SegmentTree(arr, op='sum')
    assert st_sum.query(1, 3) == 15  # 3 + 5 + 7
    print(f"Sum query [1, 3] -> Expected: 15, Got: {st_sum.query(1, 3)}")
    
    # Add 2 to range [1, 3], array conceptually becomes: [1, 5, 7, 9, 9, 11]
    st_sum.update_range(1, 3, 2)
    new_sum = st_sum.query(1, 3)
    assert new_sum == 21  # 5 + 7 + 9
    print(f"Sum query [1, 3] after adding 2 to [1, 3] -> Expected: 21, Got: {new_sum}")
    
    # 2. Test Range Min
    st_min = SegmentTree(arr, op='min')
    assert st_min.query(2, 5) == 5  # min(5, 7, 9, 11)
    print(f"\nMin query [2, 5] -> Expected: 5, Got: {st_min.query(2, 5)}")
    
    # Subtract 10 from range [3, 4], array conceptually becomes: [1, 3, 5, -3, -1, 11]
    st_min.update_range(3, 4, -10)
    new_min = st_min.query(2, 5)
    assert new_min == -3
    print(f"Min query [2, 5] after subtracting 10 from [3, 4] -> Expected: -3, Got: {new_min}")

    print("\nAll tests passed successfully! 🚀")

"""
Interview Challenge:
--------------------
Problem: "Count Number of Inversions using a Segment Tree"
Given an array `arr`, an inversion is a pair `(i, j)` such that `i < j` and `arr[i] > arr[j]`.
How can you use a Segment Tree to count the number of inversions in an array of size N in O(N log MAX_VAL) time?

Hint: Start from the rightmost element. Use a Segment Tree representing frequencies of elements.
For each element X in the array, query the segment tree for the sum in range [0, X-1] to count 
how many elements strictly smaller than X have already been seen. Then, update the tree by 
adding 1 at index X. (Note: Coordinate compression is needed if MAX_VAL is very large).
"""
