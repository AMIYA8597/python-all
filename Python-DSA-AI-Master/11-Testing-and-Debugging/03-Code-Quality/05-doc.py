"""
Module Docstring: Code Documentation

Learning Objectives:
1. Understand the importance of code documentation.
2. Write effective docstrings in various formats (Google, Sphinx/reST, NumPy).
3. Use the `doctest` module to write testable documentation.
4. Extract documentation programmatically.

Concept Explanation:
Python allows adding documentation directly to modules, classes, and functions using
docstrings (triple-quoted strings). These docstrings can be parsed by tools like 
Sphinx to generate HTML documentation, or read using the built-in `help()` function.
`doctest` can execute examples embedded in docstrings to ensure documentation stays 
up-to-date with code.
"""

import math
import pydoc
import time
from typing import Union
import unittest

# Basic Implementation: Google Style Docstring and Doctest
def calculate_factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer.

    Args:
        n (int): The integer to calculate the factorial of.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.

    Example:
        >>> calculate_factorial(5)
        120
        >>> calculate_factorial(0)
        1
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)

# Intermediate Implementation: Sphinx/reST Style and Type hints integration
def find_roots(a: float, b: float, c: float) -> Union[tuple[float, float], None]:
    """
    Finds the real roots of a quadratic equation ax^2 + bx + c = 0.

    :param float a: Coefficient of x^2. Must not be zero.
    :param float b: Coefficient of x.
    :param float c: Constant term.
    :return: A tuple containing the two real roots, or None if roots are complex.
    :rtype: Union[tuple[float, float], None]
    :raises ValueError: if `a` is zero.
    
    Example:
        >>> find_roots(1, -3, 2)
        (2.0, 1.0)
        >>> find_roots(1, 0, 1) is None
        True
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero in a quadratic equation.")
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    root1 = (-b + math.sqrt(discriminant)) / (2*a)
    root2 = (-b - math.sqrt(discriminant)) / (2*a)
    return (root1, root2)

# Advanced Implementation: Programmatically extracting documentation using pydoc
def get_function_documentation(func_name: str) -> str:
    """
    Uses pydoc to extract the documentation of a given function programmatically.
    """
    func_obj = eval(func_name)
    doc = pydoc.render_doc(func_obj, renderer=pydoc.plaintext)
    return doc

# Performance Analysis
def performance_analysis() -> None:
    """
    Docstrings are loaded into memory when the module is imported.
    They consume a small amount of memory, but don't impact execution speed.
    """
    start = time.time()
    for _ in range(10000):
        _ = calculate_factorial.__doc__
    doc_access_time = time.time() - start
    print(f"Time to access docstring 10000 times: {doc_access_time:.6f} seconds")

# Edge Cases
# - Using raw strings (r"") for docstrings that contain escape characters (like regex \n or \t).
# - Stripping leading whitespace from docstrings when rendering (textwrap.dedent).
# - Code examples in doctests that depend on dictionary ordering (which can be arbitrary in older Pythons).

# Interview Challenge
"""
Challenge: Write a function with a doctest that tests for an exception being raised.
"""
def divide(a: int, b: int) -> float:
    """
    Divides a by b.
    
    >>> divide(10, 2)
    5.0
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    return a / b

# Tests
class TestDocumentation(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(calculate_factorial(5), 120)
        with self.assertRaises(ValueError):
            calculate_factorial(-1)
            
    def test_find_roots(self):
        self.assertEqual(find_roots(1, -3, 2), (2.0, 1.0))
        self.assertIsNone(find_roots(1, 0, 1))
        
    def test_get_doc(self):
        doc = get_function_documentation('calculate_factorial')
        self.assertTrue('Calculates the factorial' in doc)

if __name__ == "__main__":
    import doctest
    print("Running doctests...")
    # Run doctests first
    doctest.testmod(verbose=False)
    
    print("\nRunning unit tests...")
    unittest.main(exit=False)
    
    print("\nRunning performance analysis...")
    performance_analysis()
