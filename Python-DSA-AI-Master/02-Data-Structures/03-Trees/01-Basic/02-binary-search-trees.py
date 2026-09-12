"""
## A. Concept Name
Binary Search Tree (BST)

## B. One-Sentence Definition
A Binary Search Tree is a node-based binary tree data structure where each node has a comparable key, and the key in any node is larger than all keys in its left subtree and smaller than all keys in its right subtree.

## C. Why Does This Exist?
It exists to combine the flexibility of a linked list (dynamic insertion/deletion) with the efficiency of a sorted array (fast search).

## D. Intuition
By maintaining elements in a sorted structure that repeatedly divides the search space in half, we can achieve logarithmic time complexity for fundamental operations.

## E. Real-Life Analogy
Think of a dictionary (the physical book). If you are looking for "Mango," you open it near the middle. If you land on "Orange," you know "Mango" must be in the left half, completely ignoring the right half. A BST does exactly this at every single step.

## F. Mental Model
Imagine a family tree where every left child represents a smaller value and every right child represents a larger value. Every decision branching left or right narrows down your destination.

## G. Visual Explanation
      50
    /    \
  30      70
 /  \    /  \
20  40  60  80
Searching for 60: Start at 50 -> 60 is larger, go right -> at 70 -> 60 is smaller, go left -> found 60!

## H. Formal Explanation
A BST is a rooted binary tree whose internal nodes each store a key greater than all the keys in the node's left subtree and less than those in its right subtree. This allows for fast lookup, addition, and removal of items, relying on the principle of binary search.

## I. Mathematical Foundation
The maximum number of nodes at level `l` is 2^l. For a balanced tree with `n` nodes, the height `h` is approximately log2(n). Operations depend on the height, taking O(h) time.

## J. From-Scratch Implementation
(See the code in this module: `BSTNode`, `BinarySearchTree`)

## K. Library / Production Implementation
Python doesn't have a built-in BST in the standard library. For production, balanced variants like `bisect` (on lists) or third-party libraries like `bintrees` (Red-Black/AVL trees) are typically used for sorted collections.

## L. Trace (walk through example)
Inserting 40 into an empty tree: root becomes 40.
Inserting 30: 30 < 40 -> insert as left child.
Inserting 50: 50 > 40 -> insert as right child.
Searching 30: start at 40, 30 < 40 -> go left, find 30.

## M. Complexity
- Time: Search/Insert/Delete average O(log n), worst-case O(n) (unbalanced/skewed tree).
- Space: O(h) for recursive call stack, average O(log n), worst-case O(n).

## N. Common Mistakes
- Not realizing that a naive BST can degrade into a linked list O(n) if elements are inserted in sorted order.
- Checking only immediate children instead of entire subtrees when validating a BST.

## O. Common Confusions
- Difference between a Binary Tree (any tree with max 2 children) and a Binary Search Tree (ordered).
- Thinking duplicates are automatically handled (they require specific rules: e.g., always go left, or store a count).

## P. When To Use
- When you need a dynamic dataset where elements are constantly added/removed, and you need fast lookups.
- When you need ordered data (e.g., finding the min, max, or next closest value quickly).

## Q. When NOT To Use
- When the data is static (use a sorted array).
- If insertions might be heavily skewed (use self-balancing trees like AVL or Red-Black).
- If you only need O(1) lookups and no ordering (use a Hash Map / Dictionary).

## R. Trade-offs
- Time vs Space: Takes extra memory for pointers compared to an array, but provides faster insertions/deletions.
- Simplicity vs Performance: Naive BST is simple to implement but lacks guaranteed logarithmic limits unlike complex balanced variants.

## S. Debugging
- Print the tree using an in-order traversal; if the output is not sorted, the BST property is violated.
- Check tree height recursively to identify skewed shapes.

## T. Memory Hook
Left is Less, Right is Raised (Greater).

## U. Active Recall
- What is the difference in worst-case time complexity between BST and a sorted array for insertion?
- How do you find the minimum value in a BST? (Go left as far as possible).

## V. Practice
- Implement an iterative version of BST search.
- Implement node deletion in a BST.

## W. Interview Question
Given the root of a binary tree, determine if it is a valid binary search tree (BST). (See `is_valid_bst` below).

## X. Project Connection
Used in building database indexes, autocomplete features, or interval scheduling algorithms where maintaining sorted, easily updatable states is required.
"""

from typing import Optional

class BSTNode:
    """A node in a Binary Search Tree."""
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        
    def __repr__(self) -> str:
        return f"BSTNode({self.key})"

class BinarySearchTree:
    """Implementation of a Binary Search Tree."""
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: int) -> None:
        """Inserts a new key into the BST."""
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node: BSTNode, key: int) -> None:
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key: int) -> Optional[BSTNode]:
        """Searches for a key in the BST."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

# Performance Analysis
"""
Time Complexity:
- Search/Insert/Delete: O(h) where h is the height. O(log n) average, O(n) worst-case (unbalanced).
Space Complexity:
- O(h) for recursive call stack. O(n) for worst-case.
"""

# Edge Cases:
"""
1. Inserting duplicates (handled by ignoring or placing conventionally).
2. Searching for non-existent elements.
3. Deleting leaf, node with one child, and node with two children.
"""

# Interview Challenge: Validate Binary Search Tree
"""
Given the root of a binary tree, determine if it is a valid binary search tree (BST).
"""
def is_valid_bst(root: Optional[BSTNode]) -> bool:
    def validate(node: Optional[BSTNode], low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.key < high):
            return False
        return (validate(node.left, low, node.key) and 
                validate(node.right, node.key, high))
    return validate(root, float('-inf'), float('inf'))

def run_tests():
    print("Testing Binary Search Tree...")
    bst = BinarySearchTree()
    keys = [50, 30, 20, 40, 70, 60, 80]
    for key in keys:
        bst.insert(key)
        
    print(f"Search for 40: {bst.search(40) is not None} (Expected: True)")
    print(f"Search for 90: {bst.search(90) is not None} (Expected: False)")
    print(f"Is valid BST? {is_valid_bst(bst.root)} (Expected: True)")

if __name__ == "__main__":
    run_tests()
