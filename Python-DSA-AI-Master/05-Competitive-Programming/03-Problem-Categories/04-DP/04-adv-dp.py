"""
## A. Concept Name
Advanced Dynamic Programming (DP) - Competitive Programming

## B. What is it?
Advanced DP encompasses various specialized techniques built upon standard Dynamic Programming to solve complex combinatorial problems efficiently. These include Bitmask DP, Digit DP, Tree DP, and DP with advanced state spaces.

## C. Why it exists?
While classical DP handles linear or grid-like state spaces well, many problems involve subsets, numbers in large ranges, or hierarchical structures (trees). Advanced DP techniques provide systematic state representations and transitions to solve these problems within polynomial time instead of exponential time.

## D. Industry Use Cases
- Bitmask DP: Route optimization (Traveling Salesperson Problem), job scheduling with constraints, circuit design.
- Digit DP: Database query optimization involving range constraints, statistical counting.
- Tree DP: Network routing protocols, hierarchical data aggregation, organizational resource allocation.

## E. Learning Objectives
1. Understand Bitmask DP for handling subsets as states.
2. Master Digit DP for solving range counting queries efficiently.
3. Learn Tree DP for optimizing values across hierarchical tree structures.

## X. Project Connection
Advanced DP algorithms form the backbone of many optimization problems seen in real-world systems, and are essential for competitive programming and technical interviews. This understanding bridges the gap between theoretical algorithm design and practical, performant software engineering.
"""
from typing import List, Dict, Tuple, Optional
import math
import sys

# Increase recursion depth for deep trees in Tree DP
sys.setrecursionlimit(200000)


# =============================================================================
# 1. Bitmask DP: Traveling Salesperson Problem (TSP)
# =============================================================================
def tsp_shortest_path(graph: List[List[int]]) -> int:
    """
    Finds the shortest Hamiltonian path that visits all nodes and returns to the start.
    Uses Bitmask DP.
    
    Time Complexity: O(n^2 * 2^n), where n is the number of nodes.
    Space Complexity: O(n * 2^n)
    
    Args:
        graph: 2D array representing adjacency matrix of the graph.
               graph[i][j] is the cost to travel from i to j.
               
    Returns:
        Minimum cost to visit all nodes and return to 0.
    """
    n = len(graph)
    if n == 0:
        return 0
    if n == 1:
        return graph[0][0]

    # memo[mask][u] = min cost to visit all nodes in 'mask' ending at 'u'
    memo: Dict[Tuple[int, int], float] = {}

    def dp(mask: int, u: int) -> float:
        # Base case: if all nodes are visited (mask is all 1s), return cost to go back to 0
        if mask == (1 << n) - 1:
            return graph[u][0]

        state = (mask, u)
        if state in memo:
            return memo[state]

        ans = float('inf')
        for v in range(n):
            # If node 'v' is not visited yet in the mask
            if not (mask & (1 << v)):
                new_mask = mask | (1 << v)
                ans = min(ans, graph[u][v] + dp(new_mask, v))

        memo[state] = ans
        return ans

    # Start from node 0, so mask is 1 (binary 0..01), current node is 0
    return int(dp(1, 0))


# =============================================================================
# 2. Digit DP: Count numbers without consecutive 1s in binary
# =============================================================================
def count_no_consecutive_ones(n: int) -> int:
    """
    Counts how many numbers in the range [0, n] do not have consecutive 1s
    in their binary representation.
    
    Time Complexity: O(log N)
    Space Complexity: O(log N)
    
    Args:
        n: The upper limit (inclusive).
        
    Returns:
        Count of valid numbers.
    """
    if n < 0:
        return 0
        
    binary_str = bin(n)[2:]
    length = len(binary_str)
    
    # memo[pos][prev_digit][is_tight]
    memo: Dict[Tuple[int, int, bool], int] = {}
    
    def dp(pos: int, prev_digit: int, is_tight: bool) -> int:
        if pos == length:
            return 1
            
        state = (pos, prev_digit, is_tight)
        if state in memo:
            return memo[state]
            
        limit = int(binary_str[pos]) if is_tight else 1
        ans = 0
        
        for digit in range(limit + 1):
            if prev_digit == 1 and digit == 1:
                continue
            
            new_tight = is_tight and (digit == limit)
            ans += dp(pos + 1, digit, new_tight)
            
        memo[state] = ans
        return ans
        
    return dp(0, 0, True)


# =============================================================================
# 3. Tree DP: Maximum Independent Set
# =============================================================================
def max_independent_set(n: int, edges: List[List[int]]) -> int:
    """
    Finds the size of the Maximum Independent Set in a tree.
    An independent set is a set of nodes where no two nodes are adjacent.
    
    Time Complexity: O(N)
    Space Complexity: O(N)
    
    Args:
        n: Number of nodes.
        edges: List of undirected edges.
        
    Returns:
        Size of the maximum independent set.
    """
    if n == 0:
        return 0
        
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # dp[u][0]: max independent set in subtree u, NOT including u
    # dp[u][1]: max independent set in subtree u, INCLUDING u
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(u: int, p: int) -> None:
        dp[u][1] = 1 # Include u
        dp[u][0] = 0 # Exclude u
        
        for v in adj[u]:
            if v != p:
                dfs(v, u)
                # If we include u, we CANNOT include v
                dp[u][1] += dp[v][0]
                # If we exclude u, we can EITHER include or exclude v (take the max)
                dp[u][0] += max(dp[v][0], dp[v][1])
                
    dfs(0, -1)
    return max(dp[0][0], dp[0][1])


# =============================================================================
# Interview Challenge
# =============================================================================
# Question: Modify the TSP solution to find the path itself, not just the cost.
# Hint: Keep a `parent` array or dictionary mapping `(mask, u)` to the next node `v`
# that resulted in the minimum cost, and trace it back after DP completes.


if __name__ == "__main__":
    print("Testing Advanced DP algorithms...")
    
    # 1. TSP Test
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    assert tsp_shortest_path(graph) == 80
    print("TSP Test: PASS")
    
    # 2. Digit DP Test
    assert count_no_consecutive_ones(5) == 5  # 0, 1, 2, 4, 5
    assert count_no_consecutive_ones(10) == 8 # 0, 1, 2, 4, 5, 8, 9, 10
    print("Digit DP Test: PASS")
    
    # 3. Tree DP Test
    edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]]
    # Tree:
    #       0
    #      / \
    #     1   2
    #    / \   \
    #   3   4   5
    # Max independent set: {3, 4, 5, 0} -> size 4
    assert max_independent_set(6, edges) == 4
    print("Tree DP Test: PASS")
    
    print("All tests passed!")
