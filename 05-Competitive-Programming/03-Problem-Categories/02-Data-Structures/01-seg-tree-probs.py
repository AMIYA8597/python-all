"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (SEGMENT TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of 100,000 integers. You need to answer 100,000 queries.
# A query asks: "What is the Sum (or Minimum) of all numbers between index L and R?"
# Interspersed with these queries, the user is modifying the array (e.g., `arr[4] = 99`).
#
# Naive Approach: A `for` loop from L to R takes $O(N)$ time. 100,000 queries 
# take $10^{10}$ operations (Time Limit Exceeded).
# Prefix Sum Approach: Prefix sums answer queries in $O(1)$ time! But if the 
# user modifies the array (`arr[4] = 99`), updating the prefix sum array takes 
# $O(N)$ time (Time Limit Exceeded).
#
# You must use a Segment Tree.
# A Segment Tree physically builds a Binary Tree over the array. It calculates 
# Range Queries in exactly $O(\log N)$ time, and updates elements in exactly 
# $O(\log N)$ time. It is the ultimate weapon for Range Query problems.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the recursive architecture of a Segment Tree (Divide & Conquer).
# - Implement the `build()`, `update()`, and `query()` functions.
# - Solve a Range Sum Query problem.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SEGMENT TREE ARCHITECTURE (RANGE SUM QUERY)
# ==============================================================================
class SegmentTree:
    """
    A 1-indexed Array-based Segment Tree for Range Sum Queries.
    Space Complexity: O(4 * N)
    Time Complexity: 
       Build: O(N)
       Query: O(log N)
       Update: O(log N)
    """
    def __init__(self, data: list[int]):
        self.n = len(data)
        # The tree requires roughly 4*N space to guarantee enough room 
        # for a perfectly balanced binary tree array structure.
        self.tree = [0] * (4 * self.n)
        
        # Build the tree mathematically. Node 1 is the Root.
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)
            
    def _build(self, data: list[int], node: int, left: int, right: int) -> None:
        """Recursively builds the Segment Tree (Bottom-Up)"""
        # Base Case: We hit a Leaf Node (A single element from the array)
        if left == right:
            self.tree[node] = data[left]
            return
            
        # Recursive Case: Divide the array segment exactly in half
        mid = (left + right) // 2
        left_child = 2 * node
        right_child = 2 * node + 1
        
        self._build(data, left_child, left, mid)
        self._build(data, right_child, mid + 1, right)
        
        # Backtracking: The parent is the SUM of its two children!
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
        
    def update(self, index: int, new_val: int) -> None:
        """Public method to update a single array element."""
        self._update(1, 0, self.n - 1, index, new_val)
        
    def _update(self, node: int, left: int, right: int, idx: int, new_val: int) -> None:
        """Recursively traverses down to the leaf, updates, and recalculates sums."""
        # Base Case: We found the exact leaf node!
        if left == right:
            self.tree[node] = new_val
            return
            
        # Determine which child holds the target index
        mid = (left + right) // 2
        left_child = 2 * node
        right_child = 2 * node + 1
        
        if idx <= mid:
            # Go left
            self._update(left_child, left, mid, idx, new_val)
        else:
            # Go right
            self._update(right_child, mid + 1, right, idx, new_val)
            
        # Backtracking: Recalculate the parent sum!
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query(self, query_l: int, query_r: int) -> int:
        """Public method to query the sum from index query_l to query_r."""
        return self._query(1, 0, self.n - 1, query_l, query_r)
        
    def _query(self, node: int, left: int, right: int, ql: int, qr: int) -> int:
        """
        Recursively fetches the sum.
        There are 3 mathematical states for node overlap:
        1. No Overlap -> Return 0
        2. Total Overlap -> Return the node's stored value instantly!
        3. Partial Overlap -> Split the query to both children and sum them.
        """
        # 1. No Overlap (This node's segment is completely outside the query)
        if right < ql or left > qr:
            return 0
            
        # 2. Total Overlap (This node's segment is completely INSIDE the query)
        # We DO NOT need to traverse down to the leaves! We return the pre-calculated sum!
        if ql <= left and right <= qr:
            return self.tree[node]
            
        # 3. Partial Overlap
        mid = (left + right) // 2
        left_sum = self._query(2 * node, left, mid, ql, qr)
        right_sum = self._query(2 * node + 1, mid + 1, right, ql, qr)
        
        return left_sum + right_sum

def demonstrate_segment_tree():
    section_header("Executing a Segment Tree")
    
    # Indices:    0  1  2  3  4  5
    arr =        [1, 3, 5, 7, 9, 11]
    
    print(f"Original Array: {arr}")
    
    # Build Tree: O(N)
    seg_tree = SegmentTree(arr)
    print("Segment Tree Successfully Built in O(N) time.")
    
    # Query: Sum from index 1 to 3 -> (3 + 5 + 7) = 15
    q_left, q_right = 1, 3
    result = seg_tree.query(q_left, q_right)
    print(f"\nQuery Sum [idx {q_left} to {q_right}]: {result} (Time: O(log N))")
    
    # Update: arr[2] becomes 10 (was 5)
    # The new array conceptually is [1, 3, 10, 7, 9, 11]
    update_idx = 2
    new_val = 10
    print(f"\nUpdating array index {update_idx} to value {new_val}...")
    seg_tree.update(update_idx, new_val) # O(log N)
    
    # Query again: Sum from index 1 to 3 -> (3 + 10 + 7) = 20
    result2 = seg_tree.query(q_left, q_right)
    print(f"Query Sum [idx {q_left} to {q_right}] after update: {result2} (Time: O(log N))")


def run_all_labs():
    demonstrate_segment_tree()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Segment Tree represented as a 1D Python Array require $4 \times N$ space?
   Answer: We map the Binary Tree directly into an array where a node at index `i` has its left child at `2*i` and its right child at `2*i + 1`. If the original array length $N$ is exactly a power of 2, the tree is a mathematically perfect binary tree requiring exactly $2N - 1$ nodes. However, if $N$ is *not* a perfect power of 2 (e.g., $N=5$), the leaf nodes are pushed down to an additional depth level. To ensure the physical array has enough index slots to accommodate these deeper, sparsely-filled right-side branches without throwing an `IndexError`, mathematics dictates that allocating exactly $4N$ space mathematically guarantees safety for any value of $N$.

2. Explain the "Total Overlap" condition in the Segment Tree `query` function and why it creates the $O(\log N)$ speed.
   Answer: The true power of a Segment Tree lies in bypassing leaf nodes. If you query the sum of elements from index 0 to 7, and the current tree node explicitly stores the pre-calculated sum of index 0 to 3, the `Total Overlap` logic `(ql <= left and right <= qr)` triggers. The algorithm instantly returns the pre-calculated sum for that entire massive block of data and *physically stops traversing down that branch*. By short-circuiting the recursion and utilizing pre-aggregated chunks, the algorithm never visits all $N$ leaves, reducing the search path to exactly $O(\log N)$.

3. How would you modify this Segment Tree to perform Range Minimum Queries (RMQ) instead of Range Sum Queries?
   Answer: The architectural skeleton (the recursive division and overlap logic) remains exactly the same. You only change the Backtracking aggregation logic and the "No Overlap" base case. 
   - During `build` and `update`, change `tree[node] = left_child + right_child` to `tree[node] = min(left_child, right_child)`.
   - During `query`, if the segment has "No Overlap", instead of returning `0` (which would corrupt a Minimum calculation if the array has positive numbers), you must return mathematical Infinity (`float('inf')`).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Segment Trees Completed.")
