"""
# ==============================================================================
# COMPETITIVE PROGRAMMING: MODULAR ARITHMETIC TEMPLATE
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You will frequently see this instruction in competitive programming:
# "Since the answer may be very large, return it modulo 10^9 + 7."
#
# Why? Because in languages like C++ and Java, if you calculate the 100th 
# Fibonacci number or 50! (factorial), the number physically exceeds the 64-bit 
# integer RAM limit (9,223,372,036,854,775,807). The CPU triggers an Integer 
# Overflow, and the number wraps around to negative billions, destroying the math.
#
# To prevent this, judges require you to wrap the math around a Prime Number, 
# typically $10^9 + 7$ (1,000,000,007).
#
# Python natively handles infinitely large integers (BigInt). You will never 
# get an overflow error in Python. However, calculating massive numbers takes 
# $O(N^2)$ time in Python's BigInt engine. To keep your code fast, you must 
# still execute the Modulo operations at every step.
#
# Furthermore, you cannot do Division under a Modulo! You must use Modular Inverse.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Modular Addition, Subtraction, and Multiplication.
# - Understand the trap of Modular Division.
# - Implement Fermat's Little Theorem (Modular Multiplicative Inverse).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# The standard Prime Modulo used in 90% of contests
MOD = 10**9 + 7

# ==============================================================================
# 3. MODULAR ADDITION & MULTIPLICATION
# ==============================================================================
def demonstrate_basic_modulo():
    section_header("Basic Modular Arithmetic")
    
    print("The Golden Rule: Apply the modulo at EVERY single step of the calculation, ")
    print("not just at the very end.\n")
    
    a = 10**8
    b = 10**8
    c = 10**8
    
    # BAD: Calculating the massive number first, then modding.
    # In C++, this causes an overflow crash before the % operator even runs!
    bad_result = (a * b * c) % MOD
    
    # GOOD: Modulo at every step!
    # (a * b) % M = ((a % M) * (b % M)) % M
    good_result = (((a * b) % MOD) * c) % MOD
    
    print(f"Result: {good_result}")
    
    print("\nIn Python, you can write `ans = (ans + x) % MOD` safely.")


# ==============================================================================
# 4. MODULAR DIVISION (THE FATAL TRAP)
# ==============================================================================
def demonstrate_modular_inverse():
    section_header("Modular Division & Fermat's Little Theorem")
    
    print("Suppose you want to calculate: (8 / 2) % 5")
    print("Math: 8 / 2 = 4.  4 % 5 = 4. The true answer is 4.")
    
    print("\nNow let's apply the modulo to the numerator and denominator separately:")
    print("Numerator  : 8 % 5 = 3")
    print("Denominator: 2 % 5 = 2")
    print("Division   : 3 / 2 = 1.5")
    print("1.5 % 5 is mathematically undefined for integers! It breaks completely.\n")
    
    print("--- Fermat's Little Theorem ---")
    print("You CANNOT divide under a modulo.")
    print("Instead of calculating (A / B), you must calculate (A * B^-1).")
    print("You must find the 'Modular Multiplicative Inverse' of B.")
    
    print("\nFermat proved that if M is Prime, the inverse of B is: B^(M-2) % M")
    
    # We want to calculate (8 / 2) % 5. 
    # M = 5 (a Prime Number)
    # A = 8
    # B = 2
    M = 5
    A = 8
    B = 2
    
    # 1. Calculate B^(M-2) % M
    # Python's built-in pow() natively supports modulo as the 3rd argument!
    # It runs in blazing fast O(log N) time using Binary Exponentiation.
    inverse_B = pow(B, M - 2, M)
    print(f"The Modular Inverse of {B} mod {M} is {inverse_B}")
    
    # 2. Multiply A by the Inverse
    final_answer = (A * inverse_B) % M
    print(f"Modular Division Result: (8 * {inverse_B}) % 5 = {final_answer}")
    print("It perfectly matches the true mathematical answer of 4!")


# ==============================================================================
# 5. PYTHON 3.8+ MAGIC CHEAT CODE
# ==============================================================================
def demonstrate_python38_inverse():
    section_header("Python 3.8+ Modular Inverse Cheat")
    
    print("If you forget Fermat's Little Theorem during a contest, do not panic.")
    print("Since Python 3.8, the built-in `pow()` function handles modular inverse ")
    print("natively if you pass a negative exponent!\n")
    
    M = 5
    B = 2
    
    # Instead of pow(B, M-2, M)
    # Just ask for B^-1 mod M!
    try:
        inverse_B = pow(B, -1, M)
        print(f"pow({B}, -1, {M}) = {inverse_B}")
    except ValueError as e:
        print(f"Error: {e}")
        
    print("\nThis only works if B and M are coprime (which is guaranteed if ")
    print("M is a prime number like 10^9+7).")


def run_all_labs():
    demonstrate_basic_modulo()
    demonstrate_modular_inverse()
    demonstrate_python38_inverse()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do competitive programming platforms force you to modulo by $10^9 + 7$?
   Answer: In statically typed languages (C++, Java), physical RAM allocations limit integers to 64 bits (max value $\approx 9 \times 10^{18}$). Algorithms calculating combinatorics (like Factorials) or large Fibonacci numbers will instantly exceed this hardware limit, causing an Integer Overflow that wraps the bits back to negative numbers, permanently corrupting the math. $10^9 + 7$ is chosen because it is large enough to prevent random hash collisions, small enough that multiplying two modded numbers together ($10^9 \times 10^9 = 10^{18}$) fits perfectly inside the 64-bit limit without overflowing before the next modulo executes, and it is a Prime Number, which is mathematically required for Division (Modular Inverse).

2. You need to calculate Combinations: $\frac{N!}{K! (N-K)!} \pmod M$. Why can't you just calculate the factorials, divide them, and apply `% M` at the very end?
   Answer: Because the raw factorial of $N$ (e.g., $10^5!$) is astronomically large. In C++, attempting to calculate it will instantly trigger an overflow. In Python, which supports infinitely large BigInts, it will not overflow, but the arbitrary-precision math engine will require $O(N^2)$ time to multiply numbers with hundreds of thousands of digits, causing a Time Limit Exceeded (TLE) error. You are mathematically forced to apply the modulo at every single step of the loop to keep the integer sizes small (under $10^9$).

3. Since you must apply the modulo at every step, how do you handle the division $\frac{A}{B}$?
   Answer: Mathematical division does not exist under a modulo constraint. You must multiply by the Modular Multiplicative Inverse ($A \times B^{-1} \pmod M$). Because the modulo $M$ ($10^9 + 7$) is a Prime Number, we can use Fermat's Little Theorem, which states that $B^{M-1} \equiv 1 \pmod M$. By dividing both sides by $B$, we mathematically prove that the inverse $B^{-1} \equiv B^{M-2} \pmod M$. In Python, this is calculated instantly in $O(\log N)$ time using binary exponentiation: `pow(B, M-2, M)` or simply `pow(B, -1, M)`.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Modular Arithmetic Template Completed.")
