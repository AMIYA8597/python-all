"""
# ==============================================================================
# LABORATORY 02: OPERATORS, EXPRESSIONS, AND EVALUATION MECHANICS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Operators seem mathematically trivial, but in Python they translate directly 
# to dunder (magic) methods at the C-level (e.g., `+` becomes `__add__`). 
# Mastering operators is required to overload them in custom objects (OOP), 
# optimize algorithms (bitwise shifts), and avoid production bugs with identity 
# vs equality and floating-point arithmetic.
#
# 2. PREREQUISITES
# ----------------
# - Understanding of basic variables and identity (Laboratory 01).
#
# 3. LEARNING OBJECTIVES
# ----------------------
# - Master arithmetic operators, focusing on precision, modulo math, and floor division.
# - Understand Bitwise operators at the binary level (crucial for DSA/flags).
# - Master logical short-circuit evaluation.
# - Differentiate between 'is' (identity) and '==' (equality).
# - Utilize the Walrus Operator (:=) for assignment expressions.
#
# ==============================================================================
"""

import sys
import math
from typing import List, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 4. ARITHMETIC OPERATORS & THE FLOATING POINT TRAP
# ==============================================================================
def demonstrate_arithmetic():
    """
    Standard arithmetic includes: +, -, *, /, //, %, **
    Every operator delegates to a dunder method:
    a + b  ->  a.__add__(b)
    """
    section_header("Arithmetic and Floating Point Mechanics")
    
    a, b = 10, 3
    
    # 1. True Division (always returns float)
    print(f"{a} / {b} = {a / b} (Type: {type(a / b).__name__})")
    
    # 2. Floor Division (returns int if inputs are int, truncates toward negative infinity)
    print(f"{a} // {b} = {a // b} (Type: {type(a // b).__name__})")
    
    # 3. Modulo (remainder)
    print(f"{a} % {b} = {a % b}")
    
    # TRAP: Modulo with negative numbers (Python vs C)
    # In C/Java, -10 % 3 = -1. 
    # In Python, -10 % 3 = 2. 
    # Python guarantees the sign of the modulo matches the sign of the divisor.
    print(f"-10 % 3 = {-10 % 3} (Python specific behavior!)")
    
    # 4. Exponentiation
    print(f"{a} ** {b} = {a ** b}")
    
    # TRAP: Floating Point Imprecision (IEEE 754)
    print("\n--- The Floating Point Trap ---")
    val = 0.1 + 0.2
    print(f"0.1 + 0.2 = {val}")  # Prints 0.30000000000000004
    print(f"0.1 + 0.2 == 0.3 is {val == 0.3}") # FALSE!
    
    # Production fix: use math.isclose()
    print(f"Using math.isclose(0.1 + 0.2, 0.3): {math.isclose(val, 0.3)}")


# ==============================================================================
# 5. BITWISE OPERATORS (CRUCIAL FOR DSA & LOW-LEVEL OPTIMIZATION)
# ==============================================================================
def demonstrate_bitwise():
    """
    Operates directly on the binary representations of integers.
    &: AND
    |: OR
    ^: XOR
    ~: NOT (Two's complement)
    <<: Left Shift
    >>: Right Shift
    """
    section_header("Bitwise Operators (Binary Level)")
    
    x = 10  # Binary: 1010
    y = 4   # Binary: 0100
    
    print(f"x = {x} (Binary: {bin(x)})")
    print(f"y = {y} (Binary: {bin(y)})")
    
    # AND (Both bits must be 1)
    # 1010 & 0100 = 0000
    print(f"x & y  = {x & y} (Binary: {bin(x & y)})")
    
    # OR (Either bit is 1)
    # 1010 | 0100 = 1110
    print(f"x | y  = {x | y} (Binary: {bin(x | y)})")
    
    # XOR (Bits must be different)
    # 1010 ^ 0100 = 1110
    print(f"x ^ y  = {x ^ y} (Binary: {bin(x ^ y)})")
    
    # XOR Trick for DSA: Missing number or duplicate number in O(N) time, O(1) space
    # x ^ x = 0
    # x ^ 0 = x
    arr = [2, 3, 2, 4, 4]
    res = 0
    for num in arr:
        res ^= num
    print(f"\nXOR Trick: Unique number in {arr} is {res}")
    
    # LEFT SHIFT (Multiply by 2^n)
    # 1010 << 1 = 10100 (20)
    print(f"\nx << 1 = {x << 1} (Binary: {bin(x << 1)}) - Multiplies by 2")
    
    # RIGHT SHIFT (Floor divide by 2^n)
    # 1010 >> 1 = 0101 (5)
    print(f"x >> 1 = {x >> 1} (Binary: {bin(x >> 1)}) - Floor Divides by 2")


