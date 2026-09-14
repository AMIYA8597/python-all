"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - TREE MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Medium" Tree problems test your ability to maintain mathematical constraints 
# during deep recursion. A binary tree is just structural, but a Binary Search 
# Tree (BST) has strict mathematical laws: Everything on the left MUST be smaller, 
# and everything on the right MUST be larger.
#
# A junior engineer validates a BST by only checking if a parent is greater than 
# its immediate left child and smaller than its immediate right child. This 
# catastrophically fails when a right-child's left-child violates the absolute 
# Root constraint!
#
# A senior engineer uses Mathematical Bounding. They pass a strict (MIN, MAX) 
# boundary down the recursive call stack. Every single node mathematically checks 
# itself against the global boundaries before dynamically tightening them for 
# its children, solving it in a flawless O(N) pass.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Mathematical Bounding limits (Validate BST).
# - Master recursive state bubbling (Lowest Common Ancestor).
# - Master Queue-based BFS (Level Order Traversal).
#
# ==============================================================================
"""

import collections
from typing import Optional, List

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
    if root is not None:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            print_tree(root.left, level + 1, "L--- ")
            print_tree(root.right, level + 1, "R--- ")


# ==============================================================================
# 4. VALIDATE BINARY SEARCH TREE (MATHEMATICAL BOUNDING)
# ==============================================================================
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Time: O(N) | Space: O(H) Call Stack
    Given the root of a binary tree, determine if it is a valid binary search tree (BST).
    """
    
    # We must track the absolute lower and upper bounds dynamically!
    def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
        # Base Case: An empty node is mathematically valid!
        if not node:
            return True
            
        print(f"  -> Validating Node [{node.val}]. Must be strictly between ({low}, {high})")
        
        # 1. THE CONSTRAINT CHECK
        if not (low < node.val < high):
            print(f"    -> [FATAL ERROR] Node {node.val} violates the boundaries!")
            return False
            
        # 2. RECURSIVE TIGHTENING
        # Left Child: Must be strictly LESS than the current node. 
        #   The high boundary tightens to `node.val`!
        left_is_valid = validate(node.left, low, node.val)
        
        # Right Child: Must be strictly GREATER than the current node.
        #   The low boundary tightens to `node.val`!
        right_is_valid = validate(node.right, node.val, high)
        
        return left_is_valid and right_is_valid

    # Start with absolute infinite boundaries!
    return validate(root, float('-inf'), float('inf'))

def demonstrate_bst():
    section_header("Medium: Validate Binary Search Tree (O(N))")
    
    # INVALID Tree Example:
    #      5
    #     / \
    #    4   6
    #       / \
    #      3   7
    # Note: 3 is the LEFT child of 6 (valid locally), but it is on the RIGHT 
    # side of 5 (violates global rule)!
    root = TreeNode(5)
    root.left = TreeNode(4)
    root.right = TreeNode(6, TreeNode(3), TreeNode(7))
    
    print("Tree Architecture:")
    print_tree(root)
    print()
    
    ans = is_valid_bst(root)
    print(f"\nResult: {ans} (Expected: False)")


# ==============================================================================
# 5. LOWEST COMMON ANCESTOR OF A BINARY TREE (RECURSIVE BUBBLING)
# ==============================================================================
def lowest_common_ancestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    """
    Time: O(N) | Space: O(H)
    Find the lowest common ancestor (LCA) of two given nodes p and q.
    """
    # 1. BASE CASES
    # If we hit the bottom, return None.
    # If we FIND either node P or node Q, instantly return that node upwards!
    if not root or root == p or root == q:
        return root
        
    # 2. RECURSIVE SEARCH
    # Send scouts down the left and right branches!
    left_result = lowest_common_ancestor(root.left, p, q)
    right_result = lowest_common_ancestor(root.right, p, q)
    
    # 3. EVALUATION
    if left_result and right_result:
        # P was found in one branch, and Q was found in the other branch!
        # Mathematically, the current node MUST be the divergence point (the LCA)!
        print(f"  -> [LCA FOUND] Node {root.val} bridges Left ({left_result.val}) and Right ({right_result.val})")
        return root
        
    # Otherwise, return whichever scout successfully found something!
    # If both found nothing, this returns None.
    return left_result if left_result else right_result

