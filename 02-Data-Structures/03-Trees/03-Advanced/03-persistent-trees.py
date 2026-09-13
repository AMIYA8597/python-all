"""
# ==============================================================================
# LABORATORY: PERSISTENT TREES (VERSION CONTROLLED DATA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# What if you need to query the state of a Database as it existed exactly 5 days 
# ago? Or what if you want to implement "Undo" in a text editor without storing 
# massive copies of the entire document? 
# A Persistent Tree allows you to update the tree while keeping the previous 
# version perfectly intact. It does this via "Path Copying" (Structural Sharing). 
# Every update returns a brand NEW Root node, but it shares 99% of its branches 
# with the old tree. It achieves O(log N) time and space per update.
# This is the secret behind Git, MVCC (Multi-Version Concurrency Control) in PostgreSQL, 
# and purely functional languages like Haskell.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Path Copying and Structural Sharing.
# - Implement a Persistent Binary Search Tree.
# - Demonstrate "Time Travel" by querying historical roots.
#
# ==============================================================================
"""

from typing import Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PATH COPYING ALGORITHM
# ==============================================================================
class PTreeNode:
    """
    A Persistent Tree Node.
    Once instantiated, a node is IMMUTABLE. We never change `val`, `left`, or `right`.
    """
    def __init__(self, val: int, left: Optional['PTreeNode'] = None, right: Optional['PTreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class PersistentBST:
    def __init__(self):
        # Instead of a single root, we store a list of all historical roots!
        # index 0 is version 0. index 1 is version 1, etc.
        self.history: list[Optional[PTreeNode]] = [None]
        
    def insert(self, val: int) -> int:
        """
        Inserts a value immutably.
        Returns the version number (index) of the newly created tree.
        Time: O(log N), Space: O(log N)
        """
        current_root = self.history[-1]
        
        # We recursively copy the path down to the insertion point.
        new_root = self._insert_immutable(current_root, val)
        
        self.history.append(new_root)
        return len(self.history) - 1

    def _insert_immutable(self, node: Optional[PTreeNode], val: int) -> PTreeNode:
        """
        The core of Path Copying.
        If we are updating the left child, we create a NEW node for the parent, 
        point its left child to the newly returned node, and point its right child 
        to the EXISTING (shared) right subtree.
        """
        if not node:
            return PTreeNode(val)
            
        if val < node.val:
            # Create a NEW node. Its left child is the result of the recursive insert.
            # Its right child is simply a pointer to the existing right subtree!
            new_left = self._insert_immutable(node.left, val)
            return PTreeNode(node.val, left=new_left, right=node.right)
            
        elif val > node.val:
            # Create a NEW node. Its right child is the result of the recursive insert.
            # Its left child is simply a pointer to the existing left subtree!
            new_right = self._insert_immutable(node.right, val)
            return PTreeNode(node.val, left=node.left, right=new_right)
            
        else:
            # Value already exists. No structural changes needed.
            return node

    def get_inorder_by_version(self, version: int) -> list[int]:
        """Fetches the state of the tree at a specific historical version."""
        if version < 0 or version >= len(self.history):
            raise ValueError("Invalid version")
            
        root = self.history[version]
        result = []
        self._inorder(root, result)
        return result
        
    def _inorder(self, node: Optional[PTreeNode], result: list[int]):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)


def demonstrate_persistent_tree():
    section_header("Algorithm: Persistent BST (Time Travel)")
    
    pbst = PersistentBST()
    
    print("Version 0 (Empty):", pbst.get_inorder_by_version(0))
    
    print("\n--- Inserting Data ---")
    v1 = pbst.insert(10)
    print(f"Inserted 10. (Version {v1})")
    
    v2 = pbst.insert(5)
    print(f"Inserted 5.  (Version {v2})")
    
    v3 = pbst.insert(15)
    print(f"Inserted 15. (Version {v3})")
    
    v4 = pbst.insert(2)
    print(f"Inserted 2.  (Version {v4})")
    
    print("\n--- Current State ---")
    print(f"Current Tree (Version {v4}): {pbst.get_inorder_by_version(v4)}")
    
    print("\n--- Time Travel (Querying Historical State) ---")
    print("Let's look at the tree exactly as it was at Version 2 (before 15 and 2 were added):")
    print(f"Version 2 Tree: {pbst.get_inorder_by_version(2)}")
    
    print("\nLet's look at Version 1 (when only 10 was inserted):")
    print(f"Version 1 Tree: {pbst.get_inorder_by_version(1)}")
    
    print("\nMemory Magic:")
    print("Version 4 did NOT copy the entire tree. It only created new nodes for the path")
    print("it took to insert '2' (which is the Root(10) -> Left(5) -> New Node(2)).")
    print("The Right child of Root(10) in Version 4 points directly to the EXACT SAME")
    print("memory address of Node(15) created in Version 3!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Path Copying" in a Persistent Tree?
   Answer: When a node is updated or inserted, we cannot mutate the tree (because old versions rely on it). Instead, we copy the target node, and then we must copy its parent, and its parent's parent, all the way up to the root. The new root represents the new version of the tree, while sharing all unmodified subtrees with the old version.

2. What is the Space Complexity of inserting 1 item into a Persistent BST?
   Answer: O(log N). Because we only copy the path from the root to the leaf. If the tree has 1,000,000 nodes, the height is ~20. We only allocate 20 new nodes in memory, while sharing the other 999,980 nodes with previous versions.

3. Name a real-world system that relies on Persistent Trees.
   Answer: PostgreSQL uses MVCC (Multi-Version Concurrency Control) allowing transactions to view the database exactly as it looked when the transaction started, even if other queries are currently modifying it. Git's internal object model also behaves like a persistent directed acyclic graph.
"""

if __name__ == "__main__":
    demonstrate_persistent_tree()
    print("\n[SUCCESS] Laboratory: Persistent Trees Completed.")
