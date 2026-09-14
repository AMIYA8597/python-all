"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - DYNAMIC PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "You are climbing a staircase. It takes N steps to reach the top. 
# You can either climb 1 or 2 steps at a time. How many distinct ways can you 
# reach the top?"
#
# A junior engineer writes a pure recursive function. At N=45, the function 
# takes 3 years to execute because it computes the exact same sub-problems 
# billions of times. O(2^N) complexity is a catastrophic failure.
#
# Dynamic Programming (DP) is the mathematical art of NEVER calculating the same 
# thing twice. A senior engineer uses "Memoization" (Top-Down caching) or 
# "Tabulation" (Bottom-Up array building) to mathematically collapse the O(2^N) 
# exponential explosion into a perfectly linear O(N) scan.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Top-Down DP (Memoization) with `functools.lru_cache`.
# - Master Bottom-Up DP (Tabulation) with an Array.
# - Master Space Optimization (Variables instead of Arrays).
#
# ==============================================================================
"""

import time
import functools

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TOP-DOWN DP (MEMOIZATION / RECURSION + CACHING)
# ==============================================================================
# We use the built-in caching engine!
@functools.lru_cache(maxsize=None)
def climb_stairs_memoized(n: int) -> int:
    """
    Time: O(N) | Space: O(N) for Recursion Stack + Cache Memory.
    Top-Down: We start at the top (N) and mathematically break it down into smaller pieces.
    """
    # Base cases:
    # If we have 1 step left, there is only 1 way to climb it (1).
    # If we have 2 steps left, there are 2 ways to climb it (1+1, or 2).
    if n == 1: return 1
    if n == 2: return 2
    
    # We branch out into two universes!
    return climb_stairs_memoized(n - 1) + climb_stairs_memoized(n - 2)

def demonstrate_memoization():
    section_header("Top-Down DP (Memoization)")
    
    n = 38
    print(f"Task: Climbing a staircase with {n} steps.")
    print("Without `@lru_cache`, this takes ~10 seconds. Let's see how fast DP is...")
    
    start = time.perf_counter()
    ways = climb_stairs_memoized(n)
    end = time.perf_counter()
    
    print(f"\nResult: {ways} distinct ways.")
    print(f"Time: {(end - start):.6f} seconds (Instantaneous O(N)!)")


# ==============================================================================
# 4. BOTTOM-UP DP (TABULATION / ITERATIVE)
# ==============================================================================
def climb_stairs_tabulated(n: int) -> int:
    """
    Time: O(N) | Space: O(N)
    Bottom-Up: We start at the absolute bottom (0) and sequentially build a 
    historical timeline (Array) until we reach the top.
    """
    if n == 1: return 1
    
    # Create an array to act as our DP state tracker!
    # dp[i] represents the number of ways to reach step i.
    dp = [0] * (n + 1)
    
    # Seed the base cases mathematically.
    dp[1] = 1
    dp[2] = 2
    
    # Sequentially build the history!
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]

def demonstrate_tabulation():
    section_header("Bottom-Up DP (Tabulation)")
    
    n = 10
    print(f"Task: Climbing a staircase with {n} steps.")
    
    result = climb_stairs_tabulated(n)
    print(f"Result: {result} ways.")


# ==============================================================================
# 5. SPACE OPTIMIZATION (THE O(1) MASTERCLASS)
# ==============================================================================
def climb_stairs_optimized(n: int) -> int:
    """
    Time: O(N) | Space: O(1)
    If `dp[i]` ONLY mathematically relies on `dp[i-1]` and `dp[i-2]`, 
    we DO NOT NEED an entire Array of size N! We only need two variables 
    to remember the last two states!
    """
    if n == 1: return 1
    if n == 2: return 2
    
    # State tracking variables
    one_step_back = 2 # Represents dp[i-1] (started at n=2)
    two_steps_back = 1 # Represents dp[i-2] (started at n=1)
    
    for i in range(3, n + 1):
        # Calculate current state
        current = one_step_back + two_steps_back
        
        # Shift the timeline forward!
        two_steps_back = one_step_back
        one_step_back = current
        
    return one_step_back

def demonstrate_optimization():
    section_header("Space Optimization (O(1) Memory)")
    
    n = 50
    print(f"Task: Climbing a staircase with {n} steps.")
    
    result = climb_stairs_optimized(n)
    print(f"Result: {result} ways.")
    print("Achieved perfectly without recursion limits and using zero arrays!")


def run_all_labs():
    demonstrate_memoization()
    demonstrate_tabulation()
    demonstrate_optimization()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the physical architectural difference between Top-Down Memoization and Bottom-Up Tabulation?"
   Senior Answer: "Top-Down Memoization uses Recursion. It starts at the massive, complex target state (e.g., $N$) and breaks it down into subproblems. It requires physical CPU Call Stack overhead and dynamic Hash Map lookups. If the recursion goes too deep, it will crash with a `RecursionError`. Bottom-Up Tabulation avoids recursion entirely. It starts at the absolute base cases ($0$ and $1$) and uses a pure Iterative `for` loop to physically construct an Array of historical states. Tabulation is mathematically safer because it eliminates Call Stack overhead and is immune to recursion limits."

2. Interviewer: "How do you mathematically determine if a Dynamic Programming algorithm's Space Complexity can be optimized from $O(N)$ to $O(1)$?"
   Senior Answer: "You must analyze the 'State Transition Equation'. If you look at the `for` loop logic and see `dp[i] = dp[i-1] + dp[i-2]`, it proves that calculating the current state ONLY requires the immediately preceding 2 states. Once state 3 is calculated, state 1 is mathematically obsolete and serves no further algorithmic purpose. Therefore, storing the entire history of 1,000 states in an Array ($O(N)$ space) is a massive waste of RAM. You can dynamically crush the array down to exactly 2 integer variables ($O(1)$ space) and continually overwrite them as you slide the timeline forward."

3. Interviewer: "If Bottom-Up Tabulation is safer and can often be memory-optimized, why would anyone ever use Top-Down Memoization?"
   Senior Answer: "Top-Down Memoization is 'Lazy'. It ONLY evaluates subproblems that are absolutely mathematically required to solve the target. If the state space is massive (e.g., a 2D matrix of $1000 \\times 1000$) but the optimal path only traverses $200$ cells, Top-Down will instantly evaluate those $200$ cells and finish. Bottom-Up Tabulation is 'Eager'. By definition, it forces a strict `for` loop that meticulously evaluates every single one of the $1,000,000$ cells from the ground up, regardless of whether they are actually needed by the final path. In sparse problem spaces, Top-Down can be infinitely faster."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Dynamic Programming) Completed.")
