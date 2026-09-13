"""
# ==============================================================================
# LABORATORY: ADVANCED SIEVES (LINEAR SIEVE & SEGMENTED)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned the standard Sieve of Eratosthenes. It runs in O(N log log N).
# While O(N log log N) is functionally close to O(N), the standard sieve has 
# a slight inefficiency: It crosses out composite numbers multiple times.
# (e.g., 30 is crossed out by 2, then by 3, then by 5).
# 
# Can we achieve strict, mathematically pure O(N) time?
# Yes! The Euler Sieve (Linear Sieve) guarantees every composite number is 
# crossed out exactly ONCE: by its Smallest Prime Factor (SPF).
#
# Why is the SPF so powerful?
# If we pre-compute the SPF for every number, we can instantly factorize ANY 
# number in O(log N) time! 
# Instead of Trial Division, we just repeatedly divide the number by its SPF 
# until it reaches 1. This is heavily used in algorithmic trading and cryptography.
#
# The Segmented Sieve:
# What if you need to find all primes between 1,000,000,000,000 and 1,000,000,100,000?
# A standard sieve would require allocating an array of 1 Trillion booleans 
# (which takes 1,000 Gigabytes of RAM). Your computer will crash.
# 
# The Segmented Sieve solves this. It only sieves up to sqrt(R), and then uses 
# those primes to specifically target the isolated [L, R] window! It uses almost 
# zero RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement the O(N) Linear Sieve.
# - Utilize the SPF array for O(log N) prime factorization.
# - Implement the Segmented Sieve for massive localized intervals.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE EULER LINEAR SIEVE & SPF FACTORIZATION (O(N))
# ==============================================================================
class LinearSieve:
    def __init__(self, limit: int):
        self.limit = limit
        self.primes = []
        
        # SPF (Smallest Prime Factor) Array
        # spf[i] will store the absolute smallest prime that evenly divides `i`.
        # Initially, we assume every number's smallest prime factor is itself.
        self.spf = [i for i in range(limit + 1)]
        
        self._build_sieve()
        
    def _build_sieve(self):
        for i in range(2, self.limit + 1):
            
            # If the SPF is still itself, it must be a Prime number!
            if self.spf[i] == i:
                self.primes.append(i)
                
            # The Magic O(N) Loop:
            # We iterate through all discovered primes. We multiply `i` by the prime 
            # to generate a composite number, and we set that composite's SPF!
            for p in self.primes:
                composite = i * p
                
                if composite > self.limit:
                    break
                    
                # We definitively mark the smallest prime factor!
                self.spf[composite] = p
                
                # THE O(N) GUARANTEE TRIGGER:
                # If `i` is cleanly divisible by `p`, we instantly HALT!
                # Why? Because if we continued to the next prime (say, `q`), 
                # the composite would be `i * q`. But `p` is a factor of `i`, 
                # so `p` would ALSO be a factor of `i * q`! 
                # Therefore, `q` would NOT be the Smallest Prime Factor of `i * q`.
                # By breaking here, we guarantee every composite is touched EXACTLY ONCE 
                # (by its true SPF).
                if i % p == 0:
                    break
                    
    def factorize(self, n: int) -> List[int]:
        """
        Extracts all prime factors of `n` in O(log N) time!
        No trial division required. We just follow the SPF breadcrumbs!
        """
        if n < 2 or n > self.limit:
            return []
            
        factors = []
        while n > 1:
            # Look up the smallest prime factor instantly!
            smallest_factor = self.spf[n]
            factors.append(smallest_factor)
            
            # Divide the number
            n //= smallest_factor
            
        return factors


# ==============================================================================
# 4. THE SEGMENTED SIEVE (MEMORY OPTIMIZED)
# ==============================================================================
def segmented_sieve(L: int, R: int) -> List[int]:
    """
    Finds all primes in the range [L, R] where R can be up to 10^12, 
    but the window size (R - L) is relatively small (e.g., 10^6).
    """
    # Step 1: Generate basic primes up to sqrt(R)
    limit = int(math.isqrt(R))
    
    # We use a standard sieve to find the root primes.
    is_prime_base = [True] * (limit + 1)
    is_prime_base[0] = is_prime_base[1] = False
    base_primes = []
    
    for p in range(2, limit + 1):
        if is_prime_base[p]:
            base_primes.append(p)
            for i in range(p * p, limit + 1, p):
                is_prime_base[i] = False
                
    # Step 2: Sieve the isolated window [L, R]
    # We allocate a boolean array ONLY for the size of the window!
    window_size = R - L + 1
    is_prime_window = [True] * window_size
    
    # Edge case: If 1 is in the window, 1 is not prime.
    if L == 1:
        is_prime_window[0] = False
        
    for p in base_primes:
        # Find the absolute FIRST multiple of `p` that is >= L.
        # Math trick: ((L + p - 1) // p) * p
        start_multiple = max(p * p, ((L + p - 1) // p) * p)
        
        # Cross out all multiples inside the window!
        for i in range(start_multiple, R + 1, p):
            is_prime_window[i - L] = False
            
    # Step 3: Extract primes from the window
    primes_in_range = []
    for i in range(window_size):
        if is_prime_window[i]:
            primes_in_range.append(L + i)
            
    return primes_in_range


def demonstrate_advanced_sieves():
    section_header("Algorithm: Linear Sieve & SPF")
    
    limit = 100
    print(f"Building O(N) Euler Sieve up to {limit}...")
    sieve = LinearSieve(limit)
    
    num_to_factor = 84
    print(f"\nO(log N) Prime Factorization of {num_to_factor}:")
    factors = sieve.factorize(num_to_factor)
    print(f"Factors: {factors} (Verification: 2 * 2 * 3 * 7 = {2*2*3*7})")
    
    section_header("Algorithm: Segmented Sieve")
    
    # A massive range. If we used a standard array, it would require 
    # 10 Billion elements!
    L = 10000000000
    R = 10000000050
    
    print(f"Finding primes in isolated window [{L}, {R}]...")
    window_primes = segmented_sieve(L, R)
    
    print(f"Found {len(window_primes)} primes: {window_primes}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `if i % p == 0: break` guarantee $O(N)$?
   Answer: In the standard sieve, the number 12 is crossed out by $p=2$ and later by $p=3$. In the Linear Sieve, when $i=6$, it iterates through the primes. First, $p=2$. It marks 12 as composite ($SPF[12] = 2$). Then it hits the trigger `6 % 2 == 0` and BREAKS! It refuses to move on to $p=3$. Why? Because if it did, it would mark 18 ($6 \times 3$). But the smallest prime factor of 18 is 2, not 3! (Because $6$ has a factor of 2, so $6 \times 3$ also has a factor of 2). By halting immediately, it ensures every number is marked exactly once by its TRUE smallest prime.

2. Why is SPF factorization $O(\log N)$?
   Answer: Every time you divide $N$ by its Smallest Prime Factor, the number physically shrinks by a factor of AT LEAST 2 (since 2 is the smallest possible prime). Therefore, it can undergo a maximum of $\log_2(N)$ divisions before hitting 1. Example: $1024 / 2 / 2 / 2 \dots = 1$. This is vastly superior to trial division, which loops all the way up to $\sqrt{N}$ checking hundreds of non-factors.

3. How does the Segmented Sieve save memory?
   Answer: If $R = 10^{12}$, creating an array of size $R$ takes roughly $1$ Terabyte of RAM! The Sieve logic mathematically proves that any composite number up to $R$ MUST have a prime factor $\le \sqrt{R}$. For $10^{12}$, the square root is only $1,000,000$. The Segmented Sieve only generates primes up to $1,000,000$ (using microscopic RAM). Then, it maps those specific primes to cross out numbers strictly inside the $[L, R]$ window!
"""

if __name__ == "__main__":
    demonstrate_advanced_sieves()
    print("\n[SUCCESS] Laboratory: Advanced Sieves Completed.")
