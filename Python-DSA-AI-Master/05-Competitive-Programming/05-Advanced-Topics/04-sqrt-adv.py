"""
Square Root (Sqrt) Decomposition

1. Introduction
---------------
Sqrt Decomposition is a technique to reduce the time complexity of operations like
range sum, range minimum, or range updates from O(N) to O(sqrt(N)).
It provides a versatile middle ground between O(1) or O(N) trivial arrays and O(log N)
Segment Trees. Often, when an operation is too difficult to formulate for a segment
tree, sqrt decomposition is straightforward and easily modifiable.

2. Learning Objectives
----------------------
- Grasp the core concept of dividing an array into blocks of size `sqrt(N)`.
- Implement Range Sum Query with Point Updates.
- Understand block boundaries and partial vs. full block overlapping.

3. Concept Explanation
----------------------
Given an array of size N, we divide it into `ceil(sqrt(N))` blocks, each containing
at most `ceil(sqrt(N))` elements. We precalculate the answer (e.g., sum) for each block.
- Point Update: Update the element in O(1), and update its block's aggregate in O(1).
- Range Query [L, R]:
  - Sum elements from L to the end of L's block (partial block).
  - Sum the precalculated block values for all completely covered blocks.
  - Sum elements from the beginning of R's block to R (partial block).
  The maximum number of partial elements scanned is ~2*sqrt(N). The maximum number of
  blocks scanned is ~sqrt(N). Thus, O(sqrt(N)) time.

4. Real-world / Industry Use Cases
----------------------------------
- Sharding / Partitioning: Used in big data systems to divide massive logs or events
  into temporal partitions (e.g., daily chunks).
- Machine Learning: Certain sampling techniques block data to balance between uniform
  random access and contiguous block access.

5. Complexity
-------------
- Preprocessing Time: O(N)
- Range Query Time: O(sqrt(N))
- Point Update Time: O(1)
- Space: O(sqrt(N)) extra space for block aggregates.
"""

from typing import List
import math

class SqrtDecomposition:
    """
    A data structure to answer Range Sum Queries and handle Point Updates
    using Sqrt Decomposition.
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.arr = arr.copy()
        
        # Calculate block size and number of blocks
        self.block_size = int(math.sqrt(self.n))
        if self.block_size == 0:
            self.block_size = 1
            
        self.num_blocks = math.ceil(self.n / self.block_size)
        
        # Precompute block sums
        self.block_sums = [0] * self.num_blocks
        for i in range(self.n):
            self.block_sums[i // self.block_size] += self.arr[i]

    def update(self, idx: int, value: int) -> None:
        """
        Update the array at `idx` to `value`.
        Time Complexity: O(1)
        """
        if idx < 0 or idx >= self.n:
            raise IndexError("Index out of bounds")
            
        block_idx = idx // self.block_size
        # Adjust the block sum by the difference
        diff = value - self.arr[idx]
        self.block_sums[block_idx] += diff
        # Update the original array
        self.arr[idx] = value

    def query(self, L: int, R: int) -> int:
        """
        Get the sum in the range [L, R] inclusive.
        Time Complexity: O(sqrt(N))
        """
        if L < 0 or R >= self.n or L > R:
            return 0
            
        total_sum = 0
        
        start_block = L // self.block_size
        end_block = R // self.block_size
        
        if start_block == end_block:
            # The range is completely within a single block
            for i in range(L, R + 1):
                total_sum += self.arr[i]
        else:
            # 1. Partial block at the beginning
            start_block_end = (start_block + 1) * self.block_size - 1
            for i in range(L, start_block_end + 1):
                total_sum += self.arr[i]
                
            # 2. Completely covered blocks in the middle
            for b in range(start_block + 1, end_block):
                total_sum += self.block_sums[b]
                
            # 3. Partial block at the end
            end_block_start = end_block * self.block_size
            for i in range(end_block_start, R + 1):
                total_sum += self.arr[i]
                
        return total_sum

# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. Block boundary indices: Off-by-one errors are extremely common when determining where
#    a partial block ends or begins.
# 2. Range queries within the same block: Must be handled carefully as `start_block == end_block`.
# 3. Caching / Python optimization: Sqrt Decomposition can be slightly slower in Python due to
#    loop overheads. It is optimal for problems where segment trees are hard to implement.

# ==========================================
# Interview Challenge / Exercise
# ==========================================
# Q: How do you support Range Updates (e.g., adding X to [L, R]) with Sqrt Decomposition?
# A: Maintain a `lazy` array of size `num_blocks`. For fully covered blocks, add X to their lazy
#    value. For partial blocks, propagate the block's lazy value to its elements, clear it, 
#    add X to the specified elements directly, and recalculate the block sum.


if __name__ == "__main__":
    print("Testing Sqrt Decomposition...")
    
    test_arr = [1, 5, 2, 4, 6, 1, 3, 5, 7, 10]
    sq = SqrtDecomposition(test_arr)
    
    # Range [1, 6] -> 5+2+4+6+1+3 = 21
    res1 = sq.query(1, 6)
    print(f"Query(1, 6): {res1}")
    assert res1 == 21, "Test 1 Failed"
    
    # Update index 3 to 10 (was 4). 
    sq.update(3, 10)
    # Range [1, 6] -> 5+2+10+6+1+3 = 27
    res2 = sq.query(1, 6)
    print(f"Query(1, 6) after update: {res2}")
    assert res2 == 27, "Test 2 Failed"
    
    # Single element query
    res3 = sq.query(8, 8)
    print(f"Query(8, 8): {res3}")
    assert res3 == 7, "Test 3 Failed"
    
    print("All tests passed!")
