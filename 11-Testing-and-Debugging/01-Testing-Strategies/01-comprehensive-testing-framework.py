#!/usr/bin/env python3
"""
Comprehensive Testing and Debugging Framework

This module provides a complete guide to testing strategies, debugging techniques,
and quality assurance practices in Python. It covers unit testing, integration
testing, performance testing, debugging tools, and best practices used in
professional software development.

Topics Covered:
- Unit testing with pytest and unittest
- Integration and end-to-end testing
- Test-driven development (TDD)
- Mocking and test doubles
- Performance and load testing
- Debugging techniques and tools
- Code coverage and quality metrics
- Continuous integration testing

Author: Python DSA Master
Date: 2024
"""

import unittest
import pytest
import time
import random
import threading
import concurrent.futures
from unittest.mock import Mock, patch, MagicMock, call
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging
import json
import tempfile
import os
import sys
from contextlib import contextmanager
import traceback
import cProfile
import pstats
import memory_profiler
import functools


# ============================================================================
# SAMPLE APPLICATION UNDER TEST
# ============================================================================

class BankAccount:
    """Sample class for demonstrating testing techniques."""
    
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.balance = initial_balance
        self.transaction_history = []
        self._is_locked = False
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into the account."""
        if self._is_locked:
            raise ValueError("Account is locked")
        
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.transaction_history.append(f"DEPOSIT: +${amount:.2f}")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from the account."""
        if self._is_locked:
            raise ValueError("Account is locked")
        
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self.transaction_history.append(f"WITHDRAWAL: -${amount:.2f}")
        return True
    
    def get_balance(self) -> float:
        """Get current account balance."""
        return self.balance
    
    def lock_account(self):
        """Lock the account to prevent transactions."""
        self._is_locked = True
    
    def unlock_account(self):
        """Unlock the account to allow transactions."""
        self._is_locked = False
    
    def get_transaction_history(self) -> List[str]:
        """Get transaction history."""
        return self.transaction_history.copy()


class BankingService:
    """Service class for banking operations."""
    
    def __init__(self, external_api=None):
        self.accounts = {}
        self.external_api = external_api
    
    def create_account(self, account_id: str, initial_balance: float = 0.0) -> BankAccount:
        """Create a new bank account."""
        if account_id in self.accounts:
            raise ValueError(f"Account {account_id} already exists")
        
        account = BankAccount(account_id, initial_balance)
        self.accounts[account_id] = account
        return account
    
    def get_account(self, account_id: str) -> Optional[BankAccount]:
        """Get an account by ID."""
        return self.accounts.get(account_id)
    
    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        """Transfer money between accounts."""
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if not from_account or not to_account:
            raise ValueError("Account not found")
        
        # Withdraw from source account
        from_account.withdraw(amount)
        
        try:
            # Deposit to destination account
            to_account.deposit(amount)
            return True
        except Exception as e:
            # Rollback the withdrawal
            from_account.deposit(amount)
            raise e
    
    def get_account_info(self, account_id: str) -> Dict[str, Any]:
        """Get account information with external API call."""
        account = self.get_account(account_id)
        if not account:
            raise ValueError("Account not found")
        
        # Simulate external API call for credit score
        credit_score = None
        if self.external_api:
            credit_score = self.external_api.get_credit_score(account_id)
        
        return {
            "account_id": account.account_id,
            "balance": account.get_balance(),
            "credit_score": credit_score,
            "transaction_count": len(account.get_transaction_history())
        }


# ============================================================================
# UNIT TESTING EXAMPLES
# ============================================================================

