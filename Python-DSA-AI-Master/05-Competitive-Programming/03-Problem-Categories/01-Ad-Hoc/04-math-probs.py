"""
## A. Concept Name
Competitive Programming Mathematics

## B. Core Intent
Understand and implement fundamental math algorithms for competitive programming: Binary/Fast Exponentiation, Sieve of Eratosthenes, Extended Euclidean Algorithm, and Combinatorics.

## C. Key Takeaways
- Mathematics can reduce time complexity from O(N) or O(N^2) to O(log N) or O(1).
- Binary Exponentiation computes a^b in O(log b).
- Sieve of Eratosthenes finds primes efficiently.
- Combinatorics with modulo require precomputing factorials and inverse factorials.

## D. Real-World Context
- Cryptography: RSA and Diffie-Hellman rely heavily on large prime numbers, modular arithmetic, and fast exponentiation.
- Hash Functions: String hashing algorithms use polynomial rolling hashes.
- Distributed Systems: Consistent hashing utilizes number theory properties.

## E. Technical Vocabulary
- Binary Exponentiation, Modulo Arithmetic, Sieve of Eratosthenes, Extended Euclidean Algorithm, Modular Multiplicative Inverse, Bezout's identity.

## F. Common Pitfalls
- Forgetting to use modulo arithmetic at EVERY addition/multiplication step, leading to overflow or slowdowns.
- Using division under modulo without calculating the Modular Inverse.

## G. Setup & Prerequisites
- Python basics, understanding of modular arithmetic properties.

## H. Step-by-Step Walkthrough
- Binary Exponentiation: Iteratively square the base and multiply to result if current bit of exponent is 1.
- Sieve: Iterate from 2 to sqrt(limit), mark all multiples of primes as non-prime.
- Extended GCD: Recursively find GCD and coefficients x, y for a*x + b*y = gcd.
- Combinatorics: Precompute factorials and their inverses to answer nCr % p queries in O(1).

## I. Best Practices
- Keep numbers small and operations fast O(1) by using modulo.

## J. Debugging Tips
- If inverse modulo fails, ensure the number and modulo are coprime.

## K. Performance Tuning
- Precompute factorials and primes if answering multiple queries.

## L. Testing Strategy
- Test algorithms against smaller edge cases where naive O(N) solutions are feasible for cross-validation.

## M. Code Organization
- Isolate each mathematical concept into distinct, reusable functions or classes.

## N. Security Considerations
- Cryptographic applications require constant-time mathematical algorithms to prevent timing attacks.

## O. Deployment Considerations
- Pure math functions can be deployed as robust, isolated microservices if needed.

## P. Maintenance & Scalability
- Python handles arbitrarily large integers, but they become slow; modulo ensures optimal scalability.

## Q. Data Handling
- Ensure input variables fit within memory limits when scaling to massive arrays.

## R. Related Patterns
- Matrix Exponentiation (extends Binary Exponentiation for linear recurrences).

## S. Alternatives
- Simulation or naive iterative approaches (only suitable for small constraints).

## T. External References
- CP-Algorithms (Number Theory sections).

## U. Further Reading
- Competitive Programmer's Handbook.

## V. Exercises
- Interview Challenge: "Count Paths on a Grid" - Calculate distinct paths moving Right/Up on an N x M grid modulo 10^9+7.

## W. FAQ
- Q: Why is 10^9+7 frequently used? A: It's a large prime number that fits in a standard 32-bit signed integer and prevents overflow during intermediate multiplications.

## X. Project Connection
These algorithms form the building blocks for solving advanced Ad-Hoc math problems and optimizing brute-force solutions in CP pipelines.
"""

import math
from typing import List, Tuple

# =============================================================================
# 1. Binary Exponentiation (Fast Power)
# =============================================================================
def fast_pow(base: int, exp: int, mod: int = 10**9 + 7) -> int:
    """
    Computes (base^exp) % mod in O(log exp) time.
    
    Explanation:
    Instead of multiplying 'base' by itself 'exp' times (O(N)), we look at the binary 
    representation of 'exp'. 
    For example: 3^13 = 3^(8 + 4 + 1) = 3^8 * 3^4 * 3^1.
    We iteratively square the base and multiply it to the result when the current bit of exp is 1.
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        # If the least significant bit is 1, multiply the current base to result
        if exp % 2 == 1:
            result = (result * base) % mod
        
        # Square the base for the next bit
        base = (base * base) % mod
        # Shift the exponent right by 1 bit (divide by 2)
        exp //= 2
        
    return result

# =============================================================================
# 2. Sieve of Eratosthenes
# =============================================================================
def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generates a list of prime numbers up to 'limit' in O(N log log N) time.
    
    Explanation:
    Start with an array of boolean values set to True. Iterate from 2 to sqrt(limit). 
    For each prime, mark all of its multiples as False (composite).
    """
    if limit < 2:
        return []
        
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[p]:
            # Mark multiples of p starting from p^2 (smaller multiples were marked by smaller primes)
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
                
    return [p for p, prime_status in enumerate(is_prime) if prime_status]

