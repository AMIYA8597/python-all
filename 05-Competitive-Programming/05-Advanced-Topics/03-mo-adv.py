"""
Mo's Algorithm (Advanced Competitive Programming)

1. Introduction
---------------
Mo's Algorithm is a powerful offline algorithm used to answer range queries on an array in
O((N + Q) * sqrt(N)) time, where N is the array size and Q is the number of queries.
It is typically applied when:
- Queries can be answered offline (i.e., we know all queries beforehand).
- There are no updates to the array (or only updates that can be integrated via techniques like 3D Mo).
- We can easily transition from the answer for range [L, R] to [L-1, R], [L+1, R], [L, R-1], or [L, R+1] in O(1) or O(log N) time.

2. Learning Objectives
----------------------
- Understand the offline query sorting technique (Sqrt Decomposition on Queries).
- Implement the add/remove transitions efficiently.
- Apply Mo's algorithm to solve classical problems like "Count unique elements in a range".

3. Concept Explanation
----------------------
We divide the array indices [0, N-1] into blocks of size approximately sqrt(N).
For any query (L, R), it falls into block `L / sqrt(N)`.
We sort all queries primarily by their block number, and secondarily by their R endpoint.
- Sorting by `L / block_size` groups queries starting in the same block.
- Sorting by `R` (often alternating ascending/descending to optimize R's movement) ensures that R moves continuously.

By moving L and R pointers one step at a time (expanding or shrinking the window) and updating the running answer, the total movement of L is bounded by O(Q * sqrt(N)), and R is bounded by O(N * sqrt(N)). Overall time complexity is O((N+Q) * sqrt(N)).

4. Real-world / Industry Use Cases
----------------------------------
While mainly popular in competitive programming, the core idea of block-processing and offline query batching translates to database query optimization, particularly in processing sliding window aggregations or batching analytical requests on static historical data.

5. Complexity
-------------
- Time Complexity: O((N + Q) * sqrt(N) * F), where F is the cost of moving a pointer one step.
- Space Complexity: O(N + Q) for storing arrays, queries, and frequencies.
"""

from typing import List, Tuple, Callable
import math

class Query:
    """Represents a range query."""
    def __init__(self, idx: int, l: int, r: int, block_size: int):
        self.idx = idx
        self.l = l
        self.r = r
        self.block_idx = l // block_size
        
    def __lt__(self, other: 'Query') -> bool:
        # Sort by block index of L first
        if self.block_idx != other.block_idx:
            return self.block_idx < other.block_idx
        # To optimize R's movement (Hilbert curve or alternating parity optimization)
        if self.block_idx % 2 == 1:
            return self.r < other.r
        return self.r > other.r


def mos_algorithm(arr: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    Given an array and a list of queries (L, R), returns the number of unique elements
    in the range [L, R] for each query using Mo's Algorithm.
    
    :param arr: The static input array.
    :param queries: List of 0-indexed query ranges (L, R) inclusive.
    :return: List of answers corresponding to each query.
    """
    n = len(arr)
    q = len(queries)
    if q == 0:
        return []
        
    block_size = int(math.sqrt(n)) + 1
    
    mo_queries = [Query(i, l, r, block_size) for i, (l, r) in enumerate(queries)]
    mo_queries.sort()
    
    answers = [0] * q
    
    # State tracking
    current_l = 0
    current_r = -1
    unique_count = 0
    freq = {}
    
    def add(idx: int):
        nonlocal unique_count
        val = arr[idx]
        if freq.get(val, 0) == 0:
            unique_count += 1
        freq[val] = freq.get(val, 0) + 1
        
    def remove(idx: int):
        nonlocal unique_count
        val = arr[idx]
        freq[val] -= 1
        if freq[val] == 0:
            unique_count -= 1
            
    for mq in mo_queries:
        L = mq.l
        R = mq.r
        
        # Expand / Shrink the window to match [L, R]
        # Expand R
        while current_r < R:
            current_r += 1
            add(current_r)
        # Shrink R
        while current_r > R:
            remove(current_r)
            current_r -= 1
        # Expand L (move left)
        while current_l > L:
            current_l -= 1
            add(current_l)
        # Shrink L (move right)
        while current_l < L:
            remove(current_l)
            current_l += 1
            
        answers[mq.idx] = unique_count
        
    return answers


# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. State integrity: Always be precise about `current_l` and `current_r`. If you start with
#    l=0, r=-1, then the initial window is empty, which is correct.
# 2. Time constants: Using Python dictionaries for `freq` can be slow. Using an array (if max
#    value is small) or array-based compression (coordinate compression) is highly recommended.
# 3. Fast transitions: Ensure `add` and `remove` are purely O(1). O(log N) inside adds log N to
#    the O(N sqrt N) complexity, causing Time Limit Exceeded (TLE) in CP.


# ==========================================
# Interview Challenge / Exercise
# ==========================================
# Q: How would you adapt Mo's algorithm if there are point updates in the array?
# A: You can use "3D Mo's Algorithm" (or Mo's with updates). We add a third dimension 'time' (t),
#    representing the number of updates applied. Queries are sorted by (L block, R block, t).
#    Complexity becomes O(N^(5/3)).

if __name__ == "__main__":
    # Test cases
    print("Testing Mo's Algorithm...")
    
    # Array: [1, 1, 2, 1, 3, 4, 5, 2, 8]
    test_arr = [1, 1, 2, 1, 3, 4, 5, 2, 8]
    # Queries:
    # 1. [0, 4] -> [1, 1, 2, 1, 3] -> Unique: 1, 2, 3 -> 3
    # 2. [1, 3] -> [1, 2, 1] -> Unique: 1, 2 -> 2
    # 3. [2, 4] -> [2, 1, 3] -> Unique: 1, 2, 3 -> 3
    # 4. [4, 8] -> [3, 4, 5, 2, 8] -> Unique: 2, 3, 4, 5, 8 -> 5
    
    test_queries = [(0, 4), (1, 3), (2, 4), (4, 8)]
    
    ans = mos_algorithm(test_arr, test_queries)
    print(f"Results: {ans}")
    
    assert ans == [3, 2, 3, 5], f"Expected [3, 2, 3, 5], got {ans}"
    print("All tests passed!")
