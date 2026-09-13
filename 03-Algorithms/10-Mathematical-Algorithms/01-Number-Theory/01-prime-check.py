"""
# ==============================================================================
# LABORATORY: PRIMALITY TESTING (SIEVE & MILLER-RABIN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Prime Number is a number greater than 1 that has exactly two divisors: 1 
# and itself. (e.g., 2, 3, 5, 7, 11).
# 
# Why do we care? Prime numbers are the fundamental building blocks of Modern 
# Cryptography (RSA). The security of the entire global banking system, the 
# internet (HTTPS), and secure messaging relies entirely on the fact that it is 
# easy to multiply two massive prime numbers, but almost impossible to factor 
# them back apart.
#
# How do we check if a number $N$ is prime?
# 1. Naive Trial Division: Check every number from 2 to $N-1$. $O(N)$ time.
#    (If $N$ is a 100-digit number, this takes longer than the age of the universe).
#
# 2. Optimized Trial Division: Check from 2 up to $\sqrt{N}$. $O(\sqrt{N})$.
#    (Why? Because factors come in pairs. If $A \times B = N$, one of them MUST 
#    be $\le \sqrt{N}$).
#
# 3. Sieve of Eratosthenes: If you need to find ALL prime numbers up to $N$, 
#    checking them one by one takes $O(N \sqrt{N})$. 
#    The Sieve instantly crosses out multiples in an array, finding all primes 
#    in a blindingly fast $O(N \log \log N)$ time.
#
# 4. Miller-Rabin Primality Test: How does Python or OpenSSL check if a 
#    massive 1024-bit integer is prime? $\sqrt{N}$ is still too slow!
#    They use a Probabilistic Mathematical test based on Fermat's Little Theorem.
#    It takes $O(K \log^3 N)$ time (where $K$ is the number of accuracy iterations).
#    For 64-bit integers, it is mathematically proven to be 100% Deterministic 
#    if you check just 7 specific prime bases!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the $\sqrt{N}$ mathematical boundary.
# - Implement the Sieve of Eratosthenes.
# - Master the Miller-Rabin cryptographic primality test.
#
# ==============================================================================
"""

import math
import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. O(SQRT(N)) TRIAL DIVISION
# ==============================================================================
def is_prime_sqrt(n: int) -> bool:
    """
    Standard Trial Division in O(sqrt(N)) time.
    """
    if n <= 1: return False
    if n <= 3: return True
    
    # 1. CONSTANT TIME OPTIMIZATIONS
    # Skip all even numbers and multiples of 3 instantly!
    # This mathematically eliminates 66.6% of all integers in O(1) time!
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    # 2. THE SQRT LOOP
    # All prime numbers (greater than 3) take the form of 6k ± 1.
    # Therefore, we can step by 6!
    # We check `i` (which is 6k - 1) and `i + 2` (which is 6k + 1).
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True


