"""
=============================================================================
Python DSA AI Master - Textbook Grade Lesson: Segment Trees
=============================================================================

## 1. Introduction and Mathematical Background

A Segment Tree is a remarkably versatile data structure primarily used for 
answering range queries and making array updates in logarithmic time. 
While standard arrays give O(1) element access, querying properties of a 
range (like sum, min, max) takes O(N) time. Conversely, a prefix sum array 
can answer range sum queries in O(1) time but requires O(N) time to update 
a single element. 

The Segment Tree provides a beautiful compromise:
- **Range Query:** O(log N)
- **Point / Range Update:** O(log N)

### 1.1 The Divide-and-Conquer Paradigm
At its core, a Segment Tree is a strictly binary tree where each node represents
an interval `[L, R]` of the array.
- The **root** represents the entire array `[0, N-1]`.
- Every **leaf** node represents a single element `[i, i]`.
- Every **internal node** represents the union of its children's intervals. 
  Specifically, if a node represents `[L, R]`, its left child represents 
  `[L, M]` and its right child represents `[M+1, R]`, where `M = (L+R)//2`.

### 1.2 Mathematical Size Bound
Why is the segment tree array of size 4N? 
Suppose the array size is N. The segment tree is a full binary tree (every 
node has 0 or 2 children).
The number of leaves is exactly N.
A full binary tree with N leaves has N-1 internal nodes, making it 2N-1 
nodes in total.
However, because we represent the tree implicitly in an array (like a heap, 
where left child is `2*i+1` and right child is `2*i+2`), the maximum depth 
of the tree is bounded by `ceil(log2(N)) + 1`. 
The maximum number of nodes in a perfectly balanced binary tree of that depth 
is `2^(ceil(log2(N))+1) - 1`. 
In the worst case (e.g., N is slightly greater than a power of 2, say N=9), 
the lowest level could extend such that the array size reaches almost 4N.
Thus, allocating `4 * N` memory guarantees no index out of bounds.

## 2. Real-World Applications and AI Connections
- **Competitive Programming:** Heavily used for dynamic range queries.
- **Computational Geometry:** Finding intersecting line segments, sweep-line algorithms.
- **Machine Learning & AI (Reinforcement Learning):** "Sum Trees", a variant 
  of Segment Trees, are the backbone of **Prioritized Experience Replay (PER)**. 
  In PER, an agent replays important transitions more frequently. A segment tree 
  allows O(log N) updates to the priorities (when TD errors change) and O(log N) 
  sampling proportional to the priority sum.
- **Databases and Streaming:** Maintaining running statistics, quantiles, and
  aggregates over sliding windows.

## 3. Complexity Analysis
Let N be the number of elements in the array.
- **Time Complexity:**
  - Build: `O(N)` since there are `2N-1` nodes and each takes O(1) to evaluate.
  - Range Query: `O(log N)` since at most 4 nodes are visited per level of the tree.
  - Point Update: `O(log N)` since the path from root to leaf has length `O(log N)`.
  - Lazy Range Update (in advanced variations): `O(log N)`.
- **Space/Memory Complexity:**
  - `O(N)` conceptually, strictly bounded by an array of size `4 * N`.

=============================================================================
"""

import math
from typing import List, Callable, TypeVar, Generic, Optional

# Type variable for generics allowing segment tree to work with int, float, etc.
T = TypeVar('T')

