"""
Module: Inclusion-Exclusion Principle

Learning Objectives:
1. Understand the mathematical formula of the Inclusion-Exclusion Principle (PIE).
2. Learn how to apply it to counting problems.
3. Compute the number of integers coprime to a set of numbers.

Concept Explanation:
- PIE is a counting technique to compute the size of a union of multiple sets.
- |A U B U C| = |A| + |B| + |C| - |A n B| - |A n C| - |B n C| + |A n B n C|
- It iterates over all non-empty subsets of sets, adding odd-sized intersections and subtracting even-sized ones.

Performance Analysis:
- Given k sets, there are 2^k - 1 subsets. Time complexity is O(2^k).
- Useful when k is small (e.g., k <= 20).

Edge Cases:
- Empty array of sets or prime factors.
"""

from typing import List
import math

# --- Basic Implementation ---
def count_divisible_by_2_or_3(n: int) -> int:
    """Count numbers in [1, n] divisible by 2 or 3."""
    c2 = n // 2
    c3 = n // 3
    c6 = n // 6 # LCM of 2 and 3
    return c2 + c3 - c6

# --- Intermediate Implementation ---
def count_divisible(n: int, primes: List[int]) -> int:
    """
    Count numbers in [1, n] divisible by at least one prime in the given list.
    Uses Inclusion-Exclusion Principle.
    """
    m = len(primes)
    ans = 0
    # Iterate through all 2^m - 1 subsets
    for i in range(1, 1 << m):
        bits = bin(i).count('1')
        lcm = 1
        for j in range(m):
            if (i & (1 << j)):
                lcm = (lcm * primes[j]) // math.gcd(lcm, primes[j])
        
        if bits % 2 == 1:
            ans += n // lcm
        else:
            ans -= n // lcm
    return ans

# --- Advanced Implementation ---
def derangements(n: int) -> int:
    """
    Compute number of derangements of n items (permutations where no item is in its original position).
    Formula: D(n) = n! * sum((-1)^i / i! for i in 0..n)
    Calculated via DP: D(n) = (n-1) * (D(n-1) + D(n-2))
    """
    if n == 0: return 1
    if n == 1: return 0
    d = [0] * (n + 1)
    d[0], d[1] = 1, 0
    for i in range(2, n + 1):
        d[i] = (i - 1) * (d[i - 1] + d[i - 2])
    return d[n]

# --- Interview Challenge ---
# Problem: Euler's Totient Function (Phi)
# Count integers up to n that are coprime to n.
def euler_totient(n: int) -> int:
    """Computes Phi(n) using prime factorization."""
    res = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            res -= res // p
        p += 1
    if n > 1:
        res -= res // n
    return res

# --- Tests ---
def run_tests():
    assert count_divisible_by_2_or_3(10) == 7 # 2,3,4,6,8,9,10
    assert count_divisible(10, [2, 3]) == 7
    assert derangements(4) == 9
    assert euler_totient(10) == 4 # 1, 3, 7, 9
    print("All tests passed for 05-incl-excl.py!")

if __name__ == "__main__":
    run_tests()
