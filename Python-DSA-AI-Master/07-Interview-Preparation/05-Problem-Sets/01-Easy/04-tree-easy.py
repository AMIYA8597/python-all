"""
Tree Easy Problem Set

Learning Objectives:
1. Master recursive tree traversals (DFS).
2. Understand iterative Level Order Traversal (BFS).
3. Learn to break down tree problems into sub-problems.

Concepts Explained:
- Binary Trees are hierarchical data structures where each node has at most two children.
- Depth-First Search (DFS) typically uses recursion or a stack.
- Breadth-First Search (BFS) typically uses a queue.
- Trees often represent recursive structures, making recursion a natural fit.
"""

from typing import Optional
import time

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Given the root of a binary tree, return its maximum depth.
    A binary tree's maximum depth is the number of nodes along the longest path 
    from the root node down to the farthest leaf node.
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Given the root of a binary tree, invert the tree, and return its root.
    """
    if not root:
        return None
        
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root

def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).
    """
    def is_mirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (t1.val == t2.val) and is_mirror(t1.right, t2.left) and is_mirror(t1.left, t2.right)
        
    return is_mirror(root, root)

def performance_analysis():
    print("Performance Analysis for Max Depth:")
    # Create a skewed tree of depth 900 (avoid recursion limit)
    root = TreeNode(0)
    curr = root
    for i in range(900):
        curr.left = TreeNode(i)
        curr = curr.left
        
    start = time.time()
    depth = max_depth(root)
    print(f"Time taken for depth {depth}: {time.time() - start:.6f} seconds")

# Interview Challenge: Check if two binary trees are identical
def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)

def test_tree_easy():
    print("Testing Max Depth...")
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    assert max_depth(root) == 3
    
    print("Testing Invert Tree...")
    inverted = invert_tree(root)
    assert inverted.left.val == 20
    assert inverted.right.val == 9
    
    print("Testing Is Symmetric...")
    sym_root = TreeNode(1)
    sym_root.left = TreeNode(2)
    sym_root.right = TreeNode(2)
    assert is_symmetric(sym_root) is True
    
    print("All tests passed!")

if __name__ == "__main__":
    test_tree_easy()
    performance_analysis()
