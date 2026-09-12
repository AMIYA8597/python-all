"""
Monte Carlo Algorithms

Learning Objectives:
1. Define a Monte Carlo algorithm and understand its probabilistic nature.
2. Differentiate Monte Carlo algorithms (deterministic time, probabilistic correctness) 
   from Las Vegas algorithms.
3. Implement practical examples like Pi estimation and primality testing.

Concept Explanation:
Monte Carlo algorithms are randomized algorithms whose output may be incorrect with a certain
probability, but their runtime is deterministic or bounded. The more iterations you run,
the higher the probability of correctness.
"""

import random
from typing import Tuple

# Basic Implementation: Estimating Pi using Monte Carlo
def estimate_pi(num_samples: int) -> float:
    """Estimates Pi by sampling random points in a unit square."""
    inside_circle = 0
    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x*x + y*y <= 1:
            inside_circle += 1
            
    return 4 * inside_circle / num_samples

# Intermediate Implementation: Karger's Min-Cut Algorithm
def kargers_min_cut(edges: list, num_vertices: int) -> int:
    """A simplified Monte Carlo implementation of Karger's Min-Cut."""
    parent = list(range(num_vertices))
    
    def find(i):
        if parent[i] == i: return i
        parent[i] = find(parent[i])
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        parent[root_i] = root_j

    vertices_left = num_vertices
    while vertices_left > 2:
        u, v = random.choice(edges)
        set_u = find(u)
        set_v = find(v)
        
        if set_u != set_v:
            vertices_left -= 1
            union(set_u, set_v)
            
    min_cut = 0
    for u, v in edges:
        if find(u) != find(v):
            min_cut += 1
            
    return min_cut

# Advanced Implementation: Fermat's Primality Test
def fermat_is_prime(n: int, k: int = 5) -> bool:
    """Fermat's Primality Test is a Monte Carlo algorithm."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
            
    return True

# Performance Analysis
def performance_analysis():
    """
    Time Complexity:
    - Pi Estimation: O(num_samples)
    - Fermat Primality: O(k * log(n))
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Extremely small num_samples yields bad estimates.
    - Carmichael numbers fool Fermat's test.
    """
    pass

# Interview Challenge
def challenge_monte_carlo_integration(func, a: float, b: float, num_samples: int) -> float:
    """Challenge: Perform numerical integration of a 1D function."""
    total = 0
    for _ in range(num_samples):
        x = random.uniform(a, b)
        total += func(x)
    return (b - a) * (total / num_samples)

# Tests
def run_tests():
    pi_est = estimate_pi(100000)
    assert 3.1 <= pi_est <= 3.2
    
    assert fermat_is_prime(7, k=5) is True
    assert fermat_is_prime(15, k=5) is False
    assert fermat_is_prime(97, k=5) is True
    
    edges = [(0,1), (0,2), (1,2), (1,3), (2,3), (3,4), (3,5), (4,5)]
    cut = kargers_min_cut(edges, 6)
    assert cut >= 1
    
    integral = challenge_monte_carlo_integration(lambda x: x**2, 0, 1, 100000)
    assert 0.32 <= integral <= 0.34
    
    print("All Monte Carlo tests passed!")

if __name__ == "__main__":
    run_tests()
