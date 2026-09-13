"""
# ==============================================================================
# LABORATORY: SPARSE TABLES (O(1) RANGE QUERIES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned about Segment Trees and Fenwick Trees earlier. They are powerful 
# because they can answer Range Queries (e.g., "What is the minimum value between 
# index 5 and 100?") in O(log N) time, AND they allow you to UPDATE values in 
# O(log N) time.
#
# But what if your data NEVER changes? (e.g., A massive array of historical 
# temperature readings). If the data is STATIC, O(log N) query time is actually 
# too slow!
#
# A "Sparse Table" is a magical data structure that precomputes answers using 
# Dynamic Programming. It takes O(N log N) time to build, but it can answer ANY 
# Range Minimum Query (RMQ) in strict O(1) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the math of "Powers of 2" overlapping intervals.
# - Implement O(N log N) DP precomputation.
# - Answer Range Minimum Queries in O(1) time.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SPARSE TABLE IMPLEMENTATION
# ==============================================================================
class SparseTable:
    def __init__(self, arr: List[int]):
        """
        Builds the Sparse Table in O(N log N) time and space.
        `table[i][j]` stores the minimum value in the range [i, i + 2^j - 1].
        Basically, starting at index `i`, what is the minimum of the next `2^j` elements?
        """
        self.n = len(arr)
        
        # Calculate the maximum power of 2 needed (e.g., if N=10, max_j is 3, since 2^3=8)
        self.max_j = int(math.log2(self.n)) + 1
        
        # Initialize table with zeroes
        self.table = [[0] * self.max_j for _ in range(self.n)]
        
        # Base Case (j = 0): 
        # The minimum of a range of length 2^0 (1 element) is just the element itself!
        for i in range(self.n):
            self.table[i][0] = arr[i]
            
        # DP Transition: Build ranges of size 2, 4, 8, 16...
        for j in range(1, self.max_j):
            # The length of the interval we are currently building is 2^j
            interval_length = 1 << j
            
            # The length of the PREVIOUS interval is 2^(j-1)
            half_length = 1 << (j - 1)
            
            for i in range(self.n):
                # Ensure the interval doesn't go out of bounds
                if i + interval_length <= self.n:
                    # To find the minimum of 8 elements, we just compare the minimum 
                    # of the FIRST 4 elements with the minimum of the LAST 4 elements!
                    # Both of these answers were already computed in the previous loop (j-1).
                    left_min = self.table[i][j - 1]
                    right_min = self.table[i + half_length][j - 1]
                    
                    self.table[i][j] = min(left_min, right_min)

    def query(self, L: int, R: int) -> int:
        """
        Answers Range Minimum Query (RMQ) in STRICT O(1) time.
        """
        if L > R or L < 0 or R >= self.n:
            raise ValueError("Invalid query range")
            
        # 1. Find the length of the query range
        length = R - L + 1
        
        # 2. Find the largest power of 2 that completely fits INSIDE this range.
        # E.g., if length is 14, the largest power of 2 is 8 (2^3). So j = 3.
        j = int(math.log2(length))
        
        # 3. Overlap two intervals of length 2^j!
        # Interval 1: Starts at L, goes forward 8 elements. [L, L+7]
        left_min = self.table[L][j]
        
        # Interval 2: Starts at (R - 2^j + 1), goes forward 8 elements ending exactly at R!
        right_min = self.table[R - (1 << j) + 1][j]
        
        # Because `min(a, a) == a`, it DOES NOT MATTER that these two intervals overlap!
        # By taking the minimum of the two intervals, we cover the entire 14-element range.
        return min(left_min, right_min)

def demonstrate_sparse_table():
    section_header("Algorithm: Sparse Table (Range Minimum Query)")
    
    # Indices:    0   1  2  3  4  5  6   7  8
    arr =       [ 7,  2, 3, 0, 5, 10, 3, 12, 18 ]
    
    print(f"Input Array: {arr}")
    print("Building Sparse Table (O(N log N))...")
    st = SparseTable(arr)
    
    queries = [
        (0, 2), # min of [7, 2, 3] -> 2
        (2, 5), # min of [3, 0, 5, 10] -> 0
        (4, 8), # min of [5, 10, 3, 12, 18] -> 3
        (6, 7), # min of [3, 12] -> 3
        (0, 8)  # min of entire array -> 0
    ]
    
    print("\nExecuting O(1) Queries:")
    for L, R in queries:
        ans = st.query(L, R)
        subarray = arr[L:R+1]
        print(f" Query [{L}, {R}]: {ans} (Subarray: {subarray})")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Sparse Table take O(1) for queries, while Segment Tree takes O(log N)?
   Answer: A Segment Tree splits a query range into exactly non-overlapping blocks. A range might be split into `log N` tiny blocks, requiring you to add them all up. A Sparse Table relies on the "Idempotent Property" (e.g., `min(x, x) = x`). Because overlapping doesn't affect the answer, a Sparse Table just drops TWO massive overlapping blocks that perfectly cover the range, finding the answer in exactly 2 lookups.

2. What is an Idempotent Operation, and why does Sparse Table require it?
   Answer: Idempotent means applying the operation multiple times yields the same result. `min(5, 5) = 5`. `max(10, 10) = 10`. `gcd(8, 8) = 8`. Sparse Tables work perfectly for Min, Max, and GCD because the two `O(1)` query intervals OVERLAP. If you tried to use a Sparse Table for RANGE SUM, the overlapping middle section would be added TWICE, corrupting the answer!

3. Can you update a value in a Sparse Table?
   Answer: Technically yes, but it is catastrophic. Updating a single value at index `i` requires recalculating every single `2^j` interval that includes `i`. This takes `O(N)` time. If you need updates, use a Segment Tree or Fenwick Tree. Sparse Tables are strictly for static, immutable data.
"""

if __name__ == "__main__":
    demonstrate_sparse_table()
    print("\n[SUCCESS] Laboratory: Sparse Tables Completed.")
