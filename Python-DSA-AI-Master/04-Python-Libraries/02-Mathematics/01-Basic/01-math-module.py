'''
Module: 01-math-module
Description: A comprehensive, textbook-grade interactive lesson on Python's `math` module.

===========================================================================
    PYTHON DSA & AI MASTERCLASS: THE MATH MODULE
===========================================================================

Learning Objectives:
1. Understand the core constants and functions provided by Python's `math` module.
2. Differentiate between built-in math operators and `math` module functions.
3. Master number-theoretic, power, logarithmic, and trigonometric operations.
4. Apply combinatorics and special functions (`math.comb`, `math.gamma`).
5. Analyze performance (Big-O, execution time) of `math` functions vs native operators.
6. Handle floating-point precision issues using `math.isclose` and `math.fsum`.
7. Solve classic technical interview challenges using mathematical optimizations.

Concept Explanation:
Python's built-in `math` module provides access to the mathematical functions defined 
by the C standard. It is a thin wrapper over the C math library, making its functions 
highly optimized and exceptionally fast.

Unlike native Python operations which can handle arbitrarily large integers, most 
functions in the `math` module return floating-point numbers and expect floats or 
values that can be converted to floats. 

Mathematical Background & Big-O:
- Most functions in `math` (like `sin`, `cos`, `exp`, `log`) execute in O(1) time complexity, 
  as they rely on CPU-level instructions or heavily optimized C-level approximations 
  (like Taylor series or CORDIC algorithms).
- `math.isqrt(n)` and `math.gcd(a, b)` are bounded by the size of the integers. 
  `math.gcd` uses the Euclidean algorithm which runs in O(log(min(a, b))) time.
- `math.comb(n, k)` takes O(k) time and space.

===========================================================================
'''

import math
import cmath
import time
import timeit
from typing import List, Tuple, Union, Optional

def section_header(title: str) -> None:
    """Helper to print formatted section headers."""
    print(f"\n{'='*70}\n {title.upper()} \n{'='*70}")


# =========================================================================
# 1. MATHEMATICAL CONSTANTS
# =========================================================================

def explore_constants() -> None:
    """
    Demonstrates the constants provided by the math module.
    
    Constants:
    - math.pi: The mathematical constant π = 3.141592..., to available precision.
    - math.e: The mathematical constant e = 2.718281..., to available precision.
    - math.tau: The mathematical constant τ = 6.283185... (2π).
    - math.inf: A floating-point positive infinity. (For negative infinity, use -math.inf).
    - math.nan: A floating-point "not a number" (NaN) value.
    """
    section_header("1. Mathematical Constants")
    
    print(f"PI (math.pi):      {math.pi}")
    print(f"Euler's e (math.e): {math.e}")
    print(f"Tau (math.tau):    {math.tau}  (Note: tau is exactly 2 * pi)")
    print(f"Infinity (math.inf): {math.inf}")
    print(f"NaN (math.nan):    {math.nan}")
    
    # Real-world application: Circle Circumference
    radius = 5.0
    circumference = math.tau * radius
    print(f"\nReal-world: Circumference of a circle with radius {radius} = {circumference:.4f}")
    
    # Understanding Infinity
    print(f"\nIs math.inf greater than 10^100? {math.inf > 10**100}")
    print(f"Negative Infinity: {-math.inf}")
    
    # Understanding NaN
    # NaN is never equal to anything, not even itself!
    print(f"Is math.nan == math.nan? {math.nan == math.nan}")
    print(f"Use math.isnan(math.nan) instead: {math.isnan(math.nan)}")


# =========================================================================
# 2. NUMBER-THEORETIC AND REPRESENTATION FUNCTIONS
# =========================================================================

