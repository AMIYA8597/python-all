#!/usr/bin/env python3
"""
Python Operators and Expressions - Comprehensive Guide
=====================================================

This module demonstrates Python's operators and expressions with detailed
explanations, performance analysis, and real-world applications.

Topics Covered:
- Arithmetic operators with precision considerations
- Comparison operators and their behavior
- Logical operators and short-circuiting
- Bitwise operations and practical uses
- Assignment operators and in-place operations
- Operator precedence and evaluation order
- Special operators (is, in, walrus :=)
- Performance benchmarks and optimizations

Author: Python DSA Master Course
Version: 1.0
"""

import operator
import timeit
import sys
from typing import Union, Any, List, Dict
from decimal import Decimal, getcontext
from fractions import Fraction
import math
import cmath  # Complex math


# ============================================================================
# SECTION 1: ARITHMETIC OPERATORS
# ============================================================================

def arithmetic_operators_demo():
    """
    Comprehensive demonstration of arithmetic operators with edge cases.
    """
    print("=== ARITHMETIC OPERATORS DEMO ===")
    
    # Basic arithmetic
    a, b = 17, 5
    print(f"a = {a}, b = {b}")
    print(f"Addition: {a} + {b} = {a + b}")
    print(f"Subtraction: {a} - {b} = {a - b}")
    print(f"Multiplication: {a} * {b} = {a * b}")
    print(f"Division: {a} / {b} = {a / b}")
    print(f"Floor division: {a} // {b} = {a // b}")
    print(f"Modulo: {a} % {b} = {a % b}")
    print(f"Exponentiation: {a} ** {b} = {a ** b}")
    
    # Divmod - efficient way to get quotient and remainder
    quotient, remainder = divmod(a, b)
    print(f"divmod({a}, {b}) = ({quotient}, {remainder})")
    
    # Precision considerations
    print(f"\n=== PRECISION CONSIDERATIONS ===")
    
    # Float precision issues
    print(f"0.1 + 0.2 = {0.1 + 0.2}")
    print(f"0.1 + 0.2 == 0.3: {0.1 + 0.2 == 0.3}")
    
    # Using Decimal for exact precision
    getcontext().prec = 10
    d1, d2 = Decimal('0.1'), Decimal('0.2')
    print(f"Decimal('0.1') + Decimal('0.2') = {d1 + d2}")
    print(f"Decimal sum == Decimal('0.3'): {d1 + d2 == Decimal('0.3')}")
    
    # Using fractions for exact rational arithmetic
    f1, f2 = Fraction(1, 10), Fraction(2, 10)
    print(f"Fraction(1,10) + Fraction(2,10) = {f1 + f2}")
    
    # Complex number arithmetic
    c1, c2 = 3 + 4j, 1 + 2j
    print(f"\nComplex: ({c1}) + ({c2}) = {c1 + c2}")
    print(f"Complex magnitude: |{c1}| = {abs(c1)}")
    print(f"Complex conjugate: {c1}* = {c1.conjugate()}")
    
    # Large integer arithmetic (Python handles arbitrary precision)
    big1, big2 = 10**100, 2**200
    print(f"\nBig integer operations:")
    print(f"10^100 digits: {len(str(big1))}")
    print(f"2^200 digits: {len(str(big2))}")
    print(f"Product has {len(str(big1 * big2))} digits")


def arithmetic_edge_cases():
    """
    Demonstrate edge cases and special behaviors.
    """
    print(f"\n=== ARITHMETIC EDGE CASES ===")
    
    # Division by zero
    try:
        result = 5 / 0
    except ZeroDivisionError as e:
        print(f"Division by zero: {e}")
    
    # Float special values
    print(f"Infinity: {float('inf')}")
    print(f"Negative infinity: {float('-inf')}")
    print(f"NaN (Not a Number): {float('nan')}")
    
    inf = float('inf')
    print(f"inf + 1 = {inf + 1}")
    print(f"inf > 1000000 = {inf > 1000000}")
    print(f"inf == inf = {inf == inf}")
    
    nan = float('nan')
    print(f"nan == nan = {nan == nan}")  # Always False!
    print(f"math.isnan(nan) = {math.isnan(nan)}")
    
    # Modulo with negative numbers
    print(f"\nModulo with negatives:")
    print(f"17 % 5 = {17 % 5}")
    print(f"-17 % 5 = {-17 % 5}")  # Result has same sign as divisor
    print(f"17 % -5 = {17 % -5}")
    print(f"-17 % -5 = {-17 % -5}")
    
    # Floor division behavior
    print(f"\nFloor division behavior:")
    print(f"17 // 5 = {17 // 5}")
    print(f"-17 // 5 = {-17 // 5}")  # Always rounds toward negative infinity
    print(f"17 // -5 = {17 // -5}")
    print(f"-17 // -5 = {-17 // -5}")


