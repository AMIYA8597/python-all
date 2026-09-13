"""
# ==============================================================================
# LABORATORY: RECURSION TREES & OVERLAPPING SUBPROBLEMS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Fibonacci sequence is: 0, 1, 1, 2, 3, 5, 8, 13...
# The mathematical formula is: F(n) = F(n-1) + F(n-2).
#
# Because the formula literally references itself twice, it seems like the most 
# perfect use-case for Recursion ever invented. But if you actually write the 
# naive recursive function and try to calculate the 50th Fibonacci number... 
# your computer will freeze for years.
#
# Why? Because the recursive function creates a "Recursion Tree". 
# F(5) calls F(4) and F(3).
# But F(4) ALSO calls F(3)!
#
# We end up calculating the exact same subproblems millions of times over and 
# over again. This catastrophic failure of recursion is known as "Overlapping 
# Subproblems", and causes the Time Complexity to explode to O(2^N) (Exponential).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the O(2^N) Recursion Tree failure.
# - Concept: Caching (Memoization) to bypass overlapping subproblems.
# - Understand how Dynamic Programming relates to Recursion.
#
# ==============================================================================
"""

import time
from typing import Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE NAIVE O(2^N) CATASTROPHE
# ==============================================================================
def fib_naive(n: int) -> int:
    """
    Time Complexity: O(2^N) (Technically O(1.618^N), the Golden Ratio).
    Space Complexity: O(N) (Max depth of the call stack).
    """
    if n == 0: return 0
    if n == 1: return 1
    
    # This branches into TWO separate function calls.
    # The left branch fully executes, then the right branch executes.
    return fib_naive(n - 1) + fib_naive(n - 2)

def demonstrate_naive():
    section_header("Algorithm: Naive Recursion (Exponential Time)")
    
    print("Calculating Fib(35) using naive recursion...")
    start = time.time()
    ans = fib_naive(35)
    end = time.time()
    
    print(f"Result: {ans}")
    print(f"Time Taken: {end - start:.2f} seconds.")
    print("If you try Fib(50), it will take years. The time doubles every step!")


# ==============================================================================
# 4. THE FIX: MEMOIZATION (TOP-DOWN DP)
# ==============================================================================
def fib_memoized(n: int, cache: Dict[int, int]) -> int:
    """
    Time Complexity: O(N) (Every unique number is calculated exactly ONCE).
    Space Complexity: O(N) (For the Call Stack and the Dictionary).
    """
    # 1. Base Cases
    if n == 0: return 0
    if n == 1: return 1
    
    # 2. The Cache Check
    # Before we do ANY math, we check the Dictionary. 
    # If we have calculated this exact problem before, return the answer instantly!
    if n in cache:
        return cache[n]
        
    # 3. Calculate and Cache
    # We must calculate it. BUT we save the answer to the dictionary before returning it!
    ans = fib_memoized(n - 1, cache) + fib_memoized(n - 2, cache)
    cache[n] = ans
    
    return ans

def demonstrate_memoization():
    section_header("Algorithm: Memoized Recursion (O(N) Time)")
    
    print("Calculating Fib(35) using Memoization...")
    
    start = time.time()
    # We must pass an empty dictionary to hold the cached answers
    ans = fib_memoized(35, {})
    end = time.time()
    
    print(f"Result: {ans}")
    print(f"Time Taken: {end - start:.6f} seconds. (Instantaneous!)")
    
    print("\nCalculating Fib(500) using Memoization...")
    ans500 = fib_memoized(500, {})
    print(f"Fib(500) has {len(str(ans500))} digits. Calculated instantly.")


# ==============================================================================
# 5. THE OPTIMAL ITERATIVE SOLUTION
# ==============================================================================
def fib_iterative(n: int) -> int:
    """
    Time Complexity: O(N)
    Space Complexity: O(1)
    
    We don't need a massive Call Stack. We don't need a massive Dictionary.
    We only need to remember the LAST TWO numbers!
    """
    if n == 0: return 0
    if n == 1: return 1
    
    prev2 = 0 # F(0)
    prev1 = 1 # F(1)
    
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Space Complexity of `fib_naive(N)`? Is it $O(2^N)$?
   Answer: NO. The Space Complexity is only $O(N)$! The execution branches to the left side of the tree first `fib(n-1)`. It goes all the way down to the base case, popping on and off the stack. The stack never holds more than $N$ frames at a single moment in time. The TIME is exponential, but the SPACE is strictly linear.

2. What is Dynamic Programming?
   Answer: Dynamic Programming (DP) is simply the act of optimizing a recursive algorithm by storing the answers to overlapping subproblems. 
   - "Top-Down" DP uses Recursion + a Hash Map (Memoization).
   - "Bottom-Up" DP uses Iteration (Loops) + an Array (Tabulation).

3. Can you use Python's built-in tools for Memoization?
   Answer: Yes! You can put `@functools.lru_cache(None)` above any naive recursive function. Python will automatically wrap the function in a C-optimized dictionary, instantly turning the $O(2^N)$ algorithm into an $O(N)$ algorithm without you having to manually write the `cache` dictionary logic!
"""

if __name__ == "__main__":
    demonstrate_naive()
    demonstrate_memoization()
    print("\n[SUCCESS] Laboratory: Overlapping Subproblems Completed.")