class SegmentTree(Generic[T]):
    """
    A textbook implementation of a Generic Segment Tree supporting point updates
    and range queries. By default, it performs Range Sum Queries, but you can 
    inject any associative combining function (e.g., min, max, gcd, bitwise OR).
    """

    def __init__(self, data: List[T], default_val: T, combine_fn: Callable[[T, T], T]):
        """
        Initializes the segment tree.
        
        Args:
            data (List[T]): The input array from which the segment tree is built.
            default_val (T): The identity value for the combine function. 
                             E.g., 0 for sum, infinity for min, -infinity for max.
            combine_fn (Callable[[T, T], T]): A function to combine two nodes.
                                              Must be associative.
        """
        self.n = len(data)
        self.default_val = default_val
        self.combine_fn = combine_fn
        
        # In a 0-indexed array representation of a binary tree:
        # Node v has left child 2*v + 1 and right child 2*v + 2
        # A size of 4 * N is safe for implicit tree storage.
        if self.n > 0:
            self.tree: List[T] = [self.default_val] * (4 * self.n)
            self._build(data, 0, 0, self.n - 1)
        else:
            self.tree: List[T] = []

    def _build(self, data: List[T], v: int, tl: int, tr: int) -> None:
        """
        Recursively builds the segment tree bottom-up.
        
        Args:
            data (List[T]): Original data array.
            v (int): Current node index in the segment tree array.
            tl (int): Left boundary of the segment managed by node v.
            tr (int): Right boundary of the segment managed by node v.
        """
        # Base case: Leaf node. The segment is exactly one element.
        if tl == tr:
            self.tree[v] = data[tl]
        else:
            # Recursive case: Divide the segment into two halves.
            tm = (tl + tr) // 2
            
            # Build the left child
            self._build(data, v * 2 + 1, tl, tm)
            
            # Build the right child
            self._build(data, v * 2 + 2, tm + 1, tr)
            
            # Merge the results from the left and right children
            self.tree[v] = self.combine_fn(self.tree[v * 2 + 1], self.tree[v * 2 + 2])

    def _query(self, v: int, tl: int, tr: int, l: int, r: int) -> T:
        """
        Recursively searches the segment tree to answer a range query.
        
        Args:
            v (int): Current node index.
            tl (int): Left boundary of the current node's segment.
            tr (int): Right boundary of the current node's segment.
            l (int): Left boundary of the query range.
            r (int): Right boundary of the query range.
            
        Returns:
            T: The aggregated result for the query range.
        """
        # Case 1: The query range is totally invalid or completely disjoint
        if l > r:
            return self.default_val
            
        # Case 2: The current node's segment matches the query range perfectly
        if l == tl and r == tr:
            return self.tree[v]
            
        # Case 3: Partial overlap. We must query both children and combine.
        tm = (tl + tr) // 2
        
        # When querying the left child, the query boundary is restricted by `tm`
        left_res = self._query(v * 2 + 1, tl, tm, l, min(r, tm))
        
        # When querying the right child, the query boundary starts at least at `tm + 1`
        right_res = self._query(v * 2 + 2, tm + 1, tr, max(l, tm + 1), r)
        
        return self.combine_fn(left_res, right_res)

    def _update(self, v: int, tl: int, tr: int, pos: int, new_val: T) -> None:
        """
        Recursively updates a single element and propagates the change upwards.
        
        Args:
            v (int): Current node index.
            tl (int): Left boundary of the current node's segment.
            tr (int): Right boundary of the current node's segment.
            pos (int): The index in the original array that is being updated.
            new_val (T): The new value for the element at index `pos`.
        """
        # Base case: Found the exact leaf node for the element.
        if tl == tr:
            self.tree[v] = new_val
        else:
            tm = (tl + tr) // 2
            # Determine which child contains the `pos` index
            if pos <= tm:
                self._update(v * 2 + 1, tl, tm, pos, new_val)
            else:
                self._update(v * 2 + 2, tm + 1, tr, pos, new_val)
                
            # After updating the child, recompute this node's value
            self.tree[v] = self.combine_fn(self.tree[v * 2 + 1], self.tree[v * 2 + 2])

    def range_query(self, l: int, r: int) -> T:
        """
        Public interface for querying the range [l, r] (0-indexed, inclusive).
        
        Args:
            l (int): Starting index of the query.
            r (int): Ending index of the query.
            
        Returns:
            T: The combined result for the specified range.
            
        Raises:
            ValueError: If the query range is out of bounds.
        """
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid query range: [{l}, {r}] for array of size {self.n}")
        return self._query(0, 0, self.n - 1, l, r)

    def point_update(self, pos: int, new_val: T) -> None:
        """
        Public interface for updating a single element at index `pos`.
        
        Args:
            pos (int): The index to update.
            new_val (T): The new value to place at `pos`.
            
        Raises:
            ValueError: If the position is out of bounds.
        """
        if pos < 0 or pos >= self.n:
            raise ValueError(f"Invalid update position: {pos} for array of size {self.n}")
        self._update(0, 0, self.n - 1, pos, new_val)