# ============================================================================
# SECTION 2: COMPARISON OPERATORS
# ============================================================================

def comparison_operators_demo():
    """
    Comprehensive demonstration of comparison operators.
    """
    print(f"\n=== COMPARISON OPERATORS DEMO ===")
    
    # Basic comparisons
    a, b, c = 5, 10, 5
    print(f"a={a}, b={b}, c={c}")
    print(f"a == c: {a == c}")
    print(f"a != b: {a != b}")
    print(f"a < b: {a < b}")
    print(f"a <= c: {a <= c}")
    print(f"b > a: {b > a}")
    print(f"b >= a: {b >= a}")
    
    # Chained comparisons
    print(f"\nChained comparisons:")
    x = 15
    print(f"10 < {x} < 20: {10 < x < 20}")
    print(f"10 < {x} <= 15: {10 < x <= 15}")
    print(f"5 <= {x} <= 10: {5 <= x <= 10}")
    
    # Comparison of different types
    print(f"\nType comparisons:")
    print(f"5 == 5.0: {5 == 5.0}")  # True - numeric equality
    print(f"5 is 5.0: {5 is 5.0}")  # False - different objects
    
    # String comparisons (lexicographic)
    s1, s2 = "apple", "banana"
    print(f"'{s1}' < '{s2}': {s1 < s2}")
    print(f"'{s1}' == '{s1.upper().lower()}': {s1 == s1.upper().lower()}")
    
    # List/tuple comparisons (element-wise)
    list1, list2 = [1, 2, 3], [1, 2, 4]
    print(f"{list1} < {list2}: {list1 < list2}")
    
    tuple1, tuple2 = (1, 2), (1, 2, 0)
    print(f"{tuple1} < {tuple2}: {tuple1 < tuple2}")


def identity_and_membership():
    """
    Demonstrate identity (is) and membership (in) operators.
    """
    print(f"\n=== IDENTITY AND MEMBERSHIP OPERATORS ===")
    
    # Identity operator (is)
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    print(f"a = {a}, b = {b}, c = a")
    print(f"a == b: {a == b}")  # True - same content
    print(f"a is b: {a is b}")  # False - different objects
    print(f"a is c: {a is c}")  # True - same object
    
    # Small integer caching
    x = 256
    y = 256
    print(f"\nInteger caching (small integers):")
    print(f"{x} is {y}: {x is y}")  # True - cached
    
    x = 257
    y = 257
    print(f"{x} is {y}: {x is y}")  # Implementation dependent
    
    # None comparisons
    value = None
    print(f"\nNone comparisons:")
    print(f"value is None: {value is None}")  # Correct way
    print(f"value == None: {value == None}")  # Works but not recommended
    
    # Membership operator (in)
    numbers = [1, 2, 3, 4, 5]
    text = "Hello World"
    
    print(f"\nMembership tests:")
    print(f"3 in {numbers}: {3 in numbers}")
    print(f"6 not in {numbers}: {6 not in numbers}")
    print(f"'Hello' in '{text}': {'Hello' in text}")
    print(f"'xyz' not in '{text}': {'xyz' not in text}")
    
    # Dictionary membership (checks keys)
    person = {'name': 'Alice', 'age': 25}
    print(f"'name' in {person}: {'name' in person}")
    print(f"'Alice' in {person}: {'Alice' in person}")  # False - checks keys, not values


# ============================================================================
# SECTION 3: LOGICAL OPERATORS
# ============================================================================

