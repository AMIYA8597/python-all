"""
Module: 05-prob-simulations
Description: A textbook-grade interactive lesson on Probability Simulations in Python.

===========================================================================
PROBABILITY SIMULATIONS: MATHEMATICAL BACKGROUND & BIG-O ANALYSIS
===========================================================================

1. Introduction to Probability Simulations
------------------------------------------
Simulation is a powerful technique to estimate probabilities and expected values 
by performing repeated random sampling. In Data Science and Statistics, this is 
frequently accomplished using the Monte Carlo method.

The core idea is based on the Frequentist interpretation of probability:
    P(Event) = limit (as N -> infinity) of (Number of times Event occurs / N)

When analytical solutions are too complex or impossible to derive, simulations 
provide empirical approximations. 

2. Law of Large Numbers (LLN)
-----------------------------
The LLN states that as the number of identically distributed, randomly generated 
variables increases, their sample mean (average) approaches their theoretical mean.
    X̄_n = (1/n) * sum(X_i from 1 to n) -> μ as n -> ∞

3. Monte Carlo Integration & Estimation
---------------------------------------
Monte Carlo simulation relies on random sampling to compute numerical results. 
For example, estimating Pi (π):
- Consider a circle of radius R inscribed in a square of side 2R.
- Area of Circle = π * R^2
- Area of Square = (2R)^2 = 4 * R^2
- Ratio of Areas = π / 4
If we drop points uniformly at random in the square, the probability of a point 
landing inside the circle is π / 4. 
Hence, π ≈ 4 * (Points in Circle / Total Points).

4. Complexity Analysis (Big-O)
------------------------------
Time Complexity: 
- Most Monte Carlo simulations scale linearly with the number of trials (N). 
- Thus, the time complexity is generally O(N), where N is the number of simulations.
- Generating a random number typically takes O(1) time.

Space Complexity:
- O(1) if we compute running totals or averages incrementally (streaming).
- O(N) if we store all simulated outcomes for later analysis or plotting.

5. Real-World Applications
--------------------------
- Finance: Options pricing (e.g., simulating asset paths), risk assessment (Value at Risk).
- Physics: Simulating particle movements (Brownian motion), quantum systems.
- Operations Research: Queuing theory, supply chain stress-testing.
- Games of Chance: Designing casino games, evaluating strategies (e.g., Blackjack, Poker).
- Biology: Population genetics, epidemiology (SIR models).

===========================================================================
LEARNING OBJECTIVES
===========================================================================
1. Master random number generation and sampling in Python using both standard 
   library and vectorization tools like NumPy.
2. Build custom Monte Carlo simulations for classical mathematical problems 
   (e.g., estimating Pi).
3. Simulate and solve counter-intuitive probability puzzles (e.g., Monty Hall).
4. Implement Random Walks to model stochastic processes.
5. Apply simulations to real-world scenarios such as financial options pricing.
6. Compare performance between plain Python loops and vectorized NumPy operations.
"""

import sys
import time
import math
import random
import statistics
from typing import List, Tuple, Dict, Any, Callable, Optional

# Attempt to import NumPy for vectorized simulations, handling the case where it's missing
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("WARNING: NumPy is not installed. Vectorized simulations will be skipped or simulated via plain Python.", file=sys.stderr)


# =========================================================================
# SECTION 1: CORE SIMULATION PRIMITIVES
# =========================================================================

