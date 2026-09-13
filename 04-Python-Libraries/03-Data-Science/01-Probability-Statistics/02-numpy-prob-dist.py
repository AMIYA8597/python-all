"""
# ==============================================================================
# LABORATORY: PROBABILITY & DISTRIBUTIONS (NUMPY.RANDOM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned about the standard Python `random` module previously. It is fine 
# for picking a random card from a deck of 52. 
# 
# But what if you are building an AI simulation and need to instantly generate 
# 10 Million random numbers conforming to a precise Gaussian Bell Curve? The 
# standard Python `random` module would take forever because of the Python `for` 
# loop overhead.
#
# NumPy provides a vectorized, highly-optimized Random module built in C. 
# It can generate arrays containing millions of complex probabilistic variables 
# (Normal, Binomial, Poisson) in milliseconds.
#
# CRITICAL EVOLUTION:
# In 2019, NumPy completely overhauled its random architecture. The old, 
# global `np.random.seed()` (Mersenne Twister) was replaced by the modern, 
# object-oriented `np.random.default_rng()` (PCG-64 algorithm), which is 
# significantly faster and mathematically vastly superior for statistical simulations.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Instantiate the modern `Generator` API (PCG-64).
# - Generate exact mathematical distributions (Normal, Binomial, Poisson).
# - Perform rapid array-based Bootstrapping and shuffling.
#
# ==============================================================================
"""

import numpy as np
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MODERN GENERATOR API (PCG-64)
# ==============================================================================
def demonstrate_modern_rng():
    section_header("The Modern Generator (default_rng)")
    
    # THE OLD WAY (Pre-2019, still commonly seen but officially discouraged!)
    # np.random.seed(42)
    # x = np.random.rand(10)
    # The old way uses a global state. If a third-party library imports numpy 
    # and changes the global seed, it destroys the reproducibility of your entire app!
    
    # THE NEW WAY (Modern NumPy)
    # We instantiate a local, isolated Generator object. 
    # It uses the PCG-64 (Permuted Congruential Generator) algorithm, which is 
    # statistically vastly superior to the Mersenne Twister.
    rng = np.random.default_rng(seed=42)
    
    print("Generating 5 random floats [0.0, 1.0) using modern PCG-64:")
    print(rng.random(5))
    
    print("\nGenerating 5 random Integers [1, 100]:")
    print(rng.integers(low=1, high=100, size=5))


# ==============================================================================
# 4. PROBABILITY DISTRIBUTIONS
# ==============================================================================
def demonstrate_distributions():
    section_header("Probability Distributions")
    
    rng = np.random.default_rng(seed=1337)
    
    # 1. NORMAL (GAUSSIAN) DISTRIBUTION
    # The Bell Curve! (e.g., Human Heights, Test Scores)
    # loc = Mean, scale = Standard Deviation
    mu, sigma = 100.0, 15.0 # IQ Scores
    iq_samples = rng.normal(loc=mu, scale=sigma, size=10)
    print("Normal Distribution (Simulated IQ Scores):")
    print(np.round(iq_samples, 1))
    
    # 2. BINOMIAL DISTRIBUTION
    # Probability of Success/Failure across N trials (e.g., Coin Flips)
    # Imagine flipping 10 coins. What is the total number of "Heads" (Successes)?
    # We run this experiment 5 times.
    n, p = 10, 0.5 # 10 flips, 50% chance of success
    coin_experiments = rng.binomial(n=n, p=p, size=5)
    print(f"\nBinomial Distribution (Total Heads from 10 coin flips, 5 trials):")
    print(coin_experiments) # e.g. [5, 4, 7, 5, 6]
    
    # 3. POISSON DISTRIBUTION
    # Modeling the frequency of rare events over a fixed period of time.
    # e.g., A web server receives an average of 3 crashes per day (lam = 3).
    # How many crashes will happen each day for the next 7 days?
    lam = 3.0
    server_crashes = rng.poisson(lam=lam, size=7)
    print(f"\nPoisson Distribution (Simulated daily crashes over a week):")
    print(server_crashes)


# ==============================================================================
# 5. HIGH-PERFORMANCE BOOTSTRAPPING & SHUFFLING
# ==============================================================================
def demonstrate_bootstrapping():
    section_header("Bootstrapping & Random Choice")
    
    rng = np.random.default_rng()
    
    # 1. MASSIVE VECTORIZED CHOICE
    # Imagine simulating a weighted die roll 1,000,000 times!
    faces = ['A', 'B', 'C', 'D']
    probabilities = [0.1, 0.2, 0.2, 0.5] # 'D' is heavily weighted (50%)
    
    print("Simulating 1,000,000 weighted die rolls...")
    start = time.perf_counter()
    
    # `rng.choice` operates entirely in C.
    results = rng.choice(faces, size=1_000_000, p=probabilities, replace=True)
    
    end = time.perf_counter()
    
    # Calculate the actual percentages of what was rolled
    unique, counts = np.unique(results, return_counts=True)
    percentages = dict(zip(unique, counts / 1_000_000))
    
    print(f"Simulation took {end - start:.4f} seconds!")
    print("Resulting Distribution (Should closely match [0.1, 0.2, 0.2, 0.5]):")
    for face, perc in percentages.items():
        print(f" {face}: {perc:.4f}")
        
    # 2. IN-PLACE SHUFFLING
    # Shuffling a massive matrix
    matrix = np.arange(20).reshape(5, 4)
    print("\nOriginal Matrix:")
    print(matrix)
    
    # `rng.shuffle` shuffles the FIRST axis (the rows) strictly in-place (no RAM copy).
    rng.shuffle(matrix)
    print("\nMatrix after in-place row shuffle:")
    print(matrix)


def run_all_labs():
    demonstrate_modern_rng()
    demonstrate_distributions()
    demonstrate_bootstrapping()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why did modern NumPy deprecate `np.random.seed()` in favor of `np.random.default_rng()`?
   Answer: `np.random.seed()` modifies a single, global mathematical state shared by the entire Python process. If you set the global seed to `42` to guarantee reproducibility in your ML training script, but one of the third-party libraries you pip-installed internally calls `np.random.rand()` inside a helper function, the third-party library just secretly advanced the global PRNG state, completely destroying the determinism of your script! The modern `default_rng()` instantiates a completely isolated Generator object. You pass this specific object to your functions, guaranteeing perfect state isolation and mathematically flawless reproducibility.

2. What is the fundamental difference between the Normal (Gaussian) and Binomial distributions?
   Answer: The Normal distribution is Continuous. It can generate an infinite spectrum of decimal floats (e.g., a person's height is $70.123$ inches). The Binomial distribution is Discrete. It mathematically simulates binary (True/False) experiments and returns strictly whole integers (e.g., You flipped 10 coins, exactly $6$ landed on Heads. It is physically impossible to get $6.5$ Heads). 

3. How does `np.random.choice` execute 1,000,000 simulated rolls so fast?
   Answer: Vectorization! The standard Python `random.choices()` would require executing a slow, interpreted Python `for` loop 1,000,000 times, performing dynamic type-checking on every loop. NumPy's `rng.choice` bypasses Python entirely. It ships the instruction, the array of faces, and the probability array down to the optimized C backend, which utilizes CPU SIMD instructions and raw C-pointers to blast the random memory allocations instantly, returning the result in milliseconds.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NumPy Probability & Distributions Completed.")