def logical_operators_demo():
    """
    Demonstrate logical operators with short-circuiting behavior.
    """
    print(f"\n=== LOGICAL OPERATORS DEMO ===")
    
    # Basic logical operations
    p, q = True, False
    print(f"p={p}, q={q}")
    print(f"p and q: {p and q}")
    print(f"p or q: {p or q}")
    print(f"not p: {not p}")
    print(f"not q: {not q}")
    
    # Truthiness of different values
    print(f"\nTruthiness of values:")
    values = [0, 1, [], [1], "", "hello", None, {}, {"key": "value"}]
    for val in values:
        print(f"bool({repr(val)}): {bool(val)}")
    
    # Short-circuiting behavior
    print(f"\nShort-circuiting demonstration:")
    
    def side_effect(value, name):
        """Function with side effect to demonstrate short-circuiting."""
        print(f"  Evaluating {name}: {value}")
        return value
    
    print("False and side_effect(True, 'second'):")
    result = False and side_effect(True, 'second')  # second not evaluated
    print(f"  Result: {result}")
    
    print("True or side_effect(False, 'second'):")
    result = True or side_effect(False, 'second')  # second not evaluated
    print(f"  Result: {result}")
    
    # Chained logical operations
    print(f"\nChained logical operations:")
    x, y, z = 5, 0, 10
    print(f"x={x}, y={y}, z={z}")
    print(f"x and y and z: {x and y and z}")  # Returns 0 (first falsy)
    print(f"x or y or z: {x or y or z}")     # Returns 5 (first truthy)
    
    # Logical operators return operands, not just True/False
    print(f"\nLogical operators return operands:")
    print(f"'hello' and 'world': {'hello' and 'world'}")
    print(f"'' or 'default': {'' or 'default'}")
    print(f"None or 0 or 'fallback': {None or 0 or 'fallback'}")


def practical_logical_patterns():
    """
    Demonstrate practical patterns using logical operators.
    """
    print(f"\n=== PRACTICAL LOGICAL PATTERNS ===")
    
    # Default value pattern
    def greet(name=None):
        name = name or "Guest"  # Use 'Guest' if name is falsy
        return f"Hello, {name}!"
    
    print(f"greet(): {greet()}")
    print(f"greet('Alice'): {greet('Alice')}")
    print(f"greet(''): {greet('')}")  # Empty string is falsy
    
    # Guard clause pattern
    def divide(a, b):
        # Guard against division by zero
        b != 0 or print("Warning: Division by zero!")
        return a / b if b != 0 else float('inf')
    
    print(f"divide(10, 2): {divide(10, 2)}")
    print(f"divide(10, 0): {divide(10, 0)}")
    
    # Chained validation
    def validate_user(user_data):
        return (
            user_data and 
            user_data.get('name') and
            user_data.get('email') and
            '@' in user_data.get('email', '')
        )
    
    valid_user = {'name': 'Alice', 'email': 'alice@example.com'}
    invalid_user = {'name': '', 'email': 'invalid'}
    
    print(f"validate_user({valid_user}): {validate_user(valid_user)}")
    print(f"validate_user({invalid_user}): {validate_user(invalid_user)}")


# ============================================================================
# SECTION 4: BITWISE OPERATORS
# ============================================================================

def bitwise_operators_demo():
    """
    Comprehensive demonstration of bitwise operators and applications.
    """
    print(f"\n=== BITWISE OPERATORS DEMO ===")
    
    # Basic bitwise operations
    a, b = 60, 13  # 111100, 1101 in binary
    print(f"a = {a} (binary: {bin(a)})")
    print(f"b = {b} (binary: {bin(b)})")
    print(f"a & b = {a & b} (binary: {bin(a & b)})  # AND")
    print(f"a | b = {a | b} (binary: {bin(a | b)})  # OR")
    print(f"a ^ b = {a ^ b} (binary: {bin(a ^ b)})  # XOR")
    print(f"~a = {~a} (binary: {bin(~a & 0xFF)})     # NOT (8-bit)")
    print(f"a << 2 = {a << 2} (binary: {bin(a << 2)}) # Left shift")
    print(f"a >> 2 = {a >> 2} (binary: {bin(a >> 2)}) # Right shift")
    
    # Practical bitwise applications
    print(f"\n=== PRACTICAL BITWISE APPLICATIONS ===")
    
    # Power of 2 check
    def is_power_of_2(n):
        return n > 0 and (n & (n - 1)) == 0
    
    test_numbers = [1, 2, 3, 4, 8, 15, 16, 32]
    print(f"Power of 2 check:")
    for num in test_numbers:
        print(f"  {num}: {is_power_of_2(num)}")
    
    # Bit manipulation for flags
    class Permissions:
        READ = 1    # 001
        WRITE = 2   # 010
        EXECUTE = 4 # 100
    
    # Set permissions using OR
    user_perms = Permissions.READ | Permissions.WRITE
    print(f"\nPermissions demo:")
    print(f"User permissions: {user_perms} (binary: {bin(user_perms)})")
    print(f"Has READ: {bool(user_perms & Permissions.READ)}")
    print(f"Has WRITE: {bool(user_perms & Permissions.WRITE)}")
    print(f"Has EXECUTE: {bool(user_perms & Permissions.EXECUTE)}")
    
    # Toggle permission using XOR
    user_perms ^= Permissions.EXECUTE  # Toggle execute permission
    print(f"After toggling EXECUTE: {user_perms} (binary: {bin(user_perms)})")
    print(f"Has EXECUTE: {bool(user_perms & Permissions.EXECUTE)}")
    
    # Remove permission using AND NOT
    user_perms &= ~Permissions.WRITE  # Remove write permission
    print(f"After removing WRITE: {user_perms} (binary: {bin(user_perms)})")
    print(f"Has WRITE: {bool(user_perms & Permissions.WRITE)}")


