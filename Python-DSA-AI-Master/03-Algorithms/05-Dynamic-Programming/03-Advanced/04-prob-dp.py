"""
Probabilistic Dynamic Programming (DP)

Learning Objectives:
1. Understand how to formulate DP states with probabilities and expected values.
2. Solve problems involving expected number of trials to reach a state.
3. Handle state transitions with stochastic outcomes.

Concept Explanation:
Probabilistic DP applies the principles of dynamic programming to problems involving
probability and expected values. Instead of computing the maximum or minimum cost,
we compute the expected cost or the probability of a certain outcome.

Basic:
- Expected value calculation.
Intermediate:
- Coupon Collector's problem.
Advanced:
- Random walk on a graph or Markov Decision Processes (MDP).

Type Hints:
We use float for probabilities and expected values.

Performance Analysis:
Time Complexity: O(states * transitions)
Space Complexity: O(states)
"""

import math
from typing import List

def basic_expected_value(n: int) -> float:
    """
    Calculate the expected number of coin tosses to get n consecutive heads.
    """
    if n == 0:
        return 0.0
    dp = [0.0] * (n + 1)
    dp[0] = 0.0
    for i in range(1, n + 1):
        dp[i] = 2 * dp[i - 1] + 2
    return dp[n]

def intermediate_coupon_collector(n: int) -> float:
    """
    Calculate the expected number of trials to collect n different coupons.
    E[i] = expected trials to collect remaining (n-i) coupons
    E[i] = 1 + (i/n)*E[i] + ((n-i)/n)*E[i+1]
    E[i] = E[i+1] + n/(n-i)
    """
    if n == 0:
        return 0.0
    expected_trials = 0.0
    for i in range(n):
        expected_trials += n / (n - i)
    return expected_trials

def advanced_random_walk(graph: List[List[float]], start: int, end: int, max_steps: int) -> float:
    """
    Probability of reaching end from start in at most max_steps on a directed graph
    represented by adjacency matrix of transition probabilities.
    """
    n = len(graph)
    dp = [[0.0] * n for _ in range(max_steps + 1)]
    dp[0][start] = 1.0
    
    for step in range(1, max_steps + 1):
        for u in range(n):
            for v in range(n):
                if graph[u][v] > 0:
                    dp[step][v] += dp[step - 1][u] * graph[u][v]
                    
    # Sum probabilities of being at the end state
    return sum(dp[step][end] for step in range(max_steps + 1))

def edge_cases():
    assert basic_expected_value(0) == 0.0
    assert intermediate_coupon_collector(1) == 1.0

def test_functions():
    assert math.isclose(basic_expected_value(1), 2.0)
    assert math.isclose(basic_expected_value(2), 6.0)
    assert math.isclose(intermediate_coupon_collector(2), 3.0)
    print("All tests passed.")

if __name__ == "__main__":
    edge_cases()
    test_functions()
