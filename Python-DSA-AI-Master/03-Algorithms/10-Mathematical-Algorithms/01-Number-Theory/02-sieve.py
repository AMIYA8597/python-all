"""
Sieve of Eratosthenes

Learning Objectives:
1. Understand the concept of sieving to find primes efficiently.
2. Implement the basic Sieve of Eratosthenes.
3. Optimize the sieve space and time complexity.
4. Learn Segmented Sieve for large ranges.

Concept Explanation:
The Sieve of Eratosthenes is an ancient algorithm for finding all prime numbers up to any given limit.
It does so by iteratively marking as composite (i.e., not prime) the multiples of each prime, starting with the first prime number, 2.
"""

import math

def sieve_basic(n: int) -> list[int]:
    """Basic implementation: O(n log log n)"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, int(math.isqrt(n)) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
                
    return [p for p in range(2, n + 1) if is_prime[p]]

def sieve_advanced(n: int) -> list[bool]:
    """Advanced implementation: returning boolean array for O(1) queries"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.isqrt(n)) + 1):
        if is_prime[p]:
            is_prime[p*p: n+1: p] = [False] * len(is_prime[p*p: n+1: p])
    return is_prime

# Performance Analysis:
# Basic/Advanced: Time Complexity O(n log log n), Space Complexity O(n)
# Using boolean array slice assignment makes the advanced implementation highly optimized in Python.

# Edge Cases:
# n < 2: No primes exist.
# Querying large n can cause MemoryError if space exceeds RAM.

# Interview Challenge:
# Count the number of primes strictly less than n.
def count_primes(n: int) -> int:
    if n <= 2:
        return 0
    return sum(sieve_advanced(n - 1))

def run_tests():
    assert sieve_basic(10) == [2, 3, 5, 7]
    assert sieve_basic(1) == []
    assert count_primes(10) == 4
    assert count_primes(0) == 0
    print("All sieve tests passed!")

if __name__ == "__main__":
    run_tests()
