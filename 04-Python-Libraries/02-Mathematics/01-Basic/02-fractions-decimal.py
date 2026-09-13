"""
# ==============================================================================
# LABORATORY: EXACT ARITHMETIC (DECIMAL & FRACTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned about the IEEE 754 Floating-Point disaster.
# `0.1 + 0.2 == 0.3` is mathematically False in Python because Binary (Base-2) 
# hardware cannot accurately represent fractional decimals like 1/10.
#
# If you are programming a video game physics engine, `math.isclose()` is fine. 
# But what if you are programming a Banking Application? 
# If a microscopic floating-point error deducts $0.00000001$ cents incorrectly 
# millions of times a day, the bank's accounting ledger will break, and you 
# will be fired.
#
# Python provides two standard library modules for PERFECT mathematical accuracy:
# 1. `decimal`: Simulates human Base-10 math perfectly (ideal for Currency).
# 2. `fractions`: Stores numbers as exact mathematical Ratios (Numerator/Denominator), 
#    completely bypassing decimal conversions (ideal for pure Algebra).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Fix the `0.1 + 0.2` bug permanently using `Decimal`.
# - Understand why `Decimal` must be initialized with Strings.
# - Execute perfect rational math using `Fraction`.
#
# ==============================================================================
"""

from decimal import Decimal, getcontext
from fractions import Fraction

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DECIMAL MODULE (BASE-10 CURRENCY MATH)
# ==============================================================================
def demonstrate_decimal():
    section_header("The Decimal Module (Banking Math)")
    
    # Let's revisit the floating point bug.
    float_sum = 0.1 + 0.2
    print(f"Standard Float Math: 0.1 + 0.2 = {float_sum:.20f}")
    
    # THE FIX
    # CRITICAL WARNING: You MUST initialize Decimals using Strings!
    # If you write `Decimal(0.1)`, Python evaluates the float `0.1` FIRST (which 
    # immediately introduces the binary hardware error), and THEN passes the 
    # corrupted binary garbage into Decimal!
    
    dec_a = Decimal("0.1")
    dec_b = Decimal("0.2")
    dec_c = Decimal("0.3")
    
    dec_sum = dec_a + dec_b
    
    print(f"\nDecimal String Math: Decimal('0.1') + Decimal('0.2') = {dec_sum}")
    print(f"Is it exactly 0.3? -> {dec_sum == dec_c}")
    
    # 2. CONFIGURING CONTEXT
    # `Decimal` allows you to change the global precision of the entire program!
    print("\nModifying Global Precision Context:")
    getcontext().prec = 50 # 50 digits of mathematical precision!
    
    massive_division = Decimal("1") / Decimal("7")
    print(f"Decimal('1') / Decimal('7') to 50 decimal places:")
    print(massive_division)


# ==============================================================================
# 4. THE FRACTIONS MODULE (RATIONAL MATH)
# ==============================================================================
def demonstrate_fractions():
    section_header("The Fractions Module (Pure Algebra)")
    
    # Even `Decimal` cannot perfectly store 1/3 (it becomes 0.333... and eventually 
    # truncates based on the context precision). 
    # `Fraction` avoids decimals entirely. It just stores the Numerator and Denominator!
    
    f1 = Fraction(1, 3)
    f2 = Fraction(1, 6)
    
    print(f"Fraction 1: {f1}")
    print(f"Fraction 2: {f2}")
    
    # 1. PERFECT ADDITION
    # Math: 1/3 + 1/6 = 2/6 + 1/6 = 3/6 = 1/2
    result_add = f1 + f2
    print(f"\nAddition: {f1} + {f2} = {result_add}")
    
    # 2. STRING INITIALIZATION
    print("\nParsing from Strings:")
    f3 = Fraction("1.25")
    print(f"Fraction('1.25') automatically simplifies to: {f3}")
    
    # 3. EXTRACTING NUMERATOR AND DENOMINATOR
    print(f"\nExtracting parts of {result_add}:")
    print(f"Numerator  : {result_add.numerator}")
    print(f"Denominator: {result_add.denominator}")
    
    # 4. AVOIDING FLOAT CORRUPTION
    # Just like Decimal, initializing Fraction with a float brings the IEEE 754 
    # garbage along with it!
    f_bad = Fraction(0.1)
    print("\nWARNING: Initializing Fraction with a float (0.1):")
    print(f"Fraction(0.1) = {f_bad}")
    print("Because 0.1 is binary garbage, the fraction represents the exact memory state!")


def run_all_labs():
    demonstrate_decimal()
    demonstrate_fractions()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must `Decimal` and `Fraction` be initialized using Strings?
   Answer: When Python encounters `Decimal(0.1)`, the Python Interpreter evaluates the parameter `0.1` *before* the `Decimal` class is ever called. The CPU converts `0.1` into the IEEE 754 Base-2 binary standard, which introduces microscopic truncation errors. By the time the `Decimal` class receives the data, it is already mathematically corrupted. By passing `"0.1"` as a String, the `Decimal` and `Fraction` classes use custom string-parsing algorithms to bypass the CPU's binary conversion entirely, building the exact mathematical representation in software.

2. If `Decimal` perfectly solves floating-point errors, why don't we use it for everything?
   Answer: Performance! Standard `float` addition is processed natively by the hardware Arithmetic Logic Unit (ALU) on the CPU in a single clock cycle (nanoseconds). `Decimal` is a Software construct. When you add two `Decimal` objects, Python must execute dozens of lines of string-parsing and software-based digit alignment logic. It is thousands of times slower than hardware floats. You use `float` for Graphics/Physics/AI where speed is critical. You use `Decimal` for Currency/Banking where perfection is required and speed is irrelevant.

3. What is the difference between `Decimal` and `Fraction`?
   Answer: 
   - `Decimal` enforces exact Base-10 arithmetic, just like human humans do math. It is perfect for fixed-point math like Currency (`$1.99`), but it still fails at infinitely repeating numbers (e.g., $1/3 = 0.3333333$, which eventually gets truncated based on `getcontext().prec`).
   - `Fraction` implements Pure Rational Mathematics. It NEVER converts to decimals. It perfectly stores the two integers (Numerator and Denominator). $1/3$ is stored exactly as $1$ and $3$. Therefore, it can hold infinitely repeating mathematical concepts with absolute perfection.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Exact Arithmetic Completed.")
