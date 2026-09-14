"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (PERSISTENT SEGMENT TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of 100,000 numbers.
# You perform 100,000 updates to this array over time.
#
# Suddenly, the user queries: "What was the sum of elements from index L to R... 
# EXACTLY AT UPDATE NUMBER 5,000?"
#
# A standard Segment Tree overwrites its data during an update. It has amnesia.
# If you tried to save a deep copy of the entire Segment Tree after every 
# single update, it would take O(N) time and space per copy. 100,000 * 100,000 
# equals 10 Billion operations and 100 GB of RAM (MLE / TLE).
#
# A Persistent Segment Tree solves this. When an update occurs, it does NOT 
# mutate the existing tree. Instead, it creates a NEW root node and only 
# duplicates the O(log N) nodes on the physical path down to the updated leaf!
# The rest of the new tree mathematically points to the branches of the OLD tree!
#
# This "Path Copying" allows you to store all 100,000 historical versions of the 
# entire tree in exactly O(N log N) space, achieving Time-Travel in O(log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Path Copying and structural sharing.
# - Build a Persistent Segment Tree.
# - Execute Time-Travel queries on historical versions.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PERSISTENT SEGMENT TREE (TIME-TRAVEL ARRAY)
# ==============================================================================
class Node:
    """A Node in a Persistent Segment Tree. Notice it uses explicit Left/Right pointers, 
    not array arithmetic (2i, 2i+1), because the tree is not a perfect array anymore!"""
    def __init__(self, value: int, left_child=None, right_child=None):
        self.value = value
        self.left = left_child
        self.right = right_child

class PersistentSegmentTree:
    def __init__(self, arr: list[int]):
        self.n = len(arr)
        # Store the Roots of all historical versions!
        # versions[0] = The root of the original array.
        # versions[1] = The root of the array after Update 1.
        self.versions = []
        
        # Build the initial version (Version 0)
        root_v0 = self._build(arr, 0, self.n - 1)
        self.versions.append(root_v0)

    def _build(self, arr: list[int], start: int, end: int) -> Node:
        """Standard Segment Tree build."""
        if start == end:
            return Node(arr[start])
            
        mid = (start + end) // 2
        left_child = self._build(arr, start, mid)
        right_child = self._build(arr, mid + 1, end)
        
        return Node(left_child.value + right_child.value, left_child, right_child)

    def update(self, index: int, new_val: int) -> int:
        """
        Updates the array and returns the ID of the new historical version.
        Time Complexity: O(log N)
        Space Complexity: O(log N) new nodes created.
        """
        # We base the new update entirely on the MOST RECENT version!
        latest_root = self.versions[-1]
        
        # Path Copying!
        new_root = self._update_recursive(latest_root, 0, self.n - 1, index, new_val)
        
        self.versions.append(new_root)
        return len(self.versions) - 1 # The Version ID

    def _update_recursive(self, node: Node, start: int, end: int, target_idx: int, new_val: int) -> Node:
        """
        Creates new nodes ONLY for the path leading to the target index.
        Reuses existing pointers for unchanged branches!
        """
        if start == end:
            # We reached the leaf! Create a brand new Node with the new value.
            return Node(new_val)
            
        mid = (start + end) // 2
        
        if target_idx <= mid:
            # The update is in the LEFT branch.
            # We must recursively path-copy the left branch.
            new_left = self._update_recursive(node.left, start, mid, target_idx, new_val)
            
            # The RIGHT branch is completely unaffected! 
            # We mathematically point our new node's right child to the OLD node's right child!
            new_right = node.right
        else:
            # The update is in the RIGHT branch.
            # We point our new node's left child to the OLD node's left child!
            new_left = node.left
            
            # We recursively path-copy the right branch.
            new_right = self._update_recursive(node.right, mid + 1, end, target_idx, new_val)
            
        # Create a brand new Parent Node linking the branches!
        return Node(new_left.value + new_right.value, new_left, new_right)

    def query(self, version_id: int, l: int, r: int) -> int:
        """
        Time-Travel Query! Queries a specific historical version in O(log N) time.
        """
        if version_id < 0 or version_id >= len(self.versions):
            raise ValueError("Invalid Version ID")
            
        target_root = self.versions[version_id]
        return self._query_recursive(target_root, 0, self.n - 1, l, r)

    def _query_recursive(self, node: Node, start: int, end: int, l: int, r: int) -> int:
        # Standard Segment Tree query logic
        if l > end or r < start:
            return 0
        if l <= start and end <= r:
            return node.value
            
        mid = (start + end) // 2
        left_sum = self._query_recursive(node.left, start, mid, l, r)
        right_sum = self._query_recursive(node.right, mid + 1, end, l, r)
        
        return left_sum + right_sum

