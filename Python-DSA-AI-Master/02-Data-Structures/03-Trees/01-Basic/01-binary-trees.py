"""
## A. Concept Name
Binary Trees

## B. One-Sentence Definition
A binary tree is a hierarchical data structure in which each node has at most two children, referred to as the left child and the right child.

## C. Why Does This Exist?
It is used in various computational applications like searching, sorting, and representing hierarchical data, forming the basis for more advanced structures like Binary Search Trees and Heaps.

## D. Intuition
When organizing data, sometimes a linear structure (like an array) is too restrictive. A branching structure allows us to divide data hierarchically, making recursive operations and pathfinding more natural.

## E. Real-Life Analogy
A family tree where each person has at most two children, or a single-elimination tournament bracket.

## F. Mental Model
Think of an upside-down tree with a single 'root' node at the top. Each node branches downwards into a left and right path, ending at 'leaf' nodes which have no children.

## G. Visual Explanation
        A (Root)
       / \
      B   C
     / \   \
    D   E   F (Leaves: D, E, F)

## H. Formal Explanation
A binary tree is a tree data structure in which each node has at most two children, which are referred to as the left child and the right child. A recursive definition is that a binary tree is either empty, or consists of a root node and two disjoint binary trees called the left subtree and right subtree.

## I. Mathematical Foundation
- Maximum nodes at level `l` is 2^l.
- Maximum nodes in a tree of height `h` is 2^(h+1) - 1.
- A binary tree with `N` nodes has `N+1` null references (empty children).

## J. From-Scratch Implementation
See `TreeNode` and `BinaryTree` classes below.

## K. Library / Production Implementation
Python doesn't have a built-in binary tree in the standard library. However, structures like `heapq` implicitly use binary trees represented as arrays.

## L. Trace (walk through example)
Inserting a left child:
1. Check if the current node has a left child.
2. If None, create a new node and assign it as `left`.
3. If not None, create a new node, make the new node's left child the current left child, and make the new node the new left child.

## M. Complexity
Time Complexity: Node Creation O(1), Insertion O(1), Height Calculation O(n).
Space Complexity: Node Storage O(n), Recursion stack for height O(h).

## N. Common Mistakes
- Forgetting to handle the base case (node is None) in recursive tree traversals.
- Confusing height (longest path to a leaf) with depth (path to the root).

## O. Common Confusions
- Confusing a Binary Tree with a Binary Search Tree (BST). A standard binary tree has no ordering constraints between nodes.

## P. When To Use
- When representing hierarchical data (e.g., abstract syntax trees, expression trees).
- When building foundations for BSTs, Heaps, Tries, and other tree-like structures.

## Q. When NOT To Use
- When data is strictly linear or tabular.
- When you need fast arbitrary lookups by a key and the tree is not ordered (a hash map is better).

## R. Trade-offs
- Provides a natural hierarchical structure but requires extra memory for left and right pointers.
- Without self-balancing (in BSTs), a tree can become skewed (like a linked list), losing the benefits of O(log n) height.

## S. Debugging
- Check base cases for `None` to avoid `AttributeError: 'NoneType' object has no attribute 'left'`.
- Write helper functions to print tree traversals to visualize the structure.

## T. Memory Hook
"Bi" = Two. Every node is a parent that can have 0, 1, or 2 children, splitting paths like a fork in the road.

## U. Active Recall
- What is the difference between a full binary tree and a complete binary tree?
- How do you calculate the maximum number of nodes in a binary tree of height h?

## V. Practice
- Write a function to perform an in-order traversal of the tree.
- Write a function to find the maximum depth of a binary tree.

## W. Interview Question
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

## X. Project Connection
Binary trees are foundational for indexing algorithms in databases (B-Trees) and represent structured code in compilers (Abstract Syntax Trees).
"""

from typing import Optional, Any

class TreeNode:
    """A basic node in a binary tree."""
    def __init__(self, value: Any):
        self.value: Any = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.value})"

class BinaryTree:
    """Basic binary tree implementation."""
    def __init__(self, root_value: Any = None):
        self.root: Optional[TreeNode] = TreeNode(root_value) if root_value is not None else None

    def insert_left(self, current_node: TreeNode, value: Any) -> TreeNode:
        """Inserts a left child to the given node."""
        if current_node.left is None:
            current_node.left = TreeNode(value)
        else:
            new_node = TreeNode(value)
            new_node.left = current_node.left
            current_node.left = new_node
        return current_node.left

    def insert_right(self, current_node: TreeNode, value: Any) -> TreeNode:
        """Inserts a right child to the given node."""
        if current_node.right is None:
            current_node.right = TreeNode(value)
        else:
            new_node = TreeNode(value)
            new_node.right = current_node.right
            current_node.right = new_node
        return current_node.right

    def get_height(self, node: Optional[TreeNode]) -> int:
        """Returns the height of the tree from the given node."""
        if node is None:
            return -1 # Conventionally, height of empty tree is -1
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        return max(left_height, right_height) + 1

# Performance Analysis
"""
Time Complexity:
- Creation of a node: O(1)
- Insertion (as implemented here): O(1)
- Calculating Height: O(n) where n is the number of nodes (must visit all)

Space Complexity:
- Node storage: O(n)
- Recursion stack for height: O(h) where h is the height of the tree (O(n) worst case, O(log n) balanced).
"""

# Edge Cases:
"""
1. Empty tree (root is None)
2. Skewed tree (all nodes only have left children or only right children)
3. Single node tree
"""

# Interview Challenge: Symmetric Tree
"""
Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).
"""
def is_symmetric(root: Optional[TreeNode]) -> bool:
    def is_mirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
        if t1 is None and t2 is None: return True
        if t1 is None or t2 is None: return False
        return (t1.value == t2.value) and is_mirror(t1.right, t2.left) and is_mirror(t1.left, t2.right)
    return is_mirror(root, root)

def run_tests():
    print("Testing Basic Binary Tree...")
    tree = BinaryTree(1)
    if tree.root is not None:
        left = tree.insert_left(tree.root, 2)
        right = tree.insert_right(tree.root, 3)
        tree.insert_left(left, 4)
        tree.insert_right(right, 5)
        print(f"Height of tree: {tree.get_height(tree.root)} (Expected: 2)")

    print("Testing Symmetric Tree Challenge...")
    sym_tree = BinaryTree(1)
    if sym_tree.root is not None:
        l = sym_tree.insert_left(sym_tree.root, 2)
        r = sym_tree.insert_right(sym_tree.root, 2)
        sym_tree.insert_left(l, 3)
        sym_tree.insert_right(l, 4)
        sym_tree.insert_left(r, 4)
        sym_tree.insert_right(r, 3)
        print(f"Is symmetric? {is_symmetric(sym_tree.root)} (Expected: True)")

if __name__ == "__main__":
    run_tests()
