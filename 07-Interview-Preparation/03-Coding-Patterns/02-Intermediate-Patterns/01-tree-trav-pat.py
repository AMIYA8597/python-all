"""
Tree Traversal Patterns

Learning Objectives:
1. Understand the core concept of tree traversal patterns (DFS and BFS).
2. Learn how to implement Pre-order, In-order, Post-order, and Level-order traversals.
3. Master both recursive and iterative implementations.
4. Analyze time and space complexity of tree traversal algorithms.
5. Apply these patterns to solve complex tree problems.

Concept Explanation:
Tree Traversal is a process of visiting each node in a tree data structure exactly once.
- Depth-First Search (DFS) explores as far as possible along each branch before backtracking. It includes Pre-order (Node, Left, Right), In-order (Left, Node, Right), and Post-order (Left, Right, Node).
- Breadth-First Search (BFS) or Level-order traversal explores the tree level by level.
"""

import collections
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

# Basic Implementation: Recursive DFS Traversals
def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Time: O(N), Space: O(H) where H is tree height"""
    res = []
    def dfs(node):
        if not node: return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return res

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Time: O(N), Space: O(H)"""
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res

def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Time: O(N), Space: O(H)"""
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)
    dfs(root)
    return res

# Intermediate Implementation: BFS / Level-order Traversal
def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """Time: O(N), Space: O(W) where W is max width of tree"""
    if not root:
        return []
    res = []
    queue = collections.deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(level)
    return res

# Advanced Implementation: Iterative DFS Traversals
def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    res, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res

# Edge Cases to Handle:
# 1. Empty tree (root is None)
# 2. Skewed tree (all left or all right children)
# 3. Single node tree

# Interview Challenge: Serialize and Deserialize Binary Tree
class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        res = []
        def dfs(node):
            if not node:
                res.append("N")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        vals = data.split(",")
        self.i = 0
        def dfs():
            if vals[self.i] == "N":
                self.i += 1
                return None
            node = TreeNode(int(vals[self.i]))
            self.i += 1
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()

def run_tests():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    assert preorder_traversal(root) == [1, 2, 4, 5, 3]
    assert inorder_traversal(root) == [4, 2, 5, 1, 3]
    assert postorder_traversal(root) == [4, 5, 2, 3, 1]
    assert level_order_traversal(root) == [[1], [2, 3], [4, 5]]
    assert inorder_iterative(root) == [4, 2, 5, 1, 3]
    
    codec = Codec()
    s = codec.serialize(root)
    assert codec.serialize(codec.deserialize(s)) == s
    
    print("All Tree Traversal tests passed!")

if __name__ == "__main__":
    run_tests()
