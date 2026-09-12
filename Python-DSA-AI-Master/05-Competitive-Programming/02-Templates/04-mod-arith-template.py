"""
## A. Concept Name
Modular Arithmetic (Mod Math)

## B. Motivation (Why use this?)
In competitive programming, results can exceed the maximum bounds of standard 64-bit integers. Modulo operations keep numbers within bounds, preventing overflow in typed languages while avoiding arbitrary-precision slowdowns in Python. Operations happen in O(1) or O(log N) time.

## C. Intuition/Mental Model
Think of a clock face. On a 12-hour clock, 13:00 is 1:00. You wrap around once you hit the limit (the modulo `M`). The same wrapping applies to addition, subtraction, and multiplication.

## D. Problem Mapping (When to use?)
- When the problem asks for the answer "modulo 10^9+7" or "modulo 998244353".
- Combinatorics problems (nCr, nPr) with large constraints.
- Fast Matrix exponentiation calculations.
- Probability modulo prime (P * Q^-1 mod M).

## E. Core Logic (How it works?)
- (A + B) % M = ((A % M) + (B % M)) % M
- (A - B) % M = ((A % M) - (B % M) + M) % M
- (A * B) % M = ((A % M) * (B % M)) % M
- (A / B) % M = (A * B^-1) % M 
where B^-1 is the modular multiplicative inverse of B modulo M.

## F. Dry Run / Tracing
Example: (5 - 8) % 7
= ((5 % 7) - (8 % 7) + 7) % 7
= (5 - 1 + 7) % 7
= 11 % 7 = 4.

## G. Code Implementation
(See the ModArithmetic and Combinatorics classes below)

## H. Complexity Analysis
- Addition, Subtraction, Multiplication: Time O(1), Space O(1).
- Exponentiation (a^b): Time O(log b), Space O(1).
- Inverse (Fermat's): Time O(log M), Space O(1).
- Combinatorics Precomputation: Time O(N), Space O(N). Queries (nCr/nPr): Time O(1).

## I. Edge Cases & Handling
- Negative Numbers: Always add `M` before taking modulo to ensure positive results.
- Division: Only valid if the denominator is coprime to `M`.
- Zero Denominator: Division by 0 must be handled before calling the modular inverse.

## J. Variations & Extensions
- Chinese Remainder Theorem (CRT) for solving systems of congruences.
- Lucas Theorem for computing `nCr % P` when `N` is huge but `P` is small.

## K. Optimization Techniques
- Use `pow(base, exp, mod)` in Python instead of custom `O(log N)` exponentiation as it is optimized in C.
- Precomputing factorials and inverse factorials allows O(1) `nCr` query answering.

## L. Common Pitfalls & Mistakes
- `(A / B) % M != (A % M) / (B % M)`. You MUST multiply by the modular inverse.
- Forgetting to take modulo at intermediate steps in Python, causing big-integer arithmetic slowdowns.

## M. Debugging Strategies
- Use small modulo (e.g., 7 or 13) and print intermediate values.
- Verify properties manually, like `(A * inv(A)) % M == 1`.

## N. Related Concepts
- Number Theory, Prime Factorization, Fermat's Little Theorem, Extended Euclidean Algorithm.

## O. Quick Revision Guide
- Fermat's Little Theorem: `A^(p-1) ≡ 1 mod p`
- Modular Inverse: `A^-1 = A^(p-2) mod p` (when `p` is prime)

## P. Standard Templates
(Included in this file as standard classes)

## Q. Practice Problems
- CSES Problem Set: Exponentiation, Binomial Coefficients.
- Codeforces: "Number of Ways", Combinatorics and Math tags.

## R. Mathematical Foundations
- Congruence relations: `a ≡ b (mod n)` implies `n` divides `(a - b)`.
- Multiplicative inverse exists if and only if `gcd(a, m) = 1`.

## S. Pattern Recognition
- Keywords: "number of ways modulo M", "huge output", "probabilities modulo 998244353".

## T. Interview Checklists
- Can you explain Fermat's Little Theorem?
- How do you find the modular inverse if M is not prime? (Answer: Extended Euclidean Algorithm).

## U. Real-World Applications
- Cryptography (RSA algorithm, Diffie-Hellman Key Exchange).
- Hash Functions and Hash Maps.

## V. Memory Aids/Mnemonics
- Subtracting? Add M first: `(A - B + M) % M`.
- Dividing? Multiply by Inverse: `(A * B^(M-2)) % M`.

## W. System Design Context
- Consistent hashing rings use modular arithmetic to distribute cache entries across servers.

## X. Project Connection
- Used heavily in cryptographic libraries, pseudorandom number generators, and big integer math systems.
"""