def explore_number_theory() -> None:
    """
    Demonstrates number-theoretic functions: rounding, truncating, absolute values,
    and floating-point equality checks.
    """
    section_header("2. Number-Theoretic & Representation Functions")
    
    value = -3.7
    positive_val = 4.2
    
    print(f"Original Value: {value}")
    
    # math.ceil() returns the smallest integer >= x
    # math.floor() returns the largest integer <= x
    # math.trunc() truncates the Real x to the nearest Integral toward 0
    print(f"math.ceil({value})  -> {math.ceil(value)}")
    print(f"math.floor({value}) -> {math.floor(value)}")
    print(f"math.trunc({value}) -> {math.trunc(value)}")
    
    # Note how trunc behaves differently than floor for negative numbers:
    print(f"Notice: floor(-3.7) is -4, but trunc(-3.7) is -3 (moves towards 0)")
    
    # math.fabs() vs built-in abs()
    # math.fabs() always returns a float. Built-in abs() returns int if input is int.
    print(f"\nmath.fabs({value}) -> {math.fabs(value)} (Type: {type(math.fabs(value)).__name__})")
    print(f"abs(-5) -> {abs(-5)} (Type: {type(abs(-5)).__name__})")
    
    # math.copysign(x, y) returns a float with the magnitude (absolute value) of x but the sign of y.
    # Useful in algorithms that need to carry signs across calculations.
    print(f"\nmath.copysign(10.0, -1.0) -> {math.copysign(10.0, -1.0)}")
    
    # Greatest Common Divisor and Least Common Multiple
    # Available from Python 3.9+ for multiple arguments, traditionally 2 arguments.
    # Time Complexity: O(log(min(a, b)))
    a, b = 28, 35
    print(f"\nmath.gcd({a}, {b}) -> {math.gcd(a, b)}")
    print(f"math.lcm({a}, {b}) -> {math.lcm(a, b)}")
    
    # Floating Point Precision & math.isclose()
    # 0.1 + 0.2 in Python yields 0.30000000000000004
    f1 = 0.1 + 0.2
    f2 = 0.3
    print(f"\nFloating Point Math: 0.1 + 0.2 == {f1}")
    print(f"Does {f1} == {f2}? {f1 == f2}")
    
    # We use math.isclose to check equality of floats with a tolerance
    # Rel_tol is relative tolerance, abs_tol is absolute tolerance.
    is_equal = math.isclose(f1, f2, rel_tol=1e-9)
    print(f"math.isclose({f1}, {f2}) -> {is_equal}")


# =========================================================================
# 3. FLOATING POINT SUMMATION
# =========================================================================

def explore_fsum() -> None:
    """
    Demonstrates math.fsum() which returns an accurate floating point sum 
    of values in an iterable. It avoids loss of precision by tracking multiple 
    intermediate partial sums.
    """
    section_header("3. Accurate Summation (math.fsum)")
    
    # Consider a list of floats where adding them naively accumulates rounding errors
    values = [0.1] * 10
    
    native_sum = sum(values)
    math_sum = math.fsum(values)
    
    print(f"List of ten 0.1s: {values}")
    print(f"Built-in sum() result: {native_sum}")
    print(f"math.fsum() result:    {math_sum}")
    print("Why? math.fsum tracks intermediate sums to avoid loss of precision!")


# =========================================================================
# 4. POWER AND LOGARITHMIC FUNCTIONS
# =========================================================================

def explore_powers_and_logs() -> None:
    """
    Demonstrates exponentiation, square roots, and logarithms.
    """
    section_header("4. Power and Logarithmic Functions")
    
    # math.pow(x, y) computes x raised to the power y.
    # Note: math.pow() converts both arguments to float and returns a float.
    # The built-in ** operator returns an integer if inputs are integers.
    print(f"math.pow(2, 3) -> {math.pow(2, 3)} (Returns float)")
    print(f"2 ** 3         -> {2 ** 3} (Returns int)")
    
    # Square roots
    x = 1024
    print(f"\nmath.sqrt({x}) -> {math.sqrt(x)}")
    
    # Integer square root (Python 3.8+)
    # math.isqrt(n) returns the integer square root of the nonnegative integer n.
    # This is exactly equal to floor(sqrt(n)) but avoids float precision issues for large integers.
    large_n = 10**20
    print(f"math.isqrt({large_n}) -> {math.isqrt(large_n)}")
    
    # Exponentiation (e^x)
    print(f"\nmath.exp(2) (e^2) -> {math.exp(2)}")
    
    # Logarithms
    # math.log(x, [base]) -> natural log by default (base e)
    print(f"math.log(math.e)      -> {math.log(math.e)} (Natural log)")
    print(f"math.log(100, 10)     -> {math.log(100, 10)} (Log base 10)")
    
    # Faster base-specific logarithms:
    print(f"math.log10(100)       -> {math.log10(100)} (More accurate/faster than log(x, 10))")
    print(f"math.log2(32)         -> {math.log2(32)} (More accurate/faster than log(x, 2))")
    
    # Note on performance:
    # math.log2 and math.log10 directly call specialized C functions.


# =========================================================================
# 5. TRIGONOMETRIC AND ANGULAR FUNCTIONS
# =========================================================================

