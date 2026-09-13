"""
# ==============================================================================
# LABORATORY: SIMULATED ANNEALING (METAHEURISTICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Genetic Algorithms borrow concepts from Biology (Evolution) 
# to solve mathematically impossible optimization problems like the TSP.
#
# Simulated Annealing borrows its concepts from Physics and Metallurgy!
# When blacksmiths forge a sword, they heat the metal to extreme temperatures. 
# The atoms vibrate violently, escaping their current microscopic structures. 
# As the blacksmith SLOWLY cools the metal, the atoms settle into a mathematically 
# perfect crystal lattice, making the sword incredibly strong. If cooled too 
# fast (quenching), the metal becomes brittle.
#
# Computer Scientists modeled this exact thermodynamic process!
# 1. Start with a random TSP route.
# 2. Set the "Temperature" (T) extremely high.
# 3. Randomly swap two cities to generate a "Neighbor" route.
# 4. If the Neighbor is BETTER (shorter), ALWAYS accept it.
# 5. If the Neighbor is WORSE, mathematically ACCEPT IT ANYWAY based on a 
#    probability equation: $P = e^{-\Delta E / T}$.
#
# Why on earth would we accept a WORSE answer?!
# To escape Local Minima! 
# At high temperatures, $T$ is huge, so the probability $P$ is close to $100\%$. 
# The algorithm violently jumps around the search space, climbing OUT of craters! 
# As the algorithm runs, we slowly "cool" the Temperature $T$. As $T$ drops, 
# the probability of accepting worse answers drops to $0\%$. The algorithm 
# transforms into a strict greedy search, freezing permanently at the bottom 
# of the deepest valley it found!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model optimization as a thermodynamic state.
# - Implement the Metropolis-Hastings Acceptance Criterion ($e^{-\Delta E / T}$).
# - Tune the Cooling Schedule (Alpha decay rate).
#
# ==============================================================================
"""

import math
import random
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Define a Point Type and Distance Matrix ---
Point = Tuple[float, float]

def get_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
# -------------------------------------------------------


# ==============================================================================
# 3. SIMULATED ANNEALING ENGINE (TSP)
# ==============================================================================
class SimulatedAnnealingTSP:
    def __init__(
        self, 
        cities: List[Point], 
        initial_temp: float = 10000.0, 
        cooling_rate: float = 0.995, 
        min_temp: float = 1.0
    ):
        self.cities = cities
        self.n = len(cities)
        
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        
    def _calculate_route_distance(self, route: List[int]) -> float:
        dist = 0.0
        for i in range(self.n):
            u = route[i]
            v = route[(i + 1) % self.n]
            dist += get_distance(self.cities[u], self.cities[v])
        return dist

    def _get_neighbor(self, route: List[int]) -> List[int]:
        """
        Generates a neighboring state by making a slight alteration.
        For TSP, the standard neighborhood function is the "2-Opt Swap".
        We pick two random indices and reverse the entire subarray between them!
        """
        neighbor = route.copy()
        i, j = random.sample(range(self.n), 2)
        
        if i > j:
            i, j = j, i
            
        # Reverse the path segment! (Uncrosses intersecting lines)
        neighbor[i:j+1] = reversed(neighbor[i:j+1])
        
        return neighbor

    def _acceptance_probability(self, current_energy: float, new_energy: float, temp: float) -> float:
        """
        The Metropolis-Hastings Criterion.
        If the new energy (distance) is lower, probability is 1.0 (100%).
        If the new energy is higher, probability exponentially decays based on 
        how much worse it is, and how cold the current temperature is.
        """
        if new_energy < current_energy:
            return 1.0
            
        # math.exp(-(new - current) / temp)
        return math.exp((current_energy - new_energy) / temp)

    def run(self) -> Tuple[float, List[int]]:
        """
        Executes the thermodynamic simulation.
        """
        # 1. Start with a completely random state
        current_route = list(range(self.n))
        random.shuffle(current_route)
        current_energy = self._calculate_route_distance(current_route)
        
        # Track the absolute best seen across all time (in case it finds a great 
        # answer but randomly jumps out of it before freezing).
        best_route = current_route.copy()
        best_energy = current_energy
        
        iteration = 0
        
        # 2. THE COOLING LOOP
        while self.temp > self.min_temp:
            
            # Generate a neighbor
            neighbor_route = _get_neighbor = self._get_neighbor(current_route)
            neighbor_energy = self._calculate_route_distance(neighbor_route)
            
            # 3. METROPOLIS ACCEPTANCE
            prob = self._acceptance_probability(current_energy, neighbor_energy, self.temp)
            
            # Roll a random number between 0 and 1
            if random.random() < prob:
                current_route = neighbor_route
                current_energy = neighbor_energy
                
                # Check global best
                if current_energy < best_energy:
                    best_energy = current_energy
                    best_route = current_route.copy()
                    
            # 4. COOL THE METAL (Alpha Decay)
            # Example: 10000 * 0.995 = 9950. Next loop: 9950 * 0.995 = 9900.25...
            self.temp *= self.cooling_rate
            iteration += 1
            
        print(f"[Thermodynamics] Metal cooled to freezing over {iteration} iterations.")
        return best_energy, best_route