class SimulationCore:
    """
    A utility class demonstrating various ways to simulate core probabilistic 
    events, from simple coin flips to complex die rolls.
    """
    
    @staticmethod
    def simulate_coin_flips(n_flips: int, p_heads: float = 0.5) -> List[str]:
        """
        Simulates 'n_flips' of a coin with probability 'p_heads' of getting Heads.
        
        Mathematical Context:
        - This represents 'n' independent Bernoulli trials.
        - The total number of heads follows a Binomial Distribution: B(n, p)
        
        Args:
            n_flips (int): Number of coin flips.
            p_heads (float): Probability of getting Heads (0 <= p <= 1).
            
        Returns:
            List[str]: A list of 'H' and 'T' outcomes.
            
        Time Complexity: O(n)
        Space Complexity: O(n) to store the results.
        """
        if not (0.0 <= p_heads <= 1.0):
            raise ValueError("Probability of heads must be between 0.0 and 1.0")
        
        results = []
        for _ in range(n_flips):
            # random.random() returns a uniform float in [0.0, 1.0)
            if random.random() < p_heads:
                results.append('H')
            else:
                results.append('T')
        return results

    @staticmethod
    def simulate_dice_rolls(n_rolls: int, sides: int = 6) -> List[int]:
        """
        Simulates rolling a fair die with a given number of sides.
        
        Mathematical Context:
        - Discrete Uniform Distribution over {1, 2, ..., sides}.
        - Expected Value: (sides + 1) / 2
        
        Args:
            n_rolls (int): Number of dice rolls.
            sides (int): Number of sides on the die.
            
        Returns:
            List[int]: Results of the rolls.
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if sides < 2:
            raise ValueError("A die must have at least 2 sides.")
            
        # random.randint(a, b) includes both a and b.
        return [random.randint(1, sides) for _ in range(n_rolls)]

    @staticmethod
    def empirical_distribution(data: List[Any]) -> Dict[Any, float]:
        """
        Calculates the empirical probability distribution from raw data.
        
        Args:
            data (List[Any]): List of experimental outcomes.
            
        Returns:
            Dict[Any, float]: Mapping of unique outcomes to their empirical probabilities.
            
        Time Complexity: O(n)
        Space Complexity: O(k) where k is the number of unique outcomes.
        """
        n_total = len(data)
        if n_total == 0:
            return {}
            
        counts = {}
        for item in data:
            counts[item] = counts.get(item, 0) + 1
            
        return {k: v / n_total for k, v in counts.items()}


# =========================================================================
# SECTION 2: MONTE CARLO METHODS
# =========================================================================

class MonteCarloPi:
    """
    Demonstrates the estimation of Pi using the Monte Carlo method.
    """
    
    @staticmethod
    def estimate_pi_standard(n_samples: int) -> float:
        """
        Estimates Pi by throwing darts randomly at a 2x2 square centered at the origin.
        
        Mathematical Theory:
        - The circle inscribed in the square has radius R=1.
        - Area_circle = pi * r^2 = pi
        - Area_square = 2 * 2 = 4
        - P(dart in circle) = Area_circle / Area_square = pi / 4
        
        Args:
            n_samples (int): Total number of random samples (darts).
            
        Returns:
            float: Estimated value of Pi.
            
        Time Complexity: O(N)
        Space Complexity: O(1) - calculating incrementally.
        """
        points_inside_circle = 0
        
        for _ in range(n_samples):
            # Generate random x and y in the range [-1.0, 1.0)
            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            
            # Check if point is inside the unit circle: x^2 + y^2 <= r^2
            # Since r = 1, r^2 = 1.
            if x*x + y*y <= 1.0:
                points_inside_circle += 1
                
        # pi/4 ≈ points_inside_circle / n_samples
        return 4.0 * points_inside_circle / n_samples

    @staticmethod
    def estimate_pi_vectorized(n_samples: int) -> float:
        """
        Estimates Pi using NumPy vectorization for massive performance gains.
        
        Args:
            n_samples (int): Total number of random samples.
            
        Returns:
            float: Estimated value of Pi.
            
        Time Complexity: O(N) but vastly smaller constant factor.
        Space Complexity: O(N) to store arrays in memory, or O(1) if batched.
        """
        if not NUMPY_AVAILABLE:
            print("NumPy not available, falling back to standard estimation.", file=sys.stderr)
            return MonteCarloPi.estimate_pi_standard(n_samples)
            
        # Generate N samples for X and Y simultaneously in range [-1, 1]
        # np.random.uniform creates contiguous memory blocks optimized in C.
        x_array = np.random.uniform(-1.0, 1.0, n_samples)
        y_array = np.random.uniform(-1.0, 1.0, n_samples)
        
        # Element-wise squaring and summation
        # (x_array**2 + y_array**2) <= 1 yields a boolean array.
        # np.sum counts the 'True' values.
        inside_circle_count = np.sum((x_array**2 + y_array**2) <= 1.0)
        
        return 4.0 * inside_circle_count / n_samples


# =========================================================================
# SECTION 3: CLASSIC PROBABILITY PUZZLES
# =========================================================================

class ProbabilityPuzzles:
    """
    Simulation can resolve counter-intuitive probability problems 
    by empirically proving the mathematical reality.
    """
    
    @staticmethod
    def simulate_monty_hall(n_trials: int, switch_door: bool) -> float:
        """
        Simulates the famous Monty Hall problem.
        
        Problem Statement:
        - 3 doors: 1 has a Car (Win), 2 have Goats (Lose).
        - You pick a door.
        - The host (Monty), who knows what's behind the doors, opens another door 
          revealing a goat.
        - You are given the choice to keep your original door or switch to the 
          remaining closed door.
        
        Is it to your advantage to switch?
        - Intuition often says 50/50.
        - Mathematics dictates that keeping wins 1/3 of the time, switching wins 2/3.
        
        Args:
            n_trials (int): Number of games to play.
            switch_door (bool): True if the player's strategy is to switch doors.
            
        Returns:
            float: Win rate (probability of winning a car).
            
        Time Complexity: O(N)
        Space Complexity: O(1)
        """
        wins = 0
        
        for _ in range(n_trials):
            # Doors are 0, 1, 2
            doors = [0, 1, 2]
            
            # Place the car behind a random door
            car_door = random.choice(doors)
            
            # Player makes an initial random choice
            player_choice = random.choice(doors)
            
            # Monty opens a door that is NEITHER the player's choice NOR the car.
            # Find all doors Monty is allowed to open:
            possible_monty_doors = [d for d in doors if d != player_choice and d != car_door]
            
            # Monty picks one of the allowed doors
            monty_door = random.choice(possible_monty_doors)
            
            if switch_door:
                # The player switches to the only remaining closed door
                # It must be the one that is not player_choice and not monty_door
                remaining_doors = [d for d in doors if d != player_choice and d != monty_door]
                player_choice = remaining_doors[0]
                
            if player_choice == car_door:
                wins += 1
                
        return wins / n_trials

    @staticmethod
    def birthday_paradox(group_size: int, n_trials: int = 10000) -> float:
        """
        Simulates the Birthday Paradox to find the probability that at least 
        two people in a room share a birthday.
        
        Mathematical Context:
        P(match) = 1 - P(no match)
        P(no match) = (365/365) * (364/365) * ... * ((365-n+1)/365)
        
        For n=23, P(match) > 50%.
        
        Args:
            group_size (int): Number of people in the room.
            n_trials (int): Number of simulations to run.
            
        Returns:
            float: Empirical probability of a shared birthday.
            
        Time Complexity: O(trials * group_size)
        Space Complexity: O(group_size) to store birthdays (set).
        """
        matches = 0
        
        for _ in range(n_trials):
            # Assume 365 days in a year (ignore leap years for simplicity)
            # We generate a list of random birthdays for the group.
            birthdays = [random.randint(1, 365) for _ in range(group_size)]
            
            # If the set of birthdays is smaller than the list, there's a duplicate
            if len(set(birthdays)) < group_size:
                matches += 1
                
        return matches / n_trials


# =========================================================================
# SECTION 4: STOCHASTIC PROCESSES & RANDOM WALKS
# =========================================================================

class RandomWalks:
    """
    Random walks model stochastic (random) processes over discrete time steps.
    Used heavily in Physics (Brownian motion), Finance (stock prices), and 
    Computer Science (randomized algorithms).
    """
    
    @staticmethod
    def one_dimensional_walk(n_steps: int) -> List[int]:
        """
        Simulates a simple 1D random walk.
        Start at 0. At each step, move +1 or -1 with equal probability.
        
        Mathematical Properties:
        - Expected final position: 0 (since E(step) = 0).
        - Expected distance from origin (RMS): sqrt(n_steps).
        
        Args:
            n_steps (int): Total number of steps.
            
        Returns:
            List[int]: The complete trajectory of positions.
            
        Time Complexity: O(N)
        Space Complexity: O(N) for trajectory.
        """
        position = 0
        trajectory = [position]
        
        for _ in range(n_steps):
            step = 1 if random.random() >= 0.5 else -1
            position += step
            trajectory.append(position)
            
        return trajectory

    @staticmethod
    def two_dimensional_walk(n_steps: int) -> Tuple[List[int], List[int]]:
        """
        Simulates a 2D random walk on an integer grid.
        Moves are (0,1), (0,-1), (1,0), or (-1,0).
        
        Args:
            n_steps (int): Total number of steps.
            
        Returns:
            Tuple[List[int], List[int]]: X coordinates, Y coordinates.
        """
        x, y = 0, 0
        x_path, y_path = [x], [y]
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for _ in range(n_steps):
            dx, dy = random.choice(directions)
            x += dx
            y += dy
            x_path.append(x)
            y_path.append(y)
            
        return x_path, y_path


# =========================================================================
# SECTION 5: REAL-WORLD APPLICATIONS (FINANCE)
# =========================================================================

class FinancialSimulations:
    """
    Applies probability simulations to model complex real-world financial 
    instruments and scenarios.
    """
    
    @staticmethod
    def simulate_asset_price_paths(S0: float, mu: float, sigma: float, 
                                   T: float, steps: int, n_paths: int) -> List[List[float]]:
        """
        Simulates geometric Brownian motion (GBM) to model stock price paths.
        
        Model: dS = mu * S * dt + sigma * S * dW
        Euler-Maruyama Discretization:
        S_{t+1} = S_t * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
        where Z ~ N(0, 1) Standard Normal.
        
        Args:
            S0 (float): Initial stock price.
            mu (float): Expected annualized return (drift).
            sigma (float): Annualized volatility.
            T (float): Time horizon in years (e.g., 1.0 = 1 year).
            steps (int): Number of time steps (e.g., 252 trading days).
            n_paths (int): Number of independent price paths to simulate.
            
        Returns:
            List[List[float]]: Collection of simulated paths.
            
        Time Complexity: O(n_paths * steps)
        Space Complexity: O(n_paths * steps)
        """
        dt = T / steps
        paths = []
        
        for _ in range(n_paths):
            current_S = S0
            path = [current_S]
            for _ in range(steps):
                # Generate standard normal random variable
                Z = random.gauss(0, 1)
                
                # Apply the GBM discrete exact solution
                drift = (mu - 0.5 * sigma**2) * dt
                shock = sigma * math.sqrt(dt) * Z
                
                current_S = current_S * math.exp(drift + shock)
                path.append(current_S)
                
            paths.append(path)
            
        return paths

    @staticmethod
    def expected_european_call_payoff(S0: float, K: float, r: float, sigma: float, 
                                      T: float, n_simulations: int = 100000) -> float:
        """
        Uses Monte Carlo simulation to price a European Call Option.
        This provides an approximation to the Black-Scholes analytical formula.
        
        A European Call Option gives the holder the right, but not the obligation,
        to buy the underlying asset at Strike Price K on Expiration Date T.
        Payoff = max(S_T - K, 0).
        
        Args:
            S0 (float): Current underlying asset price.
            K (float): Strike price.
            r (float): Risk-free interest rate.
            sigma (float): Volatility.
            T (float): Time to expiration in years.
            n_simulations (int): Number of simulated terminal prices.
            
        Returns:
            float: Estimated Option Premium (Price).
        """
        payoffs_sum = 0.0
        
        # We only care about the terminal price S_T, not the whole path.
        # S_T = S0 * exp((r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z)
        drift = (r - 0.5 * sigma**2) * T
        volatility = sigma * math.sqrt(T)
        
        for _ in range(n_simulations):
            Z = random.gauss(0, 1)
            S_T = S0 * math.exp(drift + volatility * Z)
            
            # The holder exercises the option if S_T > K
            payoff = max(S_T - K, 0.0)
            payoffs_sum += payoff
            
        # Expected payoff
        expected_payoff = payoffs_sum / n_simulations
        
        # Present value of the expected payoff (discounted continuously at risk-free rate)
        option_price = expected_payoff * math.exp(-r * T)
        return option_price


# =========================================================================
# SECTION 6: PERFORMANCE BENCHMARKING
# =========================================================================

def benchmark_pi_estimation(n_samples: int) -> None:
    """
    Compares standard Python looping vs NumPy Vectorization (if available).
    Demonstrates why Data Scientists rely heavily on optimized libraries.
    """
    print(f"\n--- Benchmarking Pi Estimation (N={n_samples:,}) ---")
    
    # 1. Standard Python Loop
    start_time = time.perf_counter()
    pi_std = MonteCarloPi.estimate_pi_standard(n_samples)
    std_time = time.perf_counter() - start_time
    print(f"Standard Python: {pi_std:.6f} | Time: {std_time:.4f} seconds")
    
    # 2. NumPy Vectorized (if available)
    if NUMPY_AVAILABLE:
        start_time = time.perf_counter()
        pi_vec = MonteCarloPi.estimate_pi_vectorized(n_samples)
        vec_time = time.perf_counter() - start_time
        print(f"NumPy Vectorized: {pi_vec:.6f} | Time: {vec_time:.4f} seconds")
        
        speedup = std_time / vec_time
        print(f"Speedup Factor: {speedup:.2f}x faster using NumPy!")
    else:
        print("NumPy not available to benchmark.")


# =========================================================================
# SECTION 7: TESTING & VALIDATION
# =========================================================================

def run_tests() -> None:
    """
    Test suite enforcing the correctness of our simulations.
    Because simulations are inherently random, we test properties 
    and bounds rather than strict exact values.
    """
    print("--- Running Test Suite ---")
    
    # 1. Coin Flip Validation
    flips = SimulationCore.simulate_coin_flips(10000, p_heads=0.5)
    heads = flips.count('H')
    # According to LLN, should be close to 5000.
    assert 4800 <= heads <= 5200, f"Coin flips skewed heavily: {heads} heads."
    
    # 2. Dice Roll Validation
    rolls = SimulationCore.simulate_dice_rolls(60000, sides=6)
    dist = SimulationCore.empirical_distribution(rolls)
    # Expected empirical prob for a fair 6-sided die is ~1/6 = 0.1666...
    for side, prob in dist.items():
        assert 0.155 <= prob <= 0.175, f"Die roll for {side} out of bounds: {prob}"
        
    # 3. Monty Hall Paradox Test
    win_keep = ProbabilityPuzzles.simulate_monty_hall(10000, switch_door=False)
    win_switch = ProbabilityPuzzles.simulate_monty_hall(10000, switch_door=True)
    # Keeping should be ~0.333, Switching should be ~0.666
    assert 0.31 <= win_keep <= 0.35, f"Keep strategy skewed: {win_keep}"
    assert 0.64 <= win_switch <= 0.69, f"Switch strategy skewed: {win_switch}"
    
    # 4. Birthday Paradox
    bday_prob = ProbabilityPuzzles.birthday_paradox(23, 10000)
    # Famous result: for 23 people, it's roughly 50.7%
    assert 0.49 <= bday_prob <= 0.52, f"Birthday paradox probability off: {bday_prob}"
    
    print("All probabilistic tests passed within acceptable margins of error!\n")


# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("WELCOME TO THE PROBABILITY SIMULATIONS MASTERCLASS")
    print("=" * 65)
    
    # Random seeding for reproducible outputs in a lesson format
    # In practice, for true Monte Carlo, you might omit this or use stronger RNG.
    random.seed(42)
    if NUMPY_AVAILABLE:
        np.random.seed(42)
        
    print("\n[1] Basic Probability Simulations")
    flips = SimulationCore.simulate_coin_flips(10)
    print(f"10 Coin Flips: {flips}")
    rolls = SimulationCore.simulate_dice_rolls(15, sides=20) # D20 die
    print(f"15 Rolls of a D20: {rolls}")
    
    print("\n[2] The Monty Hall Problem (Simulating 10,000 games)")
    keep_win = ProbabilityPuzzles.simulate_monty_hall(10000, False)
    switch_win = ProbabilityPuzzles.simulate_monty_hall(10000, True)
    print(f"Win Rate if you KEEP your initial door  : {keep_win:.4%} (Theoretical: 33.33%)")
    print(f"Win Rate if you SWITCH to the other door: {switch_win:.4%} (Theoretical: 66.67%)")
    
    print("\n[3] The Birthday Paradox")
    n_people = 23
    prob = ProbabilityPuzzles.birthday_paradox(n_people, 10000)
    print(f"Probability of a shared birthday with {n_people} people: {prob:.4%} (Theoretical: ~50.7%)")
    
    print("\n[4] Random Walks (1D Trajectory)")
    walk_1d = RandomWalks.one_dimensional_walk(20)
    print(f"20-step 1D Random Walk Trajectory:\n{walk_1d}")
    
    print("\n[5] Financial Monte Carlo: Pricing a European Call Option")
    # Black-Scholes params: Stock=100, Strike=100, Rate=5%, Vol=20%, Time=1 Year
    call_price = FinancialSimulations.expected_european_call_payoff(
        S0=100.0, K=100.0, r=0.05, sigma=0.20, T=1.0, n_simulations=100000
    )
    print(f"Estimated Option Price (Premium) via Monte Carlo: ${call_price:.2f}")
    # Theoretical BS price is roughly $10.45
    
    print("\n[6] Performance Benchmarking")
    benchmark_pi_estimation(n_samples=5_000_000)
    
    print("\n[7] Executing Built-In Test Suite")
    run_tests()
    
    print("=" * 65)
    print("LESSON COMPLETED SUCCESSFULLY. KEEP EXPLORING PROBABILITY!")
    print("=" * 65)