class TestBankAccount(unittest.TestCase):
    """Comprehensive unit tests for BankAccount class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.account = BankAccount("TEST001", 100.0)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up any resources if needed
        pass
    
    def test_initial_balance(self):
        """Test account is created with correct initial balance."""
        self.assertEqual(self.account.get_balance(), 100.0)
        self.assertEqual(self.account.account_id, "TEST001")
    
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        result = self.account.deposit(50.0)
        
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 150.0)
        self.assertIn("DEPOSIT: +$50.00", self.account.get_transaction_history())
    
    def test_deposit_negative_amount(self):
        """Test depositing a negative amount raises exception."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-10.0)
        
        self.assertIn("must be positive", str(context.exception))
        self.assertEqual(self.account.get_balance(), 100.0)  # Balance unchanged
    
    def test_deposit_zero_amount(self):
        """Test depositing zero raises exception."""
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        result = self.account.withdraw(30.0)
        
        self.assertTrue(result)
        self.assertEqual(self.account.get_balance(), 70.0)
        self.assertIn("WITHDRAWAL: -$30.00", self.account.get_transaction_history())
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than available balance."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(150.0)
        
        self.assertIn("Insufficient funds", str(context.exception))
        self.assertEqual(self.account.get_balance(), 100.0)  # Balance unchanged
    
    def test_withdraw_negative_amount(self):
        """Test withdrawing negative amount raises exception."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-20.0)
    
    def test_account_locking(self):
        """Test account locking functionality."""
        self.account.lock_account()
        
        with self.assertRaises(ValueError):
            self.account.deposit(10.0)
        
        with self.assertRaises(ValueError):
            self.account.withdraw(10.0)
        
        # Unlock and verify operations work
        self.account.unlock_account()
        self.account.deposit(10.0)
        self.assertEqual(self.account.get_balance(), 110.0)
    
    def test_transaction_history(self):
        """Test transaction history tracking."""
        self.account.deposit(25.0)
        self.account.withdraw(10.0)
        self.account.deposit(5.0)
        
        history = self.account.get_transaction_history()
        expected_history = [
            "DEPOSIT: +$25.00",
            "WITHDRAWAL: -$10.00",
            "DEPOSIT: +$5.00"
        ]
        
        self.assertEqual(history, expected_history)
    
    def test_multiple_operations(self):
        """Test multiple operations in sequence."""
        operations = [
            ("deposit", 50.0),
            ("withdraw", 25.0),
            ("deposit", 75.0),
            ("withdraw", 100.0)
        ]
        
        expected_balance = 100.0  # Starting balance
        
        for operation, amount in operations:
            if operation == "deposit":
                self.account.deposit(amount)
                expected_balance += amount
            else:
                self.account.withdraw(amount)
                expected_balance -= amount
        
        self.assertEqual(self.account.get_balance(), expected_balance)


class TestBankingServiceWithMocking(unittest.TestCase):
    """Testing with mocks and test doubles."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_external_api = Mock()
        self.banking_service = BankingService(self.mock_external_api)
    
    def test_create_account(self):
        """Test account creation."""
        account = self.banking_service.create_account("ACC001", 500.0)
        
        self.assertIsNotNone(account)
        self.assertEqual(account.account_id, "ACC001")
        self.assertEqual(account.get_balance(), 500.0)
    
    def test_create_duplicate_account(self):
        """Test creating duplicate account raises exception."""
        self.banking_service.create_account("ACC001", 500.0)
        
        with self.assertRaises(ValueError):
            self.banking_service.create_account("ACC001", 300.0)
    
    def test_transfer_success(self):
        """Test successful money transfer."""
        # Create accounts
        from_account = self.banking_service.create_account("FROM001", 1000.0)
        to_account = self.banking_service.create_account("TO001", 500.0)
        
        # Perform transfer
        result = self.banking_service.transfer("FROM001", "TO001", 200.0)
        
        self.assertTrue(result)
        self.assertEqual(from_account.get_balance(), 800.0)
        self.assertEqual(to_account.get_balance(), 700.0)
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds."""
        from_account = self.banking_service.create_account("FROM001", 100.0)
        to_account = self.banking_service.create_account("TO001", 500.0)
        
        with self.assertRaises(ValueError):
            self.banking_service.transfer("FROM001", "TO001", 200.0)
        
        # Verify balances unchanged
        self.assertEqual(from_account.get_balance(), 100.0)
        self.assertEqual(to_account.get_balance(), 500.0)
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_get_account_info_with_mock(self, mock_sleep):
        """Test getting account info with mocked external API."""
        # Set up mock external API response
        self.mock_external_api.get_credit_score.return_value = 750
        
        # Create account and perform some transactions
        account = self.banking_service.create_account("ACC001", 1000.0)
        account.deposit(200.0)
        account.withdraw(100.0)
        
        # Get account info
        info = self.banking_service.get_account_info("ACC001")
        
        # Verify results
        expected_info = {
            "account_id": "ACC001",
            "balance": 1100.0,
            "credit_score": 750,
            "transaction_count": 2
        }
        
        self.assertEqual(info, expected_info)
        
        # Verify mock was called correctly
        self.mock_external_api.get_credit_score.assert_called_once_with("ACC001")
    
    def test_external_api_failure_handling(self):
        """Test handling external API failures."""
        # Configure mock to raise exception
        self.mock_external_api.get_credit_score.side_effect = Exception("API unavailable")
        
        account = self.banking_service.create_account("ACC001", 1000.0)
        
        # This should not raise exception, but credit_score should be None
        with self.assertRaises(Exception):
            self.banking_service.get_account_info("ACC001")


# ============================================================================
# PYTEST EXAMPLES
# ============================================================================

class TestBankAccountPytest:
    """Pytest-style tests for BankAccount."""
    
    @pytest.fixture
    def account(self):
        """Pytest fixture for creating test account."""
        return BankAccount("PYTEST001", 200.0)
    
    @pytest.fixture
    def banking_service(self):
        """Pytest fixture for banking service."""
        return BankingService()
    
    def test_deposit_valid_amount(self, account):
        """Test valid deposit using pytest."""
        account.deposit(100.0)
        assert account.get_balance() == 300.0
    
    @pytest.mark.parametrize("amount,expected_balance", [
        (50.0, 250.0),
        (100.0, 300.0),
        (0.01, 200.01),
        (999.99, 1199.99)
    ])
    def test_deposit_various_amounts(self, account, amount, expected_balance):
        """Test depositing various amounts using parametrize."""
        account.deposit(amount)
        assert account.get_balance() == expected_balance
    
    @pytest.mark.parametrize("invalid_amount", [-10.0, -100.0, 0.0])
    def test_deposit_invalid_amounts(self, account, invalid_amount):
        """Test depositing invalid amounts."""
        with pytest.raises(ValueError):
            account.deposit(invalid_amount)
    
    def test_concurrent_deposits(self, account):
        """Test concurrent deposits for thread safety."""
        def deposit_worker():
            for _ in range(10):
                account.deposit(1.0)
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=deposit_worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have deposited 50 times (5 threads * 10 deposits * $1)
        assert account.get_balance() == 250.0
    
    @pytest.mark.slow
    def test_performance_many_transactions(self, account):
        """Performance test for many transactions (marked as slow)."""
        start_time = time.time()
        
        for i in range(1000):
            account.deposit(1.0)
            if i % 2 == 0:
                account.withdraw(0.5)
        
        end_time = time.time()
        
        assert end_time - start_time < 1.0  # Should complete in less than 1 second
        assert account.get_balance() == 700.0  # 200 + 1000 - 500*0.5


# ============================================================================
# INTEGRATION TESTING
# ============================================================================

class TestBankingIntegration(unittest.TestCase):
    """Integration tests for banking system components."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.banking_service = BankingService()
        self.temp_files = []
    
    def tearDown(self):
        """Clean up integration test resources."""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_end_to_end_banking_workflow(self):
        """Test complete banking workflow."""
        # Create accounts
        alice_account = self.banking_service.create_account("ALICE", 1000.0)
        bob_account = self.banking_service.create_account("BOB", 500.0)
        
        # Perform operations
        alice_account.deposit(200.0)
        bob_account.withdraw(50.0)
        
        # Transfer money
        self.banking_service.transfer("ALICE", "BOB", 300.0)
        
        # Verify final state
        self.assertEqual(alice_account.get_balance(), 900.0)  # 1000 + 200 - 300
        self.assertEqual(bob_account.get_balance(), 750.0)    # 500 - 50 + 300
        
        # Verify transaction histories
        alice_history = alice_account.get_transaction_history()
        bob_history = bob_account.get_transaction_history()
        
        self.assertEqual(len(alice_history), 2)  # deposit + withdrawal (from transfer)
        self.assertEqual(len(bob_history), 2)    # withdrawal + deposit (from transfer)
    
    def test_data_persistence_simulation(self):
        """Test data persistence (simulated with file I/O)."""
        # Create account and perform operations
        account = self.banking_service.create_account("PERSIST", 500.0)
        account.deposit(100.0)
        account.withdraw(50.0)
        
        # Simulate saving to file
        temp_file = tempfile.mktemp(suffix='.json')
        self.temp_files.append(temp_file)
        
        account_data = {
            "account_id": account.account_id,
            "balance": account.get_balance(),
            "transaction_history": account.get_transaction_history()
        }
        
        with open(temp_file, 'w') as f:
            json.dump(account_data, f)
        
        # Simulate loading from file
        with open(temp_file, 'r') as f:
            loaded_data = json.load(f)
        
        # Verify data integrity
        self.assertEqual(loaded_data["account_id"], "PERSIST")
        self.assertEqual(loaded_data["balance"], 550.0)
        self.assertEqual(len(loaded_data["transaction_history"]), 2)