def demonstrate_annealing():
    section_header("Algorithm: Simulated Annealing (Thermodynamic TSP)")
    
    # 20 random cities on a grid
    random.seed(1337)
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
    
    print(f"Tracking {len(cities)} Amazon Delivery Destinations...")
    print("Heating algorithm forge to 10,000 Degrees...")
    print("Cooling rate: 0.995 per iteration...")
    
    sa = SimulatedAnnealingTSP(cities, initial_temp=10000.0, cooling_rate=0.995, min_temp=1.0)
    best_dist, best_route = sa.run()
    
    print(f"\nMetal Frozen!")
    print(f"Best Annealed Tour Route: {' -> '.join(map(str, best_route))}")
    print(f"Best Annealed Tour Cost : {best_dist:.2f}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Simulated Annealing accept WORSE solutions?
   Answer: To escape Local Minima! Imagine the search space is a mountain range. You are trying to find the absolute lowest valley. A Greedy Algorithm (like Hill Climbing) only ever accepts moves that go down. It will rapidly slide into a crater and get permanently trapped there, completely missing the Mariana Trench one mountain over! By occasionally accepting WORSE moves (climbing UP), Simulated Annealing gives itself the physical momentum to jump out of the shallow crater and continue exploring the mountain range.

2. How does the equation $P = e^{-\Delta E / T}$ perfectly model real-world Physics?
   Answer: In statistical mechanics, this is literally the Boltzmann Distribution equation that defines the probability of a particle transitioning to a higher energy state. 
   - If $T$ is massive (10,000 degrees), $\Delta E / T$ becomes a microscopic fraction. $e^{-0.0001} \approx 0.999$. The probability of accepting the bad move is $99\%$. The atoms are vibrating violently and jumping everywhere.
   - If $T$ drops to near $0$ (freezing), $\Delta E / T$ becomes massive. $e^{-100} \approx 0.0000000001$. The probability of accepting the bad move drops to Absolute Zero. The atoms lock into place. It's a flawless mathematical simulation of physical cooling.

3. Genetic Algorithms vs Simulated Annealing. Which is better?
   Answer: 
   - Genetic Algorithms maintain a massive "Population" (e.g., 100 routes at once). This makes them incredibly thorough at exploring vast, multi-dimensional search spaces, but they require heavy RAM and CPU overhead to evaluate and breed 100 routes every generation.
   - Simulated Annealing only tracks ONE SINGLE ROUTE in memory at all times. It is incredibly lightweight, blindingly fast to execute, and perfect for localized optimization. SA is generally preferred for classical combinatorial problems like TSP or Circuit Board routing.
"""

if __name__ == "__main__":
    demonstrate_annealing()
    print("\n[SUCCESS] Laboratory: Simulated Annealing Completed.")
