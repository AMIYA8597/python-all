"""
## A. Concept Name
Genetic Algorithms

## B. Concept Explanation
Genetic Algorithms (GA) are search heuristics inspired by Charles Darwin's
theory of natural evolution. They reflect the process of natural selection
where the fittest individuals are selected for reproduction to produce
offspring of the next generation.

## C. Learning Objectives
1. Understand evolutionary algorithms and survival of the fittest.
2. Implement Population, Crossover, Mutation, and Selection operations.
3. Optimize a simple mathematical function using GA.

## D. Type Hints & Edge Cases
- Premature convergence (all individuals identical).
- Tuning mutation rate.

## X. Project Connection
This algorithm serves as a foundational component for advanced optimization
tasks, providing a scalable heuristic approach for complex spaces where exact
algorithms are unfeasible, such as hyperparameter tuning or large NP-hard
problems like Knapsack optimizations.
"""

import random
from typing import List, Callable, Tuple

# Advanced Implementation: Function Maximization GA
# Goal: Maximize f(x) = x * sin(10 * pi * x) + 1.0 for x in [-1, 2]

def objective_function(x: float) -> float:
    import math
    return x * math.sin(10 * math.pi * x) + 1.0

def create_individual(bounds: Tuple[float, float]) -> float:
    return random.uniform(bounds[0], bounds[1])

def selection(population: List[float], fitnesses: List[float]) -> float:
    """Tournament selection."""
    idx1, idx2 = random.sample(range(len(population)), 2)
    if fitnesses[idx1] > fitnesses[idx2]:
        return population[idx1]
    return population[idx2]

def crossover(parent1: float, parent2: float) -> float:
    """Blend crossover."""
    alpha = random.random()
    return alpha * parent1 + (1 - alpha) * parent2

def mutate(child: float, bounds: Tuple[float, float], rate: float = 0.1) -> float:
    """Gaussian mutation."""
    if random.random() < rate:
        child += random.gauss(0, 0.1)
        child = max(bounds[0], min(bounds[1], child)) # clamp
    return child

def genetic_algorithm(bounds: Tuple[float, float], generations: int = 50, pop_size: int = 20) -> Tuple[float, float]:
    population = [create_individual(bounds) for _ in range(pop_size)]
    
    best_ind = population[0]
    best_fit = objective_function(best_ind)
    
    for gen in range(generations):
        fitnesses = [objective_function(ind) for ind in population]
        
        # Track best
        for i, fit in enumerate(fitnesses):
            if fit > best_fit:
                best_fit = fit
                best_ind = population[i]
                
        new_population = []
        for _ in range(pop_size):
            p1 = selection(population, fitnesses)
            p2 = selection(population, fitnesses)
            child = crossover(p1, p2)
            child = mutate(child, bounds)
            new_population.append(child)
            
        population = new_population
        
    return best_ind, best_fit

# Interview Challenge
def challenge_knapsack_ga_chromosome(weights: List[int], values: List[int], capacity: int) -> List[int]:
    """
    Challenge: Create a random chromosome for the 0/1 knapsack problem
    that strictly satisfies the capacity constraint.
    """
    chrom = [0] * len(weights)
    indices = list(range(len(weights)))
    random.shuffle(indices)
    
    current_weight = 0
    for idx in indices:
        if current_weight + weights[idx] <= capacity:
            chrom[idx] = 1
            current_weight += weights[idx]
            
    return chrom

def test_ga():
    bounds = (-1.0, 2.0)
    best_x, best_y = genetic_algorithm(bounds, generations=20, pop_size=10)
    assert bounds[0] <= best_x <= bounds[1], "Out of bounds"
    
    weights = [10, 20, 30]
    values = [60, 100, 120]
    cap = 50
    chrom = challenge_knapsack_ga_chromosome(weights, values, cap)
    assert sum(w*c for w, c in zip(weights, chrom)) <= cap, "Capacity exceeded"
    
    print("All tests passed.")

if __name__ == "__main__":
    print("Genetic Algorithm Execution\n" + "-"*30)
    test_ga()
