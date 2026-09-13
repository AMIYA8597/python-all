"""
# ==============================================================================
# LABORATORY: AVL TREES (SELF-BALANCING BST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Binary Search Tree (BST) is disastrous if you feed it sorted data. 
# If you insert [1, 2, 3, 4, 5], every node attaches to the right of the previous 
# node. The tree becomes a Linked List, and search time degrades from O(log N) 
# to O(N). 
# An AVL Tree solves this by calculating the "Balance Factor" of every node and 
# performing algorithmic "Rotations" during insertion to guarantee the tree remains 
# perfectly balanced. This guarantees O(log N) operations regardless of input order.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Balance Factor (Height of Left - Height of Right).
# - Understand the 4 Types of Rotations (Left, Right, Left-Right, Right-Left).
# - Implement AVL Node Height tracking.
# - Implement an AVL Tree Insertion with automatic rebalancing.
#
# ==============================================================================
"""

from typing import Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. AVL NODE DEFINITION
# ==============================================================================
class AVLNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        # The key to an AVL tree is caching the height of each node!
        self.height = 1


# ==============================================================================
# 4. AVL TREE IMPLEMENTATION
# ==============================================================================
class AVLTree:
    
    # --- UTILITY METHODS ---
    def _get_height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """
        Balance Factor = Height of Left Subtree - Height of Right Subtree
        If > 1, the tree is Left-Heavy.
        If < -1, the tree is Right-Heavy.
        """
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # --- ROTATIONS ---
    def _right_rotate(self, z: AVLNode) -> AVLNode:
        """
        Used when the tree is Left-Left heavy.
             z (Heavy)            y (New Root)
            / \                  / \
           y   T4      --->     x   z
          / \                      / \
         x   T3                   T3  T4
        """
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights (MUST update z first because it is now below y!)
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y # Return the new root

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        """
        Used when the tree is Right-Right heavy.
           z (Heavy)              y (New Root)
          / \                    / \
         T1  y        --->      z   x
            / \                / \
           T2  x              T1  T2
        """
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y # Return the new root

    # --- INSERTION ---
    def insert(self, root: Optional[AVLNode], key: int) -> AVLNode:
        """
        Recursive insertion that automatically rebalances the tree on the way back up.
        """
        # 1. Standard BST Insert
        if not root:
            return AVLNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update the height of this ancestor node
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        # 3. Get the balance factor to check if it became unbalanced
        balance = self._get_balance(root)

        # 4. If unbalanced, there are 4 Cases

        # Case 1: Left-Left Heavy
        # The key was inserted to the left of the left child.
        if balance > 1 and key < root.left.val:
            return self._right_rotate(root)

        # Case 2: Right-Right Heavy
        # The key was inserted to the right of the right child.
        if balance < -1 and key > root.right.val:
            return self._left_rotate(root)

        # Case 3: Left-Right Heavy
        # The key was inserted to the right of the left child.
        if balance > 1 and key > root.left.val:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Case 4: Right-Left Heavy
        # The key was inserted to the left of the right child.
        if balance < -1 and key < root.right.val:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root # Return the (possibly unchanged) root


def print_tree(root: Optional[AVLNode], level=0, prefix="Root: "):
    """Helper to visualize tree structure in the console."""
    if root is not None:
        print(" " * (level * 4) + prefix + f"{root.val} (h={root.height})")
        print_tree(root.left, level + 1, "L: ")
        print_tree(root.right, level + 1, "R: ")


# ==============================================================================
# 5. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_avl_rotations():
    section_header("AVL Tree Auto-Balancing (Right-Right Case)")
    
    tree = AVLTree()
    root = None
    
    # Inserting sorted data into a standard BST would create a Linked List.
    # Watch the AVL tree dynamically rotate to maintain balance!
    print("Inserting 1, 2, 3 (Sorted Data)...")
    
    root = tree.insert(root, 1)
    root = tree.insert(root, 2)
    # The moment 3 is inserted, Node 1 becomes Right-Right heavy (balance = -2).
    # A Left Rotation is triggered, making 2 the new root!
    root = tree.insert(root, 3)
    
    print_tree(root)
    print("\nNotice how 2 became the root! The tree remained perfectly balanced.")
    
    print("\nInserting 4, 5, 6...")
    for v in [4, 5, 6]:
        root = tree.insert(root, v)
        
    print_tree(root)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What triggers an AVL Tree to rotate?
   Answer: When the Balance Factor of any node (Height of Left - Height of Right) becomes greater than 1 or less than -1.

2. In the Left-Right heavy case (e.g., node has a left child, and that left child has a right child), why do we need TWO rotations?
   Answer: If you try to do a single Right Rotation, the tree will just turn into a Right-Left heavy tree! You must first perform a Left Rotation on the left child to straighten the "dog leg" into a pure Left-Left line, and THEN perform a Right Rotation on the root.

3. AVL Trees vs Red-Black Trees. Which is better?
   Answer: AVL Trees are strictly balanced, meaning they guarantee the absolute fastest O(log N) lookup times. However, because they are so strict, they require more Rotations during insertion. Red-Black trees are loosely balanced (less rotations), making them slightly faster for Write-heavy workloads, which is why Red-Black is used in Java's `TreeMap` and C++'s `std::map`.
"""

if __name__ == "__main__":
    demonstrate_avl_rotations()
    print("\n[SUCCESS] Laboratory: AVL Trees Completed.")