def bit_tricks_and_optimizations():
    """
    Demonstrate useful bit manipulation tricks and optimizations.
    """
    print(f"\n=== BIT TRICKS AND OPTIMIZATIONS ===")
    
    # Fast multiplication and division by powers of 2
    n = 42
    print(f"n = {n}")
    print(f"n * 4 = {n * 4} vs n << 2 = {n << 2}")
    print(f"n / 8 = {n / 8} vs n >> 3 = {n >> 3}")
    
    # Swap two numbers without temporary variable
    a, b = 15, 27
    print(f"\nSwapping without temp variable:")
    print(f"Before: a={a}, b={b}")
    a = a ^ b
    b = a ^ b
    a = a ^ b
    print(f"After XOR swap: a={a}, b={b}")
    
    # Count set bits (population count)
    def count_set_bits(n):
        count = 0
        while n:
            count += n & 1
            n >>= 1
        return count
    
    def count_set_bits_builtin(n):
        return bin(n).count('1')
    
    test_num = 170  # 10101010
    print(f"\nCounting set bits in {test_num} ({bin(test_num)}):")
    print(f"Manual count: {count_set_bits(test_num)}")
    print(f"Built-in count: {count_set_bits_builtin(test_num)}")
    
    # Find rightmost set bit
    def rightmost_set_bit(n):
        return n & (-n)
    
    print(f"\nRightmost set bit:")
    for num in [12, 20, 16]:  # 1100, 10100, 10000
        rsb = rightmost_set_bit(num)
        print(f"{num} ({bin(num)}): rightmost set bit = {rsb} ({bin(rsb)})")
    
    # Check if number is even/odd (faster than modulo)
    def is_even_bitwise(n):
        return (n & 1) == 0
    
    print(f"\nEven/odd check using bitwise:")
    for num in range(10):
        print(f"{num}: {'even' if is_even_bitwise(num) else 'odd'}")


# ============================================================================
# SECTION 5: ASSIGNMENT OPERATORS
# ============================================================================

def assignment_operators_demo():
    """
    Demonstrate assignment operators and their behaviors.
    """
    print(f"\n=== ASSIGNMENT OPERATORS DEMO ===")
    
    # Basic assignment
    x = 10
    print(f"x = {x}")
    
    # Compound assignment operators
    x += 5   # x = x + 5
    print(f"After x += 5: x = {x}")
    
    x -= 3   # x = x - 3
    print(f"After x -= 3: x = {x}")
    
    x *= 2   # x = x * 2
    print(f"After x *= 2: x = {x}")
    
    x /= 4   # x = x / 4
    print(f"After x /= 4: x = {x}")
    
    x //= 2  # x = x // 2
    print(f"After x //= 2: x = {x}")
    
    x %= 3   # x = x % 3
    print(f"After x %= 3: x = {x}")
    
    x **= 3  # x = x ** 3
    print(f"After x **= 3: x = {x}")
    
    # Bitwise assignment operators
    y = 60  # 111100
    print(f"\nBitwise assignments (starting with y = {y}):")
    
    y &= 13  # y = y & 13
    print(f"After y &= 13: y = {y}")
    
    y |= 8   # y = y | 8
    print(f"After y |= 8: y = {y}")
    
    y ^= 5   # y = y ^ 5
    print(f"After y ^= 5: y = {y}")
    
    y <<= 1  # y = y << 1
    print(f"After y <<= 1: y = {y}")
    
    y >>= 2  # y = y >> 2
    print(f"After y >>= 2: y = {y}")


