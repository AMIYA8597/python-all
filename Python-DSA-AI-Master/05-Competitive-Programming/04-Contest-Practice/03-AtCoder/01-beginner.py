"""
AtCoder Beginner Contest (ABC) Practice

This module covers the core concepts typically tested in AtCoder Beginner Contests.
These contests focus heavily on fundamentals: loops, basic arrays, combinatorics,
greedy algorithms, basic dynamic programming (like the Knapsack problem), and 
graph traversal (DFS/BFS).

Learning Objectives:
1. Develop speed and accuracy in basic algorithmic implementations.
2. Master 1D and 2D Dynamic Programming.
3. Learn to identify Greedy choices and implement graph traversals.

Industry Use Cases:
Basic DP and Greedy algorithms are ubiquitous in software engineering, appearing
in resource allocation, scheduling, parsing, and text formatting. DFS and BFS
are the foundations of web crawlers, dependency resolution, and routing.
"""

from typing import List

def solve_knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Solves the classic 0/1 Knapsack Problem, often featured in AtCoder.
    
    Time Complexity: O(N * W), where N is number of items and W is capacity.
    Space Complexity: O(W) using a 1D DP array.
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        w, v = weights[i], values[i]
        # Traverse backwards to prevent using the same item multiple times
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
            
    return dp[capacity]

def test_knapsack():
    w = [3, 4, 5]
    v = [30, 50, 60]
    c = 8
    assert solve_knapsack(w, v, c) == 90
    
if __name__ == "__main__":
    test_knapsack()
    print("AtCoder Beginner tests passed.")
