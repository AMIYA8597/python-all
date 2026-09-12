"""
## A. Concept Name
Fibonacci Sequence using Dynamic Programming

## B. Real-world Analogy
Imagine climbing a staircase. To reach step `n`, you could have come from step `n-1` or step `n-2`. The total ways to reach step `n` is the sum of the ways to reach the previous two steps. This builds a sequence where each step relies on the previous two.

## C. Core Principles
The Fibonacci sequence exhibits overlapping subproblems (computing the same values repeatedly in a naive recursive approach) and optimal substructure (the nth value is composed of the (n-1)th and (n-2)th values). Dynamic Programming optimizes this by caching results (memoization) or building up from the base cases (tabulation).

## D. Mathematical Definition
F(n) = F(n-1) + F(n-2) for n > 1
with base cases: F(0) = 0, F(1) = 1

## E. Naive Approach
A simple recursive function `fib(n) = fib(n-1) + fib(n-2)` has an exponential time complexity of O(2^n).

## F. Top-Down Approach (Memoization)
Store the results of expensive function calls and return the cached result when the same inputs occur again.

## G. Bottom-Up Approach (Tabulation)
Solve the problem from the smallest base cases up to the desired `n` iteratively.

## H. Space Optimization
Instead of storing all previous Fibonacci numbers, we only need to keep track of the last two.

## I. Time Complexity
With Dynamic Programming, the time complexity is reduced to O(n) because each number up to n is computed exactly once.

## J. Space Complexity
- Memoization: O(n) for the call stack and cache.
- Tabulation (array): O(n) for the DP table.
- Space Optimized: O(1) by only storing the last two values.

## K. Edge Cases
Handling n < 0, n = 0, and n = 1 correctly.

## L. Common Pitfalls
Forgetting the base cases or exceeding recursion depth in the top-down approach for large `n`.

## M. Implementation Details
Using Python's `functools.lru_cache` makes memoization trivial, but implementing it manually helps in understanding DP concepts.

## N. Best Practices
Prefer iterative approaches for this specific problem in production to avoid stack overflow exceptions and reduce memory overhead.

## O. Advanced Operations
Matrix exponentiation can find the nth Fibonacci number in O(log n) time.

## P. Variations
Tribonacci sequence (sum of last 3), finding Fibonacci numbers in O(1) using Binet's formula (though floating-point precision becomes an issue).

## Q. Limitations
Python integers have arbitrary precision, but in other languages, Fibonacci numbers quickly exceed the maximum limit for 32-bit or 64-bit integers.

## R. Alternatives
Recursive, DP, Matrix Exponentiation, Binet's Formula.

## S. Interview Tips
If asked about Fibonacci, quickly mention the O(2^n) naive approach and immediately suggest the O(n) space-optimized iterative DP approach. Be ready to explain the memoization vs tabulation tradeoff.

## T. Testing Strategy
Test base cases (0, 1), small inputs (5, 10), and large inputs (100) to ensure performance and correctness.

## U. Historical Context
Named after the Italian mathematician Fibonacci (Leonardo of Pisa), who introduced it to Western European mathematics in his 1202 book Liber Abaci.

## V. References
Introduction to Algorithms (CLRS) - Chapter on Dynamic Programming.

## W. Code Implementation
See the functions below for Memoization and Space-Optimized Tabulation.

## X. Project Connection
Understanding the core DP patterns (overlapping subproblems and optimal substructure) through Fibonacci is the foundation for solving complex optimization problems in AI algorithms, such as sequence alignment, reinforcement learning state value functions, and pathfinding on grids.
"""

def fibonacci_memo(n: int, memo: dict = None) -> int:
    """
    Top-Down Dynamic Programming approach (Memoization).
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tab(n: int) -> int:
    """
    Bottom-Up Space-Optimized Dynamic Programming approach (Tabulation).
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1

if __name__ == "__main__":
    n = 10
    print(f"Fibonacci({n}) using Memoization: {fibonacci_memo(n)}")
    print(f"Fibonacci({n}) using Tabulation (Space Optimized): {fibonacci_tab(n)}")