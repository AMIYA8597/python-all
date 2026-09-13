"""
# ==============================================================================
# LABORATORY: GENETIC ALGORITHMS (METAHEURISTICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that you can mathematically approximate TSP within exactly $2\times$ 
# the optimal cost using the MST algorithm. But that ONLY works if the graph 
# perfectly obeys the Triangle Inequality! 
# 
# What if you are trying to optimize the design of an airplane wing? Or the 
# hyperparameters of a Neural Network? There is no "Minimum Spanning Tree" for 
# a 100-dimensional physics problem. The math is completely unsolvable.
#
# The Solution: Metaheuristics (Nature's Algorithms).
# When Computer Scientists encounter an unsolvable optimization problem, they 
# steal algorithms from Mother Nature. The most famous is the Genetic Algorithm (GA).
#
# How Evolution solves unsolvable math:
# 1. INITIALIZATION: Spawn a random "Population" of 100 terrible, random solutions.
# 2. FITNESS: Evaluate how "good" each solution is. (e.g., How short is the route?)
# 3. SELECTION: Let the worst 50% die. The best 50% survive to become parents.
# 4. CROSSOVER: The parents "mate". A child route takes the first half of the 
#    cities from the Mother, and the second half from the Father.
# 5. MUTATION: Randomly swap two cities in the child's DNA. (This prevents the 
#    entire population from getting stuck in a local minimum!).
# 
# By repeating this process for 500 generations, the population organically 
# "evolves" towards an incredibly optimized answer! It cannot mathematically 
# guarantee it is the absolute optimal, but it is routinely used to design 
# antennas for NASA satellites and aerodynamic shapes for Formula 1 cars!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model a solution as a Genetic Chromosome.
# - Implement Tournament Selection and Ordered Crossover (OX1).
# - Understand the necessity of Genetic Mutation to escape Local Minima.
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
# 3. GENETIC ALGORITHM ENGINE (TSP)
# ==============================================================================
class GeneticTSP:
    def __init__(self, cities: List[Point], pop_size: int = 100, mutation_rate: float = 0.05):
        self.cities = cities
        self.n = len(cities)
        
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        
        # The Population is a list of "Chromosomes" (Routes)
        self.population: List[List[int]] = []
        self.fitness: List[float] = []
        
    def _calculate_route_distance(self, route: List[int]) -> float:
        dist = 0.0
        for i in range(self.n):
            u = route[i]
            # Wrap around to the start to complete the tour
            v = route[(i + 1) % self.n]
            dist += get_distance(self.cities[u], self.cities[v])
        return dist

    def _initialize_population(self):
        """Creates Generation 0 with completely random routes."""
        self.population = []
        base_route = list(range(self.n))
        
        for _ in range(self.pop_size):
            shuffled = base_route.copy()
            random.shuffle(shuffled)
            self.population.append(shuffled)
            
    def _evaluate_fitness(self):
        """
        Calculates fitness. We want the SHORTEST route. 
        So Fitness = 1 / Distance. (Higher fitness is better).
        """
        self.fitness = []
        for route in self.population:
            dist = self._calculate_route_distance(route)
            # Add a tiny epsilon to prevent division by zero just in case
            self.fitness.append(1.0 / (dist + 1e-9))

    def _tournament_selection(self, k: int = 5) -> List[int]:
        """
        Picks `k` random individuals from the population, lets them fight, 
        and returns the winner (the one with the highest fitness).
        This models "Survival of the Fittest" while keeping some randomness!
        """
        best_idx = random.randint(0, self.pop_size - 1)
        
        for _ in range(k - 1):
            idx = random.randint(0, self.pop_size - 1)
            if self.fitness[idx] > self.fitness[best_idx]:
                best_idx = idx
                
        return self.population[best_idx]

    def _ordered_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        Mating two TSP routes is incredibly difficult! If you just split them in 
        half, the child might visit City 3 twice, and forget to visit City 5!
        
        Ordered Crossover (OX1) solves this:
        1. Pick a random substring from Parent 1 and drop it exactly into the Child.
        2. Fill the remaining empty slots in the Child with the cities from Parent 2, 
           in the exact order they appear, skipping any cities already in the Child!
        """
        start_idx = random.randint(0, self.n - 1)
        end_idx = random.randint(0, self.n - 1)
        
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
            
        child = [-1] * self.n
        
        # 1. Inherit exact substring from Parent 1
        for i in range(start_idx, end_idx + 1):
            child[i] = parent1[i]
            
        # 2. Fill the rest from Parent 2
        p2_idx = 0
        for i in range(self.n):
            if child[i] == -1:
                # Find the next city in Parent 2 that isn't already in the child
                while parent2[p2_idx] in child:
                    p2_idx += 1
                child[i] = parent2[p2_idx]
                
        return child

    def _mutate(self, route: List[int]):
        """
        Randomly mutates the DNA to maintain genetic diversity in the gene pool.
        For TSP, we randomly swap two cities.
        """
        for i in range(self.n):
            if random.random() < self.mutation_rate:
                j = random.randint(0, self.n - 1)
                route[i], route[j] = route[j], route[i]

    def evolve(self, generations: int) -> Tuple[float, List[int]]:
        """Runs the entire biological evolution simulation."""
        self._initialize_population()
        
        best_overall_distance = float('inf')
        best_overall_route = []
        
        for gen in range(generations):
            self._evaluate_fitness()
            
            # Track the absolute best individual
            for i in range(self.pop_size):
                dist = self._calculate_route_distance(self.population[i])
                if dist < best_overall_distance:
                    best_overall_distance = dist
                    best_overall_route = self.population[i].copy()
                    
            # Create the Next Generation
            new_population = []
            
            # ELITISM: We perfectly clone the absolute best individual to 
            # guarantee our gene pool never degrades!
            new_population.append(best_overall_route.copy())
            
            # Breed the rest of the children
            for _ in range(self.pop_size - 1):
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()
                
                child = self._ordered_crossover(parent1, parent2)
                self._mutate(child)
                new_population.append(child)
                
            # The children become the new adult population!
            self.population = new_population
            
        return best_overall_distance, best_overall_route


