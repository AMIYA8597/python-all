"""
Module: 02-fractions-decimal
Description: A textbook-grade interactive lesson on Python's `fractions` and `decimal` modules.

===========================================================================
TEXTBOOK-GRADE LESSON: FRACTIONS AND DECIMALS IN PYTHON
===========================================================================

1. INTRODUCTION TO THE PROBLEM
------------------------------
In standard computing, numbers with fractional parts are usually represented
using the IEEE 754 double-precision floating-point format (the `float` type in
Python). Because floats are based on base-2 (binary) fractions, many base-10
decimals cannot be represented exactly.

For example, 0.1 in binary is a repeating fraction:
0.000110011001100110011...

This leads to precision loss:
0.1 + 0.1 + 0.1 != 0.3 (in standard floats, it evaluates to 0.30000000000000004)

While this is perfectly acceptable for most engineering, scientific, and graphics
applications due to its high speed (hardware support), it is UNACCEPTABLE in
domains like:
- Finance and Banking (where $0.01 differences accumulate over millions of transactions).
- Strict scientific arithmetic where exact fractional representation is required.
- High-precision engineering tolerances.

2. THE `decimal` MODULE
-----------------------
The `decimal` module provides support for fast correctly rounded decimal floating
point arithmetic. It offers several advantages over the `float` datatype:
- Exact decimal representation.
- Preservation of significance (e.g., 1.30 + 1.20 = 2.50, keeping trailing zeros).
- User-alterable precision (default is 28 places, but can be set to anything).
- Various rounding modes (ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_CEILING, etc.).

Mathematical Background:
Decimals are represented as a sign, a coefficient (digits), and an exponent.
Value = (-1)^sign * coefficient * 10^exponent.

3. THE `fractions` MODULE
-------------------------
The `fractions` module provides support for rational number arithmetic. A rational
number is any number that can be expressed as the quotient or fraction p/q of two
integers, a numerator p and a non-zero denominator q.

Advantages over `float` and `decimal`:
- Completely exact representation of any rational number, regardless of base-10
  or base-2 repeating patterns (e.g., 1/3 is exactly 1/3, not 0.33333333...).
- Simplification of fractions is automatic (e.g., 2/4 becomes 1/2).

Mathematical Background:
Fraction operations follow standard arithmetic for rationals:
- Addition: a/b + c/d = (ad + bc) / bd
- Multiplication: a/b * c/d = ac / bd
- GCD (Greatest Common Divisor) is used to simplify the resulting fraction.

4. BIG-O TIME COMPLEXITY ANALYSIS
---------------------------------
# `decimal.Decimal`
- Instantiation: O(N) where N is the number of digits.
- Addition/Subtraction: O(N), dependent on the number of significant digits.
- Multiplication: O(N^2) for standard implementation, but fast multiplication
  algorithms (like Karatsuba or Toom-Cook) may be used for very large numbers.

# `fractions.Fraction`
- Instantiation: O(log(min(a, b))) due to the GCD calculation to simplify.
- Addition/Subtraction: O(log(min(a, b))) to O(N) where N is the bit length, due
  to GCD calculation after finding the common denominator.
- Multiplication/Division: O(log(min(a, b))) for GCD simplification of the result.

5. BEST PRACTICES & TYPE HINTS
------------------------------
Always import explicitly and type hint appropriately using `Decimal` and `Fraction`.
Do NOT mix `float` with `Decimal` or `Fraction` unless absolutely necessary,
as it re-introduces precision issues. Instantiate them from strings (`"0.1"`)
or integers instead of floats (`0.1`).
"""

import sys
import time
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, InvalidOperation
from fractions import Fraction
from typing import List, Tuple, Union, Any, Dict

# ---------------------------------------------------------------------------
# SECTION 1: FLOATING POINT ISSUES
# ---------------------------------------------------------------------------

