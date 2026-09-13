"""
# ==============================================================================
# LABORATORY: GCD, LCM & EXTENDED EUCLIDEAN ALGORITHM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Greatest Common Divisor (GCD). 
# If you have a room of 105 men and 90 women, what is the largest team size you 
# can create where every team has the exact same number of people, and no one 
# is left out? GCD(105, 90) = 15.
#
# Around 300 BC, the Greek mathematician Euclid wrote the "Elements", publishing 
# the Euclidean Algorithm. It is widely considered the oldest non-trivial algorithm 
# in human history that is still used today.
# 
# The magic: GCD(A, B) is mathematically identical to GCD(B, A % B).
# By continuously taking the remainder, the numbers plummet in size logarithmically.
# It computes the GCD of two massive 100-digit numbers in fractions of a millisecond, 
# taking exactly O(log(min(A, B))) time.
#
# The Extended Euclidean Algorithm:
# In the 1600s, Étienne Bézout proved that you can always find two integers 
# `x` and `y` such that: A*x + B*y = GCD(A, B).
# The Extended algorithm computes these `x` and `y` coefficients.
#
# Why do we care? 
# Because this equation is the exact mathematical mechanism used to calculate 
# the "Modular Multiplicative Inverse". 
# The Modular Inverse is the cryptographic "Key" used to DECRYPT RSA encryption. 
# Every time you securely log into a website (HTTPS), your computer runs the 
# Extended Euclidean algorithm in the background to establish the secure connection!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement the 300 BC Euclidean Algorithm (Recursive & Iterative).
# - Understand LCM = (A * B) / GCD(A, B).
# - Master the Extended Euclidean Algorithm and Bézout's Identity.
#
# ==============================================================================
"""

from typing import Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE EUCLIDEAN ALGORITHM (O(LOG N))
# ==============================================================================
def gcd_recursive(a: int, b: int) -> int:
    """
    The classic Euclidean Algorithm.
    Base Case: When B hits 0, A holds the Greatest Common Divisor.
    Recursive Step: Swap the numbers and take the remainder (A % B).
    """
    if b == 0:
        return a
    return gcd_recursive(b, a % b)

def gcd_iterative(a: int, b: int) -> int:
    """
    Iterative version to prevent Python's maximum recursion depth limits 
    when dealing with pathologically massive integers.
    """
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """
    Least Common Multiple (LCM).
    Math formula: A * B = GCD * LCM
    Therefore: LCM = (A * B) / GCD
    Note: We divide FIRST to prevent integer overflow in strongly typed languages.
    """
    if a == 0 or b == 0:
        return 0
    # Use integer division `//` to return a clean integer!
    return (a // gcd_iterative(a, b)) * b


# ==============================================================================
# 4. EXTENDED EUCLIDEAN ALGORITHM & MODULAR INVERSE
# ==============================================================================
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Finds the GCD, AND the coefficients `x` and `y` for Bézout's Identity:
    A*x + B*y = GCD(A, B)
    
    Returns: (gcd, x, y)
    """
    # Base Case: When B hits 0, GCD is A.
    # The equation becomes: A*1 + 0*0 = A. So x=1, y=0.
    if b == 0:
        return a, 1, 0
        
    # Recursive Call: Calculate for (B, A % B)
    gcd, x1, y1 = extended_gcd(b, a % b)
    
    # Back-Substitution Math:
    # A % B = A - (A // B) * B
    # Substituting this back into the equation reveals the coefficient update rules!
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Calculates the Modular Multiplicative Inverse of `a` modulo `m`.
    This means finding an `x` such that: (a * x) % m == 1
    
    This is mathematically ONLY possible if GCD(a, m) == 1 (they are coprime).
    If they are coprime, Bézout's Identity says: a*x + m*y = 1
    Taking both sides modulo `m` destroys the `m*y` term, leaving:
    (a*x) % m = 1 % m
    Therefore, the `x` from the Extended GCD is the exact answer!
    """
    gcd, x, y = extended_gcd(a, m)
    
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist. {a} and {m} are not coprime.")
        
    # `x` might be negative because of the back-substitution math.
    # We add `m` and take modulo `m` to wrap it around into a positive domain!
    return (x % m + m) % m


def demonstrate_euclidean():
    section_header("Algorithm: Euclidean GCD & LCM")
    
    a, b = 105, 90
    print(f"Finding GCD for {a} and {b}...")
    g = gcd_iterative(a, b)
    print(f"GCD({a}, {b}) = {g}")
    
    l = lcm(a, b)
    print(f"LCM({a}, {b}) = {l}")
    
    section_header("Extended Euclidean & Bézout's Identity")
    
    a, b = 240, 46
    print(f"Solving A*x + B*y = GCD(A, B) for A={a}, B={b}")
    gcd, x, y = extended_gcd(a, b)
    
    print(f"Result: GCD = {gcd}, x = {x}, y = {y}")
    print(f"Verification: ({a} * {x}) + ({b} * {y}) = {a*x} + {b*y} = {a*x + b*y}")
    
    section_header("Cryptographic Application: Modular Inverse")
    
    a = 3
    m = 11
    print(f"Finding Modular Inverse of {a} mod {m}")
    print(f"We need an integer 'x' where ({a} * x) % {m} == 1")
    
    inv = mod_inverse(a, m)
    print(f"Calculated Inverse: {inv}")
    print(f"Verification: ({a} * {inv}) = {a*inv}. {a*inv} % {m} = {(a*inv)%m}!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `gcd(A, B) == gcd(B, A % B)`?
   Answer: Let $G$ be the greatest common divisor of $A$ and $B$. This means $A = xG$ and $B = yG$.
   The remainder $A \% B$ is mathematically equal to $A - k \times B$ (where $k$ is the integer quotient).
   Substituting the variables: $A \% B = (xG) - k \times (yG) = G(x - ky)$.
   Notice that $G$ perfectly factors out! Therefore, whatever divides both $A$ and $B$ must ALSO perfectly divide the remainder. The GCD is mathematically preserved across the modulo operation!

2. Why is the time complexity $O(\log \min(A, B))$?
   Answer: Lamé's Theorem (1844) proved that the absolute worst-case scenario for the Euclidean algorithm occurs when $A$ and $B$ are consecutive Fibonacci numbers. Because the Fibonacci sequence grows exponentially, the number of modulo divisions required to reach 0 is bounded logarithmically by the golden ratio. At worst, the algorithm terminates in $5 \times d$ steps, where $d$ is the number of decimal digits in the smaller number.

3. Why is the Modular Inverse critical for RSA Cryptography?
   Answer: In RSA, your public key contains a number $E$ (the encryption exponent) and a massive modulus $M$. To encrypt a message $X$, you do $X^E \pmod M$. 
   How do you get $X$ back? You need a magical Decryption exponent $D$. 
   The math of RSA dictates that $D$ MUST be the Modular Multiplicative Inverse of $E$. The only way to calculate $D$ is to run the Extended Euclidean Algorithm! Without it, decryption would be mathematically impossible.
"""

if __name__ == "__main__":
    demonstrate_euclidean()
    print("\n[SUCCESS] Laboratory: GCD, LCM & Extended Euclidean Completed.")
