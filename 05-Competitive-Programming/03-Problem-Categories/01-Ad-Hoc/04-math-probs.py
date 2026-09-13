"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (MATH & NUMBER THEORY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Competitive Programming platforms love Math. If a problem asks you to find 
# all the Prime Numbers between 1 and 1,000,000, and you write a double 
# `for` loop to check if every number is divisible, your code will execute 
# roughly 1 Trillion modulo operations. (Time Limit Exceeded).
#
# You must memorize ancient algorithms, like the Sieve of Eratosthenes 
# (invented in 200 BC), to do this in exactly O(N log(log N)) time!
#
# If you are asked to find the Greatest Common Divisor (GCD) of two massive 
# numbers, you cannot use a `for` loop. You must use the Euclidean Algorithm 
# (invented in 300 BC) which solves it in O(log(min(a, b))) time using recursion!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Euclidean Algorithm for GCD (and LCM).
# - Execute the Sieve of Eratosthenes to generate Prime Numbers rapidly.
# - Understand Fast Exponentiation for large powers.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EUCLIDEAN ALGORITHM (GCD & LCM)
# ==============================================================================
def calculate_gcd(a: int, b: int) -> int:
    """
    Finds the Greatest Common Divisor (GCD) using the Euclidean Algorithm.
    Time Complexity: O(log(min(a, b)))
    
    The Math: GCD(a, b) is mathematically identical to GCD(b, a % b).
    We recursively shrink the numbers using modulo until one becomes 0!
    """
    if b == 0:
        return a
    return calculate_gcd(b, a % b)
    
def calculate_lcm(a: int, b: int) -> int:
    """
    Finds the Least Common Multiple (LCM).
    The Math: a * b = GCD(a, b) * LCM(a, b)
    Therefore: LCM = (a * b) // GCD
    """
    # Use integer division (//) to prevent floating point conversion!
    return (a * b) // calculate_gcd(a, b)

def demonstrate_gcd_lcm():
    section_header("Greatest Common Divisor (Euclidean Algorithm)")
    
    a, b = 48, 18
    print(f"Number A: {a}, Number B: {b}")
    
    gcd_val = calculate_gcd(a, b)
    lcm_val = calculate_lcm(a, b)
    
    print(f"GCD: {gcd_val}")
    print(f"LCM: {lcm_val}")
    
    print("\nNote: In Python 3.9+, you can just use `math.gcd(a, b)` and `math.lcm(a, b)`!")
    print("But you must understand the underlying recursion for interview questions.")


# ==============================================================================
# 4. SIEVE OF ERATOSTHENES (PRIME NUMBERS)
# ==============================================================================
def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Finds all Prime Numbers strictly less than N.
    Time Complexity: O(N * log(log(N))), Space Complexity: O(N)
    
    The Algorithm:
    Create a boolean array. Start at 2. If 2 is prime, cross out all multiples 
    of 2 (4, 6, 8...). Move to 3. Cross out all multiples of 3. 
    """
    if n <= 2: return []
    
    # 1. Initialize a boolean array of size N
    # We assume all numbers are prime (True) initially.
    is_prime = [True] * n
    
    # 0 and 1 are mathematically not prime numbers.
    is_prime[0] = is_prime[1] = False
    
    # 2. Iterate up to the SQUARE ROOT of N.
    # Why? If N = 100, the largest prime factor we need to check is 10.
    # Any composite number > 100 must have at least one factor <= 10!
    limit = int(math.isqrt(n)) + 1
    
    for p in range(2, limit):
        # If we haven't crossed out 'p' yet, it is officially a Prime!
        if is_prime[p]:
            # Cross out all multiples of 'p' starting from p^2!
            # We start at p^2 because smaller multiples (like p*2, p*3) 
            # were already crossed out by smaller primes!
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
                
    # 3. Collect the primes
    primes = []
    for i in range(2, n):
        if is_prime[i]:
            primes.append(i)
            
    return primes

def demonstrate_sieve():
    section_header("Sieve of Eratosthenes (Prime Generation)")
    
    n = 50
    print(f"Generating all Prime Numbers strictly less than {n}...\n")
    
    primes = sieve_of_eratosthenes(n)
    
    print(f"Primes: {primes}")
    print(f"Total count: {len(primes)}")
    print("\nThis algorithm can find all primes up to 10 Million in less than 1 second!")


def run_all_labs():
    demonstrate_gcd_lcm()
    demonstrate_sieve()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the mathematical logic behind the Euclidean Algorithm: `GCD(A, B) == GCD(B, A % B)`.
   Answer: Suppose you have a $48 \times 18$ rectangle, and you want to tile it with the largest possible perfect squares. You can fit two $18 \times 18$ squares, leaving a remainder rectangle of size $18 \times 12$. The largest tile that can perfectly fill the $48 \times 18$ board is mathematically identical to the largest tile that can fill the leftover $18 \times 12$ board! This remainder is exactly `A % B`. By recursively taking the modulo (`18 % 12 = 6`, then `12 % 6 = 0`), the algorithm rapidly shrinks the numbers until the remainder is 0, revealing that 6 is the Greatest Common Divisor in $O(\log(\min(A, B)))$ time.

2. In the Sieve of Eratosthenes, why do we only need to iterate the outer loop up to the Square Root of $N$ (`isqrt(n)`)?
   Answer: If $N = 100$, we only check primes up to 10. Why? Because every composite number has at least two factors. If a composite number $C \le 100$, it is impossible for *both* of its factors to be strictly greater than 10 (since $11 \times 11 = 121$). Therefore, every non-prime number up to 100 is mathematically guaranteed to have at least one factor $\le 10$. If we cross out all multiples of 2, 3, 5, and 7, we have definitively eliminated all non-primes. Any number remaining untouched after the square root is mathematically proven to be prime!

3. In the Sieve of Eratosthenes, when crossing out the multiples of a prime $P$, why is it safe to start crossing out at $P^2$ instead of $P \times 2$?
   Answer: Optimization. Suppose we are crossing out multiples of $P = 5$. We could cross out $5 \times 2$, $5 \times 3$, and $5 \times 4$. But $5 \times 2$ (10) was already crossed out when we processed the multiples of 2! $5 \times 3$ (15) was already crossed out when we processed 3! $5 \times 4$ (20) was already crossed out by 2! Every multiple of $P$ smaller than $P \times P$ has a smaller prime factor that we already processed in earlier loops. Starting exactly at $P^2$ prevents redundant memory writes and drastically speeds up the algorithm.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Math & Number Theory Completed.")
