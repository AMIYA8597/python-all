"""
# ==============================================================================
# LABORATORY: INCLUSION-EXCLUSION PRINCIPLE (PIE) & EULER'S TOTIENT
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Problem: "How many numbers from 1 to 1 Billion are perfectly divisible by 
# 2, 3, or 5?"
#
# A naive `for` loop takes O(N) time (1 Billion operations).
# But there is a mathematical shortcut using Set Theory:
# 1. Count multiples of 2: 1B // 2 = 500M
# 2. Count multiples of 3: 1B // 3 = 333M
# 3. Count multiples of 5: 1B // 5 = 200M
# Total = 1.033 Billion. Wait, that's impossible! There are only 1 Billion numbers!
#
# The Problem: Overlapping Sets. 
# The number 6 was counted TWICE (once by 2, once by 3).
# The number 30 was counted THREE TIMES.
#
# The Principle of Inclusion-Exclusion (PIE) fixes this:
# + INCLUDE all single sets (2, 3, 5).
# - EXCLUDE all pairwise intersections (6, 10, 15).
# + INCLUDE all triple intersections (30).
#
# Math: (500M + 333M + 200M) - (166M + 100M + 66M) + (33M) = 734 Million!
# We solved a 1 Billion operation problem in exactly 7 math steps! O(2^K) time!
#
# Application: Euler's Totient Function $\phi(N)$.
# How many numbers up to N are coprime to N? (Share no common prime factors).
# PIE mathematically simplifies this into a single formula:
# $\phi(N) = N \times (1 - 1/p_1) \times (1 - 1/p_2) \dots$
# This function is the absolute foundation of the RSA Cryptography key generation!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master combinatorial set intersections.
# - Implement PIE systematically using Bitmasking.
# - Implement Euler's Totient Function in O(sqrt N).
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Least Common Multiple ---
def lcm(a: int, b: int) -> int:
    return (a * b) // math.gcd(a, b)
# -----------------------------------


# ==============================================================================
# 3. INCLUSION-EXCLUSION ENGINE (BITMASKING)
# ==============================================================================
def count_divisibles_pie(n: int, divisors: List[int]) -> int:
    """
    Counts how many numbers from 1 to N are divisible by AT LEAST ONE of the 
    provided divisors.
    Time Complexity: O(2^K * K) where K is the number of divisors.
    """
    k = len(divisors)
    total_valid = 0
    
    # We use Bitmasking to generate all possible combinatorial intersections!
    # If K = 3, there are 2^3 = 8 combinations.
    # 001 = Set A
    # 011 = Intersection of Set A and Set B
    # 111 = Intersection of Sets A, B, and C
    
    # We loop from 1 to (2^K - 1)
    for mask in range(1, 1 << k):
        
        # 1. Calculate the mathematical intersection of the chosen sets
        current_lcm = 1
        set_bits_count = 0
        
        for i in range(k):
            # Check if the i-th bit is active in our mask
            if (mask & (1 << i)) != 0:
                set_bits_count += 1
                current_lcm = lcm(current_lcm, divisors[i])
                
                # Optimization: If the LCM exceeds N, it will contribute 0 anyway.
                if current_lcm > n:
                    break
                    
        # 2. Apply PIE Logic!
        # How many numbers up to N are divisible by this intersection?
        count_for_intersection = n // current_lcm
        
        # If the number of intersecting sets is ODD (1, 3, 5...), we ADD it! (Inclusion)
        if set_bits_count % 2 == 1:
            total_valid += count_for_intersection
        # If the number of intersecting sets is EVEN (2, 4, 6...), we SUBTRACT it! (Exclusion)
        else:
            total_valid -= count_for_intersection
            
    return total_valid


# ==============================================================================
# 4. EULER'S TOTIENT FUNCTION (O(SQRT N))
# ==============================================================================
def eulers_totient(n: int) -> int:
    """
    Calculates $\phi(N)$: The number of integers from 1 to N that are coprime to N.
    (i.e., GCD(x, N) == 1).
    Time Complexity: O(sqrt(N))
    """
    if n <= 0: return 0
    
    result = n
    
    # We find all prime factors of N using standard Trial Division.
    # The PIE mathematical simplification states:
    # result = result * (1 - 1/P) for every unique prime factor P.
    
    i = 2
    while i * i <= n:
        # If i is a prime factor of n
        if n % i == 0:
            
            # Divide out all occurrences of `i` to guarantee we only process 
            # UNIQUE prime factors!
            while n % i == 0:
                n //= i
                
            # Apply the PIE Formula for this prime!
            # result = result * (1 - 1/i)
            # To avoid floating point inaccuracies, we rewrite it algebraically:
            # result = result - (result // i)
            result -= result // i
            
        i += 1
        
    # If N was originally a prime number, or if there is one large prime factor 
    # left over after the sqrt loop, we must apply the formula to it as well!
    if n > 1:
        result -= result // n
        
    return result


def demonstrate_pie():
    section_header("Algorithm: Principle of Inclusion-Exclusion (PIE)")
    
    n_massive = 1000000000 # 1 Billion
    divisors = [2, 3, 5]
    
    print(f"How many numbers up to {n_massive:,} are divisible by 2, 3, or 5?")
    print("Executing O(2^K) PIE via Bitmasking...")
    
    ans = count_divisibles_pie(n_massive, divisors)
    print(f"Result: {ans:,} numbers!")
    
    section_header("Algorithm: Euler's Totient Function (Phi)")
    
    num = 12
    print(f"Calculating phi({num})...")
    # Coprimes of 12 are: 1, 5, 7, 11 (Because 2,3,4,6,8,9,10 share factors with 12)
    phi = eulers_totient(num)
    print(f"Result: {phi} (Matches visual list: 1, 5, 7, 11)")
    
    # Prime number test!
    prime = 17
    # For any prime number P, ALL numbers before it are coprime!
    # Therefore, phi(P) mathematically MUST equal P - 1.
    print(f"\nCalculating phi({prime}) [A Prime Number]")
    print(f"Result: {eulers_totient(prime)} (Expected: {prime - 1})")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Bitmasking perfectly model Combinatorial Intersections?
   Answer: A set of $K$ elements has exactly $2^K$ possible subsets. A binary number with $K$ bits can represent every single integer from $0$ to $2^K - 1$. There is a perfect 1-to-1 mathematical mapping! 
   If Bit 0 is '1', Set A is included. If Bit 1 is '0', Set B is excluded. 
   By looping from $1$ to $(1 \ll K)$, we mechanically visit every single possible combinatorial intersection without writing complex recursive backtracking code.

2. Why do we alternate Addition and Subtraction in PIE?
   Answer: It's a geometric Venn Diagram balancing act. 
   - We add all the individual circles (Sets). 
   - Now the overlapping lens between two circles has been counted twice! So we subtract the pairwise intersections. 
   - But wait! The center triangle where ALL THREE circles overlap was added 3 times (by the individuals), and subtracted 3 times (by the pairs). Its current weight is 0! 
   - So we must ADD the triple intersection back in to restore its weight to 1! 
   This $+ - + - + -$ ripple effect continues perfectly for any number of sets, ensuring every region in the Venn Diagram has an exact weight of 1.

3. How does PIE simplify into the $N \times (1 - 1/P)$ formula for Euler's Totient?
   Answer: Suppose we want numbers coprime to $N = 30$. 
   The prime factors of 30 are 2, 3, and 5. 
   We want the numbers that are NOT divisible by 2, NOT by 3, and NOT by 5. 
   The probability of a number NOT being divisible by 2 is $(1 - 1/2)$. 
   The probability of NOT being divisible by 3 is $(1 - 1/3)$. 
   Because prime factors are perfectly independent, we can just multiply the probabilities! 
   Total coprime count = $30 \times (1 - 1/2) \times (1 - 1/3) \times (1 - 1/5) = 8$. 
   This probabilistic multiplication is a direct algebraic factorization of the PIE addition/subtraction series!
"""

if __name__ == "__main__":
    demonstrate_pie()
    print("\n[SUCCESS] Laboratory: Inclusion-Exclusion & Totient Completed.")
