"""
# ==============================================================================
# LABORATORY: FENWICK TREES (BINARY INDEXED TREES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You just learned that Segment Trees achieve O(log N) Range Queries and Point 
# Updates. But Segment Trees use `4 * N` memory and require a lot of code (recursive 
# DFS). 
# A Fenwick Tree (or Binary Indexed Tree) solves the EXACT same problem, but uses 
# exactly `N + 1` memory, requires zero recursion, and can be implemented in 
# about 5 lines of code using Bitwise operations! It is the absolute optimal 
# solution for prefix sums in competitive programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Two's Complement bitwise trick: `index & -index`.
# - Implement a Fenwick Tree for O(log N) updates.
# - Implement a Fenwick Tree for O(log N) prefix sums.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BITWISE OPERATIONS OVERVIEW
# ==============================================================================
def demonstrate_lsb_trick():
    """
    The entire Fenwick tree relies on finding the Lowest Significant Bit (LSB).
    In Two's Complement arithmetic, `-x` is calculated by flipping all bits of `x` 
    and adding 1. 
    Therefore, `x & -x` mathematically isolates the lowest set bit!
    """
    section_header("The Bitwise Magic: x & -x")
    
    # 10 in binary is 1010
    # The lowest set bit is the 2nd bit (value = 2)
    x = 10
    lsb = x & -x
    
    print(f"Number: {x} (Binary: {bin(x)})")
    print(f"Isolating lowest set bit: x & -x = {lsb} (Binary: {bin(lsb)})")
    print("\nThis operation tells the Fenwick Tree exactly how far to jump up")
    print("or down the array during updates and queries.")


# ==============================================================================
# 4. FENWICK TREE IMPLEMENTATION
# ==============================================================================
class FenwickTree:
    """
    Also known as a Binary Indexed Tree (BIT).
    Note: Fenwick trees are strictly 1-indexed. The array size is N + 1.
    """
    def __init__(self, size: int):
        self.size = size
        # 1-indexed array of size N + 1
        self.tree = [0] * (size + 1)
        
    def add(self, index: int, delta: int) -> None:
        """
        Adds `delta` to the element at `index`. (O(log N))
        It then updates all the "parent" ranges that cover this index.
        To find the parent, we ADD the LSB: `index += index & -index`
        """
        # Fenwick trees are 1-indexed. If user passes 0, it causes an infinite loop.
        # So we usually assume the user passes a 1-based index, or we increment it.
        # Let's assume `index` is 1-based.
        while index <= self.size:
            self.tree[index] += delta
            # Jump to the next responsible node
            index += index & -index
            
    def prefix_sum(self, index: int) -> int:
        """
        Calculates the sum of elements from index 1 to `index`. (O(log N))
        To calculate the sum, we subtract the LSB to traverse the ranges:
        `index -= index & -index`
        """
        total = 0
        while index > 0:
            total += self.tree[index]
            # Jump to the previous responsible node
            index -= index & -index
        return total
        
    def range_sum(self, left: int, right: int) -> int:
        """
        Calculates the sum between left and right inclusive. (O(log N))
        Just like standard prefix sums: sum[L, R] = prefix_sum(R) - prefix_sum(L-1).
        """
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

def demonstrate_fenwick():
    section_header("Algorithm: Fenwick Tree (Binary Indexed Tree)")
    
    # We want to represent this data: [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    # Let's assume 1-based indexing for the input data to match the tree.
    data = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    n = len(data)
    
    ft = FenwickTree(n)
    
    # 1. Build the tree (O(N log N) by doing N updates)
    # (Note: There is an O(N) build method, but N log N is usually fine)
    print("Building Fenwick Tree...")
    for i, val in enumerate(data):
        # enumerate starts at 0, Fenwick needs 1-based
        ft.add(i + 1, val)
        
    print(f"Data: {data}")
    
    # 2. Query Prefix Sum
    print("\nQuerying Prefix Sum up to index 5 (1-based)...")
    # Sum of [3, 2, -1, 6, 5] = 15
    print(f"Result: {ft.prefix_sum(5)} (Expected: 15)")
    
    # 3. Query Range Sum
    print("\nQuerying Range Sum from index 2 to index 6 (1-based)...")
    # Sum of [2, -1, 6, 5, 4] = 16
    print(f"Result: {ft.range_sum(2, 6)} (Expected: 16)")
    
    # 4. Point Update
    print("\nAdding 10 to index 4 (Value was 6, becomes 16)...")
    # Data is now: [3, 2, -1, 16, 5, 4, -3, 3, 7, 2, 3]
    ft.add(4, 10)
    
    print("Querying Range Sum from index 2 to 6 again...")
    # Sum of [2, -1, 16, 5, 4] = 26
    print(f"Result: {ft.range_sum(2, 6)} (Expected: 26)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `x & -x` important?
   Answer: It mathematically isolates the lowest set bit of a number. In a Fenwick tree, adding this value to the current index jumps to the "parent" node responsible for the range. Subtracting it jumps backwards through the sequence of ranges that form the prefix sum.

2. Segment Tree vs Fenwick Tree. Which is better?
   Answer: Fenwick trees are better for memory (O(N) vs O(4N)) and are incredibly easy to code using bitwise operators. However, Fenwick trees primarily only work for invertible operations (like Addition, where you can subtract to get a range). Segment Trees can easily handle non-invertible operations (like finding the Maximum or Minimum of a range).

3. Why is a Fenwick tree always 1-indexed?
   Answer: Because the LSB of 0 is 0. If you try to add or subtract the LSB from index 0, it stays 0, causing an infinite `while` loop. The bitwise logic inherently requires starting at 1.
"""

if __name__ == "__main__":
    demonstrate_lsb_trick()
    demonstrate_fenwick()
    print("\n[SUCCESS] Laboratory: Fenwick Trees Completed.")