from typing import List, Tuple

# Standard prime moduli
MOD1 = 10**9 + 7
MOD2 = 998244353

class ModArithmetic:
    def __init__(self, mod: int = MOD1):
        """Initialize with a prime modulo."""
        self.mod = mod

    def add(self, a: int, b: int) -> int:
        """Modular addition."""
        return (a + b) % self.mod

    def sub(self, a: int, b: int) -> int:
        """Modular subtraction."""
        return (a - b + self.mod) % self.mod

    def mul(self, a: int, b: int) -> int:
        """Modular multiplication."""
        return (a * b) % self.mod

    def power(self, base: int, exp: int) -> int:
        """
        Modular exponentiation: (base^exp) % mod
        Computes in O(log(exp)) time. Note: Python's built-in pow() is heavily optimized.
        """
        return pow(base, exp, self.mod)
    
    def inv(self, n: int) -> int:
        """
        Modular inverse of n modulo mod.
        Requires mod to be prime (Fermat's Little Theorem).
        n^-1 = n^(mod - 2) % mod
        """
        return self.power(n, self.mod - 2)

    def div(self, a: int, b: int) -> int:
        """Modular division: (a / b) % mod"""
        return self.mul(a, self.inv(b))

class Combinatorics:
    """Precomputes factorials for O(1) nCr and nPr queries."""
    
    def __init__(self, max_n: int, mod: int = MOD1):
        self.mod = mod
        self.max_n = max_n
        self.fact = [1] * (max_n + 1)
        self.inv_fact = [1] * (max_n + 1)
        self._precompute()

    def _precompute(self):
        """Precomputes factorials and their modular inverses."""
        for i in range(2, self.max_n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % self.mod
        
        # Compute inverse of highest factorial
        self.inv_fact[self.max_n] = pow(self.fact[self.max_n], self.mod - 2, self.mod)
        
        # Compute other inverses retroactively
        for i in range(self.max_n - 1, 0, -1):
            self.inv_fact[i] = (self.inv_fact[i + 1] * (i + 1)) % self.mod

    def nCr(self, n: int, r: int) -> int:
        """Combinations: n choose r."""
        if r < 0 or r > n:
            return 0
        num = self.fact[n]
        den = (self.inv_fact[r] * self.inv_fact[n - r]) % self.mod
        return (num * den) % self.mod

    def nPr(self, n: int, r: int) -> int:
        """Permutations: n arrange r."""
        if r < 0 or r > n:
            return 0
        return (self.fact[n] * self.inv_fact[n - r]) % self.mod

# --- Example Usage and Tests ---
if __name__ == "__main__":
    mod_math = ModArithmetic(MOD1)
    
    # Test basic ops
    assert mod_math.add(MOD1 - 1, 2) == 1
    assert mod_math.sub(2, 5) == MOD1 - 3
    assert mod_math.mul(MOD1 // 2, 4) == (MOD1 // 2 * 4) % MOD1
    
    # Test division and inverse
    # 5 / 2 = 5 * (2^-1)
    ans = mod_math.div(5, 2)
    # Check if ans * 2 == 5 mod MOD1
    assert mod_math.mul(ans, 2) == 5
    
    # Test Combinatorics
    combo = Combinatorics(1000, MOD1)
    # 5C2 = 10
    assert combo.nCr(5, 2) == 10
    # 5P2 = 20
    assert combo.nPr(5, 2) == 20
    
    print("All Modular Arithmetic tests passed!")
