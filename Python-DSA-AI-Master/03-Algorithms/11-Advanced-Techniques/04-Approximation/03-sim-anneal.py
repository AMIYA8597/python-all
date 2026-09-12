"""
Module: Simulated Annealing
===========================

Learning Objectives:
1. Understand the thermodynamic analogy of Simulated Annealing (SA).
2. Learn how SA escapes local optima by accepting worse solutions early on.
3. Implement a cooling schedule and acceptance probability function.

Concept Explanation:
SA is a probabilistic technique for approximating the global optimum of a given function.
It uses a 'temperature' parameter that decreases over time. When the temperature is high,
the algorithm explores the search space broadly. As it cools, it exploits local areas to
find exact peaks/valleys.

Type Hints & Edge Cases:
- Temperature reaching 0 (prevent division by zero).
- Proper neighbor generation.
"""

import math
import random
from typing import Callable, Tuple

# Basic Implementation: Function Minimization using SA
# Objective: Minimize f(x) = x^2 + 4 * cos(x)

def objective_function(x: float) -> float:
    return x**2 + 4 * math.cos(x)

def get_neighbor(x: float, step_size: float = 0.5) -> float:
    return x + random.uniform(-step_size, step_size)

def acceptance_probability(old_cost: float, new_cost: float, temp: float) -> float:
    if new_cost < old_cost:
        return 1.0
    if temp == 0:
        return 0.0
    return math.exp((old_cost - new_cost) / temp)

def simulated_annealing(init_x: float, init_temp: float, cooling_rate: float, min_temp: float = 1e-5) -> Tuple[float, float]:
    current_x = init_x
    current_cost = objective_function(current_x)
    best_x = current_x
    best_cost = current_cost
    
    temp = init_temp
    
    while temp > min_temp:
        neighbor_x = get_neighbor(current_x)
        neighbor_cost = objective_function(neighbor_x)
        
        if random.random() < acceptance_probability(current_cost, neighbor_cost, temp):
            current_x = neighbor_x
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_cost = current_cost
                best_x = current_x
                
        temp *= cooling_rate # Cooling schedule
        
    return best_x, best_cost

# Interview Challenge
def challenge_cooling_schedules(temp: float, iteration: int) -> float:
    """
    Challenge: Implement different cooling schedules.
    Linear: temp - alpha
    Logarithmic: T_0 / log(iteration + 1)
    """
    alpha = 0.01
    t_0 = 100.0
    linear = temp - alpha if temp - alpha > 0 else 0
    logarithmic = t_0 / math.log(iteration + 1) if iteration > 0 else t_0
    return logarithmic

def test_sa():
    best_x, best_cost = simulated_annealing(init_x=5.0, init_temp=100.0, cooling_rate=0.95)
    # The global minimum is near 0 or somewhere close
    assert isinstance(best_x, float), "Result should be float"
    assert isinstance(best_cost, float), "Cost should be float"
    
    assert challenge_cooling_schedules(100.0, 1) > 0, "Cooling failed"
    print("All tests passed.")

if __name__ == "__main__":
    print("Simulated Annealing Execution\\n" + "-"*30)
    test_sa()
