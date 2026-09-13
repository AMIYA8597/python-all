"""
# ==============================================================================
# LABORATORY: THE CATALAN NUMBERS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Catalan Numbers are the most famous sequence in combinatorial mathematics 
# after the Fibonacci sequence. 
# 
# While Fibonacci models simple linear recurrence (rabbits breeding, climbing stairs), 
# the Catalan sequence models RECURSIVE BRANCHING STRUCTURES.
#
# If you are in a FAANG interview and you see a problem asking:
# - "How many structurally unique Binary Search Trees can you form with N nodes?"
# - "How many valid combinations of N pairs of parentheses exist?"
# - "How many ways can you triangulate an N-sided polygon?"
# - "How many paths on an NxN grid from bottom-left to top-right stay below the diagonal?"
#
# The answer to EVERY SINGLE ONE of these questions is the N-th Catalan Number!
#
# Sequence: 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862...
#
# There are two ways to calculate it:
# 1. Mathematical Formula: C(N) = (2n)! / ((n+1)! * n!) = (1 / (n+1)) * (2n C n).
#    (Requires $O(1)$ nCr pre-computation).
#
# 2. Dynamic Programming: C(N) = sum( C(i) * C(n-1-i) ) for i from 0 to N-1.
#    (This fundamentally describes splitting a tree into a Left Subtree and a 
#    Right Subtree, which perfectly explains WHY it models Binary Trees!).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement Catalan calculation via Dynamic Programming $O(N^2)$.
# - Implement Catalan calculation via direct Formula $O(N)$.
# - Apply the logic to generate Valid Parentheses and Unique BSTs.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CATALAN CALCULATORS
# ==============================================================================
def catalan_dp(n: int) -> int:
    """
    Calculates the N-th Catalan number using Dynamic Programming.
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    
    Formula: C[i] += C[j] * C[i - j - 1]
    """
    if n <= 1: return 1
    
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        for j in range(i):
            # Left subtree choices * Right subtree choices
            dp[i] += dp[j] * dp[i - j - 1]
            
    return dp[n]


def catalan_formula(n: int) -> int:
    """
    Calculates the N-th Catalan number using the direct mathematical formula.
    Time Complexity: O(N) (without pre-computation).
    Space Complexity: O(1)
    
    Formula: C(n) = (2n)! / ((n+1)! * n!)
    """
    if n <= 1: return 1
    
    # We can optimize the factorial calculation!
    # (2n)! / n! leaves just the numbers from (n+1) to (2n) in the numerator.
    numerator = 1
    for i in range(n + 1, 2 * n + 1):
        numerator *= i
        
    denominator = 1
    # We still need to divide by (n+1)!
    for i in range(1, n + 2):
        denominator *= i
        
    # Standard integer division
    return numerator // denominator


# ==============================================================================
# 4. APPLICATIONS OF CATALAN LOGIC (GENERATORS)
# ==============================================================================
def generate_parentheses(n: int) -> List[str]:
    """
    Generates all valid combinations of `n` pairs of parentheses.
    The number of combinations generated will perfectly match Catalan(N).
    """
    results = []
    
    def backtrack(current_string: str, open_count: int, close_count: int):
        # Base Case: We used all N pairs!
        if len(current_string) == 2 * n:
            results.append(current_string)
            return
            
        # Recursive Rules:
        # 1. We can always add an OPEN parenthesis if we haven't used all N.
        if open_count < n:
            backtrack(current_string + "(", open_count + 1, close_count)
            
        # 2. We can ONLY add a CLOSE parenthesis if it balances an existing open one.
        # This mathematically translates to staying "below the diagonal" on a grid!
        if close_count < open_count:
            backtrack(current_string + ")", open_count, close_count + 1)
            
    backtrack("", 0, 0)
    return results


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generate_unique_bst(n: int) -> List[TreeNode]:
    """
    Generates all structurally unique Binary Search Trees containing nodes 1 to N.
    The number of trees generated will perfectly match Catalan(N).
    """
    def build_trees(start: int, end: int) -> List[TreeNode]:
        if start > end:
            return [None] # Empty subtree
            
        all_trees = []
        
        # Pick every possible value to be the ROOT
        for i in range(start, end + 1):
            
            # Recursively build all possible LEFT subtrees (values < root)
            left_trees = build_trees(start, i - 1)
            
            # Recursively build all possible RIGHT subtrees (values > root)
            right_trees = build_trees(i + 1, end)
            
            # Cartesian Product: Combine every left tree with every right tree!
            # Notice how this physical loop perfectly mirrors the DP formula:
            # DP[i] = DP[j] * DP[i - j - 1]
            for l in left_trees:
                for r in right_trees:
                    current_tree = TreeNode(i)
                    current_tree.left = l
                    current_tree.right = r
                    all_trees.append(current_tree)
                    
        return all_trees
        
    if n == 0: return []
    return build_trees(1, n)


def demonstrate_catalan():
    section_header("Algorithm: Catalan Numbers (DP vs Formula)")
    
    n = 10
    print(f"Calculating the first {n} Catalan numbers:")
    
    dp_results = [catalan_dp(i) for i in range(n)]
    form_results = [catalan_formula(i) for i in range(n)]
    
    print(f"DP Result      : {dp_results}")
    print(f"Formula Result : {form_results}")
    
    section_header("Application: Valid Parentheses Generation")
    
    pairs = 3
    print(f"Generating valid parentheses for {pairs} pairs...")
    parentheses = generate_parentheses(pairs)
    
    print(f"Result count: {len(parentheses)} (Matches Catalan(3) = {catalan_formula(3)})")
    print(f"Combinations: {parentheses}")
    
    section_header("Application: Structurally Unique BSTs")
    
    nodes = 3
    print(f"Generating structurally unique BSTs for {nodes} nodes...")
    trees = generate_unique_bst(nodes)
    
    print(f"Total Trees Generated: {len(trees)} (Matches Catalan(3) = {catalan_formula(3)})")
    print("This perfect combinatorial mapping is why Catalan numbers are so famous!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the DP formula `dp[i] += dp[j] * dp[i - j - 1]` perfectly model a Binary Tree?
   Answer: Imagine you have $N$ nodes. You pick one node to be the absolute Root. You have $N-1$ nodes left. 
   You must distribute these $N-1$ nodes between the Left Subtree and the Right Subtree. 
   If you put $j$ nodes in the Left Subtree, the Right Subtree MUST get $(N - 1) - j$ nodes. 
   How many unique Left subtrees can you build with $j$ nodes? $DP[j]$. 
   How many unique Right subtrees? $DP[N - 1 - j]$. 
   To find the total combinations for this specific root, you multiply them together! You then sum this up across all possible sizes of $j$. This mathematical truth dictates the entire structure of the Catalan numbers.

2. What is the "Dyck Path" grid connection to Parentheses?
   Answer: Imagine an $N \times N$ grid. You start at $(0, 0)$ and must walk to $(N, N)$ using only Right and Up steps. The rule: You must never cross the diagonal line $y = x$. 
   If we map "Right Step = Open Parenthesis `(`" and "Up Step = Close Parenthesis `)`", the diagonal restriction $y \le x$ perfectly translates to: "The number of Close parentheses can never exceed the number of Open parentheses"! A valid Dyck Path IS a valid sequence of parentheses. Both are mathematically identical and yield the Catalan number.

3. Why use DP if the Formula is $O(N)$?
   Answer: If a problem asks for Catalan modulo $10^9+7$, the direct division formula $(2n)! / ((n+1)! \times n!)$ requires calculating Modular Multiplicative Inverses for the denominator. If you haven't pre-computed an inverse array (which requires Fermat's Little Theorem), the pure $O(N^2)$ DP array is completely immune to division errors. You can just do `dp[i] = (dp[i] + dp[j] * dp[i - j - 1]) % M` directly!
"""

if __name__ == "__main__":
    demonstrate_catalan()
    print("\n[SUCCESS] Laboratory: The Catalan Numbers Completed.")
