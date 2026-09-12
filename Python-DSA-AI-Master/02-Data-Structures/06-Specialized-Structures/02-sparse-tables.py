"""
# Sparse Tables: The Art of Idempotent Range Queries

## A. Concept Name
Sparse Tables

## B. Intuition & Real-World Analogy
Imagine you are a meteorologist and need to find the lowest temperature over a specific range of days in a year. The temperatures do not change (they are historical data). Instead of iterating through the days every time someone asks for the minimum temperature, you can precalculate the minimums for various intervals of days. 
However, precalculating every possible interval takes too much time and space. Instead, you precalculate the minimums for intervals of lengths that are powers of 2 (1, 2, 4, 8, 16...). If someone asks for the minimum over a 7-day period, you don't need a 7-day precalculated answer! You can simply look at the minimum of the first 4 days and the minimum of the last 4 days (they overlap, but since finding a minimum over overlapping elements doesn't change the answer, this is perfectly fine). This overlapping trick works for any "idempotent" operation (where applying it multiple times doesn't change the result, like min, max, or GCD).

## C. Formal Explanation
A Sparse Table is a data structure that answers range queries on a static array. It is particularly famous for the Range Minimum Query (RMQ) problem. It relies on the concept of idempotent functions—functions where `f(x, x) = x`. For such functions, overlapping ranges can be combined to answer queries over any arbitrary range in O(1) time.
The structure precomputes answers for all intervals of length `2^j` starting at index `i`.
- `st[i][j]` stores the answer for the range `[i, i + 2^j - 1]`.
- The recurrence relation to build the table is:
  `st[i][j] = min(st[i][j - 1], st[i + 2^(j - 1)][j - 1])`
- To query a range `[L, R]`, we find the largest power of 2, say `2^k`, that is less than or equal to the length of the range `R - L + 1`. The answer is then:
  `min(st[L][k], st[R - 2^k + 1][k])`

## D. Complexity
- **Time Complexity:**
  - **Preprocessing:** `O(N log N)` where `N` is the number of elements. We compute `N` states for each of the `log N` levels.
  - **Query:** `O(1)` for idempotent operations (like min, max, GCD). O(log N) for non-idempotent ones (like sum), though Fenwick/Segment trees are usually better for sum.
- **Space Complexity:**
  - `O(N log N)` to store the table.

## E. Implementation (Beginner to Professional)
"""

import math
from typing import List, Callable

class SparseTable:
    """
    A professional-grade Sparse Table implementation supporting any idempotent operation.
    """
    def __init__(self, arr: List[int], func: Callable[[int, int], int] = min):
        """
        Initializes the sparse table.
        
        :param arr: The static input array.
        :param func: The idempotent function to use (e.g., min, max, math.gcd).
        """
        self.n = len(arr)
        self.func = func
        
        if self.n == 0:
            self.st = []
            return
            
        # The maximum power of 2 needed is log2(N)
        self.max_pow = int(math.log2(self.n)) + 1
        
        # Precompute logs to avoid math.log2 calls during queries for O(1) strictly
        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1
            
        # st[i][j] stores the result of func for range [i, i + 2^j - 1]
        self.st = [[0] * self.max_pow for _ in range(self.n)]
        
        # Base case: intervals of length 2^0 = 1
        for i in range(self.n):
            self.st[i][0] = arr[i]
            
        # Build the table dynamically for lengths 2^1, 2^2, ..., 2^max_pow
        for j in range(1, self.max_pow):
            # We can only start at index i if an interval of length 2^j fits in the array
            for i in range(self.n - (1 << j) + 1):
                # Combine two intervals of length 2^(j-1)
                left_interval_val = self.st[i][j - 1]
                right_interval_val = self.st[i + (1 << (j - 1))][j - 1]
                self.st[i][j] = self.func(left_interval_val, right_interval_val)

    def query(self, L: int, R: int) -> int:
        """
        Answers the range query [L, R] in O(1) time.
        
        :param L: Left boundary (inclusive).
        :param R: Right boundary (inclusive).
        :return: The result of the idempotent function over the range.
        """
        if self.n == 0:
            raise ValueError("Cannot query an empty Sparse Table.")
        if L > R or L < 0 or R >= self.n:
            raise ValueError(f"Invalid query range: [{L}, {R}] for array of size {self.n}")
            
        # The length of the range
        length = R - L + 1
        
        # Find the largest power of 2 that fits into the range
        # Using precomputed logs for strict O(1)
        j = self.log_table[length]
        
        # Overlap the two intervals of length 2^j
        left_val = self.st[L][j]
        right_val = self.st[R - (1 << j) + 1][j]
        
        return self.func(left_val, right_val)

