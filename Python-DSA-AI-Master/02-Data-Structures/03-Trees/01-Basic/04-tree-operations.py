"""
## A. Concept Name
Binary Tree Operations

## B. One-Sentence Definition
Common algorithms for traversing, modifying, and querying properties of binary trees using recursive or iterative techniques.

## C. Why Does This Exist?
Because tree structures naturally represent hierarchical data, operations like finding depth, inversion, or ancestors are foundational primitives for manipulating and understanding these hierarchies.

## D. Intuition
Since a tree is defined recursively (a node has subtrees which are themselves trees), operations on trees can often be broken down into performing the operation on a node's left subtree, its right subtree, and combining the results.

## E. Real-Life Analogy
Think of a company's organizational chart. Finding the "Lowest Common Ancestor" of two employees is like finding their closest mutual manager. The "Max Depth" is the length of the longest chain of command from the CEO down to an entry-level employee.

## F. Mental Model
Visualize a tree operation as sending a scout down every path. The scout reaches the end (leaf nodes), and as they return back up, they bring information (like depth or inverted branches) to combine at each junction until they reach the start (root).

## G. Visual Explanation
Inverting a tree:
     1               1
   /   \    =>     /   \
  2     3         3     2
 / \                   / \
4   5                 5   4
You recursively swap the left and right children at each node.

## H. Formal Explanation
Tree operations often utilize Depth-First Search (DFS) algorithms, relying on the Call Stack to maintain state. They require visiting each node exactly once to compute global properties (like diameter) or finding specific relationships (like LCA), combining results from sub-problems in a bottom-up or top-down manner.

## I. Mathematical Foundation
The operations depend on the properties of a tree graph G = (V, E), where |E| = |V| - 1. Time complexity is often O(|V|) as we visit each node. The maximum stack depth corresponds to the tree height h, where log_2(n) <= h <= n.

## J. From-Scratch Implementation
(See the code below for implementations of Max Depth, Invert Tree, and LCA).

## K. Library / Production Implementation
Python doesn't have a built-in tree implementation in its standard library, but packages like `networkx` provide comprehensive graphing and tree operations. In practice, custom tree nodes are standard for algorithm interviews and domain-specific hierarchical structures.

## L. Trace (walk through example)
LCA(root=1, p=4, q=3):
- Call LCA on 1.
- Left child (2): neither p nor q. Calls LCA on 4 (returns 4) and 5 (returns None). Returns 4 to root.
- Right child (3): equals q. Returns 3 to root.
- Root sees left returned 4 and right returned 3. Since both are non-null, root (1) is the LCA.

## M. Complexity
Time Complexity: O(n) for traversing all nodes (n is number of nodes).
Space Complexity: O(h) for the recursion stack, where h is height of tree. O(log n) for balanced tree, O(n) worst case (skewed tree).

## N. Common Mistakes
1. Not handling the base case properly (e.g., `if not root:`).
2. Forgetting to return values from recursive calls.
3. Using global variables instead of passing state or using `nonlocal` (like in the Diameter problem).

## O. Common Confusions
"How does the recursion know where to go back to?" -> The call stack automatically keeps track of where each function was called from.
"Is LCA always the parent?" -> No, a node can be its own ancestor (if node p is a descendant of node q, q is the LCA).

## P. When To Use
Whenever you need to extract metrics (depth, diameter) or manipulate structures (invert, prune) of hierarchical data.

## Q. When NOT To Use
When the data is not strictly hierarchical (contains cycles). In that case, graph traversal algorithms (with visited sets) are necessary.

## R. Trade-offs
Recursion is cleaner and easier to write but can cause StackOverflow on extremely deep trees. Iterative solutions (using explicit stacks or queues) avoid StackOverflow but are often more verbose.

## S. Debugging
Use a small tree (3-5 nodes). Trace the variables manually on paper. Print the node value at the beginning of the recursive function and just before returning to see the order of execution.

## T. Memory Hook
"Recursion goes DOWN to the leaves, and brings the answers UP to the root."

## U. Active Recall
- What is the base case for most tree operations? (If node is None, return 0 or None).
- How do you find LCA if one node is in the left subtree and the other is in the right? (The current node is the LCA).

## V. Practice
- Find the sum of all left leaves.
- Check if two trees are identical.
- Determine if a tree is height-balanced.

## W. Interview Question
"Find the diameter of a binary tree (the longest path between any two nodes)." (Implementation provided in the module).

## X. Project Connection
In a compiler or interpreter, Abstract Syntax Trees (ASTs) are evaluated using similar recursive operations to traverse and execute code or find scoping depths.
"""

from typing import Optional

class TreeNode:
    def __init__(self, value: int):
        self.value: int = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class TreeOperations:
    @staticmethod
    def max_depth(root: Optional[TreeNode]) -> int:
        """Finds the maximum depth (height) of the binary tree."""
        if not root:
            return 0
        return max(TreeOperations.max_depth(root.left), TreeOperations.max_depth(root.right)) + 1

    @staticmethod
    def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
        """Inverts a binary tree (mirrors it)."""
        if not root:
            return None
        root.left, root.right = TreeOperations.invert_tree(root.right), TreeOperations.invert_tree(root.left)
        return root

    @staticmethod
    def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
        """Finds the lowest common ancestor of two nodes in a binary tree."""
        if not root or root == p or root == q:
            return root
        left = TreeOperations.lowest_common_ancestor(root.left, p, q)
        right = TreeOperations.lowest_common_ancestor(root.right, p, q)
        if left and right:
            return root
        return left if left else right

# Performance Analysis
"""
Time Complexity: 
- Most operations like depth, invert, LCA require visiting each node: O(n).
Space Complexity:
- O(h) for the recursion stack, where h is the tree height. O(n) worst case, O(log n) balanced.
"""

# Edge Cases:
"""
1. The tree is empty.
2. One of the target nodes in LCA is the root or doesn't exist (though usually guaranteed to exist).
3. The tree is a straight line (linked list equivalent).
"""

# Interview Challenge: Diameter of Binary Tree
"""
The diameter of a binary tree is the length of the longest path between any two nodes in a tree. 
This path may or may not pass through the root.
"""
def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    diameter = 0
    def depth(node: Optional[TreeNode]) -> int:
        nonlocal diameter
        if not node:
            return 0
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        diameter = max(diameter, left_depth + right_depth)
        return max(left_depth, right_depth) + 1
    depth(root)
    return diameter

def run_tests():
    print("Testing Tree Operations...")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print(f"Max Depth: {TreeOperations.max_depth(root)} (Expected: 3)")
    
    lca = TreeOperations.lowest_common_ancestor(root, root.left.left, root.right)
    print(f"LCA of 4 and 3: {lca.value if lca else None} (Expected: 1)")

    print(f"Diameter of tree: {diameter_of_binary_tree(root)} (Expected: 3)")

if __name__ == "__main__":
    run_tests()