def walrus_operator_demo():
    """
    Demonstrate the walrus operator (:=) introduced in Python 3.8.
    """
    print(f"\n=== WALRUS OPERATOR (:=) DEMO ===")
    
    # Basic walrus operator usage
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Traditional approach
    print("Traditional approach:")
    filtered = [x for x in data if x > 5]
    print(f"Filtered: {filtered}")
    
    # Using walrus operator for complex expressions
    print(f"\nUsing walrus operator:")
    # Process each number and keep track of the processed value
    results = []
    for x in data:
        if (processed := x ** 2) > 25:  # Square and check if > 25
            results.append(processed)
    print(f"Squared values > 25: {results}")
    
    # Walrus in list comprehensions
    squares_gt_25 = [y for x in data if (y := x ** 2) > 25]
    print(f"List comprehension with walrus: {squares_gt_25}")
    
    # Walrus in while loops
    print(f"\nWalrus in while loop:")
    import random
    random.seed(42)  # For reproducible results
    
    numbers = []
    while (num := random.randint(1, 100)) != 50:  # Generate until we get 50
        numbers.append(num)
        if len(numbers) >= 10:  # Prevent infinite loop for demo
            break
    print(f"Generated numbers: {numbers}")
    print(f"Last number: {num}")
    
    # Practical example: file processing
    print(f"\nPractical walrus usage pattern:")
    # Simulating reading lines from a file
    lines = ["line1", "line2", "", "line4", "", "line6"]
    
    # Process non-empty lines
    processed_lines = []
    for line in lines:
        if (stripped := line.strip()):  # Strip and check if non-empty
            processed_lines.append(stripped.upper())
    
    print(f"Processed lines: {processed_lines}")


# ============================================================================
# SECTION 6: OPERATOR PRECEDENCE AND EVALUATION
# ============================================================================

def operator_precedence_demo():
    """
    Demonstrate operator precedence and evaluation order.
    """
    print(f"\n=== OPERATOR PRECEDENCE DEMO ===")
    
    # Precedence examples
    result1 = 2 + 3 * 4
    result2 = (2 + 3) * 4
    print(f"2 + 3 * 4 = {result1}")
    print(f"(2 + 3) * 4 = {result2}")
    
    result3 = 2 ** 3 ** 2  # Right associative
    result4 = (2 ** 3) ** 2
    print(f"2 ** 3 ** 2 = {result3} (right associative)")
    print(f"(2 ** 3) ** 2 = {result4}")
    
    # Complex precedence example
    expr = 2 + 3 * 4 ** 2 // 3 - 1
    step_by_step = (
        f"2 + 3 * 4 ** 2 // 3 - 1\n"
        f"2 + 3 * 16 // 3 - 1     # 4 ** 2 = 16\n"
        f"2 + 48 // 3 - 1         # 3 * 16 = 48\n"
        f"2 + 16 - 1              # 48 // 3 = 16\n"
        f"18 - 1                  # 2 + 16 = 18\n"
        f"17                      # Final result"
    )
    print(f"\nComplex expression evaluation:")
    print(step_by_step)
    print(f"Result: {expr}")
    
    # Operator precedence table (highest to lowest)
    precedence_table = """
    Operator Precedence (Highest to Lowest):
    1. () [] {}                    # Parentheses, indexing, calls
    2. **                          # Exponentiation (right associative)
    3. +x -x ~x                    # Unary plus, minus, bitwise NOT
    4. * / // %                    # Multiplication, division, modulo
    5. + -                         # Addition, subtraction
    6. << >>                       # Bitwise shifts
    7. &                           # Bitwise AND
    8. ^                           # Bitwise XOR
    9. |                           # Bitwise OR
    10. == != < > <= >= is in      # Comparisons, identity, membership
    11. not                        # Boolean NOT
    12. and                        # Boolean AND
    13. or                         # Boolean OR
    14. :=                         # Assignment expressions (walrus)
    """
    print(precedence_table)


