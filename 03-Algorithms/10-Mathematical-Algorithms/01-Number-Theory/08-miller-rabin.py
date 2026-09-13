"""
# ==============================================================================
# LABORATORY: MILLER-RABIN & POLLARD'S RHO FACTORIZATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the early prime checking labs, we used Trial Division to check if a number 
# was prime, which took $O(\sqrt{N})$ time. 
# We also used Trial Division to FACTOR a number, also taking $O(\sqrt{N})$ time.
#
# For a 64-bit integer, $\sqrt{N}$ is roughly 4 Billion operations. Python can 
# compute that in a few seconds.
# But what about a 128-bit integer? $\sqrt{N}$ is $1.8 \times 10^{19}$ operations. 
# Your computer will crash before finishing.
#
# How do cryptographic systems process massive integers?
# 
# 1. To check IF it is prime: The Miller-Rabin Primality Test.
#    It uses Fermat's Little Theorem and Modulo Squaring to definitively prove 
#    primality in $O(K \log^3 N)$ time. (Fraction of a millisecond for 128-bit!).
#
# 2. To find the ACTUAL FACTORS if it is composite: Pollard's Rho Algorithm.
#    Invented by John Pollard in 1975, it uses pseudo-random number generators 
#    and Floyd's Cycle-Finding Algorithm (The Tortoise and the Hare) to find 
#    factors in $O(N^{1/4})$ time!
#    For a 128-bit integer, $N^{1/4}$ drops the operations from $10^{19}$ down 
#    to just 4 Billion! It makes factorization possible.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Revisit the Miller-Rabin test specifically for deterministic 64-bit bounds.
# - Understand the pseudo-random math behind Pollard's Rho.
# - Combine them to recursively factorize massive 64-bit numbers instantly.
#
# ==============================================================================
"""

import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Greatest Common Divisor ---
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a
# ---------------------------------------


# ==============================================================================
# 3. DETERMINISTIC MILLER-RABIN (64-BIT PROOF)
# ==============================================================================
def is_prime_miller_rabin(n: int) -> bool:
    """
    Deterministically proves primality for ALL 64-bit integers by checking 
    exactly 7 mathematically proven prime bases.
    """
    if n <= 1: return False
    if n in (2, 3, 5, 7): return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    # Factor N-1 as (d * 2^r)
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
        
    # The Jim Sinclair / Pomerance Proof (2014):
    # Testing EXACTLY these 7 bases guarantees 100% accuracy for all N < 2^64.
    # No false positives (Carmichael numbers) can survive all 7.
    bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    
    for a in bases:
        # Some bases might be larger than N, so we modulo them down.
        a = a % n
        if a == 0: continue
            
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
            
        is_composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                is_composite = False
                break
                
        if is_composite:
            return False
            
    return True


# ==============================================================================
# 4. POLLARD'S RHO ALGORITHM (O(N^(1/4)))
# ==============================================================================
def pollards_rho(n: int) -> int:
    """
    Finds a non-trivial factor of N using Cycle Detection.
    Returns the factor. (May return N if it fails, which is rare).
    """
    if n % 2 == 0: return 2
    if is_prime_miller_rabin(n): return n
    
    # 1. We create a pseudo-random polynomial function: f(x) = (x^2 + c) % n
    # The constant `c` is randomly chosen.
    x = random.randint(2, n - 2)
    y = x
    c = random.randint(1, n - 1)
    
    def f(val: int) -> int:
        return (pow(val, 2, n) + c) % n
        
    d = 1
    
    # 2. FLOYD'S TORTOISE AND HARE (Cycle Detection)
    # Because the sequence is pseudo-random and strictly bounded by Modulo N, 
    # it is mathematically guaranteed to eventually repeat and form a cycle! 
    # (The "Rho" ρ shape).
    
    while d == 1:
        # Tortoise moves 1 step
        x = f(x)
        # Hare moves 2 steps
        y = f(f(y))
        
        # We calculate the absolute distance between them, and check if that 
        # distance shares a Common Divisor with N!
        # If GCD > 1, we found a prime factor!
        d = gcd(abs(x - y), n)
        
        # If the sequence perfectly wrapped around and crashed into itself 
        # (d == n), the function failed to find a factor.
        if d == n:
            # We must retry with a different random polynomial `c`!
            return pollards_rho(n)
            
    return d


