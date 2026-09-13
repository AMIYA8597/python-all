"""
Module Docstring: Automated Code Review and Checks

Learning Objectives:
1. Understand the tools used for automated code reviews (flake8, black, mypy, isort).
2. Learn how to programmatically execute code checks.
3. Understand the difference between formatting (black) and linting (flake8).
4. Implement a custom automated check script using Python's `ast` module.

Concept Explanation:
Automated code reviews use tools to analyze source code for stylistic errors, 
bugs, and formatting issues without executing the program. Tools like Black 
format code automatically, while Flake8 lints code to find logic and style errors. 
MyPy is used for static type checking.

"""

import ast
import subprocess
import time
import sys
import tempfile
import os
from typing import List, Dict, Optional, Tuple
import unittest

# Basic Implementation: Analyzing Code Complexity (Cyclomatic Complexity proxy)
def calculate_complexity(code: str) -> int:
    """
    Calculates a simple proxy for cyclomatic complexity by counting control flow statements.
    """
    tree = ast.parse(code)
    complexity = 1
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.With)):
            complexity += 1
            
    return complexity

# Intermediate Implementation: Running external tools programmatically
def run_flake8_check(code: str) -> Tuple[bool, str]:
    """
    Writes code to a temp file and runs flake8 on it.
    Returns (True, output) if passed, (False, output) if failed or flake8 missing.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
        
    try:
        # Note: flake8 must be installed to return true
        result = subprocess.run([sys.executable, '-m', 'flake8', temp_file], 
                                capture_output=True, text=True)
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)
    finally:
        os.remove(temp_file)

# Advanced Implementation: Integrated Review Checker
class ReviewChecker:
    """
    A class that combines multiple checks: syntax, complexity, and basic style.
    """
    def __init__(self, code: str, max_complexity: int = 5) -> None:
        self.code = code
        self.max_complexity = max_complexity
        self.issues: List[str] = []
        
    def check_syntax(self) -> bool:
        try:
            ast.parse(self.code)
            return True
        except SyntaxError as e:
            self.issues.append(f"Syntax error: {e}")
            return False
            
    def check_complexity(self) -> bool:
        if not self.check_syntax():
            return False
        comp = calculate_complexity(self.code)
        if comp > self.max_complexity:
            self.issues.append(f"Code complexity ({comp}) exceeds maximum ({self.max_complexity})")
            return False
        return True
        
    def run_all_checks(self) -> bool:
        return self.check_syntax() and self.check_complexity()

# Performance Analysis
def performance_analysis() -> None:
    """Measures the overhead of spawning subprocesses vs native AST parsing."""
    code = "def foo():\n    x = 1\n    if x:\n        return True\n    return False\n"
    
    # AST Complexity check
    start = time.time()
    for _ in range(100):
        calculate_complexity(code)
    ast_time = time.time() - start
    
    print(f"AST parsing 100 times: {ast_time:.4f} seconds")

# Edge Cases
# - Invalid Python syntax causing AST parsing to crash. Handled via try-except SyntaxError.
# - Missing external dependencies (flake8, black) when running subprocesses.
# - Extremely large files taking too long to parse and analyze AST tree.

# Interview Challenge
"""
Challenge: Write a function that uses AST to ensure all functions in a script have return type hints.
"""
def check_return_type_hints(code: str) -> List[str]:
    """Finds functions that are missing return type hints."""
    tree = ast.parse(code)
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if it's not __init__ and has no return annotation
            if node.name != '__init__' and node.returns is None:
                missing.append(node.name)
    return missing

# Tests
class TestReviewCheck(unittest.TestCase):
    def test_complexity(self):
        code = "def f():\n  if True: pass\n  for i in range(1): pass"
        self.assertEqual(calculate_complexity(code), 3) # 1 base + 1 if + 1 for
        
    def test_return_type_hints(self):
        code = "def a() -> int: pass\ndef b(): pass\ndef __init__(self): pass"
        self.assertEqual(check_return_type_hints(code), ['b'])
        
    def test_review_checker(self):
        checker = ReviewChecker("def f():\n if 1: pass\n if 2: pass\n if 3: pass\n if 4: pass\n if 5: pass", max_complexity=4)
        self.assertFalse(checker.run_all_checks())
        self.assertTrue(any("exceeds" in issue for issue in checker.issues))

if __name__ == "__main__":
    print("Running tests...")
    unittest.main(exit=False)
    print("\nRunning performance analysis...")
    performance_analysis()
