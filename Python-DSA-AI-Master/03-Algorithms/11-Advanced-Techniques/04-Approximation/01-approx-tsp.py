"""
Module: Approximation Algorithms - Traveling Salesperson Problem (TSP)
======================================================================

Learning Objectives:
1. Understand NP-Hard problems and why approximation is necessary.
2. Implement Nearest Neighbor heuristic for Metric TSP.
3. Evaluate the approximation ratio of heuristics.

Concept Explanation:
TSP asks for the shortest possible route that visits every city exactly once
and returns to the origin. Since it is NP-Hard, we use heuristics like Nearest
Neighbor, which often yields a path within a certain factor of the optimal in 
metric spaces (where triangle inequality holds).

Type Hints & Edge Cases:
- Less than 2 cities.
- Disconnected graphs (not metric).
"""

import math
from typing import List, Tuple

Point = Tuple[float, float]

def distance(p1: Point, p2: Point) -> float:
    """Euclidean distance between two points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Basic Implementation: Nearest Neighbor Heuristic
def tsp_nearest_neighbor(cities: List[Point]) -> Tuple[List[int], float]:
    """
    Returns the order of visited city indices and the total distance.
    Starts at city 0.
    """
    if not cities:
        return [], 0.0
    if len(cities) == 1:
        return [0], 0.0
        
    n = len(cities)
    unvisited = set(range(1, n))
    current_city = 0
    route = [0]
    total_dist = 0.0
    
    while unvisited:
        next_city = min(unvisited, key=lambda city: distance(cities[current_city], cities[city]))
        total_dist += distance(cities[current_city], cities[next_city])
        current_city = next_city
        unvisited.remove(current_city)
        route.append(current_city)
        
    # Return to start
    total_dist += distance(cities[current_city], cities[route[0]])
    route.append(route[0])
    
    return route, total_dist

# Interview Challenge
def challenge_tsp_2opt(route: List[int], cities: List[Point]) -> Tuple[List[int], float]:
    """
    Challenge: Implement a single pass of 2-Opt swap to improve the TSP route.
    """
    best_dist = sum(distance(cities[route[i]], cities[route[i+1]]) for i in range(len(route)-1))
    best_route = route[:]
    
    for i in range(1, len(route) - 2):
        for j in range(i + 1, len(route) - 1):
            new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
            new_dist = sum(distance(cities[new_route[k]], cities[new_route[k+1]]) for k in range(len(new_route)-1))
            if new_dist < best_dist:
                best_route = new_route
                best_dist = new_dist
                
    return best_route, best_dist

def test_tsp():
    cities = [(0, 0), (0, 3), (4, 0), (4, 3)]
    route, dist = tsp_nearest_neighbor(cities)
    assert len(route) == 5, "Route must return to start"
    assert route[0] == route[-1], "Route must form a cycle"
    
    improved_route, improved_dist = challenge_tsp_2opt(route, cities)
    assert improved_dist <= dist, "2-opt must not worsen the route"
    
    print("All tests passed.")

if __name__ == "__main__":
    print("Approx TSP Execution\\n" + "-"*30)
    test_tsp()
