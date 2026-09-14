"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ATCODER BEGINNER CONTEST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# AtCoder (Japan's premier competitive programming platform) has a completely 
# different flavor than Codeforces. 
# While Codeforces focuses heavily on greedy brain-teasers and ad-hoc math, 
# AtCoder focuses fiercely on classical algorithms, specifically Dynamic Programming.
#
# The "AtCoder Educational DP Contest" is legendary in the CP community. 
# It is the gold standard for learning DP.
#
# In this lab, we will solve the very first problem of that legendary contest: 
# "Frog 1". A frog is at stone 1, trying to reach stone N. It can jump 1 or 2 
# stones forward. The cost of a jump is the absolute difference in heights 
# between the stones. What is the minimum cost to reach stone N?
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master 1D Dynamic Programming (AtCoder DP Contest A - Frog 1).
# - Understand State Transition Equations for cost minimization.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ATCODER DP CONTEST A: FROG 1
# ==============================================================================
def frog_minimum_cost(heights: list[int]) -> int:
    """
    Problem: Find the minimum cost to reach the last stone.
    The frog can jump from stone `i` to `i+1` or `i+2`.
    Cost = abs(height[i] - height[target]).
    
    Time Complexity: O(N)
    Space Complexity: O(N) (can easily be optimized to O(1) space).
    """
    n = len(heights)
    if n == 1:
        return 0
        
    # dp[i] will perfectly store the absolute minimum cost to reach stone `i`
    # Initialize the array with infinity! (Because we are searching for a minimum).
    dp = [float('inf')] * n
    
    # Base Case: The frog starts at stone 0. The cost to reach where you already are is 0!
    dp[0] = 0
    
    # State Transition Equation
    for i in range(1, n):
        # 1. Jump from the immediately previous stone (i-1)
        cost_jump_1 = dp[i - 1] + abs(heights[i] - heights[i - 1])
        
        # 2. Jump from the stone 2 steps back (i-2) (Only if it physically exists!)
        if i >= 2:
            cost_jump_2 = dp[i - 2] + abs(heights[i] - heights[i - 2])
            # The mathematical minimum of the two universes!
            dp[i] = min(cost_jump_1, cost_jump_2)
        else:
            # If we are at stone 1, we physically can only reach it from stone 0!
            dp[i] = cost_jump_1
            
    # The final answer is strictly the minimum cost to reach the absolute last stone!
    return dp[n - 1]

def demonstrate_frog():
    section_header("AtCoder DP Contest (Frog 1)")
    
    # Let's say there are 4 stones.
    heights = [10, 30, 40, 20]
    print(f"Stone Heights: {heights}")
    
    ans = frog_minimum_cost(heights)
    
    print(f"\nAbsolute Minimum Cost: {ans}")
    print("Why? Jump 0 -> 1 (Cost |10-30| = 20)")
    print("Jump 1 -> 3 (Cost |30-20| = 10)")
    print("Total Cost = 30.")


# ==============================================================================
# 4. ATCODER DP CONTEST B: FROG 2 (K JUMPS)
# ==============================================================================
def frog_k_jumps(heights: list[int], k: int) -> int:
    """
    Problem: Same as Frog 1, but the frog can jump up to K stones forward!
    (i+1, i+2, ..., i+k).
    
    Time Complexity: O(N * K)
    Space Complexity: O(N)
    """
    n = len(heights)
    if n == 1: return 0
    
    dp = [float('inf')] * n
    dp[0] = 0
    
    for i in range(1, n):
        # Instead of manually checking 2 universes, we check K universes!
        # We look backwards to all stones `j` we could have possibly jumped from.
        # `max(0, i-k)` mathematically protects us from checking negative indices!
        for j in range(max(0, i - k), i):
            cost_from_j = dp[j] + abs(heights[i] - heights[j])
            dp[i] = min(dp[i], cost_from_j)
            
    return dp[n - 1]

def demonstrate_frog_k():
    section_header("AtCoder DP Contest (Frog 2 - K Jumps)")
    
    # 5 stones. The frog can jump up to 3 stones at once!
    heights = [10, 30, 40, 50, 20]
    k = 3
    print(f"Stone Heights: {heights}")
    print(f"Max Jump Distance (K): {k}")
    
    ans = frog_k_jumps(heights, k)
    
    print(f"\nAbsolute Minimum Cost: {ans}")
    print("Why? Jump 0 -> 3 (Cost |10-50| = 40)")
    print("Jump 3 -> 4 (Cost |50-20| = 30)")
    print("Total Cost = 70.")
    print("Wait, what about jumping 0 -> 4? (Distance 4). That is forbidden because K=3!")


def run_all_labs():
    demonstrate_frog()
    demonstrate_frog_k()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the `frog_minimum_cost` DP array, why is the array initialized with `float('inf')` instead of `0`?
   Answer: In Dynamic Programming, the default initialization value must mathematically reflect the worst possible outcome for the type of optimization you are performing. We are trying to find the *Minimum* Cost. If we initialized the array with `0`, the line `dp[i] = min(0, cost)` would mathematically ALWAYS choose `0`. The algorithm would instantly break and report a total cost of 0. By initializing with mathematical Infinity, the very first valid cost evaluated (e.g., 20) will successfully overwrite the infinity (`min(inf, 20) = 20`), allowing the algorithm to correctly track the lowest valid number.

2. In the "Frog 1" problem, how would you optimize the Space Complexity from $O(N)$ down to strict $O(1)$?
   Answer: Rolling Arrays! Look strictly at the State Transition Equation: `cost_jump_1 = dp[i-1] + ...` and `cost_jump_2 = dp[i-2] + ...`. The mathematical variable `i` only ever looks back at a maximum depth of 2 (`i-1` and `i-2`). It NEVER looks at `dp[i-3]` or `dp[i-4]`. Therefore, any data older than 2 steps is mathematically obsolete and wasting RAM. You can replace the entire $O(N)$ array with exactly two integer variables: `prev_1` and `prev_2`. As the loop advances, you calculate the new cost, shift `prev_1` into `prev_2`, and assign the new cost to `prev_1`, perfectly executing the DP in $O(1)$ space.

3. In "Frog 2", what is the exact mechanism of `max(0, i - k)` inside the inner `for` loop?
   Answer: Boundary Protection! If the frog is at stone 5 (`i=5`), and it can jump up to 10 stones backwards (`k=10`), the mathematical calculation `i - k` results in `-5`. The frog would attempt to check if it jumped from stone `-5`. This is physically impossible and would throw an IndexError in Python. By wrapping the lower bound in `max(0, i - k)`, we mathematically force the loop to halt perfectly at stone 0. It says: "Look backwards up to $K$ steps, but if you hit the absolute beginning of the array, slam on the brakes and stop searching."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AtCoder Beginner (DP Frog) Completed.")
