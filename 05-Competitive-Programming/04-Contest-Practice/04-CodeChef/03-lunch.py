"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODECHEF LUNCHTIME)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The CodeChef Lunchtime is a fast-paced sprint that often acts as a bridge 
# between Easy algorithms and Hard algorithms. 
# 
# One of the most infamous "Medium-Hard" patterns is Dynamic Programming on Trees 
# (Tree DP).
#
# Imagine you are the CEO of a company. You are throwing a party. You want to 
# invite employees to maximize the "Fun Rating" of the party. However, there is 
# a strict rule: You CANNOT invite an employee AND their direct manager. 
# (This mathematically prevents any two adjacent nodes in the corporate hierarchy 
# tree from being selected).
#
# This is the "Maximum Independent Set on a Tree" problem.
# You cannot use a 1D DP array (`dp[i]`) because a tree is not a line. 
# You must execute a Post-Order Depth-First Search (DFS) that calculates the 
# DP states from the bottom (the interns) all the way up to the root (the CEO)!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Tree DP.
# - Solve the Maximum Independent Set on a Tree.
# - Manage State Transitions passing UP the recursion stack.
#
# ==============================================================================
"""

import sys

# Increase recursion depth for massive trees
sys.setrecursionlimit(200000)

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TREE DP (MAXIMUM INDEPENDENT SET)
# ==============================================================================
def max_party_fun(n: int, fun_ratings: list[int], edges: list[tuple[int, int]]) -> int:
    """
    Solves the Maximum Independent Set on a Tree using DFS DP.
    Time Complexity: O(N)
    Space Complexity: O(N) for recursion stack and DP array.
    """
    if n == 0: return 0
    if n == 1: return fun_ratings[0]
    
    # 1. Build the Adjacency List
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        
    # 2. The 2D DP Array!
    # dp[node][0] = Maximum fun in the subtree rooted at `node`, IF we DO NOT invite `node`.
    # dp[node][1] = Maximum fun in the subtree rooted at `node`, IF we DO invite `node`.
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(current: int, parent: int) -> None:
        """
        Post-Order DFS. We calculate the children FIRST, and mathematically 
        pull their answers UP to the parent!
        """
        # Base Case Setup:
        # If we DO NOT invite the current node, we get 0 fun from them.
        dp[current][0] = 0
        # If we DO invite the current node, we instantly get their fun rating!
        dp[current][1] = fun_ratings[current]
        
        # Traverse all children
        for neighbor in graph[current]:
            if neighbor != parent:
                # 1. Recursively calculate the DP values for the child subtree!
                dfs(neighbor, current)
                
                # 2. State Transition Phase! (The child's data is now perfectly calculated).
                
                # Universe A: We DO NOT invite the current node (`current`).
                # Because `current` is NOT going, there is absolutely no restriction 
                # on the child! The child can go, or not go. We greedily take 
                # whatever is mathematically highest from the child's subtree!
                dp[current][0] += max(dp[neighbor][0], dp[neighbor][1])
                
                # Universe B: We DO invite the current node (`current`).
                # Because `current` IS going, the child is MATHEMATICALLY FORBIDDEN 
                # from going. We are strictly forced to use the child's [0] state!
                dp[current][1] += dp[neighbor][0]

    # Start the DFS from an arbitrary root (e.g., node 0), with -1 as its parent.
    dfs(0, -1)
    
    # The final answer is strictly the maximum of the two possible universes at the Root!
    return max(dp[0][0], dp[0][1])

def demonstrate_tree_dp():
    section_header("Tree DP (Maximum Independent Set)")
    
    # Corporate Hierarchy:
    #      0 (CEO, Fun: 10)
    #     / \
    #    1   2 (Managers, Fun: 20, 20)
    #   /     \
    #  3       4 (Interns, Fun: 50, 50)
    
    n = 5
    fun_ratings = [10, 20, 20, 50, 50]
    edges = [
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 4)
    ]
    
    print("Corporate Hierarchy Tree built.")
    print(f"Fun Ratings: {fun_ratings}")
    print("Rule: You CANNOT invite a manager and their direct subordinate.")
    
    ans = max_party_fun(n, fun_ratings, edges)
    
    print(f"\nAbsolute Maximum Fun: {ans}")
    print("Why? If we invite the CEO (10), we cannot invite the Managers.")
    print("We then invite the Interns (50+50). Total = 110.")
    print("If we didn't invite the CEO, we could invite the Managers (20+20 = 40), ")
    print("but we lose the Interns. 40 < 110.")
    print("The Post-Order DFS flawlessly evaluated all branches in O(N) time!")


def run_all_labs():
    demonstrate_tree_dp()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Tree DP, why is a Post-Order DFS required instead of a Pre-Order DFS?
   Answer: Pre-Order DFS evaluates the Parent *before* the Children. If you attempt to calculate the maximum fun of the CEO before you have calculated the fun of the Managers and Interns, you have absolutely zero mathematical data to base your decision on. You are guessing. Post-Order DFS dives straight to the absolute bottom of the tree (the leaf nodes) first. It perfectly calculates the states for the leaves, and passes those hard mathematical answers UP the tree to their parents. The Parent waits until all of its children have returned valid DP states, allowing the Parent to instantly compute its own state using $O(1)$ math.

2. In the State Transition equation, explain the logic behind `dp[current][0] += max(dp[child][0], dp[child][1])`.
   Answer: `dp[current][0]` represents the universe where the current node is physically ABSENT from the party. The fundamental rule of the problem is: "You cannot invite two *adjacent* nodes." Because the current node is absent, that adjacency rule is completely deactivated for the child! The child is mathematically free to attend or not attend. To maximize our overall fun, we greedily look at the child's two possible universes (`dp[child][0]` and `dp[child][1]`) and physically take whichever number is higher. We then add this maximum to our current running total.

3. Why do we maintain a `parent` parameter in the DFS signature `def dfs(current: int, parent: int)`?
   Answer: In a mathematically rigorous Graph Adjacency List, edges are bidirectional. If Node 0 is connected to Node 1, `graph[0]` contains `1`, and `graph[1]` contains `0`. When the DFS moves from Node 0 down to Node 1, it will loop through all of Node 1's neighbors. One of those neighbors is Node 0! If it recursively calls `dfs(0)`, the code will instantly enter an infinite loop, ping-ponging between 0 and 1 until the Stack Overflow crashes the program. By explicitly passing `parent = 0`, the loop `if neighbor != parent:` mathematically prevents the DFS from ever walking backwards up the tree it just came down!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CodeChef Lunchtime Completed.")
