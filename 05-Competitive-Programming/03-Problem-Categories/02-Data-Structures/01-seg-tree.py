"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (LAZY PROPAGATION SEGMENT TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Segment Tree answers Range Queries in O(log N) and updates a 
# SINGLE element in O(log N).
#
# But what if the user wants to update a massive RANGE of elements? 
# Example: "Add +5 to every element between index 0 and index 100,000."
#
# If you run the standard O(log N) point update 100,000 times in a loop, it 
# takes O(K * log N) time, which causes an instant Time Limit Exceeded (TLE).
#
# To execute a Range Update in exactly O(log N) time, you must use the most 
# advanced data structure concept in Competitive Programming: LAZY PROPAGATION.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of the Lazy Array.
# - Understand the mathematical concept of delaying updates.
# - Implement `range_update()` and `push_down()` functions.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LAZY PROPAGATION ARCHITECTURE (RANGE ADD QUERY)
# ==============================================================================
class LazySegmentTree:
    """
    Segment Tree for Range Sum Queries WITH Range Updates (Add to Range).
    Space Complexity: O(4*N) for Tree, O(4*N) for Lazy Array.
    """
    def __init__(self, data: list[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        
        # The Lazy Array acts as an I.O.U. notebook!
        self.lazy = [0] * (4 * self.n)
        
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)
            
    def _build(self, data: list[int], node: int, left: int, right: int):
        if left == right:
            self.tree[node] = data[left]
            return
        mid = (left + right) // 2
        self._build(data, 2 * node, left, mid)
        self._build(data, 2 * node + 1, mid + 1, right)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
        
    def _push_down(self, node: int, left: int, right: int):
        """
        If this node has a pending update (an I.O.U. in the lazy array),
        apply it physically to the tree now, and pass the I.O.U. to its children!
        """
        if self.lazy[node] != 0:
            # 1. Update the current node's physical value!
            # If we are adding +5 to a range of 4 elements, the total sum increases by 4 * 5 = 20.
            num_elements_in_range = right - left + 1
            self.tree[node] += self.lazy[node] * num_elements_in_range
            
            # 2. If it is NOT a leaf node, pass the I.O.U. down to the children!
            if left != right:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
                
            # 3. Clear the I.O.U. for the current node (debt paid!)
            self.lazy[node] = 0

    def update_range(self, ql: int, qr: int, add_val: int) -> None:
        """Public method to add `add_val` to all elements from index ql to qr."""
        self._update_range(1, 0, self.n - 1, ql, qr, add_val)
        
    def _update_range(self, node: int, left: int, right: int, ql: int, qr: int, add_val: int):
        # Always resolve pending lazy updates before processing this node
        self._push_down(node, left, right)
        
        # 1. No Overlap
        if right < ql or left > qr:
            return
            
        # 2. Total Overlap
        if ql <= left and right <= qr:
            # Add the I.O.U. to the lazy array!
            self.lazy[node] += add_val
            # Instantly push it down to apply it to the physical tree, 
            # and stop traversing downwards! (O(log N) magic!)
            self._push_down(node, left, right)
            return
            
        # 3. Partial Overlap
        mid = (left + right) // 2
        self._update_range(2 * node, left, mid, ql, qr, add_val)
        self._update_range(2 * node + 1, mid + 1, right, ql, qr, add_val)
        
        # Recalculate parent based on updated children
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, ql: int, qr: int) -> int:
        return self._query(1, 0, self.n - 1, ql, qr)
        
    def _query(self, node: int, left: int, right: int, ql: int, qr: int) -> int:
        # Always resolve pending lazy updates before querying!
        self._push_down(node, left, right)
        
        if right < ql or left > qr:
            return 0
            
        if ql <= left and right <= qr:
            return self.tree[node]
            
        mid = (left + right) // 2
        return self._query(2 * node, left, mid, ql, qr) + self._query(2 * node + 1, mid + 1, right, ql, qr)


def demonstrate_lazy_propagation():
    section_header("Segment Tree with Lazy Propagation")
    
    # Indices:    0  1  2  3  4  5
    arr =        [1, 3, 5, 7, 9, 11]
    print(f"Original Array: {arr}")
    
    seg_tree = LazySegmentTree(arr)
    
    print("\nExecuting RANGE Update: Adding +10 to indices 1 through 4...")
    # New logical array: [1, 13, 15, 17, 19, 11]
    seg_tree.update_range(1, 4, 10) # Executes in strictly O(log N) time!
    
    # Query index 2 to 5 -> (15 + 17 + 19 + 11) = 62
    q_left, q_right = 2, 5
    ans = seg_tree.query(q_left, q_right)
    
    print(f"Query Sum [idx {q_left} to {q_right}]: {ans}")
    print("\nBecause we used Lazy Propagation, we updated 4 elements in a single ")
    print("O(log N) pass instead of writing a slow O(N) loop!")


def run_all_labs():
    demonstrate_lazy_propagation()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the architectural concept of "Lazy Propagation". Why is a second array (`self.lazy`) required?
   Answer: In a Range Update, updating a massive block of 100,000 leaf nodes at the bottom of the tree mathematically requires $O(N)$ operations. To bypass this, we use the `lazy` array as an "I.O.U. notebook". When the algorithm identifies a node whose range is totally overlapped by the update (e.g., Node X represents indices 0-3), it writes the update command into `lazy[X]` and *physically halts traversal*. It refuses to update the leaf nodes until absolutely necessary. This short-circuit guarantees an $O(\log N)$ update time. 

2. In the `_push_down()` function for a Range Sum Segment Tree, why do we multiply `self.lazy[node] * num_elements_in_range` instead of just adding `self.lazy[node]`?
   Answer: A Segment Tree node represents the aggregated math of its children. If a Node represents the segment `[left=0, right=3]`, it covers exactly 4 elements. If the user commands an update to "Add +5 to all elements", the total internal Sum of that branch doesn't increase by 5; it increases by 5 for *every* element in the range. Therefore, the Node's sum must physically increase by $+5 \times 4 = +20$. If you forget to multiply by the length of the segment, the parent node's mathematical aggregation will be completely corrupted.

3. Why is it absolutely mandatory to call `self._push_down(node, left, right)` as the very first line of both the `_update_range()` and `_query()` functions?
   Answer: Because of the I.O.U. system! If you traverse down the tree to query the value of a specific leaf, but an ancestor node is holding a pending Lazy Update (debt) that was never resolved, the leaf node will return stale, outdated mathematical data. By calling `_push_down()` at the absolute top of the recursive function, the algorithm mathematically guarantees that it resolves its local debt and pushes the I.O.U. down to its children *before* calculating any overlaps or returning values, ensuring 100% data consistency.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Lazy Propagation Segment Trees Completed.")
