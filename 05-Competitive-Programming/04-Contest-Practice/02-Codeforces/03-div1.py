"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODEFORCES DIV-1)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Codeforces Division 1 is the realm of Grandmasters.
# 
# You are given an array of 100,000 numbers. You are given 100,000 queries.
# Each query asks: "How many UNIQUE numbers exist between index L and index R?"
#
# Can you use a Prefix Sum array? No! Unique counts do not add linearly. 
# (If Left has '5' and Right has '5', they combine to 1 unique, not 2).
#
# Can you use a Segment Tree? Yes, but merging unique sets takes O(N) time 
# per node, which destroys the O(log N) tree performance, causing a TLE.
#
# The queries are "Offline" (you are given all queries in advance). You must 
# use Mo's Algorithm! Mo's Algorithm uses Square Root Decomposition to chop 
# the array into blocks of size sqrt(N). It then performs a highly specialized 
# 2D mathematical sort on the queries, simulating a two-pointer sliding window 
# that answers ALL queries in exactly O(N * sqrt(N)) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Square Root Decomposition.
# - Master Mo's Algorithm for Offline Queries.
# - Master the mathematical Block Sorting logic.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MO'S ALGORITHM (SQUARE ROOT DECOMPOSITION)
# ==============================================================================
def mos_algorithm(arr: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """
    Solves Offline Range Queries (like count of Unique Elements).
    Time Complexity: O((N + Q) * sqrt(N))
    Space Complexity: O(N) for frequency tracking.
    """
    n = len(arr)
    q = len(queries)
    
    # 1. Calculate the Block Size (Square Root of N)
    # The array is mathematically divided into chunks of this size.
    block_size = int(math.sqrt(n)) + 1
    
    # We must append the ORIGINAL index of the query to it, because we are 
    # about to scramble the order of the queries! We need to put the answers 
    # back into the correct slots at the very end.
    processed_queries = []
    for i, (l, r) in enumerate(queries):
        processed_queries.append((l, r, i))
        
    # 2. THE MO'S SORTING MAGIC
    # Sort primarily by the BLOCK the Left pointer is in.
    # Sort secondarily by the position of the Right pointer.
    # This mathematical sort guarantees that the Sliding Window barely moves!
    processed_queries.sort(key=lambda x: (x[0] // block_size, x[1]))
    
    # Global state tracker for the sliding window
    current_l = 0
    current_r = -1
    current_unique = 0
    freq = {}
    
    # Array to hold the answers in the correct original order
    answers = [0] * q
    
    # Helper functions to add/remove elements as the window slides
    def add(index: int):
        nonlocal current_unique
        val = arr[index]
        freq[val] = freq.get(val, 0) + 1
        # If this is the FIRST time we are seeing this value in the window...
        if freq[val] == 1:
            current_unique += 1
            
    def remove(index: int):
        nonlocal current_unique
        val = arr[index]
        freq[val] -= 1
        # If the value is completely gone from the window...
        if freq[val] == 0:
            current_unique -= 1
            
    # 3. Process the queries!
    for target_l, target_r, original_idx in processed_queries:
        
        # Expand/Contract the window until it perfectly matches [target_l, target_r]
        
        # Expand Right
        while current_r < target_r:
            current_r += 1
            add(current_r)
            
        # Contract Right
        while current_r > target_r:
            remove(current_r)
            current_r -= 1
            
        # Contract Left
        while current_l < target_l:
            remove(current_l)
            current_l += 1
            
        # Expand Left
        while current_l > target_l:
            current_l -= 1
            add(current_l)
            
        # The window perfectly matches the query! Save the answer!
        answers[original_idx] = current_unique
        
    return answers

def demonstrate_mos_algorithm():
    section_header("Mo's Algorithm (Offline Unique Count)")
    
    arr = [1, 1, 2, 1, 3, 4, 2, 2]
    # Queries: (L, R)
    queries = [(0, 3), (1, 6), (2, 4), (0, 7)]
    
    print(f"Array: {arr}")
    print(f"Queries (L, R): {queries}")
    
    ans = mos_algorithm(arr, queries)
    
    print(f"\nResults for Unique Count in Range:")
    for i, (l, r) in enumerate(queries):
        print(f"Query {i} ({l}, {r}): {ans[i]} unique numbers.")
        
    print("\nExpected:")
    print("Query 0 (0,3): [1,1,2,1] -> 2 unique (1, 2)")
    print("Query 1 (1,6): [1,2,1,3,4,2] -> 4 unique (1, 2, 3, 4)")
    print("Query 2 (2,4): [2,1,3] -> 3 unique (1, 2, 3)")


def run_all_labs():
    demonstrate_mos_algorithm()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the philosophical concept of an "Offline Algorithm" versus an "Online Algorithm".
   Answer: An Online algorithm is forced to answer queries exactly as they are fed to it, one by one. If it receives Query 1, it must output Answer 1 before it is allowed to see Query 2. (This simulates real-time server traffic). An Offline algorithm is given the entire list of 100,000 queries instantly, in advance. Because it can see the future, it is mathematically allowed to completely ignore the order the queries were asked in. It can sort them, group them, process them in whatever order is most mathematically efficient, and then simply re-organize the answers at the very end. Mo's Algorithm strictly relies on seeing the future to achieve its time complexity.

2. In Mo's Algorithm, how does the mathematical sort `key=lambda x: (x[0] // block_size, x[1])` drop the time complexity to $O(N \sqrt{N})$?
   Answer: We chop the array into blocks of size $\sqrt{N}$. The primary sort groups all queries whose Left Pointer sits inside the exact same Block. Within that same block, it sorts the queries by their Right Pointer. Let's trace the pointers! The Left pointer is restricted to moving inside a block of size $\sqrt{N}$. It moves at most $\sqrt{N}$ steps per query. Over $Q$ queries, the Left pointer moves $Q \times \sqrt{N}$ times. The Right pointer is strictly ascending! Within a single block, the Right pointer only sweeps forward, moving at most $N$ steps across the entire array. Because there are $\sqrt{N}$ blocks, the Right pointer sweeps across the array $\sqrt{N}$ times. Over the entire execution, the maximum pointer movements are mathematically bound to $(Q \sqrt{N}) + (N \sqrt{N})$, which simplifies beautifully to $O((N+Q)\sqrt{N})$.

3. Why can't Mo's Algorithm be used to solve "Range Sum Queries" faster than a Segment Tree?
   Answer: A Segment Tree solves Range Sum Queries in exactly $O(\log N)$ time per query. If there are $Q$ queries, the total time is $O(Q \log N)$. Mo's Algorithm runs in $O(Q \sqrt{N})$. Mathematically, $\sqrt{N}$ is drastically larger and slower than $\log N$! For an array of 1,000,000, $\sqrt{N}$ is 1000 operations, but $\log N$ is only 20 operations! Mo's Algorithm is computationally inferior to a Segment Tree for simple problems. Mo's Algorithm is ONLY used for problems where the mathematical State (like tracking Unique Counts or Mode Frequencies) is physically impossible to merge inside a Segment Tree node without triggering an $O(N)$ penalty.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Codeforces Div-1 Completed.")
