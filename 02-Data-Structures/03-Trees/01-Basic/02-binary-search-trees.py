"""
# ==============================================================================
# LABORATORY: BINARY SEARCH TREES (BST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# An array takes O(N) to insert data and maintain sorted order (because you have 
# to shift elements). A standard Linked List takes O(N) to search. 
# A Binary Search Tree (BST) combines the O(log N) search speed of a sorted array 
# with the O(1) pointer-based insertion speed of a linked list (resulting in 
# O(log N) total insertion time). It is the conceptual foundation of database indexes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the BST Property: Left < Root < Right.
# - Implement O(log N) Search and Insertion.
# - Prove that an In-Order traversal of a BST yields a sorted array.
# - Master the notoriously tricky algorithm: BST Deletion (3 Cases).
#
# ==============================================================================
"""

from typing import Optional, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BST NODE AND CORE OPERATIONS
# ==============================================================================
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class BinarySearchTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    # --- 3.1 INSERTION ---
    def insert(self, val: int) -> None:
        """Inserts a value in O(log N) average time."""
        if not self.root:
            self.root = TreeNode(val)
            return
            
        curr = self.root
        while True:
            if val < curr.val:
                # Go left
                if curr.left is None:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            elif val > curr.val:
                # Go right
                if curr.right is None:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right
            else:
                # Value already exists, ignore (or handle duplicates depending on requirement)
                break

    # --- 3.2 SEARCH ---
    def search(self, val: int) -> bool:
        """Searches for a value in O(log N) average time."""
        curr = self.root
        while curr:
            if val == curr.val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    # --- 3.3 IN-ORDER TRAVERSAL ---
    def get_sorted_data(self) -> List[int]:
        """An in-order traversal of a valid BST ALWAYS yields sorted data."""
        result = []
        self._inorder(self.root, result)
        return result
        
    def _inorder(self, node: Optional[TreeNode], result: List[int]):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

def demonstrate_bst_basics():
    section_header("BST: Insert, Search, and In-Order Sort")
    
    bst = BinarySearchTree()
    values = [10, 5, 15, 3, 7, 12, 18]
    print(f"Inserting values: {values}")
    
    for v in values:
        bst.insert(v)
        
    print(f"\nExtracted Sorted Data (In-Order Traversal): {bst.get_sorted_data()}")
    
    print("\nSearch Tests:")
    print(f" Search for 7 (Exists): {bst.search(7)}")
    print(f" Search for 99 (Missing): {bst.search(99)}")


# ==============================================================================
# 4. ADVANCED: DELETING A NODE IN A BST
# ==============================================================================
def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    LeetCode #450: Delete Node in a BST (Medium)
    There are 3 cases when deleting a node:
    1. It is a Leaf Node (No children) -> Just delete it.
    2. It has 1 child -> Bypass it (connect its parent directly to its child).
    3. It has 2 children -> Find the "In-Order Successor" (the smallest node in 
       its right subtree), copy that value to the current node, and recursively 
       delete the successor.
    """
    if not root:
        return None

    # Step 1: Find the node
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Step 2: We found the node to delete!
        
        # Case 1 & 2: Node has 0 or 1 child
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
            
        # Case 3: Node has 2 children
        # Find the In-Order Successor (Smallest value in the right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left
            
        # Replace the value of the node we want to delete with the successor's value
        root.val = successor.val
        
        # Delete the successor node from the right subtree
        root.right = delete_node(root.right, successor.val)
        
    return root

def demonstrate_bst_deletion():
    section_header("Algorithm: Deleting a Node (The 3 Cases)")
    
    bst = BinarySearchTree()
    for v in [10, 5, 15, 3, 7, 12, 18]:
        bst.insert(v)
        
    print("Initial Tree In-Order:", bst.get_sorted_data())
    
    # Case 1: Leaf
    print("\nDeleting Leaf Node (3)...")
    bst.root = delete_node(bst.root, 3)
    print(bst.get_sorted_data())
    
    # Case 2: 1 Child
    # To set up Case 2, let's add a child to 7
    bst.insert(8)
    print("\nAdded 8. Deleting Node with 1 child (7)...")
    bst.root = delete_node(bst.root, 7)
    print(bst.get_sorted_data())
    
    # Case 3: 2 Children
    print("\nDeleting Node with 2 children (10, The Root)...")
    bst.root = delete_node(bst.root, 10)
    print(bst.get_sorted_data())


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental property of a Binary Search Tree (BST)?
   Answer: For any given node, ALL values in its left subtree must be strictly less than the node's value, and ALL values in its right subtree must be strictly greater than the node's value.

2. Why is an In-Order traversal of a BST significant?
   Answer: Because visiting Left -> Root -> Right perfectly aligns with the BST property (Smaller -> Current -> Larger), resulting in a perfectly sorted list of values in O(N) time.

3. What is the worst-case Time Complexity for searching a BST, and how does it happen?
   Answer: O(N). If you insert data into a BST that is already sorted (e.g., 1, 2, 3, 4, 5), every node will be attached to the right pointer of the previous node. The tree degenerates into a standard Linked List, destroying the O(log N) binary search property. (This is why AVL and Red-Black trees were invented).
"""

if __name__ == "__main__":
    demonstrate_bst_basics()
    demonstrate_bst_deletion()
    print("\n[SUCCESS] Laboratory: Binary Search Trees Completed.")
