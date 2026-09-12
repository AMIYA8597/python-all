"""
Module: 04-advanced-math
Description: Comprehensive textbook-grade lesson on Advanced Mathematics in Python.

===========================================================================
Python Advanced Mathematics: A Deep Dive
===========================================================================

Learning Objectives:
1. Understand and utilize Python's advanced standard library math features.
2. Master high-precision arithmetic using `decimal` and `fractions`.
3. Explore complex number mathematics using the `cmath` module.
4. Analyze mathematical algorithms, particularly their Time & Space Complexity (Big-O).
5. Apply these concepts to solve real-world problems like cryptography and finance.

Mathematical Background:
------------------------
Python provides several built-in modules for mathematical operations beyond basic arithmetic.

1. Combinatorics and Special Functions (math)
   - Permutations (P(n, k) = n! / (n-k)!) and Combinations (C(n, k) = n! / (k!(n-k)!))
   - Gamma function (Γ(n) = (n-1)!) - generalization of factorial for real/complex numbers.
   - Error function (erf(x)) - used in probability and statistics.

2. High-Precision Arithmetic (decimal, fractions)
   - Floating-point arithmetic (IEEE 754) introduces precision errors (e.g., 0.1 + 0.2 != 0.3).
   - `Decimal` provides arbitrary precision, essential for financial calculations.
   - `Fraction` provides exact rational number representation (p/q).

3. Complex Numbers (cmath)
   - Numbers in the form z = a + bj, where j = sqrt(-1).
   - Polar coordinate representation: z = r * e^(iθ).

4. Modular Arithmetic
   - Fast exponentiation `pow(base, exp, mod)` solves (base^exp) % mod in O(log(exp)) time.

Big-O Analysis:
---------------
- math.comb(n, k): O(k) time complexity, O(1) space.
- math.gcd(a, b): O(log(min(a, b))) time complexity (Euclidean algorithm).
- Fast Modular Exponentiation (pow): O(log(exp)) time complexity.
"""

import math
import cmath
import decimal
import time
from fractions import Fraction
from typing import List, Tuple, Union, Optional


# ============================================================================
# 1. SPECIAL FUNCTIONS & COMBINATORICS (math)
# ============================================================================

def calculate_probability_of_winning(n_total: int, k_choices: int) -> float:
    """
    Calculates the probability of winning a lottery where you must choose
    `k_choices` correct numbers out of `n_total` possible numbers.

    Mathematical Concept:
    Combinations determine the number of ways to choose k items from n items without replacement
    and without regard to order. Formula: C(n, k) = n! / (k!(n-k)!)

    Time Complexity: O(min(k, n-k)) - Python's math.comb is optimized in C.
    Space Complexity: O(1)

    Args:
        n_total: Total number of available choices.
        k_choices: Number of choices required to win.

    Returns:
        float: The probability of winning.
    """
    # Edge cases
    if k_choices > n_total or k_choices < 0 or n_total <= 0:
        return 0.0

    # Calculate total possible combinations
    total_combinations = math.comb(n_total, k_choices)
    
    # Probability is 1 over the total number of combinations
    probability = 1.0 / total_combinations
    return probability


def compute_gamma_and_factorial(n: float) -> Tuple[float, float]:
    """
    Demonstrates the relationship between the Gamma function and Factorial.
    Γ(n) = (n-1)! for positive integers.

    Args:
        n: A real number (preferably an integer > 0 for factorial comparison).

    Returns:
        Tuple[float, float]: (gamma_value, factorial_value)
    """
    gamma_val = math.gamma(n)
    
    # math.factorial only works on integers. We approximate if it's a float.
    if n.is_integer() and n > 0:
        fact_val = float(math.factorial(int(n) - 1))
    else:
        fact_val = float('nan') # Factorial is undefined for non-integers in standard math
        
    return gamma_val, fact_val


# ============================================================================
# 2. HIGH-PRECISION ARITHMETIC (decimal & fractions)
# ============================================================================