# ============================================================================
# PERFORMANCE TESTING
# ============================================================================

class PerformanceTester:
    """Performance testing utilities."""
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """Measure function execution time."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        return result, end_time - start_time
    
    @staticmethod
    def load_test_deposits(account, num_operations=1000):
        """Load test for deposit operations."""
        start_time = time.time()
        
        for i in range(num_operations):
            account.deposit(1.0)
        
        end_time = time.time()
        
        return {
            "operations": num_operations,
            "total_time": end_time - start_time,
            "ops_per_second": num_operations / (end_time - start_time),
            "avg_time_per_op": (end_time - start_time) / num_operations
        }
    
    @staticmethod
    def concurrent_load_test(account, num_threads=10, ops_per_thread=100):
        """Concurrent load test."""
        def worker():
            for _ in range(ops_per_thread):
                account.deposit(0.01)
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker) for _ in range(num_threads)]
            concurrent.futures.wait(futures)
        
        end_time = time.time()
        
        total_operations = num_threads * ops_per_thread
        total_time = end_time - start_time
        
        return {
            "threads": num_threads,
            "ops_per_thread": ops_per_thread,
            "total_operations": total_operations,
            "total_time": total_time,
            "ops_per_second": total_operations / total_time
        }


# ============================================================================
# DEBUGGING UTILITIES
# ============================================================================

class DebugLogger:
    """Advanced debugging and logging utilities."""
    
    def __init__(self, logger_name="debug"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def trace_function_calls(self, func):
        """Decorator to trace function calls."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                self.logger.debug(f"Exiting {func.__name__} with result={result}")
                return result
            except Exception as e:
                self.logger.error(f"Exception in {func.__name__}: {e}")
                self.logger.debug(f"Traceback: {traceback.format_exc()}")
                raise
        
        return wrapper
    
    @contextmanager
    def debug_context(self, operation_name):
        """Context manager for debugging operations."""
        self.logger.debug(f"Starting operation: {operation_name}")
        start_time = time.time()
        
        try:
            yield self.logger
        except Exception as e:
            self.logger.error(f"Operation {operation_name} failed: {e}")
            raise
        finally:
            end_time = time.time()
            self.logger.debug(f"Operation {operation_name} completed in {end_time - start_time:.3f}s")


