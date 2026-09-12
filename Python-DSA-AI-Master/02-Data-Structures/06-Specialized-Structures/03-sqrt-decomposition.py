"""
## A. Concept Name
Square Root Decomposition

## B. Learning Objectives
1. Understand the concept of Square Root (Sqrt) Decomposition.
2. Partition an array into blocks to speed up range queries.
3. Combine block updates and partial block updates efficiently.

## C. Concept Explanation
Sqrt Decomposition is a technique to answer range queries and perform range updates in O(sqrt(N)) time. By dividing an array of length N into blocks of size sqrt(N), any range query can be answered by combining precomputed answers for full blocks and sequentially processing partial blocks at the boundaries.

## X. Project Connection
Can be directly applied to AI data processing pipelines where time-series analytics and rolling sum operations are updated incrementally while being queried simultaneously in constant-time batches.
"""

import math
from typing import List

class SqrtDecomposition:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.arr = list(arr)
        if self.n > 0:
            self.block_size = int(math.sqrt(self.n))
            self.num_blocks = math.ceil(self.n / self.block_size)
            self.blocks = [0] * self.num_blocks
            
            # Precompute sum for each block
            for i in range(self.n):
                self.blocks[i // self.block_size] += self.arr[i]

    def update(self, idx: int, val: int) -> None:
        """Updates the value at arr[idx] to val."""
        block_idx = idx // self.block_size
        self.blocks[block_idx] += val - self.arr[idx]
        self.arr[idx] = val

    def query_sum(self, L: int, R: int) -> int:
        """Returns the sum of arr[L:R+1]."""
        total = 0
        start_block = L // self.block_size
        end_block = R // self.block_size
        
        if start_block == end_block:
            # Same block, iterate sequentially
            for i in range(L, R + 1):
                total += self.arr[i]
        else:
            # Add partial start block
            for i in range(L, (start_block + 1) * self.block_size):
                total += self.arr[i]
            # Add full intermediate blocks
            for b in range(start_block + 1, end_block):
                total += self.blocks[b]
            # Add partial end block
            for i in range(end_block * self.block_size, R + 1):
                total += self.arr[i]
                
        return total

# Performance Analysis:
# - Time Complexity: Build O(N). Update O(1). Query O(sqrt(N)).
# - Space Complexity: O(sqrt(N)) auxiliary space for the blocks array.

# Edge Cases:
# - Array with a single element.
# - Range query encompassing the entire array or a single element.

# Interview Challenge:
# Implement a mutable range sum query data structure (Segment Tree or Sqrt Decomposition).

# Tests
def test_sqrt_decomposition():
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sd = SqrtDecomposition(arr)
    
    assert sd.query_sum(0, 2) == 6
    assert sd.query_sum(2, 6) == 25
    
    sd.update(3, 10) # arr becomes [1, 2, 3, 10, 5, 6, 7, 8, 9]
    assert sd.query_sum(2, 6) == 31

if __name__ == "__main__":
    test_sqrt_decomposition()
    print("03-sqrt-decomposition.py tests passed successfully!")
