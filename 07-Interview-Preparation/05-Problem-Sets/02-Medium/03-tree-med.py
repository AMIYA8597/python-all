"""
Medium-Level Tree Problems for Interview Preparation
===================================================

This module covers medium-level tree problems commonly encountered in software engineering interviews.
Trees, particularly Binary Trees and Binary Search Trees (BST), are fundamental data structures.

Topics Covered:
1. Binary Tree Right Side View (BFS/DFS)
2. Lowest Common Ancestor of a Binary Tree (DFS)
3. Validate Binary Search Tree (DFS/Inorder)
4. Construct Binary Tree from Preorder and Inorder Traversal (Divide and Conquer)

Beginner Explanation:
A tree is a hierarchical data structure consisting of nodes. Medium tree problems usually involve
traversing the tree in a specific order (preorder, inorder, postorder, or level-order) and keeping
track of some state (like depth, path, or valid ranges).

Deep Technical Explanation:
- Time Complexity: Most tree traversal algorithms visit each node exactly once, resulting in O(N) time complexity, where N is the number of nodes.
- Space Complexity: The space complexity is usually dictated by the recursion stack (for DFS) or the queue size (for BFS).
  - For a balanced tree, the maximum depth is O(log N).
  - For a skewed tree (worst case), the depth can be O(N).
  - Level-order traversal (BFS) space complexity is O(W), where W is the maximum width of the tree. In the worst case (a complete binary tree), W = N/2, so O(N).

Real-World Use Cases:
- File systems (hierarchical structure)
- Abstract Syntax Trees (AST) in compilers
- DOM representation in web browsers
- Fast lookup, insertion, and deletion in databases (B-Trees)
"""

from typing import List, Optional, Deque
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

# -----------------------------------------------------------------------------
# 1. Binary Tree Right Side View
# -----------------------------------------------------------------------------
"""
Problem: Given the root of a binary tree, imagine yourself standing on the right side of it,
return the values of the nodes you can see ordered from top to bottom.

Approach (BFS):
Use level-order traversal. For each level, the last node processed is the one visible from the right.

Time Complexity: O(N) where N is the number of nodes.
Space Complexity: O(D) to keep the queues, where D is a tree diameter. Worst case O(N/2) = O(N).
"""

def rightSideView(root: Optional[TreeNode]) -> List[int]:
    """
    Returns the right side view of a binary tree.
    """
    if not root:
        return []
        
    result = []
    queue: Deque[TreeNode] = deque([root])
    
    while queue:
        level_length = len(queue)
        
        for i in range(level_length):
            node = queue.popleft()
            
            # If it's the last node in the current level, add it to result
            if i == level_length - 1:
                result.append(node.val)
                
            # Add child nodes to the queue for the next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
    return result

# -----------------------------------------------------------------------------
# 2. Lowest Common Ancestor of a Binary Tree
# -----------------------------------------------------------------------------
"""
Problem: Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
LCA is defined between two nodes p and q as the lowest node in T that has both p and q as descendants 
(where we allow a node to be a descendant of itself).

Approach (DFS):
Traverse the tree. If the current node is p or q, return the current node.
Recursively search the left and right subtrees.
If both left and right return a non-null node, it means p and q are found in different subtrees,
so the current node is their LCA.
If only one returns a non-null node, return that node (it might be the LCA, or just pass it up).

Time Complexity: O(N)
Space Complexity: O(N) worst case (skewed tree), O(log N) for balanced tree.
"""

def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'Optional[TreeNode]':
    """
    Finds the lowest common ancestor of two nodes.
    """
    # Base case
    if root is None or root == p or root == q:
        return root
        
    # Look for LCA in left and right subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both left and right are non-null, this node is the LCA
    if left and right:
        return root
        
    # Otherwise, return the non-null child
    return left if left else right

# -----------------------------------------------------------------------------
# 3. Validate Binary Search Tree
# -----------------------------------------------------------------------------
"""
Problem: Given the root of a binary tree, determine if it is a valid binary search tree (BST).
A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Approach (DFS with Range):
Keep track of the valid range (min_val, max_val) for the current node.
When going left, update the max_val to the current node's value.
When going right, update the min_val to the current node's value.

Time Complexity: O(N)
Space Complexity: O(N) worst case
"""

def isValidBST(root: Optional[TreeNode]) -> bool:
    """
    Validates if a binary tree is a valid BST.
    """
    def validate(node: Optional[TreeNode], low: float = float('-inf'), high: float = float('inf')) -> bool:
        # Empty trees are valid BSTs
        if not node:
            return True
            
        # The current node's value must be between low and high
        if node.val <= low or node.val >= high:
            return False
            
        # The left subtree must be < node.val, and right subtree must be > node.val
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    return validate(root)

# -----------------------------------------------------------------------------
# 4. Construct Binary Tree from Preorder and Inorder Traversal
# -----------------------------------------------------------------------------
"""
Problem: Given two integer arrays preorder and inorder where preorder is the preorder traversal 
of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

Approach (Divide and Conquer with HashMap):
The first element in `preorder` is always the root.
Find this root in `inorder` to split the tree into left and right subtrees.
Use a hash map to store the indices of `inorder` values for O(1) lookup.
Recursively build the left and right subtrees.

Time Complexity: O(N) - Building the hash map takes O(N), and we process each node once.
Space Complexity: O(N) - Hash map takes O(N) space, plus recursion stack.
"""

def buildTree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Constructs a binary tree from preorder and inorder traversals.
    """
    # Create a hash map to quickly find the root's index in the inorder array
    inorder_index_map = {val: idx for idx, val in enumerate(inorder)}
    preorder_index = 0
    
    def array_to_tree(left: int, right: int) -> Optional[TreeNode]:
        nonlocal preorder_index
        # If there are no elements to construct the tree
        if left > right:
            return None
            
        # Select the preorder_index element as the root and increment it
        root_val = preorder[preorder_index]
        root = TreeNode(root_val)
        preorder_index += 1
        
        # Build left and right subtrees
        # Elements from 'left' to 'inorder_index_map[root_val] - 1' belong to the left subtree
        root.left = array_to_tree(left, inorder_index_map[root_val] - 1)
        # Elements from 'inorder_index_map[root_val] + 1' to 'right' belong to the right subtree
        root.right = array_to_tree(inorder_index_map[root_val] + 1, right)
        
        return root

    return array_to_tree(0, len(preorder) - 1)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing Medium Tree Problems...")

    # Build a sample tree:
    #      1
    #    /   \
    #   2     3
    #    \     \
    #     5     4
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(5)
    root.right.right = TreeNode(4)

    print(f"Right Side View: {rightSideView(root)}") # Expected: [1, 3, 4]
    
    lca_node = lowestCommonAncestor(root, root.left, root.right)
    print(f"LCA of 2 and 3: {lca_node.val if lca_node else None}") # Expected: 1
    
    print(f"Is Valid BST (sample): {isValidBST(root)}") # Expected: False

    # Valid BST:
    #      2
    #    /   \
    #   1     3
    bst_root = TreeNode(2)
    bst_root.left = TreeNode(1)
    bst_root.right = TreeNode(3)
    print(f"Is Valid BST (BST): {isValidBST(bst_root)}") # Expected: True
    
    # Test Build Tree
    preorder = [3,9,20,15,7]
    inorder = [9,3,15,20,7]
    built_tree = buildTree(preorder, inorder)
    print(f"Built Tree root: {built_tree.val}") # Expected: 3
    print("All tests passed.")
