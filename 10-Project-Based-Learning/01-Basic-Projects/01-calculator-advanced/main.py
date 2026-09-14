"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (ADVANCED OOP CALCULATOR)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a calculator using a massive 500-line `if/elif/else` 
# block to handle every possible mathematical operation. When the client asks 
# them to add "Matrix Multiplication", the developer must crack open the core 
# execution logic, accidentally deleting the "Division" logic in the process. 
# The application crashes in Production.
#
# A senior software architect builds a calculator using the "Strategy Design Pattern" 
# and the Open-Closed Principle (SOLID). They mathematically decouple the 
# "Execution Engine" from the "Mathematical Operations". When the client asks 
# for Matrix Multiplication, the architect writes a standalone Plugin, injects 
# it into the Engine's Registry without touching a single line of core logic, 
# and deploys flawlessly in 3 minutes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Strategy Design Pattern via Abstract Base Classes (ABC).
# - Understand the Open-Closed Principle (OCP) in OOP.
# - Execute a robust Unit Testing suite for business logic verification.
#
# ==============================================================================
"""

import math
from abc import ABC, abstractmethod
import unittest
from typing import Dict, Union

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE ARCHITECTURAL INTERFACE (THE STRATEGY)
# ==============================================================================
class CalculationError(Exception):
    """Custom exception for domain-specific mathematical errors."""
    pass

class Operation(ABC):
    """
    THE ABSTRACT BASE CLASS (The Strategy Interface)
    This is a mathematical blueprint. Any class that inherits from this MUST 
    implement the `execute` method, or Python will violently crash at instantiation.
    """
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass


# ==============================================================================
# 4. THE CONCRETE STRATEGIES (THE PLUGINS)
# ==============================================================================
# Notice how each mathematical operation is completely physically isolated!
# If `DivideOperation` breaks, `AddOperation` is mathematically immune.

class AddOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class SubtractOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class MultiplyOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class DivideOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            # We strictly prevent the Python Interpreter from throwing a generic ZeroDivisionError.
            # We intercept it and throw our Domain-Specific error!
            raise CalculationError("Mathematical domain error: Division by absolute zero.")
        return a / b

class PowerOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        try:
            return math.pow(a, b)
        except OverflowError:
            raise CalculationError("Mathematical domain error: Float overflow to infinity.")
        except ValueError:
            raise CalculationError("Mathematical domain error: Imaginary numbers not supported.")


# ==============================================================================
# 5. THE CONTEXT ENGINE (THE CALCULATOR)
# ==============================================================================
class AdvancedCalculator:
    """
    THE EXECUTION ENGINE
    This class has absolutely zero knowledge of how to perform addition or subtraction.
    It merely holds a Dictionary (Registry) of available operations and routes 
    the data to them blindly.
    """
    def __init__(self):
        # The Registry!
        self._operations: Dict[str, Operation] = {}
        self._boot_default_plugins()

    def _boot_default_plugins(self):
        """Automatically registers the standard library of math plugins."""
        self.register_plugin('+', AddOperation())
        self.register_plugin('-', SubtractOperation())
        self.register_plugin('*', MultiplyOperation())
        self.register_plugin('/', DivideOperation())
        self.register_plugin('^', PowerOperation())

    def register_plugin(self, symbol: str, operation: Operation):
        """
        THE OPEN-CLOSED PRINCIPLE
        We can dynamically inject new mathematical logic into the Engine at runtime 
        without ever modifying the Engine's source code!
        """
        if not isinstance(operation, Operation):
            raise TypeError("Fatal Architecture Error: Plugin must inherit from Operation ABC.")
        self._operations[symbol] = operation

    def execute_math(self, a: Union[int, float], symbol: str, b: Union[int, float]) -> float:
        """The Router."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
             raise TypeError("Engine Error: Operands must be strictly numeric.")

        target_plugin = self._operations.get(symbol)
        
        if not target_plugin:
            raise CalculationError(f"Engine Error: Unknown symbol '{symbol}'.")
        
        # We blindly execute the plugin! Polymorphism at its finest!
        return target_plugin.execute(float(a), float(b))