def demonstrate_genetic_algo():
    section_header("Algorithm: Genetic Metaheuristic (TSP Evolution)")
    
    # 15 random cities on a grid
    random.seed(42) # For reproducible output
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(15)]
    
    print(f"Tracking {len(cities)} Amazon Delivery Destinations...")
    print("Generating Population: 100")
    print("Executing 500 Generations of biological evolution...")
    
    ga = GeneticTSP(cities, pop_size=100, mutation_rate=0.05)
    best_dist, best_route = ga.evolve(generations=500)
    
    print(f"\nEvolution Completed!")
    print(f"Best Evolved Tour Route: {' -> '.join(map(str, best_route))}")
    print(f"Best Evolved Tour Cost : {best_dist:.2f}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a "Local Minimum" and how does Mutation fix it?
   Answer: Imagine the optimal TSP route is the bottom of the Mariana Trench. The Genetic Algorithm is searching, but gets trapped in a shallow crater (a "Local Minimum"). If the crossover phase only recombines the DNA of parents trapped in the crater, the children will never escape the crater! Mutation introduces completely new, randomized genetic sequences that didn't exist in the parents. This physical "jolt" allows a child to accidentally jump out of the crater and discover the Mariana Trench!

2. Why do we use "Tournament Selection" instead of just picking the top 10%?
   Answer: If you rigidly only allow the absolute best 10% of individuals to mate, you destroy genetic diversity. The entire population becomes inbred clones of the best solution, trapping them immediately in a local minimum! By using Tournament Selection, you randomly pick 5 individuals to fight. The winner gets to mate. This allows a TERRIBLE solution to occasionally win a tournament and mate, injecting its weird (but potentially useful) DNA into the gene pool! It balances Exploitation (finding the best answer) with Exploration (searching new areas).

3. Why is Crossover so difficult for the Traveling Salesperson Problem?
   Answer: In a normal Genetic Algorithm (like tuning Neural Network weights), DNA is just a list of independent numbers: `[0.5, 0.2, 0.9]`. You can safely cut it in half. 
   TSP DNA is a Permutation: `[City1, City2, City3]`. If you cut two routes in half and stitch them together, the child might have `[City1, City2, City1]`. This is an invalid route because City 3 was forgotten and City 1 was visited twice! Algorithms like Ordered Crossover (OX1) or Partially Mapped Crossover (PMX) use highly complex repair logic to guarantee the child remains a perfectly valid permutation of all $N$ cities.
"""

if __name__ == "__main__":
    demonstrate_genetic_algo()
    print("\n[SUCCESS] Laboratory: Genetic Algorithms Completed.")
