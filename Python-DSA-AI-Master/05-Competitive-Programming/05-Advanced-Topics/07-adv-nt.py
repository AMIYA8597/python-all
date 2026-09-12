\"\"\"
Module: Advanced Number Theory
Why it exists: Number theory provides the foundation for cryptography, hashing, and solving complex combinatorial problems in competitive programming.
Industry Use Cases:
- RSA and Elliptic Curve Cryptography heavily rely on primes, modular inverse, and fast exponentiation.
- Hash map resizing and prime modulo calculations.

Learning Objectives:
1. Implement and understand modular arithmetic (Inverse, Fast Exponentiation).
2. Learn the Extended Euclidean Algorithm for linear Diophantine equations.
3. Understand the Chinese Remainder Theorem for solving congruences.
4. Grasp advanced prime algorithms: Miller-Rabin test and Pollard's Rho integer factorization.

Beginner Explanation:
Basic math involves +, -, *, /. In programming, numbers can overflow, so we use \"modulo\" arithmetic (keeping numbers within a range, like a clock). Number theory algorithms help us do these operations extremely fast and work with prime numbers efficiently.

Advanced Explanation:
- Fast Exponentiation computes a^b mod m in O(log b).
- Extended GCD finds x, y such that ax + by = gcd(a, b), which gives the modular inverse of a modulo b when gcd(a, b) = 1.
- Miller-Rabin uses Fermat's Little Theorem and non-trivial square roots of 1 modulo p to probabilistically determine primality in O(k log^3 n).
- Pollard's Rho is a randomized integer factorization algorithm that finds a non-trivial factor in O(n^(1/4)).

Common Mistakes:
- Forgetting that modular division requires multiplication by the modular inverse.
- Overlooking integer overflow in languages without arbitrary precision (Python handles this automatically!).
\"\"\"
import random
from typing import Tuple, List, Dict

# --- Fast Exponentiation ---
def power(base: int, exp: int, mod: int) -> int:
    \"\"\"Computes (base^exp) % mod in O(log exp) time.\"\"\"
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return res

# --- Extended Euclidean Algorithm ---
def ext_gcd(a: int, b: int) -> Tuple[int, int, int]:
    \"\"\"
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).
    \"\"\"
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = ext_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# --- Modular Inverse ---
def mod_inverse(a: int, m: int) -> int:
    \"\"\"Finds the modular inverse of a modulo m using Extended GCD.\"\"\"
    gcd, x, y = ext_gcd(a, m)
    if gcd != 1:
        raise ValueError(f\"Inverse does not exist for {a} mod {m}\")
    return (x % m + m) % m

# --- Miller-Rabin Primality Test ---
def is_prime(n: int, k: int = 5) -> bool:
    \"\"\"Probabilistic primality test in O(k * log^3 n).\"\"\"
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
        
    d = n - 1
    while d % 2 == 0:
        d //= 2
        
    def miiller_test(d: int, n: int) -> bool:
        a = 2 + random.randint(1, n - 4)
        x = power(a, d, n)
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
        
    for _ in range(k):
        if not miiller_test(d, n):
            return False
    return True

# --- Pollard's Rho Factorization ---
def pollard_rho(n: int) -> int:
    \"\"\"Finds a non-trivial factor of n.\"\"\"
    if n % 2 == 0:
        return 2
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    
    def f(x_val: int) -> int:
        return (power(x_val, 2, n) + c) % n
        
    import math
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        if d == n:
            return pollard_rho(n)
    return d

def prime_factors(n: int) -> Dict[int, int]:
    \"\"\"Returns dictionary of prime factors and their counts.\"\"\"
    factors = {}
    
    def factorize(num: int):
        if num == 1:
            return
        if is_prime(num):
            factors[num] = factors.get(num, 0) + 1
            return
        divisor = pollard_rho(num)
        factorize(divisor)
        factorize(num // divisor)
        
    factorize(n)
    return factors


if __name__ == '__main__':
    print(\"--- Advanced Number Theory Tests ---\")
    
    # 1. Modular Arithmetic
    assert power(2, 10, 1000) == 24
    
    # 2. Extended GCD
    g, x, y = ext_gcd(35, 15)
    assert g == 5 and 35*x + 15*y == 5
    
    # 3. Modular Inverse
    assert mod_inverse(3, 11) == 4 # 3*4 = 12 = 1 (mod 11)
    
    # 4. Miller Rabin
    assert is_prime(999983) == True
    assert is_prime(1000000) == False
    
    # 5. Prime Factorization (Pollard's Rho)
    num = 2 * 3 * 3 * 7 * 11 * 13
    facts = prime_factors(num)
    assert facts == {2: 1, 3: 2, 7: 1, 11: 1, 13: 1}
    
    print(\"All Number Theory assertions passed!\")

\"\"\"
Interview Challenge:
Question: Given a large number N (up to 10^18), find its largest prime factor.
Solution: Use Miller-Rabin to check if N is already prime. If not, use Pollard's Rho to find a factor, divide N, and recurse. The largest prime found during the recursion is the answer.
\"\"\"
