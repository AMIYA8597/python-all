"""
Tree Dynamic Programming (Tree DP)

Concept Explanation:
Tree DP is an advanced dynamic programming technique used when the problem is defined on a tree graph.
Since trees have a natural recursive structure (a node and its subtrees), we can define a DP state for each node 
based on the results computed for its children. 
Generally, Tree DP is done using Depth-First Search (DFS). The DP values are propagated from the leaves to the root.

Common State definitions:
dp[u][0]: The optimal answer for the subtree rooted at `u`, assuming `u` is NOT included in the solution.
dp[u][1]: The optimal answer for the subtree rooted at `u`, assuming `u` IS included in the solution.

Learning Objectives:
1. Understand how to traverse a tree and build a DP state recursively.
2. Solve the "Maximum Independent Set on a Tree" (or House Robber III) problem.
3. Analyze time and space complexity of Tree DP (typically O(V) or O(V+E)).
4. Recognize how to handle undirected trees without parent pointers using a `parent` parameter in DFS.

Industry Use Cases:
- Network routing and hierarchical resource allocation.
- Organizational structure optimization (e.g., inviting non-conflicting employees to a party).
- Syntax tree analysis in compilers.
"""

from typing import List, Dict, Optional, Tuple

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right


def rob_binary_tree(root: Optional[TreeNode]) -> int:
    """
    House Robber III: Find the maximum amount of money the thief can rob without robbing 
    two directly connected nodes (Maximum Independent Set on a Binary Tree).
    
    Time Complexity: O(N) where N is the number of nodes.
    Space Complexity: O(H) where H is the height of the tree (for recursion stack).
    """
    def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
        # Returns a tuple: (max_val_without_node, max_val_with_node)
        if not node:
            return (0, 0)
        
        left_without, left_with = dfs(node.left)
        right_without, right_with = dfs(node.right)
        
        # If we don't rob this node, we can choose to rob or not rob its children
        without_node = max(left_without, left_with) + max(right_without, right_with)
        
        # If we rob this node, we CANNOT rob its children
        with_node = node.val + left_without + right_without
        
        return (without_node, with_node)

    return max(dfs(root))


def max_independent_set_n_ary_tree(n: int, edges: List[List[int]], weights: List[int]) -> int:
    """
    Maximum Independent Set on a general N-ary Tree (represented as an undirected graph).
    Given `n` nodes (0 to n-1) and their weights, pick a subset of nodes with max weight such that 
    no two nodes share an edge.
    
    Time Complexity: O(N)
    Space Complexity: O(N) for adjacency list, DP arrays, and recursion stack.
    """
    # Build adjacency list
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # dp[u][0] = max weight in subtree u not including u
    # dp[u][1] = max weight in subtree u including u
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(u: int, p: int) -> None:
        dp[u][1] = weights[u]
        dp[u][0] = 0
        
        for v in adj[u]:
            if v == p:
                continue
            dfs(v, u)
            # If we don't include u, we can either include or not include v
            dp[u][0] += max(dp[v][0], dp[v][1])
            # If we include u, we CANNOT include v
            dp[u][1] += dp[v][0]

    if n == 0: return 0
    # Root the tree arbitrarily at node 0
    dfs(0, -1)
    
    return max(dp[0][0], dp[0][1])


# -----------------------------------------------------------------------------
# Interview Challenge: Tree Diameter using DP
# -----------------------------------------------------------------------------
# Find the longest path between any two nodes in a tree.

def tree_diameter(n: int, edges: List[List[int]]) -> int:
    """
    Computes the diameter of a tree (number of edges in the longest path).
    """
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    diameter = 0
    
    def dfs(u: int, p: int) -> int:
        nonlocal diameter
        max_1 = 0
        max_2 = 0
        
        for v in adj[u]:
            if v == p: continue
            depth = dfs(v, u)
            if depth > max_1:
                max_2 = max_1
                max_1 = depth
            elif depth > max_2:
                max_2 = depth
                
        # Update diameter with the path passing through `u`
        diameter = max(diameter, max_1 + max_2)
        # Return depth of subtree rooted at `u`
        return max_1 + 1

    if n > 0:
        dfs(0, -1)
        
    return diameter


if __name__ == "__main__":
    print("--- House Robber III (Binary Tree) ---")
    # Tree:
    #     3
    #    / \
    #   2   3
    #    \   \ 
    #     3   1
    root = TreeNode(3)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(1)
    
    ans = rob_binary_tree(root)
    assert ans == 7 # (3 + 3 + 1)
    print("Max robbed amount:", ans)
    
    print("\n--- Max Independent Set (N-ary Tree) ---")
    edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]]
    weights = [10, 20, 30, 40, 50, 60]
    # Optimal: pick 4(50), 3(40), 5(60), 0(10) -> Total 160
    # Or maybe 1(20), 5(60) -> 80
    ans_n_ary = max_independent_set_n_ary_tree(6, edges, weights)
    print("Max weight independent set:", ans_n_ary)
    assert ans_n_ary == 160
    
    print("\n--- Tree Diameter ---")
    edges_diam = [[0,1], [1,2], [2,3], [1,4], [4,5]]
    diam = tree_diameter(6, edges_diam)
    print("Tree Diameter:", diam)
    assert diam == 4 # path: 3-2-1-4-5
    
    print("\nAll Tree DP tests passed!")