def demonstrate_persistent_seg_tree():
    section_header("Persistent Segment Tree (Time Travel)")
    
    arr = [1, 2, 3, 4, 5]
    print(f"Original Array (Version 0): {arr}")
    
    pst = PersistentSegmentTree(arr)
    
    print("\nUpdating Index 2 from '3' to '10'...")
    v1 = pst.update(2, 10)
    print(f"Update completed. New timeline created: Version {v1}")
    
    print("Updating Index 0 from '1' to '100'...")
    v2 = pst.update(0, 100)
    print(f"Update completed. New timeline created: Version {v2}")
    
    print("\nTime-Travel Queries!")
    
    ans0 = pst.query(0, 0, 4)
    print(f"Sum of [0..4] in Version 0 (Original) : {ans0}  (Expected: 1+2+3+4+5 = 15)")
    
    ans1 = pst.query(1, 0, 4)
    print(f"Sum of [0..4] in Version 1 (idx2=10): {ans1}  (Expected: 1+2+10+4+5 = 22)")
    
    ans2 = pst.query(2, 0, 4)
    print(f"Sum of [0..4] in Version 2 (idx0=100): {ans2} (Expected: 100+2+10+4+5 = 121)")
    
    print("\nThe Tree perfectly preserved all realities using $O(\\log N)$ memory per update!")


def run_all_labs():
    demonstrate_persistent_seg_tree()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Persistent Segment Tree abandon the traditional `2*i` and `2*i + 1` array-based architecture for Nodes with physical `left` and `right` pointers?
   Answer: In a traditional array-based Segment Tree, the physical structure of the tree is permanently locked into a single contiguous block of memory (e.g., indices 1 to $4N$). If you want to create a "new" root node for Version 1, where would you put it in the array? The array is already full of Version 0! Persistent Segment Trees are mathematically asymmetrical; Version 1 might share its entire left branch with Version 0, but have a completely unique right branch. Because the tree is constantly splicing and re-wiring branches across different historical timelines, it is impossible to map it to a rigid flat array. It strictly requires dynamic memory allocation using independent Nodes with explicit pointers.

2. Explain the mechanism of "Path Copying". Why does updating a leaf node require copying $\log_2(N)$ nodes instead of just 1?
   Answer: If you only created a new leaf node and pointed the old parent to it, you would irreversibly mutate the old parent! Version 0 would suddenly see the new leaf, destroying the historical timeline. To mathematically protect Version 0, the Parent must remain untouched. Therefore, to connect our new leaf, we must create a *brand new Parent*. But if we create a new Parent, we must create a *brand new Grandparent* to connect to it! This chain reaction propagates all the way up the tree until we are forced to create a *brand new Root*. Because the height of the tree is exactly $\log_2(N)$, we must create exactly $\log_2(N)$ new nodes to safely insulate the new timeline from the old timeline!

3. In the `_update_recursive` function, what is the mathematical significance of the line `new_right = node.right` when the target index is in the left branch?
   Answer: Structural Sharing! This is the core magic of the Persistent Segment Tree. We determined that the update strictly occurred in the left branch. Therefore, the entire right branch of the tree is mathematically unchanged! Instead of traversing down the right branch and wasting CPU cycles copying thousands of unchanged nodes, we simply copy the *pointer*! Our brand new Parent node mathematically points its right child directly into the depths of Version 0's untouched right branch! This $O(1)$ pointer assignment effortlessly carries over $O(N)$ historical data into the new timeline, achieving the $O(\log N)$ space complexity.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (Persistent Seg Tree) Completed.")
