import os

content = """\"\"\"
================================================================================
LABORATORY 02: OPERATORS AND EXPRESSIONS (DEEP DIVE)
================================================================================
Course: Python Fundamentals
Module: 02-Basic
Target File: 02-operators-and-expressions.py

DESCRIPTION:
This file is a textbook-level laboratory script that exhaustively covers 
Python operators and expressions. It includes extensive documentation,
production-grade type-hinted code, edge case demonstrations, assertions, 
active recall exercises, and interview questions.

TABLE OF CONTENTS:
1. Arithmetic Operators & Edge Cases
2. Bitwise Operators (Bit-level Deep Dive)
3. Logical Operators & Short-circuiting
4. Comparison Operators & Chaining
5. Identity Operators (`is` vs `==`)
6. Membership Operators (`in`)
7. The Walrus Operator (`:=`)

================================================================================
ACTIVE RECALL & INTERVIEW QUESTIONS
================================================================================

Q1: What is the difference between `/` and `//` in Python?
A: `/` performs true division and always returns a float. `//` performs floor 
division, returning an integer (if operands are integers) that is the largest 
integer less than or equal to the true division result. E.g., -5 // 2 is -3.

Q2: How does Python's modulo `%` handle negative numbers?
A: The result of `a % b` always has the same sign as the divisor `b`. 
This is because it follows the equation `a = (a // b) * b + (a % b)`.

Q3: Explain logical short-circuiting in Python.
A: When evaluating `a and b`, if `a` is falsy, Python returns `a` without 
evaluating `b`. When evaluating `a or b`, if `a` is truthy, Python returns `a` 
without evaluating `b`.

Q4: What is the difference between `is` and `==`?
A: `is` checks for object identity (whether two variables point to the same 
object in memory), whereas `==` checks for value equality.

Q5: What is the Walrus Operator (`:=`) and when was it introduced?
A: Introduced in Python 3.8, it is an assignment expression that assigns a 
value to a variable as part of a larger expression.

\"\"\"

import math
import sys
from typing import List, Tuple, Any, Optional

def demonstrate_arithmetic_operators() -> None:
    \"\"\"
    Section 1: Arithmetic Operators
    
    This function demonstrates true division, floor division, modulo, and 
    exponentiation, paying special attention to negative numbers and floats.
    \"\"\"
    print("--- 1. Arithmetic Operators ---")
    
    # 1.1 True Division vs Floor Division
    # True division always returns a float
    assert (10 / 2) == 5.0
    assert type(10 / 2) is float
    
    # Floor division returns an int (if inputs are ints)
    assert (10 // 3) == 3
    
    # Floor division with negative numbers rounds towards negative infinity
    # -10 / 3 = -3.333... -> floor is -4
    assert (-10 // 3) == -4
    assert (10 // -3) == -4
    
    # 1.2 Modulo Operator
    # Modulo with negative numbers follows: a = (a // b) * b + (a % b)
    assert (10 % 3) == 1   # 10 = (10 // 3)*3 + 1 = 3*3 + 1
    assert (-10 % 3) == 2  # -10 = (-10 // 3)*3 + 2 = -4*3 + 2 = -12 + 2
    assert (10 % -3) == -2 # 10 = (10 // -3)*-3 + (-2) = -4*-3 - 2 = 12 - 2
    
    # 1.3 Exponentiation and Precedence
    # Note that exponentiation binds tighter than unary minus
    assert -2 ** 2 == -4  # -(2**2)
    assert (-2) ** 2 == 4 # (-2)**2
    
    # Floats and precision issues
    res = 0.1 + 0.2
    assert res != 0.3
    assert math.isclose(res, 0.3)
    
    print("Arithmetic operators demo passed.\\n")


def demonstrate_bitwise_operators() -> None:
    \"\"\"
    Section 2: Bitwise Operators
    
    Python bitwise operators work on integers as if they were represented in 
    two's complement binary.
    
    Operators:
    & (AND): Sets each bit to 1 if both bits are 1
    | (OR): Sets each bit to 1 if one of two bits is 1
    ^ (XOR): Sets each bit to 1 if only one of two bits is 1
    ~ (NOT): Inverts all the bits (returns -x - 1)
    << (Zero fill left shift): Shift left by pushing zeros
    >> (Signed right shift): Shift right by pushing copies of the leftmost bit
    \"\"\"
    print("--- 2. Bitwise Operators ---")
    
    a: int = 0b1010  # 10 in decimal
    b: int = 0b1100  # 12 in decimal
    
    # 2.1 Bitwise AND
    # 1010 & 1100 = 1000 (8 in decimal)
    assert (a & b) == 0b1000
    
    # 2.2 Bitwise OR
    # 1010 | 1100 = 1110 (14 in decimal)
    assert (a | b) == 0b1110
    
    # 2.3 Bitwise XOR
    # 1010 ^ 1100 = 0110 (6 in decimal)
    assert (a ^ b) == 0b0110
    
    # 2.4 Bitwise NOT
    # ~x = -x - 1
    assert ~a == -11
    
    # 2.5 Left Shift
    # x << y is equivalent to x * (2**y)
    assert (a << 2) == 0b101000 # 40 in decimal
    assert (a << 2) == a * 4
    
    # 2.6 Right Shift
    # x >> y is equivalent to x // (2**y)
    assert (a >> 1) == 0b0101 # 5 in decimal
    assert (a >> 1) == a // 2
    
    # Negative right shift
    # -10 is ...11110110
    # -10 >> 1 is ...11111011 (-5)
    assert (-10 >> 1) == -5
    
    print("Bitwise operators demo passed.\\n")


def demonstrate_logical_operators() -> None:
    \"\"\"
    Section 3: Logical Operators & Short-Circuiting
    
    Python uses 'and', 'or', and 'not'.
    These operators are short-circuiting and evaluate sequentially.
    \"\"\"
    print("--- 3. Logical Operators ---")
    
    # 3.1 Truthy and Falsy values
    # Falsy values: False, None, 0, 0.0, empty strings, empty collections
    falsy_values = [False, None, 0, 0.0, "", [], (), {}, set()]
    for val in falsy_values:
        assert not val, f"{val} should be falsy"
        
    # 3.2 Short-Circuiting behavior with 'or'
    # 'a or b' returns 'a' if 'a' is truthy, else evaluates and returns 'b'
    assert ("truthy_string" or 0) == "truthy_string"
    assert (0 or "fallback") == "fallback"
    
    # Demonstrating short-circuit side-effects
    def side_effect() -> bool:
        raise RuntimeError("This should not be executed!")
        
    # This won't raise an error because True short-circuits the evaluation
    result_or = True or side_effect()
    assert result_or is True
    
    # 3.3 Short-Circuiting behavior with 'and'
    # 'a and b' returns 'a' if 'a' is falsy, else evaluates and returns 'b'
    assert (0 and "truthy") == 0
    assert ("truthy" and 42) == 42
    
    # This won't raise an error because False short-circuits the evaluation
    result_and = False and side_effect()
    assert result_and is False
    
    print("Logical operators demo passed.\\n")


def demonstrate_comparison_chaining() -> None:
    \"\"\"
    Section 4: Comparison Operators & Chaining
    
    Python allows chaining of relational operators.
    a < b < c is equivalent to (a < b) and (b < c)
    \"\"\"
    print("--- 4. Comparison Operators & Chaining ---")
    
    x: int = 5
    y: int = 10
    z: int = 15
    
    # 4.1 Basic Chaining
    assert x < y < z
    assert 1 < x <= 5
    assert z > y > x
    
    # 4.2 Chaining with different operators
    # Evaluates to (x < y) and (y == 10) and (10 > 5)
    assert x < y == 10 > 5
    
    # 4.3 Short-circuiting in chaining
    def get_z_with_error() -> int:
        raise RuntimeError("Should not evaluate z")
        
    # If the first part fails, the rest isn't evaluated
    # False and (y < get_z_with_error())
    try:
        res = y < x < get_z_with_error()
        assert res is False
    except RuntimeError:
        assert False, "Chaining did not short-circuit correctly!"
        
    print("Comparison chaining demo passed.\\n")


def demonstrate_identity_and_membership() -> None:
    \"\"\"
    Section 5 & 6: Identity and Membership Operators
    
    'is' checks for object identity (memory address).
    'in' checks for membership in a collection.
    \"\"\"
    print("--- 5 & 6. Identity and Membership ---")
    
    # 5.1 Identity (is, is not)
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    
    assert a == b  # Same values
    assert a is not b  # Different objects in memory
    assert a is c  # Same object in memory
    
    # Python caches small integers (typically -5 to 256) and small strings
    x = 256
    y = 256
    assert x is y
    
    x_large = 1000
    y_large = 1000
    # Depending on the interpreter or context (REPL vs Script), this might 
    # actually be True due to constant folding, but generally it's not guaranteed.
    # In a script, the compiler might fold them, so we just use == for large ints.
    assert x_large == y_large
    
    # 6.1 Membership (in, not in)
    my_str = "Hello World"
    assert "World" in my_str
    assert "world" not in my_str  # Case-sensitive
    
    my_dict = {"key1": "value1", "key2": "value2"}
    assert "key1" in my_dict  # Checks keys, not values
    assert "value1" not in my_dict
    assert "value1" in my_dict.values()
    
    print("Identity and Membership demo passed.\\n")


def demonstrate_walrus_operator() -> None:
    \"\"\"
    Section 7: The Walrus Operator (:=)
    
    Introduced in Python 3.8. It allows assignment of variables within an 
    expression. Useful in while loops and list comprehensions to avoid 
    redundant computations.
    \"\"\"
    print("--- 7. Walrus Operator ---")
    
    # 7.1 Simple usage
    # Assigns 10 to n, and then evaluates the expression (n > 5)
    if (n := 10) > 5:
        assert n == 10
        
    # 7.2 In a list comprehension to avoid repeated function calls
    def slow_computation(x: int) -> int:
        return x * x
        
    data = [1, 2, 3, 4, 5]
    
    # Without walrus:
    # results = [slow_computation(x) for x in data if slow_computation(x) > 10]
    
    # With walrus:
    results = [y for x in data if (y := slow_computation(x)) > 10]
    assert results == [16, 25]
    
    # 7.3 In a while loop (simulated)
    buffer = ["chunk1", "chunk2", "chunk3", ""]
    def get_chunk() -> str:
        return buffer.pop(0)
        
    chunks_read = []
    # Read until empty string
    while (chunk := get_chunk()) != "":
        chunks_read.append(chunk)
        
    assert chunks_read == ["chunk1", "chunk2", "chunk3"]
    
    print("Walrus operator demo passed.\\n")


def main() -> None:
    print("Starting Laboratory 02: Operators and Expressions...\\n")
    
    demonstrate_arithmetic_operators()
    demonstrate_bitwise_operators()
    demonstrate_logical_operators()
    demonstrate_comparison_chaining()
    demonstrate_identity_and_membership()
    demonstrate_walrus_operator()
    
    print("\\n================================================================================")
    print("LABORATORY 02 COMPLETED SUCCESSFULLY")
    print("================================================================================")


if __name__ == "__main__":
    main()
"""

target_path = r'd:\work\python-all\01-Python-Fundamentals\02-Basic\02-operators-and-expressions.py'
os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Generated successfully')
