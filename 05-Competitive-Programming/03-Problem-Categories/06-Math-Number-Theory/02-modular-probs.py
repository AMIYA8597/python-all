"""
## A. Concept Name
Modular Arithmetic Problems

## B. Motivation
Many competitive programming problems require results modulo 10^9+7 to avoid large number operations and overflow issues.

## C. Definition
Arithmetic operations performed on remainders after division by a modulus.

## D. Prerequisites
Basic algebra and understanding of remainders (Euclidean division).

## E. Core Idea
Operations (+, -, *) distribute over the modulo operator. Division requires modular multiplicative inverse.

## F. Algorithm
Fast modular exponentiation (binary exponentiation) and Modular Inverse using Fermat's Little Theorem or Extended Euclidean Algorithm.

## G. Time Complexity
O(log N) for exponentiation and modular inverse (where N is the exponent or the modulus).

## H. Space Complexity
O(1) auxiliary space.

## I. Base Cases
Base ^ 0 = 1. Modulo 1 is always 0.

## J. Edge Cases
Negative numbers in modulo, exponent being zero, modulo being 1.

## K. Common Pitfalls
Applying modulo to division directly: `(a/b) % m != ((a % m) / (b % m)) % m`. 

## L. Code Implementation
Provided below (fast exponentiation and modular inverse).

## M. Example Walkthrough
3^5 % 7:
3^5 = 3 * (3^2)^2 = 3 * 9^2. 
9 % 7 = 2, so 3 * 2^2 % 7 = 12 % 7 = 5.

## N. Visualization
Think of numbers on a clock face (modulo 12). 10 o'clock + 4 hours = 2 o'clock.

## O. Variations
Matrix exponentiation, modular logarithms (Baby-step Giant-step).

## P. Related Problems
Chinese Remainder Theorem, Lucas Theorem for combinations.

## Q. Testing
Test with small primes, test base > mod, test negative numbers.

## R. Debugging
Verify intermediate steps don't overflow the language's integer limits (not an issue in Python, but conceptually important).

## S. Optimization
Use iterative binary exponentiation instead of recursive. Use Python's native `pow(base, exp, mod)` which is highly optimized in C.

## T. Alternative Approaches
Using Python's built-in `pow()` directly instead of writing a custom function.

## U. Real-world Applications
Cryptography (RSA, Diffie-Hellman), hashing algorithms.

## V. Interview Tips
Always clarify if the modulus is prime. If it's not prime, you cannot use Fermat's Little Theorem for inverses.

## W. Glossary
Modulo, Multiplicative Inverse, Coprime, Fermat's Little Theorem.

## X. Project Connection
Useful for building cryptographic modules or solving competitive programming math queries within our AI analysis platform.
"""

def fast_modular_exponentiation(base: int, exp: int, mod: int) -> int:
    """
    Computes (base^exp) % mod in O(log exp) time.
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        
        base = (base * base) % mod
        exp >>= 1
        
    return result

def modular_inverse(a: int, m: int) -> int:
    """
    Computes the modular multiplicative inverse of a modulo m using Fermat's Little Theorem.
    Requires m to be a prime number.
    Returns x such that (a * x) % m == 1.
    """
    # According to Fermat's Little Theorem: a^(m-1) % m = 1
    # Multiplying both sides by a^-1: a^(m-2) % m = a^-1
    return fast_modular_exponentiation(a, m - 2, m)

def solve_modulo_problem():
    """
    Example runner for modular arithmetic.
    """
    MOD = 10**9 + 7
    base = 123456
    exp = 789012
    
    # Custom implementation
    ans1 = fast_modular_exponentiation(base, exp, MOD)
    
    # Python built-in
    ans2 = pow(base, exp, MOD)
    
    print(f"Custom: {ans1}, Built-in: {ans2}")
    
    # Modular inverse example
    a = 5
    inv = modular_inverse(a, MOD)
    print(f"Inverse of {a} mod {MOD} is {inv}")
    print(f"Verification: ({a} * {inv}) % {MOD} = {(a * inv) % MOD}")

if __name__ == "__main__":
    solve_modulo_problem()
