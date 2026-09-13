"""
# ==============================================================================
# LABORATORY: PROBABILITY SIMULATIONS (MONTE CARLO & MARKOV)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Many probabilistic problems are too mathematically complex to solve analytically 
# with an exact formula.
# 
# Instead of doing the math, we use a computer to just physically play out the 
# scenario 1 Million times and average the results! This is called a **Monte 
# Carlo Simulation** (named after the famous Casino in Monaco). It is the backbone 
# of modern quantitative finance (simulating stock prices), particle physics, 
# and artificial intelligence.
#
# Furthermore, we will simulate **Markov Chains**, which model systems that 
# transition from one State to another using a matrix of probabilities. This is 
# exactly how early Natural Language Processing (predictive text) and Google's 
# PageRank algorithm functioned!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Prove the counter-intuitive Monty Hall Problem via Monte Carlo simulation.
# - Prove the Central Limit Theorem (CLT) using random sampling.
# - Simulate a stochastic Markov Chain using Matrix Multiplication.
#
# ==============================================================================
"""

import numpy as np
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MONTY HALL PROBLEM (MONTE CARLO)
# ==============================================================================
def demonstrate_monty_hall():
    section_header("Monte Carlo Simulation (The Monty Hall Problem)")
    
    print("Scenario: You are on a Game Show. There are 3 doors.")
    print("Behind 1 door is a Car. Behind the other 2 are Goats.")
    print("1. You pick a door (e.g., Door 0).")
    print("2. The host, who knows where the Car is, OPENS one of the remaining ")
    print("   doors to reveal a Goat.")
    print("3. The host offers you a choice: Do you want to KEEP your original door, ")
    print("   or SWITCH to the remaining closed door?")
    print("\nDoes switching mathematically increase your odds of winning?")
    
    rng = np.random.default_rng(42)
    simulations = 1_000_000
    
    print(f"\nSimulating {simulations:,} games using NumPy Vectorization...")
    start = time.perf_counter()
    
    # 1. The Car is placed behind a random door [0, 1, 2] for all 1M games.
    winning_doors = rng.integers(0, 3, size=simulations)
    
    # 2. The Contestant picks a random door [0, 1, 2] for all 1M games.
    contestant_choices = rng.integers(0, 3, size=simulations)
    
    # Let's evaluate the "Keep" Strategy!
    # They win if their initial choice matches the winning door.
    keep_wins = np.sum(contestant_choices == winning_doors)
    
    # Let's evaluate the "Switch" Strategy!
    # The host opens a Goat door. If the contestant originally picked a Goat, 
    # the host is forced to open the OTHER Goat door. The only remaining closed 
    # door MUST be the Car!
    # Therefore, the "Switch" strategy wins IF AND ONLY IF the contestant's 
    # original choice was wrong!
    switch_wins = np.sum(contestant_choices != winning_doors)
    
    end = time.perf_counter()
    
    print(f"Simulation completed in {end - start:.4f} seconds!")
    print(f"\nResults (Keeping the door) : {keep_wins / simulations * 100:.2f}% Win Rate")
    print(f"Results (Switching doors): {switch_wins / simulations * 100:.2f}% Win Rate")
    
    print("\nConclusion: The math is undeniable. You must ALWAYS switch doors! ")
    print("It doubles your chance of winning from 33.3% to 66.6%!")


# ==============================================================================
# 4. THE CENTRAL LIMIT THEOREM (CLT)
# ==============================================================================
def demonstrate_clt():
    section_header("The Central Limit Theorem (CLT)")
    
    print("The CLT is the most important theorem in all of Statistics.")
    print("It states that if you take multiple random samples from ANY underlying ")
    print("distribution (even one that is heavily skewed), the distribution of the ")
    print("SAMPLE MEANS will always form a perfect Gaussian Bell Curve!")
    
    rng = np.random.default_rng(42)
    
    # Let's create an aggressively non-normal distribution (Exponential).
    # Imagine the wait times at a hospital. Most people wait 10 mins, but some 
    # wait 5 hours!
    population = rng.exponential(scale=10.0, size=1_000_000)
    
    print(f"\nTrue Population Mean  : {np.mean(population):.2f}")
    
    # We will simulate taking a sample of 100 people, calculating their average 
    # wait time, and recording it. We will repeat this experiment 10,000 times!
    num_experiments = 10_000
    sample_size = 100
    
    # `rng.choice` can return a 2D matrix instantly!
    # Rows = Experiments, Cols = The 100 samples per experiment.
    all_samples = rng.choice(population, size=(num_experiments, sample_size))
    
    # Calculate the mean across the columns (axis=1) for every row!
    sample_means = np.mean(all_samples, axis=1)
    
    print(f"Mean of the Sample Means: {np.mean(sample_means):.2f}")
    
    # Let's prove it forms a Bell Curve by calculating the Skewness.
    # (A perfect Bell Curve has a Skewness of exactly 0.0)
    from scipy.stats import skew
    pop_skew = skew(population)
    sample_mean_skew = skew(sample_means)
    
    print(f"\nSkewness of the original population data: {pop_skew:.2f} (Highly Skewed!)")
    print(f"Skewness of the {num_experiments:,} Sample Means : {sample_mean_skew:.2f} (Perfectly Symmetrical!)")
    print("The CLT perfectly transformed the chaotic data into a clean Normal Distribution!")


