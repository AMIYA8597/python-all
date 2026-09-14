"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - MATHEMATICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Count all prime numbers strictly less than 10 Million."
#
# A junior engineer writes a `is_prime()` function using a `for` loop up to `sqrt(N)`, 
# and then loops it 10 Million times. Time Complexity: O(N * sqrt(N)). 
# For N = 10,000,000, it performs over 30 Billion operations and times out.
#
# A senior engineer uses the Sieve of Eratosthenes. They instantiate a boolean 
# array of size 10 Million. They find the first prime (2), and mathematically 
# annihilate every multiple of 2 (4, 6, 8...). Then they step to the next uncrossed 
# number (3), and annihilate every multiple of 3 (9, 12, 15...). By bulk-eliminating 
# non-primes instantly, the algorithm completes in O(N log(log N)) time, reducing 
# 30 Billion operations down to just 25 Million.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Sieve of Eratosthenes (Prime Generation).
# - Master Fast Exponentiation (O(log N) power calculation).
# - Understand the limits of modular arithmetic and Integer boundaries.
#
# ==============================================================================
"""

import time
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE SIEVE OF ERATOSTHENES (PRIME GENERATION)
# ==============================================================================
def count_primes_sieve(n: int) -> int:
    """
    Time: O(N log(log N)) | Space: O(N)
    Returns the number of prime numbers strictly less than n.
    """
    if n <= 2: return 0
    
    # Initialize a Boolean array assuming EVERYTHING is prime.
    is_prime = [True] * n
    # 0 and 1 are mathematically NOT prime.
    is_prime[0] = is_prime[1] = False
    
    # We only need to process up to the Square Root of N!
    # Because if a number has a factor larger than sqrt(N), its corresponding 
    # factor MUST be smaller than sqrt(N), which we would have already crossed out!
    limit = int(n ** 0.5) + 1
    
    for i in range(2, limit):
        if is_prime[i]:
            # It's prime! Now we ANNIHILATE every multiple of it!
            # We start crossing out at `i * i`. Why? 
            # Because all smaller multiples (e.g., `i * 2`) were ALREADY crossed 
            # out when we processed the number 2!
            for multiple in range(i * i, n, i):
                is_prime[multiple] = False
                
    # Count how many True flags remain!
    return sum(is_prime)

def demonstrate_sieve():
    section_header("Sieve of Eratosthenes (Prime Numbers)")
    
    n = 10_000_000
    print(f"Task: Count all primes strictly less than {n:,}")
    print("Executing Sieve...")
    
    start = time.perf_counter()
    count = count_primes_sieve(n)
    end = time.perf_counter()
    
    print(f"\nResult: Found {count:,} primes.")
    print(f"Time: {(end - start):.4f} seconds (Blazing fast!)")


# ==============================================================================
# 4. FAST EXPONENTIATION (MODULAR ARITHMETIC)
# ==============================================================================
def fast_power(x: float, n: int) -> float:
    """
    Time: O(log N) | Space: O(1)
    Calculates x^n.
    
    If n is 1 Billion, a `for` loop takes 1 Billion multiplications.
    Fast Exponentiation uses the binary representation of N to compute it in 
    just 30 multiplications! 
    Concept: 2^10 = (2^5) * (2^5). 
    """
    # Handle negative powers!
    if n < 0:
        x = 1 / x
        n = -n
        
    result = 1.0
    current_product = x
    
    print(f"  Calculating {x}^{n}")
    
    while n > 0:
        # If the current bit is 1 (n is odd)
        if n % 2 == 1:
            result *= current_product
            print(f"    -> [ODD BIT] Multiplying result. Result is now {result}")
            
        # Mathematically square the product for the next bit!
        current_product *= current_product
        # Shift bits to the right (Integer division by 2)
        n //= 2
        print(f"    -> Squaring base. Base is now {current_product}. Remaining power: {n}")
        
    return result

def demonstrate_fast_power():
    section_header("Fast Exponentiation O(log N)")
    
    base = 2.0
    power = 10
    
    ans = fast_power(base, power)
    print(f"\nResult: {base}^{power} = {ans}")


def run_all_labs():
    demonstrate_sieve()
    demonstrate_fast_power()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Sieve of Eratosthenes, why does the outer loop stop at exactly `sqrt(N)`? Why not loop all the way to `N`?"
   Senior Answer: "The Sieve algorithm crosses out all composite (non-prime) numbers. Every composite number $C$ is mathematically constructed by multiplying two factors: $C = A \\times B$. If both $A$ and $B$ were strictly greater than $\\sqrt{C}$, their product would be greater than $C$, which is a paradox. Therefore, it is mathematically guaranteed that every composite number MUST have at least one prime factor that is less than or equal to its square root. By checking up to $\\sqrt{N}$, we have definitively eliminated every single possible composite number up to $N$. Looping beyond $\\sqrt{N}$ is algorithmically redundant."

2. Interviewer: "In the Sieve of Eratosthenes, when crossing out the multiples of a prime $P$ (e.g., $P=5$), why do we start the inner loop exactly at $P^2$ (e.g., $25$) instead of $P \\times 2$ (e.g., $10$)?"
   Senior Answer: "If we are processing the prime number $5$, the multiples below $5^2$ are $5 \\times 2$, $5 \\times 3$, and $5 \\times 4$. The number 2 is prime, and when the outer loop processed $2$, it *already* crossed out all of its multiples, including $10$ and $20$. The number 3 is prime, and it *already* crossed out $15$. Therefore, every multiple of $P$ that is less than $P^2$ has mathematically already been eliminated by a smaller prime. Starting the inner loop at $P^2$ physically bypasses thousands of redundant Hash Table or Array writes, drastically reducing the Constant Factor of the algorithm."

3. Interviewer: "Why does the Fast Exponentiation algorithm achieve $O(\\log N)$ time, and how does it relate to the Binary representation of the exponent?"
   Senior Answer: "If we calculate $3^{13}$, the naive approach loops 13 times. However, the number 13 in Binary is `1101`. This mathematically translates to $13 = 8 + 4 + 1$. Therefore, $3^{13} = 3^8 \\times 3^4 \\times 3^1$. Instead of multiplying 13 times, we can simply square the base in a loop ($3^1 \\to 3^2 \\to 3^4 \\to 3^8$). At each step, if the corresponding Binary bit of the exponent is `1` (tested via `n % 2 == 1`), we multiply our global result by that squared chunk. Because a number $N$ is represented by exactly $\\log_2(N)$ bits, the `while` loop runs exactly $\\log_2(N)$ times. It calculates $X^1,000,000,000$ in exactly 30 operations."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Mathematics) Completed.")