"""
## F. Debugging & Common Mistakes
1. **Off-by-One Errors in Table Building:**
   When looping `for i in range(self.n - (1 << j) + 1)`, the `+ 1` is crucial to include the last valid starting index. Forgetting it will leave the table incomplete.
2. **Non-Idempotent Operations:**
   Using Sparse Tables for Sum Queries is a mistake if you try to use the O(1) query method. Summing two overlapping intervals will double-count the overlap! For sums, use a Segment Tree, Fenwick Tree, or Prefix Sums.
3. **Logarithm Overhead in Queries:**
   Calling `math.log2()` inside the `query()` function makes the query operation heavily constrained by float operations. Precomputing logs in an array ensures true `O(1)` integer operations.
4. **Out of Bounds Query:**
   Always validate `0 <= L <= R < n` before computing anything.

## G. Active Recall & Memory Anchors
- **Memory Anchor:** Sparse Table = "Power of 2 Overlap".
- **Question:** Why does Sparse Table take `O(N log N)` space?
  **Answer:** For each of the `N` elements, we store answers for intervals of length `1, 2, 4, 8...` up to `N`. There are `log2(N)` such lengths. Thus, `N * log2(N)` space.
- **Question:** Why doesn't Sparse Table work for Range Sum Queries in `O(1)`?
  **Answer:** Sum is not idempotent. Adding overlapping ranges `[0, 3]` and `[2, 5]` to cover `[0, 5]` means elements at index 2 and 3 are summed twice!

## H. Real-World Application Connection
Sparse tables are foundational in AI data preprocessing steps, particularly when analyzing time-series data or making rapid idempotent queries (like finding the minimum error rate over overlapping sliding windows in machine learning pipelines) where array values do not change. They are also used as a building block for the O(1) LCA (Lowest Common Ancestor) algorithm on trees.
"""

# Tests
def test_sparse_table():
    arr = [1, 3, 2, 7, 9, 11, 3, 5, 4, 1]
    
    # Range Minimum Query
    st_min = SparseTable(arr, min)
    assert st_min.query(0, 2) == 1
    assert st_min.query(1, 4) == 2
    assert st_min.query(3, 7) == 3
    assert st_min.query(0, 9) == 1
    assert st_min.query(5, 5) == 11

    # Range Maximum Query
    st_max = SparseTable(arr, max)
    assert st_max.query(0, 2) == 3
    assert st_max.query(1, 4) == 9
    assert st_max.query(3, 7) == 11
    assert st_max.query(0, 9) == 11
    
    # Range GCD Query
    arr_gcd = [2, 4, 6, 8, 12, 18, 6, 3]
    st_gcd = SparseTable(arr_gcd, math.gcd)
    assert st_gcd.query(0, 3) == 2  # gcd(2,4,6,8) = 2
    assert st_gcd.query(4, 5) == 6  # gcd(12,18) = 6
    assert st_gcd.query(4, 7) == 3  # gcd(12,18,6,3) = 3
    
if __name__ == "__main__":
    test_sparse_table()
    print("02-sparse-tables.py tests passed successfully!")
