"""
# ==============================================================================
# LABORATORY: BINARY TREES & TRAVERSALS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Linked List is a 1-dimensional data structure (each node points to 1 next node).
# A Binary Tree is a 2-dimensional data structure (each node points to up to 2 
# children). Trees represent hierarchical data: File Systems, HTML DOM (Document 
# Object Model), Abstract Syntax Trees (Compilers), and JSON payloads. 
# Mastering Tree Traversals (DFS and BFS) is arguably the most tested skill in 
# software engineering interviews.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a Binary Tree Node.
# - Master Depth-First Search (DFS) Traversals: Pre-order, In-order, Post-order.
# - Master Breadth-First Search (BFS) Traversal: Level-order using a Queue.
# - Solve a classic FAANG problem: Maximum Depth of Binary Tree.
#
# ==============================================================================
"""

from collections import deque
from typing import Optional, List, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE NODE & MANUAL CONSTRUCTION
# ==============================================================================
class TreeNode:
    """The fundamental building block of a Binary Tree."""
    def __init__(self, val: Any = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def build_sample_tree() -> TreeNode:
    """
    Builds the following tree:
            1
          /   \
         2     3
        / \     \
       4   5     6
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    root.right.right = TreeNode(6)
    return root


# ==============================================================================
# 4. DEPTH-FIRST SEARCH (DFS) TRAVERSALS
# ==============================================================================
# DFS dives as deep as possible down one branch before backtracking.
# Implemented using the Call Stack (Recursion).

def preorder_traversal(root: Optional[TreeNode]) -> List[Any]:
    """Pre-order: ROOT, LEFT, RIGHT. (Used to copy a tree)."""
    if not root:
        return []
    # Process the node BEFORE processing children
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)

def inorder_traversal(root: Optional[TreeNode]) -> List[Any]:
    """In-order: LEFT, ROOT, RIGHT. (Used to get sorted data out of a BST)."""
    if not root:
        return []
    # Process the node BETWEEN processing children
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)

def postorder_traversal(root: Optional[TreeNode]) -> List[Any]:
    """Post-order: LEFT, RIGHT, ROOT. (Used to safely delete a tree from the bottom up)."""
    if not root:
        return []
    # Process the node AFTER processing children
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.val]

def demonstrate_dfs():
    section_header("Depth-First Search (DFS) Traversals")
    
    root = build_sample_tree()
    print("Tree Structure:")
    print("        1        ")
    print("      /   \\     ")
    print("     2     3     ")
    print("    / \\     \\  ")
    print("   4   5     6   \n")
    
    print(f"Pre-order (Root-Left-Right): {preorder_traversal(root)}")
    print(f"In-order (Left-Root-Right):  {inorder_traversal(root)}")
    print(f"Post-order (Left-Right-Root):{postorder_traversal(root)}")


# ==============================================================================
# 5. BREADTH-FIRST SEARCH (BFS) TRAVERSAL
# ==============================================================================
# BFS explores horizontally, level-by-level.
# Implemented using a Queue.

def level_order_traversal(root: Optional[TreeNode]) -> List[List[Any]]:
    """
    LeetCode #102: Binary Tree Level Order Traversal.
    Returns a list of lists, where each inner list contains the nodes at that depth.
    """
    if not root:
        return []
        
    result = []
    # Initialize queue with the root
    queue = deque([root])
    
    while queue:
        # The number of elements currently in the queue is exactly the number 
        # of nodes at the CURRENT level!
        level_size = len(queue)
        current_level_vals = []
        
        # Process ONLY the nodes at the current level
        for _ in range(level_size):
            node = queue.popleft()
            current_level_vals.append(node.val)
            
            # Queue up the children for the NEXT level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        # Append the completed level to the final result
        result.append(current_level_vals)
        
    return result

def demonstrate_bfs():
    section_header("Breadth-First Search (BFS) / Level-Order Traversal")
    
    root = build_sample_tree()
    levels = level_order_traversal(root)
    
    for i, level in enumerate(levels):
        print(f"Level {i}: {level}")


# ==============================================================================
# 6. CLASSIC INTERVIEW PROBLEM: MAXIMUM DEPTH
# ==============================================================================
def max_depth(root: Optional[TreeNode]) -> int:
    """
    LeetCode #104: Maximum Depth of Binary Tree.
    Time Complexity: O(N) (Must visit every node).
    Space Complexity: O(H) where H is the height of the tree (Call Stack depth).
    """
    # Base case: an empty tree has a depth of 0
    if not root:
        return 0
        
    # The depth of the current node is 1 + the max depth of its deepest child
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return 1 + max(left_depth, right_depth)

def demonstrate_max_depth():
    section_header("Algorithm: Maximum Depth")
    
    root = build_sample_tree()
    print(f"The maximum depth (height) of the tree is: {max_depth(root)}")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What dictates whether a DFS traversal is Pre-order, In-order, or Post-order?
   Answer: It depends entirely on WHEN the current node's value is processed relative to the recursive calls. Pre-order processes the node FIRST. In-order processes it BETWEEN the left and right children. Post-order processes it LAST.

2. Why do we use a Queue (deque) for BFS / Level-Order traversal?
   Answer: Because we want to process nodes First-In, First-Out. We want to process all nodes at Depth 1 before we process any nodes at Depth 2. A Queue ensures that the children (Depth 2) that get pushed onto the back of the queue wait until the parents (Depth 1) are popped off the front.

3. What is the Space Complexity of a recursive DFS algorithm?
   Answer: The space complexity is O(H), where H is the maximum height of the tree. This is because the recursive function calls stack up in memory. In a perfectly balanced tree, H = log(N). In the worst-case (a completely unbalanced tree that looks like a linked list), H = N.
"""

if __name__ == "__main__":
    demonstrate_dfs()
    demonstrate_bfs()
    demonstrate_max_depth()
    print("\n[SUCCESS] Laboratory: Binary Trees Completed.")
