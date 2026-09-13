"""
# ==============================================================================
# LABORATORY: DYNAMIC PROGRAMMING RECAP & THE CLIMBING STAIRS PROBLEM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you are encountering this file, you are entering (or reviewing) the Dynamic 
# Programming curriculum.
#
# Dynamic Programming (DP) solves complex problems by breaking them down into 
# simpler overlapping subproblems. 
# 
# We've already discussed the 4 Stages of DP (Naive Recursion -> Memoization -> 
# Tabulation -> Space Optimization).
#
# To firmly solidify this, we will solve the "Climbing Stairs" problem. 
# It asks: "You are climbing a staircase. It takes N steps to reach the top. 
# Each time you can either climb 1 or 2 steps. In how many distinct ways can 
# you climb to the top?"
#
# This is a classic combinatorics question. If you write out the first few 
# answers by hand, you will realize a profound mathematical truth: 
# The "Climbing Stairs" problem is literally just the Fibonacci Sequence in disguise!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Recognize combinatorial problems as DP.
# - Prove that `ways(n) = ways(n-1) + ways(n-2)`.
# - Implement O(1) space optimization for combinatorial state.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CLIMBING STAIRS (TABULATION)
# ==============================================================================
def climb_stairs(n: int) -> int:
    """
    Time Complexity: O(N)
    Space Complexity: O(N) (Tabulation Array)
    """
    # 1. BASE CASES
    # If the staircase has 1 step, there is 1 way (take 1 step).
    if n == 1:
        return 1
    # If the staircase has 2 steps, there are 2 ways (1+1, or 2).
    if n == 2:
        return 2
        
    # 2. STATE DEFINITION
    # `dp[i]` represents the total number of distinct ways to reach step `i`.
    dp = [0] * (n + 1)
    
    dp[1] = 1
    dp[2] = 2
    
    # 3. STATE TRANSITION EQUATION
    for i in range(3, n + 1):
        # How could you possibly arrive at step `i`?
        # You either jumped 1 step from `i-1`, or you jumped 2 steps from `i-2`.
        # Because these are mutually exclusive, the total number of ways to arrive 
        # is the mathematical SUM of the ways to arrive at `i-1` and `i-2`!
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]


# ==============================================================================
# 4. CLIMBING STAIRS (SPACE OPTIMIZED)
# ==============================================================================
def climb_stairs_optimized(n: int) -> int:
    """
    Time Complexity: O(N)
    Space Complexity: O(1) (Perfect constant space).
    """
    if n <= 2:
        return n
        
    prev2 = 1 # Ways to reach step (i-2)
    prev1 = 2 # Ways to reach step (i-1)
    
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1


def demonstrate_climbing_stairs():
    section_header("Algorithm: Climbing Stairs (Combinatorics DP)")
    
    print("Question: How many ways to climb 5 stairs? (Max 2 steps at a time)")
    
    ans = climb_stairs_optimized(5)
    print(f"\nResult: {ans} ways.")
    print("Proof by enumeration:")
    print(" 1. (1, 1, 1, 1, 1)")
    print(" 2. (1, 1, 1, 2)")
    print(" 3. (1, 1, 2, 1)")
    print(" 4. (1, 2, 1, 1)")
    print(" 5. (2, 1, 1, 1)")
    print(" 6. (1, 2, 2)")
    print(" 7. (2, 1, 2)")
    print(" 8. (2, 2, 1)")
    print("Total = 8. (Notice: Fib(1)=1, Fib(2)=2, Fib(3)=3, Fib(4)=5, Fib(5)=8).")
    
    n_massive = 100
    print(f"\nQuestion: How many ways to climb {n_massive} stairs?")
    ans_massive = climb_stairs_optimized(n_massive)
    print(f"Result: {ans_massive} ways!")
    print("Calculated instantly using O(1) Space DP.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Climbing Stairs literally the Fibonacci Sequence?
   Answer: Because the constraints perfectly mirror the recursive definition of Fibonacci. Fibonacci asks $F(n) = F(n-1) + F(n-2)$. Climbing Stairs asks "I can jump 1 step or 2 steps". Therefore, the only possible nodes you can arrive from are $N-1$ and $N-2$. The sum of those possibilities IS the mathematical definition of Fibonacci.

2. What if the rules changed, and you could jump 1, 2, or 3 steps at a time?
   Answer: The State Transition Equation simply expands! `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`. This is often called the "Tribonacci Sequence". You can still space-optimize this to $O(1)$ by using 3 sliding integer variables instead of an array.

3. Why do we initialize `dp[1] = 1` and `dp[2] = 2`? Why not `dp[0] = 1`?
   Answer: Both are mathematically valid. If you say `dp[0] = 1` (meaning there is 1 way to stand on the ground: doing nothing), then `dp[1] = dp[0]` (1 way), and `dp[2] = dp[1] + dp[0] = 1 + 1 = 2`. Starting at index 1 and 2 just bypasses the abstract philosophy of "How many ways to climb 0 stairs" and seeds the array with undeniable physical truths.
"""

if __name__ == "__main__":
    demonstrate_climbing_stairs()
    print("\n[SUCCESS] Laboratory: Climbing Stairs Completed.")