def explore_trigonometry() -> None:
    """
    Demonstrates trigonometric functions and angle conversions.
    """
    section_header("5. Trigonometric Functions")
    
    # Conversions
    deg = 180
    rad = math.radians(deg)
    print(f"{deg} degrees -> {rad} radians (which is math.pi: {math.pi})")
    print(f"{rad} radians -> {math.degrees(rad)} degrees")
    
    # Trigonometry expects radians!
    angle_30_deg = math.radians(30)
    print(f"\nmath.sin(30 degrees) -> {math.sin(angle_30_deg)}")
    print(f"math.cos(60 degrees) -> {math.cos(math.radians(60))}")
    print(f"math.tan(45 degrees) -> {math.tan(math.radians(45))}")
    
    # Inverse Trigonometry (returns radians)
    asin_val = math.asin(0.5)
    print(f"\nmath.asin(0.5) -> {asin_val} radians -> {math.degrees(asin_val)} degrees")
    
    # math.hypot() returns the Euclidean norm, sqrt(x*x + y*y).
    # Useful for finding distance between origin and point (x, y), or magnitude of vector.
    x, y = 3, 4
    print(f"math.hypot({x}, {y}) -> {math.hypot(x, y)} (Distance from origin to (3, 4))")
    
    # Multi-dimensional hypot (Python 3.8+)
    print(f"math.hypot(1, 2, 2) -> {math.hypot(1, 2, 2)} (Distance in 3D space)")


# =========================================================================
# 6. COMBINATORICS AND SPECIAL FUNCTIONS
# =========================================================================

def explore_combinatorics() -> None:
    """
    Demonstrates combinatorics (combinations, permutations) and the factorial function.
    """
    section_header("6. Combinatorics & Special Functions")
    
    # Factorial: Product of all positive integers less than or equal to n.
    n = 5
    print(f"math.factorial({n}) -> {math.factorial(n)} (5 * 4 * 3 * 2 * 1)")
    
    # math.comb(n, k): Number of ways to choose k items from n items without repetition and without order.
    # Formula: n! / (k! * (n-k)!)
    print(f"math.comb(10, 3) -> {math.comb(10, 3)} (Ways to choose 3 items from 10)")
    
    # math.perm(n, k): Number of ways to choose k items from n items without repetition and with order.
    # Formula: n! / (n-k)!
    print(f"math.perm(10, 3) -> {math.perm(10, 3)} (Ways to arrange 3 items out of 10)")
    
    # Gamma Function: math.gamma(x)
    # The gamma function is an extension of the factorial function to complex numbers.
    # For a positive integer n, Gamma(n) = (n-1)!
    print(f"\nmath.gamma(6) -> {math.gamma(6)} (Equivalent to factorial(5))")
    print(f"math.gamma(5.5) -> {math.gamma(5.5)} (Factorial for non-integers!)")


# =========================================================================
# 7. PERFORMANCE ANALYSIS (Big-O & Benchmarks)
# =========================================================================

def analyze_performance() -> None:
    """
    Compares the performance of math module functions vs built-in operators.
    """
    section_header("7. Performance Analysis")
    
    print("Running benchmarks (1 million iterations each)...")
    
    # Square root vs Exponentiation operator
    t_sqrt = timeit.timeit('math.sqrt(12345.6789)', setup='import math', number=1000000)
    t_pow  = timeit.timeit('12345.6789 ** 0.5', number=1000000)
    
    print(f"\nmath.sqrt()     : {t_sqrt:.5f} seconds")
    print(f"** 0.5 operator : {t_pow:.5f} seconds")
    if t_pow < t_sqrt:
         print("-> Built-in ** 0.5 is heavily optimized at compile-time in modern Python.")
    
    # Power vs Exponentiation operator for INTEGERS
    t_math_pow = timeit.timeit('math.pow(2, 20)', setup='import math', number=1000000)
    t_built_pow = timeit.timeit('2 ** 20', number=1000000)
    
    print(f"\nmath.pow(2, 20) : {t_math_pow:.5f} seconds")
    print(f"2 ** 20         : {t_built_pow:.5f} seconds")
    print("-> For pure integer math without function call overhead, ** is faster.")


# =========================================================================
# 8. INTERVIEW CHALLENGES
# =========================================================================

