"""
Module: 02-numpy-prob-dist
Description: Comprehensive textbook-grade interactive lesson on NumPy Probability Distributions.

===========================================================================
NUMPY PROBABILITY DISTRIBUTIONS: A DEEP DIVE
===========================================================================

Learning Objectives:
1. Understand the theoretical foundations of random variables and probability distributions.
2. Master NumPy's `numpy.random` module for generating random numbers from various distributions.
3. Compare discrete and continuous probability distributions.
4. Analyze the mathematical background, parameters, and Big-O performance of NumPy's PRNG (Pseudo-Random Number Generator).
5. Apply these distributions to solve real-world problems like Monte Carlo simulations and A/B testing.

---------------------------------------------------------------------------
1. MATHEMATICAL BACKGROUND
---------------------------------------------------------------------------
A random variable is a variable whose possible values are numerical outcomes of a random phenomenon.
There are two main types of probability distributions:
- Discrete: Outcomes are countable (e.g., rolling a die, number of emails received).
  Characterized by a Probability Mass Function (PMF).
- Continuous: Outcomes take any value in an interval (e.g., height, time taken).
  Characterized by a Probability Density Function (PDF).

Key Distributions covered in this module:
1. Uniform (Discrete/Continuous): Every outcome has an equal probability.
2. Normal (Gaussian): Continuous, symmetric, bell-shaped. Defined by mean (μ) and variance (σ^2).
   PDF: f(x) = (1 / (σ * sqrt(2π))) * e^(-(x - μ)^2 / (2σ^2))
3. Binomial: Discrete, number of successes in 'n' independent Bernoulli trials with probability 'p'.
   PMF: P(X=k) = C(n, k) * p^k * (1-p)^(n-k)
4. Poisson: Discrete, number of events occurring in a fixed interval of time/space, with known constant mean rate (λ).
   PMF: P(X=k) = (λ^k * e^-λ) / k!
5. Exponential: Continuous, time between events in a Poisson process.
   PDF: f(x) = λ * e^(-λx) for x ≥ 0

---------------------------------------------------------------------------
2. PERFORMANCE & BIG-O ANALYSIS
---------------------------------------------------------------------------
NumPy historically used the Mersenne Twister PRNG, but since version 1.17, it utilizes the 
PCG64 (Permuted Congruential Generator) by default via `numpy.random.Generator`.

- Time Complexity: Generating `N` samples from most standard distributions (Uniform, Normal) 
  has a Time Complexity of O(N).
- Space Complexity: O(N) to store the generated samples in an array.
- Vectorization: NumPy achieves massive speedups (often 10x-100x compared to pure Python `random` module)
  because the looping is implemented in optimized C code.

---------------------------------------------------------------------------
3. BEST PRACTICES
---------------------------------------------------------------------------
- Always use the modern `numpy.random.default_rng()` for generating random numbers rather than 
  the legacy `numpy.random` functions (like `np.random.randn`). 
- Seed your random number generator for reproducibility during testing and debugging.
- Choose the correct distribution based on the underlying real-world process you are modeling.
"""

import math
import time
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

# Ensure matplotlib is imported for potential plotting if run interactively, 
# though we'll primarily rely on numerical summaries in the terminal.
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# =========================================================================
# CLASS DEFINITION: ProbabilityDistributionsMaster
# =========================================================================

