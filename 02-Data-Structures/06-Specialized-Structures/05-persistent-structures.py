"""
# ==============================================================================
# LABORATORY: PERSISTENT DATA STRUCTURES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When you update an array `arr[5] = 99`, the old value is destroyed forever.
# What if you are building an "Undo" feature? Or what if you are building a 
# database (like Datomic) where you need to query the database as it existed 
# exactly 5 years ago?
# 
# You need a "Persistent" (Immutable) data structure. A persistent data structure 
# always preserves the previous version of itself when it is modified.
#
# If you just copy the entire array every time you make a change, it takes 
# O(N) time and O(N) memory per update. 1 million updates on a 1 million element 
# array will instantly exhaust your RAM.
#
# By using a Tree (Path Copying) to represent the array, an update only requires 
# copying the nodes along the path from the root to the leaf. 
# Everything else is structurally SHARED between the old version and the new version!
# This reduces the update cost to O(log N) time and O(log N) memory!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Structural Sharing.
# - Understand Path Copying.
# - Implement a fully Persistent Array using a Binary Tree.
#
# ==============================================================================
"""

import math
from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STRUCTURAL SHARING & PATH COPYING
# ==============================================================================
class PersistentNode:
    """A single node in the Persistent Array Tree."""
    def __init__(self, value: int = 0):
        self.value = value
        self.left: Optional['PersistentNode'] = None
        self.right: Optional['PersistentNode'] = None


class PersistentArray:
    """
    An array implemented as a Binary Tree to allow O(log N) persistent updates.
    The leaves of the tree hold the actual array values.
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        # Create Version 0 (The initial state)
        self.versions: List[PersistentNode] = []
        self.versions.append(self._build(arr, 0, self.n - 1))

    def _build(self, arr: List[int], L: int, R: int) -> PersistentNode:
        """Recursively builds the initial tree (O(N) time)."""
        node = PersistentNode()
        if L == R:
            node.value = arr[L]
            return node
            
        mid = (L + R) // 2
        node.left = self._build(arr, L, mid)
        node.right = self._build(arr, mid + 1, R)
        return node

    def get(self, version_id: int, index: int) -> int:
        """
        Retrieves the value at `index` as it existed in `version_id`. O(log N) time.
        """
        if version_id < 0 or version_id >= len(self.versions):
            raise ValueError("Invalid version ID")
        return self._get_recursive(self.versions[version_id], 0, self.n - 1, index)

    def _get_recursive(self, node: PersistentNode, L: int, R: int, index: int) -> int:
        if L == R:
            return node.value
            
        mid = (L + R) // 2
        if index <= mid:
            return self._get_recursive(node.left, L, mid, index)
        else:
            return self._get_recursive(node.right, mid + 1, R, index)

    def update(self, index: int, new_value: int) -> int:
        """
        Updates the array by creating a NEW VERSION. O(log N) time and memory.
        Returns the ID of the new version.
        """
        # The new version starts by copying the path from the CURRENT latest version
        latest_root = self.versions[-1]
        new_root = self._update_recursive(latest_root, 0, self.n - 1, index, new_value)
        
        self.versions.append(new_root)
        return len(self.versions) - 1

    def _update_recursive(self, node: PersistentNode, L: int, R: int, index: int, new_value: int) -> PersistentNode:
        """
        PATH COPYING: We create a brand new node for every step down the path.
        But the new nodes point to the OLD unmodified branches! (Structural Sharing).
        """
        # 1. Create a brand new node to represent this step in the new version
        new_node = PersistentNode()
        
        # Base Case: We reached the leaf that needs to be updated
        if L == R:
            new_node.value = new_value
            return new_node
            
        mid = (L + R) // 2
        
        if index <= mid:
            # The update is in the LEFT subtree.
            # We recursively copy the left path.
            new_node.left = self._update_recursive(node.left, L, mid, index, new_value)
            # MAGIC: The right subtree wasn't touched. So the new node simply POINTS 
            # to the EXACT SAME right subtree from the old version! (Zero memory cost!)
            new_node.right = node.right
        else:
            # The update is in the RIGHT subtree.
            new_node.right = self._update_recursive(node.right, mid + 1, R, index, new_value)
            new_node.left = node.left
            
        return new_node


def demonstrate_persistent_array():
    section_header("Algorithm: Persistent Array (Path Copying)")
    
    # Indices:    0   1   2   3
    arr =       [ 10, 20, 30, 40 ]
    
    print(f"Initial Array (Version 0): {arr}")
    pa = PersistentArray(arr)
    
    print("\nUpdating Index 2 from 30 to 999...")
    v1 = pa.update(index=2, new_value=999)
    print(f"Created Version {v1}.")
    
    print("Updating Index 0 from 10 to 555...")
    v2 = pa.update(index=0, new_value=555)
    print(f"Created Version {v2}.")
    
    print("\n--- TIME TRAVEL QUERIES ---")
    
    print("Querying Index 2:")
    print(f" In Version 0 (Original): {pa.get(0, 2)} (Expected: 30)")
    print(f" In Version 1 (After 1st): {pa.get(1, 2)} (Expected: 999)")
    print(f" In Version 2 (After 2nd): {pa.get(2, 2)} (Expected: 999)")
    
    print("\nQuerying Index 0:")
    print(f" In Version 0 (Original): {pa.get(0, 0)} (Expected: 10)")
    print(f" In Version 1 (After 1st): {pa.get(1, 0)} (Expected: 10)")
    print(f" In Version 2 (After 2nd): {pa.get(2, 0)} (Expected: 555)")
    
    print("\nBy using Path Copying, we maintained 3 entirely independent versions")
    print("of the array in memory, but we only allocated O(log N) new nodes per update.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is Structural Sharing?
   Answer: When creating a new version of an immutable data structure, you do not copy the entire structure. Instead, the new version creates only the nodes that were modified (and their parent path up to the root) and maintains pointers to the unmodified subtrees of the old version. Both versions share the exact same objects in memory for the parts that didn't change.

2. Why is a Tree used instead of a standard Array for Persistent Arrays?
   Answer: A standard array is contiguous in memory. If you change one element, you cannot "structurally share" the rest of the array with a new version without doing massive pointer arithmetic trickery. A Tree structure natively supports branching pointers, allowing subtrees to be shared effortlessly between multiple roots.

3. Is Persistent Data Structure the same as Git version control?
   Answer: Conceptually, yes! Git uses a Directed Acyclic Graph (DAG) with structural sharing. A Git Commit is just a pointer to a root tree object. If you change one file, Git creates a new commit root, a new folder node, and a new file node (Path Copying), but the new folder node points to the exact same unmodified file blobs from the previous commit (Structural Sharing)!
"""

if __name__ == "__main__":
    demonstrate_persistent_array()
    print("\n[SUCCESS] Laboratory: Persistent Data Structures Completed.")