def evaluation_order_and_side_effects():
    """
    Demonstrate evaluation order and side effects.
    """
    print(f"\n=== EVALUATION ORDER AND SIDE EFFECTS ===")
    
    # Function calls with side effects
    call_order = []
    
    def func_a():
        call_order.append('A')
        return 1
    
    def func_b():
        call_order.append('B')
        return 2
    
    def func_c():
        call_order.append('C')
        return 3
    
    # Expression evaluation order
    call_order.clear()
    result = func_a() + func_b() * func_c()
    print(f"func_a() + func_b() * func_c() = {result}")
    print(f"Call order: {call_order}")
    
    # Short-circuiting affects evaluation
    call_order.clear()
    result = func_a() or func_b() and func_c()
    print(f"func_a() or func_b() and func_c() = {result}")
    print(f"Call order with short-circuit: {call_order}")
    
    # List evaluation order
    call_order.clear()
    lst = [func_a(), func_b(), func_c()]
    print(f"List creation order: {call_order}")
    
    # Dictionary evaluation order
    call_order.clear()
    d = {'a': func_a(), 'b': func_b(), 'c': func_c()}
    print(f"Dict creation order: {call_order}")


# ============================================================================
# SECTION 7: PERFORMANCE BENCHMARKS
# ============================================================================

def performance_benchmarks():
    """
    Benchmark various operator operations for performance analysis.
    """
    print(f"\n=== PERFORMANCE BENCHMARKS ===")
    
    # Arithmetic operation benchmarks
    def benchmark_arithmetic():
        x, y = 1000, 37
        return x + y, x - y, x * y, x / y, x // y, x % y, x ** y
    
    def benchmark_bitwise():
        x, y = 1000, 37
        return x & y, x | y, x ^ y, ~x, x << 2, x >> 2
    
    def benchmark_comparison():
        x, y = 1000, 37
        return x == y, x != y, x < y, x > y, x <= y, x >= y
    
    # Time the operations
    arith_time = timeit.timeit(benchmark_arithmetic, number=100000)
    bit_time = timeit.timeit(benchmark_bitwise, number=100000)
    comp_time = timeit.timeit(benchmark_comparison, number=100000)
    
    print(f"Arithmetic operations: {arith_time:.6f}s")
    print(f"Bitwise operations: {bit_time:.6f}s")
    print(f"Comparison operations: {comp_time:.6f}s")
    
    # Division vs multiplication benchmark
    def division_test():
        return 1000 / 8
    
    def multiplication_test():
        return 1000 * 0.125
    
    def bit_shift_test():
        return 1000 >> 3  # Divide by 8 using bit shift
    
    div_time = timeit.timeit(division_test, number=100000)
    mul_time = timeit.timeit(multiplication_test, number=100000)
    shift_time = timeit.timeit(bit_shift_test, number=100000)
    
    print(f"\nDivision by 8:")
    print(f"  Regular division (/): {div_time:.6f}s")
    print(f"  Multiplication (*): {mul_time:.6f}s")
    print(f"  Bit shift (>>): {shift_time:.6f}s")
    print(f"  Bit shift is {div_time/shift_time:.1f}x faster than division")
    
    # Membership testing benchmarks
    small_list = list(range(10))
    small_set = set(range(10))
    large_list = list(range(1000))
    large_set = set(range(1000))
    
    def test_list_membership():
        return 999 in large_list
    
    def test_set_membership():
        return 999 in large_set
    
    list_time = timeit.timeit(test_list_membership, number=10000)
    set_time = timeit.timeit(test_set_membership, number=10000)
    
    print(f"\nMembership testing (1000 elements):")
    print(f"  List membership: {list_time:.6f}s")
    print(f"  Set membership: {set_time:.6f}s")
    print(f"  Set is {list_time/set_time:.0f}x faster for membership testing")


# ============================================================================
# SECTION 8: REAL-WORLD APPLICATIONS
# ============================================================================

