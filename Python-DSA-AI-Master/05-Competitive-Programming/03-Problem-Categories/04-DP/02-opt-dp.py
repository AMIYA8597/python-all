"""
## A. Concept Name
Optimized Dynamic Programming in Competitive Programming

## B. Problem Statement
Many competitive programming problems have extremely tight time or space limits. 
Standard dynamic programming approaches (e.g., O(N*M) space or O(N) time for large N) 
may lead to Time Limit Exceeded (TLE) or Memory Limit Exceeded (MLE) and must be optimized.

## C. Solution Approach
1. Space Optimization: Reducing O(N*M) space to O(M) or even O(1) when we only need previous states.
2. State Machine DP: Using state transitions for sequence problems (like Stock Trading).
3. Matrix Exponentiation for DP: Speeding up linear recurrence relations from O(N) to O(log N).

## D. Time & Space Complexity
- Space Optimization: Modifies space from O(N*M) to O(M). Time remains the same.
- State Machine DP: Generally O(N) time and O(1) space.
- Matrix Exponentiation: Speeds up O(N) linear recurrences to O(log N) time, O(1) space.

## E. Corner Cases
- Base cases (e.g., n=0 or n=1 for Fibonacci).
- Empty arrays or grid in space-optimized variants.

## X. Project Connection
Industry Use Cases:
- Rendering algorithms and physics simulations (Memory constraint handling)
- Cryptography and Pseudo-Random Number Generators (Matrix Exponentiation)
- Financial modeling algorithms (State Machine DP)
"""

from typing import List
import copy

# =============================================================================
# 1. Space Optimization (Fibonacci & Grid Paths)
# =============================================================================

def fib_optimized(n: int) -> int:
    """
    Computes the n-th Fibonacci number.
    Instead of an O(N) array, we only keep track of the last two values.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def min_path_sum_optimized(grid: List[List[int]]) -> int:
    """
    Finds the minimum path sum from top-left to bottom-right of a grid.
    Instead of using O(M*N) space, we overwrite a 1D array of size N (O(N) space).
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = grid[0][0]
    
    # Initialize first row
    for j in range(1, n):
        dp[j] = dp[j-1] + grid[0][j]
        
    for i in range(1, m):
        dp[0] += grid[i][0] # Update first column
        for j in range(1, n):
            dp[j] = min(dp[j], dp[j-1]) + grid[i][j]
            
    return dp[n-1]

# =============================================================================
# 2. State Machine DP (Best Time to Buy and Sell Stock with Cooldown)
# =============================================================================

def max_profit_cooldown(prices: List[int]) -> int:
    """
    Professional implementation using State Machines.
    States:
    - hold: We own a stock
    - sold: We just sold a stock (triggering cooldown tomorrow)
    - rest: We don't own a stock, not in cooldown
    
    Time: O(N), Space: O(1)
    """
    if not prices:
        return 0
    hold, sold, rest = float('-inf'), 0, 0
    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)
    return max(sold, rest)

# =============================================================================
# 3. Matrix Exponentiation (O(log N) nth Fibonacci)
# =============================================================================

def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Multiplies two 2x2 matrices."""
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_pow(mat: List[List[int]], p: int) -> List[List[int]]:
    """Computes mat^p in O(log p) time."""
    result = [[1, 0], [0, 1]] # Identity matrix
    base = copy.deepcopy(mat)
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, base)
        base = matrix_mult(base, base)
        p //= 2
    return result

def fib_matrix(n: int) -> int:
    """
    Computes the n-th Fibonacci number using Matrix Exponentiation.
    Time Complexity: O(log N)
    Space Complexity: O(1)
    """
    if n <= 1:
        return n
    T = [[1, 1], [1, 0]]
    T_n = matrix_pow(T, n - 1)
    return T_n[0][0]


def run_tests():
    print("Testing Optimized DP algorithms...")
    
    # Space Optimization Tests
    assert fib_optimized(10) == 55
    grid = [[1,3,1],[1,5,1],[4,2,1]]
    assert min_path_sum_optimized(grid) == 7
    print("Space Optimization tests passed.")
    
    # State Machine DP Tests
    assert max_profit_cooldown([1,2,3,0,2]) == 3
    print("State Machine DP tests passed.")
    
    # Matrix Exponentiation Tests
    assert fib_matrix(10) == 55
    assert fib_matrix(50) == 12586269025
    print("Matrix Exponentiation tests passed.")

if __name__ == "__main__":
    run_tests()

"""
Interview Challenge:
How would you use Matrix Exponentiation to solve a linear recurrence relation of the form:
F(n) = a*F(n-1) + b*F(n-2) + c*F(n-3)?
Hint: You'll need a 3x3 transformation matrix.
"""
