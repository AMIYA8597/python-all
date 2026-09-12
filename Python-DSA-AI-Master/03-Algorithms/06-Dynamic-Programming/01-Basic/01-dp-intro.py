"""
## A. Concept Name
Dynamic Programming (Introduction)

## B. Core Idea
Breaking down a complex problem into simpler subproblems, solving each of those subproblems just once, and storing their solutions.

## C. Time & Space Complexity
- Time Complexity: Typically O(n) for 1D DP like Fibonacci.
- Space Complexity: O(n) using an array, or O(1) using variables.

## D. Best Practices
- Always identify if the problem has Optimal Substructure and Overlapping Subproblems.
- Use Memoization (Top-Down) or Tabulation (Bottom-Up).

## E. Common Pitfalls
- Forgetting to initialize base cases.
- Incorrect state transitions.

## F. Memory Management
- Reusing variables can save space (e.g., in Fibonacci, keeping track of only the last two values).

## G. Edge Cases
- n = 0 or n = 1.

## H. Testing Strategy
- Test with small inputs (0, 1, 2).
- Test with large inputs to ensure no stack overflow (for memoization).

## I. Debugging Tips
- Print the DP table/array to visualize the state transitions.

## J. Performance Tuning
- Convert recursion + memoization to pure iterative tabulation to avoid function call overhead.

## K. Related Concepts
- Recursion
- Divide and Conquer
- Greedy Algorithms

## L. Real-World Applications
- Resource allocation, routing algorithms, scheduling.

## M. Code Reusability
- DP patterns can be reused across string matching (LCS), knapsack, etc.

## N. Error Handling
- Validate input types and ranges before computation.

## O. Security Implications
- Not directly applicable, though mitigating DoS via efficient algorithms is a factor.

## P. Scalability
- DP tables can grow too large, so space optimization is critical.

## Q. Maintainability
- Keep state transitions clear and comment on what each state represents.

## R. Extensibility
- Generalize DP solutions to handle multi-dimensional constraints.

## S. Data Validation
- Ensure DP indices don't go out of bounds.

## T. Async/Await
- Typically DP computations are synchronous CPU-bound operations.

## U. Environment Variables
- Not applicable.

## V. Deployment
- Package the algorithm as part of a utility library.

## W. Monitoring
- Measure time taken for large inputs to ensure performance SLAs.

## X. Project Connection
This forms the foundational layer for AI optimization tasks, such as reinforcement learning value iteration and search algorithms.
"""

def fibonacci_memoization(n: int, memo: dict = None) -> int:
    """
    Top-Down Dynamic Programming (Memoization) for Fibonacci.
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoization(n - 1, memo) + fibonacci_memoization(n - 2, memo)
    return memo[n]

def fibonacci_tabulation(n: int) -> int:
    """
    Bottom-Up Dynamic Programming (Tabulation) for Fibonacci.
    """
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]

def fibonacci_optimized(n: int) -> int:
    """
    Space-optimized Bottom-Up Dynamic Programming.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    n_val = 10
    print(f"Fibonacci({n_val}) via Memoization: {fibonacci_memoization(n_val)}")
    print(f"Fibonacci({n_val}) via Tabulation: {fibonacci_tabulation(n_val)}")
    print(f"Fibonacci({n_val}) Optimized: {fibonacci_optimized(n_val)}")
