"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (TEST AUTOMATION & TDD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer writes a complex banking function. They test it by adding a 
# `print()` statement at the bottom, running the script, reading the terminal, 
# and saying "looks good." A month later, they modify a different part of the 
# file, accidentally breaking the banking function. They deploy to Production 
# because they didn't manually run the `print()` statement again. The bank 
# loses $50,000.
#
# A senior engineer understands "Test-Driven Development" (TDD) and CI/CD. 
# They use `pytest`. They write a dedicated Python script that mathematically 
# asserts the absolute perfection of the banking function under 50 different 
# edge cases (negative numbers, floats, strings). This script is wired to GitHub 
# Actions. The exact second any developer attempts to merge broken code, the 
# automated testing suite mathematically rejects the code, rendering it physically 
# impossible to deploy a regression to Production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of the `pytest` framework.
# - Execute algorithmic Edge Case validation (`assert`).
# - Master Fixtures and Parameterization for scalable test matrices.
#
# ==============================================================================
"""

import math
import pytest

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TARGET BUSINESS LOGIC (THE BANKING ENGINE)
# ==============================================================================
class InsufficientFundsError(Exception):
    pass

class BankAccount:
    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.balance = float(initial_balance)
        
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        
    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(f"Cannot withdraw {amount}. Balance is {self.balance}.")
        self.balance -= amount


# ==============================================================================
# 4. THE AUTOMATED TESTING SUITE (PYTEST ARCHITECTURE)
# ==============================================================================
# In a real repository, these functions would live in a separate file named `test_bank.py`.
# Pytest automatically scans the directory for files starting with `test_` and 
# functions starting with `test_`.

# --- 1. BASIC ASSERTIONS ---
def test_initial_balance():
    """Mathematically guarantees the constructor sets the correct state."""
    account = BankAccount(100.50)
    # The `assert` keyword is Python's native validation. If it evaluates to False,
    # it violently throws an AssertionError and the CI/CD pipeline fails!
    assert account.balance == 100.50

def test_valid_deposit():
    """Mathematically guarantees addition logic."""
    account = BankAccount(50.0)
    account.deposit(25.0)
    assert account.balance == 75.0


# --- 2. TESTING EXCEPTIONS (EDGE CASES) ---
def test_negative_deposit():
    """Mathematically guarantees that the system REJECTS bad data."""
    account = BankAccount(100.0)
    
    # We use a Context Manager (`pytest.raises`) to catch the expected exception!
    # If the `deposit` function DOES NOT throw a ValueError, this test FAILS!
    with pytest.raises(ValueError):
        account.deposit(-50.0)

def test_overdraft_protection():
    """Mathematically guarantees the bank doesn't lose money."""
    account = BankAccount(100.0)
    
    with pytest.raises(InsufficientFundsError) as exc_info:
        account.withdraw(500.0)
        
    # We can even assert the exact error message!
    assert "Cannot withdraw 500.0" in str(exc_info.value)


# --- 3. FIXTURES (STATE INJECTION) ---
# A Fixture is a mathematically pure Dependency Injection mechanism.
# Instead of writing `account = BankAccount(1000)` in every single test, 
# Pytest automatically injects this object into any test that requests it!
@pytest.fixture
def rich_account():
    """Yields a heavily funded account for advanced testing."""
    return BankAccount(100_000.0)

def test_massive_withdrawal(rich_account):
    """The `rich_account` fixture was dynamically injected by Pytest!"""
    rich_account.withdraw(90_000.0)
    assert rich_account.balance == 10_000.0


# --- 4. PARAMETERIZATION (THE TEST MATRIX) ---
# Testing one deposit is weak. What if we want to test 5 different scenarios?
# Parameterization mathematically runs this single function 5 different times 
# with 5 different mathematical inputs!
@pytest.mark.parametrize("initial, deposit, expected", [
    (0.0,   100.0, 100.0),
    (50.0,  50.0,  100.0),
    (0.99,  0.01,  1.00),
    (100.0, 0.001, 100.001), # Float precision check!
])
def test_multiple_deposit_scenarios(initial, deposit, expected):
    """Executes the test matrix."""
    account = BankAccount(initial)
    account.deposit(deposit)
    # Using `math.isclose` instead of `==` due to IEEE 754 Float precision errors!
    assert math.isclose(account.balance, expected, rel_tol=1e-9)