class LazySegmentTree(Generic[T]):
    """
    An advanced textbook implementation of a Lazy Segment Tree.
    This variant supports RANGE UPDATES (e.g., add X to all elements in [L, R]) 
    in O(log N) time, by deferring updates to children using a 'lazy' array.
    """
    
    def __init__(self, data: List[int]):
        """
        Initializes a Range-Sum Lazy Segment tree.
        (For simplicity, specifically implemented for Range Add and Range Sum).
        
        Args:
            data (List[int]): The initial data array.
        """
        self.n = len(data)
        if self.n > 0:
            self.tree: List[int] = [0] * (4 * self.n)
            # The lazy array stores pending updates for the children of a node
            self.lazy: List[int] = [0] * (4 * self.n)
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], v: int, tl: int, tr: int) -> None:
        if tl == tr:
            self.tree[v] = data[tl]
        else:
            tm = (tl + tr) // 2
            self._build(data, v * 2 + 1, tl, tm)
            self._build(data, v * 2 + 2, tm + 1, tr)
            self.tree[v] = self.tree[v * 2 + 1] + self.tree[v * 2 + 2]

    def _push(self, v: int, tl: int, tr: int) -> None:
        """
        Propagates the pending lazy update to the children nodes.
        
        Args:
            v (int): The parent node index.
            tl (int): Left bound of parent's segment.
            tr (int): Right bound of parent's segment.
        """
        if self.lazy[v] != 0:
            tm = (tl + tr) // 2
            
            # Propagate to left child
            self.lazy[v * 2 + 1] += self.lazy[v]
            # Since the left child covers (tm - tl + 1) elements, its sum increases proportionally
            self.tree[v * 2 + 1] += self.lazy[v] * (tm - tl + 1)
            
            # Propagate to right child
            self.lazy[v * 2 + 2] += self.lazy[v]
            # The right child covers (tr - tm) elements
            self.tree[v * 2 + 2] += self.lazy[v] * (tr - tm)
            
            # Clear the lazy value for the parent, as it has been pushed down
            self.lazy[v] = 0

    def _range_update(self, v: int, tl: int, tr: int, l: int, r: int, addend: int) -> None:
        """
        Recursively adds a value `addend` to the range [l, r].
        """
        if l > r:
            return
            
        if l == tl and r == tr:
            # We found the exact segment covering the update range.
            self.tree[v] += addend * (tr - tl + 1)
            self.lazy[v] += addend
        else:
            # Push pending updates down before branching
            self._push(v, tl, tr)
            tm = (tl + tr) // 2
            
            self._range_update(v * 2 + 1, tl, tm, l, min(r, tm), addend)
            self._range_update(v * 2 + 2, tm + 1, tr, max(l, tm + 1), r, addend)
            
            # Recompute current node's value based on updated children
            self.tree[v] = self.tree[v * 2 + 1] + self.tree[v * 2 + 2]

    def _query(self, v: int, tl: int, tr: int, l: int, r: int) -> int:
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.tree[v]
            
        # Before returning children values, we must ensure they are up to date!
        self._push(v, tl, tr)
        
        tm = (tl + tr) // 2
        left_res = self._query(v * 2 + 1, tl, tm, l, min(r, tm))
        right_res = self._query(v * 2 + 2, tm + 1, tr, max(l, tm + 1), r)
        
        return left_res + right_res

    def range_update(self, l: int, r: int, addend: int) -> None:
        """
        Public API to add `addend` to all elements in range [l, r].
        """
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid update range: [{l}, {r}]")
        self._range_update(0, 0, self.n - 1, l, r, addend)

    def range_query(self, l: int, r: int) -> int:
        """
        Public API to query the sum in the range [l, r].
        """
        if l < 0 or r >= self.n or l > r:
            raise ValueError(f"Invalid query range: [{l}, {r}]")
        return self._query(0, 0, self.n - 1, l, r)


