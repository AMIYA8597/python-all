"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - TREE EASY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Binary Trees are the absolute foundation of recursive thinking. Almost all 
# tree problems can be solved by recognizing that a Tree is just a collection 
# of smaller, mathematically identical Sub-Trees.
#
# A junior engineer tries to traverse a tree using complex global variables 
# and iterative loops, getting tangled in pointer states and edge cases.
#
# A senior engineer uses pure Mathematical Recursion. They trust the Call Stack 
# to maintain the state. By defining a strict Base Case (`if not root: return`) 
# and formulating a mathematical relationship between the current Node and its 
# Left/Right children, they reduce 50 lines of iterative code down to 4 lines 
# of flawless recursive logic.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Mathematical Recursion (Maximum Depth).
# - Master pointer swapping in Trees (Invert Binary Tree).
# - Master parallel recursion (Symmetric Tree).
#
# ==============================================================================
"""

from typing import Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE ARCHITECTURE & HELPERS
# ==============================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def print_tree(root: Optional[TreeNode], level=0, prefix="Root: "):
    """Helper to visualize the tree in the terminal."""
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")


# ==============================================================================
# 4. MAXIMUM DEPTH OF BINARY TREE (PURE RECURSION)
# ==============================================================================
def max_depth(root: Optional[TreeNode]) -> int:
    """
    Time: O(N) | Space: O(H) where H is the height of the tree (Call Stack)
    """
    # BASE CASE: If the node doesn't exist, its depth is exactly 0.
    if not root:
        return 0
        
    # RECURSIVE STEP: 
    # Mathematically ask the Left Child for its maximum depth.
    # Mathematically ask the Right Child for its maximum depth.
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    # The depth of the CURRENT node is 1 (itself) PLUS the deepest of its children!
    current_depth = 1 + max(left_depth, right_depth)
    
    print(f"  -> Node [{root.val}] computed Depth: {current_depth} (L:{left_depth}, R:{right_depth})")
    
    return current_depth

def demonstrate_max_depth():
    section_header("Easy: Maximum Depth of Binary Tree")
    
    # Build Tree:
    #       3
    #      / \
    #     9  20
    #       /  \
    #      15   7
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    
    print("Tree Architecture:")
    print_tree(root)
    print("\nExecuting Recursive Depth Calculation...")
    
    ans = max_depth(root)
    print(f"\nResult: {ans} (Expected: 3)")


# ==============================================================================
# 5. INVERT BINARY TREE (THE INFAMOUS INTERVIEW PROBLEM)
# ==============================================================================
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Time: O(N) | Space: O(H) Call Stack
    Max Howell (creator of Homebrew) famously failed a Google interview because 
    he couldn't invert a binary tree on a whiteboard.
    It is mathematically trivial if you understand recursion.
    """
    if not root:
        return None
        
    print(f"  -> Visiting Node [{root.val}]. Swapping Left/Right children...")
    
    # 1. SWAP THE POINTERS
    # Physically exchange the memory pointers in RAM!
    root.left, root.right = root.right, root.left
    
    # 2. RECURSE DOWNWARDS
    # Now that the current node is fixed, command the children to fix themselves!
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root

def demonstrate_invert_tree():
    section_header("Easy: Invert Binary Tree (Pointer Swapping)")
    
    # Build Tree:
    #       4
    #      / \
    #     2   7
    #    / \ / \
    #   1  3 6  9
    root = TreeNode(4)
    root.left = TreeNode(2, TreeNode(1), TreeNode(3))
    root.right = TreeNode(7, TreeNode(6), TreeNode(9))
    
    print("Original Tree:")
    print_tree(root)
    print("\nExecuting Inversion Engine...")
    
    inverted_root = invert_tree(root)
    
    print("\nInverted Tree (Mirrored!):")
    print_tree(inverted_root)