def demonstrate_floating_point_issues() -> None:
    """
    Demonstrates why floats are dangerous for exact arithmetic (like money).
    """
    print("\n" + "="*50)
    print(" SECTION 1: THE PROBLEM WITH FLOATING POINT (IEEE 754) ")
    print("="*50)

    # Issue 1: Simple Addition
    val = 0.1 + 0.1 + 0.1
    print(f"0.1 + 0.1 + 0.1 evaluates to: {val}")
    print(f"Is 0.1 + 0.1 + 0.1 == 0.3?  {val == 0.3}")

    # Issue 2: Accumulation of error
    balance = 0.0
    for _ in range(10):
        balance += 0.1
    print(f"\nAdding 0.1 ten times to 0.0 gives: {balance}")
    print(f"Is balance == 1.0? {balance == 1.0}")
    
    # Issue 3: Subtraction cancellation
    large_num = 1e16
    small_num = 1.0
    result = large_num + small_num - large_num
    print(f"\n(1e16 + 1.0) - 1e16 evaluates to: {result}")
    print("Note how the 1.0 was completely lost due to precision limits of 64-bit floats!")

# ---------------------------------------------------------------------------
# SECTION 2: THE DECIMAL MODULE
# ---------------------------------------------------------------------------

def decimal_basics() -> None:
    """
    Demonstrates basic instantiation and context manipulation with `decimal`.
    """
    print("\n" + "="*50)
    print(" SECTION 2: DECIMAL BASICS AND CONTEXT ")
    print("="*50)
    
    # Correct way to instantiate Decimal
    # ALWAYS use strings or integers, NEVER floats (unless intentional)
    d_str = Decimal("0.1")
    d_int = Decimal(5)
    d_float = Decimal(0.1) # DANGEROUS! Inherits float inaccuracy
    
    print("Instantiation Examples:")
    print(f"Decimal('0.1') -> {d_str} (Exact)")
    print(f"Decimal(5)     -> {d_int} (Exact)")
    print(f"Decimal(0.1)   -> {d_float} (Inherits float precision loss!)")
    
    # Fixing the earlier addition issue
    correct_val = Decimal("0.1") + Decimal("0.1") + Decimal("0.1")
    print(f"\nDecimal('0.1') + Decimal('0.1') + Decimal('0.1') == Decimal('0.3'): {correct_val == Decimal('0.3')}")

    # Context management
    ctx = getcontext()
    print("\n--- Default Decimal Context ---")
    print(f"Default Precision: {ctx.prec} digits")
    print(f"Default Rounding Mode: {ctx.rounding}")

    # Changing precision
    ctx.prec = 50
    result_high_prec = Decimal(1) / Decimal(7)
    print(f"\n1/7 with 50 digits precision:\n{result_high_prec}")
    
    # Restore default for subsequent tests
    ctx.prec = 28

def decimal_rounding_modes() -> None:
    """
    Showcases the various rounding modes available in the decimal module.
    Crucial for financial applications (e.g., Bankers' Rounding).
    """
    print("\n" + "="*50)
    print(" SECTION 3: DECIMAL ROUNDING MODES ")
    print("="*50)

    numbers_to_round = [Decimal("2.5"), Decimal("3.5"), Decimal("-2.5"), Decimal("2.4"), Decimal("2.6")]
    
    print(f"{'Number':<10} | {'HALF_EVEN':<12} | {'HALF_UP':<12} | {'CEILING':<12} | {'FLOOR':<12}")
    print("-" * 65)

    ctx = getcontext()
    for num in numbers_to_round:
        # Quantize is used to round to a specific number of decimal places.
        # Decimal("1.") means round to 0 decimal places (nearest integer)
        
        ctx.rounding = ROUND_HALF_EVEN # Default, "Banker's Rounding" (rounds to nearest even number if exactly half)
        r_even = num.quantize(Decimal("1."))
        
        ctx.rounding = ROUND_HALF_UP # Standard school rounding (0.5 always rounds up)
        r_up = num.quantize(Decimal("1."))
        
        ctx.rounding = ROUND_CEILING # Rounds towards positive infinity
        r_ceil = num.quantize(Decimal("1."))
        
        ctx.rounding = ROUND_FLOOR # Rounds towards negative infinity
        r_floor = num.quantize(Decimal("1."))
        
        print(f"{str(num):<10} | {str(r_even):<12} | {str(r_up):<12} | {str(r_ceil):<12} | {str(r_floor):<12}")

    # Restore default
    ctx.rounding = ROUND_HALF_EVEN
    
    print("\nTakeaway: ROUND_HALF_EVEN is the default because it minimizes cumulative rounding errors")
    print("in large datasets by balancing the direction of rounding for .5 cases.")

