"""
Module: Factorial using Recursion

Learning Objectives:
1. Understand the mathematical definition of a factorial.
2. Translate the mathematical recurrence relation into a recursive function.
3. Identify the base case and the recursive step.
4. Compare performance and space complexity of recursion vs. iteration.
5. Handle edge cases such as negative numbers or non-integers.

Concept Explanation:
Factorial of a non-negative integer n, denoted by n!, is the product of all positive integers less than or equal to n.
Recurrence relation:
  n! = n * (n - 1)!
Base case:
  0! = 1

Imports:
"""
import sys
import timeit
import math

def factorial_recursive(n: int) -> int:
    """Basic implementation of factorial using recursion."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base case
    if n == 0 or n == 1:
        return 1
    
    # Recursive step
    return n * factorial_recursive(n - 1)

def factorial_iterative(n: int) -> int:
    """Intermediate implementation using iteration to avoid call stack overflow."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial_tail_recursive(n: int, accumulator: int = 1) -> int:
    """Advanced implementation: Tail recursive approach (though Python doesn't optimize it)."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return accumulator
    return factorial_tail_recursive(n - 1, n * accumulator)

def performance_analysis():
    """Analyze performance of different implementations."""
    setup = "from __main__ import factorial_recursive, factorial_iterative"
    
    print("Performance Analysis:")
    for n in [10, 50, 100]:
        t_rec = timeit.timeit(f"factorial_recursive({n})", setup=setup, number=10000)
        t_iter = timeit.timeit(f"factorial_iterative({n})", setup=setup, number=10000)
        print(f"n = {n:3} | Recursive: {t_rec:.5f}s | Iterative: {t_iter:.5f}s")
        
def edge_cases():
    """Handle and demonstrate edge cases."""
    print("\nEdge Cases:")
    try:
        factorial_recursive(-5)
    except ValueError as e:
        print(f"Negative input handled: {e}")
        
    try:
        factorial_recursive(5.5)
    except TypeError as e:
        print(f"Non-integer input handled: {e}")

def interview_challenge():
    """
    Challenge: Count trailing zeroes in n! without calculating the factorial.
    Explanation: A trailing zero is produced by a factor of 10.
    10 = 2 * 5. In n!, the number of 2s is always greater than the number of 5s.
    So, count the number of 5s.
    """
    def count_trailing_zeroes(n: int) -> int:
        count = 0
        while n >= 5:
            n //= 5
            count += n
        return count
    
    print("\nInterview Challenge: Trailing zeroes in 100!")
    print(f"Result: {count_trailing_zeroes(100)}")

def run_tests():
    """Unit tests for the implementations."""
    assert factorial_recursive(0) == 1
    assert factorial_recursive(5) == 120
    assert factorial_iterative(5) == 120
    assert factorial_tail_recursive(5) == 120
    assert math.factorial(5) == 120
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Factorial Recursion ---\n")
    print(f"5! = {factorial_recursive(5)}")
    performance_analysis()
    edge_cases()
    interview_challenge()
    run_tests()