# =============================================================================
# 3. Extended Euclidean Algorithm & Modular Inverse
# =============================================================================
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Finds the greatest common divisor (GCD) of a and b, and the coefficients x and y 
    such that a*x + b*y = gcd(a, b). (Bezout's identity)
    
    Time Complexity: O(log(min(a, b)))
    """
    if a == 0:
        return b, 0, 1
        
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    # Update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def mod_inverse(n: int, p: int) -> int:
    """
    Finds the modular multiplicative inverse of n modulo p.
    Returns x such that (n * x) % p == 1.
    Raises ValueError if the inverse does not exist (when n and p are not coprime).
    
    Note: If p is prime, we can simply use Fermat's Little Theorem: fast_pow(n, p-2, p).
    This function uses Extended GCD, which works for ANY coprime n and p, not just prime p.
    """
    gcd, x, y = extended_gcd(n, p)
    if gcd != 1:
        raise ValueError(f"Modular inverse of {n} modulo {p} does not exist (GCD is {gcd}, not 1).")
    
    # x might be negative, so we take modulo p
    return (x % p + p) % p

# =============================================================================
# 4. Combinatorics (nCr Modulo P)
# =============================================================================
class Combinatorics:
    """
    Precomputes factorials and inverse factorials to answer nCr % p queries in O(1) time.
    Time Complexity: O(N) to build, O(1) per query.
    Space Complexity: O(N)
    """
    def __init__(self, max_n: int, mod: int = 10**9 + 7):
        self.mod = mod
        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)
        
        # Precompute factorials
        for i in range(1, max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % self.mod
            
        # Precompute inverse factorials
        # Inverse of N! is (N!)^(mod-2) % mod
        self.inv_fact[max_n] = fast_pow(self.fact[max_n], self.mod - 2, self.mod)
        
        # Compute other inverse factorials iteratively backwards
        # 1/(N-1)! = 1/N! * N
        for i in range(max_n - 1, -1, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % self.mod

    def nCr(self, n: int, r: int) -> int:
        """Computes "n choose r" modulo P."""
        if r < 0 or r > n:
            return 0
        
        # nCr = n! / (r! * (n-r)!)
        # Modulo arithmetic representation: n! * inv_fact[r] * inv_fact[n-r] % mod
        numerator = self.fact[n]
        denominator = (self.inv_fact[r] * self.inv_fact[n - r]) % self.mod
        
        return (numerator * denominator) % self.mod


# =============================================================================
# Tests and Main Guard
# =============================================================================
if __name__ == "__main__":
    print("Running Tests for Mathematics module...\n")
    MOD = 10**9 + 7

    # Test 1: Fast Exponentiation
    base, exp = 3, 13
    assert fast_pow(base, exp, MOD) == (3**13) % MOD
    print(f"fast_pow({base}, {exp}) % {MOD} = {fast_pow(base, exp, MOD)}")
    
    # Test 2: Sieve of Eratosthenes
    primes_up_to_30 = sieve_of_eratosthenes(30)
    assert primes_up_to_30 == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    print(f"Primes up to 30: {primes_up_to_30}")
    
    # Test 3: Extended GCD & Mod Inverse
    # Find inverse of 3 modulo 11. (3 * 4 = 12 = 1 mod 11) -> inverse is 4
    n, p = 3, 11
    inv = mod_inverse(n, p)
    assert inv == 4
    print(f"Modular inverse of {n} mod {p} is {inv} (Check: {n} * {inv} % {p} = {(n * inv) % p})")
    
    # Test 4: Combinatorics
    combo = Combinatorics(100, MOD)
    # 5 choose 2 = 10
    nCr_5_2 = combo.nCr(5, 2)
    assert nCr_5_2 == 10
    print(f"5 Choose 2 = {nCr_5_2}")
    print("\nAll tests passed successfully! 🚀")
