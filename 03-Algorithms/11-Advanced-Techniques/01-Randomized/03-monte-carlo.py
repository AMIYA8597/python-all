"""
# ==============================================================================
# LABORATORY: MONTE CARLO ALGORITHMS (PROBABILISTIC APPROXIMATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# There are two families of Randomized Algorithms in Computer Science:
#
# 1. LAS VEGAS ALGORITHMS:
#    - Example: Randomized Quicksort.
#    - Rule: The algorithm MUST return the 100% mathematically correct answer.
#    - Tradeoff: The runtime is probabilistic. It will *probably* run in 
#      O(N log N), but might theoretically degrade if you are extremely unlucky.
#
# 2. MONTE CARLO ALGORITHMS:
#    - Example: Miller-Rabin Primality Test, Calculating Pi via random darts.
#    - Rule: The algorithm MUST finish within a strict bounded time limit.
#    - Tradeoff: The answer is probabilistic! It might be slightly wrong. However, 
#      by running the algorithm multiple times (increasing $K$), the probability 
#      of failure drops exponentially towards zero.
#
# Why use Monte Carlo?
# Sometimes, calculating the exact mathematical answer is physically impossible. 
# Imagine trying to calculate the exact win probability of a complex board game 
# like Monopoly. The state space (combinations of dice rolls, cards, properties) 
# exceeds the number of atoms in the universe. You cannot use Dynamic Programming.
#
# Instead, you program two bots to play Monopoly against each other 1,000,000 times 
# using random dice rolls. If Bot A wins 620,000 times, you confidently estimate 
# their win probability at 62%. You bypassed the impossible math by leveraging 
# the Law of Large Numbers!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Las Vegas and Monte Carlo.
# - Leverage the Law of Large Numbers.
# - Calculate the value of Pi ($\pi$) using randomized geometric darts.
#
# ==============================================================================
"""

import random
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MONTE CARLO ENGINE (ESTIMATING PI)
# ==============================================================================
def estimate_pi_monte_carlo(num_darts: int) -> float:
    """
    Estimates the value of Pi by throwing random darts at a 2x2 square target 
    that contains a circle of radius 1.
    
    Math:
    Area of Square = 2 * 2 = 4
    Area of Circle = pi * r^2 = pi * (1)^2 = pi
    Ratio of Area = pi / 4
    
    If we throw random darts, the ratio of (Darts in Circle) / (Total Darts) 
    should perfectly converge to (pi / 4)!
    Therefore: pi = 4 * (Darts in Circle / Total Darts)
    """
    darts_inside_circle = 0
    
    for _ in range(num_darts):
        # Generate a random dart coordinate between -1.0 and 1.0
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        
        # Check if the dart landed inside the circle!
        # Pythagorean theorem: x^2 + y^2 <= radius^2
        # Since radius = 1, we check if x^2 + y^2 <= 1
        if x**2 + y**2 <= 1.0:
            darts_inside_circle += 1
            
    # Calculate the probabilistic approximation of Pi
    pi_estimate = 4 * (darts_inside_circle / num_darts)
    
    return pi_estimate


# ==============================================================================
# 4. MONTE CARLO ENGINE (INTEGRAL APPROXIMATION)
# ==============================================================================
def estimate_integral_monte_carlo(num_samples: int) -> float:
    """
    Calculates the Definite Integral of f(x) = x^2 from x=0 to x=2.
    
    Exact Calculus Math:
    Integral(x^2) = x^3 / 3. 
    Evaluate from 0 to 2: (8/3) - (0/3) = 2.6666...
    
    Monte Carlo approach:
    We generate random points in the bounding box: x in [0, 2], y in [0, 4] 
    (since f(2) = 4).
    We count how many points fall UNDER the curve y = x^2.
    """
    points_under_curve = 0
    
    box_width = 2.0
    box_height = 4.0
    box_area = box_width * box_height # Area = 8
    
    for _ in range(num_samples):
        x = random.uniform(0.0, box_width)
        y = random.uniform(0.0, box_height)
        
        # Is the point under the mathematical curve?
        if y <= (x**2):
            points_under_curve += 1
            
    # The integral is the Area under the curve!
    ratio = points_under_curve / num_samples
    estimated_area = ratio * box_area
    
    return estimated_area


def demonstrate_monte_carlo():
    section_header("Algorithm: Estimating Pi (Geometric Darts)")
    
    dart_counts = [100, 10_000, 1_000_000]
    
    print("Throwing darts at a 2x2 board...")
    for count in dart_counts:
        estimate = estimate_pi_monte_carlo(count)
        error = abs(math.pi - estimate)
        print(f"[{count:>9,} Darts] -> Pi: {estimate:.5f} | Error: {error:.5f}")
        
    print(f"Exact Math Pi    -> Pi: {math.pi:.5f}")
    
    section_header("Algorithm: Estimating Calculus Integrals")
    
    samples = 1_000_000
    print(f"Estimating Integral of x^2 from 0 to 2 using {samples:,} random samples...")
    
    integral_est = estimate_integral_monte_carlo(samples)
    exact_math = 8.0 / 3.0
    
    print(f"Monte Carlo Result : {integral_est:.5f}")
    print(f"Exact Calculus     : {exact_math:.5f}")
    print("Notice how randomness perfectly models complex mathematics!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Las Vegas and Monte Carlo algorithms?
   Answer: Las Vegas algorithms (like Randomized Quicksort) NEVER lie. They will run until they find the 100% mathematically correct answer, meaning their Runtime is the random variable. 
   Monte Carlo algorithms (like the Pi Dartboard) NEVER timeout. They run for exactly $K$ iterations and stop instantly, meaning their Accuracy is the random variable. 

2. How do we increase the accuracy of a Monte Carlo algorithm?
   Answer: The Law of Large Numbers. As the number of randomized trials (or samples) approaches infinity, the observed probabilistic average converges exactly to the true mathematical expected value. If you throw 10 darts, Pi might evaluate to 3.2. If you throw 10 Billion darts, Pi will evaluate to 3.14159... with microscopic variance. You can literally trade CPU compute time for mathematical precision.

3. Where is Monte Carlo used in Production?
   Answer: AlphaGo (Google DeepMind)! Chess and Go have too many possible board states for a computer to analyze every single move using Minimax (the game tree explodes). Instead, AlphaGo uses "Monte Carlo Tree Search (MCTS)". From the current board position, the AI simulates 10,000 completely random games until the end. If a specific move resulted in a win 70% of the time in the random simulations, the AI confidently plays that move! It bypassed the impossible math by relying on randomized statistical sampling.
"""

if __name__ == "__main__":
    demonstrate_monte_carlo()
    print("\n[SUCCESS] Laboratory: Monte Carlo Algorithms Completed.")
