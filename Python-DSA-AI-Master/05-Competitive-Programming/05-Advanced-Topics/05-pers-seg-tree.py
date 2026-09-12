"""
Persistent Segment Tree

1. Introduction
---------------
A Persistent Segment Tree is a data structure that keeps the historical versions of a
segment tree after every update. Instead of modifying nodes in place, we create new nodes
for the paths that change. Because a single point update in a segment tree only modifies
O(log N) nodes, we can reuse the unmodified subtrees from the previous version.
This allows querying any previous state of the tree in O(log N) time.

2. Learning Objectives
----------------------
- Understand the concept of pointer-based segment trees and immutability.
- Learn how path copying enables O(log N) time and space updates.
- Solve classical problems like querying the K-th smallest element in a range [L, R].

3. Concept Explanation
----------------------
- A standard segment tree array representation isn't suitable here. We use node objects
  with `left` and `right` pointers.
- Upon an update, instead of traversing and modifying, the recursive function returns a
  *new* node that copies the child pointers of the old node, modifying only the path to
  the updated leaf.
- We maintain an array of `roots`, where `roots[i]` points to the root of the tree at
  version `i`.

4. Real-world / Industry Use Cases
----------------------------------
- Databases: Multi-Version Concurrency Control (MVCC) uses similar immutable historical 
  trees to allow lock-free reads while writes occur.
- Git / VCS: Git commits are immutable snapshots sharing references to unmodified tree structures.

5. Complexity
-------------
- Time Complexity: O(log N) per update, O(log N) per query.
- Space Complexity: O(N + U log N), where U is the number of updates.
"""

from typing import List, Optional

class Node:
    """A Node in the Persistent Segment Tree."""
    __slots__ = ['val', 'left', 'right']
    
    def __init__(self, val: int = 0, left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.val = val
        self.left = left
        self.right = right


class PersistentSegmentTree:
    """
    A Persistent Segment Tree for Range Sum Queries.
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.versions = [] # stores the root of each version
        if self.n > 0:
            root = self._build(arr, 0, self.n - 1)
            self.versions.append(root)
            
    def _build(self, arr: List[int], start: int, end: int) -> Node:
        """Build the initial segment tree (Version 0)."""
        if start == end:
            return Node(val=arr[start])
            
        mid = (start + end) // 2
        left_child = self._build(arr, start, mid)
        right_child = self._build(arr, mid + 1, end)
        return Node(val=left_child.val + right_child.val, left=left_child, right=right_child)

    def _update(self, prev_node: Optional[Node], start: int, end: int, idx: int, diff: int) -> Node:
        """
        Returns a new node representing the updated segment.
        Shares pointers to unmodified subtrees.
        """
        # Create a new node. Copy the value from prev_node (if it exists)
        new_node = Node(val=prev_node.val if prev_node else 0)
        
        if start == end:
            new_node.val += diff
            return new_node
            
        mid = (start + end) // 2
        
        # Copy child pointers
        new_node.left = prev_node.left if prev_node else None
        new_node.right = prev_node.right if prev_node else None
        
        if idx <= mid:
            new_node.left = self._update(new_node.left, start, mid, idx, diff)
        else:
            new_node.right = self._update(new_node.right, mid + 1, end, idx, diff)
            
        # Recompute value
        left_val = new_node.left.val if new_node.left else 0
        right_val = new_node.right.val if new_node.right else 0
        new_node.val = left_val + right_val
        
        return new_node

    def update(self, idx: int, diff: int) -> int:
        """
        Apply a point update (adding `diff` to `idx`), creating a new version.
        Returns the new version index.
        """
        prev_root = self.versions[-1]
        new_root = self._update(prev_root, 0, self.n - 1, idx, diff)
        self.versions.append(new_root)
        return len(self.versions) - 1

    def _query(self, node: Optional[Node], start: int, end: int, l: int, r: int) -> int:
        """Recursive range sum query on a specific tree version."""
        if node is None or start > r or end < l:
            return 0
        if start >= l and end <= r:
            return node.val
            
        mid = (start + end) // 2
        left_sum = self._query(node.left, start, mid, l, r)
        right_sum = self._query(node.right, mid + 1, end, l, r)
        return left_sum + right_sum

    def query(self, version: int, l: int, r: int) -> int:
        """
        Query the sum in range [l, r] at a specific historical `version`.
        """
        if version < 0 or version >= len(self.versions):
            raise ValueError(f"Version {version} does not exist.")
        root = self.versions[version]
        return self._query(root, 0, self.n - 1, l, r)


# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. In-place modification: Accidentally changing `prev_node.val` instead of creating `new_node`.
#    This destroys persistence and mutates historical states.
# 2. Memory Overhead: In languages like Python, creating O(log N) objects per update can cause
#    memory pressure and GC pauses. Pre-allocating a large array of objects and using integer
#    indices as pointers is often faster for competitive programming.

# ==========================================
# Interview Challenge / Exercise
# ==========================================
# Q: How can a persistent segment tree be used to find the K-th smallest element in a range [L, R]?
# A: Map array elements to their ranks. Create an empty tree (all 0s). Iteratively insert elements
#    from index 0 to N-1, creating N versions. Now, `versions[R] - versions[L-1]` (conceptually) 
#    represents the frequency of elements in [L, R]. We can binary search down this difference tree 
#    to find the K-th smallest in O(log N).


if __name__ == "__main__":
    print("Testing Persistent Segment Tree...")
    arr = [1, 2, 3, 4, 5]
    pst = PersistentSegmentTree(arr)
    
    # Version 0: [1, 2, 3, 4, 5]
    print(f"Version 0, Query(1, 3): {pst.query(0, 1, 3)}") # 2+3+4 = 9
    assert pst.query(0, 1, 3) == 9
    
    # Update index 2 by adding 10.
    # Version 1: [1, 2, 13, 4, 5]
    v1 = pst.update(2, 10)
    print(f"Version {v1}, Query(1, 3): {pst.query(v1, 1, 3)}") # 2+13+4 = 19
    assert pst.query(v1, 1, 3) == 19
    
    # Update index 4 by adding 5.
    # Version 2: [1, 2, 13, 4, 10]
    v2 = pst.update(4, 5)
    print(f"Version {v2}, Query(1, 4): {pst.query(v2, 1, 4)}") # 2+13+4+10 = 29
    assert pst.query(v2, 1, 4) == 29
    
    # Validate historical data
    print(f"Historical check: Version 0, Query(1, 3): {pst.query(0, 1, 3)}") # Still 9
    assert pst.query(0, 1, 3) == 9
    
    print("All tests passed!")
