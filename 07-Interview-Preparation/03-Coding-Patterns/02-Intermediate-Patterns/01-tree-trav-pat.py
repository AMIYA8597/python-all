"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - TREE TRAVERSALS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Traverse a Binary Tree in Level-Order (BFS)."
#
# A junior engineer uses a standard Python List as a Queue. They write `queue.pop(0)`.
# Because `pop(0)` is an O(N) memory shifting operation, traversing a tree with 
# 1 Million nodes results in O(N^2) time complexity. The server crashes.
# You MUST use `collections.deque` for mathematically perfect O(1) Queue operations.
#
# Interviewer: "Now write an In-Order Traversal (DFS), but DO NOT use Recursion."
# 
# Recursion in Python is inherently dangerous due to the strict Recursion Limit 
# (default 1000 frames). If the Tree is highly unbalanced (like a Linked List), 
# a recursive DFS will violently crash with a `RecursionError`. A senior engineer 
# knows how to manually simulate the CPU Call Stack using a pure `While` loop 
# and a Heap-allocated List, achieving infinite depth traversal!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Breadth-First Search (BFS) using `collections.deque`.
# - Master Depth-First Search (DFS) Iteratively (Simulating the Call Stack).
# - Understand Pre-Order, In-Order, and Post-Order algorithmic rules.
#
# ==============================================================================
"""

import collections
from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BINARY TREE ARCHITECTURE
# ==============================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_sample_tree() -> TreeNode:
    """
    Builds the following tree:
            1
          /   \
         2     3
        / \   / \
       4   5 6   7
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    return root


# ==============================================================================
# 4. BREADTH-FIRST SEARCH (BFS - LEVEL ORDER)
# ==============================================================================
def bfs_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Time: O(N) | Space: O(W) where W is max width of tree (O(N) in worst case)
    BFS uses a QUEUE (First-In, First-Out).
    """
    if not root: return []
    
    result = []
    # CRITICAL: We MUST use deque. A list pop(0) would cause O(N^2) disaster!
    queue = collections.deque([root])
    
    level = 0
    while queue:
        # We mathematically freeze the size of the queue for this specific level!
        level_size = len(queue)
        current_level_vals = []
        
        print(f"  Level {level} Processing {level_size} node(s)...")
        
        # Process ONLY the nodes that were in the queue at the start of this level!
        for _ in range(level_size):
            # O(1) Pop from the front!
            node = queue.popleft()
            current_level_vals.append(node.val)
            
            # Enqueue the children for the NEXT level
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
            
        result.append(current_level_vals)
        print(f"    -> Extracted: {current_level_vals}")
        level += 1
        
    return result

def demonstrate_bfs():
    section_header("Breadth-First Search (Level-Order)")
    root = build_sample_tree()
    print("Tree Structure: 1 -> (2,3) -> (4,5,6,7)\n")
    
    result = bfs_level_order(root)
    print(f"\nFinal BFS Matrix: {result}")


# ==============================================================================
# 5. DEPTH-FIRST SEARCH (DFS - ITERATIVE IN-ORDER)
# ==============================================================================
def dfs_inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    Time: O(N) | Space: O(H) where H is the height of the tree.
    In-Order: Left -> Node -> Right.
    We are mathematically simulating the CPU Call Stack using a list `stack`!
    """
    result = []
    stack = []
    current = root
    
    print("  Beginning iterative traversal (Simulating the CPU stack)...")
    
    while current or stack:
        # 1. Dive as deep to the LEFT as mathematically possible!
        while current:
            stack.append(current)
            current = current.left
            
        # 2. We hit rock bottom. Pop the top of the stack (The Left-most node!)
        current = stack.pop()
        
        # 3. Process the Node!
        print(f"    -> Visiting Node: {current.val}")
        result.append(current.val)
        
        # 4. Now, explore its Right branch!
        current = current.right
        
    return result

def demonstrate_dfs():
    section_header("Depth-First Search (Iterative In-Order)")
    root = build_sample_tree()
    print("Tree Structure: 1 -> (2,3) -> (4,5,6,7)")
    print("Expected In-Order: 4, 2, 5, 1, 6, 3, 7\n")
    
    result = dfs_inorder_iterative(root)
    print(f"\nFinal DFS Array: {result}")


def run_all_labs():
    demonstrate_bfs()
    demonstrate_dfs()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the physical architectural difference between BFS and DFS in memory?"
   Senior Answer: "BFS uses a Queue (First-In, First-Out). It expands horizontally, meaning it must store an entire 'Level' of the tree in memory at once. At the absolute bottom of a balanced binary tree, the last level contains $N/2$ nodes, meaning BFS requires $O(N)$ Space. DFS uses a Stack (Last-In, First-Out). It dives vertically. It only needs to store the current path of nodes from the Root down to the leaf. In a perfectly balanced tree, the maximum height is $\\log N$, meaning DFS only requires $O(\\log N)$ Space! DFS is vastly more memory-efficient for deep, balanced trees."

2. Interviewer: "Why would an interviewer specifically ask you to write DFS iteratively instead of recursively?"
   Senior Answer: "Recursion utilizes the physical CPU Call Stack. In Python, the CPython interpreter mathematically hardcodes the Recursion Limit to 1000 frames to prevent `StackOverflow` C-level crashes. If the Binary Tree degrades into a straight Linked List (e.g., every node only has a Right child), and there are 1,001 nodes, the recursive function will violently crash the server with a `RecursionError`. By writing it iteratively, we manually simulate the Call Stack using a standard Heap-allocated Python List (`stack = []`). The Heap is only constrained by the physical RAM of the server, allowing the Iterative DFS to safely traverse trees that are millions of layers deep."

3. Interviewer: "When traversing a Binary Search Tree (BST), what unique mathematical property does an In-Order traversal possess?"
   Senior Answer: "In a Binary Search Tree, all Left children are mathematically smaller than the Parent, and all Right children are larger. An In-Order Traversal strictly visits `Left -> Node -> Right`. Therefore, it perfectly aligns with the mathematical constraints of the BST! If you run an In-Order Traversal on a valid BST, the resulting output array is mathematically guaranteed to be perfectly sorted in Ascending order. If the output array drops in value at any point, the BST is invalid."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Tree Traversals) Completed.")
