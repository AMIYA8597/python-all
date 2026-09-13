"""
# ==============================================================================
# LABORATORY: TREE DP (DYNAMIC PROGRAMMING ON TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen DP on 1D Arrays (Fibonacci) and 2D Grids (LCS, Min Path Sum).
# But what if the data is a Tree?
#
# Classic Problem: "House Robber III" (or Maximum Independent Set of a Tree).
# You are a thief. You found a neighborhood where the houses are laid out in a 
# Binary Tree. If you rob a house, you trigger the alarm if you also rob its 
# DIRECT children. (You cannot rob two connected nodes).
#
# How do you maximize your profit?
# 
# A naive algorithm would try every combination (O(2^N)).
# DP on Trees uses a Post-Order DFS (Depth First Search). 
# At every single node, we calculate exactly TWO states simultaneously:
# 1. What is the max profit of this subtree IF WE ROB this root node?
# 2. What is the max profit of this subtree IF WE DO NOT ROB this root node?
# 
# We return both states as a Tuple up the recursion chain! This allows the parent 
# nodes to make mathematically perfect decisions in O(N) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Post-Order Traversal for Bottom-Up Tree DP.
# - Master State Tuples `(robbed, not_robbed)`.
# - Implement the mathematical transition across parent/child nodes.
#
# ==============================================================================
"""

from typing import Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BINARY TREE STRUCTURE
# ==============================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ==============================================================================
# 4. TREE DP (POST-ORDER STATE TUPLES)
# ==============================================================================
def rob_tree(root: Optional[TreeNode]) -> int:
    """
    Time Complexity: O(N) where N is the number of nodes.
    Space Complexity: O(H) where H is the height of the tree (Call Stack).
    """
    
    def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
        """
        Returns a tuple of two integers: (rob_this_node, do_not_rob_this_node).
        """
        # 1. BASE CASE
        # A null node yields $0 if robbed, and $0 if not robbed.
        if not node:
            return (0, 0)
            
        # 2. POST-ORDER TRAVERSAL (BOTTOM-UP)
        # We MUST go all the way down to the leaves first. We cannot make a 
        # decision about the current house until we know the optimal profits 
        # of the subtrees below it!
        left_robbed, left_not_robbed = dfs(node.left)
        right_robbed, right_not_robbed = dfs(node.right)
        
        # 3. STATE TRANSITION EQUATIONS
        
        # Scenario A: WE ROB THE CURRENT NODE.
        # If we rob this node, we CANNOT rob its direct children.
        # So we MUST take the `not_robbed` profits from the left and right children.
        rob_current = node.val + left_not_robbed + right_not_robbed
        
        # Scenario B: WE DO NOT ROB THE CURRENT NODE.
        # If we skip this node, we have total freedom! We CAN rob the children, 
        # but we don't HAVE to. We should take whatever scenario yielded the most 
        # money for the left child, and whatever yielded the most for the right child.
        not_rob_current = max(left_robbed, left_not_robbed) + max(right_robbed, right_not_robbed)
        
        # 4. RETURN THE TUPLE STATE UPWARDS
        return (rob_current, not_rob_current)

    # The dfs function returns the two final states for the entire tree.
    # We just return the maximum of the two!
    final_robbed, final_not_robbed = dfs(root)
    return max(final_robbed, final_not_robbed)


def demonstrate_tree_dp():
    section_header("Algorithm: Tree DP (House Robber III)")
    
    # Tree Structure:
    #       3
    #      / \
    #     2   3
    #      \   \ 
    #       3   1
    
    root = TreeNode(3)
    root.left = TreeNode(2, right=TreeNode(3))
    root.right = TreeNode(3, right=TreeNode(1))
    
    print("Tree Structure:")
    print("      $3")
    print("     /  \\")
    print("   $2    $3")
    print("    \\     \\")
    print("    $3    $1")
    
    ans = rob_tree(root)
    
    print(f"\nMaximum Profit: ${ans} (Expected: 7)")
    print("Optimal Strategy: Rob the root ($3), the bottom-left ($3), and the bottom-right ($1).")
    
    # Tree 2:
    #       3
    #      / \
    #     4   5
    #    / \   \ 
    #   1   3   1
    root2 = TreeNode(3)
    root2.left = TreeNode(4, left=TreeNode(1), right=TreeNode(3))
    root2.right = TreeNode(5, right=TreeNode(1))
    
    print("\nTree Structure 2:")
    print("       $3")
    print("      /  \\")
    print("    $4    $5")
    print("   /  \\     \\")
    print(" $1   $3    $1")
    
    ans2 = rob_tree(root2)
    print(f"\nMaximum Profit: ${ans2} (Expected: 9)")
    print("Optimal Strategy: Rob $4 and $5. (Skip the root, skip the leaves).")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Tree DP require a Post-Order DFS?
   Answer: In Dynamic Programming, you cannot calculate the State of a problem until the Sub-problems are fully solved. A Tree's sub-problems are its children. Pre-Order processes the Root first. Post-Order processes the Children first, allowing the mathematical answers to flow Bottom-Up from the leaves to the root.

2. Why is the `not_rob_current` equation `max(rob, not_rob) + max(rob, not_rob)`? Why not just `rob + rob`?
   Answer: Just because you DON'T rob the parent, doesn't mean you are mathematically FORCED to rob the child! If a child has a negative value, or if skipping the child unlocks an ultra-wealthy grandchild, the optimal math might be to skip the parent AND skip the child. The `max()` function guarantees we always take the absolute best path, regardless of whether it involved robbing the child or not.

3. Is the Space Complexity $O(1)$ since we didn't allocate an array?
   Answer: NO. The Space Complexity is $O(H)$ where $H$ is the height of the tree. The DFS algorithm uses the Operating System's Call Stack to maintain state. In a completely unbalanced tree (a straight line), the height is $N$, so it takes $O(N)$ memory and could trigger a Stack Overflow.
"""

if __name__ == "__main__":
    demonstrate_tree_dp()
    print("\n[SUCCESS] Laboratory: Tree DP Completed.")
