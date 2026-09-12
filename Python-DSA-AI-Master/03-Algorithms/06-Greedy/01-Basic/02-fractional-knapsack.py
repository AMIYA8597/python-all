"""
Fractional Knapsack Problem

Learning Objectives:
1. Understand the greedy approach to the knapsack problem.
2. Calculate and utilize value-to-weight ratios.
3. Compare fractional knapsack (greedy) with 0/1 knapsack (dynamic programming).

Concept Explanation:
In the Fractional Knapsack problem, you are given a set of items, each with a weight and a value, 
and a knapsack with a maximum weight capacity. The goal is to maximize the total value in the knapsack.
Unlike the 0/1 Knapsack problem where items cannot be broken, here you can take fractions of items.
The greedy strategy is to sort items by their value-to-weight ratio in descending order and greedily 
pick items until the knapsack is full.

Performance Analysis:
- Time Complexity: O(N log N) dominated by sorting the items.
- Space Complexity: O(N) or O(1) depending on in-place sorting.

Edge Cases:
- Knapsack capacity is 0.
- All items have 0 weight (infinite ratio, need to handle division by zero).
- Item values are 0.

Interview Challenge:
"Given a knapsack of capacity W and N items with values V and weights W, find the max value achievable allowing fractions."
"""

from typing import List, Tuple
import unittest

def fractional_knapsack_basic(weights: List[int], values: List[int], capacity: int) -> float:
    """Basic implementation returning max value."""
    if not weights or not values or capacity <= 0:
        return 0.0
        
    items = [(values[i], weights[i], values[i]/weights[i]) for i in range(len(weights))]
    items.sort(key=lambda x: x[2], reverse=True)
    
    total_value = 0.0
    
    for v, w, ratio in items:
        if capacity >= w:
            total_value += v
            capacity -= w
        else:
            total_value += ratio * capacity
            break
            
    return total_value

class Item:
    def __init__(self, value: float, weight: float):
        self.value = value
        self.weight = weight
        self.ratio = value / weight if weight != 0 else float('inf')

def fractional_knapsack_intermediate(items: List[Item], capacity: float) -> float:
    """Intermediate implementation using class objects."""
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    total_value = 0.0
    for item in items:
        if capacity >= item.weight:
            total_value += item.value
            capacity -= item.weight
        else:
            total_value += item.ratio * capacity
            break
            
    return total_value

def fractional_knapsack_advanced(items_dict: List[dict], capacity: float) -> Tuple[float, List[dict]]:
    """Advanced implementation returning total value and the chosen fractions."""
    for item in items_dict:
        item['ratio'] = item['value'] / item['weight'] if item['weight'] != 0 else float('inf')
        
    items_sorted = sorted(items_dict, key=lambda x: x['ratio'], reverse=True)
    
    total_value = 0.0
    chosen = []
    
    for item in items_sorted:
        if capacity <= 0:
            break
        if capacity >= item['weight']:
            total_value += item['value']
            capacity -= item['weight']
            chosen.append({**item, 'fraction_taken': 1.0})
        else:
            fraction = capacity / item['weight']
            total_value += item['value'] * fraction
            chosen.append({**item, 'fraction_taken': fraction})
            capacity = 0
            
    return total_value, chosen

class TestFractionalKnapsack(unittest.TestCase):
    def test_basic(self):
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50
        self.assertEqual(fractional_knapsack_basic(weights, values, capacity), 240.0)
        
    def test_intermediate(self):
        items = [Item(60, 10), Item(100, 20), Item(120, 30)]
        self.assertEqual(fractional_knapsack_intermediate(items, 50), 240.0)
        
    def test_advanced(self):
        items = [{'name': 'A', 'value': 60, 'weight': 10}, 
                 {'name': 'B', 'value': 100, 'weight': 20}, 
                 {'name': 'C', 'value': 120, 'weight': 30}]
        val, chosen = fractional_knapsack_advanced(items, 50)
        self.assertEqual(val, 240.0)
        self.assertEqual(len(chosen), 3)

if __name__ == "__main__":
    unittest.main()