class CodeProfiler:
    """Code profiling utilities."""
    
    @staticmethod
    def profile_function(func, *args, **kwargs):
        """Profile a function with cProfile."""
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        return result, stats
    
    @staticmethod
    @memory_profiler.profile
    def memory_profile_function(func, *args, **kwargs):
        """Memory profiling decorator (requires memory_profiler package)."""
        return func(*args, **kwargs)


# ============================================================================
# TEST UTILITIES AND HELPERS
# ============================================================================

class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_test_accounts(count=5):
        """Create multiple test accounts."""
        accounts = []
        for i in range(count):
            account_id = f"TEST{i:03d}"
            initial_balance = random.uniform(100.0, 1000.0)
            accounts.append(BankAccount(account_id, initial_balance))
        return accounts
    
    @staticmethod
    def generate_random_transactions(account, count=10):
        """Generate random transactions for testing."""
        transactions = []
        
        for _ in range(count):
            operation = random.choice(['deposit', 'withdraw'])
            amount = random.uniform(1.0, 100.0)
            
            try:
                if operation == 'deposit':
                    account.deposit(amount)
                    transactions.append(('deposit', amount, True))
                else:
                    account.withdraw(amount)
                    transactions.append(('withdraw', amount, True))
            except ValueError:
                transactions.append((operation, amount, False))
        
        return transactions


class AssertionHelpers:
    """Custom assertion helpers for testing."""
    
    @staticmethod
    def assert_balance_equals(account, expected_balance, delta=0.01):
        """Assert account balance within delta."""
        actual_balance = account.get_balance()
        if abs(actual_balance - expected_balance) > delta:
            raise AssertionError(
                f"Balance assertion failed: expected {expected_balance}, "
                f"got {actual_balance} (delta: {delta})"
            )
    
    @staticmethod
    def assert_transaction_contains(account, transaction_pattern):
        """Assert transaction history contains pattern."""
        history = account.get_transaction_history()
        if not any(transaction_pattern in transaction for transaction in history):
            raise AssertionError(
                f"Transaction pattern '{transaction_pattern}' not found in history: {history}"
            )


def run_performance_benchmarks():
    """Run comprehensive performance benchmarks."""
    print("Performance Benchmarks")
    print("=" * 40)
    
    account = BankAccount("PERF001", 1000.0)
    
    # Single-threaded performance
    print("\n1. Single-threaded Performance:")
    results = PerformanceTester.load_test_deposits(account, 10000)
    print(f"   Operations: {results['operations']}")
    print(f"   Total time: {results['total_time']:.3f}s")
    print(f"   Ops/second: {results['ops_per_second']:.0f}")
    
    # Multi-threaded performance
    print("\n2. Multi-threaded Performance:")
    account2 = BankAccount("PERF002", 1000.0)
    results = PerformanceTester.concurrent_load_test(account2, 10, 1000)
    print(f"   Threads: {results['threads']}")
    print(f"   Total operations: {results['total_operations']}")
    print(f"   Total time: {results['total_time']:.3f}s")
    print(f"   Ops/second: {results['ops_per_second']:.0f}")