# ==============================================================================
# 4. THE SIEVE OF ERATOSTHENES (O(N LOG LOG N))
# ==============================================================================
def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Finds ALL prime numbers up to `n` in O(N log log N) time.
    """
    if n < 2: return []
    
    # Create a boolean array, assuming everything is Prime initially.
    # We use True/False to save RAM.
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    # We only need to run the outer loop up to sqrt(N)!
    # Why? Because any composite number > sqrt(N) will ALREADY have been 
    # crossed out by one of its smaller prime factors!
    limit = int(math.isqrt(n))
    
    for p in range(2, limit + 1):
        if is_prime[p]:
            
            # If `p` is prime, CROSS OUT all multiples of `p`!
            # Optimization: We can start crossing out at `p^2`. 
            # (Because p*2, p*3, etc. were already crossed out by 2, 3, etc.)
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
                
    # Extract the physical prime numbers
    primes = [i for i, prime in enumerate(is_prime) if prime]
    return primes


# ==============================================================================
# 5. MILLER-RABIN PRIMALITY TEST (O(K LOG^3 N))
# ==============================================================================
def is_prime_miller_rabin(n: int, k: int = 5) -> bool:
    """
    Probabilistic Primality Test.
    Used in RSA cryptography for massive 1024-bit numbers.
    """
    # 1. Base Edge Cases
    if n <= 1: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    
    # 2. FACTOR OUT POWERS OF 2
    # We want to write (N - 1) as (2^r * d) where d is an odd number.
    # This prepares the mathematical stage for Fermat's Little Theorem.
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
    # 3. THE WITNESS LOOP
    # We will test `k` random bases.
    # For a 64-bit integer, if we test exactly these 7 bases: [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    # The result is mathematically guaranteed 100% deterministic! No false positives.
    
    for _ in range(k):
        # Pick a random base 'a'
        a = random.randint(2, n - 2)
        
        # Calculate x = (a^d) % n
        # Python's built-in `pow()` uses Modular Exponentiation (Fast Powering Algorithm).
        # It takes strictly O(log D) time! This is the secret to its speed.
        x = pow(a, d, n)
        
        # Condition 1: If x is 1 or (n - 1), it passes this round! 'a' thinks it's prime.
        if x == 1 or x == n - 1:
            continue
            
        # Condition 2: Repeatedly square 'x' up to 'r-1' times.
        # We are checking the sequence: a^d, a^2d, a^4d ... a^(2^(r-1)*d)
        is_composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            
            # If any of the squared terms hits (n - 1), it passes!
            if x == n - 1:
                is_composite = False
                break
                
        # If it failed BOTH conditions, we have absolute mathematical proof that 
        # N is a Composite number! We halt instantly.
        if is_composite:
            return False
            
    # If it survived `k` rounds of intense mathematical grilling, it is 
    # overwhelmingly likely to be Prime!
    return True


def demonstrate_primality():
    section_header("Algorithm: O(sqrt(N)) Primality")
    num = 1000000007 # A famous large prime
    print(f"Is {num} prime? -> {is_prime_sqrt(num)}")
    
    section_header("Algorithm: Sieve of Eratosthenes")
    limit = 100
    print(f"Finding all primes up to {limit}...")
    primes = sieve_of_eratosthenes(limit)
    print(f"Total Primes Found: {len(primes)}")
    print(f"List: {primes}")
    
    section_header("Algorithm: Miller-Rabin Cryptographic Test")
    # A massive 20-digit prime number
    massive_prime = 10000000000000000051 
    print(f"Checking massive integer: {massive_prime}")
    
    # Even sqrt(N) would take 3 Billion iterations (several seconds).
    # Miller-Rabin does it in microseconds!
    result = is_prime_miller_rabin(massive_prime)
    print(f"Miller-Rabin verdict (k=5): {'PRIME' if result else 'COMPOSITE'}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Sieve of Eratosthenes start crossing out multiples at $p^2$?
   Answer: Optimization! If you are evaluating $p = 7$, its multiples are 14, 21, 28, 35, 42, 49. 
   - 14 ($2 \times 7$) was already crossed out when evaluating $p = 2$.
   - 21 ($3 \times 7$) was already crossed out by $p = 3$.
   - 35 ($5 \times 7$) was already crossed out by $p = 5$.
   Every multiple less than $7 \times 7$ is guaranteed to have a smaller prime factor! Therefore, the absolute first uncrossed multiple of 7 is exactly $7^2 = 49$.

2. What is Fermat's Little Theorem?
   Answer: The bedrock of prime testing. It states: If $p$ is a prime number, then for any integer $a$, $a^{p-1} - 1$ is a perfect multiple of $p$. 
   Expressed in modulo math: $a^{p-1} \equiv 1 \pmod p$.
   If you calculate $2^{N-1} \pmod N$ and the answer is NOT 1, you have absolute mathematical proof that $N$ is NOT a prime number! (However, if the answer IS 1, it might still be a fake prime called a Carmichael Number, which is why Miller-Rabin adds the square root checks to eliminate the fakes).

3. How does Python's `pow(x, y, mod)` calculate $x^{1,000,000,000} \pmod M$ instantly?
   Answer: "Modular Exponentiation" (or Binary Exponentiation). Instead of multiplying by $x$ a billion times ($O(Y)$), it looks at the binary representation of $Y$. It squares the base continuously: $x \to x^2 \to x^4 \to x^8 \to x^{16}$, taking the modulo at every single step to keep the numbers tiny! It calculates the answer in strictly $O(\log Y)$ multiplications. For $Y = 1$ Billion, it takes only 30 operations!
"""

if __name__ == "__main__":
    demonstrate_primality()
    print("\n[SUCCESS] Laboratory: Primality Testing Completed.")
