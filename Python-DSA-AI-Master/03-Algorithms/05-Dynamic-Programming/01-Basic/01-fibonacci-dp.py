"""
Fibonacci Sequence - Dynamic Programming
========================================

# 🎯 Learning Objectives:
1. Understand the fundamental concepts of Dynamic Programming: Overlapping Subproblems and Optimal Substructure.
2. Transition from exponential recursion to linear time DP using Top-Down (Memoization) and Bottom-Up (Tabulation).
3. Evolve space complexity from O(n) to O(1).
4. Discover professional-grade algorithms like Matrix Exponentiation (O(log n)) and Binet's Formula.

# 🧠 Intuition & Real-World Analogy
Imagine you are climbing a staircase. To reach step `n`, you could have come from step `n-1` or `n-2`.
If you want to know how many ways you can reach step `n`, it's exactly the sum of ways to reach `n-1` and `n-2`.
But calculating this from scratch every time is like asking "how do I get to step 10?" by re-calculating the path to step 9, step 8, step 7...
Instead, write down the answers on each step as you pass them. When you need it again, just look at your notebook!
That notebook is "Dynamic Programming".

# 📖 Formal Explanation
Dynamic Programming is an algorithmic technique for solving an optimization problem by breaking it down into simpler subproblems.
For Fibonacci, the state transition relation is mathematically defined as:
    F(n) = F(n-1) + F(n-2) for n > 1
    F(0) = 0, F(1) = 1

## Key Properties:
- **Optimal Substructure**: The solution to the problem can be constructed from solutions to subproblems.
- **Overlapping Subproblems**: The recursive algorithm solves the same subproblems repeatedly.

# ⚠️ Common Mistakes & Debugging
1. **Missing Base Cases**: Forgetting `if n <= 1: return n` leading to infinite recursion or `KeyError` / `IndexError`.
2. **Mutable Default Arguments in Python**: Using `def fib(n, memo={})` can cause state leakage between independent calls. Always use `memo=None`.
3. **Array Out of Bounds**: In bottom-up DP, allocating `dp = [0] * n` instead of `dp = [0] * (n + 1)` will cause an index error for `dp[n]`.
4. **Integer Overflow**: While Python automatically handles arbitrarily large integers, in C++/Java, `fib(100)` easily overflows a 64-bit integer.

# 🧠 Active Recall / Memory Anchors
- What are the two essential properties required to use Dynamic Programming?
  (Answer: Overlapping Subproblems and Optimal Substructure)
- How does memoization differ from tabulation?
  (Answer: Memoization is top-down, caching recursive calls. Tabulation is bottom-up, building up iteratively.)
- Can you achieve O(1) space complexity in all DP problems?
  (Answer: No, only when the current state depends on a strictly limited, constant number of previous states.)
"""

import time
import sys
import math
from typing import Dict, List

# Increase recursion depth for deep recursive calls in Python
sys.setrecursionlimit(2000)


def fib_naive(n: int) -> int:
    """
    [Beginner] Naive Recursive Approach
    
    Explanation:
    Directly translates the mathematical recurrence relation into code.
    
    Complexity:
    - Time: O(2^n) - Exponential due to recomputing the same subproblems repeatedly.
    - Space: O(n) - Call stack depth.
    
    Common Mistake:
    - Writing this for production. It freezes for n >= 40.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memoization(n: int, memo: Dict[int, int] = None) -> int:
    """
    [Intermediate] Top-Down Dynamic Programming (Memoization)
    
    Intuition:
    "Remember the past so you don't repeat it."
    We keep a `memo` dictionary. Before calculating fib(n), we check if it's already there.
    
    Complexity:
    - Time: O(n) - Each state is computed exactly once.
    - Space: O(n) - Call stack depth + size of the memo dictionary.
    
    Debugging Tip:
    - Ensure `memo=None` in the signature and initialize it inside to avoid state retention across different top-level calls.
    """
    if memo is None:
        memo = {}
        
    if n in memo:
        return memo[n]
        
    if n <= 1:
        return n
        
    memo[n] = fib_memoization(n - 1, memo) + fib_memoization(n - 2, memo)
    return memo[n]


def fib_tabulation(n: int) -> int:
    """
    [Intermediate] Bottom-Up Dynamic Programming (Tabulation)
    
    Intuition:
    Instead of starting from the top and breaking it down, start from the base cases and build up.
    We create an array (a table) and fill it iteratively.
    
    Complexity:
    - Time: O(n) - Single loop iterating from 2 to n.
    - Space: O(n) - An array of size n+1.
    """
    if n <= 1:
        return n
        
    # Mistake: initializing as [0] * n instead of n + 1
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]


def fib_optimized_space(n: int) -> int:
    """
    [Advanced] Bottom-Up DP with O(1) Space
    
    Intuition:
    Do we really need the entire `dp` array? To compute `dp[i]`, we only need `dp[i-1]` and `dp[i-2]`.
    We can just keep track of the last two variables, discarding the older ones to save memory.
    
    Complexity:
    - Time: O(n) - Single loop.
    - Space: O(1) - Constant auxiliary space.
    """
    if n <= 1:
        return n
        
    prev2 = 0  # Represents F(n-2)
    prev1 = 1  # Represents F(n-1)
    
    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
        
    return prev1


def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Helper function for multiplying two 2x2 matrices."""
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            C[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j]
    return C

