"""
Extended Euclidean Algorithm

Learning Objectives:
1. Understand the Extended Euclidean Algorithm.
2. Find coefficients x and y such that ax + by = gcd(a, b).
3. Compute modular multiplicative inverse using this algorithm.

Concept Explanation:
The Extended Euclidean Algorithm not only finds the GCD of integers a and b,
but also finds integers x and y (Bézout coefficients) such that:
a*x + b*y = gcd(a, b)
This is particularly useful in cryptography and modular arithmetic to find modular inverses.
"""

from typing import Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Advanced implementation: O(log(min(a, b)))
    Returns (gcd, x, y) such that a*x + b*y = gcd
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    
    # Update x and y using results of recursive call
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def mod_inverse(a: int, m: int) -> int:
    """
    Finds the modular multiplicative inverse of a modulo m.
    Returns x such that (a*x) % m == 1.
    """
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist since gcd({a}, {m}) != 1")
    else:
        return x % m

# Performance Analysis:
# Extended GCD: Time O(log(min(a, b))), Space O(log(min(a, b))) for call stack
# Modular Inverse: Time O(log(m))

# Edge Cases:
# a = 0 or b = 0.
# GCD != 1 when finding modular inverse.

# Interview Challenge:
# Solve the linear congruence equation ax = b (mod m).
def solve_linear_congruence(a: int, b: int, m: int) -> int:
    """Solves ax = b (mod m). Returns one solution x."""
    g, x, y = extended_gcd(a, m)
    if b % g != 0:
        raise ValueError("No solution exists")
    x0 = (x * (b // g)) % m
    if x0 < 0:
        x0 += m
    return x0

def run_tests():
    g, x, y = extended_gcd(30, 20)
    assert g == 10
    assert 30 * x + 20 * y == 10
    
    assert mod_inverse(3, 11) == 4  # 3*4 = 12 = 1 (mod 11)
    
    try:
        mod_inverse(2, 4)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
        
    assert solve_linear_congruence(14, 30, 100) == 95  # 14*95 = 1330 = 30 (mod 100)
    
    print("All ext-euclid tests passed!")

if __name__ == "__main__":
    run_tests()
