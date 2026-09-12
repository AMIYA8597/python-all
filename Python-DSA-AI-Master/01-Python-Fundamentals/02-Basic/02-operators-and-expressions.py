"""
# 02 - Python Operators, Expressions, and Bitwise Logic

## A. Concept Name
Python Operators, Expressions, and Bitwise Logic

## B. One-Sentence Definition
Operators are special symbols or keywords that perform specific computations (mathematical, logical, or bitwise) on one or more operands (values/variables).

## C. Why Does This Exist?
To do any meaningful work, a program must manipulate data. Operators provide a concise syntax for invoking underlying object methods (like `__add__` for `+`) to compute new values or evaluate conditions.

## D. Intuition
Think of operators as the verbs in the Python language. If variables are the nouns (data), operators define the actions taken upon them.
- `+` (add this to that)
- `and` (are both of these true?)
- `&` (combine these at the microscopic bit level)

## E. Mental Model
An expression (like `a + b`) is a recipe. Python evaluates the recipe by calling `a.__add__(b)` under the hood, and produces a single new resulting object.

## F. Visual Explanation (Short-Circuiting)
Logical `and` and `or` use short-circuit evaluation.

```text
Condition A `and` Condition B
     |
     v
 Is A True? ---> NO ---> Return A (Stop immediately. B is ignored!)
     |
    YES
     |
     v
 Return B
```

## G. Formal Explanation
Python supports several categories of operators:
1. **Arithmetic**: `+`, `-`, `*`, `/` (float division), `//` (floor division), `%` (modulo), `**` (exponentiation).
2. **Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`.
3. **Identity**: `is`, `is not` (compares memory addresses via `id()`).
4. **Membership**: `in`, `not in` (calls `__contains__`).
5. **Logical**: `and`, `or`, `not`.
6. **Bitwise**: `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (Left Shift), `>>` (Right Shift).

## H. Implementation & Examples
See the functions `arithmetic_and_comparison`, `short_circuit_logic`, and `bitwise_operations` below.

## I. Trace (XOR Swap)
Trace of an XOR swap (a common interview trick to swap variables without temp):
a = 5 (0101)
b = 3 (0011)

1. a = a ^ b  -> a is now 0110 (6)
2. b = a ^ b  -> b is now 0110 ^ 0011 = 0101 (5)
3. a = a ^ b  -> a is now 0110 ^ 0101 = 0011 (3)
Variables are swapped!
(Note: In Python, `a, b = b, a` is better and faster, but this is conceptually important.)

## J. Common Mistakes
1. Confusing `is` and `==`. 
   `==` means "do they have the same value?"
   `is` means "are they the exact same object in memory?"
2. Using bitwise `&` instead of logical `and`.
   `True and False` is a logical operation.
   `1 & 0` is a bitwise operation. They behave differently on non-boolean objects.
3. Chained comparisons:
   `1 < x < 10` is valid in Python and translates to `1 < x and x < 10`.

## K. Common Confusions
`is` vs `==` with strings and integers:
Python caches small integers (-5 to 256) and short strings (interning).
```python
a = 256
b = 256
a is b # True

a = 257
b = 257
a is b # False (Usually, depending on the compiler context!)
```
Rule: NEVER use `is` for comparing numbers or strings. ONLY use `is` to check `is None`.

## L. When To Use
- Use `//` when you explicitly need an integer result (e.g., array indices).
- Use `is None` to check for null values (it is faster and safer than `== None`).
- Use bitwise operators (`&`, `|`) for permissions, masks, or specific LeetCode optimizations.

## M. Debugging
Symptom: `TypeError: unsupported operand type(s) for +: 'int' and 'str'`
Cause: Strongly typed nature of Python. It won't auto-convert int to string.
Fix: Explicitly cast: `str(5) + " apples"`

## N. Memory Hook
1. `==` checks the VALUE (What's inside the box?)
2. `is` checks the IDENTITY (Is it the exact same box?)
3. `and`/`or` are LAZY (Short-circuit evaluation).

## O. Active Recall
1. What does `10 // -3` evaluate to, and why?
2. If `a = [1,2]` and `b = [1,2]`, what does `a == b` return? What about `a is b`?
3. Why is `x = x ^ x` always 0?

## P. Practice
Exercise 1: Write a function `is_even(n)` that uses BITWISE operators, not modulo (`%`).
Hint: The least significant bit of an even number in binary is always 0.

## Q. Interview Question
Q: How does Python evaluate `A or B or C`?
A: It evaluates from left to right. It returns the FIRST truthy object it encounters. 
If none are truthy, it returns the LAST object (C). It does NOT necessarily return `True` or `False`.

## R. Real-World Applications
Short-circuit logic is heavily utilized to safely access nested attributes or check states before proceeding with heavier computation. Bitwise operators are widely used in low-level communication, data compression, cryptography, and managing states with bitmasks.

## S. Advanced Techniques
Advanced Python code often overrides operator behavior by defining magic methods (`__add__`, `__mul__`, `__eq__`) in custom classes, enabling domain-specific syntaxes like numpy arrays where `A + B` performs element-wise addition.

## T. Best Practices
Avoid writing overly complex, dense expressions that chain too many operators. Use parentheses heavily to make the order of operations explicit even if you've memorized PEP 8's precedence table. Use Python's chained comparisons `0 <= i < len(arr)` instead of `i >= 0 and i < len(arr)`.

## U. Ecosystem Context
In frameworks like pandas and numpy, logical operators `and` / `or` are replaced with bitwise operators `&` / `|` for element-wise array operations, overriding their typical use.

## V. Performance Characteristics
Bitwise operations are significantly faster than their arithmetic equivalents when performing specific mathematical tasks (like multiplying/dividing by powers of 2 or parity checks) because they map more directly to CPU-level operations.

## W. Edge Cases
Float arithmetic operations can suffer from precision issues (`0.1 + 0.2` is `0.30000000000000004`). `NaN` != `NaN` in IEEE 754, so `math.isnan()` must be used instead of `==`.

## X. Project Connection
Short-circuiting is heavily used in configuration loading:
`api_key = os.getenv("API_KEY") or load_from_file() or "DEFAULT_KEY"`
This gracefully falls back from environment variable -> file -> default without executing the file loader if the env var exists.
"""

