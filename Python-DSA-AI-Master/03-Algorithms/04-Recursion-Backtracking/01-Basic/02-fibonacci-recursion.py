"""
Module: Fibonacci Sequence using Recursion

Learning Objectives:
1. Understand the Fibonacci sequence mathematically.
2. Implement multiple overlapping recursive calls.
3. Recognize the exponential time complexity of naive recursion.
4. Optimize using memoization (Top-down DP).
5. Compare with iterative (Bottom-up DP) approach.

Concept Explanation:
The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones.
Recurrence relation:
  F(n) = F(n-1) + F(n-2)
Base cases:
  F(0) = 0, F(1) = 1

Imports:
"""
import timeit
from functools import lru_cache

def fibonacci_naive(n: int) -> int:
    """Basic implementation: Naive recursion. O(2^n) time."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Intermediate implementation: Recursion with memoization. O(n) time."""
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)

def fibonacci_iterative(n: int) -> int:
    """Advanced implementation: Iteration with O(1) space and O(n) time."""
    if n < 0:
        raise ValueError("Negative numbers not allowed")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def performance_analysis():
    """Analyze performance of different implementations."""
    setup = "from __main__ import fibonacci_naive, fibonacci_memoized, fibonacci_iterative"
    
    print("Performance Analysis:")
    n = 30
    t_naive = timeit.timeit(f"fibonacci_naive({n})", setup=setup, number=10)
    t_memo = timeit.timeit(f"fibonacci_memoized({n})", setup=setup, number=10)
    t_iter = timeit.timeit(f"fibonacci_iterative({n})", setup=setup, number=10)
    print(f"n = {n} | Naive: {t_naive:.5f}s | Memoized: {t_memo:.5f}s | Iterative: {t_iter:.5f}s")
        
def edge_cases():
    """Handle and demonstrate edge cases."""
    print("\nEdge Cases:")
    try:
        fibonacci_naive(-1)
    except ValueError as e:
        print(f"Negative input handled: {e}")

def interview_challenge():
    """
    Challenge: Matrix Exponentiation approach to find Nth Fibonacci in O(log N).
    """
    def multiply(mat1, mat2):
        x = mat1[0][0] * mat2[0][0] + mat1[0][1] * mat2[1][0]
        y = mat1[0][0] * mat2[0][1] + mat1[0][1] * mat2[1][1]
        z = mat1[1][0] * mat2[0][0] + mat1[1][1] * mat2[1][0]
        w = mat1[1][0] * mat2[0][1] + mat1[1][1] * mat2[1][1]
        mat1[0][0], mat1[0][1], mat1[1][0], mat1[1][1] = x, y, z, w

    def power(mat, n):
        if n == 0 or n == 1:
            return
        M = [[1, 1], [1, 0]]
        power(mat, n // 2)
        multiply(mat, mat)
        if n % 2 != 0:
            multiply(mat, M)

    def fib_matrix(n):
        if n == 0:
            return 0
        mat = [[1, 1], [1, 0]]
        power(mat, n - 1)
        return mat[0][0]
        
    print(f"\nInterview Challenge: Fibonacci(50) using matrix exponentiation: {fib_matrix(50)}")

def run_tests():
    """Unit tests for the implementations."""
    assert fibonacci_naive(10) == 55
    assert fibonacci_memoized(10) == 55
    assert fibonacci_iterative(10) == 55
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Fibonacci Recursion ---\n")
    print(f"Fibonacci(10) = {fibonacci_iterative(10)}")
    performance_analysis()
    edge_cases()
    interview_challenge()
    run_tests()
