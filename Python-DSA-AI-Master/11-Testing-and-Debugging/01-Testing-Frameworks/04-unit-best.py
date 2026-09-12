"""
Unit Testing Best Practices - Educational Script

Learning Objectives:
1. Understand the Arrange-Act-Assert (AAA) pattern.
2. Learn how to write Independent, Repeatable, and Fast tests (FIRST principles).
3. Discover the importance of descriptive test names.
4. Understand Test-Driven Development (TDD) concepts.
5. Learn how to measure and interpret Code Coverage.

Concept Explanation:
Writing tests is not just about executing code; it's about documenting behavior,
preventing regressions, and designing better APIs. Good tests are readable,
maintainable, and reliable.

Key Principles:
- F.I.R.S.T.: Fast, Isolated, Repeatable, Self-validating, Timely.
- A.A.A.: Arrange (setup), Act (execute), Assert (verify).
- Single Responsibility: A test should verify one specific behavior.
"""

import unittest
from typing import List, Optional

# --- The Code Under Test ---

class Order:
    """Represents a customer order."""
    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self.items: List[dict] = [] # type: ignore
        self.status = "pending"
        
    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append({"name": name, "price": price, "quantity": quantity})
        
    def calculate_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)
        
    def checkout(self) -> None:
        if not self.items:
            raise ValueError("Cannot checkout an empty order")
        self.status = "completed"

# --- Basic Implementation: Bad vs Good Tests ---

class TestOrderBadPractices(unittest.TestCase):
    """Examples of how NOT to write tests."""
    
    def test_order(self) -> None: # Bad: Vague name
        # Bad: Multiple responsibilities in one test
        o = Order("123")
        o.add_item("Apple", 1.0)
        self.assertEqual(o.calculate_total(), 1.0)
        o.add_item("Banana", 2.0, 2)
        self.assertEqual(o.calculate_total(), 5.0)
        o.checkout()
        self.assertEqual(o.status, "completed")

class TestOrderGoodPractices(unittest.TestCase):
    """Examples of good testing practices following AAA and FIRST."""
    
    def test_calculate_total_with_multiple_items_returns_correct_sum(self) -> None:
        """Good: Descriptive name, Single responsibility, AAA pattern."""
        # Arrange
        order = Order("123")
        order.add_item("Apple", 1.5, 2)
        order.add_item("Banana", 2.0, 1)
        
        # Act
        total = order.calculate_total()
        
        # Assert
        self.assertEqual(total, 5.0)
        
    def test_checkout_empty_order_raises_value_error(self) -> None:
        """Test for expected failures explicitly."""
        # Arrange
        order = Order("123")
        
        # Act & Assert
        with self.assertRaisesRegex(ValueError, "empty order"):
            order.checkout()

    def test_checkout_valid_order_updates_status(self) -> None:
        # Arrange
        order = Order("123")
        order.add_item("Apple", 1.0)
        
        # Act
        order.checkout()
        
        # Assert
        self.assertEqual(order.status, "completed")

# --- Intermediate Implementation: Test Data Builders (Factory Pattern) ---
# For complex objects, use helper functions to create test data, keeping tests clean.

def create_valid_order_with_items(order_id: str = "test-1") -> Order:
    """Helper method to construct an order for testing."""
    order = Order(order_id)
    order.add_item("Item1", 10.0, 1)
    order.add_item("Item2", 5.0, 2)
    return order

class TestOrderWithFactory(unittest.TestCase):
    def test_calculate_total_uses_factory(self) -> None:
        order = create_valid_order_with_items()
        self.assertEqual(order.calculate_total(), 20.0)

# --- Performance Analysis ---
# Fast tests encourage frequent execution.
# Avoid network calls, file I/O, or database queries in unit tests; mock them instead.
# If a test requires heavy setup, consider if the class is doing too much (violation of Single Responsibility Principle).

# --- Edge Cases ---
# Always test boundary conditions: zero, negative numbers, empty strings, max values.
# Example: Adding an item with quantity 0 or negative price.

class TestOrderEdgeCases(unittest.TestCase):
    def test_add_item_negative_price_raises_error(self) -> None:
        order = Order("123")
        with self.assertRaises(ValueError):
            order.add_item("Apple", -1.0)

# --- Interview Challenge ---
# Challenge: How do you achieve 100% test coverage, and is it a good metric?
# Answer: Coverage measures the percentage of code lines executed during tests.
# While high coverage is good, 100% doesn't guarantee the absence of bugs.
# It doesn't measure if the *logic* is correct or if all *edge cases* are handled.
# Aim for meaningful tests over just hitting coverage numbers.

if __name__ == "__main__":
    unittest.main(verbosity=2)
