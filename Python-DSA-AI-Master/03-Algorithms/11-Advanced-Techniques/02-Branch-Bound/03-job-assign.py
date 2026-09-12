"""
Job Assignment Problem via Branch and Bound

Learning Objectives:
1. Model the Job Assignment problem as a state-space tree.
2. Develop a tight bounding function for pruning sub-optimal assignments.
3. Solve the assignment efficiently compared to naive O(N!) approach.

Concept Explanation:
Given N workers and N jobs, and a cost matrix where matrix[i][j] is the cost of assigning 
worker i to job j, find the minimum cost to assign exactly one job to each worker.
Using Branch and Bound, the state is the subset of assigned jobs. The cost lower bound 
can be estimated by summing the minimum available costs for unassigned workers.
"""

import heapq
from typing import List, Tuple

class Node:
    def __init__(self, cost: int, path: List[int], assigned: int, worker_id: int):
        self.cost = cost
        self.path = path
        self.assigned = assigned
        self.worker_id = worker_id

    def __lt__(self, other):
        return self.cost < other.cost

def calculate_cost_bound(matrix: List[List[int]], current_cost: int, worker_id: int, assigned: int) -> int:
    """Calculate a lower bound on the cost from the current state."""
    n = len(matrix)
    bound = current_cost
    for i in range(worker_id + 1, n):
        min_cost = float('inf')
        for j in range(n):
            if not (assigned & (1 << j)):
                min_cost = min(min_cost, matrix[i][j])
        bound += min_cost
    return bound

def job_assignment_bnb(cost_matrix: List[List[int]]) -> Tuple[int, List[int]]:
    """Solves Job Assignment problem using Branch and Bound."""
    n = len(cost_matrix)
    if n == 0:
        return 0, []

    pq = []
    
    root = Node(cost=0, path=[], assigned=0, worker_id=-1)
    bound = calculate_cost_bound(cost_matrix, 0, -1, 0)
    heapq.heappush(pq, (bound, id(root), root))

    min_cost = float('inf')
    best_path = []

    while pq:
        estimated_bound, _, u = heapq.heappop(pq)

        if estimated_bound >= min_cost:
            continue

        next_worker = u.worker_id + 1
        
        if next_worker == n:
            if u.cost < min_cost:
                min_cost = u.cost
                best_path = u.path
            continue

        for j in range(n):
            if not (u.assigned & (1 << j)):
                new_cost = u.cost + cost_matrix[next_worker][j]
                new_assigned = u.assigned | (1 << j)
                new_path = u.path + [j]
                
                new_bound = calculate_cost_bound(cost_matrix, new_cost, next_worker, new_assigned)
                
                if new_bound < min_cost:
                    v = Node(new_cost, new_path, new_assigned, next_worker)
                    heapq.heappush(pq, (new_bound, id(v), v))

    return min_cost, best_path

# Performance Analysis
def performance_analysis():
    """
    Time Complexity: Worst case O(N!), but B&B reduces it significantly. 
    (Note: Hungarian algorithm solves this in polynomial time O(N^3)).
    Space Complexity: O(N * 2^N) for priority queue in the worst case.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Empty matrix.
    - Large cost variations.
    """
    pass

# Interview Challenge
def challenge_hungarian():
    """Challenge: Implement the Hungarian Algorithm for job assignment in O(N^3)."""
    pass

# Tests
def run_tests():
    matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    
    cost, assignments = job_assignment_bnb(matrix)
    assert cost == 13
    assert assignments == [1, 0, 2, 3]
    
    print("All Job Assignment tests passed!")

if __name__ == "__main__":
    run_tests()