def financial_calculation_example(principal: str, rate: str, years: int) -> decimal.Decimal:
    """
    Calculates compound interest precisely using the Decimal module.
    Formula: A = P * (1 + R)^t
    
    Why Decimal?
    Floating point precision issues can lead to penny discrepancies in financial software.
    Decimal ensures exact base-10 arithmetic.

    Time Complexity: O(log(years)) for the exponentiation.
    Space Complexity: O(1)

    Args:
        principal: Starting amount as a string (to avoid initial float conversion loss).
        rate: Annual interest rate as a string.
        years: Number of years.

    Returns:
        decimal.Decimal: Final amount.
    """
    # Set the precision to 28 decimal places (default)
    decimal.getcontext().prec = 28
    
    p_dec = decimal.Decimal(principal)
    r_dec = decimal.Decimal(rate)
    
    # Calculate compounded amount
    amount = p_dec * ((decimal.Decimal('1') + r_dec) ** years)
    
    # Quantize to 2 decimal places (standard for currency)
    return amount.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)


def precise_fraction_operations() -> Tuple[Fraction, float]:
    """
    Demonstrates the difference between Fraction and float addition.
    Adding 1/3 three times should equal exactly 1.
    """
    # Fraction approach (Exact)
    f1 = Fraction(1, 3)
    frac_sum = f1 + f1 + f1
    
    # Float approach (Subject to floating point representation error)
    fl1 = 1 / 3
    float_sum = fl1 + fl1 + fl1
    
    return frac_sum, float_sum


# ============================================================================
# 3. COMPLEX NUMBERS (cmath)
# ============================================================================