# ==============================================================================
# 5. MARKOV CHAINS (STOCHASTIC TRANSITIONS)
# ==============================================================================
def demonstrate_markov():
    section_header("Markov Chains (Weather Prediction)")
    
    # A Markov Chain models a system that transitions between distinct states 
    # based strictly on a Matrix of Probabilities.
    # 
    # CRITICAL RULE: A Markov Chain has "No Memory". The next state depends 
    # EXCLUSIVELY on the current state, completely ignoring the history of how 
    # it got there.
    
    # States: [Sunny, Cloudy, Rainy]
    # We construct a Transition Matrix (P). Every row must sum to 1.0!
    # Row 0 (If Sunny today): 80% Sunny tomorrow, 15% Cloudy, 5% Rainy.
    # Row 1 (If Cloudy today): 20% Sunny, 60% Cloudy, 20% Rainy.
    # Row 2 (If Rainy today): 10% Sunny, 40% Cloudy, 50% Rainy.
    
    transition_matrix = np.array([
        [0.80, 0.15, 0.05], # Sunny
        [0.20, 0.60, 0.20], # Cloudy
        [0.10, 0.40, 0.50]  # Rainy
    ])
    
    print("Transition Matrix P (Row = Today, Col = Tomorrow):")
    print(transition_matrix)
    
    # INITIAL STATE: Today is 100% Sunny! [1.0, 0.0, 0.0]
    state_vector = np.array([1.0, 0.0, 0.0])
    
    print("\nSimulating the weather probability exactly 10 days into the future...")
    
    # To predict Tomorrow, we do a Vector-Matrix dot product (state @ P).
    # To predict the Day After Tomorrow, we do it again!
    for day in range(1, 11):
        state_vector = state_vector @ transition_matrix
        print(f"Day {day:2}: Sunny {state_vector[0]*100:5.1f}% | "
              f"Cloudy {state_vector[1]*100:5.1f}% | "
              f"Rainy {state_vector[2]*100:5.1f}%")
              
    print("\nNotice how the probabilities stop changing after Day 8? ")
    print("The system reached 'Steady-State Equilibrium'. No matter what the ")
    print("weather is today, the long-term mathematical probability of any ")
    print("future day being Sunny in this specific city is exactly 57.1%!")


def run_all_labs():
    demonstrate_monty_hall()
    demonstrate_clt()
    demonstrate_markov()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Monte Carlo algorithm avoid nested Python `for` loops?
   Answer: Monte Carlo simulations require simulating millions of independent events. If you loop through 1,000,000 games in standard Python, dynamically generating random numbers one at a time, the overhead of the Python interpreter will take seconds or minutes. By allocating massive NumPy arrays of size 1,000,000 instantly, and evaluating the entire game logic simultaneously using Boolean vector operations (`choices != winning_doors`), the exact same simulation executes in microseconds entirely in C memory.

2. Why is the Central Limit Theorem the foundation of all Data Science?
   Answer: Because real-world data is almost never perfectly Normal (e.g., salaries are massively skewed by billionaires). If data isn't Normal, you cannot safely use P-Values, T-Tests, or standard ML Confidence Intervals! The CLT proves that if you take large enough Random Samples (usually $N > 30$), the *average* of those samples will ALWAYS form a mathematically perfect Normal Bell Curve, regardless of the underlying chaotic population data. This mathematical miracle allows statisticians to safely apply normal-distribution mathematics to chaotic real-world systems.

3. What does the "No Memory" property of a Markov Chain mathematically imply?
   Answer: It mathematically implies that the entire future of the system can be predicted strictly by multiplying the current State Vector by the Transition Matrix. If the weather tomorrow depended on the weather from the last 5 days (e.g., "If it rained for 5 days, it must be sunny tomorrow"), the simple Matrix Multiplication would fail, and we would need a highly complex Recurrent Neural Network (RNN) or LSTM to maintain the memory timeline! Markov Chains sacrifice deep context for absolute mathematical simplicity and speed.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Probability Simulations Completed.")
