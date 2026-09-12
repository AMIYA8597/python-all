"""
Python `unittest` Framework - Educational Script

Learning Objectives:
1. Understand the core concepts of unit testing.
2. Learn how to use Python's built-in `unittest` module.
3. Master test cases, test suites, test runners, and assertions.
4. Understand how to use setUp and tearDown methods for test fixtures.
5. Learn how to mock dependencies using `unittest.mock`.

Concept Explanation:
The `unittest` module provides a rich set of tools for constructing and running tests.
It supports test automation, sharing of setup and shutdown code for tests,
aggregation of tests into collections, and independence of the tests from the reporting framework.

Key Components:
- Test Fixture: Preparation needed to perform tests, and any associated cleanup actions.
- Test Case: The individual unit of testing. It checks for a specific response to a particular set of inputs.
- Test Suite: A collection of test cases, test suites, or both.
- Test Runner: A component which orchestrates the execution of tests and provides the outcome to the user.
"""

import unittest
from unittest.mock import MagicMock, patch
from typing import List, Dict, Any, Optional
import time

# --- Basic Implementation: Simple Functions to Test ---

def add(a: int, b: int) -> int:
    """Returns the sum of two integers."""
    return a + b

def divide(a: float, b: float) -> float:
    """Returns the quotient of two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

class TestBasicFunctions(unittest.TestCase):
    """Test cases for basic math functions."""
    
    def test_add(self) -> None:
        """Test the add function with various inputs."""
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)
        
    def test_divide(self) -> None:
        """Test the divide function and its exceptions."""
        self.assertEqual(divide(10, 2), 5.0)
        self.assertAlmostEqual(divide(10, 3), 3.3333333, places=5)
        
        # Test exception
        with self.assertRaises(ValueError):
            divide(10, 0)

# --- Intermediate Implementation: Classes and Fixtures ---

class BankAccount:
    """A simple bank account class to demonstrate stateful testing."""
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance
        
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        
    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        self.balance -= amount

class TestBankAccount(unittest.TestCase):
    """Test cases for the BankAccount class using setUp and tearDown fixtures."""
    
    def setUp(self) -> None:
        """Runs before each test method."""
        self.account = BankAccount("Alice", 100.0)
        
    def tearDown(self) -> None:
        """Runs after each test method."""
        self.account = None # type: ignore
        
    def test_deposit(self) -> None:
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)
        
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)
            
    def test_withdraw(self) -> None:
        self.account.withdraw(40.0)
        self.assertEqual(self.account.balance, 60.0)
        
        with self.assertRaises(ValueError):
            self.account.withdraw(200.0)

# --- Advanced Implementation: Mocking Dependencies ---

class ExternalAPI:
    """Simulates an external API."""
    def fetch_data(self, user_id: int) -> Dict[str, Any]:
        time.sleep(1) # Simulate network delay
        return {"id": user_id, "name": "User Data", "status": "active"}

class DataProcessor:
    """Processes data from an external API."""
    def __init__(self, api: ExternalAPI) -> None:
        self.api = api
        
    def get_user_status(self, user_id: int) -> str:
        data = self.api.fetch_data(user_id)
        return data.get("status", "unknown")

class TestDataProcessor(unittest.TestCase):
    """Test cases demonstrating mocking."""
    
    @patch.object(ExternalAPI, 'fetch_data')
    def test_get_user_status_with_mock(self, mock_fetch: MagicMock) -> None:
        """Test DataProcessor without hitting the real API (which is slow)."""
        # Configure the mock to return specific data
        mock_fetch.return_value = {"id": 1, "status": "inactive"}
        
        api = ExternalAPI()
        processor = DataProcessor(api)
        status = processor.get_user_status(1)
        
        self.assertEqual(status, "inactive")
        mock_fetch.assert_called_once_with(1)

# --- Performance Analysis ---
# Unittest is generally fast for isolated unit tests.
# Performance issues usually arise from test dependencies (like DB or network calls)
# which is why mocking is crucial for fast test suites.

# --- Edge Cases ---
# Floating point comparisons can fail due to precision issues -> use assertAlmostEqual.
# Exception messages should sometimes be verified -> use assertRaisesRegex.

# --- Interview Challenge ---
# Challenge: Write a test for a function that reads a file and returns its lines.
# Requirements: Mock the built-in `open` function so no real file is needed.

def read_file_lines(filepath: str) -> List[str]:
    with open(filepath, 'r') as f:
        return f.readlines()

class TestFileReading(unittest.TestCase):
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="line1\nline2\n")
    def test_read_file_lines(self, mock_file: MagicMock) -> None:
        lines = read_file_lines("dummy.txt")
        self.assertEqual(lines, ["line1\n", "line2\n"])
        mock_file.assert_called_once_with("dummy.txt", 'r')

if __name__ == "__main__":
    # In a real environment, you might use: unittest.main()
    # Here, we run tests verbosely programmatically to show output.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBasicFunctions))
    suite.addTest(unittest.makeSuite(TestBankAccount))
    suite.addTest(unittest.makeSuite(TestDataProcessor))
    suite.addTest(unittest.makeSuite(TestFileReading))
    
    runner = unittest.TextTestRunner(verbosity=2)
    print("Running unittest suite...\n")
    runner.run(suite)