def real_world_applications():
    """
    Demonstrate real-world applications of operators.
    """
    print(f"\n=== REAL-WORLD APPLICATIONS ===")
    
    # 1. Configuration flags using bitwise operators
    class ServerConfig:
        LOGGING = 1      # 0001
        DEBUG = 2        # 0010
        CACHING = 4      # 0100
        COMPRESSION = 8  # 1000
    
    def configure_server(config_flags):
        """Configure server based on bitwise flags."""
        config = {
            'logging': bool(config_flags & ServerConfig.LOGGING),
            'debug': bool(config_flags & ServerConfig.DEBUG),
            'caching': bool(config_flags & ServerConfig.CACHING),
            'compression': bool(config_flags & ServerConfig.COMPRESSION)
        }
        return config
    
    # Production configuration
    prod_config = ServerConfig.LOGGING | ServerConfig.CACHING | ServerConfig.COMPRESSION
    dev_config = ServerConfig.LOGGING | ServerConfig.DEBUG
    
    print("Server configuration using bitwise flags:")
    print(f"Production: {configure_server(prod_config)}")
    print(f"Development: {configure_server(dev_config)}")
    
    # 2. Data validation using logical operators
    def validate_email(email):
        """Validate email using logical operators."""
        return (
            email and                           # Not empty
            isinstance(email, str) and          # Is string
            '@' in email and                    # Contains @
            '.' in email.split('@')[-1] and     # Domain has dot
            len(email.split('@')) == 2 and      # Exactly one @
            all(part for part in email.split('@'))  # Both parts non-empty
        )
    
    test_emails = ['user@example.com', 'invalid-email', 'user@', '@domain.com', '']
    print(f"\nEmail validation:")
    for email in test_emails:
        print(f"  '{email}': {validate_email(email)}")
    
    # 3. Financial calculations with precision
    def calculate_compound_interest(principal, rate, time, precision=2):
        """Calculate compound interest with proper precision."""
        # Using Decimal for financial precision
        from decimal import Decimal, getcontext
        
        getcontext().prec = 28  # High precision
        
        p = Decimal(str(principal))
        r = Decimal(str(rate)) / 100
        t = Decimal(str(time))
        
        amount = p * ((1 + r) ** t)
        interest = amount - p
        
        return {
            'principal': float(p),
            'amount': round(float(amount), precision),
            'interest': round(float(interest), precision)
        }
    
    investment = calculate_compound_interest(10000, 5.5, 10)
    print(f"\nCompound interest calculation:")
    print(f"  Principal: ${investment['principal']:,}")
    print(f"  Final amount: ${investment['amount']:,}")
    print(f"  Interest earned: ${investment['interest']:,}")
    
    # 4. Hash table implementation using modulo operator
    class SimpleHashTable:
        def __init__(self, size=10):
            self.size = size
            self.table = [[] for _ in range(size)]
        
        def _hash(self, key):
            """Simple hash function using modulo."""
            return hash(key) % self.size
        
        def set(self, key, value):
            """Set key-value pair."""
            index = self._hash(key)
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return
            self.table[index].append((key, value))
        
        def get(self, key):
            """Get value by key."""
            index = self._hash(key)
            for k, v in self.table[index]:
                if k == key:
                    return v
            raise KeyError(key)
    
    # Demo hash table
    ht = SimpleHashTable(5)
    ht.set('name', 'Alice')
    ht.set('age', 25)
    ht.set('city', 'New York')
    
    print(f"\nSimple hash table demonstration:")
    print(f"  name: {ht.get('name')}")
    print(f"  age: {ht.get('age')}")
    print(f"  city: {ht.get('city')}")


# ============================================================================
# SECTION 9: TESTING AND VALIDATION
# ============================================================================

