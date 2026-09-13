"""
# ==============================================================================
# LABORATORY: CHINESE REMAINDER THEOREM (CRT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the 3rd century AD, the Chinese mathematician Sun Tzu proposed a puzzle 
# in his book "Sun Tzu Suan Ching":
# 
# "There are certain things whose number is unknown. 
#  If we count them by 3, we have 2 left over. 
#  If we count them by 5, we have 3 left over. 
#  If we count them by 7, we have 2 left over. 
#  How many things are there?"
#
# Mathematically, this is a system of linear congruences:
# X % 3 == 2
# X % 5 == 3
# X % 7 == 2
#
# The Chinese Remainder Theorem mathematically guarantees that if the divisors 
# (3, 5, and 7) are "Pairwise Coprime" (meaning none of them share any common 
# prime factors, so GCD(A, B) == 1 for all pairs), then there is EXACTLY ONE 
# unique solution for X between 0 and the product of all divisors!
# Product = 3 * 5 * 7 = 105.
# The unique answer is X = 23. (23%3=2, 23%5=3, 23%7=2).
#
# How do we calculate this without looping 105 times?
# We use the Modular Multiplicative Inverse (which we learned via the Extended 
# Euclidean Algorithm) to perfectly scale the remainders into the final answer!
#
# Why is this used today? 
# RSA Cryptography decryption involves massive 1024-bit modulo operations. 
# Using the CRT, computers can split the massive modulo into two smaller 512-bit 
# modulos, do the math 4x faster, and then perfectly recombine the answer!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Pairwise Coprime mathematical constraint.
# - Re-use the Extended Euclidean Algorithm for Modular Inverses.
# - Implement the $O(K \log M)$ direct CRT formula.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helpers: The Mathematics Toolbox from previous labs ---
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a: int, m: int) -> int:
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Inverse does not exist. {a} and {m} are not coprime.")
    return (x % m + m) % m
# -----------------------------------------------------------


# ==============================================================================
# 3. CHINESE REMAINDER THEOREM ENGINE (COPRIME MODULI)
# ==============================================================================
def chinese_remainder_theorem(remainders: List[int], modulos: List[int]) -> int:
    """
    Solves the system of equations: X % modulos[i] == remainders[i]
    Assumes all numbers in `modulos` are pairwise coprime.
    Time Complexity: O(K log M) where K is number of equations, M is max modulo.
    """
    if len(remainders) != len(modulos):
        raise ValueError("Arrays must be the same length!")
        
    k = len(remainders)
    
    # 1. CALCULATE THE TOTAL PRODUCT (The mathematical universe bounds)
    # This is the maximum possible range. The unique answer is guaranteed 
    # to be strictly between 0 and (total_product - 1).
    total_product = 1
    for mod in modulos:
        total_product *= mod
        
    result_x = 0
    
    # 2. THE CRT FORMULA LOOP
    for i in range(k):
        # Extract the specific remainder and modulo for this equation
        rem = remainders[i]
        mod = modulos[i]
        
        # M_i is the product of ALL OTHER modulos except this one!
        # Math trick: total_product // mod
        M_i = total_product // mod
        
        # Calculate the Modular Inverse of M_i with respect to our specific modulo!
        # We need an integer `inv_i` such that (M_i * inv_i) % mod == 1
        inv_i = mod_inverse(M_i, mod)
        
        # The Magic Formula: 
        # Add (Remainder * M_i * Inverse) to the running total.
        # Why does this work? Because when you evaluate this specific term modulo 
        # our specific `mod`, the M_i * inv_i cancels perfectly to 1! Leaving 
        # just the Remainder! 
        # When you evaluate this term modulo ANY OTHER modulo in the array, 
        # M_i contains that other modulo as a factor, so it perfectly evaluates to 0!
        # It is mathematically flawless isolation.
        term = rem * M_i * inv_i
        result_x += term
        
    # The final answer must be wrapped around the total product boundary
    return result_x % total_product


# ==============================================================================
# 4. ADVANCED CRT: MERGING (NON-COPRIME MODULI)
# ==============================================================================
def crt_merge_non_coprime(remainders: List[int], modulos: List[int]) -> int:
    """
    What if the modulos are NOT coprime? (e.g., Mod 4 and Mod 6).
    The direct formula fails because Modular Inverse throws an error!
    Instead, we iteratively MERGE the equations two at a time using 
    the Extended Euclidean Algorithm.
    """
    k = len(remainders)
    if k == 0: return 0
    
    ans_rem = remainders[0]
    ans_mod = modulos[0]
    
    for i in range(1, k):
        rem = remainders[i]
        mod = modulos[i]
        
        # We want to merge (ans_rem, ans_mod) with (rem, mod)
        # Equation: ans_rem + ans_mod * x == rem + mod * y
        # Rearranging: ans_mod * x - mod * y == rem - ans_rem
        # This is a Linear Diophantine Equation! A*x + B*y = C
        A = ans_mod
        B = mod
        C = rem - ans_rem
        
        gcd, x_g, y_g = extended_gcd(A, B)
        
        # Solvability check from Diophantine rules
        if C % gcd != 0:
            raise ValueError("Mathematically contradictory equations! No solution.")
            
        # Scale X to hit target C
        multiplier = C // gcd
        x = x_g * multiplier
        
        # Calculate the new combined modulo! (Which is just the LCM of both)
        lcm_mod = (ans_mod * mod) // gcd
        
        # Calculate the new combined remainder!
        # ans_rem + ans_mod * x
        ans_rem = (ans_rem + ans_mod * x) % lcm_mod
        ans_rem = (ans_rem + lcm_mod) % lcm_mod # Force positive
        
        ans_mod = lcm_mod
        
    return ans_rem


def demonstrate_crt():
    section_header("Algorithm: Sun Tzu's Classic Puzzle (Coprime Moduli)")
    
    # "Count by 3 -> 2 left. Count by 5 -> 3 left. Count by 7 -> 2 left."
    remainders = [2, 3, 2]
    modulos = [3, 5, 7]
    
    print(f"Remainders : {remainders}")
    print(f"Modulos    : {modulos}")
    
    ans = chinese_remainder_theorem(remainders, modulos)
    
    print(f"\nThe Unique Solution (X) is: {ans}")
    print("Verification:")
    print(f" {ans} % 3 = {ans%3} (Expected: 2)")
    print(f" {ans} % 5 = {ans%5} (Expected: 3)")
    print(f" {ans} % 7 = {ans%7} (Expected: 2)")
    
    section_header("Algorithm: Merging Equations (Non-Coprime Moduli)")
    
    # Equation 1: X % 4 == 2
    # Equation 2: X % 6 == 4
    # Note: 4 and 6 are NOT coprime. GCD(4, 6) = 2.
    rem2 = [2, 4]
    mod2 = [4, 6]
    
    ans2 = crt_merge_non_coprime(rem2, mod2)
    print(f"Equations: X % 4 == 2, X % 6 == 4")
    print(f"The Unique Solution (X) is: {ans2}")
    print("Verification:")
    print(f" {ans2} % 4 = {ans2%4} (Expected: 2)")
    print(f" {ans2} % 6 = {ans2%6} (Expected: 4)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the direct CRT formula require the modulos to be Pairwise Coprime?
   Answer: The absolute core of the formula relies on calculating `inv_i = mod_inverse(M_i, mod)`. As proved in the Extended Euclidean lab, a modular multiplicative inverse MATHEMATICALLY ONLY EXISTS if the two numbers are Coprime ($GCD(A, B) == 1$). If the modulos share prime factors, $M_i$ and the current $mod$ will also share prime factors! The GCD will be $> 1$, the inverse will fail to exist, and the math crashes.

2. Why does the isolation term $R \times M_i \times \text{inv}$ evaluate perfectly?
   Answer: Imagine modulo array $[3, 5, 7]$. When evaluating the first term (mod 3), $M_i$ is $5 \times 7 = 35$. The inverse makes $(35 \times \text{inv}) \equiv 1 \pmod 3$. So the term becomes $(R \times 1) = R \pmod 3$. Perfect! 
   But what happens when this exact same term is evaluated by the OTHER modulos, say modulo 5? 
   The term is $(R \times 35 \times \text{inv})$. But wait, 35 is a perfect multiple of 5! So $35 \equiv 0 \pmod 5$. 
   The ENTIRE massive term instantly collapses to $(R \times 0 \times \text{inv}) = 0 \pmod 5$! 
   The term perfectly triggers for its own modulo, and mathematically vanishes for all others.

3. How does the Iterative Merge handle Non-Coprime modulos?
   Answer: It completely abandons the Modular Inverse! Instead, it looks at two equations: $X = R_1 + M_1 \times Y_1$ and $X = R_2 + M_2 \times Y_2$. It sets them equal to each other, creating a classic Linear Diophantine Equation: $M_1 \times Y_1 - M_2 \times Y_2 = R_2 - R_1$. It uses the Extended GCD to find the integer steps $Y_1$, scales them, and physically calculates the intersection point! It then collapses the two modulos into a single massive modulo using their Least Common Multiple (LCM), perfectly bypassing the coprime restriction.
"""

if __name__ == "__main__":
    demonstrate_crt()
    print("\n[SUCCESS] Laboratory: Chinese Remainder Theorem Completed.")
