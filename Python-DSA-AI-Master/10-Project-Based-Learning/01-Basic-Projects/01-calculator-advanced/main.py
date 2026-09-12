"""
Advanced Calculator Project Implementation

This module provides an advanced calculator implementation in Python, utilizing 
Object-Oriented Programming (OOP) principles, the Strategy design pattern, 
comprehensive error handling, and unit testing.

# Educational Content

## What is this and why does it exist?
A calculator is a foundational project for software engineering beginners. However, an 
"advanced" calculator goes beyond simple functions. It introduces architectural concepts 
like extensibility (adding new operations without modifying existing code), robust error 
handling (preventing application crashes on bad input), and unit testing (proving the 
code works). In industry, similar architectures are used for processing pipelines, 
rule engines, and plugin systems.

## Beginner Explanation
Imagine you have a machine that can only do one thing at a time: add, subtract, multiply, 
or divide. In a basic script, you might use a lot of `if-elif` statements to figure out 
which operation the user wants. In this advanced version, we create a blueprint (an interface) 
for what an "operation" should look like. Then we create separate modules for each operation. 
This keeps our code organized and makes it easy to add new features later.

## Deep Technical Explanation (Advanced)
This implementation employs the Strategy Design Pattern. We define an abstract base class 
`Operation` which acts as our strategy interface. Concrete strategies (`AddOperation`, 
`DivideOperation`, etc.) implement the specific logic. The `Calculator` context class maintains 
a registry of available strategies and delegates execution to them. This adheres to the 
Open-Closed Principle (OCP) of SOLID: the system is open for extension (by adding new 
operations) but closed for modification (the core calculator logic doesn't change).

## Common Mistakes & Considerations
- Floating-Point Inaccuracy: `0.1 + 0.2` in Python doesn't equal `0.3` exactly due to 
  IEEE 754 representation. For financial applications, `decimal.Decimal` is preferred 
  over native floats.
- Division by Zero: Failing to handle `ZeroDivisionError` is a classic bug. 
- Input Sanitization: In a real-world app, raw input eval (like `eval()`) is a critical 
  security vulnerability. Never use `eval()` on user input.

## Interview Questions
1. How would you handle a continuous stream of calculations (like a running total)?
2. Why is the Strategy pattern better than a giant switch/case or if/elif block here?
3. How do you mitigate floating point precision issues in Python?

## Practical Exercise
- Add a `PowerOperation` (x^y) and a `ModuloOperation` (x%y).
- Integrate the `logging` module to keep an audit trail of all calculations performed.
- Modify the calculator to accept an unlimited number of arguments.
"""

import math
from abc import ABC, abstractmethod
import unittest
from typing import Dict, Union, Type

# --- Core Business Logic ---

class CalculationError(Exception):
    """Custom exception for errors during calculation."""
    pass


class Operation(ABC):
    """
    Abstract Base Class representing a mathematical operation.
    This acts as the interface for the Strategy pattern.
    """
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Executes the operation on two operands."""
        pass


class AddOperation(Operation):
    """Concrete strategy for addition."""
    def execute(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    """Concrete strategy for subtraction."""
    def execute(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    """Concrete strategy for multiplication."""
    def execute(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    """Concrete strategy for division."""
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise CalculationError("Division by zero is mathematically undefined and not allowed.")
        return a / b


class PowerOperation(Operation):
    """Concrete strategy for exponentiation."""
    def execute(self, a: float, b: float) -> float:
        try:
            return math.pow(a, b)
        except OverflowError:
            raise CalculationError("Result too large to be represented.")
        except ValueError:
            raise CalculationError("Math domain error (e.g., negative number to a fractional power).")


class Calculator:
    """
    The Context class that delegates execution to the registered operations.
    Maintains a registry of available operations.
    """
    def __init__(self):
        self._operations: Dict[str, Operation] = {}
        self._register_default_operations()

    def _register_default_operations(self):
        """Registers the basic math operations upon initialization."""
        self.register_operation('+', AddOperation())
        self.register_operation('-', SubtractOperation())
        self.register_operation('*', MultiplyOperation())
        self.register_operation('/', DivideOperation())
        self.register_operation('^', PowerOperation())

    def register_operation(self, symbol: str, operation: Operation):
        """
        Registers a new operation, demonstrating the Open-Closed Principle.
        
        Args:
            symbol (str): The string symbol used to trigger the operation (e.g., '+').
            operation (Operation): An instance of a class derived from Operation.
        """
        if not isinstance(operation, Operation):
            raise TypeError("operation must be an instance of a subclass of Operation.")
        self._operations[symbol] = operation

    def calculate(self, a: Union[int, float], symbol: str, b: Union[int, float]) -> float:
        """
        Performs the calculation using the registered strategy.
        
        Args:
            a: First operand.
            symbol: The operation symbol.
            b: Second operand.
            
        Returns:
            float: The result of the calculation.
            
        Raises:
            CalculationError: If the operation fails or the symbol is unknown.
            TypeError: If operands are not numeric.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
             raise TypeError("Operands must be numeric types (int or float).")

        operation = self._operations.get(symbol)
        if not operation:
            raise CalculationError(f"Unsupported operation symbol: '{symbol}'. Available: {list(self._operations.keys())}")
        
        return operation.execute(float(a), float(b))

# --- Unit Tests ---

class TestCalculator(unittest.TestCase):
    """Unit test suite for the Calculator application."""
    
    def setUp(self):
        """Runs before every test method."""
        self.calc = Calculator()

    def test_addition(self):
        self.assertEqual(self.calc.calculate(5, '+', 3), 8.0)
        self.assertEqual(self.calc.calculate(-5, '+', 3), -2.0)

    def test_subtraction(self):
        self.assertEqual(self.calc.calculate(10, '-', 4), 6.0)
        self.assertEqual(self.calc.calculate(5.5, '-', 2.5), 3.0)

    def test_multiplication(self):
        self.assertEqual(self.calc.calculate(4, '*', 3), 12.0)
        self.assertEqual(self.calc.calculate(-2, '*', 5), -10.0)

    def test_division(self):
        self.assertEqual(self.calc.calculate(10, '/', 2), 5.0)
        self.assertEqual(self.calc.calculate(5, '/', 2), 2.5)

    def test_division_by_zero(self):
        with self.assertRaises(CalculationError) as context:
            self.calc.calculate(10, '/', 0)
        self.assertTrue("Division by zero" in str(context.exception))

    def test_power(self):
        self.assertEqual(self.calc.calculate(2, '^', 3), 8.0)
        self.assertEqual(self.calc.calculate(9, '^', 0.5), 3.0)

    def test_invalid_symbol(self):
        with self.assertRaises(CalculationError):
            self.calc.calculate(5, '%', 3)

    def test_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.calculate("5", '+', 3)
            
    def test_custom_operation_registration(self):
        class ModuloOperation(Operation):
            def execute(self, a: float, b: float) -> float:
                return a % b
                
        self.calc.register_operation('%', ModuloOperation())
        self.assertEqual(self.calc.calculate(10, '%', 3), 1.0)

if __name__ == '__main__':
    # When run directly, execute the tests.
    unittest.main()