# ==============================================================================
# 5. SIMULATING THE PYTEST RUNNER
# ==============================================================================
def demonstrate_pytest():
    section_header("Test Automation: Pytest Pipeline")
    
    print("  [ERROR] This file is designed to be executed via `pytest`!")
    print("  Command: `pytest -v 04-testing-auto.py`\n")
    
    print("  [SIMULATED PYTEST OUTPUT]")
    print("  ============================= test session starts ==============================")
    print("  platform win32 -- Python 3.10.0, pytest-7.4.0")
    print("  collected 9 items")
    print("\n  04-testing-auto.py::test_initial_balance PASSED                       [ 11%]")
    print("  04-testing-auto.py::test_valid_deposit PASSED                         [ 22%]")
    print("  04-testing-auto.py::test_negative_deposit PASSED                      [ 33%]")
    print("  04-testing-auto.py::test_overdraft_protection PASSED                  [ 44%]")
    print("  04-testing-auto.py::test_massive_withdrawal PASSED                    [ 55%]")
    print("  04-testing-auto.py::test_multiple_deposit_scenarios[0.0-100.0-100.0] PASSED [ 66%]")
    print("  04-testing-auto.py::test_multiple_deposit_scenarios[50.0-50.0-100.0] PASSED [ 77%]")
    print("  04-testing-auto.py::test_multiple_deposit_scenarios[0.99-0.01-1.0] PASSED   [ 88%]")
    print("  04-testing-auto.py::test_multiple_deposit_scenarios[100.0-0.001-100.001] PASSED [100%]")
    print("\n  ============================== 9 passed in 0.04s ===============================")
    
    print("\n  [ANALYSIS]")
    print("  The Business Logic has been mathematically proven against 9 edge cases.")
    print("  If a Junior Engineer alters the `deposit` function to allow negative numbers,")
    print("  the `test_negative_deposit` function will violently fail during the CI/CD")
    print("  build, blocking the deployment to Production and saving the Bank.")


def run_all_labs():
    demonstrate_pytest()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we use a testing framework like `pytest` instead of just writing standard `assert` statements at the bottom of our `main.py` script?"
   Senior Answer: "If you place `assert` statements at the bottom of a standard script, the execution is completely linear and catastrophic. If the very first assertion fails, the Python interpreter throws an `AssertionError` and instantly terminates the entire OS process. You never find out if the remaining $49$ assertions passed or failed. You are forced to fix bugs one at a time. The `pytest` framework mathematically alters this architecture. It discovers all $50$ tests, dynamically executes them in isolated logical sandboxes, intercepts all exceptions, and generates a comprehensive, formatted final report detailing exactly which tests failed, what the expected variables were vs the actual variables, and provides a full stack trace for each failure."

2. Interviewer: "What is a `pytest.fixture`, and how does it solve the problem of 'Test State Pollution'?"
   Senior Answer: "If Test A modifies a global `BankAccount` object, and Test B reads that same global object, you have created a 'State Dependency' (Test Pollution). If Test B runs before Test A, it passes; if it runs after, it fails. Tests must be mathematically isolated. A Fixture (`@pytest.fixture`) acts as a Dependency Injection Factory. Instead of using global variables, a test function requests the fixture via a parameter (e.g., `def test_deposit(account_fixture):`). Pytest dynamically executes the fixture function, generates a brand new, mathematically pure instance of the object in RAM, and injects it into that specific test. When the test finishes, the object is destroyed. This guarantees absolute state isolation for thousands of concurrent tests."

3. Interviewer: "Explain the concept of TDD (Test-Driven Development) and the 'Red, Green, Refactor' cycle."
   Senior Answer: "TDD is an architectural paradigm where you write the mathematical Proof of Execution *before* you write the actual business logic. 1) Red Phase: You write `test_deposit()`, which attempts to call a `deposit()` function that doesn't physically exist yet. You run `pytest`, and it mathematically fails (Red) because the code is missing. 2) Green Phase: You write the absolute minimum amount of messy, terrible business logic required to make the test pass (Green). 3) Refactor Phase: Now that the mathematical safety net is fully operational and glowing Green, you can confidently rewrite, optimize, and clean up the messy business logic, knowing that if you accidentally break anything, the test will instantly flip back to Red, warning you of the regression."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Automation (Pytest) Completed.")
