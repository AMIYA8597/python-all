"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (DP OPTIMIZATIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You write a flawless $O(N \times M)$ Dynamic Programming solution. 
# It passes the test cases... and then throws a "Memory Limit Exceeded" (MLE) crash.
#
# Why? Because $N$ is 100,000 and $M$ is 100,000. Your 2D matrix `dp[N][M]` 
# attempts to allocate 10 Billion integers in RAM. Python crashes instantly.
# 
# You must master Space Optimization. A DP matrix usually only needs to look 
# at the *immediately previous row* to calculate the current row. You don't 
# need to keep all 100,000 rows in memory! You only need 2 rows!
#
# Second, what if you are solving the Traveling Salesperson Problem (TSP)? 
# Finding the shortest path visiting all 20 cities. The state involves keeping 
# track of exactly *which* cities have been visited. You cannot use an Array 
# or a Set as a DP State (they are slow and unhashable). You must use Bitmask DP.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Space Optimization (Rolling Arrays) to reduce $O(N \times M)$ to $O(M)$ memory.
# - Master Bitmask DP (using integers as boolean states).
# - Utilize Python's `@cache` for effortless Top-Down Memoization.
#
# ==============================================================================
"""

import sys
from functools import cache

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SPACE OPTIMIZATION (ROLLING ARRAYS)
# ==============================================================================
def lcs_space_optimized(text1: str, text2: str) -> int:
    """
    Finds the Longest Common Subsequence using only O(M) memory!
    Time Complexity: O(N * M)
    Space Complexity: O(M) (instead of O(N * M)!)
    """
    n, m = len(text1), len(text2)
    
    # We only need TWO rows in memory at any time: 
    # The 'previous' row we just calculated, and the 'current' row we are building.
    prev_row = [0] * (m + 1)
    curr_row = [0] * (m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i - 1] == text2[j - 1]:
                # Look back at the previous row's diagonal!
                curr_row[j] = 1 + prev_row[j - 1]
            else:
                # Look at previous row (above), or current row (left)
                curr_row[j] = max(prev_row[j], curr_row[j - 1])
                
        # The current row is completely finished!
        # It now becomes the "previous" row for the next iteration!
        # We use slice assignment to copy the values efficiently.
        prev_row[:] = curr_row
        
    return prev_row[m]

def demonstrate_space_optimization():
    section_header("Space Optimization (Rolling Arrays)")
    
    s1 = "abcde" * 1000 # Massive strings
    s2 = "ace" * 1000
    
    print("If we used a full 2D Matrix for this string, it would allocate")
    print("5000 x 3000 = 15,000,000 integers in memory.")
    
    ans = lcs_space_optimized(s1, s2)
    print(f"\nLongest Common Subsequence Length: {ans}")
    print("By using Rolling Arrays, we only allocated 6000 integers total!")
    print("Memory Limit Exceeded (MLE) permanently avoided.")


# ==============================================================================
# 4. BITMASK DP & TOP-DOWN MEMOIZATION
# ==============================================================================
def solve_tsp(n: int, dist: list[list[int]]) -> int:
    """
    Solves the Traveling Salesperson Problem (TSP).
    Finds the shortest path starting at city 0, visiting all cities, and 
    returning to city 0.
    
    Time Complexity: O(N^2 * 2^N)
    Space Complexity: O(N * 2^N)
    """
    # The ultimate goal state: All N bits are set to 1!
    # If N = 4, VISITED_ALL = 1111 (in binary), which is (1 << 4) - 1 = 15.
    VISITED_ALL = (1 << n) - 1
    
    # `@cache` automatically creates a Hash Map in memory!
    # The keys will be a tuple: (mask, pos).
    # If we ever call the function with the exact same (mask, pos) again, 
    # it intercepts the call and instantly returns the cached answer in O(1) time!
    @cache
    def tsp(mask: int, pos: int) -> int:
        # Base Case: If all cities are visited, return the cost to go back to 0.
        if mask == VISITED_ALL:
            return dist[pos][0]
            
        min_cost = float('inf')
        
        # Try traveling to every other city...
        for city in range(n):
            # BITWISE CHECK: Have we visited this city already?
            # E.g., mask = 1010, city = 2 (which is 0100).
            # 1010 & 0100 == 0. The city is unvisited!
            if (mask & (1 << city)) == 0:
                
                # BITWISE UPDATE: Mark the city as visited using OR!
                # E.g., 1010 | 0100 = 1110.
                new_mask = mask | (1 << city)
                
                # Recursively calculate the cost of the rest of the journey
                new_cost = dist[pos][city] + tsp(new_mask, city)
                
                min_cost = min(min_cost, new_cost)
                
        return min_cost

    # Start at city 0. The mask is 0001 (only city 0 is visited).
    return tsp(1, 0)

def demonstrate_bitmask_dp():
    section_header("Bitmask DP (Traveling Salesperson)")
    
    # 4 Cities (0, 1, 2, 3)
    # dist[i][j] is the cost to travel from city i to city j
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    print("Distance Matrix:")
    for row in dist: print(row)
    
    ans = solve_tsp(4, dist)
    
    print(f"\nMinimum cost to visit all cities and return home: {ans}")
    print("Because we used a single Integer as the boolean state, the `@cache` ")
    print("hashed the states blazingly fast in O(1) time!")


def run_all_labs():
    demonstrate_space_optimization()
    demonstrate_bitmask_dp()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When rolling arrays to optimize Space Complexity from $O(N \times M)$ down to $O(M)$, how do you mathematically prove that it is safe to throw away the older rows?
   Answer: You look strictly at the State Transition Equation. For LCS, the equation is `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])` or `1 + dp[i - 1][j - 1]`. The mathematical variable `i` represents the Row. In all three scenarios, the equation only ever looks at row `i` (the current row) or row `i - 1` (the immediately previous row). It never looks at row `i - 2` or `i - 3`. Because the mathematical dependency strictly reaches backward by a maximum depth of 1, any row older than `i - 1` is mathematically obsolete and can be safely purged from RAM, dropping the memory requirement from 10 Billion to just 2.

2. In Python, what does `@cache` (or `@lru_cache(None)`) physically do under the hood when attached to a recursive function?
   Answer: It converts standard recursion into Top-Down Dynamic Programming (Memoization). Under the hood, Python creates a global dictionary hidden in the function's memory space. When you call `tsp(mask=5, pos=2)`, the decorator intercepts the call. It checks if the tuple `(5, 2)` exists in the dictionary. If it does not, it executes the mathematical logic, calculates the final answer (e.g., 150), and invisibly stores `{(5, 2): 150}` in the dictionary. If the recursive tree ever branches and attempts to call `tsp(5, 2)` again, the decorator intercepts it, completely bypasses the function execution, and instantly returns `150` in $O(1)$ time, transforming an $O(N!)$ catastrophic search into a lightning-fast $O(N^2 \times 2^N)$ algorithm.

3. Why use Bitmasks (integers) to represent visited cities instead of a Python `set` or a `list` of booleans?
   Answer: Hashability, Speed, and Memory. A Python `set` or `list` is a mutable object. You cannot use mutable objects as Dictionary Keys, meaning the `@cache` decorator will instantly crash with a `TypeError: unhashable type: 'set'`. You could cast it to a `frozenset` or `tuple`, but those allocate heavy Python objects in memory, triggering excessive Garbage Collection overhead. An Integer is an immutable C-level primitive. Modifying it takes 1 CPU cycle (`mask | (1 << city)`), and hashing an integer takes $O(1)$ time with zero overhead. A 32-bit integer acts as an ultra-fast boolean array of size 32 that fits entirely inside the L1 CPU cache.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: DP Optimizations Completed.")