def decimal_real_world_finance() -> None:
    """
    Simulates a real-world scenario of tax calculation requiring precision.
    """
    print("\n" + "="*50)
    print(" SECTION 4: REAL WORLD APPLICATION - FINANCE ")
    print("="*50)
    
    items = [
        {"name": "Widget A", "price": Decimal("19.99")},
        {"name": "Widget B", "price": Decimal("5.49")},
        {"name": "Widget C", "price": Decimal("3.33")},
    ]
    
    tax_rate = Decimal("0.075") # 7.5% tax
    
    subtotal = sum(item["price"] for item in items)
    # The sum function works with Decimals seamlessly
    
    # Calculate tax. Must round to 2 decimal places using standard financial rounding (HALF_UP)
    raw_tax = subtotal * tax_rate
    
    # Use quantize to round the final monetary amount
    getcontext().rounding = ROUND_HALF_UP
    tax = raw_tax.quantize(Decimal("0.01"))
    total = subtotal + tax
    
    print(f"Subtotal:    ${subtotal}")
    print(f"Tax Rate:     {tax_rate * Decimal('100')}%")
    print(f"Raw Tax:     ${raw_tax} (needs rounding)")
    print(f"Rounded Tax: ${tax} (quantized to 0.01)")
    print(f"Total:       ${total}")

# ---------------------------------------------------------------------------
# SECTION 3: THE FRACTIONS MODULE
# ---------------------------------------------------------------------------

def fraction_basics() -> None:
    """
    Demonstrates instantiation and core operations of the fractions module.
    """
    print("\n" + "="*50)
    print(" SECTION 5: FRACTION BASICS ")
    print("="*50)
    
    # Instantiating Fractions
    f1 = Fraction(1, 3)          # From numerator, denominator
    f2 = Fraction('2/5')         # From string
    f3 = Fraction(Decimal('0.1'))# From Decimal
    
    print("Instantiation Examples:")
    print(f"Fraction(1, 3)          -> {f1}")
    print(f"Fraction('2/5')         -> {f2}")
    print(f"Fraction(Decimal('0.1'))-> {f3}")
    
    # Auto-simplification
    f4 = Fraction(10, 20)
    print(f"\nSimplification: Fraction(10, 20) automatically becomes -> {f4}")
    
    # Arithmetic
    result_add = f1 + f2
    result_mul = f1 * f2
    
    print(f"\nArithmetic:")
    print(f"{f1} + {f2} = {result_add}")
    print(f"{f1} * {f2} = {result_mul}")
    
    # Mixed type arithmetic (Fraction + int is ok, Fraction + float results in float)
    mixed_add = f1 + 2
    mixed_float = f1 + 0.5
    print(f"\n{f1} + 2 = {mixed_add} (Type: {type(mixed_add).__name__})")
    print(f"{f1} + 0.5 = {mixed_float} (Type: {type(mixed_float).__name__}) -> Beware precision loss!")

