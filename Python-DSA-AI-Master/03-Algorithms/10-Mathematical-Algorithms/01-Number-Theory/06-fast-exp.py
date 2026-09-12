"""
Fast Exponentiation (Binary Exponentiation)

Learning Objectives:
1. Understand the naive O(n) exponentiation.
2. Learn Binary Exponentiation (Fast Exponentiation) to calculate a^n in O(log n).
3. Apply Fast Exponentiation with modulo arithmetic.

Concept Explanation:
Binary exponentiation calculates a^n in O(log n) multiplications.
Instead of multiplying 'a' n times, it squares the base and halves the exponent.
If the exponent is odd, it multiplies the result by the base.
a^n = (a^(n/2))^2 if n is even
a^n = a * (a^((n-1)/2))^2 if n is odd
"""

def power_basic(base: int, exp: int) -> int:
    """Basic implementation: O(n) time"""
    if exp < 0:
        base = 1 / base
        exp = -exp
    res = 1
    for _ in range(exp):
        res *= base
    return res

def power_fast(base: int, exp: int) -> int:
    """Advanced implementation: O(log n) time"""
    if exp < 0:
        base = 1 / base
        exp = -exp
        
    res = 1
    while exp > 0:
        if exp % 2 == 1:
            res *= base
        base *= base
        exp //= 2
    return res

def power_mod(base: int, exp: int, mod: int) -> int:
    """Fast Exponentiation with Modulo: O(log n) time"""
    res = 1
    base = base % mod
    if base == 0:
        return 0
        
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

# Performance Analysis:
# Basic: Time O(n), Space O(1)
# Fast / Mod: Time O(log n), Space O(1)

# Edge Cases:
# exp = 0 (returns 1)
# Negative exponent (handled with float division, but not typical in modular arithmetic)
# base = 0 (returns 0)

# Interview Challenge:
# Compute the sum of a geometric series a^0 + a^1 + ... + a^n modulo m
def geo_series_sum_mod(a: int, n: int, m: int) -> int:
    if n == 0:
        return 1
    if n % 2 == 1:
        # a^0 + ... + a^n = (a^0 + ... + a^(n//2)) * (1 + a^(n//2 + 1))
        half = geo_series_sum_mod(a, n // 2, m)
        return (half * (1 + power_mod(a, n // 2 + 1, m))) % m
    else:
        # a^0 + ... + a^n = a^0 + a * (a^0 + ... + a^(n-1))
        return (1 + a * geo_series_sum_mod(a, n - 1, m)) % m

def run_tests():
    assert power_basic(2, 5) == 32
    assert power_fast(2, 10) == 1024
    assert power_fast(3, 0) == 1
    assert power_mod(2, 10, 1000) == 24
    assert power_mod(5, 117, 10**9 + 7) == 245037562
    assert geo_series_sum_mod(2, 3, 100) == 15 # 1+2+4+8 = 15
    print("All fast-exp tests passed!")

if __name__ == "__main__":
    run_tests()
