"""
# ==============================================================================
# LABORATORY: CORE TREE OPERATIONS & FAANG ALGORITHMS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know how to build a tree and traverse it. Now you must manipulate it.
# The algorithms in this file are legendary interview questions. In 2015, the 
# creator of Homebrew (Max Howell) famously tweeted that Google rejected him 
# because he couldn't "Invert a Binary Tree" on a whiteboard. 
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Solve: Invert a Binary Tree (LeetCode #226).
# - Solve: Validate a Binary Search Tree (LeetCode #98).
# - Solve: Lowest Common Ancestor of a BST (LeetCode #235).
#
# ==============================================================================
"""

from typing import Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE NODE DEFINITION
# ==============================================================================
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def print_tree(root: Optional[TreeNode], level=0, prefix="Root: "):
    """Helper to visualize tree structure in the console."""
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        print_tree(root.left, level + 1, "L: ")
        print_tree(root.right, level + 1, "R: ")


# ==============================================================================
# 4. INVERT A BINARY TREE
# ==============================================================================
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    LeetCode #226: Invert Binary Tree.
    Every left child becomes a right child, and vice versa.
    Time Complexity: O(N) (Visit every node once).
    Space Complexity: O(H) (Call stack).
    """
    if not root:
        return None
        
    # 1. Swap the left and right pointers
    temp = root.left
    root.left = root.right
    root.right = temp
    
    # 2. Recursively invert the subtrees
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root

def demonstrate_invert_tree():
    section_header("Algorithm: Invert a Binary Tree")
    
    #      4
    #    /   \
    #   2     7
    #  / \   / \
    # 1   3 6   9
    root = TreeNode(4)
    root.left, root.right = TreeNode(2), TreeNode(7)
    root.left.left, root.left.right = TreeNode(1), TreeNode(3)
    root.right.left, root.right.right = TreeNode(6), TreeNode(9)
    
    print("Original Tree:")
    print_tree(root)
    
    print("\nInverted Tree (Mirror Image):")
    inverted = invert_tree(root)
    print_tree(inverted)


# ==============================================================================
# 5. VALIDATE A BINARY SEARCH TREE
# ==============================================================================
def is_valid_bst(root: Optional[TreeNode], min_val: float = float('-inf'), max_val: float = float('inf')) -> bool:
    """
    LeetCode #98: Validate Binary Search Tree.
    A common trap: People just check if `left.val < root.val < right.val`. 
    THIS IS WRONG. The entire left subtree must be less than the root.
    We solve this by passing down a valid `min_val` and `max_val` range.
    """
    if not root:
        return True
        
    # The current node's value must fall strictly inside the allowed boundaries
    if not (min_val < root.val < max_val):
        return False
        
    # When going left, the maximum allowed value becomes the current node's value
    # When going right, the minimum allowed value becomes the current node's value
    return (is_valid_bst(root.left, min_val, root.val) and 
            is_valid_bst(root.right, root.val, max_val))

def demonstrate_validate_bst():
    section_header("Algorithm: Validate a BST")
    
    # Valid BST
    #      5
    #    /   \
    #   1     7
    valid = TreeNode(5)
    valid.left, valid.right = TreeNode(1), TreeNode(7)
    
    # Invalid BST (The 4 is in the right subtree of 5, which violates BST rules!)
    #      5
    #    /   \
    #   1     7
    #        / \
    #       4   8
    invalid = TreeNode(5)
    invalid.left, invalid.right = TreeNode(1), TreeNode(7)
    invalid.right.left, invalid.right.right = TreeNode(4), TreeNode(8)
    
    print(f"Is Tree 1 a valid BST? {is_valid_bst(valid)}")
    print(f"Is Tree 2 a valid BST? {is_valid_bst(invalid)} (Because 4 < 5 but is on the right)")


# ==============================================================================
# 6. LOWEST COMMON ANCESTOR (LCA) OF A BST
# ==============================================================================
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LeetCode #235: Lowest Common Ancestor of a Binary Search Tree.
    Because it is a BST, the logic is incredibly simple:
    If both p and q are less than the root, the LCA must be in the left subtree.
    If both p and q are greater than the root, the LCA must be in the right subtree.
    The FIRST node where they split paths (one is smaller, one is larger) IS the LCA.
    
    Time: O(H) | Space: O(1) (Iterative)
    """
    curr = root
    
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            # We found the split point (or one of the nodes IS the current node)
            return curr
            
    return root

def demonstrate_lca():
    section_header("Algorithm: Lowest Common Ancestor (BST)")
    
    #      6
    #    /   \
    #   2     8
    #  / \   / \
    # 0   4 7   9
    root = TreeNode(6)
    root.left, root.right = TreeNode(2), TreeNode(8)
    root.left.left, root.left.right = TreeNode(0), TreeNode(4)
    root.right.left, root.right.right = TreeNode(7), TreeNode(9)
    
    p = root.left       # 2
    q = root.right      # 8
    lca1 = lowest_common_ancestor(root, p, q)
    print(f"LCA of {p.val} and {q.val} is: {lca1.val} (Expected 6)")
    
    p2 = root.left.left # 0
    q2 = root.left.right # 4
    lca2 = lowest_common_ancestor(root, p2, q2)
    print(f"LCA of {p2.val} and {q2.val} is: {lca2.val} (Expected 2)")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is checking `left.val < root.val < right.val` insufficient for validating a BST?
   Answer: Because a node deep in the right subtree might have a value that is smaller than the absolute root of the tree. The BST rule states that ALL nodes in a left subtree must be smaller, and ALL nodes in a right subtree must be larger. You must pass down min/max boundary limits.

2. How do you invert a binary tree?
   Answer: Swap the `left` and `right` pointers of the current node, then recursively call the invert function on the left child and right child.

3. Why is finding the Lowest Common Ancestor (LCA) in a BST $O(\log N)$ but finding the LCA in a generic Binary Tree $O(N)$?
   Answer: In a BST, we can use the sorted property to mathematically determine if the target nodes are to the left or right, allowing us to drop half the tree at every step (Binary Search). In a generic binary tree, we don't know where the nodes are, so we must visit every single node (DFS) to find them.
"""

if __name__ == "__main__":
    demonstrate_invert_tree()
    demonstrate_validate_bst()
    demonstrate_lca()
    print("\n[SUCCESS] Laboratory: Core Tree Operations Completed.")
