"""
Hard Optimization Problems - Interview Preparation

Learning Objectives:
1. Formulate optimization problems (e.g., Knapsack, Traveling Salesperson).
2. Implement exact algorithms using Backtracking/DP and approximate ones using Greedy techniques.
3. Understand Branch and Bound concepts.

This module contains algorithms for computationally hard optimization problems.
"""

from typing import List, Tuple
import sys

# 1. 0/1 Knapsack Problem (Dynamic Programming)
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Finds the maximum value that can be put in a knapsack of capacity W.
    Time Complexity: O(N * W) where N is number of items, W is capacity.
    Space Complexity: O(W) with state compression.
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Traverse backwards to use the 1D array effectively for 0/1 Knapsack
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
            
    return dp[capacity]

# 2. Traveling Salesperson Problem (TSP) using Dynamic Programming with Bitmask
def tsp(graph: List[List[int]]) -> int:
    """
    Finds the shortest possible route that visits every city exactly once and returns to the origin.
    Time Complexity: O(N^2 * 2^N)
    Space Complexity: O(N * 2^N)
    """
    n = len(graph)
    # dp[mask][i] - minimum cost to visit a set of cities (represented by mask) ending at city i
    dp = [[sys.maxsize] * n for _ in range(1 << n)]
    
    # Base case: starting at city 0
    dp[1][0] = 0
    
    for mask in range(1, 1 << n):
        for u in range(n):
            # If city u is in the mask
            if mask & (1 << u):
                for v in range(n):
                    # If city v is NOT in the mask and we can go from u to v
                    if not (mask & (1 << v)) and graph[u][v] != 0:
                        dp[mask | (1 << v)][v] = min(dp[mask | (1 << v)][v], dp[mask][u] + graph[u][v])
                        
    # Find minimum cost to return to city 0 from the last visited city
    min_cost = sys.maxsize
    for i in range(1, n):
        if graph[i][0] != 0:
            min_cost = min(min_cost, dp[(1 << n) - 1][i] + graph[i][0])
            
    return min_cost

def test_optimizations():
    print("Testing 0/1 Knapsack:")
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    res = knapsack(weights, values, capacity)
    print(f"Max value: {res}")
    assert res == 220
    
    print("\nTesting TSP:")
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    min_tour = tsp(graph)
    print(f"Minimum cost of tour: {min_tour}")
    assert min_tour == 80

if __name__ == "__main__":
    test_optimizations()
    print("\nAll optimization tests passed!")
