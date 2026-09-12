"""
## A. Concept Name
Prime Check Algorithms

## B. Concept Explanation
A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
The simplest way to check for primality is to test all numbers up to n.
A more efficient way is to test up to sqrt(n) because a larger factor of n must be a multiple of a smaller factor that has been already checked.

## C. Learning Objectives
1. Understand the definition of a prime number.
2. Implement a naive prime checking algorithm.
3. Optimize prime checking up to the square root of n.
4. Learn advanced prime checking for competitive programming.

## D. Performance Analysis
- Basic: O(n) time, O(1) space
- Intermediate: O(sqrt(n)) time, O(1) space
- Advanced: O(sqrt(n)) time, O(1) space (approx 3x faster than intermediate)

## E. Edge Cases
- n <= 1 (0, 1, negatives) are not prime.
- n = 2 is the only even prime.

## F. Interview Challenge
Given an array of integers, find the sum of all prime numbers.

## X. Project Connection
Understanding prime checking forms the foundation for algorithms in cryptography (like RSA) and is crucial for creating efficient hash tables.
"""

import math
import time

def is_prime_basic(n: int) -> bool:
    """Basic implementation: O(n)"""
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def is_prime_intermediate(n: int) -> bool:
    """Intermediate implementation: O(sqrt(n))"""
    if n <= 1:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_prime_advanced(n: int) -> bool:
    """Advanced implementation: O(sqrt(n)) with 6k +/- 1 optimization"""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sum_of_primes(arr: list[int]) -> int:
    return sum(x for x in arr if is_prime_advanced(x))

def run_tests():
    assert is_prime_basic(2) == True
    assert is_prime_basic(4) == False
    assert is_prime_intermediate(17) == True
    assert is_prime_intermediate(1) == False
    assert is_prime_advanced(97) == True
    assert is_prime_advanced(100) == False
    assert is_prime_advanced(-5) == False
    assert sum_of_primes([1, 2, 3, 4, 5]) == 10
    print("All prime-check tests passed!")

if __name__ == "__main__":
    run_tests()