class ProbabilityDistributionsMaster:
    """
    A comprehensive educational class to demonstrate NumPy's random distributions.
    Utilizes the modern `np.random.default_rng()` approach.
    """

    def __init__(self, seed: Optional[int] = 42) -> None:
        """
        Initializes the random number generator.
        
        Args:
            seed (int, optional): Seed for reproducibility. Defaults to 42.
        """
        # Modern NumPy approach for random generation
        self.rng = np.random.default_rng(seed)
        self.seed = seed
        print(f"Initialized PRNG with seed: {self.seed}")

    def demonstrate_uniform(self, size: int = 10000) -> Dict[str, float]:
        """
        Demonstrates Continuous Uniform Distribution.
        
        A continuous uniform distribution U(a, b) means any value between 'a' and 'b'
        is equally likely. 
        Mean = (a + b) / 2
        Variance = (b - a)^2 / 12
        
        Args:
            size (int): Number of samples to generate.
            
        Returns:
            Dict[str, float]: Statistical summary of the samples.
        """
        print("\n--- 1. Continuous Uniform Distribution ---")
        low, high = 0.0, 10.0
        
        # Generate 'size' samples from U(0, 10)
        samples = self.rng.uniform(low=low, high=high, size=size)
        
        # Calculate empirical statistics
        emp_mean = np.mean(samples)
        emp_var = np.var(samples)
        
        # Theoretical statistics
        theo_mean = (low + high) / 2.0
        theo_var = ((high - low) ** 2) / 12.0
        
        print(f"Generated {size} samples from U({low}, {high}).")
        print(f"Theoretical Mean: {theo_mean:.4f} | Empirical Mean: {emp_mean:.4f}")
        print(f"Theoretical Var : {theo_var:.4f} | Empirical Var : {emp_var:.4f}")
        
        return {"emp_mean": float(emp_mean), "emp_var": float(emp_var)}

    def demonstrate_normal(self, size: int = 10000) -> Dict[str, float]:
        """
        Demonstrates Normal (Gaussian) Distribution.
        
        The Normal Distribution N(μ, σ^2) is the most important distribution in statistics
        due to the Central Limit Theorem.
        
        Args:
            size (int): Number of samples.
            
        Returns:
            Dict[str, float]: Statistical summary.
        """
        print("\n--- 2. Normal (Gaussian) Distribution ---")
        mu, sigma = 50.0, 5.0  # Mean and Standard Deviation
        
        # Generate samples
        samples = self.rng.normal(loc=mu, scale=sigma, size=size)
        
        emp_mean = np.mean(samples)
        emp_std = np.std(samples)
        
        # Checking the Empirical Rule (68-95-99.7)
        within_1_std = np.sum((samples > mu - sigma) & (samples < mu + sigma)) / size
        within_2_std = np.sum((samples > mu - 2*sigma) & (samples < mu + 2*sigma)) / size
        within_3_std = np.sum((samples > mu - 3*sigma) & (samples < mu + 3*sigma)) / size
        
        print(f"Generated {size} samples from N({mu}, {sigma}^2).")
        print(f"Theoretical Mean: {mu:.4f} | Empirical Mean: {emp_mean:.4f}")
        print(f"Theoretical Std : {sigma:.4f} | Empirical Std : {emp_std:.4f}")
        print("Empirical Rule Checks:")
        print(f"  ~68% within 1 std: {within_1_std * 100:.2f}%")
        print(f"  ~95% within 2 std: {within_2_std * 100:.2f}%")
        print(f"  ~99.7% within 3 std: {within_3_std * 100:.2f}%")
        
        return {"emp_mean": float(emp_mean), "emp_std": float(emp_std)}

    def demonstrate_binomial(self, size: int = 10000) -> Dict[str, float]:
        """
        Demonstrates Binomial Distribution.
        
        Models the number of successes in 'n' independent Bernoulli trials,
        each with success probability 'p'.
        Mean = n * p
        Variance = n * p * (1 - p)
        
        Args:
            size (int): Number of samples.
            
        Returns:
            Dict[str, float]: Statistical summary.
        """
        print("\n--- 3. Binomial Distribution ---")
        n, p = 20, 0.5  # 20 coin flips per trial, 50% chance of heads
        
        samples = self.rng.binomial(n=n, p=p, size=size)
        
        emp_mean = np.mean(samples)
        emp_var = np.var(samples)
        
        theo_mean = n * p
        theo_var = n * p * (1 - p)
        
        print(f"Generated {size} samples representing {n} trials with p={p}.")
        print(f"Theoretical Mean: {theo_mean:.4f} | Empirical Mean: {emp_mean:.4f}")
        print(f"Theoretical Var : {theo_var:.4f} | Empirical Var : {emp_var:.4f}")
        
        return {"emp_mean": float(emp_mean), "emp_var": float(emp_var)}

    def demonstrate_poisson(self, size: int = 10000) -> Dict[str, float]:
        """
        Demonstrates Poisson Distribution.
        
        Models the number of independent events occurring in a fixed interval,
        given a constant average rate λ (lambda).
        Mean = λ
        Variance = λ
        
        Args:
            size (int): Number of samples.
            
        Returns:
            Dict[str, float]: Statistical summary.
        """
        print("\n--- 4. Poisson Distribution ---")
        lam = 3.5  # e.g., 3.5 emails received per hour
        
        samples = self.rng.poisson(lam=lam, size=size)
        
        emp_mean = np.mean(samples)
        emp_var = np.var(samples)
        
        print(f"Generated {size} samples from Poisson(λ={lam}).")
        print(f"Theoretical Mean: {lam:.4f} | Empirical Mean: {emp_mean:.4f}")
        print(f"Theoretical Var : {lam:.4f} | Empirical Var : {emp_var:.4f}")
        
        return {"emp_mean": float(emp_mean), "emp_var": float(emp_var)}

    def demonstrate_exponential(self, size: int = 10000) -> Dict[str, float]:
        """
        Demonstrates Exponential Distribution.
        
        Models the time elapsed between events in a Poisson process.
        Mean = 1 / λ (NumPy scale parameter = 1/λ)
        Variance = 1 / λ^2
        
        Args:
            size (int): Number of samples.
            
        Returns:
            Dict[str, float]: Statistical summary.
        """
        print("\n--- 5. Exponential Distribution ---")
        scale_param = 2.0  # scale = 1/λ, so λ = 0.5 events per unit time
        
        samples = self.rng.exponential(scale=scale_param, size=size)
        
        emp_mean = np.mean(samples)
        emp_var = np.var(samples)
        
        theo_mean = scale_param
        theo_var = scale_param ** 2
        
        print(f"Generated {size} samples from Exponential(scale={scale_param}).")
        print(f"Theoretical Mean: {theo_mean:.4f} | Empirical Mean: {emp_mean:.4f}")
        print(f"Theoretical Var : {theo_var:.4f} | Empirical Var : {emp_var:.4f}")
        
        return {"emp_mean": float(emp_mean), "emp_var": float(emp_var)}


