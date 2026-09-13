"""
# ==============================================================================
# LABORATORY: DYNAMIC PROGRAMMING (THE 4 STAGES OF OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Dynamic Programming" (DP) is often considered the hardest topic in Computer 
# Science interviews. 
# 
# Fun fact: The name "Dynamic Programming" is completely meaningless. The inventor, 
# Richard Bellman (1950s), was trying to secure military funding for mathematics 
# research. His boss hated the word "Mathematics". So Bellman invented a buzzword 
# ("Dynamic Programming") that sounded military and futuristic, just to get funding!
#
# So what is DP actually? 
# It is just "Smart Recursion". 
# If a problem can be broken down into smaller subproblems, and those subproblems 
# OVERLAP (we calculate the exact same thing multiple times), we can use DP to 
# save the answers and reuse them, dropping Time Complexity from Exponential O(2^N) 
# to Linear O(N).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the 4 Stages of DP (Naive -> Top-Down -> Bottom-Up -> Optimized).
# - Understand Memoization vs Tabulation.
# - Master the "State Transition Equation": DP[i] = DP[i-1] + DP[i-2]
#
# ==============================================================================
"""

import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE 4 STAGES OF DYNAMIC PROGRAMMING
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: NAIVE RECURSION
# ------------------------------------------------------------------------------
def fib_1_naive(n: int) -> int:
    """
    Time: O(2^N) - Exponential Catastrophe.
    Space: O(N) - Call Stack depth.
    """
    if n <= 1: return n
    return fib_1_naive(n - 1) + fib_1_naive(n - 2)


# ------------------------------------------------------------------------------
# STAGE 2: TOP-DOWN (MEMOIZATION)
# ------------------------------------------------------------------------------
def fib_2_memoized(n: int, memo: dict) -> int:
    """
    Time: O(N) - Linear (Every unique N is calculated exactly once).
    Space: O(N) Call Stack + O(N) Hash Map.
    
    Why "Top-Down"? Because we start at N (e.g. 100), and recursively dive DOWN 
    the tree to 0. It is easy to write, but suffers from Python's RecursionLimit 
    and Call Stack overhead.
    """
    if n <= 1: return n
    
    if n in memo:
        return memo[n]
        
    memo[n] = fib_2_memoized(n - 1, memo) + fib_2_memoized(n - 2, memo)
    return memo[n]


# ------------------------------------------------------------------------------
# STAGE 3: BOTTOM-UP (TABULATION)
# ------------------------------------------------------------------------------
def fib_3_tabulation(n: int) -> int:
    """
    Time: O(N) - Linear.
    Space: O(N) - For the Array (Table).
    
    Why "Bottom-Up"? We kill Recursion entirely! We start at 0 and build UP to N.
    We pre-allocate an Array (a Table) of size N+1. We seed the base cases, 
    and use a simple `for` loop to fill the table.
    No Recursion means NO Call Stack overhead, NO RecursionError, and much faster 
    constant-time execution!
    """
    if n <= 1: return n
    
    # Pre-allocate the DP Table
    dp = [0] * (n + 1)
    
    # Seed the Base Cases
    dp[0] = 0
    dp[1] = 1
    
    # The State Transition Loop
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]


# ------------------------------------------------------------------------------
# STAGE 4: BOTTOM-UP (SPACE OPTIMIZED)
# ------------------------------------------------------------------------------
def fib_4_optimized(n: int) -> int:
    """
    Time: O(N) - Linear.
    Space: O(1) - Perfect Constant Space!
    
    Look at the State Transition Equation in Stage 3: `dp[i] = dp[i-1] + dp[i-2]`.
    Notice that to calculate `i`, we ONLY care about the previous 2 elements!
    We don't care about `dp[i-3]` or `dp[i-50]`. 
    So why are we storing them in a massive O(N) array?
    We can throw the array away, and just use 2 sliding integer variables!
    """
    if n <= 1: return n
    
    prev2 = 0
    prev1 = 1
    
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1


# ==============================================================================
# 4. BENCHMARKING
# ==============================================================================
def run_benchmark():
    section_header("Algorithm: The 4 Stages of DP")
    
    N_SMALL = 35
    print(f"Benchmarking N = {N_SMALL}...\n")
    
    # Stage 1
    start = time.time()
    ans = fib_1_naive(N_SMALL)
    print(f"Stage 1 (Naive)      : Ans={ans}, Time={time.time()-start:.4f}s")
    
    # Stage 2
    start = time.time()
    ans = fib_2_memoized(N_SMALL, {})
    print(f"Stage 2 (Memoized)   : Ans={ans}, Time={time.time()-start:.6f}s")
    
    # Stage 3
    start = time.time()
    ans = fib_3_tabulation(N_SMALL)
    print(f"Stage 3 (Tabulation) : Ans={ans}, Time={time.time()-start:.6f}s")
    
    # Stage 4
    start = time.time()
    ans = fib_4_optimized(N_SMALL)
    print(f"Stage 4 (Optimized)  : Ans={ans}, Time={time.time()-start:.6f}s")
    
    print("\nAttempting N = 1500 for the Iterative stages...")
    print(f"Stage 3 (Tabulation) : {len(str(fib_3_tabulation(1500)))} digits. (Instant)")
    print(f"Stage 4 (Optimized)  : {len(str(fib_4_optimized(1500)))} digits. (Instant)")
    print("Stage 2 (Memoized) would likely hit Python's Recursion Limit!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Memoization and Tabulation?
   Answer: 
   - Memoization (Top-Down): Starts at $N$. Uses Recursion. Stores answers in a Hash Map / Dictionary on the fly. Susceptible to Stack Overflows.
   - Tabulation (Bottom-Up): Starts at $0$. Uses Iteration (for loops). Stores answers in a pre-allocated Array / Table. Extremely fast and safe.

2. How do you know if a problem can be space-optimized from $O(N)$ to $O(1)$?
   Answer: Look strictly at the "State Transition Equation". If `dp[i]` only relies on a FIXED window of previous elements (e.g. `dp[i-1]` and `dp[i-2]`), you can always optimize it to $O(1)$ by using sliding variables. If `dp[i]` requires looking at ALL previous elements (e.g. `dp[i]` needs a `for j from 0 to i` loop), you CANNOT space optimize it, you must keep the $O(N)$ array.

3. Why is DP the hardest topic to master?
   Answer: Because figuring out the "State" and the "State Transition Equation" requires mathematical intuition. Once you realize that the State is `dp[i]` and the equation is `dp[i] = dp[i-1] + dp[i-2]`, the code takes exactly 3 minutes to write. The difficulty is purely in finding the equation.
"""

if __name__ == "__main__":
    # Increase recursion limit just in case tests run high
    sys.setrecursionlimit(2000)
    run_benchmark()
    print("\n[SUCCESS] Laboratory: DP Fundamentals Completed.")
