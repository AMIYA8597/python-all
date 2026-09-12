"""
0/1 Knapsack Problem via Branch and Bound

Learning Objectives:
1. Apply the Branch and Bound technique to the 0/1 Knapsack Problem.
2. Formulate an upper bound using the fractional knapsack approach.
3. Compare Branch and Bound with Dynamic Programming for Knapsack.

Concept Explanation:
For the 0/1 Knapsack problem, the items are sorted by value/weight ratio. 
At each node of the decision tree, we either include an item or exclude it. 
To bound the maximum possible profit for a branch, we calculate the profit if we 
could take fractions of remaining items (Fractional Knapsack). If this optimistic 
bound is worse than our current best solution, we prune the branch.
"""

from typing import List
from collections import deque

class Item:
    def __init__(self, weight: int, value: int, index: int):
        self.weight = weight
        self.value = value
        self.index = index
        self.ratio = value / weight

class Node:
    def __init__(self, level: int, profit: int, weight: int, bound: float):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.bound = bound

# Basic Implementation: Bounding Function
def bound(node: Node, n: int, capacity: int, items: List[Item]) -> float:
    """Returns the upper bound of profit for a subtree rooted at node."""
    if node.weight >= capacity:
        return 0

    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + items[j].weight <= capacity:
        total_weight += items[j].weight
        profit_bound += items[j].value
        j += 1

    if j < n:
        profit_bound += (capacity - total_weight) * items[j].ratio

    return profit_bound

# Advanced Implementation: Branch and Bound Solver
def knapsack_bnb(capacity: int, weights: List[int], values: List[int]) -> int:
    """Solves the 0/1 Knapsack problem using Branch and Bound."""
    n = len(weights)
    items = [Item(weights[i], values[i], i) for i in range(n)]
    items.sort(key=lambda x: x.ratio, reverse=True)

    q = deque()
    
    u = Node(level=-1, profit=0, weight=0, bound=0.0)
    u.bound = bound(u, n, capacity, items)
    q.append(u)

    max_profit = 0

    while q:
        u = q.popleft()

        if u.level == n - 1:
            continue

        v = Node(level=u.level + 1, 
                 profit=u.profit + items[u.level + 1].value, 
                 weight=u.weight + items[u.level + 1].weight,
                 bound=0.0)

        if v.weight <= capacity and v.profit > max_profit:
            max_profit = v.profit

        v.bound = bound(v, n, capacity, items)
        if v.bound > max_profit:
            q.append(v)

        v2 = Node(level=u.level + 1, profit=u.profit, weight=u.weight, bound=0.0)
        v2.bound = bound(v2, n, capacity, items)
        
        if v2.bound > max_profit:
            q.append(v2)

    return max_profit

# Performance Analysis
def performance_analysis():
    """
    Time Complexity: O(2^N) in the worst case, but heavily pruned in practice.
    Space Complexity: O(2^N) worst-case queue size, but typically much less.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Item weights larger than the capacity.
    - All items fit in the knapsack.
    - Zero capacity.
    """
    pass

# Interview Challenge
def challenge_knapsack_path():
    """Challenge: Return the actual items included in the optimal solution."""
    pass

# Tests
def run_tests():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    
    profit = knapsack_bnb(capacity, weights, values)
    assert profit == 7
    
    weights2 = [10, 20, 30]
    values2 = [60, 100, 120]
    cap2 = 50
    assert knapsack_bnb(cap2, weights2, values2) == 220
    
    print("All Knapsack Branch and Bound tests passed!")

if __name__ == "__main__":
    run_tests()