# =========================================================================
# REAL-WORLD APPLICATION 1: MONTE CARLO SIMULATION (PI ESTIMATION)
# =========================================================================
def estimate_pi_monte_carlo(num_samples: int = 10_000_000) -> float:
    """
    Estimates the value of Pi using a Monte Carlo simulation.
    
    Algorithm:
    1. Inscribe a circle of radius r=1 inside a square of side 2 (from -1 to 1).
    2. Area of circle = π*r^2 = π.
    3. Area of square = 2*2 = 4.
    4. Ratio of areas = π / 4.
    5. Generate N random points uniformly inside the square.
    6. Count how many fall inside the circle (x^2 + y^2 <= 1).
    7. Pi ≈ 4 * (points_in_circle / total_points).
    
    Args:
        num_samples (int): Number of random points to generate.
        
    Returns:
        float: Estimated value of Pi.
    """
    print("\n--- Real-World App 1: Monte Carlo Pi Estimation ---")
    print(f"Running simulation with {num_samples:,} points...")
    
    rng = np.random.default_rng(42)
    start_time = time.time()
    
    # Generate points in the square [-1, 1] x [-1, 1]
    # O(N) time and space complexity
    x = rng.uniform(-1.0, 1.0, size=num_samples)
    y = rng.uniform(-1.0, 1.0, size=num_samples)
    
    # Check if inside circle (vectorized operation)
    # x^2 + y^2 <= 1
    inside_circle = (x**2 + y**2) <= 1.0
    
    points_in_circle = np.sum(inside_circle)
    pi_estimate = 4.0 * points_in_circle / num_samples
    
    end_time = time.time()
    
    print(f"Estimated Pi : {pi_estimate:.6f}")
    print(f"Actual Pi    : {math.pi:.6f}")
    print(f"Error        : {abs(pi_estimate - math.pi):.6f}")
    print(f"Execution Time: {end_time - start_time:.4f} seconds")
    
    return pi_estimate


# =========================================================================
# REAL-WORLD APPLICATION 2: RANDOM WALK SIMULATION (FINANCE)
# =========================================================================
def simulate_random_walk(steps: int = 1000, simulations: int = 5) -> np.ndarray:
    """
    Simulates a 1D Random Walk, often used as a simple model for stock price movements 
    or particle diffusion (Brownian Motion).
    
    Algorithm:
    1. Start at 0.
    2. At each step, move +1 or -1 with equal probability.
    3. The position at step N is the cumulative sum of the steps.
    
    Args:
        steps (int): Number of steps in the random walk.
        simulations (int): Number of independent random walks to simulate.
        
    Returns:
        np.ndarray: Matrix of shape (simulations, steps) representing the paths.
    """
    print(f"\n--- Real-World App 2: Random Walk ({simulations} paths, {steps} steps) ---")
    rng = np.random.default_rng()
    
    # Generate random steps: +1 or -1
    # We first generate binomial with n=1, p=0.5 (0 or 1), then scale to -1 or 1
    # 0 -> -1, 1 -> +1 (Mapping: 2 * x - 1)
    step_choices = rng.binomial(n=1, p=0.5, size=(simulations, steps))
    step_values = 2 * step_choices - 1
    
    # Calculate cumulative sum across the steps axis (axis=1)
    paths = np.cumsum(step_values, axis=1)
    
    # Print the final position of each simulation
    for i in range(simulations):
        print(f"Simulation {i+1} Final Position: {paths[i, -1]}")
        
    return paths