def fraction_float_limits() -> None:
    """
    Shows how Fractions can expose floating point inaccuracies and how to limit denominators.
    """
    print("\n" + "="*50)
    print(" SECTION 6: FRACTIONS, FLOATS, AND DENOMINATOR LIMITS ")
    print("="*50)
    
    # Extracting fraction from a mathematically "clean" float that is actually imprecise
    f_float = Fraction(math.pi)
    
    print(f"Fraction(math.pi) -> {f_float}")
    print("Notice the massive denominator! This is the EXACT rational representation of the float approximation of Pi.")
    
    # limit_denominator(max_denominator)
    # This is incredibly useful for finding rational approximations of floats.
    approx_pi = f_float.limit_denominator(100)
    best_approx_pi = f_float.limit_denominator(1000)
    
    print(f"\nApproximations of Pi:")
    print(f"Limit denominator to 100:  {approx_pi} (Value: {float(approx_pi):.6f})")
    print(f"Limit denominator to 1000: {best_approx_pi} (Value: {float(best_approx_pi):.6f}) -> Famous 355/113!")
    
    print("\nUse Case: Converting a float like 0.33333333333 to a clean fraction.")
    ugly_float = 0.3333333333333333
    clean_fraction = Fraction(ugly_float).limit_denominator(10)
    print(f"Fraction({ugly_float}).limit_denominator(10) -> {clean_fraction}")

# ---------------------------------------------------------------------------
# SECTION 4: PERFORMANCE & BIG-O COMPARISON
# ---------------------------------------------------------------------------

def performance_analysis() -> None:
    """
    Compares the performance of Float, Decimal, and Fraction for a computationally heavy task.
    
    Big-O Analysis for Arithmetic:
    Float: O(1) - Handled purely by CPU hardware via IEEE 754 circuits. Blazing fast.
    Decimal: O(N) - N is the precision length. Software-based math, significantly slower.
    Fraction: O(log(min(a,b))) - Requires calculating the GCD for simplification on every op.
    """
    print("\n" + "="*50)
    print(" SECTION 7: PERFORMANCE ANALYSIS (BIG-O) ")
    print("="*50)
    
    ITERATIONS = 500_000
    
    print(f"Running {ITERATIONS:,} additions for each type...\n")
    
    # 1. Float Performance
    start = time.perf_counter()
    val_float = 0.0
    add_float = 0.001
    for _ in range(ITERATIONS):
        val_float += add_float
    time_float = time.perf_counter() - start
    
    # 2. Decimal Performance
    start = time.perf_counter()
    val_decimal = Decimal("0.0")
    add_decimal = Decimal("0.001")
    for _ in range(ITERATIONS):
        val_decimal += add_decimal
    time_decimal = time.perf_counter() - start
    
    # 3. Fraction Performance
    start = time.perf_counter()
    val_fraction = Fraction(0, 1)
    add_fraction = Fraction(1, 1000)
    for _ in range(ITERATIONS):
        val_fraction += add_fraction
    time_fraction = time.perf_counter() - start
    
    print(f"{'Data Type':<10} | {'Time Taken (s)':<15} | {'Final Value':<15} | {'Accuracy'}")
    print("-" * 65)
    print(f"{'Float':<10} | {time_float:<15.5f} | {val_float:<15} | Inaccurate (0.001 lost precision)")
    print(f"{'Decimal':<10} | {time_decimal:<15.5f} | {str(val_decimal):<15} | Exact")
    print(f"{'Fraction':<10} | {time_fraction:<15.5f} | {str(val_fraction):<15} | Exact")
    
    print("\nConclusion: Float is O(1) hardware-accelerated. Decimal and Fraction are O(N) or O(log N)")
    print("software objects. Only use Decimal/Fraction when EXACT precision is mandated by the domain.")

# ---------------------------------------------------------------------------
# SECTION 5: INTERVIEW CHALLENGE & EDGE CASES
# ---------------------------------------------------------------------------

