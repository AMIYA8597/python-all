"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (SQUARE ROOT DECOMPOSITION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given an array of 100,000 numbers.
# You must handle two types of queries:
# 1. Add X to all elements in range [L, R].
# 2. Find the Sum of all elements in range [L, R].
#
# You could write a Segment Tree with Lazy Propagation. But Lazy Segment Trees 
# are notoriously difficult to debug and require ~100 lines of complex recursion.
#
# Square Root Decomposition offers a stunningly elegant alternative. 
# It chops the array into Blocks of size sqrt(N). 
# If a query completely engulfs a Block, you instantly update/query the Block's 
# metadata in O(1) time. 
# If a query partially touches a Block (at the edges L or R), you manually 
# loop through those few elements in O(sqrt N) time!
#
# It answers both Range Updates and Range Queries in strictly O(sqrt N) time 
# using simple, iterative `for` loops. No recursion. No trees. Just math.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the physical architecture of Block Decomposition.
# - Implement Range Addition and Range Sum queries.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SQUARE ROOT DECOMPOSITION (BLOCKS)
# ==============================================================================
class SqrtDecomposition:
    def __init__(self, arr: list[int]):
        self.n = len(arr)
        # 1. Calculate Block Size (usually sqrt(N))
        self.block_size = int(math.sqrt(self.n)) + 1
        
        # Calculate total number of blocks needed
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        
        # The raw data array
        self.arr = arr.copy()
        
        # Block Metadata!
        # block_sum[b] = the total sum of all elements currently in Block `b`
        self.block_sum = [0] * self.num_blocks
        # block_lazy[b] = a pending addition that applies to EVERY element in Block `b`
        self.block_lazy = [0] * self.num_blocks
        
        # Precompute the initial block sums
        for i in range(self.n):
            block_idx = i // self.block_size
            self.block_sum[block_idx] += self.arr[i]

    def update_range(self, l: int, r: int, value: int) -> None:
        """
        Adds `value` to all elements from index `l` to `r`.
        Time Complexity: O(sqrt N)
        """
        start_block = l // self.block_size
        end_block = r // self.block_size
        
        if start_block == end_block:
            # The entire query falls strictly INSIDE a single block!
            # We must iterate manually (Partial Block Update).
            for i in range(l, r + 1):
                self.arr[i] += value
                self.block_sum[start_block] += value
        else:
            # 1. Left Partial Block
            # Update from `l` to the absolute end of the `start_block`
            end_of_start_block = (start_block + 1) * self.block_size - 1
            for i in range(l, end_of_start_block + 1):
                self.arr[i] += value
                self.block_sum[start_block] += value
                
            # 2. Middle FULL Blocks!
            # These blocks are completely engulfed by the [L, R] range.
            # We update their Lazy tags in exactly O(1) time per block!
            for b in range(start_block + 1, end_block):
                self.block_lazy[b] += value
                # The block sum instantly increases by (value * number of elements in block)
                self.block_sum[b] += value * self.block_size
                
            # 3. Right Partial Block
            # Update from the absolute beginning of the `end_block` to `r`
            start_of_end_block = end_block * self.block_size
            for i in range(start_of_end_block, r + 1):
                self.arr[i] += value
                self.block_sum[end_block] += value

    def query_range(self, l: int, r: int) -> int:
        """
        Finds the sum of elements from index `l` to `r`.
        Time Complexity: O(sqrt N)
        """
        start_block = l // self.block_size
        end_block = r // self.block_size
        total = 0
        
        if start_block == end_block:
            # Strictly inside a single block
            for i in range(l, r + 1):
                total += self.arr[i] + self.block_lazy[start_block]
        else:
            # 1. Left Partial Block
            end_of_start_block = (start_block + 1) * self.block_size - 1
            for i in range(l, end_of_start_block + 1):
                total += self.arr[i] + self.block_lazy[start_block]
                
            # 2. Middle FULL Blocks!
            # We instantly grab the precomputed block sums in O(1) time!
            for b in range(start_block + 1, end_block):
                total += self.block_sum[b]
                
            # 3. Right Partial Block
            start_of_end_block = end_block * self.block_size
            for i in range(start_of_end_block, r + 1):
                total += self.arr[i] + self.block_lazy[end_block]
                
        return total

def demonstrate_sqrt_decomp():
    section_header("Square Root Decomposition")
    
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Array: {arr}")
    print(f"Length: {len(arr)}")
    
    sq = SqrtDecomposition(arr)
    print(f"Block Size calculated as: {sq.block_size}")
    
    print("\nInitial Query Sum[1, 8] (Indices 1 to 8):")
    ans = sq.query_range(1, 8)
    print(f"Result: {ans} (Expected: 2+3+4+5+6+7+8+9 = 44)")
    
    print("\nExecuting Range Update: Add 10 to indices [2, 6]...")
    sq.update_range(2, 6, 10)
    
    print("Executing New Query Sum[1, 8]:")
    ans = sq.query_range(1, 8)
    
    # Indices 2, 3, 4, 5, 6 were increased by 10 (Total +50).
    # 44 + 50 = 94.
    print(f"Result: {ans} (Expected: 44 + 50 = 94)")
    print("The O(sqrt N) array successfully handled lazy blocks and partial edges!")


def run_all_labs():
    demonstrate_sqrt_decomp()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference in Time Complexity between a Segment Tree and Square Root Decomposition?
   Answer: A Segment Tree answers queries and updates in strictly $O(\log N)$ time by traversing a binary tree height. Square Root Decomposition divides the array into chunks, answering queries in $O(\sqrt{N})$ time. Mathematically, $\log N$ is much faster than $\sqrt{N}$. However, a Segment Tree carries massive hidden constant factors (recursion overhead, cache misses across pointers). Sqrt Decomposition is purely iterative over a contiguous array, utilizing hardware CPU caching flawlessly. While theoretically slower, Sqrt Decomposition often runs blisteringly fast in reality and is significantly easier to write bug-free.

2. In the `update_range` function, explain the logic behind `block_lazy`. Why is it so powerful?
   Answer: Without `block_lazy`, if an update engulfed a block of 300 elements, you would be forced to loop 300 times to physically add the value to each element. `block_lazy` abstracts this mathematically. If the update perfectly engulfs Block $B$, we simply add the value to `block_lazy[B]` in exactly $O(1)$ time! We don't touch the 300 elements! We also instantly update `block_sum[B] += value * 300`. Later, if a query touches that block, we simply return the precalculated `block_sum`. If a query *partially* touches the block, we loop through the raw elements, adding `arr[i] + block_lazy[B]` on the fly. It is the epitome of doing zero work until absolutely necessary.

3. Why do we explicitly check `if start_block == end_block:` before processing the Left/Middle/Right segments?
   Answer: Edge Case collision! If $L = 2$ and $R = 4$, and the block size is $10$, both $L$ and $R$ sit inside Block $0$. If we didn't check this, the logic would trigger "Left Partial Block" (updating from $L$ to the end of the block... which overshoots $R$!), and then trigger "Right Partial Block", catastrophically double-counting elements and corrupting memory out of bounds. If $L$ and $R$ share the exact same block, the query is purely a local loop `from L to R`. Bypassing the macro-block logic perfectly isolates this edge case.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Topics (Sqrt Decomposition) Completed.")