# =========================================================================
# PERFORMANCE COMPARISON: PURE PYTHON VS NUMPY
# =========================================================================
def compare_performance(size: int = 1_000_000) -> None:
    """
    Compares the performance of generating normal distribution samples 
    using pure Python's `random` module vs NumPy.
    
    Args:
        size (int): Number of samples to generate.
    """
    import random
    
    print(f"\n--- Performance Comparison: Generating {size:,} Normal Samples ---")
    
    # Pure Python
    start_py = time.time()
    py_samples = [random.gauss(0, 1) for _ in range(size)]
    end_py = time.time()
    py_time = end_py - start_py
    print(f"Pure Python execution time: {py_time:.4f} seconds")
    
    # NumPy
    rng = np.random.default_rng()
    start_np = time.time()
    np_samples = rng.normal(0, 1, size)
    end_np = time.time()
    np_time = end_np - start_np
    print(f"NumPy execution time      : {np_time:.4f} seconds")
    
    speedup = py_time / np_time if np_time > 0 else float('inf')
    print(f"NumPy is ~{speedup:.1f}x faster!")


# =========================================================================
# INTERVIEW CHALLENGE: MARKOV CHAIN STATE TRANSITION
# =========================================================================
def interview_challenge_markov_chain(steps: int = 10) -> List[int]:
    """
    Interview Challenge: Markov Chain Simulation
    
    Problem Statement:
    You are given a system with 3 states (0, 1, 2) and a transition matrix P,
    where P[i][j] is the probability of transitioning from state i to state j.
    Simulate the sequence of states for `steps` steps, starting at state 0.
    
    P = [
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ]
    
    Args:
        steps (int): Number of transitions to simulate.
        
    Returns:
        List[int]: The sequence of states visited.
    """
    print(f"\n--- Interview Challenge: Markov Chain Simulation ({steps} steps) ---")
    
    transition_matrix = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ])
    
    rng = np.random.default_rng(99)
    current_state = 0
    history = [current_state]
    
    for _ in range(steps):
        # np.random.choice allows sampling from an array given specific probabilities
        probabilities = transition_matrix[current_state]
        next_state = rng.choice([0, 1, 2], p=probabilities)
        history.append(next_state)
        current_state = next_state
        
    print(f"State sequence: {history}")
    return history


# =========================================================================
# TEST SUITE
# =========================================================================
def run_tests() -> None:
    """
    Validates the statistical properties using assertions.
    Since randomness is involved, we set seeds and check within tolerances.
    """
    print("\n--- Running Tests ---")
    
    # 1. Test Seed Reproducibility
    rng1 = np.random.default_rng(100)
    rng2 = np.random.default_rng(100)
    arr1 = rng1.normal(0, 1, 100)
    arr2 = rng2.normal(0, 1, 100)
    assert np.array_equal(arr1, arr2), "Random seed failed to produce identical sequences."
    
    # 2. Test Uniform Distribution Bounds
    master = ProbabilityDistributionsMaster(seed=42)
    uni_samples = master.rng.uniform(low=-5, high=5, size=1000)
    assert np.all((uni_samples >= -5) & (uni_samples < 5)), "Uniform distribution bounds violation."
    
    # 3. Test Pi Estimation (Tolerant check)
    pi_est = estimate_pi_monte_carlo(100_000) # Smaller sample for fast tests
    assert math.isclose(pi_est, math.pi, abs_tol=0.05), f"Pi estimation way off: {pi_est}"
    
    print("All tests passed successfully! The properties of the PRNG are solid.")


# =========================================================================
# MAIN EXECUTION BLOCK
# =========================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("NUMPY PROBABILITY DISTRIBUTIONS: INTERACTIVE LESSON".center(70))
    print("=" * 70)
    
    master = ProbabilityDistributionsMaster(seed=42)
    
    # Demonstrate Distributions
    master.demonstrate_uniform(100_000)
    master.demonstrate_normal(100_000)
    master.demonstrate_binomial(100_000)
    master.demonstrate_poisson(100_000)
    master.demonstrate_exponential(100_000)
    
    # Real-World Applications
    estimate_pi_monte_carlo(num_samples=5_000_000)
    simulate_random_walk(steps=20, simulations=3)
    
    # Performance
    compare_performance(size=1_000_000)
    
    # Interview Challenge
    interview_challenge_markov_chain(steps=15)
    
    # Testing
    run_tests()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETED SUCCESSFULLY".center(70))
    print("=" * 70)
