"""
Chinese Remainder Theorem (CRT)

Learning Objectives:
1. Understand the Chinese Remainder Theorem problem statement.
2. Implement CRT using the Extended Euclidean Algorithm.
3. Solve a system of congruences.

Concept Explanation:
The Chinese Remainder Theorem states that if one knows the remainders of the 
division of an integer n by several integers, then one can determine uniquely the 
remainder of the division of n by the product of these integers, provided the divisors are pairwise coprime.
System:
x = a1 (mod m1)
x = a2 (mod m2)
...
x = ak (mod mk)
"""

from typing import List

def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a: int, m: int) -> int:
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse doesn't exist for {a} mod {m}")
    return x % m

def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> int:
    """
    Advanced implementation of CRT.
    Assumes all moduli are pairwise coprime.
    """
    if len(remainders) != len(moduli):
        raise ValueError("Lengths of remainders and moduli must be equal")
        
    total_product = 1
    for m in moduli:
        total_product *= m
        
    result = 0
    for a_i, m_i in zip(remainders, moduli):
        p = total_product // m_i
        result += a_i * mod_inverse(p, m_i) * p
        
    return result % total_product

# Performance Analysis:
# CRT: O(k * log(M)) where k is the number of congruences and M is the product of all moduli.
# Space: O(k)

# Edge Cases:
# Moduli are not pairwise coprime (requires a generalized CRT approach).
# Empty input arrays.

# Interview Challenge:
# A number leaves remainder 2 when divided by 3, 3 when divided by 5, and 2 when divided by 7.
# What is the smallest positive number?
def interview_challenge():
    rem = [2, 3, 2]
    mod = [3, 5, 7]
    return chinese_remainder_theorem(rem, mod)

def run_tests():
    # x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7)
    # Expected: 23
    assert chinese_remainder_theorem([2, 3, 2], [3, 5, 7]) == 23
    
    assert interview_challenge() == 23
    print("All CRT tests passed!")

if __name__ == "__main__":
    run_tests()
