"""
Miller-Rabin Primality Test

Learning Objectives:
1. Understand probabilistic primality testing.
2. Implement the Miller-Rabin algorithm.
3. Understand how to make it deterministic for reasonable limits (e.g., up to 2^64).

Concept Explanation:
The Miller-Rabin primality test is a probabilistic algorithm which determines whether a given number is prime.
It relies on the property that for a prime p and any a < p, a^(p-1) = 1 (mod p).
If p > 2 is prime, p-1 is even, so p-1 = d * 2^s.
Then either a^d = 1 (mod p) or a^(d*2^r) = -1 (mod p) for some 0 <= r < s.
"""

import random

def power_mod(base: int, exp: int, mod: int) -> int:
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

def miller_rabin_test(d: int, n: int, a: int) -> bool:
    """Helper for Miller-Rabin. Returns False if composite, True if probably prime."""
    x = power_mod(a, d, n)
    if x == 1 or x == n - 1:
        return True
        
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        
        if x == 1:
            return False
        if x == n - 1:
            return True
            
    return False

def is_prime_miller_rabin(n: int, k: int = 5) -> bool:
    """
    Probabilistic implementation.
    k is the number of iterations; higher k = higher accuracy.
    """
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    
    # Find d such that n-1 = d * 2^r
    d = n - 1
    while d % 2 == 0:
        d //= 2
        
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not miller_rabin_test(d, n, a):
            return False
            
    return True

def is_prime_deterministic(n: int) -> bool:
    """
    Deterministic for 64-bit integers by testing against a specific set of bases.
    """
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    
    d = n - 1
    while d % 2 == 0:
        d //= 2
        
    # Valid bases for testing up to 2^64
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n <= a:
            break
        if not miller_rabin_test(d, n, a):
            return False
            
    return True

# Performance Analysis:
# Time Complexity: O(k * log^3(n)) where k is the number of bases tested.
# Space Complexity: O(1)

# Edge Cases:
# Small numbers like 2, 3, and even numbers should be handled directly to avoid invalid bounds in random generation.

# Interview Challenge:
# Generate a large random prime number with a specific bit length (e.g., 512 bits).
def generate_large_prime(bits: int) -> int:
    while True:
        # Generate random odd number
        p = random.getrandbits(bits)
        p |= (1 << bits - 1) | 1
        if is_prime_miller_rabin(p, k=10):
            return p

def run_tests():
    assert is_prime_miller_rabin(2) == True
    assert is_prime_miller_rabin(4) == False
    assert is_prime_miller_rabin(97) == True
    assert is_prime_deterministic(104729) == True  # 10000th prime
    assert is_prime_deterministic(104730) == False
    print("All miller-rabin tests passed!")

if __name__ == "__main__":
    run_tests()
