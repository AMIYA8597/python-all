"""
## A. Concept Name
Tree Traversals (DFS and BFS)

## B. One-Sentence Definition
Tree traversal is the systematic process of visiting every node in a tree data structure exactly once, either by exploring deeply first (DFS) or broadly level-by-level (BFS).

## C. Why Does This Exist?
Trees are non-linear data structures, meaning there isn't a single natural sequence to read their elements. Traversals provide deterministic ways to process, search, copy, or flatten the hierarchical data into a linear format based on the problem's needs.

## D. Intuition
Imagine exploring a large building. You can either walk down a single hallway all the way to its end before checking other rooms (Depth-First Search), or you can check all the rooms on the current floor before moving to the next floor (Breadth-First Search).

## E. Real-Life Analogy
- Preorder: Reading a book's table of contents (Chapter 1, Section 1.1, Section 1.2, Chapter 2).
- Inorder: Flattening a mathematical expression tree into a standard human-readable equation (e.g., 3 + 4).
- Postorder: Evaluating the size of directories on your computer (you must calculate the size of all subdirectories before you can know the total size of the parent directory).
- Level-order (BFS): A company's organizational chart processed by rank—first the CEO, then all VPs, then all Managers.

## F. Mental Model
For DFS (Preorder, Inorder, Postorder), imagine drawing a continuous outline tightly around the tree structure.
- Preorder: Visit the node the *first* time you pass its left side. (Root, Left, Right)
- Inorder: Visit the node when you pass its *bottom* side. (Left, Root, Right)
- Postorder: Visit the node the *last* time you pass its right side. (Left, Right, Root)
For BFS (Level-order), imagine shining a spotlight across the tree horizontally from top to bottom.

## G. Visual Explanation
Consider this binary tree:
       1
      / \
     2   3
    / \
   4   5

- Preorder (Root, L, R): 1 -> 2 -> 4 -> 5 -> 3
- Inorder (L, Root, R): 4 -> 2 -> 5 -> 1 -> 3
- Postorder (L, R, Root): 4 -> 5 -> 2 -> 3 -> 1
- Level-order (Top to Bottom): [1] -> [2, 3] -> [4, 5]

## H. Formal Explanation
Tree traversals are algorithms that visit all nodes of a tree in a specific order. 
- Depth-First Search (DFS) typically uses the call stack (recursion) or an explicit stack. The three main DFS strategies dictate when the root node is processed relative to its subtrees.
- Breadth-First Search (BFS) explores the tree level by level, utilizing a Queue (FIFO) to keep track of nodes to visit next.

## I. Mathematical Foundation
A tree with N nodes has exactly N-1 edges. Since each traversal visits every node exactly once and traverses each edge a constant number of times, the time complexity is bounded by O(N). The number of unique binary trees that yield the same inorder traversal sequence of length N is given by the N-th Catalan number: C_n = (2n)! / ((n+1)! * n!).

## J. From-Scratch Implementation
(See the `Traversals` class in the code below for implementation)

## K. Library / Production Implementation
Python's standard library provides generic data structures to help with traversal, like `collections.deque` for BFS queues. In production, tree traversal logic is often embedded within specific libraries like `ast` (Abstract Syntax Trees for Python code) which uses the Visitor pattern (`NodeVisitor.generic_visit` handles traversal).

## L. Trace (walk through example)
For `inorder_recursive(root=1)`:
1. `root=1`, call `inorder(2)`
2. `root=2`, call `inorder(4)`
3. `root=4`, `root.left` is None, append 4, `root.right` is None. Return `[4]`
4. Back at `root=2`, append 2, call `inorder(5)`
5. `root=5`, returns `[5]`
6. Back at `root=2`, returns `[4] + [2] + [5] = [4, 2, 5]`
7. Back at `root=1`, append 1, call `inorder(3)`
8. `root=3`, returns `[3]`
9. Back at `root=1`, returns `[4, 2, 5] + [1] + [3] = [4, 2, 5, 1, 3]`

## M. Complexity
- **Time Complexity:** O(N) for all traversals, as every node is visited once.
- **Space Complexity:** 
  - DFS: O(H) where H is the height of the tree. Best/Average case (balanced tree): O(log N). Worst case (skewed tree): O(N).
  - BFS: O(W) where W is the maximum width of the tree. Worst case (perfect binary tree leaf level): O(N/2) = O(N).

## N. Common Mistakes
- Modifying the tree structure while traversing without careful reference tracking.
- Forgetting to check if `root` is `None` before attempting to access `root.left` or `root.value`.
- Using a standard list `[]` as a queue for BFS and using `.pop(0)`, which is O(N) time. Always use `collections.deque.popleft()` which is O(1).

## O. Common Confusions
- Confusing the terms Pre/In/Post. *Remember: the prefix (Pre, In, Post) refers to when the ROOT is visited relative to its children.*
- Mixing up iterative implementations of DFS and BFS. DFS uses a Stack (LIFO), BFS uses a Queue (FIFO).

## P. When To Use
- **Preorder:** Copying or serializing a tree structure.
- **Inorder:** Getting elements of a Binary Search Tree (BST) in sorted (ascending) order.
- **Postorder:** Deleting a tree (you must delete children before the parent), or evaluating bottom-up properties (e.g., height, directory sizes).
- **Level-order (BFS):** Finding the shortest path in an unweighted graph/tree, or solving problems that require understanding relationships at the same depth.

## Q. When NOT To Use
- Do not use DFS when looking for a node strictly close to the root (BFS is better).
- Do not use BFS when memory is highly constrained and the tree is very wide (DFS uses O(H) space, which might be less than O(W)).
- Avoid deep recursive DFS in languages like Python if the tree depth can exceed the recursion limit (default 1000); use an iterative stack instead.

## R. Trade-offs
- **Recursive vs. Iterative DFS:** Recursive is cleaner and easier to write but vulnerable to stack overflow. Iterative is more robust for deep trees but requires explicitly managing the stack.
- **DFS vs. BFS:** DFS is often more memory efficient for balanced trees (O(log N) space vs O(N) for BFS). BFS guarantees finding the shallowest target first.

## S. Debugging
- Print the nodes as they are visited to trace the traversal order.
- If using recursion, visualize the call stack depth.
- Ensure your queue/stack isn't accumulating duplicates if the graph contains cycles (not typically an issue for pure trees, but critical for general graphs).

## T. Memory Hook
- **Pre**-order: **Pre**fix (Parent first)
- **In**-order: **In**-between (Parent in middle)
- **Post**-order: **Post**fix (Parent last)

## U. Active Recall
- What traversal gives a sorted list for a BST? (Inorder)
- Which data structure is used for BFS? (Queue)
- If you need to delete a tree, which traversal is safest? (Postorder)

## V. Practice
- Implement the iterative versions of Inorder, Preorder, and Postorder traversals.
- LeetCode 94: Binary Tree Inorder Traversal
- LeetCode 102: Binary Tree Level Order Traversal

## W. Interview Question
Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree. (Implemented below!)

## X. Project Connection
In web scraping or DOM manipulation (like React's Virtual DOM), trees are traversed continuously. A web crawler often uses BFS to visit links (finding links one click away before two clicks away). Compilers use Postorder traversal to generate machine code from syntax trees.
"""

