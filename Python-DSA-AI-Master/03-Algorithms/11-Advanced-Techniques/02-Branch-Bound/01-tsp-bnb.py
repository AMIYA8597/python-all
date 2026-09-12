"""
Traveling Salesperson Problem (TSP) via Branch and Bound

Learning Objectives:
1. Understand the Branch and Bound paradigm.
2. Apply Branch and Bound to solve NP-Hard problems like TSP exactly.
3. Learn how to calculate lower bounds using a cost matrix reduction.

Concept Explanation:
Branch and Bound (B&B) is an algorithm design paradigm for discrete and combinatorial optimization.
It systematically enumerates candidate solutions by exploring branches of a state space tree. 
It "prunes" branches that cannot yield a better solution than the best one found so far.
For TSP, reducing the adjacency matrix provides a lower bound on the path cost.
"""

import copy
import heapq
from typing import List, Tuple

# Basic Implementation: Setup and Cost Matrix Reduction
def reduce_matrix(matrix: List[List[float]]) -> Tuple[List[List[float]], float]:
    """Reduces the TSP cost matrix and returns the reduction cost (lower bound)."""
    n = len(matrix)
    cost = 0.0
    reduced = copy.deepcopy(matrix)

    # Row reduction
    for i in range(n):
        min_val = min(reduced[i])
        if min_val != float('inf') and min_val > 0:
            cost += min_val
            for j in range(n):
                if reduced[i][j] != float('inf'):
                    reduced[i][j] -= min_val

    # Column reduction
    for j in range(n):
        min_val = min(reduced[i][j] for i in range(n))
        if min_val != float('inf') and min_val > 0:
            cost += min_val
            for i in range(n):
                if reduced[i][j] != float('inf'):
                    reduced[i][j] -= min_val

    return reduced, cost

# Intermediate Implementation: State Space Tree Node
class Node:
    def __init__(self, matrix: List[List[float]], path: List[int], level: int, cost: float, bound: float):
        self.matrix = matrix
        self.path = path
        self.level = level
        self.cost = cost
        self.bound = bound

    def __lt__(self, other):
        return self.bound < other.bound

# Advanced Implementation: Full Branch and Bound TSP Solver
def tsp_branch_and_bound(adj_matrix: List[List[float]]) -> Tuple[float, List[int]]:
    """Solves the TSP using Branch and Bound."""
    n = len(adj_matrix)
    pq = []
    
    reduced_matrix, initial_bound = reduce_matrix(adj_matrix)
    root = Node(reduced_matrix, [0], 1, 0.0, initial_bound)
    heapq.heappush(pq, (root.bound, id(root), root))
    
    min_cost = float('inf')
    best_path = []

    while pq:
        bound, _, current = heapq.heappop(pq)

        if bound >= min_cost:
            continue

        u = current.path[-1]

        if current.level == n:
            tour_cost = current.cost + adj_matrix[u][0]
            if tour_cost < min_cost:
                min_cost = tour_cost
                best_path = current.path + [0]
            continue

        for v in range(n):
            if v not in current.path and current.matrix[u][v] != float('inf'):
                child_matrix = copy.deepcopy(current.matrix)
                
                for k in range(n):
                    child_matrix[u][k] = float('inf')
                    child_matrix[k][v] = float('inf')
                child_matrix[v][0] = float('inf')

                child_reduced, reduction_cost = reduce_matrix(child_matrix)
                new_cost = current.cost + current.matrix[u][v]
                new_bound = current.bound + current.matrix[u][v] + reduction_cost

                if new_bound < min_cost:
                    child_node = Node(child_reduced, current.path + [v], current.level + 1, new_cost, new_bound)
                    heapq.heappush(pq, (child_node.bound, id(child_node), child_node))

    return min_cost, best_path

# Performance Analysis
def performance_analysis():
    """
    Time Complexity: Worst-case O(N!) if no pruning occurs.
    Space Complexity: O(N^2 * N!) worst-case.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Disconnected graph (no path possible).
    - N = 1 or 2.
    """
    pass

# Interview Challenge
def challenge_tsp():
    """Challenge: Implement 1-Tree lower bound using Minimum Spanning Tree."""
    pass

# Tests
def run_tests():
    INF = float('inf')
    matrix = [
        [INF, 10, 15, 20],
        [10, INF, 35, 25],
        [15, 35, INF, 30],
        [20, 25, 30, INF]
    ]
    
    cost, path = tsp_branch_and_bound(matrix)
    assert cost == 80.0
    assert path in ([0, 1, 3, 2, 0], [0, 2, 3, 1, 0])
    
    print("All TSP Branch and Bound tests passed!")

if __name__ == "__main__":
    run_tests()
