"""
Generalized Branch and Bound Framework

Learning Objectives:
1. Abstract the Branch and Bound logic into a reusable framework.
2. Understand object-oriented design patterns for algorithmic paradigms.
3. Apply the framework to solve a generic optimization problem.

Concept Explanation:
By defining abstract base classes for `Problem`, `State`, and `Bound`, we can create
a generalized engine that processes nodes in a Priority Queue. This allows us to
separate the algorithm's core logic (the PQ, pruning) from the problem-specific logic 
(generating children, calculating bounds).
"""

from abc import ABC, abstractmethod
import heapq
from typing import List, Optional, Tuple

# Basic Implementation: Framework Classes
class State(ABC):
    @abstractmethod
    def is_solution(self) -> bool:
        pass
        
    @abstractmethod
    def generate_children(self) -> List['State']:
        pass
        
    @abstractmethod
    def get_cost(self) -> float:
        pass
        
    @abstractmethod
    def get_bound(self) -> float:
        pass

class BranchAndBoundSolver:
    def __init__(self, minimize: bool = True):
        self.minimize = minimize
        self.best_solution: Optional[State] = None
        self.best_cost = float('inf') if minimize else float('-inf')

    def solve(self, initial_state: State) -> Optional[State]:
        pq = []
        
        priority = initial_state.get_bound() if self.minimize else -initial_state.get_bound()
        heapq.heappush(pq, (priority, id(initial_state), initial_state))

        while pq:
            current_priority, _, current_state = heapq.heappop(pq)
            bound = current_priority if self.minimize else -current_priority

            if self.minimize and bound >= self.best_cost:
                continue
            if not self.minimize and bound <= self.best_cost:
                continue

            if current_state.is_solution():
                cost = current_state.get_cost()
                if self.minimize and cost < self.best_cost:
                    self.best_cost = cost
                    self.best_solution = current_state
                elif not self.minimize and cost > self.best_cost:
                    self.best_cost = cost
                    self.best_solution = current_state
                continue

            for child in current_state.generate_children():
                child_bound = child.get_bound()
                
                if self.minimize and child_bound < self.best_cost:
                    heapq.heappush(pq, (child_bound, id(child), child))
                elif not self.minimize and child_bound > self.best_cost:
                    heapq.heappush(pq, (-child_bound, id(child), child))

        return self.best_solution

# Intermediate/Advanced Implementation: Applying Framework to 0/1 Knapsack
class KnapsackState(State):
    def __init__(self, level: int, current_weight: int, current_profit: int, 
                 items: List[Tuple[int, int]], capacity: int):
        self.level = level
        self.current_weight = current_weight
        self.current_profit = current_profit
        self.items = items
        self.capacity = capacity

    def is_solution(self) -> bool:
        return self.level == len(self.items) - 1

    def get_cost(self) -> float:
        return self.current_profit

    def get_bound(self) -> float:
        if self.current_weight > self.capacity:
            return 0.0
            
        profit_bound = self.current_profit
        total_weight = self.current_weight
        j = self.level + 1
        n = len(self.items)

        while j < n and total_weight + self.items[j][0] <= self.capacity:
            total_weight += self.items[j][0]
            profit_bound += self.items[j][1]
            j += 1

        if j < n:
            profit_bound += (self.capacity - total_weight) * (self.items[j][1] / self.items[j][0])

        return float(profit_bound)

    def generate_children(self) -> List['State']:
        if self.level == len(self.items) - 1:
            return []
            
        children = []
        next_level = self.level + 1
        next_w, next_v = self.items[next_level]
        
        if self.current_weight + next_w <= self.capacity:
            children.append(KnapsackState(next_level, self.current_weight + next_w, 
                                          self.current_profit + next_v, self.items, self.capacity))
        
        children.append(KnapsackState(next_level, self.current_weight, 
                                      self.current_profit, self.items, self.capacity))
                                      
        return children

# Performance Analysis
def performance_analysis():
    """
    The framework abstracts the BFS/Priority Queue logic. Performance depends entirely
    on the bounding function and state generation of the specific problem implementation.
    """
    pass

# Tests
def run_tests():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    
    items = sorted(zip(weights, values), key=lambda x: x[1]/x[0], reverse=True)
    
    solver = BranchAndBoundSolver(minimize=False)
    initial_state = KnapsackState(-1, 0, 0, items, capacity)
    best = solver.solve(initial_state)
    
    assert best is not None
    assert best.get_cost() == 7
    
    print("All Branch and Bound Framework tests passed!")

if __name__ == "__main__":
    run_tests()
