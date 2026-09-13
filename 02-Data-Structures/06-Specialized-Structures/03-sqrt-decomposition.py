"""
# ==============================================================================
# LABORATORY: SQUARE ROOT DECOMPOSITION (SQRT DECOMP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned many ways to answer Range Queries:
# - Segment Trees: O(log N) Query, O(log N) Update. Complex to write.
# - Fenwick Trees: O(log N) Query, O(log N) Update. Only works for invertible math (Sum).
# - Sparse Tables: O(1) Query, O(N) Update. Fails if data changes.
#
# Square Root (Sqrt) Decomposition is a beautifully simple alternative. 
# If an array has 10,000 elements, we simply chop it up into 100 blocks, where 
# each block has exactly 100 elements (sqrt(10,000)).
# We precalculate the Sum (or Min/Max) for each of those 100 blocks.
#
# If a query asks for the sum from index 15 to 885, we just add the precalculated 
# totals of blocks 1, 2, 3, 4, 5, 6, 7, and 8, and manually scan the few straggling 
# elements at the edges!
#
# Query Time: O(sqrt(N)). Update Time: O(1).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to partition an array into Sqrt blocks.
# - Implement O(1) point updates.
# - Implement O(sqrt(N)) range queries.
# - Understand why this powers "Mo's Algorithm".
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SQRT DECOMPOSITION IMPLEMENTATION
# ==============================================================================
class SqrtDecomposition:
    """
    A Square Root Decomposition structure for Range Sum Queries.
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.arr = arr.copy() # Keep a copy of the original array for point updates
        
        # 1. Calculate the optimal block size
        self.block_size = int(math.ceil(math.sqrt(self.n)))
        
        # 2. Create the blocks array. 
        # If N=10 and block_size=4, we need 3 blocks: [0-3], [4-7], [8-9]
        num_blocks = int(math.ceil(self.n / self.block_size))
        self.blocks = [0] * num_blocks
        
        # 3. Precalculate the sum for each block (O(N) time)
        for i in range(self.n):
            block_index = i // self.block_size
            self.blocks[block_index] += self.arr[i]

    def update(self, index: int, new_value: int) -> None:
        """
        Updates a specific element in O(1) time!
        Segment Trees take O(log N) to update. Sqrt Decomp is strictly O(1)!
        """
        if index < 0 or index >= self.n:
            raise IndexError("Index out of bounds")
            
        # Calculate the difference
        difference = new_value - self.arr[index]
        
        # Update the original array
        self.arr[index] = new_value
        
        # Update the precalculated block sum
        block_index = index // self.block_size
        self.blocks[block_index] += difference

    def query(self, L: int, R: int) -> int:
        """
        Calculates the Range Sum in O(sqrt(N)) time.
        """
        if L < 0 or R >= self.n or L > R:
            raise ValueError("Invalid query range")
            
        total_sum = 0
        
        # Determine which blocks the Left and Right pointers fall into
        start_block = L // self.block_size
        end_block = R // self.block_size
        
        # Case 1: L and R are in the EXACT SAME BLOCK
        # We can't use the precalculated block sum, because the query might 
        # only cover a tiny slice of the block. We must scan it manually.
        if start_block == end_block:
            for i in range(L, R + 1):
                total_sum += self.arr[i]
            return total_sum
            
        # Case 2: L and R span across multiple blocks
        
        # Step A: Manually scan the "straggling" elements in the START block
        # From L to the very end of the start block
        end_of_start_block = (start_block + 1) * self.block_size - 1
        for i in range(L, end_of_start_block + 1):
            total_sum += self.arr[i]
            
        # Step B: Add the FULL blocks perfectly trapped in the middle!
        # This is where the magic happens. We skip hundreds of elements at a time.
        for block in range(start_block + 1, end_block):
            total_sum += self.blocks[block]
            
        # Step C: Manually scan the "straggling" elements in the END block
        # From the exact start of the end block to R
        start_of_end_block = end_block * self.block_size
        for i in range(start_of_end_block, R + 1):
            total_sum += self.arr[i]
            
        return total_sum


def demonstrate_sqrt_decomp():
    section_header("Algorithm: Square Root Decomposition (Range Sum)")
    
    # Indices:    0   1  2  3    4  5  6  7    8  9
    arr =       [ 1,  5, 2, 4,   6, 1, 3, 5,   7, 9 ]
    
    # Let's say block size is 4.
    # Block 0: [1, 5, 2, 4] -> Sum = 12
    # Block 1: [6, 1, 3, 5] -> Sum = 15
    # Block 2: [7, 9]       -> Sum = 16
    
    print(f"Input Array: {arr}")
    print(f"Array Length: {len(arr)}. Sqrt(10) is ~3.16. Block size will be 4.")
    
    sqd = SqrtDecomposition(arr)
    
    print(f"Precalculated Blocks: {sqd.blocks} (Expected: [12, 15, 16])")
    
    print("\nExecuting Query [1, 8] (From 5 to 7)...")
    ans = sqd.query(1, 8)
    print(f"Answer: {ans}")
    print("How it worked:")
    print(" 1. Scanned stragglers in Block 0 (Indices 1, 2, 3) -> 5 + 2 + 4 = 11")
    print(" 2. Instantly added entire Block 1 -> 15")
    print(" 3. Scanned straggler in Block 2 (Index 8) -> 7")
    print(" Total: 11 + 15 + 7 = 33")
    
    print("\nExecuting Point Update: Index 5 changes from 1 to 10")
    sqd.update(5, 10)
    
    print(f"New Precalculated Blocks: {sqd.blocks} (Expected: [12, 24, 16])")
    
    print("\nExecuting Query [1, 8] again...")
    ans2 = sqd.query(1, 8)
    print(f"Answer: {ans2} (Expected: 42)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Sqrt Decomposition O(sqrt(N)) for queries?
   Answer: In the worst-case scenario (querying from 0 to N-1), we scan exactly 0 straggling elements on the left, 0 straggling elements on the right, and we iterate through exactly `sqrt(N)` precalculated blocks in the middle. The maximum number of operations is bound by `sqrt(N)`.

2. Why use this over a Segment Tree if Segment Trees are O(log N)?
   Answer: `log(N)` is mathematically much faster than `sqrt(N)`. However, Sqrt Decomposition is astonishingly easy to code compared to a Segment Tree (no complex recursion or bitwise math). Also, Sqrt Decomposition updates in strictly O(1) time, while Segment Trees take O(log N) to update! If your algorithm does millions of updates but only a few queries, Sqrt Decomp is actually faster.

3. What is Mo's Algorithm?
   Answer: Mo's Algorithm takes Sqrt Decomposition to the extreme. If you have 100,000 "Offline Queries" (queries known in advance), Mo's algorithm sorts the queries based on the Sqrt Block of their Left pointer. By processing queries in this specialized sorted order, a simple Two-Pointer sliding window can answer all queries in a total time of `O(N * sqrt(N))`, which is fast enough for competitive programming.
"""

if __name__ == "__main__":
    demonstrate_sqrt_decomp()
    print("\n[SUCCESS] Laboratory: Sqrt Decomposition Completed.")
