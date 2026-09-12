"""
## A. Concept Name
Mo's Algorithm

## B. Concept Explanation
Mo's Algorithm is used for answering offline range queries. If queries can be answered offline (i.e., all queries are known beforehand and can be answered in any order), we can sort them using a specialized criteria based on Sqrt Decomposition. We then use a sliding window (two pointers) to transition from one query's range to the next, keeping a running answer.

## C. Learning Objectives
1. Understand offline query processing.
2. Combine Sqrt Decomposition with two-pointer techniques.
3. Solve complex range queries efficiently using Mo's Algorithm.

## D. Performance Analysis
- Time Complexity: Sorting queries takes O(Q log Q). Transitioning pointers takes O(N * sqrt(N) + Q * sqrt(N)). Total Time: O((N+Q) * sqrt(N)).
- Space Complexity: O(Q) for queries and answers.

## E. Edge Cases
- Empty arrays or zero queries.
- Overlapping ranges and single-element ranges.

## F. Interview Challenge
D-Query (Spoj)
Find the number of distinct elements in various subarray ranges offline.

## X. Project Connection
Used in database and data analytics systems for efficiently processing a large batch of read-only aggregation queries over static arrays or time-series datasets.
"""

import math
from typing import List, Tuple

class MosQuery:
    def __init__(self, L: int, R: int, id: int, block_size: int):
        self.L = L
        self.R = R
        self.id = id
        self.block_idx = L // block_size

    def __lt__(self, other: 'MosQuery'):
        if self.block_idx != other.block_idx:
            return self.block_idx < other.block_idx
        # Optimize by alternating R sorting direction for odd/even blocks
        if self.block_idx % 2 == 1:
            return self.R < other.R
        return self.R > other.R

def mos_algorithm(arr: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    n = len(arr)
    q = len(queries)
    if n == 0 or q == 0:
        return []

    block_size = int(math.sqrt(n))
    mos_queries = [MosQuery(L, R, i, block_size) for i, (L, R) in enumerate(queries)]
    mos_queries.sort()

    answers = [0] * q
    current_sum = 0
    curr_L, curr_R = 0, -1

    def add(idx: int):
        nonlocal current_sum
        current_sum += arr[idx]

    def remove(idx: int):
        nonlocal current_sum
        current_sum -= arr[idx]

    for mq in mos_queries:
        L, R = mq.L, mq.R
        
        while curr_L > L:
            curr_L -= 1
            add(curr_L)
        while curr_R < R:
            curr_R += 1
            add(curr_R)
        while curr_L < L:
            remove(curr_L)
            curr_L += 1
        while curr_R > R:
            remove(curr_R)
            curr_R -= 1
            
        answers[mq.id] = current_sum

    return answers


# Tests
def test_mos_algorithm():
    arr = [1, 1, 2, 1, 3, 4, 5, 2, 8]
    queries = [(0, 4), (1, 3), (2, 4)]
    
    # query(0,4) -> sum(1,1,2,1,3) = 8
    # query(1,3) -> sum(1,2,1) = 4
    # query(2,4) -> sum(2,1,3) = 6
    ans = mos_algorithm(arr, queries)
    assert ans == [8, 4, 6]

if __name__ == "__main__":
    test_mos_algorithm()
    print("04-mos-algorithm.py tests passed successfully!")
