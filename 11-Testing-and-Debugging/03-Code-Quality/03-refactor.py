"""
Module Docstring: Code Refactoring Techniques

Learning Objectives:
1. Understand the principles of code refactoring.
2. Learn how to refactor monolithic code into modular functions.
3. Apply Pythonic idioms (list comprehensions, generators) during refactoring.
4. Refactor code to apply design patterns (e.g., Strategy Pattern).

Concept Explanation:
Refactoring is the process of restructuring existing computer code—changing the 
factoring—without changing its external behavior. It improves nonfunctional attributes 
of the software, making it more readable, maintainable, and less complex.
"""

import time
from abc import ABC, abstractmethod
from typing import List, Callable, Dict
import unittest

# Basic Implementation: Refactoring Monolithic Code
# BEFORE: Monolithic function
def process_data_old(data: List[int]) -> Dict[str, float]:
    result = {}
    
    # Filter even numbers
    evens = []
    for x in data:
        if x % 2 == 0:
            evens.append(x)
            
    # Calculate sum of squares
    sum_squares = 0
    for x in evens:
        sum_squares += x ** 2
        
    # Calculate mean
    if len(evens) > 0:
        mean = sum_squares / len(evens)
    else:
        mean = 0.0
        
    result['evens_count'] = float(len(evens))
    result['sum_squares'] = float(sum_squares)
    result['mean_square'] = float(mean)
    return result

# AFTER: Modular and Pythonic
def filter_evens(data: List[int]) -> List[int]:
    return [x for x in data if x % 2 == 0]

def calculate_sum_squares(data: List[int]) -> int:
    return sum(x ** 2 for x in data)

def process_data_new(data: List[int]) -> Dict[str, float]:
    """Refactored version using smaller functions and comprehensions."""
    evens = filter_evens(data)
    sum_squares = calculate_sum_squares(evens)
    mean = sum_squares / len(evens) if evens else 0.0
    
    return {
        'evens_count': float(len(evens)),
        'sum_squares': float(sum_squares),
        'mean_square': float(mean)
    }

# Intermediate Implementation: Refactoring if-else chains using a Dictionary (Strategy/Dispatch)
# BEFORE
def get_discount_old(customer_type: str, amount: float) -> float:
    if customer_type == 'regular':
        return amount * 0.05
    elif customer_type == 'premium':
        return amount * 0.10
    elif customer_type == 'vip':
        return amount * 0.20
    else:
        return 0.0

# AFTER
DISCOUNT_STRATEGIES: Dict[str, Callable[[float], float]] = {
    'regular': lambda amount: amount * 0.05,
    'premium': lambda amount: amount * 0.10,
    'vip':     lambda amount: amount * 0.20,
}

def get_discount_new(customer_type: str, amount: float) -> float:
    """Refactored version using a dictionary dispatch."""
    strategy = DISCOUNT_STRATEGIES.get(customer_type, lambda amt: 0.0)
    return strategy(amount)

# Advanced Implementation: Refactoring to use the Strategy Design Pattern (OOP)
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class RegularDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.05

class PremiumDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.10

class Order:
    def __init__(self, amount: float, discount_strategy: DiscountStrategy) -> None:
        self.amount = amount
        self.discount_strategy = discount_strategy
        
    def get_final_price(self) -> float:
        discount = self.discount_strategy.apply_discount(self.amount)
        return self.amount - discount

# Performance Analysis
def performance_analysis() -> None:
    """Compare performance of old vs new processing function."""
    large_data = list(range(100000))
    
    start = time.time()
    for _ in range(10):
        process_data_old(large_data)
    time_old = time.time() - start
    
    start = time.time()
    for _ in range(10):
        process_data_new(large_data)
    time_new = time.time() - start
    
    print(f"Old approach time: {time_old:.4f}s")
    print(f"New approach time (list comprehensions & generators): {time_new:.4f}s")
    # Usually the generator/comprehension version is faster and uses less memory in Python!

# Edge Cases
# - Refactoring could accidentally change behavior (always write tests before refactoring).
# - Floating point precision changes when reordering math operations.
# - Dictionary dispatch might evaluate arguments eagerly, unlike lazy if-else short-circuiting.

# Interview Challenge
"""
Challenge: Refactor a nested loop to a single list comprehension or generator expression.
Given: A list of lists of numbers. Return the flattened list containing only positive numbers.
"""
def flatten_positives(nested_list: List[List[int]]) -> List[int]:
    return [num for sublist in nested_list for num in sublist if num > 0]

# Tests
class TestRefactoring(unittest.TestCase):
    def test_process_data(self):
        data = [1, 2, 3, 4, 5, 6]
        res_old = process_data_old(data)
        res_new = process_data_new(data)
        self.assertEqual(res_old['sum_squares'], res_new['sum_squares'])
        self.assertEqual(res_old['mean_square'], res_new['mean_square'])
        
    def test_discount(self):
        self.assertEqual(get_discount_old('premium', 100), 10.0)
        self.assertEqual(get_discount_new('premium', 100), 10.0)
        
    def test_strategy_pattern(self):
        order = Order(100, PremiumDiscount())
        self.assertEqual(order.get_final_price(), 90.0)
        
    def test_flatten_positives(self):
        nested = [[-1, 2, -3], [4, -5, 6]]
        self.assertEqual(flatten_positives(nested), [2, 4, 6])

if __name__ == "__main__":
    print("Running tests...")
    unittest.main(exit=False)
    print("\nRunning performance analysis...")
    performance_analysis()
