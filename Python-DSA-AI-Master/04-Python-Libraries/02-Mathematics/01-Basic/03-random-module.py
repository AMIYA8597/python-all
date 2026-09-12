"""
Module: 03-random-module.py
Description: A comprehensive, textbook-grade interactive lesson on Python's `random` module.

================================================================================
PYTHON DSA MASTER: RANDOM MODULE (PSEUDO-RANDOM NUMBER GENERATION)
================================================================================

Learning Objectives:
1. Understand the theoretical background of Pseudo-Random Number Generators (PRNGs),
   specifically the Mersenne Twister algorithm used by Python.
2. Master core `random` functions for integers, sequences, and real numbers.
3. Learn to generate random data based on specific statistical distributions 
   (Uniform, Normal/Gaussian, Exponential, etc.).
4. Understand the limitations of PRNGs and when to use `secrets` (SystemRandom) 
   for cryptographically secure randomness.
5. Analyze time and space complexity (Big-O) of random operations.
6. Solve real-world interview and engineering challenges using randomness.

Mathematical Background:
------------------------
Python uses the Mersenne Twister (MT19937) as the core generator. It produces 
53-bit precision floats and has a period of 2**19937 - 1. 

Why "Pseudo"?
A PRNG starts with an initial value called a "seed". It applies deterministic 
mathematical operations to produce the next number. Given the same seed, the 
sequence of generated numbers is exactly the same. This reproducibility is useful 
for debugging and simulations, but vulnerable to cryptographic attacks.

Formulas for distributions:
- Uniform(a, b): f(x) = 1 / (b - a)
- Gaussian/Normal: Uses the Box-Muller transform or the Ziggurat algorithm 
  to transform uniform random numbers into normal-distributed numbers.

Big-O Analysis:
---------------
- `random.random()`: O(1) time and space.
- `random.randint(a, b)`: O(1) time and space.
- `random.choice(seq)`: O(1) time, O(1) space. (Array access is O(1)).
- `random.shuffle(seq)`: O(N) time using the Fisher-Yates shuffle algorithm. O(1) auxiliary space.
- `random.sample(population, k)`: O(k) time and space if k is small, up to O(N) depending on 
  the implementation details (sets vs arrays).

Real-World Applications:
------------------------
- Monte Carlo simulations (e.g., estimating Pi).
- Randomized algorithms (QuickSort pivot selection).
- Machine Learning (initializing neural network weights, shuffling datasets).
- Game Development (loot drops, enemy spawning logic).
- A/B Testing in software engineering.
"""

import math
import random
import time
from typing import List, Dict, Any, Tuple, Optional

# ==============================================================================
# SECTION 1: SEEDING & REPRODUCIBILITY
# ==============================================================================