def test_operator_behaviors():
    """
    Test various operator behaviors and edge cases.
    """
    print(f"\n=== TESTING OPERATOR BEHAVIORS ===")
    
    # Test arithmetic operators
    assert 5 + 3 == 8, "Addition test failed"
    assert 5 - 3 == 2, "Subtraction test failed"
    assert 5 * 3 == 15, "Multiplication test failed"
    assert 5 / 2 == 2.5, "Division test failed"
    assert 5 // 2 == 2, "Floor division test failed"
    assert 5 % 2 == 1, "Modulo test failed"
    assert 2 ** 3 == 8, "Exponentiation test failed"
    
    # Test comparison operators
    assert 5 == 5, "Equality test failed"
    assert 5 != 3, "Inequality test failed"
    assert 5 > 3, "Greater than test failed"
    assert 3 < 5, "Less than test failed"
    assert 5 >= 5, "Greater or equal test failed"
    assert 5 <= 5, "Less or equal test failed"
    
    # Test logical operators
    assert True and True, "Logical AND test failed"
    assert True or False, "Logical OR test failed"
    assert not False, "Logical NOT test failed"
    
    # Test bitwise operators
    assert 5 & 3 == 1, "Bitwise AND test failed"
    assert 5 | 3 == 7, "Bitwise OR test failed"
    assert 5 ^ 3 == 6, "Bitwise XOR test failed"
    assert 5 << 1 == 10, "Left shift test failed"
    assert 5 >> 1 == 2, "Right shift test failed"
    
    # Test identity and membership
    a = [1, 2, 3]
    b = a
    assert a is b, "Identity test failed"
    assert 2 in a, "Membership test failed"
    
    print("✅ All operator tests passed!")


def edge_case_tests():
    """
    Test edge cases and special behaviors.
    """
    print(f"\n=== EDGE CASE TESTS ===")
    
    # Test float precision
    assert abs((0.1 + 0.2) - 0.3) < 1e-10, "Float precision test failed"
    
    # Test integer overflow (Python handles arbitrary precision)
    big_num = 10 ** 100
    assert big_num * big_num == 10 ** 200, "Big integer test failed"
    
    # Test division by zero handling
    try:
        result = 1 / 0
        assert False, "Division by zero should raise exception"
    except ZeroDivisionError:
        pass  # Expected
    
    # Test NaN behavior
    nan = float('nan')
    assert nan != nan, "NaN equality test failed"
    assert math.isnan(nan), "NaN detection test failed"
    
    # Test infinity
    inf = float('inf')
    assert inf > 1000000, "Infinity comparison test failed"
    assert inf == inf, "Infinity equality test failed"
    
    # Test short-circuiting
    def side_effect():
        side_effect.called = True
        return True
    
    side_effect.called = False
    result = False and side_effect()
    assert not side_effect.called, "Short-circuiting test failed"
    
    side_effect.called = False
    result = True or side_effect()
    assert not side_effect.called, "Short-circuiting OR test failed"
    
    print("✅ All edge case tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all operator demonstrations.
    """
    print("Python Operators and Expressions - Comprehensive Demonstration")
    print("=" * 65)
    
    try:
        # Run all demonstrations
        arithmetic_operators_demo()
        arithmetic_edge_cases()
        comparison_operators_demo()
        identity_and_membership()
        logical_operators_demo()
        practical_logical_patterns()
        bitwise_operators_demo()
        bit_tricks_and_optimizations()
        assignment_operators_demo()
        walrus_operator_demo()
        operator_precedence_demo()
        evaluation_order_and_side_effects()
        performance_benchmarks()
        real_world_applications()
        test_operator_behaviors()
        edge_case_tests()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 65}")
        print("Operator demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement a calculator that handles operator precedence correctly.

2. Create a binary number class that supports all bitwise operations.

3. Write a function that uses only bitwise operations to:
   - Multiply by 3
   - Check if a number is a power of 4
   - Count trailing zeros

4. Implement a simple expression evaluator that parses and evaluates
   mathematical expressions with proper precedence.

5. Create a flags system for user permissions using bitwise operations.

6. Write a function that finds the single non-duplicate number in an array
   where every other number appears twice (use XOR).

7. Implement a hash function using various operators for string keys.

8. Create a validation system that uses logical operators to check
   complex business rules.

9. Write a function that performs arithmetic operations on fractions
   without using the fractions module.

10. Implement a simple compiler that converts infix expressions to
    postfix notation (Shunting Yard algorithm).

PERFORMANCE CHALLENGES:

1. Compare the performance of different ways to check if a number is even.
2. Benchmark various methods of computing powers of 2.
3. Measure the performance difference between 'is' and '==' for different types.
4. Time the performance of membership testing in different data structures.

MUSCLE MEMORY DRILLS:

Practice these patterns daily:
- Bitwise flags: flag |= BIT, flag &= ~BIT, flag ^= BIT
- Null coalescing: value = input_val or default_val
- Bounds checking: 0 <= index < len(array)
- Power of 2 check: (n & (n-1)) == 0
- Even/odd check: n & 1
"""