def is_prime_optimized(n: int) -> bool:
    """
    Interview Challenge 1: Check if a number is prime optimally.
    
    Naive approach: loop from 2 to n-1. (Time: O(N))
    Optimized approach: loop from 2 to int(math.sqrt(n)). (Time: O(sqrt(N)))
    Why? If N = a * b, one of the factors must be less than or equal to sqrt(N).
    
    Args:
        n: Integer to check
        
    Returns:
        True if prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    
    # Handle multiples of 2 and 3 specifically for a 6k +/- 1 optimization (optional but fast)
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    # We only need to check up to the square root of n
    limit = math.isqrt(n)
    
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
            
    return True


def my_sqrt(x: float, tolerance: float = 1e-7) -> float:
    """
    Interview Challenge 2: Implement your own square root function without using math.sqrt.
    
    Algorithm: Newton-Raphson Method (Babylonian method)
    Approximation formula: guess = (guess + x / guess) / 2
    
    Time Complexity: O(log N) precision bits. Extremely fast convergence.
    Space Complexity: O(1)
    """
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    if x == 0:
        return 0.0
        
    guess = x / 2.0  # Initial guess
    
    while True:
        next_guess = (guess + x / guess) / 2.0
        # If the difference is within our acceptable tolerance, we've found the root
        if abs(guess - next_guess) < tolerance:
            return next_guess
        guess = next_guess


def solve_interview_challenges() -> None:
    """Runs the interview challenge implementations."""
    section_header("8. Interview Challenges")
    
    print("Challenge 1: Primality Test O(sqrt(N))")
    primes_to_test = [2, 17, 18, 97, 100, 104729] # 104729 is the 10,000th prime
    for num in primes_to_test:
        print(f"is_prime_optimized({num:6}) -> {is_prime_optimized(num)}")
        
    print("\nChallenge 2: Implement sqrt() using Newton-Raphson Method")
    num_to_sqrt = 123456.789
    custom_res = my_sqrt(num_to_sqrt)
    math_res = math.sqrt(num_to_sqrt)
    
    print(f"Number to sqrt: {num_to_sqrt}")
    print(f"my_sqrt result:   {custom_res}")
    print(f"math.sqrt result: {math_res}")
    print(f"Difference:       {abs(custom_res - math_res):.10f}")


# =========================================================================
# 9. TEST SUITE
# =========================================================================

def run_tests() -> None:
    """
    Comprehensive test suite validating our implementations and understanding 
    of the math module. Uses `assert` to verify expected conditions.
    """
    section_header("9. Automated Test Suite")
    print("Running tests...")
    
    try:
        # Test 1: Number theory
        assert math.floor(-3.14) == -4, "math.floor handles negative numbers incorrectly"
        assert math.trunc(-3.14) == -3, "math.trunc handles negative numbers incorrectly"
        
        # Test 2: Floating point closeness
        assert math.isclose(0.1 + 0.2, 0.3), "Floating point math broke reality"
        
        # Test 3: Math summation
        assert math.isclose(math.fsum([0.1]*10), 1.0), "fsum failed to aggregate correctly"
        
        # Test 4: Trigonometry
        assert math.isclose(math.sin(math.pi / 2), 1.0), "sin(90deg) should be 1"
        assert math.isclose(math.cos(math.pi), -1.0), "cos(180deg) should be -1"
        
        # Test 5: Custom implementations (Interview challenges)
        assert is_prime_optimized(97) is True, "Primality test failed for prime"
        assert is_prime_optimized(100) is False, "Primality test failed for composite"
        assert math.isclose(my_sqrt(144), 12.0), "Custom sqrt failed"
        
        print("✅ All test cases passed successfully!")
    
    except AssertionError as ae:
        print(f"❌ Test Suite Failed: {ae}")
        
    print("\n")


# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    print("\n" + "#" * 70)
    print("   WELCOME TO THE PYTHON MATH MODULE MASTERCLASS   ")
    print("#" * 70)
    
    # 1. Constants
    explore_constants()
    
    # 2. Number theory
    explore_number_theory()
    
    # 3. fsum
    explore_fsum()
    
    # 4. Powers and logs
    explore_powers_and_logs()
    
    # 5. Trigonometry
    explore_trigonometry()
    
    # 6. Combinatorics
    explore_combinatorics()
    
    # 7. Performance Benchmarks
    analyze_performance()
    
    # 8. Interview Challenges
    solve_interview_challenges()
    
    # 9. Tests
    run_tests()
    
    print("=" * 70)
    print("   LESSON COMPLETED. MASTERING 'math' IS CRITICAL FOR ALGORITHMS.   ")
    print("=" * 70 + "\n")
