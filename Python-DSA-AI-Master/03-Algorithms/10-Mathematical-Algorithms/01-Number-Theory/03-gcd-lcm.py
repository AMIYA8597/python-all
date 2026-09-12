"""
## A. Concept Name
Greatest Common Divisor (GCD) and Least Common Multiple (LCM)

## B. Overview
GCD of two numbers is the largest positive integer that divides both numbers without a remainder. LCM is the smallest positive integer that is divisible by both numbers. 

## C. Learning Objectives
1. Understand the mathematical definitions of GCD and LCM.
2. Implement basic algorithms for GCD/LCM.
3. Learn and implement the Euclidean algorithm for GCD.
4. Understand the relationship between GCD and LCM.

## D. Real-World Applications
Used in cryptography (like RSA), resource allocation, tiling problems, and scheduling tasks with periodic cycles.

## E. Core Mechanics
The Euclidean algorithm efficiently computes GCD by repeatedly applying gcd(a, b) = gcd(b, a % b) until b becomes 0. LCM is derived from GCD using lcm(a, b) = abs(a * b) // gcd(a, b).

## F. Step-by-Step Walkthrough
1. For GCD(48, 18), applying Euclidean:
2. a=48, b=18 -> a=18, b=48%18=12
3. a=18, b=12 -> a=12, b=18%12=6
4. a=12, b=6 -> a=6, b=12%6=0. GCD is 6.

## G. Code Structure
- `gcd_basic`: Naive brute-force approach.
- `gcd_intermediate`: Optimized Euclidean approach.
- `lcm`: Computes LCM leveraging `gcd_intermediate`.
- `gcd_array`: Extends GCD to an array of numbers using `reduce`.

## H. Complexity Analysis
- Basic GCD: O(min(a, b)) time, O(1) space. Slow for large numbers.
- Euclidean GCD: O(log(min(a, b))) time, O(1) space. Extremely fast.
- LCM: O(log(min(a, b))) time due to GCD call.

## I. Edge Cases
- One or both numbers are 0.
- Negative numbers (handled using absolute value).

## J. Common Pitfalls
Forgetting to take the absolute value when computing the LCM or GCD of negative integers, leading to negative results which violate the definition.

## K. Interview Patterns
Questions asking to reduce fractions, distribute items evenly, or find synchronized repeating events often boil down to GCD or LCM.

## L. Optimization Techniques
Using bitwise operations (Binary GCD or Stein's algorithm) can offer slight optimizations at the hardware level, though Euclidean is generally optimal enough.

## M. Related Concepts
Modular Arithmetic, Prime Factorization, Extended Euclidean Algorithm.

## N. Memory Management
Space complexity is O(1) as no auxiliary data structures are maintained beyond a few state variables.

## O. Scaling Considerations
When dealing with BigInts in Python, the time complexity O(log(min(a, b))) ensures it scales comfortably even to thousands of digits.

## P. Testing Strategies
Verify with small primes, identical numbers, one zero, two zeros, and large prime products.

## Q. Debugging Tips
Trace the variables `a` and `b` at each step of the while loop to visualize the Euclidean remainder reduction.

## R. Alternative Approaches
Prime factorization can be used to find GCD and LCM, but factorization is computationally harder than the Euclidean algorithm.

## S. Industry Standards
Standard libraries like Python's `math.gcd` use highly optimized versions of the Euclidean or Binary GCD algorithms under the hood.

## T. Code Review Checklist
Ensure zeros are handled gracefully. Ensure negative numbers return positive GCD/LCM. Check for integer overflow in other languages (Python handles arbitrary-precision ints).

## U. Security Implications
GCD is foundational in generating RSA public/private key pairs. Constant-time implementations may be required to prevent timing attacks in cryptography.

## V. Historical Context
The Euclidean algorithm is one of the oldest algorithms in common use, described by Euclid in his Elements (c. 300 BC).

## W. Quick Reference
gcd(a,b) * lcm(a,b) = |a * b|

## X. Project Connection
These algorithms serve as foundational utility functions for building a full-fledged cryptographic module or a rational number (fraction) class.
"""

def gcd_basic(a: int, b: int) -> int:
    """Basic implementation: O(min(a, b))"""
    if a == 0 and b == 0:
        return 0
    a, b = abs(a), abs(b)
    if a == 0: return b
    if b == 0: return a
    
    res = 1
    for i in range(1, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            res = i
    return res

def gcd_intermediate(a: int, b: int) -> int:
    """Intermediate implementation: Euclidean Algorithm O(log(min(a, b)))"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """LCM using GCD: O(log(min(a, b)))"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd_intermediate(a, b)

# Performance Analysis:
# Basic GCD: O(min(a, b)) time, O(1) space. Slow for large numbers.
# Euclidean GCD: O(log(min(a, b))) time, O(1) space. Extremely fast.

# Edge Cases:
# One or both numbers are 0.
# Negative numbers (handled using absolute value).

# Interview Challenge:
# Find the GCD of an array of numbers.
from typing import List
from functools import reduce

def gcd_array(arr: List[int]) -> int:
    if not arr:
        return 0
    return reduce(gcd_intermediate, arr)

def run_tests():
    assert gcd_basic(48, 18) == 6
    assert gcd_intermediate(48, 18) == 6
    assert lcm(4, 6) == 12
    assert gcd_intermediate(0, 5) == 5
    assert lcm(0, 5) == 0
    assert gcd_array([24, 36, 48]) == 12
    print("All gcd-lcm tests passed!")

if __name__ == "__main__":
    run_tests()