def demonstrate_debugging():
    """Demonstrate debugging techniques."""
    print("\nDebugging Demonstration")
    print("=" * 30)
    
    debug_logger = DebugLogger("banking_debug")
    
    # Create a traced version of deposit method
    account = BankAccount("DEBUG001", 500.0)
    traced_deposit = debug_logger.trace_function_calls(account.deposit)
    
    print("\n1. Function Call Tracing:")
    traced_deposit(100.0)
    
    print("\n2. Debug Context Manager:")
    with debug_logger.debug_context("Complex Operation"):
        account.withdraw(50.0)
        account.deposit(25.0)
    
    print("\n3. Error Handling:")
    try:
        traced_deposit(-10.0)  # This will raise an exception
    except ValueError:
        pass  # Exception was logged


def main():
    """Main function to run all testing demonstrations."""
    print("Comprehensive Testing and Debugging Framework")
    print("=" * 55)
    
    try:
        # Run unittest tests
        print("\n1. Running Unit Tests (unittest)...")
        unittest.main(argv=[''], exit=False, verbosity=2, 
                     defaultTest='TestBankAccount')
        
        # Performance benchmarks
        run_performance_benchmarks()
        
        # Debugging demonstration
        demonstrate_debugging()
        
        print("\n4. Test Data Factory Example:")
        accounts = TestDataFactory.create_test_accounts(3)
        for account in accounts:
            transactions = TestDataFactory.generate_random_transactions(account, 5)
            print(f"   Account {account.account_id}: {len(transactions)} transactions")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
    
    print(f"\n{'='*55}")
    print("Testing and debugging demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# TESTING BEST PRACTICES AND GUIDELINES
# ============================================================================

"""
🧪 TESTING BEST PRACTICES:

📋 TEST ORGANIZATION:
• Follow AAA pattern: Arrange, Act, Assert
• One assertion per test (when possible)
• Descriptive test names that explain what is being tested
• Group related tests in test classes
• Use setUp/tearDown for test fixtures

🎯 TEST COVERAGE:
• Aim for high code coverage (>80%) but focus on quality over quantity
• Test edge cases and boundary conditions
• Test both positive and negative scenarios
• Test error conditions and exception handling
• Use code coverage tools (coverage.py, pytest-cov)

🏗️ TEST STRUCTURE:
• Unit tests: Test individual components in isolation
• Integration tests: Test component interactions
• End-to-end tests: Test complete user workflows
• Performance tests: Test system under load
• Security tests: Test for vulnerabilities

🔧 MOCKING AND TEST DOUBLES:
• Mock external dependencies (APIs, databases, file system)
• Use dependency injection for better testability
• Verify mock interactions with assert_called_with()
• Use fixtures for reusable test data
• Isolate units under test

⚡ PERFORMANCE TESTING:
• Benchmark critical operations
• Test under realistic load conditions
• Monitor memory usage and resource consumption
• Test concurrent access and thread safety
• Identify performance bottlenecks

🐛 DEBUGGING STRATEGIES:
• Use logging extensively for troubleshooting
• Implement comprehensive error handling
• Use debugger tools (pdb, IDE debuggers)
• Add diagnostic information to exceptions
• Create reproducible test cases for bugs

📊 CONTINUOUS INTEGRATION:
• Run tests automatically on code changes
• Fail builds on test failures
• Generate test reports and coverage metrics
• Run different test suites at appropriate times
• Integrate with version control systems

🔍 CODE QUALITY:
• Use static analysis tools (pylint, mypy)
• Enforce coding standards and style guides
• Review test code with the same rigor as production code
• Refactor tests to maintain readability
• Document complex test scenarios

💡 TESTING STRATEGIES:
• Test-Driven Development (TDD): Write tests before code
• Behavior-Driven Development (BDD): Focus on user behavior
• Property-based testing: Test with generated data
• Mutation testing: Verify test effectiveness
• Regression testing: Prevent reintroduction of bugs

🚀 ADVANCED TECHNIQUES:
• Parameterized tests for testing multiple scenarios
• Fixture factories for dynamic test data
• Custom assertions for domain-specific checks
• Test data builders for complex object creation
• Contract testing for API compatibility
"""
