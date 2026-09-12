"""
Module: Testing Automation Scripting
====================================

Learning Objectives:
1. Understand test-driven development (TDD) principles.
2. Master the built-in `unittest` framework for automating code validation.
3. Learn how to isolate tests using `unittest.mock` (patching, mock objects).
4. Structure test cases, test suites, and assertions for enterprise-grade applications.

Concept Explanation:
Automated testing ensures that software behaves exactly as expected, preventing regressions 
when code is modified. The `unittest` module is standard in Python. A test case is created by 
subclassing `unittest.TestCase`. Tests are isolated by setting up preconditions (`setUp`) and 
cleaning up afterward (`tearDown`). Mocking is used to simulate external dependencies (like APIs 
or databases) to ensure the test only validates the internal logic of the function.

Industry Use Cases:
- Continuous Integration/Continuous Deployment (CI/CD) pipelines (GitHub Actions, Jenkins).
- Ensuring API contracts remain unbroken during major refactors.
- Isolating components to identify bottlenecks or logic flaws.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# ==========================================
# 1. APPLICATION LOGIC (Code to test)
# ==========================================

class PaymentGateway:
    def charge(self, user_id: int, amount: float) -> bool:
        """Simulates an external API call to charge a user."""
        # In a real scenario, this would make an HTTP request.
        raise NotImplementedError("Real gateway not configured.")

class OrderProcessor:
    """Processes customer orders and triggers payment."""
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
        
    def process_order(self, user_id: int, items: list, total_cost: float) -> Dict[str, Any]:
        if not items:
            return {"status": "failed", "reason": "empty order"}
            
        success = self.gateway.charge(user_id, total_cost)
        
        if success:
            return {"status": "success", "user_id": user_id, "amount": total_cost}
        return {"status": "failed", "reason": "payment declined"}

# ==========================================
# 2. PROFESSIONAL IMPLEMENTATION (Test Suite)
# ==========================================

class TestOrderProcessor(unittest.TestCase):
    """
    A comprehensive test suite for the OrderProcessor class demonstrating
    various unittest features including Setup, Teardown, and Mocking.
    """
    
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests in the class."""
        print("Starting Test Suite for OrderProcessor...")
        
    def setUp(self):
        """Runs before EVERY individual test."""
        # We create a new processor and mocked gateway for each test to ensure isolation.
        self.mock_gateway = MagicMock(spec=PaymentGateway)
        self.processor = OrderProcessor(gateway=self.mock_gateway)
        
    def tearDown(self):
        """Runs after EVERY individual test."""
        # Cleanup resources if necessary
        pass

    def test_process_order_empty_items(self):
        """Test business logic handling of empty items."""
        result = self.processor.process_order(user_id=1, items=[], total_cost=0.0)
        
        # Assertions
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["reason"], "empty order")
        # Ensure the payment gateway was never called since items were empty
        self.mock_gateway.charge.assert_not_called()

    def test_process_order_payment_success(self):
        """Test successful payment flow using Mock object."""
        # Configure the mock to simulate a successful API response
        self.mock_gateway.charge.return_value = True
        
        result = self.processor.process_order(user_id=42, items=["laptop"], total_cost=1500.0)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["amount"], 1500.0)
        # Verify the mock was called exactly once with the correct arguments
        self.mock_gateway.charge.assert_called_once_with(42, 1500.0)

    @patch('__main__.PaymentGateway.charge')
    def test_process_order_payment_failure_with_patch(self, mock_charge):
        """Test failed payment flow using @patch decorator instead of injected Mock."""
        # Note: In this specific architecture, dependency injection (as in setUp) is preferred, 
        # but @patch is demonstrated here for educational purposes on how to intercept classes.
        mock_charge.return_value = False
        
        # We have to instantiate a fresh processor with the patched class
        temp_processor = OrderProcessor(gateway=PaymentGateway())
        result = temp_processor.process_order(user_id=10, items=["book"], total_cost=20.0)
        
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["reason"], "payment declined")


# ==========================================
# 3. COMPLEXITY ANALYSIS & INTERVIEW CHALLENGE
# ==========================================
"""
Complexity Analysis:
- Time Complexity (of executing tests): O(N) where N is the number of test cases.
- Space Complexity: O(M) where M is the memory footprint of the objects mocked and created in setUp.

Interview Challenge:
Question: Why might you choose dependency injection with `MagicMock` over the `@patch` decorator?
Answer Guidelines: 
- The `@patch` decorator relies on string paths to the module being imported, which is brittle and breaks if refactored or imported using `from x import y`.
- Dependency injection (passing the mock in the constructor) tightly couples the mock to the specific instance being tested and is safer, cleaner, and avoids namespace pollution or patching errors.
"""

# ==========================================
# 4. EXAMPLE USAGE & TESTS
# ==========================================

if __name__ == '__main__':
    # unittest.main() will automatically discover and run all classes inheriting from unittest.TestCase
    print("Running Tests via unittest.main()...")
    unittest.main(verbosity=2, exit=False)