def matrix_power(M: List[List[int]], p: int) -> List[List[int]]:
    """Helper function for raising a 2x2 matrix to the power of p in O(log p)."""
    res = [[1, 0], [0, 1]] # Identity matrix
    base = M
    
    while p > 0:
        if p % 2 == 1:
            res = matrix_multiply(res, base)
        base = matrix_multiply(base, base)
        p //= 2
        
    return res

def fib_matrix_exponentiation(n: int) -> int:
    """
    [Professional] Matrix Exponentiation
    
    Formal Explanation:
    The Fibonacci sequence can be represented as a matrix multiplication:
    | F(n+1) F(n)   |   | 1 1 |^n
    | F(n)   F(n-1) | = | 1 0 |
    
    By using fast exponentiation (similar to calculating x^n in O(log n)),
    we can find the nth Fibonacci number logarithmically.
    
    Complexity:
    - Time: O(log n) - Fast matrix exponentiation.
    - Space: O(1) - Constant number of matrix operations.
    """
    if n <= 1:
        return n
        
    M = [[1, 1], [1, 0]]
    result_matrix = matrix_power(M, n - 1)
    # The top-left element is F(n)
    return result_matrix[0][0]


def binet_formula(n: int) -> int:
    """
    [Professional] Binet's Formula (Closed-Form Solution)
    
    Mathematical formula to find Fibonacci numbers directly.
    F(n) = (phi^n - psi^n) / sqrt(5)
    where phi = (1 + sqrt(5)) / 2 and psi = (1 - sqrt(5)) / 2
    
    Complexity:
    - Time: O(1) mathematical computation (ignoring precision handling of large floats).
    - Space: O(1)
    
    Warning / Common Mistake:
    - Floating point precision issues! Beyond n ~ 70, this will give incorrect integers 
      in standard float implementations due to rounding errors.
    """
    if n <= 1:
        return n
    
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    return round((phi**n - psi**n) / sqrt5)


def performance_analysis():
    """
    Analyzes the execution time of different Fibonacci implementations.
    Shows the dramatic transition from exponential time to logarithmic time.
    """
    print("\n--- 🚀 Performance Analysis ---")
    small_n = 35 # Use small N to avoid naive recursion hanging
    
    print(f"Testing naive recursive for n={small_n} (Warning: Can take several seconds)...")
    start = time.time()
    fib_naive(small_n)
    print(f"1. Naive (O(2^n)): {time.time() - start:.6f}s")
    
    large_n = 100000
    # Python sets a default recursion limit (~1000). We raised it for memoization.
    med_n = 1500 
    
    start = time.time()
    fib_memoization(med_n)
    print(f"2. Memoization (O(n)) for n={med_n}: {time.time() - start:.6f}s")
    
    start = time.time()
    fib_tabulation(large_n)
    print(f"3. Tabulation (O(n)) for n={large_n}: {time.time() - start:.6f}s")
    
    start = time.time()
    fib_optimized_space(large_n)
    print(f"4. Opt Space (O(n)) for n={large_n}: {time.time() - start:.6f}s")
    
    start = time.time()
    fib_matrix_exponentiation(large_n)
    print(f"5. Matrix Expr (O(log n)) for n={large_n}: {time.time() - start:.6f}s")


def test_fib():
    """Test suite comparing all valid implementations."""
    print("\n--- 🧪 Running Tests ---")
    
    test_cases = [0, 1, 2, 5, 10, 50]
    
    for n in test_cases:
        expected = fib_optimized_space(n)
        assert fib_memoization(n) == expected, f"Memoization failed for {n}"
        assert fib_tabulation(n) == expected, f"Tabulation failed for {n}"
        if n < 30: # Avoid naive for n >= 30 in tests
            assert fib_naive(n) == expected, f"Naive failed for {n}"
            
        assert fib_matrix_exponentiation(n) == expected, f"Matrix Exp failed for {n}"
        
        # Binet formula is accurate for small N
        if n <= 70:
            assert binet_formula(n) == expected, f"Binet failed for {n}"
            
    print("✅ All unit tests passed perfectly!")


if __name__ == "__main__":
    print("🎓 Dynamic Programming Masterclass: Fibonacci Sequence")
    test_fib()
    performance_analysis()