def solve_quadratic(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """
    Solves a quadratic equation ax^2 + bx + c = 0, supporting complex roots.
    
    Mathematical Concept:
    Discriminant Δ = b^2 - 4ac. 
    If Δ < 0, the roots are complex conjugates. `cmath.sqrt` handles negative inputs seamlessly.

    Time Complexity: O(1)
    Space Complexity: O(1)

    Args:
        a: Coefficient of x^2 (must be non-zero).
        b: Coefficient of x.
        c: Constant term.

    Returns:
        Tuple[complex, complex]: The two roots of the quadratic equation.
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation.")
        
    discriminant = (b ** 2) - (4 * a * c)
    
    # Use cmath.sqrt to automatically handle negative discriminants
    sqrt_val = cmath.sqrt(discriminant)
    
    root1 = (-b + sqrt_val) / (2 * a)
    root2 = (-b - sqrt_val) / (2 * a)
    
    return root1, root2


def complex_polar_conversion(z: complex) -> Tuple[float, float]:
    """
    Converts a complex number from rectangular (x + yj) to polar (r, theta) coordinates.
    
    Returns:
        Tuple[float, float]: (modulus r, phase theta in radians).
    """
    return cmath.polar(z)


# ============================================================================
# 4. ALGORITHMIC PERFORMANCE (Fast Exponentiation)
# ============================================================================

def fast_modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Computes (base^exponent) % modulus efficiently.
    
    Real-world Application:
    This is the core of RSA cryptography. When exponents are very large (e.g., 2048 bits),
    computing base^exponent directly and then taking the modulus is impossible due to memory limits.
    Fast modular exponentiation keeps the numbers small at each step.

    Big-O Analysis:
    Time Complexity: O(log(exponent))
    Space Complexity: O(1)

    Args:
        base: The base integer.
        exponent: The exponent integer.
        modulus: The modulo integer.

    Returns:
        int: The result.
    """
    # Python's built-in pow() with 3 arguments uses this exact O(log N) algorithm under the hood.
    return pow(base, exponent, modulus)


# ============================================================================
# INTERVIEW CHALLENGE
# ============================================================================

def interview_challenge_gcd_lcm(numbers: List[int]) -> Tuple[int, int]:
    """
    Challenge: Given an array of integers, compute their Greatest Common Divisor (GCD)
               and Least Common Multiple (LCM).

    Mathematical Concept:
    - GCD of multiple numbers can be found by reducing the list: gcd(a, b, c) = gcd(gcd(a, b), c).
    - LCM(a, b) = abs(a * b) // gcd(a, b).
    
    Time Complexity: O(N * log(min_val)) where N is the length of the list.
    Space Complexity: O(1)

    Args:
        numbers: List of positive integers.

    Returns:
        Tuple[int, int]: (GCD of all numbers, LCM of all numbers)
    """
    if not numbers:
        return 0, 0
        
    current_gcd = numbers[0]
    current_lcm = numbers[0]
    
    for i in range(1, len(numbers)):
        num = numbers[i]
        # Update GCD
        current_gcd = math.gcd(current_gcd, num)
        # Update LCM using the relationship LCM(a, b) = (a * b) // GCD(a, b)
        # Note: math.lcm is available in Python 3.9+, but doing it manually is a good exercise.
        current_lcm = (current_lcm * num) // math.gcd(current_lcm, num)
        
    return current_gcd, current_lcm


# ============================================================================
# TESTS & EXECUTION
# ============================================================================

def run_tests() -> None:
    """
    Exhaustive test suite to validate all mathematical functions.
    """
    print("--- Running Advanced Math Tests ---")
    
    # 1. Combinatorics Test
    prob = calculate_probability_of_winning(69, 5) # Powerball odds (roughly)
    assert 0 < prob < 1e-7, "Probability calculation failed"
    print("[\u2713] Combinatorics Test Passed.")
    
    # 2. Gamma Function Test
    gamma_v, fact_v = compute_gamma_and_factorial(5.0)
    assert math.isclose(gamma_v, fact_v), "Gamma/Factorial equality failed for integers"
    print("[\u2713] Gamma Function Test Passed.")
    
    # 3. High Precision Test
    fin_res = financial_calculation_example("1000.00", "0.05", 10)
    assert fin_res == decimal.Decimal("1628.89"), "Financial compound interest calculation failed"
    print("[\u2713] Decimal Financial Test Passed.")
    
    frac_res, float_res = precise_fraction_operations()
    assert frac_res == Fraction(1, 1), "Fraction exact representation failed"
    print("[\u2713] Fraction Representation Test Passed.")
    
    # 4. Complex Numbers Test
    r1, r2 = solve_quadratic(1, 0, 1) # x^2 + 1 = 0 => x = i, -i
    assert cmath.isclose(r1, 1j) or cmath.isclose(r1, -1j), "Quadratic complex root failed"
    print("[\u2713] Complex Quadratic Test Passed.")
    
    # 5. Fast Exponentiation Test
    # 2^10 % 1000 = 1024 % 1000 = 24
    mod_res = fast_modular_exponentiation(2, 10, 1000)
    assert mod_res == 24, "Fast modular exponentiation failed"
    print("[\u2713] Modular Exponentiation Test Passed.")
    
    # 6. Interview Challenge Test
    g, l = interview_challenge_gcd_lcm([12, 18, 24])
    assert g == 6, "GCD failed"
    assert l == 72, "LCM failed"
    print("[\u2713] Interview Challenge (GCD/LCM) Test Passed.")
    
    print("All tests passed successfully!\n")


if __name__ == "__main__":
    print(f"{'='*60}")
    print(" EXPLORING PYTHON ADVANCED MATHEMATICS ")
    print(f"{'='*60}\n")
    
    # 1. Combinatorics
    print("--- 1. Combinatorics (math.comb) ---")
    n_total, k_choices = 50, 5
    p_win = calculate_probability_of_winning(n_total, k_choices)
    print(f"Probability of matching {k_choices} from {n_total}: {p_win:.8f} (1 in {int(1/p_win)})\n")
    
    # 2. Decimal Mathematics
    print("--- 2. High-Precision Finance (decimal) ---")
    principal, rate, years = "10000.00", "0.08", 30
    final_amount = financial_calculation_example(principal, rate, years)
    print(f"Investing ${principal} at {float(rate)*100}% for {years} years yields: ${final_amount}\n")
    
    # 3. Complex Roots
    print("--- 3. Complex Number Roots (cmath) ---")
    eq_a, eq_b, eq_c = 1, -4, 5  # x^2 - 4x + 5 = 0
    root_a, root_b = solve_quadratic(eq_a, eq_b, eq_c)
    print(f"Roots of {eq_a}x^2 + {eq_b}x + {eq_c} = 0 are:")
    print(f"  Root 1: {root_a}")
    print(f"  Root 2: {root_b}\n")
    
    # 4. Cryptography Primitive
    print("--- 4. Cryptographic Exponentiation (pow) ---")
    base, exp, mod = 5, 1_000_000, 1000000007
    start = time.time()
    crypto_result = fast_modular_exponentiation(base, exp, mod)
    end = time.time()
    print(f"Result of ({base}^{exp}) % {mod} = {crypto_result}")
    print(f"Computed in {(end - start):.6f} seconds (O(log(N)) performance)\n")
    
    # 5. Tests
    run_tests()
    
    print(f"{'='*60}")
    print(" END OF ADVANCED MATHEMATICS LESSON ")
    print(f"{'='*60}\n")