# ==============================================================================
# 6. SYMMETRIC TREE (PARALLEL RECURSION)
# ==============================================================================
def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Time: O(N) | Space: O(H)
    Check if a tree is a perfect mirror of itself around the center axis.
    """
    if not root: return True
    
    # We must deploy a helper function because we need to compare TWO nodes 
    # simultaneously (the left branch and the right branch)!
    def is_mirror(left_node: Optional[TreeNode], right_node: Optional[TreeNode]) -> bool:
        # BASE CASES
        if not left_node and not right_node:
            return True # Both hit NULL simultaneously. Perfect!
        if not left_node or not right_node:
            print("    -> [FAIL] One side hit NULL while the other had a node.")
            return False # Asymmetrical structure!
        if left_node.val != right_node.val:
            print(f"    -> [FAIL] Value mismatch! Left: {left_node.val}, Right: {right_node.val}")
            return False
            
        print(f"    -> [MATCH] Left [{left_node.val}] == Right [{right_node.val}]")
            
        # RECURSIVE STEP (The tricky part)
        # To be a mirror, the Outer-Left must match Outer-Right, AND 
        # the Inner-Right must match Inner-Left!
        outer_match = is_mirror(left_node.left, right_node.right)
        inner_match = is_mirror(left_node.right, right_node.left)
        
        return outer_match and inner_match
        
    return is_mirror(root.left, root.right)

def demonstrate_symmetric():
    section_header("Easy: Symmetric Tree (Parallel Recursion)")
    
    # Build Symmetric Tree:
    #       1
    #      / \
    #     2   2
    #    / \ / \
    #   3  4 4  3
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(3), TreeNode(4))
    root.right = TreeNode(2, TreeNode(4), TreeNode(3))
    
    print("Evaluating Tree Symmetry...")
    ans = is_symmetric(root)
    print(f"\nResult: {ans} (Expected: True)")


def run_all_labs():
    demonstrate_max_depth()
    demonstrate_invert_tree()
    demonstrate_symmetric()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Recursive Tree algorithms, what is the Space Complexity, and what defines it?"
   Senior Answer: "While the algorithm does not allocate extra Data Structures like Hash Maps or Arrays ($O(1)$ auxiliary space), true Space Complexity must account for the OS Call Stack. Every time a recursive function is called, the OS pushes a new frame onto the Stack. The maximum depth of this Stack is mathematically identical to the Maximum Height of the tree ($H$). If the tree is perfectly balanced, $H = \\log N$, making the Space Complexity $O(\\log N)$. However, if the tree is violently unbalanced (a straight line like a Linked List), $H = N$, driving the Space Complexity to a worst-case $O(N)$."

2. Interviewer: "In `invert_tree`, does it mathematically matter if we process the current node before we recurse on the children (Pre-Order), or if we recurse on the children first (Post-Order)?"
   Senior Answer: "For tree inversion, Pre-Order and Post-Order both mathematically work perfectly. If we use Pre-Order, we swap the left and right sub-trees at the root, and then recursively travel down the newly swapped branches to invert them internally. If we use Post-Order, we travel down to the absolute bottom leaves, invert them, and swap as we travel back up. The only approach that catastrophically fails is In-Order traversal (Left, Process, Right). If we process (swap) the node after returning from the Left branch, our 'new' Right branch is actually the *already processed* Left branch! When we recursively call the Right branch, we process the exact same branch twice, completely destroying the inversion!"

3. Interviewer: "Why does `is_symmetric` require a separate helper function with TWO parameters, when the original function only takes one?"
   Senior Answer: "Symmetry cannot be proven by looking at a single node in isolation. Symmetry is the mathematical equality of two completely distinct sub-trees. To evaluate equality, the execution context MUST hold simultaneous physical pointers to both the Left side of the tree and the Right side of the tree. The primary `is_symmetric(root)` function only has one pointer (`root`). By injecting `root.left` and `root.right` into a two-parameter helper function, we physically fork our traversal engine, allowing us to simultaneously push one pointer down the left flank and the other down the right flank to verify structural mirroring."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Tree Easy) Completed.")