def arithmetic_and_comparison():
    """Demonstrates standard arithmetic and the importance of float vs floor division."""
    print("--- 1. Arithmetic & Comparison ---")
    a = 10
    b = 3
    
    print(f"{a} / {b}  = {a / b} (True division, returns float)")
    print(f"{a} // {b} = {a // b} (Floor division, returns int truncated towards negative infinity)")
    print(f"{a} % {b}  = {a % b} (Modulo, remainder)")
    print(f"{a} ** {b} = {a ** b} (Exponentiation)")
    
    # Negative floor division trick
    print(f"-10 // 3 = {-10 // 3} (Notice it is -4, not -3! Truncates towards negative infinity)")


def short_circuit_logic():
    """
    Advanced Concept: Short-Circuit Evaluation.
    Python stops evaluating logical expressions as soon as the result is determined.
    """
    print("\n--- 2. Short-Circuit Logic ---")
    
    def dangerous_call():
        raise Exception("This function should never be called!")

    # 'and' requires BOTH to be True. Since False is encountered first, it stops.
    result = False and dangerous_call()
    print("False and dangerous_call() -> Safely stopped early.")
    
    # 'or' requires ONLY ONE to be True. Since True is encountered first, it stops.
    result = True or dangerous_call()
    print("True or dangerous_call() -> Safely stopped early.")
    
    # Python returns the actual object, not necessarily a boolean!
    print(f"'Hello' or 'World' returns: {'Hello' or 'World'}")
    print(f"0 or 'World' returns: {0 or 'World'}")


def bitwise_operations():
    """
    Advanced Concept: Bitwise operations manipulate numbers at the binary level.
    Crucial for algorithmic optimization, cryptography, and systems programming.
    """
    print("\n--- 3. Bitwise Operations ---")
    # 5 is 0101 in binary
    # 3 is 0011 in binary
    x, y = 5, 3
    
    print(f"{x} & {y} = {x & y}  (Binary 0001)")
    print(f"{x} | {y} = {x | y}  (Binary 0111)")
    print(f"{x} ^ {y} = {x ^ y}  (Binary 0110 - XOR: 1 if bits are different)")
    
    # Shifts
    print(f"{x} << 1 = {x << 1} (Left shift by 1 multiplies by 2)")
    print(f"{x} >> 1 = {x >> 1} (Right shift by 1 floor-divides by 2)")


def is_even(n: int) -> bool:
    # 5 in binary is 101. 101 & 001 is 001 (True)
    # 4 in binary is 100. 100 & 001 is 000 (False)
    return (n & 1) == 0

if __name__ == "__main__":
    arithmetic_and_comparison()
    short_circuit_logic()
    bitwise_operations()
    
    # Practice validation
    assert is_even(10) is True
    assert is_even(7) is False
    print("\nPractice functions passed.")
