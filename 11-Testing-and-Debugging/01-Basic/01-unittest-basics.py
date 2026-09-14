"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (UNITTEST BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a new function `calculate_tax()`. To test it, they 
# add `print(calculate_tax(100))` to the bottom of their script, run it, look 
# at the terminal, say "looks good", and delete the print statement. Three months 
# later, a different developer modifies the function and accidentally breaks the 
# tax logic. Because there are no automated tests, the bug deploys to Production, 
# resulting in a $50,000 accounting error.
#
# A senior software engineer understands "Test-Driven Development" (TDD). They 
# write a robust, automated Test Suite using Python's `unittest` framework. 
# The test mathematically forces the function to execute against dozens of edge 
# cases (negative numbers, zero, massive integers) and explicitly asserts the 
# correct outcome. If any developer ever breaks the tax logic in the future, 
# the CI/CD pipeline will violently crash, mathematically blocking the code from 
# ever reaching Production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the `unittest.TestCase` architectural inheritance.
# - Execute explicit mathematical assertions (`assertEqual`, `assertRaises`).
# - Architect automated, repeatable validation pipelines.
#
# ==============================================================================
"""

import unittest
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CODE WE ARE TESTING)
# ==============================================================================
# In a real architecture, this code lives in `tax_engine.py` and the tests 
# live in `test_tax_engine.py`. We combine them here for the laboratory.

class FinancialEngine:
    @staticmethod
    def calculate_tax(amount: float, rate: float) -> float:
        """Calculates exact tax, rounding to 2 decimal places."""
        if amount < 0 or rate < 0:
            # We strictly throw a ValueError to prevent negative taxation bugs!
            raise ValueError("Financial parameters cannot be mathematically negative.")
        return round(amount * rate, 2)
        
    @staticmethod
    def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
        """Calculates continuous compounding: A = P * e^(rt)"""
        if principal < 0 or rate < 0 or years < 0:
            raise ValueError("Time and money cannot be negative.")
        result = principal * math.exp(rate * years)
        return round(result, 2)


# ==============================================================================
# 4. THE AUTOMATED TEST SUITE
# ==============================================================================
# Every Test Suite MUST mathematically inherit from `unittest.TestCase`.
# The Python `unittest` runner uses Introspection (Reflection) to automatically 
# find and execute any method that starts with the word `test_`.

class TestFinancialEngine(unittest.TestCase):
    
    # --------------------------------------------------------------------------
    # ARCHITECTURAL LIFECYCLE HOOKS
    # --------------------------------------------------------------------------
    def setUp(self):
        """
        Executes mathematically BEFORE EVERY SINGLE TEST.
        Used to reset the state, boot up dummy databases, or instantiate fresh classes,
        guaranteeing absolute State Isolation between tests.
        """
        self.engine = FinancialEngine()
        
    def tearDown(self):
        """
        Executes mathematically AFTER EVERY SINGLE TEST.
        Used to close database connections or wipe temp files.
        """
        pass # Not needed for pure math tests
        
    # --------------------------------------------------------------------------
    # THE TESTS
    # --------------------------------------------------------------------------
    def test_calculate_tax_standard(self):
        """Mathematically verifies a standard, expected input."""
        # 10% tax on $100 should be exactly $10.00
        result = self.engine.calculate_tax(100.0, 0.10)
        self.assertEqual(result, 10.0)
        
    def test_calculate_tax_rounding(self):
        """Mathematically verifies edge-case float precision."""
        # $10.555 * 0.10 = $1.0555. It should round to $1.06
        result = self.engine.calculate_tax(10.555, 0.10)
        self.assertEqual(result, 1.06)
        
    def test_calculate_tax_negative_values(self):
        """
        Mathematically verifies that the function violently crashes 
        when fed invalid data. (Defensive Programming Proof)
        """
        # We mathematically assert that a ValueError MUST be thrown!
        with self.assertRaises(ValueError):
            self.engine.calculate_tax(-100.0, 0.10)
            
    def test_calculate_compound_interest(self):
        """Mathematically verifies complex formulas."""
        # A = 1000 * e^(0.05 * 10) = 1648.72
        result = self.engine.calculate_compound_interest(1000.0, 0.05, 10)
        self.assertEqual(result, 1648.72)


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE TEST RUNNER)
# ==============================================================================
def demonstrate_testing():
    section_header("Unit Testing: The Financial Engine")
    
    print("  [EXECUTION] Booting the Automated Test Runner...")
    print("  The runner will use Python Introspection to find and execute 4 isolated tests.\n")
    
    # We hijack the unittest runner to print to the console programmatically
    # instead of halting the entire Python script execution!
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFinancialEngine)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Tests Run: {test_result.testsRun}")
    print(f"  Failures:  {len(test_result.failures)}")
    print(f"  Errors:    {len(test_result.errors)}")
    
    if test_result.wasSuccessful():
        print("  -> [FLAWLESS] The Financial Engine passed all mathematical constraints!")
    else:
        print("  -> [FATAL] The CI/CD pipeline has blocked deployment!")


def run_all_labs():
    demonstrate_testing()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must every test run in absolute 'State Isolation', and how does the `setUp()` method architecturally guarantee this?"
   Senior Answer: "Test Interdependence is the root cause of flaky test suites. If Test A mutates a global variable or modifies a Database row, and Test B runs immediately after, Test B will mathematically fail because it is testing the corrupted state left behind by Test A. By enforcing State Isolation, we mathematically guarantee that the outcome of Test B is identical regardless of whether Test A ran before it, after it, or didn't run at all. The `setUp()` method physically guarantees this by instantiating a brand new, pristine copy of the object (or database connection) into RAM immediately before executing the test function, completely annihilating any lingering state from previous executions."

2. Interviewer: "In Python Unit Testing, what is the architectural difference between a 'Failure' and an 'Error'?"
   Senior Answer: "Assertion vs Crash. A 'Failure' means the code successfully executed from start to finish without crashing, but the mathematical assertion was wrong (e.g., you asserted $2+2=5$). A Failure indicates a logic bug in your business rules. An 'Error' means the Python interpreter violently crashed (e.g., throwing a `TypeError` or `IndexError`) before the code could even reach the assertion line. An Error indicates a catastrophic architectural bug, such as trying to access an invalid dictionary key or calling a method on a `None` type."

3. Interviewer: "Why did we use `with self.assertRaises(ValueError):` instead of wrapping the function in a standard `try/except` block to test the negative tax edge case?"
   Senior Answer: "Architectural Precision and Readability. If we use a manual `try/except` block, the test logic becomes mathematically inverted and verbose. We have to create a boolean flag `crashed = False`, set it to `True` in the `except` block, and then manually assert `True` at the bottom. The Context Manager (`with self.assertRaises`) mathematically delegates that entire flow directly to the CPython interpreter. It executes the contained code, intercepts the specific Exception, verifies its exact class type, and passes the test—all in a single highly-optimized line of code, preventing false positives where the test accidentally passes because the function returned `None` instead of crashing."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Unittest Basics) Completed.")