def interview_challenge_egyptian_fractions(frac: Fraction) -> List[Fraction]:
    """
    Interview Challenge: Egyptian Fractions
    
    Problem Statement:
    Every positive fraction a/b (where a < b) can be represented as a sum of 
    distinct unit fractions (fractions with numerator 1). This is called an 
    Egyptian Fraction.
    
    Write an algorithm to return the list of unit fractions that sum up to `frac`.
    
    Algorithm (Greedy Approach by Fibonacci/Sylvester):
    1. If the fraction is exactly a unit fraction, append and return.
    2. Otherwise, find the largest unit fraction 1/n that is <= frac.
       The smallest n such that 1/n <= a/b is ceil(b/a).
    3. Add 1/n to the result list.
    4. Recursively apply the algorithm to the remainder: frac - 1/n.
    
    Time Complexity:
    The length of the resulting series is roughly bounded by O(log(denominator)),
    and fraction math operations are O(log(min(a,b))).
    Overall Time Complexity: O(log^2 D) where D is the denominator.
    """
    if frac <= 0 or frac >= 1:
        raise ValueError("Fraction must be between 0 and 1 exclusive.")
        
    result = []
    current = frac
    
    while current.numerator != 1:
        # Find the ceiling of denominator / numerator
        # e.g. for 5/121, ceil(121/5) = 25. So largest unit fraction is 1/25.
        n = math.ceil(current.denominator / current.numerator)
        
        unit_frac = Fraction(1, n)
        result.append(unit_frac)
        
        # Subtract the unit fraction from current
        current = current - unit_frac
        
    # The remainder is now a unit fraction
    result.append(current)
    
    return result

def run_interview_challenge() -> None:
    print("\n" + "="*50)
    print(" SECTION 8: INTERVIEW CHALLENGE - EGYPTIAN FRACTIONS ")
    print("="*50)
    
    test_fractions = [
        Fraction(2, 3),    # Should be 1/2 + 1/6
        Fraction(6, 14),   # Simplified to 3/7 -> 1/3 + 1/11 + 1/231
        Fraction(12, 13)
    ]
    
    for f in test_fractions:
        egyptian = interview_challenge_egyptian_fractions(f)
        sum_verification = sum(egyptian)
        
        str_repr = " + ".join(str(ef) for ef in egyptian)
        print(f"Target: {f}")
        print(f"Egyptian Representation: {str_repr}")
        print(f"Verification Sum: {sum_verification} (Matches target: {sum_verification == f})\n")


# ---------------------------------------------------------------------------
# MAIN EXECUTION & TESTS
# ---------------------------------------------------------------------------

def run_all_tests() -> None:
    """
    Self-contained unit tests to guarantee correctness of the module's logic.
    """
    print("\n" + "="*50)
    print(" SECTION 9: UNIT TESTS ")
    print("="*50)
    
    try:
        # Test Decimal
        assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3"), "Decimal math failed!"
        
        # Test Context Rounding
        ctx = getcontext()
        ctx.rounding = ROUND_HALF_UP
        assert Decimal("2.5").quantize(Decimal("1.")) == Decimal("3"), "Decimal Half-Up failed!"
        ctx.rounding = ROUND_HALF_EVEN
        assert Decimal("2.5").quantize(Decimal("1.")) == Decimal("2"), "Decimal Half-Even failed!"
        
        # Test Fractions
        assert Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2), "Fraction arithmetic failed!"
        assert Fraction(0.3333333333).limit_denominator(10) == Fraction(1, 3), "limit_denominator failed!"
        
        # Test Egyptian Fractions
        egyptian_res = interview_challenge_egyptian_fractions(Fraction(3, 7))
        assert egyptian_res == [Fraction(1, 3), Fraction(1, 11), Fraction(1, 231)], "Egyptian fractions logic failed!"
        
        print("ALL TESTS PASSED SUCCESSFULLY! ✅")
        
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print(f"\n{'*'*70}")
    print(f"EXPLORING PYTHON MATH: FRACTIONS AND DECIMALS".center(70))
    print(f"{'*'*70}")
    
    demonstrate_floating_point_issues()
    decimal_basics()
    decimal_rounding_modes()
    decimal_real_world_finance()
    
    fraction_basics()
    fraction_float_limits()
    
    performance_analysis()
    
    run_interview_challenge()
    
    run_all_tests()
    
    print("\nEnd of Lesson.")
