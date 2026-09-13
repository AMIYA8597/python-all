"""
# ==============================================================================
# LABORATORY: MODULAR ARITHMETIC & BINARY EXPONENTIATION
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you solve a hard algorithmic problem, you will often see this dreaded phrase:
# "The answer may be very large. Return it modulo 10^9 + 7."
#
# Why? Because in many languages (like C++, Java, or Rust), an integer is 
# physically limited to 64 bits. The absolute maximum number a 64-bit integer 
# can store is 9,223,372,036,854,775,807.
# 
# If your dynamic programming algorithm calculates the 100th Fibonacci number 
# or computes $1000!$ (factorial), the number will exceed the RAM limits and crash 
# (Integer Overflow).
#
# The solution is Modular Arithmetic. We wrap the number around a massive prime 
# boundary (like $10^9 + 7$) at EVERY SINGLE STEP of the calculation!
# 
# The Mathematical Rules of Modulo:
# - Addition: (A + B) % M = ( (A % M) + (B % M) ) % M
# - Multiplication: (A * B) % M = ( (A % M) * (B % M) ) % M
# - Subtraction: (A - B) % M = ( (A % M) - (B % M) + M ) % M  <-- The +M Trick!
# - Division: Division is completely illegal in modular arithmetic! 
#   You cannot do (A / B) % M. You must multiply A by the "Modular Inverse" of B!
#   (A / B) % M = ( A * ModInverse(B, M) ) % M
#
# Binary Exponentiation (Fast Power):
# If you need to calculate (2^1000000000) % M, you cannot loop a billion times.
# Binary Exponentiation calculates it in exactly O(log N) multiplications!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Modulo Distribution properties.
# - Handle Negative Modulo mathematically safely.
# - Implement O(log N) Binary Exponentiation from scratch.
# - Understand Fermat's Little Theorem for O(log M) modular inverses.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BINARY EXPONENTIATION (O(LOG B))
# ==============================================================================
def binary_exponentiation(base: int, exp: int, mod: int) -> int:
    """
    Calculates (base ^ exp) % mod in strict O(log(exp)) time.
    This is identical to Python's built-in `pow(base, exp, mod)`.
    """
    result = 1
    
    # We must modulo the base first in case it is already larger than the mod!
    base = base % mod
    
    # Example: 3^13
    # 13 in binary is 1101 (8 + 4 + 1).
    # 3^13 = 3^8 * 3^4 * 3^1
    # We just continuously square the base (3 -> 9 -> 81 -> 6561).
    # If the current binary bit is a '1', we multiply it into our result!
    while exp > 0:
        
        # Check if the rightmost bit is 1 (Odd)
        if exp % 2 == 1:
            result = (result * base) % mod
            
        # Shift the exponent right by 1 bit (Integer Division by 2)
        exp //= 2
        
        # Square the base for the next bit!
        base = (base * base) % mod
        
    return result


# ==============================================================================
# 4. MODULAR ARITHMETIC ENGINES
# ==============================================================================
class ModMath:
    def __init__(self, modulo: int = 1000000007):
        self.M = modulo

    def add(self, a: int, b: int) -> int:
        return ((a % self.M) + (b % self.M)) % self.M

    def subtract(self, a: int, b: int) -> int:
        """
        In C++, -5 % 3 equals -2. In Python, it mathematically wraps to 1.
        To be language-agnostic and cryptographically safe, we explicitly add 
        the Modulo to force a positive domain before the final modulo!
        """
        return ((a % self.M) - (b % self.M) + self.M) % self.M

    def multiply(self, a: int, b: int) -> int:
        return ((a % self.M) * (b % self.M)) % self.M

    def mod_inverse(self, b: int) -> int:
        """
        Calculates the Modular Inverse of B using Fermat's Little Theorem!
        If M is a Prime number, Fermat states: B^(M-1) = 1 (mod M).
        If we divide both sides by B, we get: B^(M-2) = B^(-1) (mod M).
        Therefore, the inverse of B is simply B^(M-2) % M !
        This takes O(log M) time using Binary Exponentiation!
        """
        # Note: This ONLY works if M is Prime. If M is not prime, you MUST use 
        # the Extended Euclidean Algorithm from the previous lab!
        return binary_exponentiation(b, self.M - 2, self.M)

    def divide(self, a: int, b: int) -> int:
        """
        (A / B) % M = (A * ModInverse(B)) % M
        """
        inverse_b = self.mod_inverse(b)
        return self.multiply(a, inverse_b)


def demonstrate_modular_arithmetic():
    section_header("Algorithm: Binary Exponentiation")
    
    base = 3
    exp = 13
    mod = 1000000007
    
    print(f"Calculating ({base}^{exp}) % {mod}...")
    ans = binary_exponentiation(base, exp, mod)
    print(f"Result: {ans}")
    print(f"Verification: {base**exp} % {mod} = {(base**exp) % mod}")
    
    section_header("Algorithm: Modular Arithmetic Operations")
    
    modmath = ModMath(7) # Use small prime for easy verification
    a, b = 20, 15
    print(f"A = {a}, B = {b}, Modulo = 7")
    
    # Subtraction (The +M trick)
    sub_ans = modmath.subtract(a, b)
    print(f"Subtraction: ({a} - {b}) % 7 = {sub_ans} | Verify: {20-15} % 7 = {(20-15)%7}")
    
    # Division (Fermat's Mod Inverse)
    # Let's do (20 / 4) % 7.
    # 20 / 4 = 5. 5 % 7 = 5.
    a2, b2 = 20, 4
    div_ans = modmath.divide(a2, b2)
    print(f"Division: ({a2} / {b2}) % 7 = {div_ans} | Verify: (20/4) = 5. 5%7 = 5!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Modulo Addition `(A % M) + (B % M)` mathematically safe?
   Answer: Because adding two remainders can at most yield $2M - 2$. For example, if $M = 10^9+7$, the maximum possible remainder is $10^9+6$. Adding two of them together yields roughly $2 \times 10^9$. This fits perfectly and safely inside a standard 32-bit integer (limit $2.14 \times 10^9$), completely preventing integer overflow! The final `% M` wraps it back down.

2. Why is Modulo Subtraction dangerous in C++/Java compared to Python?
   Answer: In mathematics, Modulo is a "Wrap-Around" operation. If it's 2 o'clock and you subtract 5 hours, it wraps around the 12-hour clock to 9 o'clock. Python correctly implements this mathematically: `-5 % 12 == 7`. 
   However, C, C++, and Java treat the `%` operator as "Remainder", not Modulo! In C++, `-5 % 12 == -5`. It retains the negative sign! If you pass a negative number into a dynamic programming array index, the program will crash. The `+ M` trick `(A - B + M) % M` guarantees the value is pushed into the positive domain before taking the remainder, ensuring safety across all languages.

3. Fermat's Little Theorem vs Extended Euclidean for Mod Inverse?
   Answer: Fermat's Little Theorem `pow(b, M-2, M)` is incredibly short to write, making it the preferred method in competitive programming. HOWEVER, it is mathematically proven to ONLY work if $M$ is a Prime number! If a problem gives you a non-prime modulo (like $10^9$), Fermat will fail catastrophically and silently return the wrong answer. In those rare non-prime cases, you MUST write out the full Extended Euclidean Algorithm.
"""

if __name__ == "__main__":
    demonstrate_modular_arithmetic()
    print("\n[SUCCESS] Laboratory: Modular Arithmetic Completed.")
