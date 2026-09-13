"""
# ==============================================================================
# LABORATORY: SEGMENT TREES (RANGE QUERIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine you have an array of 100,000 numbers and you constantly need to find 
# the SUM (or MIN or MAX) of elements between index L and index R.
# If you iterate `sum(arr[L:R])`, it takes O(N) time per query. Too slow.
# If you precompute a Prefix Sum array, queries take O(1) time! BUT, if you 
# modify a single element in the original array, updating the Prefix Sum array 
# takes O(N) time.
# A Segment Tree solves this by achieving O(log N) for BOTH updates AND queries. 
# It is heavily used in computational geometry and competitive programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Segment Tree (Implicit Array implementation).
# - Build the Tree recursively in O(N) time.
# - Perform Point Updates in O(log N) time.
# - Perform Range Queries in O(log N) time.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SEGMENT TREE IMPLEMENTATION (SUM QUERIES)
# ==============================================================================
class SegmentTree:
    """
    LeetCode #307: Range Sum Query - Mutable
    Like a Heap, a Segment Tree is a Complete Binary Tree. 
    Therefore, we can store it in a 1D array where:
    - Left Child = 2 * i + 1
    - Right Child = 2 * i + 2
    """
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        # The maximum size of a segment tree array is roughly 4 * N
        self.tree = [0] * (4 * self.n)
        
        if self.n > 0:
            self._build_tree(nums, 0, 0, self.n - 1)
            
    def _build_tree(self, nums: List[int], tree_index: int, left: int, right: int):
        """Recursively builds the tree in O(N) time."""
        # Base case: Leaf node (represents a single element from the original array)
        if left == right:
            self.tree[tree_index] = nums[left]
            return
            
        mid = left + (right - left) // 2
        left_child = 2 * tree_index + 1
        right_child = 2 * tree_index + 2
        
        # Recursively build the left and right subtrees
        self._build_tree(nums, left_child, left, mid)
        self._build_tree(nums, right_child, mid + 1, right)
        
        # The current node's value is the SUM of its two children!
        # (Change to `min()` or `max()` depending on the problem)
        self.tree[tree_index] = self.tree[left_child] + self.tree[right_child]

    def update(self, index: int, val: int) -> None:
        """Updates a specific index in the original array to a new value (O(log N))."""
        self._update_recursive(0, 0, self.n - 1, index, val)
        
    def _update_recursive(self, tree_index: int, left: int, right: int, target_idx: int, val: int):
        # Base case: We found the exact leaf node for the target index
        if left == right:
            self.tree[tree_index] = val
            return
            
        mid = left + (right - left) // 2
        left_child = 2 * tree_index + 1
        right_child = 2 * tree_index + 2
        
        # Determine which subtree the target index falls into
        if target_idx <= mid:
            self._update_recursive(left_child, left, mid, target_idx, val)
        else:
            self._update_recursive(right_child, mid + 1, right, target_idx, val)
            
        # As we return up the call stack, we must update the sums of the parents
        self.tree[tree_index] = self.tree[left_child] + self.tree[right_child]

    def sum_range(self, L: int, R: int) -> int:
        """Queries the sum between index L and index R inclusive (O(log N))."""
        return self._query_recursive(0, 0, self.n - 1, L, R)
        
    def _query_recursive(self, tree_index: int, left: int, right: int, qL: int, qR: int) -> int:
        """
        left, right = The range that THIS NODE represents.
        qL, qR      = The range that the USER is querying for.
        """
        # Case 1: Total Overlap. The node's range is COMPLETELY inside the query range.
        if qL <= left and qR >= right:
            # We can return this node's precomputed sum immediately! No need to traverse deeper.
            return self.tree[tree_index]
            
        # Case 2: No Overlap. The node's range is completely outside the query range.
        if qL > right or qR < left:
            return 0
            
        # Case 3: Partial Overlap. We must look at both children and combine their results.
        mid = left + (right - left) // 2
        left_sum = self._query_recursive(2 * tree_index + 1, left, mid, qL, qR)
        right_sum = self._query_recursive(2 * tree_index + 2, mid + 1, right, qL, qR)
        
        return left_sum + right_sum

def demonstrate_segment_tree():
    section_header("Segment Tree: Range Sum Queries")
    
    nums = [1, 3, 5, 7, 9, 11]
    print(f"Original Array: {nums}")
    
    # 1. Build the tree
    st = SegmentTree(nums)
    print("Tree built successfully.")
    
    # 2. Range Query
    print(f"\nQuerying Sum from index 1 to 3: sum([3, 5, 7])")
    print(f"Result: {st.sum_range(1, 3)} (Expected: 15)")
    
    # 3. Point Update
    print("\nUpdating index 2 (value 5) to value 10...")
    st.update(2, 10)
    # The array is conceptually now: [1, 3, 10, 7, 9, 11]
    
    # 4. Range Query Again
    print(f"Querying Sum from index 1 to 3 again:")
    print(f"Result: {st.sum_range(1, 3)} (Expected: 3 + 10 + 7 = 20)")
    
    print("\nNotice that updating the value instantly updated the parent nodes in O(log N) time!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why not just use a Prefix Sum array?
   Answer: A Prefix Sum array achieves O(1) queries, but if you change a single value at index 0, you have to recalculate the prefix sums for EVERY subsequent element, which takes O(N) time. Segment Trees balance this out, achieving O(log N) for both queries and updates.

2. How large does the Segment Tree array need to be?
   Answer: The mathematical upper bound for a Segment Tree array is exactly `4 * N` where N is the length of the input array.

3. How does the Range Query achieve O(log N) time?
   Answer: When the tree recursively checks a node, if that node's range falls COMPLETELY within the user's query range, it returns its precomputed value immediately. It does NOT traverse down to the leaves. This drastically prunes the search space.
"""

if __name__ == "__main__":
    demonstrate_segment_tree()
    print("\n[SUCCESS] Laboratory: Segment Trees Completed.")