# ==============================================================================
# 6. MATHEMATICAL PROOF (UNIT TESTS)
# ==============================================================================
class TestAdvancedCalculator(unittest.TestCase):
    """Architectural Unit Testing Suite"""
    
    def setUp(self):
        # Boot a fresh engine for every single test mathematically guaranteeing State Isolation!
        self.engine = AdvancedCalculator()

    def test_core_plugins(self):
        self.assertEqual(self.engine.execute_math(5, '+', 3), 8.0)
        self.assertEqual(self.engine.execute_math(10, '-', 4), 6.0)
        self.assertEqual(self.engine.execute_math(4, '*', 3), 12.0)
        self.assertEqual(self.engine.execute_math(10, '/', 2), 5.0)
        self.assertEqual(self.engine.execute_math(2, '^', 3), 8.0)

    def test_zero_division_interception(self):
        with self.assertRaises(CalculationError):
            self.engine.execute_math(10, '/', 0)

    def test_dynamic_plugin_injection(self):
        # We define a brand new plugin on the fly!
        class ModuloPlugin(Operation):
            def execute(self, a: float, b: float) -> float:
                return a % b
                
        # We inject it into the Engine!
        self.engine.register_plugin('%', ModuloPlugin())
        
        # We mathematically prove the Engine can route to the new Plugin!
        self.assertEqual(self.engine.execute_math(10, '%', 3), 1.0)


def run_all_labs():
    section_header("Project: Advanced OOP Calculator (Strategy Pattern)")
    print("  [EXECUTION] Booting the Unit Testing Suite...")
    
    # We hijack the unittest runner to print to the console programmatically
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvancedCalculator)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  The Calculator Engine successfully executed mathematical plugins")
    print("  and dynamically accepted a new Modulo Plugin at runtime without")
    print("  altering its core source code.")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we use an `Abstract Base Class` (ABC) for the Operation, instead of just using a normal Python class with an `execute` method?"
   Senior Answer: "Architectural Enforcement. If we use a normal Python class, a junior developer could create a `ModuloPlugin`, forget to name the method `execute` (maybe they name it `run_math`), inject it into the Engine, and crash the system in Production when the Engine blindly calls `.execute()`. By inheriting from an ABC with an `@abstractmethod`, Python mathematically intercepts the compilation. If the junior developer forgets to implement `execute`, the Python Interpreter will violently crash the exact millisecond they try to instantiate `ModuloPlugin`, guaranteeing the bug is caught in Development, not Production."

2. Interviewer: "What is the Open-Closed Principle (OCP), and how does the `register_plugin` method physically satisfy it?"
   Senior Answer: "The 'O' in SOLID dictates that a software entity must be Open for Extension, but Closed for Modification. In a basic calculator, if you want to add Modulo, you must physically open `calculator.py`, find the `if` block, modify the core logic, and risk breaking addition. By using a Registry Dictionary (`self._operations`), the Engine is mathematically 'Closed' (we never touch the core `execute_math` routing function again). Yet, it is infinitely 'Open' for extension because we can dynamically inject a million new plugins into the dictionary at runtime via `register_plugin`."

3. Interviewer: "Why is `isinstance(a, (int, float))` critical before routing the data to the plugins?"
   Senior Answer: "To prevent 'Poison Pills'. In Python's dynamic typing system, a user could pass a String `\"Hello\"` and an Integer `3` into the multiplier. Python strings natively support multiplication (`\"Hello\" * 3` becomes `\"HelloHelloHello\"`). If the Engine blindly routes this to the `MultiplyOperation`, the calculator will return a string instead of a float, catastrophically crashing the downstream financial systems that mathematically expect a float. The Engine acts as a strict firewall, sanitizing the Types *before* the plugins are executed, ensuring mathematical integrity across the entire architecture."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Advanced Calculator) Completed.")
