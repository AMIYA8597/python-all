"""
Module Docstring: Static Code Analysis with Pylint

Learning Objectives:
1. Understand the importance of static code analysis for code quality.
2. Learn how to use pylint programmatically to check code quality.
3. Understand pylint messages (errors, warnings, refactor, convention).
4. Learn to configure pylint and handle edge cases.

Concept Explanation:
Pylint is a static code analyser for Python. It checks for errors in Python code,
tries to enforce a coding standard and looks for code smells. It can also look for
certain type errors, it can recommend suggestions about how particular blocks can be
refactored and can offer you details about the code's complexity.

"""

import sys
import io
import time
import ast
import tempfile
import os
from typing import List, Dict, Any, Optional
import unittest

try:
    from pylint.lint import Run
    from pylint.reporters.text import TextReporter
    HAS_PYLINT = True
except ImportError:
    HAS_PYLINT = False

# Basic Implementation: A function that violates some pylint rules, and its corrected version
def bad_function( A,  b):
    c=A+b
    return c

def good_function(first_number: int, second_number: int) -> int:
    """
    Adds two numbers and returns the result.
    
    Args:
        first_number: The first number.
        second_number: The second number.
    
    Returns:
        The sum of the two numbers.
    """
    return first_number + second_number

# Intermediate Implementation: Running Pylint programmatically
def run_pylint_on_code(code: str) -> str:
    """
    Runs pylint on a given string of Python code.
    """
    if not HAS_PYLINT:
        return "Pylint not installed. Cannot run programmatic test."
        
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file_name = f.name
        
    pylint_output = io.StringIO()
    reporter = TextReporter(pylint_output)
    
    try:
        Run([temp_file_name, '--disable=missing-module-docstring'], reporter=reporter, exit=False)
    finally:
        os.remove(temp_file_name)
        
    return pylint_output.getvalue()

# Advanced Implementation: Custom Pylint Checker Concept (Simulation)
class CustomLinter(ast.NodeVisitor):
    """
    A custom AST-based linter that checks if functions have docstrings.
    """
    def __init__(self) -> None:
        self.issues: List[str] = []
        
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if not ast.get_docstring(node):
            self.issues.append(f"Function '{node.name}' at line {node.lineno} is missing a docstring.")
        self.generic_visit(node)

def custom_lint(code: str) -> List[str]:
    """Runs the custom linter on the provided code."""
    tree = ast.parse(code)
    linter = CustomLinter()
    linter.visit(tree)
    return linter.issues

# Performance Analysis
def performance_analysis() -> None:
    """Analyzes the performance overhead of parsing AST vs regex."""
    code = "def test():\n    pass\n" * 1000
    
    start = time.time()
    custom_lint(code)
    ast_time = time.time() - start
    
    print(f"AST Parsing & Linting Time (1000 functions): {ast_time:.4f} seconds")

# Edge Cases
# - Syntax errors in the code being linted will cause AST parse failure.
# - Dynamically generated code that pylint cannot analyze fully statically.
# - Circular imports can trigger complex resolution warnings.

# Interview Challenge
"""
Challenge: Write a function that checks if a Python script has any print statements using `ast`.
"""
class PrintChecker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.has_print = False
        
    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            self.has_print = True
        self.generic_visit(node)

def check_for_print(code: str) -> bool:
    tree = ast.parse(code)
    checker = PrintChecker()
    checker.visit(tree)
    return checker.has_print

# Tests
class TestPylintConcepts(unittest.TestCase):
    def test_good_function(self):
        self.assertEqual(good_function(2, 3), 5)
        
    def test_custom_lint(self):
        code = "def foo():\n    pass\ndef bar():\n    '''docstring'''\n    pass"
        issues = custom_lint(code)
        self.assertEqual(len(issues), 1)
        self.assertIn("foo", issues[0])
        
    def test_check_for_print(self):
        self.assertTrue(check_for_print("print('Hello')"))
        self.assertFalse(check_for_print("x = 1"))

if __name__ == "__main__":
    print("Running tests...")
    unittest.main(exit=False)
    print("\nRunning performance analysis...")
    performance_analysis()
