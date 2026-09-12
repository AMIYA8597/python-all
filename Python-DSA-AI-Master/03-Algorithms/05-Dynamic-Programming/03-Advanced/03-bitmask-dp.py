"""
Bitmask Dynamic Programming (Bitmask DP)

Concept Explanation:
Bitmask DP is used for problems where the state includes a subset of a small set of items (typically N <= 20).
Instead of using arrays or sets to represent the state (which is slow and memory-intensive to hash), 
we use an integer where each bit represents whether an item is included (1) or excluded (0).
For N items, there are 2^N possible subsets, corresponding to integers from 0 to 2^N - 1.

Common Operations:
- Check if i-th bit is set: `(mask & (1 << i)) > 0`
- Set i-th bit: `mask | (1 << i)`
- Clear i-th bit: `mask & ~(1 << i)`
- Toggle i-th bit: `mask ^ (1 << i)`

Learning Objectives:
1. Understand how to represent subsets as integers using bitwise operations.
2. Solve the Traveling Salesperson Problem (TSP) using Bitmask DP.
3. Solve Job Assignment / Bipartite Matching variants.
4. Analyze the exponential time complexity O(2^N * N^2) and recognize when to use Bitmask DP.

Industry Use Cases:
- Route optimization (delivery vehicles, logistics) for a small number of nodes.
- Task assignment where agents and tasks have affinity matrices.
- Circuit board routing and constraint satisfaction solvers.
"""

from typing import List, Tuple, Dict
import math

def traveling_salesperson(n: int, dist: List[List[int]]) -> int:
    """
    Solves the Traveling Salesperson Problem using Bitmask DP.
    Find the minimum cost to visit all nodes exactly once and return to the starting node (node 0).
    
    :param n: Number of nodes.
    :param dist: 2D array where dist[i][j] is the distance from i to j.
    
    Time Complexity: O(N^2 * 2^N)
    Space Complexity: O(N * 2^N)
    """
    # memo[(mask, u)] = min cost to visit all remaining unvisited nodes (indicated by 0s in mask)
    # starting from node `u` and eventually returning to node 0.
    memo = {}
    
    ALL_VISITED_MASK = (1 << n) - 1

    def dp(mask: int, u: int) -> int:
        # Base case: all nodes visited
        if mask == ALL_VISITED_MASK:
            # Return cost to go back to origin (node 0)
            return dist[u][0]
            
        if (mask, u) in memo:
            return memo[(mask, u)]
            
        ans = float('inf')
        
        # Try visiting all unvisited nodes
        for v in range(n):
            if not (mask & (1 << v)): # v is not visited
                # Visit v
                cost = dist[u][v] + dp(mask | (1 << v), v)
                ans = min(ans, cost)
                
        memo[(mask, u)] = ans
        return ans

    # Start at node 0, with only node 0 visited (mask = 1)
    if n == 0: return 0
    if n == 1: return 0
    return int(dp(1, 0))


def job_assignment(cost: List[List[int]]) -> int:
    """
    Given N workers and N jobs, cost[i][j] is the cost of assigning worker i to job j.
    Assign exactly one job to each worker to minimize total cost.
    
    Time Complexity: O(N * 2^N)
    Space Complexity: O(2^N)
    """
    n = len(cost)
    # dp[mask] = min cost to assign jobs for workers 0 to k-1,
    # where k is the number of set bits in mask, and the set bits indicate which jobs are taken.
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    
    for mask in range(1 << n):
        # Number of set bits in mask tells us which worker we are assigning a job to
        worker_id = bin(mask).count('1') - 1
        
        for job_id in range(n):
            if mask & (1 << job_id): # If this job is assigned in current mask
                prev_mask = mask & ~(1 << job_id)
                dp[mask] = min(dp[mask], dp[prev_mask] + cost[worker_id][job_id])
                
    return int(dp[(1 << n) - 1])


if __name__ == "__main__":
    print("--- Traveling Salesperson Problem ---")
    # 4 cities
    # Distances:
    # 0 -> 1: 10, 0 -> 2: 15, 0 -> 3: 20
    # 1 -> 0: 10, 1 -> 2: 35, 1 -> 3: 25
    # 2 -> 0: 15, 2 -> 1: 35, 2 -> 3: 30
    # 3 -> 0: 20, 3 -> 1: 25, 3 -> 2: 30
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    min_cost = traveling_salesperson(4, dist_matrix)
    print("TSP Minimum Cost:", min_cost)
    # Path: 0 -> 1 -> 3 -> 2 -> 0 = 10 + 25 + 30 + 15 = 80
    assert min_cost == 80
    
    print("\n--- Job Assignment Problem ---")
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    # Optimal:
    # W0 -> J1 (2)
    # W1 -> J0 (6) or W2->J2(1), W3->J3(4), W1->J0(6) => 2+6+1+4 = 13
    assign_cost = job_assignment(cost_matrix)
    print("Minimum Assignment Cost:", assign_cost)
    assert assign_cost == 13
    
    print("\nAll Bitmask DP tests passed!")
