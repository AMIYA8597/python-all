"""
Module: Catalan Numbers

Learning Objectives:
1. Understand Catalan numbers and their applications.
2. Implement Catalan number generation using recursion, DP, and binomial coefficients.
3. Recognize interview problems solvable via Catalan numbers.

Concept Explanation:
- Catalan numbers form a sequence of natural numbers that occur in various counting problems.
- Applications: Number of valid parentheses, count of full binary trees, triangulations of a polygon.
- Formula: C(n) = (1 / (n + 1)) * (2n C n)

Performance Analysis:
- Recursive: O(3^n)
- DP: O(n^2) time, O(n) space
- Binomial Coefficient: O(n) time, O(1) space

Edge Cases:
- n = 0: C(0) = 1
- Negative n: Invalid
"""

import math
from typing import List

# --- Basic Implementation ---
def catalan_recursive(n: int) -> int:
    """Computes nth Catalan number using recursion (exponential time)."""
    if n <= 1:
        return 1
    res = 0
    for i in range(n):
        res += catalan_recursive(i) * catalan_recursive(n - i - 1)
    return res

# --- Intermediate Implementation ---
def catalan_dp(n: int) -> int:
    """Computes nth Catalan number using Dynamic Programming (O(n^2) time)."""
    if n <= 1:
        return 1
    catalan = [0] * (n + 1)
    catalan[0] = catalan[1] = 1
    
    for i in range(2, n + 1):
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - j - 1]
    return catalan[n]

# --- Advanced Implementation ---
def catalan_binomial(n: int) -> int:
    """Computes nth Catalan number using binomial coefficients (O(n) time)."""
    if n < 0: return 0
    c = math.comb(2 * n, n)
    return c // (n + 1)

# --- Interview Challenge ---
# Problem: Generate Parentheses
# Generate all combinations of well-formed parentheses given n pairs.
def generate_parenthesis(n: int) -> List[str]:
    res = []
    def backtrack(s: str, left: int, right: int):
        if len(s) == 2 * n:
            res.append(s)
            return
        if left < n:
            backtrack(s + '(', left + 1, right)
        if right < left:
            backtrack(s + ')', left, right + 1)
    backtrack("", 0, 0)
    return res

# --- Tests ---
def run_tests():
    assert catalan_recursive(3) == 5
    assert catalan_dp(4) == 14
    assert catalan_binomial(5) == 42
    
    parentheses = generate_parenthesis(3)
    assert len(parentheses) == catalan_binomial(3)
    assert "((()))" in parentheses
    assert "()()()" in parentheses
    print("All tests passed for 02-catalan.py!")

if __name__ == "__main__":
    run_tests()