from typing import Optional, Any, List
from collections import deque

class TreeNode:
    def __init__(self, value: Any):
        self.value: Any = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class Traversals:
    @staticmethod
    def inorder_recursive(root: Optional[TreeNode]) -> List[Any]:
        """Left -> Root -> Right"""
        res = []
        if root:
            res = Traversals.inorder_recursive(root.left)
            res.append(root.value)
            res = res + Traversals.inorder_recursive(root.right)
        return res

    @staticmethod
    def preorder_recursive(root: Optional[TreeNode]) -> List[Any]:
        """Root -> Left -> Right"""
        res = []
        if root:
            res.append(root.value)
            res = res + Traversals.preorder_recursive(root.left)
            res = res + Traversals.preorder_recursive(root.right)
        return res

    @staticmethod
    def postorder_recursive(root: Optional[TreeNode]) -> List[Any]:
        """Left -> Right -> Root"""
        res = []
        if root:
            res = Traversals.postorder_recursive(root.left)
            res = res + Traversals.postorder_recursive(root.right)
            res.append(root.value)
        return res

    @staticmethod
    def level_order(root: Optional[TreeNode]) -> List[List[Any]]:
        """Breadth-First Search"""
        if not root: return []
        res = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)
                if node.left: queue.append(node.left)
                if node.right: queue.append(node.right)
            res.append(current_level)
        return res

def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    if not preorder or not inorder:
        return None
    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)
    root.left = build_tree(preorder[1:mid+1], inorder[:mid])
    root.right = build_tree(preorder[mid+1:], inorder[mid+1:])
    return root

def run_tests():
    print("Testing Traversals...")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print(f"Inorder: {Traversals.inorder_recursive(root)} (Expected: [4, 2, 5, 1, 3])")
    print(f"Preorder: {Traversals.preorder_recursive(root)} (Expected: [1, 2, 4, 5, 3])")
    print(f"Postorder: {Traversals.postorder_recursive(root)} (Expected: [4, 5, 2, 3, 1])")
    print(f"Level Order: {Traversals.level_order(root)} (Expected: [[1], [2, 3], [4, 5]])")

if __name__ == "__main__":
    run_tests()
