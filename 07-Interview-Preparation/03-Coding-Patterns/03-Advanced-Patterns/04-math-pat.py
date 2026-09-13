"""
Math & Bit Manipulation Patterns
================================

Learning Objectives:
1. Perform basic and advanced bit manipulation.
2. Understand modular arithmetic and fast exponentiation.
3. Master primes generation (Sieve of Eratosthenes).

Concept Explanation:
Math problems in interviews often rely on recognizing number properties (primes, modulo)
or optimizing memory/speed using bitwise operators. Bit manipulation can track states 
using integers instead of arrays.
"""

from typing import List
import unittest

class MathAlgorithms:
    
    @staticmethod
    def count_primes(n: int) -> int:
        """
        Sieve of Eratosthenes to count primes less than n.
        Time: O(N log log N)
        """
        if n < 2: return 0
        primes = [True] * n
        primes[0] = primes[1] = False
        
        p = 2
        while p * p < n:
            if primes[p]:
                for i in range(p * p, n, p):
                    primes[i] = False
            p += 1
            
        return sum(primes)

    @staticmethod
    def power(x: float, n: int) -> float:
        """
        Fast Exponentiation. Calculate x^n in O(log n) time.
        """
        if n == 0: return 1.0
        if n < 0:
            x = 1 / x
            n = -n
            
        res = 1.0
        current_product = x
        while n > 0:
            if n % 2 == 1:
                res *= current_product
            current_product *= current_product
            n //= 2
        return res

class BitManipulation:
    
    @staticmethod
    def single_number(nums: List[int]) -> int:
        """
        Given a non-empty array where every element appears twice except one, find it.
        Uses XOR: a ^ a = 0, a ^ 0 = a. Time O(N), Space O(1).
        """
        res = 0
        for num in nums:
            res ^= num
        return res
        
    @staticmethod
    def count_set_bits(n: int) -> int:
        """
        Brian Kernighan's Algorithm. Clears the lowest set bit.
        Time: O(set bits)
        """
        count = 0
        while n:
            n &= (n - 1)
            count += 1
        return count

# --- Performance Analysis ---
# Sieve: Space O(N), Time O(N log log N).
# Fast Exp: Space O(1), Time O(log N).
# Bit tricks: Generally O(1) space and highly efficient time.
#
# Edge Cases: Negative exponents, integer overflow (Python handles it, but good to mention), 
# zero values.

class TestMathPatterns(unittest.TestCase):
    def test_primes(self):
        self.assertEqual(MathAlgorithms.count_primes(10), 4) # 2,3,5,7
        self.assertEqual(MathAlgorithms.count_primes(0), 0)

    def test_power(self):
        self.assertAlmostEqual(MathAlgorithms.power(2.0, 10), 1024.0)
        self.assertAlmostEqual(MathAlgorithms.power(2.0, -2), 0.25)

    def test_single_number(self):
        self.assertEqual(BitManipulation.single_number([4,1,2,1,2]), 4)

    def test_set_bits(self):
        self.assertEqual(BitManipulation.count_set_bits(11), 3) # 1011 in binary

if __name__ == '__main__':
    unittest.main()