def demonstrate_lca():
    section_header("Medium: Lowest Common Ancestor (Recursive Bubbling)")
    
    # Build Tree:
    #       3
    #      / \
    #     5   1
    #    / \ / \
    #   6  2 0  8
    #     / \
    #    7   4
    root = TreeNode(3)
    p = TreeNode(5)
    p.left = TreeNode(6)
    
    node2 = TreeNode(2, TreeNode(7), TreeNode(4))
    q = node2.right # node 4!
    
    p.right = node2
    
    root.left = p
    root.right = TreeNode(1, TreeNode(0), TreeNode(8))
    
    print(f"Searching for LCA of [{p.val}] and [{q.val}]")
    ans = lowest_common_ancestor(root, p, q)
    print(f"\nResult: LCA Node is [{ans.val}] (Expected: 5)")


# ==============================================================================
# 6. BINARY TREE LEVEL ORDER TRAVERSAL (QUEUE BFS)
# ==============================================================================
def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Time: O(N) | Space: O(W) where W is the maximum width of the tree.
    Returns the level order traversal of its nodes' values (Left to Right, level by level).
    """
    if not root: return []
    
    result = []
    
    # We MUST use a Deque for strict O(1) pops from the front!
    queue = collections.deque([root])
    
    level_depth = 0
    while queue:
        # Freeze the number of nodes CURRENTLY in the queue!
        # These are ALL the nodes for the current horizontal level.
        level_size = len(queue)
        current_level_values = []
        
        print(f"  Processing Level {level_depth} (Size: {level_size})")
        
        # Process ONLY the nodes that were present at the start of this level!
        for _ in range(level_size):
            node = queue.popleft()
            current_level_values.append(node.val)
            
            # Queue up the children for the NEXT level!
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
            
        result.append(current_level_values)
        level_depth += 1
        
    return result

def demonstrate_level_order():
    section_header("Medium: Level Order Traversal (Queue BFS)")
    
    #      3
    #     / \
    #    9  20
    #      /  \
    #     15   7
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    
    ans = level_order(root)
    print(f"\nResult: {ans}")


def run_all_labs():
    demonstrate_bst()
    demonstrate_lca()
    demonstrate_level_order()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Validate BST, why is checking `node.left.val < node.val < node.right.val` structurally insufficient?"
   Senior Answer: "That logic only validates the immediate local relationship between a parent and its direct children. In a Binary Search Tree, the rules are global. The absolute Root node establishes a permanent boundary for the entire tree: every single descendant on the left branch, no matter how deep, MUST be smaller than the Root. If you only check immediate children, a node 5 levels deep on the left side could easily be larger than the Root, silently violating the fundamental laws of a BST. By passing the `(low, high)` boundaries down the Call Stack, we mathematically enforce the global constraints upon every local node."

2. Interviewer: "In Lowest Common Ancestor, if the tree was actually a Binary Search Tree (BST) instead of a standard Binary Tree, how could you optimize the algorithm?"
   Senior Answer: "If the tree is a BST, we do not need to use $O(N)$ Recursive Bubbling to blindly scout both branches. A BST is already sorted! We simply look at the current node's value. If `p` and `q` are BOTH smaller than the current node, the LCA is mathematically guaranteed to be in the Left branch. If they are BOTH larger, the LCA is in the Right branch. If one is smaller and one is larger, it means the paths to `p` and `q` physically diverge at the current node! The exact point of divergence is mathematically the Lowest Common Ancestor. This allows us to traverse straight down a single path without branching, crushing the time complexity from $O(N)$ down to $O(\\log N)$."

3. Interviewer: "In Level Order Traversal (BFS), why do we execute `level_size = len(queue)` at the beginning of the `while` loop, instead of just popping from the queue dynamically?"
   Senior Answer: "If we don't freeze the `level_size` into a static integer, the `for` loop will become chaotic. As we pop nodes from the current level, we are simultaneously appending their children (the next level) into the exact same queue. If we loop based on the dynamic length of the queue, the loop will never terminate for the current level; it will seamlessly bleed into processing the children, and then the grandchildren, destroying the horizontal level grouping completely. By capturing the exact size of the queue *before* the loop starts, we guarantee that the `for` loop executes exactly the correct number of times to drain only the current level, completely ignoring the newly appended children until the next iteration of the outer `while` loop."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Tree Medium) Completed.")
