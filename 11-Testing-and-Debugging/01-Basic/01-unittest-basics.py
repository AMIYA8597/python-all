"""
## A. Concept Name
Unittest Basics

## B. Motivation
Testing is crucial to ensure that code behaves as expected and to prevent regressions when modifying code.

## C. Core Idea
The `unittest` module in Python provides a rich set of tools for constructing and running tests. It is inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages.

## D. Setup and Configuration
Tests are created by subclassing `unittest.TestCase`. The framework automatically runs methods that start with the word `test`.

## E. Assertions
Assertions are the core of tests. Methods like `assertEqual()`, `assertTrue()`, `assertFalse()`, and `assertRaises()` check for expected outcomes.

## F. Test Fixtures
Fixtures provide a baseline state for tests. `setUp()` runs before each test method, and `tearDown()` runs after.

## G. Test Suites
Multiple test cases can be aggregated into test suites, though test discovery often handles this automatically.

## H. Test Runner
The component that orchestrates the execution of tests and provides the outcome to the user.

## I. Mocking Basics
While part of `unittest.mock`, mocking allows replacing parts of your system under test with mock objects.

## J. Command-Line Interface
Tests can be run from the command line using `python -m unittest`.

## K. Test Discovery
The `unittest` module can automatically discover tests in your project using `python -m unittest discover`.

## L. Skipping Tests
Tests can be skipped using decorators like `@unittest.skip("reason")`.

## M. Expected Failures
Tests that are known to fail can be marked with `@unittest.expectedFailure`.

## N. Subtests
Subtests allow running a test with multiple varying inputs without failing the whole test on the first failure, using `self.subTest()`.

## O. Parameterized Tests
Running the same test logic with different parameters. (Often done with subtests or external libraries).

## P. Integration vs Unit Tests
Understanding the scope: unit tests check isolated components, while integration tests check their interactions.

## Q. Code Coverage
Measuring how much of your code is executed by your tests (typically using the `coverage` package).

## R. Best Practices
Keep tests fast, isolated, repeatable, and independent. Name tests clearly.

## S. Common Pitfalls
Testing implementation details instead of behavior, or writing tests that are too brittle.

## T. Advanced Fixtures
Class-level fixtures `setUpClass()` and `tearDownClass()`, or module-level `setUpModule()` and `tearDownModule()`.

## U. Continuous Integration
Running tests automatically on a CI/CD server whenever code is pushed.

## V. Debugging Tests
Using `print`, logging, or debugging tools (like `pdb`) when a test fails unexpectedly.

## W. Performance Testing
Basic profiling or timing of test execution, though usually handled by specialized tools.

## X. Project Connection
Understanding `unittest` basics is foundational for the AI projects in this masterclass, ensuring that data processing algorithms and machine learning pipelines are robust and error-free.
"""

import unittest

def add(a, b):
    """Adds two numbers."""
    return a + b

def divide(a, b):
    """Divides first number by the second. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestMathOperations(unittest.TestCase):
    
    def setUp(self):
        """This method is called before each test."""
        self.a = 10
        self.b = 5

    def tearDown(self):
        """This method is called after each test."""
        pass

    def test_add(self):
        """Test the add functionality."""
        self.assertEqual(add(self.a, self.b), 15)
        
    def test_divide(self):
        """Test the divide functionality."""
        self.assertEqual(divide(self.a, self.b), 2.0)
        
    def test_divide_by_zero(self):
        """Test division by zero raises appropriate error."""
        with self.assertRaises(ValueError):
            divide(self.a, 0)

if __name__ == '__main__':
    unittest.main()
