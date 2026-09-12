"""
Modular Arithmetic

Learning Objectives:
1. Understand operations (addition, subtraction, multiplication) under a modulo.
2. Learn how to handle negative numbers in modular arithmetic.
3. Understand modular division using multiplicative inverse.

Concept Explanation:
Modular arithmetic is a system of arithmetic for integers, where numbers "wrap around" 
upon reaching a certain value (the modulus). 
Formulas:
(A + B) % M = (A % M + B % M) % M
(A * B) % M = (A % M * B % M) % M
(A - B) % M = (A % M - B % M + M) % M
(A / B) % M = (A * mod_inverse(B, M)) % M
"""

class ModArithmetic:
    def __init__(self, mod: int):
        self.mod = mod

    def add(self, a: int, b: int) -> int:
        return ((a % self.mod) + (b % self.mod)) % self.mod

    def sub(self, a: int, b: int) -> int:
        return ((a % self.mod) - (b % self.mod) + self.mod) % self.mod

    def mul(self, a: int, b: int) -> int:
        return ((a % self.mod) * (b % self.mod)) % self.mod

    def _extended_gcd(self, a: int, b: int):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def mod_inverse(self, a: int) -> int:
        g, x, y = self._extended_gcd(a, self.mod)
        if g != 1:
            raise ValueError("Inverse doesn't exist")
        return (x % self.mod + self.mod) % self.mod

    def div(self, a: int, b: int) -> int:
        return self.mul(a, self.mod_inverse(b))

# Performance Analysis:
# Add/Sub/Mul: O(1) time and space
# Div/ModInverse: O(log(mod)) time, due to Extended GCD.

# Edge Cases:
# Modulo by 0 is invalid.
# Division when divisor has no modular inverse (gcd(divisor, mod) != 1).

# Interview Challenge:
# Compute the factorial of N modulo M.
def factorial_mod(n: int, mod: int) -> int:
    ma = ModArithmetic(mod)
    res = 1
    for i in range(1, n + 1):
        res = ma.mul(res, i)
    return res

def run_tests():
    ma = ModArithmetic(10**9 + 7)
    
    assert ma.add(10**9, 10**9) == 999999993
    assert ma.sub(5, 10) == 10**9 + 2
    assert ma.mul(10**5, 10**5) == 999999937
    
    # Division test: (8 / 2) % 7
    ma7 = ModArithmetic(7)
    assert ma7.div(8, 2) == 4
    
    assert factorial_mod(5, 10**9 + 7) == 120
    print("All mod-arith tests passed!")

if __name__ == "__main__":
    run_tests()
