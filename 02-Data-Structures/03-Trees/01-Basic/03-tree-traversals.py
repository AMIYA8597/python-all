"""
# ==============================================================================
# LABORATORY: ADVANCED TREE TRAVERSALS (ITERATIVE & MORRIS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Recursive Tree Traversals (DFS) are easy to write, but they rely on the OS Call 
# Stack. If a tree is 10,000 levels deep, a recursive function will throw a 
# `RecursionError` and crash the server. FAANG interviewers often explicitly ask: 
# "Now solve it iteratively using an explicit stack." 
# Furthermore, the legendary "Morris Traversal" achieves In-Order traversal using 
# O(1) auxiliary space (no stack at all!), which is a peak technical challenge.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement Iterative Pre-Order and In-Order traversals using a Stack.
# - Understand how an explicit stack prevents Recursion limits.
# - Master the Morris Traversal (O(1) Space In-Order).
#
# ==============================================================================
"""

from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE SETUP
# ==============================================================================
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def build_sample_tree() -> TreeNode:
    """
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
# 4. ITERATIVE TRAVERSALS (O(N) SPACE)
# ==============================================================================
def iterative_preorder(root: Optional[TreeNode]) -> List[int]:
    """
    Pre-order: ROOT, LEFT, RIGHT.
    Iterative strategy: 
    1. Push root to stack.
    2. Pop node, process it.
    3. Push RIGHT child, then LEFT child (so left is popped first due to LIFO).
    """
    if not root:
        return []
        
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Note the reverse order! We want to process left first, so we push right first.
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
            
    return result

def iterative_inorder(root: Optional[TreeNode]) -> List[int]:
    """
    In-order: LEFT, ROOT, RIGHT.
    Iterative strategy:
    1. Dive as far left as possible, pushing all nodes to the stack.
    2. When you hit a dead end, pop the stack, process the node.
    3. Move to the right child and repeat.
    """
    result = []
    stack = []
    curr = root
    
    while curr or stack:
        # Dive left
        while curr:
            stack.append(curr)
            curr = curr.left
            
        # Hit a dead end. Pop and process.
        curr = stack.pop()
        result.append(curr.val)
        
        # Move right
        curr = curr.right
        
    return result

def demonstrate_iterative():
    section_header("Iterative Traversals (Explicit Stack)")
    root = build_sample_tree()
    print(f"Iterative Pre-order: {iterative_preorder(root)}")
    print(f"Iterative In-order:  {iterative_inorder(root)}")


# ==============================================================================
# 5. MORRIS TRAVERSAL (O(1) SPACE)
# ==============================================================================
def morris_inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    The legendary Morris Traversal. 
    Time: O(N) | Space: O(1) (No recursion, no stack!)
    
    How does it work?
    If we dive left, how do we find our way back up without a stack? 
    We temporarily modify the tree! We find the node's "In-Order Predecessor" 
    (the rightmost node in its left subtree) and wire its `next` pointer to 
    the current node. When we return via this temporary bridge, we delete it 
    to restore the tree structure.
    """
    result = []
    curr = root
    
    while curr:
        if curr.left is None:
            # No left child? Process node and move right.
            result.append(curr.val)
            curr = curr.right
        else:
            # Find the In-Order Predecessor
            pre = curr.left
            while pre.right and pre.right != curr:
                pre = pre.right
                
            if pre.right is None:
                # 1. Establish the temporary bridge
                pre.right = curr
                curr = curr.left
            else:
                # 2. We hit the bridge! The left side is done.
                # Destroy the bridge to restore original tree structure.
                pre.right = None
                result.append(curr.val) # Process node
                curr = curr.right       # Move right
                
    return result

def demonstrate_morris():
    section_header("Morris Traversal (O(1) Space In-Order)")
    root = build_sample_tree()
    print("Executing Morris Traversal (Temporarily mutating tree pointers)...")
    print(f"Result: {morris_inorder_traversal(root)}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is an Iterative Pre-Order traversal safer than a Recursive one?
   Answer: A Recursive traversal uses the Python Call Stack, which will throw a `RecursionError` if the tree is heavily unbalanced (e.g., thousands of nodes deep). An Iterative traversal allocates its Stack on the heap memory, allowing it to scale indefinitely.

2. In an Iterative Pre-Order traversal, why do we push the right child to the stack BEFORE the left child?
   Answer: Because a Stack is LIFO (Last-In, First-Out). To ensure the left child is processed immediately on the next iteration, it must be at the very top of the stack, meaning it must be pushed last.

3. How does Morris Traversal achieve O(1) auxiliary space?
   Answer: Instead of using a Stack to remember where to return to after exploring a left subtree, it finds the right-most leaf of the left subtree and temporarily points it back to the root node (creating a threaded bridge). It destroys this bridge on the way back up to restore the tree.
"""

if __name__ == "__main__":
    demonstrate_iterative()
    demonstrate_morris()
    print("\n[SUCCESS] Laboratory: Advanced Traversals Completed.")