# ==============================================================================
# 6. LOGICAL OPERATORS & SHORT-CIRCUIT EVALUATION
# ==============================================================================
def expensive_function(name: str) -> bool:
    print(f"   [!] expensive_function called for '{name}'")
    return True

def demonstrate_logical():
    """
    and, or, not
    Python uses short-circuit evaluation. It stops evaluating as soon as 
    the result is determined.
    """
    section_header("Logical Operators & Short-Circuiting")
    
    print("Testing: False and expensive_function()")
    # 'and' requires both to be True. Since the first is False, Python stops.
    result = False and expensive_function("A")
    print(f"Result: {result} (Notice function A was NOT called)\n")
    
    print("Testing: True or expensive_function()")
    # 'or' requires one to be True. Since the first is True, Python stops.
    result = True or expensive_function("B")
    print(f"Result: {result} (Notice function B was NOT called)\n")
    
    # Truthiness: Python considers 0, None, "", [], {}, False as Falsy. 
    # Everything else is Truthy.
    # The 'or' operator actually returns the FIRST truthy value, not True/False.
    name = ""
    default = "Guest"
    # If name is falsy, it evaluates and returns 'default'
    user = name or default 
    print(f"Falsy evaluation: name='{name}' -> user='{user}'")


# ==============================================================================
# 7. COMPARISON & IDENTITY
# ==============================================================================
def demonstrate_comparison():
    """
    ==, !=, >, <, >=, <=, is, is not, in, not in
    """
    section_header("Comparison, Chaining, and Identity")
    
    # Python supports mathematical chaining!
    x = 5
    print(f"1 < {x} <= 10 : {1 < x <= 10}") # Evaluates as (1 < x) and (x <= 10)
    
    # Identity vs Equality (Review from Lab 01, applied to expressions)
    a = [1, 2, 3]
    b = [1, 2, 3]
    print(f"\na == b : {a == b} (Values match)")
    print(f"a is b : {a is b} (Memory locations differ)")


# ==============================================================================
# 8. THE WALRUS OPERATOR (ASSIGNMENT EXPRESSION)
# ==============================================================================
def demonstrate_walrus():
    """
    Added in Python 3.8.
    := allows assigning a value to a variable AS PART OF an expression.
    """
    section_header("The Walrus Operator (:=)")
    
    # Traditional way:
    text = "Hello World"
    n = len(text)
    if n > 10:
        print(f"Traditional: Text is {n} chars long.")
        
    # Walrus way:
    if (n_walrus := len(text)) > 10:
        print(f"Walrus: Text is {n_walrus} chars long.")
        
    # It is especially useful in while loops:
    # while (chunk := file.read(1024)): 
    #     process(chunk)


# ==============================================================================
# 9. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the difference between / and // in Python.
   Answer: / is true division (always returns float). // is floor division (truncates toward negative infinity).
   
2. How does -10 % 3 evaluate in Python vs C?
   Answer: Python returns 2 (matches sign of divisor). C returns -1.
   
3. What is short-circuit evaluation?
   Answer: Logical expressions stop evaluating as soon as the outcome is certain. 
   (e.g., in `A or B`, if A is True, B is never evaluated).
   
4. How do you find a unique number in an array of duplicates in O(1) space?
   Answer: Use XOR (`^`). x ^ x = 0, so all duplicates cancel out, leaving the unique number.

5. What does the Walrus operator (:=) do?
   Answer: It assigns a value to a variable within a larger expression, saving a line of code and a redundant evaluation.
"""

if __name__ == "__main__":
    demonstrate_arithmetic()
    demonstrate_bitwise()
    demonstrate_logical()
    demonstrate_comparison()
    demonstrate_walrus()
    print("\n[SUCCESS] Laboratory 02 Completed.")
