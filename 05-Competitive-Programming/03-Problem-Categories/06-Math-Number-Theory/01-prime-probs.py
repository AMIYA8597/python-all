"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (PRIME FACTORIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are asked to find all the Prime Factors of a massive number $N = 10^{12}$.
# E.g., the prime factors of 60 are 2, 2, 3, 5.
#
# If you run a `for` loop from 2 up to $10^{12}$ checking `N % i == 0`, your 
# code will execute 1 Trillion operations and crash (Time Limit Exceeded).
# You must mathematically optimize this to $O(\sqrt{N})$.
#
# Second Scenario: The judge gives you an array of 100,000 numbers and asks 
# for the prime factorization of EVERY single number.
# Even the $O(\sqrt{N})$ algorithm will crash if you run it 100,000 times!
# You must invent the SPF (Smallest Prime Factor) Array using a modified 
# Sieve of Eratosthenes to answer prime factorization queries in exactly 
# $O(\log N)$ time per query!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Trial Division for $O(\sqrt{N})$ Prime Factorization.
# - Master the Smallest Prime Factor (SPF) Sieve for $O(\log N)$ Factorization.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRIAL DIVISION (O(sqrt N) Prime Factorization)
# ==============================================================================
def prime_factors_sqrt(n: int) -> list[int]:
    """
    Finds all prime factors of N in O(sqrt(N)) time.
    Used for a SINGLE massive query (e.g., N = 10^12).
    """
    factors = []
    
    # 1. Extract all the 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
        
    # 2. Extract odd primes up to the Square Root of N!
    # A composite number can mathematically have at most ONE prime factor 
    # strictly greater than its square root.
    limit = int(math.isqrt(n)) + 1
    
    # Start at 3, increment by 2 (skip all even numbers)
    for i in range(3, limit, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
            
    # 3. The Remainder Exception
    # If after dividing everything out up to the Square Root, N is still > 2,
    # then N itself must be a Prime Number (the ONE allowed prime > sqrt(N)).
    if n > 2:
        factors.append(n)
        
    return factors

def demonstrate_trial_division():
    section_header("Trial Division (O(sqrt N))")
    
    # 315 = 3 * 3 * 5 * 7
    number = 315
    print(f"Finding prime factors of: {number}")
    
    factors = prime_factors_sqrt(number)
    print(f"Factors: {factors}")
    
    massive_number = 10**12 + 7 # Some large number
    print(f"\nFinding prime factors of massive number: {massive_number}")
    print(f"Factors: {prime_factors_sqrt(massive_number)}")
    print("Notice how fast it executes! The loop stopped at 1 Million instead of 1 Trillion.")


# ==============================================================================
# 4. SMALLEST PRIME FACTOR (SPF) SIEVE (O(log N) Queries)
# ==============================================================================
class SPFSieve:
    """
    Precomputes the Smallest Prime Factor (SPF) for all numbers up to MAX_N.
    Build Time: O(N log(log N))
    Query Time: O(log N)
    Used when a problem asks you to factorize 100,000 different numbers rapidly!
    """
    def __init__(self, max_n: int):
        self.spf = [0] * (max_n + 1)
        
        # 1. Initialize SPF of every number to itself.
        for i in range(2, max_n + 1):
            self.spf[i] = i
            
        # 2. Even numbers all share 2 as their smallest prime factor!
        for i in range(4, max_n + 1, 2):
            self.spf[i] = 2
            
        # 3. Modified Sieve of Eratosthenes
        limit = int(math.isqrt(max_n)) + 1
        for i in range(3, limit, 2):
            # If the SPF is still itself, it is mathematically a Prime!
            if self.spf[i] == i:
                # Mark all multiples of this prime!
                for j in range(i * i, max_n + 1, i):
                    # Only mark it if it hasn't been marked by a smaller prime yet!
                    if self.spf[j] == j:
                        self.spf[j] = i

    def get_factors(self, n: int) -> list[int]:
        """
        Recursively divides N by its pre-calculated SPF until it reaches 1.
        Takes exactly O(log N) time!
        """
        factors = []
        while n != 1:
            prime = self.spf[n]
            factors.append(prime)
            n //= prime
        return factors

def demonstrate_spf():
    section_header("Smallest Prime Factor (SPF) Sieve")
    
    # Suppose the maximum number in the array is 100,000.
    sieve = SPFSieve(100000)
    print("SPF Sieve built in O(N log log N) time.")
    
    queries = [120, 600, 99991]
    print(f"\nProcessing Queries: {queries}")
    
    for q in queries:
        factors = sieve.get_factors(q)
        print(f"Factors of {q}: {factors}")
        
    print("\nBecause we precalculated the SPF, each query hopped down to 1 in O(log N) time!")


def run_all_labs():
    demonstrate_trial_division()
    demonstrate_spf()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Trial Division for Prime Factorization, why is it safe to stop the `for` loop exactly at the Square Root of N?
   Answer: It is a mathematical impossibility for a composite number to have *two* prime factors that are both strictly greater than its Square Root (e.g., for $N=100$, you cannot have two factors $>10$, because $11 \times 11 = 121$). Therefore, a number can have at most ONE prime factor larger than $\sqrt{N}$. If we systematically divide out all the smaller prime factors up to the Square Root, the number that is left over in the `N` variable at the very end of the loop is mathematically guaranteed to be either `1` (all factors extracted), or the single massive Prime Factor that was $> \sqrt{N}$!

2. How does the SPF Sieve drop Prime Factorization query times from $O(\sqrt{N})$ to exactly $O(\log N)$?
   Answer: The SPF Sieve is an extension of the Sieve of Eratosthenes. Instead of storing `True/False` for primality, it stores the exact numerical value of the Smallest Prime Factor (e.g., `spf[15] = 3`). When querying the factors for 15, the array instantly tells us in $O(1)$ time that `3` is a factor. We divide `15 // 3 = 5`. The array then tells us in $O(1)$ time that `spf[5] = 5`. We divide `5 // 5 = 1`. The loop terminates. Because the smallest prime factor is $\ge 2$, dividing a number by $\ge 2$ mathematically cuts the number in half at every step. Dropping a number down to 1 by halving it strictly requires exactly $O(\log N)$ steps!

3. In the SPF Sieve builder, why do we use `if self.spf[j] == j:` before overwriting the SPF of a multiple?
   Answer: To preserve the *Smallest* Prime Factor. Suppose we are crossing out multiples of 3. We reach $j = 15$. The SPF of 15 is 15. We overwrite it to 3. Later in the loop, we are crossing out multiples of 5. We reach $j = 15$. If we blindly overwrote it, the SPF of 15 would become 5! This destroys the algorithm. By checking `if spf[15] == 15`, we see that it has already been claimed by a smaller prime (3), so we skip it.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Prime Factorization Completed.")