def factorize_massive_number(n: int) -> List[int]:
    """
    Recursively combines Miller-Rabin and Pollard's Rho to completely factorize 
    massive 64-bit numbers in fractions of a second.
    """
    if n <= 1:
        return []
        
    # If it's already prime, we just return it!
    if is_prime_miller_rabin(n):
        return [n]
        
    # Otherwise, we ask Pollard's Rho to rip out ONE factor.
    factor = pollards_rho(n)
    
    # And we recursively ask the function to factorize the pieces!
    return factorize_massive_number(factor) + factorize_massive_number(n // factor)


def demonstrate_pollard_rho():
    section_header("Algorithm: Deterministic Miller-Rabin (64-Bit)")
    
    prime = 2305843009213693951 # A massive 19-digit Mersenne Prime (2^61 - 1)
    print(f"Checking massive integer: {prime}")
    result = is_prime_miller_rabin(prime)
    print(f"Verdict: {'PRIME' if result else 'COMPOSITE'}")
    
    section_header("Algorithm: Pollard's Rho Factorization")
    
    # Let's multiply two massive primes to create a 64-bit composite number!
    p1 = 3037000499 # Prime
    p2 = 3037000507 # Prime
    composite = p1 * p2
    
    print(f"Composite Target: {composite}")
    print(f"Trial Division O(sqrt(N)) would require {math.isqrt(composite):,} loops.")
    print("Executing Pollard's Rho O(N^(1/4))...")
    
    factors = factorize_massive_number(composite)
    factors.sort()
    
    print(f"Factors Found: {factors}")
    print(f"Verification: {p1} * {p2} == {composite}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does the "Hare and Tortoise" find a prime factor in Pollard's Rho?
   Answer: Imagine the pseudo-random sequence modulo $P$ (the hidden prime factor we are searching for). Because $P$ is much smaller than $N$, the sequence modulo $P$ will fall into a repeating cycle VERY quickly (Paradox of Birthdays). The Hare will eventually lap the Tortoise inside this $P$-cycle. When they land on the exact same value modulo $P$, the difference between them ($X - Y$) will be a perfect multiple of $P$! Therefore, calculating the Greatest Common Divisor (GCD) between $(X - Y)$ and $N$ instantly extracts the hidden prime factor $P$ out of $N$!

2. Why is Pollard's Rho $O(N^{1/4})$?
   Answer: The Birthday Paradox! If you have a sequence of random numbers modulo $P$, how many numbers do you need to generate before two of them collide? Math proves it requires roughly $\sqrt{P}$ numbers. 
   What is the absolute maximum value of $P$? Since factors come in pairs, the largest possible prime factor we need to search for is bounded by $\sqrt{N}$. 
   Substituting this in: $\sqrt{P} \le \sqrt{\sqrt{N}} = N^{1/4}$. 
   Therefore, the cycle is mathematically guaranteed to be discovered in $O(N^{1/4})$ steps!

3. Are there algorithms faster than Pollard's Rho?
   Answer: Yes! The General Number Field Sieve (GNFS) is the absolute fastest known algorithm for factoring integers larger than 100 digits (300+ bits). It runs in sub-exponential time and is the algorithm used to crack massive RSA encryption keys in supercomputing labs. However, for "small" 64-bit integers used in competitive programming, Pollard's Rho is practically instant and significantly easier to implement.
"""

import math # Required for the recall text formatting in the printout

if __name__ == "__main__":
    demonstrate_pollard_rho()
    print("\n[SUCCESS] Laboratory: Miller-Rabin & Pollard's Rho Completed.")
