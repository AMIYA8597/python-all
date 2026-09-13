"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED DP: TREE DP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Normal Dynamic Programming problems are usually strictly linear (arrays) or 
# strictly rectangular (grids).
# 
# But what if the problem is physically structured as a Tree (an acyclic graph)?
# Example: "You are the CEO of a company. The company hierarchy is a Tree. 
# You want to invite employees to a party. If you invite a Manager, you CANNOT 
# invite their direct Subordinate (because it would be awkward). How do you 
# maximize the "fun rating" of the party?"
#
# This is the "Maximum Independent Set on a Tree" problem. 
# It cannot be solved with standard linear DP. You must execute DP recursively 
# via Depth-First Search (DFS) from the root down to the leaves, passing 
# calculated states UP the tree as the recursion backtracks!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Tree DP.
# - Master the "Take vs Don't Take" State passing from children to parents.
#
# ==============================================================================
"""

import sys
from collections import defaultdict

# Tree DP can go extremely deep. Always expand the recursion limit!
sys.setrecursionlimit(2000000)

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE DP (MAXIMUM INDEPENDENT SET)
# ==============================================================================
def maximize_party_fun(n: int, edges: list[list[int]], fun_ratings: list[int]) -> int:
    """
    Solves the Maximum Independent Set problem on a Tree.
    You cannot select two adjacent nodes (Manager and Direct Subordinate).
    
    Time Complexity: O(N) because every node is visited exactly once.
    Space Complexity: O(N) for recursion stack and DP array.
    """
    # 1. Build the Tree
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # DP Array
    # dp[node][0] = Max fun in the subtree rooted at `node` if we DO NOT invite `node`.
    # dp[node][1] = Max fun in the subtree rooted at `node` if we DO invite `node`.
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(node: int, parent: int) -> None:
        # Base Case Setup:
        # If we DO NOT invite the current node, we get 0 fun from this node.
        # If we DO invite the current node, we get its fun rating!
        dp[node][0] = 0
        dp[node][1] = fun_ratings[node]
        
        # Traverse down to all subordinates (children)
        for child in adj[node]:
            # Do not bounce back up to the manager!
            if child == parent:
                continue
                
            # Dive to the absolute bottom of the tree first! (Post-Order Traversal)
            dfs(child, node)
            
            # ------------------------------------------------------------------
            # STATE TRANSITION EQUATIONS (Backtracking)
            # ------------------------------------------------------------------
            
            # Scenario A: We DO NOT invite the current Node.
            # Because the Manager is absent, the Subordinate is completely free! 
            # We can EITHER invite the Subordinate OR not invite them. 
            # We greedily take whichever option yields the mathematically higher fun!
            dp[node][0] += max(dp[child][0], dp[child][1])
            
            # Scenario B: We DO invite the current Node.
            # Because the Manager is present, the Subordinate is STRICTLY FORBIDDEN!
            # We are mathematically forced to take the "DO NOT invite child" state.
            dp[node][1] += dp[child][0]

    # Assume Node 0 is the CEO (Root of the tree)
    dfs(0, -1)
    
    # The global maximum is either we invite the CEO or we don't.
    return max(dp[0][0], dp[0][1])

def demonstrate_tree_dp():
    section_header("Tree DP (Maximum Independent Set)")
    
    # Tree Structure:
    #      0 (CEO, Fun: 10)
    #     / \
    #    /   \
    #   1     2 (Managers, Fun: 50, 40)
    #  / \   / \
    # 3   4 5   6 (Interns, Fun: 20, 20, 30, 30)
    
    fun_ratings = [10, 50, 40, 20, 20, 30, 30]
    edges = [
        [0, 1], [0, 2],
        [1, 3], [1, 4],
        [2, 5], [2, 6]
    ]
    
    print("Tree Hierarchy with Fun Ratings:")
    for i, fun in enumerate(fun_ratings):
        print(f"Employee {i} has Fun Rating: {fun}")
        
    ans = maximize_party_fun(7, edges, fun_ratings)
    
    print(f"\nAbsolute Maximum Party Fun: {ans}")
    
    # Why?
    # If we take CEO (10) + Interns (20+20+30+30) = 110.
    # If we take Managers (50+40) = 90.
    # Therefore, taking the CEO + Interns is optimal!


def run_all_labs():
    demonstrate_tree_dp()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Tree DP, why must the algorithm strictly utilize Post-Order Traversal (calling `dfs(child)` before executing the mathematical state transitions)?
   Answer: Dynamic Programming relies on having smaller sub-problems already solved before attempting to solve the current problem. In a Tree hierarchy, the CEO's maximum fun rating relies entirely on knowing the mathematically optimal choices of the Managers. The Managers rely on knowing the optimal choices of the Interns. If we tried to calculate the CEO's state first (Pre-Order), the children's DP arrays would be completely empty (`[0, 0]`), returning garbage data. Post-Order traversal mathematically guarantees that the DFS dives all the way down to the leaf nodes (Interns) first. It solves the leaves, and passes the concrete results UP the call stack, guaranteeing that when a parent executes its state transition equation, all of its children have already been flawlessly evaluated.

2. Explain the State Transition Equation: `dp[node][1] += dp[child][0]`. Why can't we use `max()` here like we did for `dp[node][0]`?
   Answer: This equation calculates the maximum fun if we explicitly `DO` invite the current Manager (`dp[node][1]`). The problem strictly forbids adjacent nodes from both being selected (A Manager and their direct Subordinate cannot both attend). Because we forced the Manager into the party, we physically closed off the universe where the Subordinate is allowed to attend. We are mathematically barred from choosing the `DO invite child` (`dp[child][1]`) state. We have zero choices. We are mathematically forced to take the exact value of the `DO NOT invite child` state (`dp[child][0]`), which is why the `max()` function is absent.

3. Why is the Time Complexity of Tree DP $O(N)$, whereas finding the Maximum Independent Set on a generic undirected graph is NP-Hard ($O(2^N)$)?
   Answer: A generic graph can contain chaotic Cycles. Because of cycles, choosing to include Node A forces Node B to be excluded, which forces Node C to be included, which wraps around and creates a paradox with Node A! Resolving these cyclic paradoxes requires testing all possible boolean combinations, leading to $O(2^N)$ exponential time. A Tree, by absolute mathematical definition, is Acyclic. There are zero cycles. The decision made at a leaf node bubbles perfectly upwards to the root without ever circling back to create a paradox. Because the flow of dependency is strictly unidirectional (bottom-up), we can evaluate each node exactly once in $O(N)$ time.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced DP (Tree DP) Completed.")