# =====================================================================
# Unit Tests & Real World Demonstration
# =====================================================================

def run_demonstration():
    print("="*60)
    print("Python DSA Master - Segment Tree Demonstration")
    print("="*60)
    
    # ---------------------------------------------------------
    # Scenario 1: Basic Range Sum
    # ---------------------------------------------------------
    print("\n[Scenario 1] Standard Range Sum Queries")
    arr = [1, 3, 5, 7, 9, 11]
    print(f"Original Array: {arr}")
    
    # Using lambda for addition, default value 0
    st_sum = SegmentTree(arr, default_val=0, combine_fn=lambda a, b: a + b)
    
    res1 = st_sum.range_query(1, 3)
    print(f"-> Sum of range [1, 3] (elements 3, 5, 7): {res1} (Expected 15)")
    assert res1 == 15, "Test failed!"
    
    print("-> Updating index 2 to value 6 (arr[2] = 6)")
    st_sum.point_update(2, 6)
    
    res2 = st_sum.range_query(1, 3)
    print(f"-> Sum of range [1, 3] after update (elements 3, 6, 7): {res2} (Expected 16)")
    assert res2 == 16, "Test failed!"
    
    
    # ---------------------------------------------------------
    # Scenario 2: Range Minimum Query (RMQ)
    # ---------------------------------------------------------
    print("\n[Scenario 2] Range Minimum Queries (RMQ)")
    arr_min = [8, 2, 9, 3, 1, 5, 7]
    print(f"Original Array: {arr_min}")
    
    # Using lambda for minimum, default value infinity
    st_min = SegmentTree(arr_min, default_val=float('inf'), combine_fn=lambda a, b: min(a, b))
    
    res3 = st_min.range_query(0, 3)
    print(f"-> Min of range [0, 3] (elements 8, 2, 9, 3): {res3} (Expected 2)")
    assert res3 == 2, "Test failed!"
    
    print("-> Updating index 1 to value 10")
    st_min.point_update(1, 10)
    
    res4 = st_min.range_query(0, 3)
    print(f"-> Min of range [0, 3] after update (elements 8, 10, 9, 3): {res4} (Expected 3)")
    assert res4 == 3, "Test failed!"


    # ---------------------------------------------------------
    # Scenario 3: Lazy Propagation (Range Updates)
    # ---------------------------------------------------------
    print("\n[Scenario 3] Lazy Propagation (Range Add, Range Sum)")
    arr_lazy = [0, 0, 0, 0, 0]
    print(f"Original Array: {arr_lazy}")
    
    lazy_st = LazySegmentTree(arr_lazy)
    
    print("-> Adding 5 to range [1, 3]...")
    lazy_st.range_update(1, 3, 5)
    # Conceptual Array: [0, 5, 5, 5, 0]
    
    res5 = lazy_st.range_query(0, 4)
    print(f"-> Sum of entire array: {res5} (Expected 15)")
    assert res5 == 15, "Test failed!"
    
    print("-> Adding 2 to range [2, 4]...")
    lazy_st.range_update(2, 4, 2)
    # Conceptual Array: [0, 5, 7, 7, 2]
    
    res6 = lazy_st.range_query(2, 3)
    print(f"-> Sum of range [2, 3]: {res6} (Expected 14)")
    assert res6 == 14, "Test failed!"

    print("\nAll textbook tests passed successfully!")
    print("="*60)

if __name__ == "__main__":
    run_demonstration()