def explore_seeding() -> None:
    """
    Demonstrates deterministic nature of Pseudo-Random Number Generators.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    print("--- Section 1: Seeding & Reproducibility ---")
    
    # Setting a seed guarantees the same output sequence
    random.seed(42)
    val1 = random.random()
    val2 = random.randint(1, 100)
    
    print(f"Seed 42 -> Random Float: {val1:.6f}, Random Int: {val2}")
    
    # Resetting the seed to 42 reproduces exactly the same sequence
    random.seed(42)
    val3 = random.random()
    val4 = random.randint(1, 100)
    
    print(f"Seed 42 (again) -> Random Float: {val3:.6f}, Random Int: {val4}")
    
    assert val1 == val3 and val2 == val4, "Seeding failed to reproduce results!"
    print("Lesson: Always use seeding when you need reproducible tests or ML environments.\n")


# ==============================================================================
# SECTION 2: INTEGERS & SEQUENCES
# ==============================================================================

def explore_integers_and_sequences() -> None:
    """
    Demonstrates random functions for integers and sequence selections.
    
    Time/Space Complexity:
    - randint, randrange: O(1) Time, O(1) Space
    - choice: O(1) Time, O(1) Space
    - choices: O(k) Time, O(k) Space
    - shuffle: O(N) Time, O(1) Space
    - sample: O(k) Time, O(k) Space
    """
    print("--- Section 2: Integers and Sequences ---")
    
    # 1. Integers
    # randint(a, b) includes both endpoints [a, b]
    r_int = random.randint(10, 20)
    # randrange(start, stop, step) includes start, excludes stop [start, stop)
    r_range = random.randrange(10, 21, 2) 
    print(f"Random integer [10, 20]: {r_int}")
    print(f"Random even integer [10, 21): {r_range}")
    
    # 2. Sequence Selection
    deck = ['Ace', 'King', 'Queen', 'Jack', '10', '9']
    
    # Pick exactly one element
    chosen_card = random.choice(deck)
    print(f"random.choice(deck): {chosen_card}")
    
    # Pick multiple elements WITH replacement
    # weights allow biased selection (e.g., 'Ace' has higher chance)
    weights = [5, 1, 1, 1, 1, 1]
    with_replacement = random.choices(deck, weights=weights, k=3)
    print(f"random.choices (with replacement, weighted): {with_replacement}")
    
    # Pick multiple elements WITHOUT replacement
    without_replacement = random.sample(deck, k=3)
    print(f"random.sample (without replacement): {without_replacement}")
    
    # 3. Shuffling in-place (Fisher-Yates Shuffle O(N))
    deck_copy = deck.copy()
    random.shuffle(deck_copy)
    print(f"random.shuffle (in-place): {deck_copy}\n")


# ==============================================================================
# SECTION 3: REAL NUMBERS & PROBABILITY DISTRIBUTIONS
# ==============================================================================

def explore_distributions() -> None:
    """
    Demonstrates continuous distributions available in the random module.
    """
    print("--- Section 3: Real Numbers & Distributions ---")
    
    # Uniform float in [0.0, 1.0)
    basic_float = random.random()
    print(f"random.random() [0.0, 1.0): {basic_float:.4f}")
    
    # Uniform float in [a, b]
    uniform_float = random.uniform(5.5, 10.5)
    print(f"random.uniform(5.5, 10.5): {uniform_float:.4f}")
    
    # Gaussian/Normal Distribution: gauss(mu, sigma)
    # mu is the mean, sigma is the standard deviation
    gauss_val = random.gauss(0, 1) # Standard Normal Distribution
    print(f"random.gauss(mu=0, sigma=1): {gauss_val:.4f}")
    
    # Exponential Distribution: expovariate(lambd)
    # Useful for simulating time between independent events (e.g., arrivals)
    lambd = 1.5
    expo_val = random.expovariate(lambd)
    print(f"random.expovariate(lambd=1.5): {expo_val:.4f}\n")


# ==============================================================================
# SECTION 4: CRYPTOGRAPHICALLY SECURE RANDOMNESS
# ==============================================================================

def explore_system_random() -> None:
    """
    Shows how to use SystemRandom for security-sensitive applications.
    The default `random` module is predictable. `SystemRandom` uses OS-level
    randomness (e.g., /dev/urandom) which is cryptographically secure.
    """
    print("--- Section 4: Cryptographically Secure Randomness ---")
    secure_rng = random.SystemRandom()
    
    token = secure_rng.randint(100000, 999999)
    print(f"Secure OTP generated using SystemRandom: {token}")
    
    # Standard choice vs secure choice
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%'
    password = ''.join(secure_rng.choice(chars) for _ in range(12))
    print(f"Secure 12-char Password: {password}\n")


# ==============================================================================
# SECTION 5: REAL-WORLD INTERVIEW CHALLENGE (MONTE CARLO SIMULATION)
# ==============================================================================

def estimate_pi_monte_carlo(num_samples: int) -> float:
    """
    Interview Challenge: Estimate the value of Pi using random numbers.
    
    Algorithm Explanation:
    1. Imagine a circle of radius R=1 inscribed in a square of side 2.
    2. Area of circle = Pi * R^2 = Pi.
    3. Area of square = (2R)^2 = 4.
    4. Ratio = Area of circle / Area of square = Pi / 4.
    5. If we randomly throw darts into the square, the fraction of darts 
       that fall inside the circle will approximate Pi / 4.
       
    Time Complexity: O(N) where N is num_samples.
    Space Complexity: O(1)
    """
    print("--- Section 5: Monte Carlo Simulation to Estimate Pi ---")
    
    points_inside_circle = 0
    
    for _ in range(num_samples):
        # Generate x, y between -1.0 and 1.0
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        # Check if point is inside the unit circle (x^2 + y^2 <= 1)
        if x**2 + y**2 <= 1:
            points_inside_circle += 1
            
    # Pi / 4 = points_inside_circle / num_samples
    pi_estimate = 4 * points_inside_circle / num_samples
    
    print(f"Samples: {num_samples}")
    print(f"Estimated Pi: {pi_estimate:.6f}")
    print(f"Actual Pi:    {math.pi:.6f}")
    print(f"Error:        {abs(math.pi - pi_estimate):.6f}\n")
    
    return pi_estimate


# ==============================================================================
# SECTION 6: ALGORITHMIC APPLICATION (RESERVOIR SAMPLING)
# ==============================================================================

def reservoir_sampling(stream: List[int], k: int) -> List[int]:
    """
    Interview Challenge: Reservoir Sampling.
    Given a stream of unknown size, select k items uniformly at random.
    
    Algorithm (Algorithm R by Alan Waterman):
    1. Store the first k elements in an array (the reservoir).
    2. For the i-th element (i > k), generate a random number j between 0 and i.
    3. If j < k, replace reservoir[j] with the i-th element.
    
    Time Complexity: O(N) where N is the length of the stream.
    Space Complexity: O(k) for the reservoir.
    """
    print("--- Section 6: Reservoir Sampling ---")
    
    reservoir = []
    
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            # Randomly decide whether to replace an existing item
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
                
    print(f"Stream Size: {len(stream)}, Sample Size (k): {k}")
    print(f"Selected Reservoir: {reservoir}\n")
    return reservoir


# ==============================================================================
# TEST SUITE
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite for the random module implementations.
    """
    print("--- Running Tests ---")
    
    # 1. Test Seed
    random.seed(1)
    val1 = random.randint(1, 100)
    random.seed(1)
    val2 = random.randint(1, 100)
    assert val1 == val2, "Seed test failed"
    
    # 2. Test Monte Carlo Pi Estimation
    pi_est = estimate_pi_monte_carlo(1000) # Small sample for quick test
    assert 2.0 <= pi_est <= 4.0, "Pi estimation is way off"
    
    # 3. Test Reservoir Sampling
    stream = list(range(100))
    res = reservoir_sampling(stream, 5)
    assert len(res) == 5, "Reservoir sampling size mismatch"
    assert all(0 <= x < 100 for x in res), "Reservoir elements out of bounds"
    
    print("All tests passed successfully!\n")


if __name__ == "__main__":
    print(f"{'='*60}")
    print("EXPLORING PYTHON RANDOM MODULE".center(60))
    print(f"{'='*60}\n")
    
    # Resetting seed in case of previous test contamination
    random.seed(time.time())
    
    explore_seeding()
    explore_integers_and_sequences()
    explore_distributions()
    explore_system_random()
    
    # Algorithmic challenges
    estimate_pi_monte_carlo(1_000_000)
    reservoir_sampling(list(range(10000)), k=10)
    
    run_tests()
    
    print(f"{'='*60}")
    print("END OF LESSON".center(60))
    print(f"{'='*60}\n")
