"""
# ==============================================================================
# LABORATORY: MO'S ALGORITHM (OFFLINE RANGE QUERIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Segment Trees answer Range Queries in O(log N) time. 
# But what if the query asks: "How many DISTINCT numbers exist between index L and R?"
# 
# Segment Trees fail catastrophically at this. If the Left child says "I have 5 
# distinct numbers" and the Right child says "I have 6 distinct numbers", you CANNOT 
# merge them! (They might share the same numbers, or they might be completely unique. 
# The Segment Tree loses that information).
#
# Mo's Algorithm solves this. It is a powerful "Sliding Window" algorithm used 
# strictly for "Offline Queries" (meaning you have all the queries in a list 
# BEFORE you start processing).
#
# By sorting the queries using a mathematical trick (Square Root Decomposition), 
# Mo's algorithm guarantees that the sliding window pointers only move a maximum 
# of O(N * sqrt(N)) times across all Q queries!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Online and Offline Queries.
# - Understand the Mo's Sorting Trick.
# - Implement a sliding window with `add()` and `remove()` methods.
# - Solve the "Distinct Elements in Range" problem.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MO'S ALGORITHM IMPLEMENTATION
# ==============================================================================
class Query:
    def __init__(self, index: int, L: int, R: int, block_size: int):
        self.index = index
        self.L = L
        self.R = R
        # The crucial step: Group queries by the Block their Left pointer falls into
        self.block_index = L // block_size

def mos_algorithm(arr: List[int], queries_input: List[Tuple[int, int]]) -> List[int]:
    """
    Finds the number of Distinct Elements in multiple ranges [L, R].
    Time Complexity: O((N + Q) * sqrt(N))
    """
    n = len(arr)
    q = len(queries_input)
    block_size = int(math.ceil(math.sqrt(n)))
    
    # 1. Prepare and Sort the Queries (Offline Mode)
    queries = []
    for i, (L, R) in enumerate(queries_input):
        queries.append(Query(i, L, R, block_size))
        
    # SORTING TRICK:
    # 1st Priority: Sort by the Block Index of the Left Pointer.
    # 2nd Priority: Sort by the Right Pointer.
    # This guarantees the Left pointer only moves around slightly within its block,
    # while the Right pointer slowly sweeps forward.
    queries.sort(key=lambda q: (q.block_index, q.R))
    
    # Results array (to store answers in their original input order)
    answers = [0] * q
    
    # Global state for the Sliding Window
    current_L = 0
    current_R = -1
    distinct_count = 0
    
    # A frequency map to track how many times a number appears in our window
    freq = {}
    
    # Helper functions for the Sliding Window
    def add(index: int):
        nonlocal distinct_count
        val = arr[index]
        if val not in freq:
            freq[val] = 0
            
        if freq[val] == 0:
            distinct_count += 1 # A brand new distinct element entered the window!
            
        freq[val] += 1

    def remove(index: int):
        nonlocal distinct_count
        val = arr[index]
        freq[val] -= 1
        
        if freq[val] == 0:
            distinct_count -= 1 # An element completely left the window!

    # 2. Process Queries
    for query in queries:
        L = query.L
        R = query.R
        
        # Expand window on the right
        while current_R < R:
            current_R += 1
            add(current_R)
            
        # Shrink window on the right
        while current_R > R:
            remove(current_R)
            current_R -= 1
            
        # Expand window on the left
        while current_L > L:
            current_L -= 1
            add(current_L)
            
        # Shrink window on the left
        while current_L < L:
            remove(current_L)
            current_L += 1
            
        # The window is now perfectly matching [L, R]! Record the answer.
        answers[query.index] = distinct_count
        
    return answers


def demonstrate_mos_algorithm():
    section_header("Algorithm: Mo's Algorithm (Offline Sliding Window)")
    
    # Indices:    0  1  2  3  4  5  6  7  8
    arr =       [ 1, 1, 2, 1, 3, 4, 5, 2, 8 ]
    
    # List of Offline Queries (L, R)
    queries_input = [
        (0, 4), # [1, 1, 2, 1, 3] -> Distinct: {1, 2, 3} -> 3
        (1, 3), # [1, 2, 1]       -> Distinct: {1, 2}    -> 2
        (2, 7), # [2, 1, 3, 4, 5, 2] -> Distinct: {1, 2, 3, 4, 5} -> 5
        (5, 8)  # [4, 5, 2, 8]    -> Distinct: {2, 4, 5, 8} -> 4
    ]
    
    print(f"Input Array: {arr}")
    print("Queries:")
    for i, (L, R) in enumerate(queries_input):
        print(f" Query {i}: Range [{L}, {R}] -> {arr[L:R+1]}")
        
    print("\nExecuting Mo's Algorithm...")
    answers = mos_algorithm(arr, queries_input)
    
    print("\nResults:")
    for i, (L, R) in enumerate(queries_input):
        print(f" Query {i} [{L}, {R}]: {answers[i]} distinct elements.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does "Offline Queries" mean?
   Answer: It means all queries are provided to the algorithm upfront as a batch. You do not have to answer Query 1 before you receive Query 2. This allows you to sort the queries in any order that optimizes computation, and then map the answers back to their original order later. Segment Trees are "Online" because they can answer queries instantly as they arrive.

2. How does sorting `(L // block_size, R)` guarantee `O(N * sqrt(N))`?
   Answer: 
   - The Right pointer always moves forward within a single block. Across all queries in one block, it travels at most `N` steps. There are `sqrt(N)` blocks. So the Right pointer moves a maximum of `N * sqrt(N)` times globally.
   - The Left pointer bounces around randomly, BUT it is strictly trapped inside its block of size `sqrt(N)`. For `Q` queries, it moves a maximum of `Q * sqrt(N)` times.
   - Total pointer movements: `O((N + Q) * sqrt(N))`.

3. Why can't Mo's algorithm handle updates (mutations to the array)?
   Answer: Because Mo's algorithm requires all queries to be known in advance and sorted out of chronological order. If you update the array at Time=2, but Mo's algorithm sorted Query 5 to be processed before Query 1, the sliding window will read corrupted, chronologically inaccurate data.
"""

if __name__ == "__main__":
    demonstrate_mos_algorithm()
    print("\n[SUCCESS] Laboratory: Mo's Algorithm Completed.")
