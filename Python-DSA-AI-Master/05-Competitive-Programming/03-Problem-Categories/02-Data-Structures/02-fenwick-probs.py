"""
Competitive Programming Problems: Fenwick Tree (Binary Indexed Tree)
====================================================================

Overview:
---------
A Fenwick Tree, or Binary Indexed Tree (BIT), is a data structure providing efficient methods 
for calculation and manipulation of the prefix sums of a table of values. 
It requires less space (O(N)) and is easier/shorter to code than a Segment Tree, while achieving 
the same time complexity for point updates and prefix queries (O(log N)).

Learning Objectives:
--------------------
1. Understand the concept of "Least Significant Bit" (LSB) extraction: `x & (-x)`.
2. Implement Point Update and Prefix Query operations.
3. Learn how to convert Range Queries to Prefix Queries.
4. Compare and contrast Fenwick Trees with Segment Trees.

Industry Use Cases:
-------------------
- Compression Algorithms: Arithmetic coding relies heavily on dynamic frequency tables 
  where rapid updates and cumulative frequency queries are required.
- Load Balancing: Managing priority queues or probabilistic trees where weights need dynamic 
  adjustments.
- Interview Problems: "Count Inversions", "Number of elements smaller than X to the right", etc.

Beginner to Advanced Explanations:
----------------------------------
- Basic: A BIT maintains prefix sums based on binary representation. 
  Every integer can be represented as a sum of powers of 2. In a BIT, the element at index `i` 
  is responsible for a range of elements. The size of this range is exactly the Least Significant Bit (LSB) of `i`.
- Advanced: 
  To get the LSB of `x`, we use the two's complement property: `LSB(x) = x & (-x)`.
  - When querying the sum up to `i`, we repeatedly remove the LSB: `i -= i & (-x)` until `i` is 0.
  - When updating at `i`, we repeatedly ADD the LSB: `i += i & (-x)` to update all nodes 
    responsible for `i`.
  - Note: Fenwick trees are strictly 1-indexed. Index 0 is not used because `0 & (-0) = 0`, 
    causing an infinite loop.

Performance & Space Considerations:
-----------------------------------
- Space: Exactly O(N) array size (Segment trees take O(4*N)).
- Time: Very fast constant factors. Bitwise operations run incredibly fast on modern CPUs.
- Limitation: Standard BIT cannot easily answer Range Min/Max queries (unlike Segment Trees).
"""

from typing import List

class FenwickTree:
    """
    A professional-grade Fenwick Tree (BIT) for point updates and range sum queries.
    
    Time Complexity:
    - Build: O(N log N) with point updates, or O(N) using the linear build algorithm.
    - Update: O(log N)
    - Query: O(log N)
    Space Complexity: O(N)
    """
    
    def __init__(self, size: int):
        """Initializes an empty BIT of a given size. Note: 1-indexed internally."""
        # We allocate size + 1 because BIT is 1-indexed
        self.size = size
        self.tree = [0] * (self.size + 1)

    @classmethod
    def build_linear(cls, arr: List[int]) -> 'FenwickTree':
        """
        Builds the BIT in O(N) time instead of O(N log N).
        This is an advanced optimization preferred in high-end competitive programming.
        """
        n = len(arr)
        bit = cls(n)
        
        # 1-based indexing copy
        for i in range(1, n + 1):
            bit.tree[i] = arr[i - 1]
            
        # Add current node's value to its immediate parent in the BIT hierarchy
        for i in range(1, n + 1):
            parent_idx = i + (i & -i)
            if parent_idx <= n:
                bit.tree[parent_idx] += bit.tree[i]
                
        return bit

    def add(self, index: int, delta: int) -> None:
        """
        Adds 'delta' to the element at 'index' (0-indexed externally, mapped to 1-indexed).
        Updates all ranges in the BIT that cover this element.
        """
        # Convert to 1-based index
        i = index + 1
        while i <= self.size:
            self.tree[i] += delta
            # Move to the next responsible node by adding LSB
            i += i & (-i)

    def prefix_sum(self, index: int) -> int:
        """
        Returns the sum of elements from index 0 to 'index' (inclusive, 0-based).
        """
        # Convert to 1-based index
        i = index + 1
        total = 0
        while i > 0:
            total += self.tree[i]
            # Move to the parent node by subtracting LSB
            i -= i & (-i)
        return total

    def range_query(self, left: int, right: int) -> int:
        """
        Returns the sum of elements in the range [left, right] (0-based indices).
        """
        if left > right:
            return 0
        if left == 0:
            return self.prefix_sum(right)
        
        # Sum(L, R) = Sum(0, R) - Sum(0, L-1)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


# =============================================================================
# Practical Application: Count Inversions
# =============================================================================
def count_inversions(arr: List[int]) -> int:
    """
    Counts the number of inversions in an array using a Fenwick Tree.
    An inversion is a pair (i, j) where i < j and arr[i] > arr[j].
    
    Time Complexity: O(N log(Max_Val))
    Space Complexity: O(Max_Val)
    """
    if not arr:
        return 0
        
    # Find the maximum element to determine BIT size
    # (In a real scenario with large numbers, we would use Coordinate Compression here)
    max_val = max(arr)
    bit = FenwickTree(max_val)
    
    inversions = 0
    # Traverse from right to left
    for num in reversed(arr):
        # Count elements strictly smaller than 'num' that we have seen so far
        # 'num' is 1-indexed natively if we assume values > 0. 
        # But our FenwickTree wrapper handles 0-indexing mapping cleanly.
        if num - 1 >= 0:
            inversions += bit.prefix_sum(num - 1)
        
        # Add current element to the BIT
        bit.add(num, 1)
        
    return inversions


# =============================================================================
# Tests and Main Guard
# =============================================================================
if __name__ == "__main__":
    print("Running Tests for Fenwick Tree (BIT)...\n")
    
    # 1. Test basic operations and linear build
    arr = [2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Initial array: {arr}")
    
    bit = FenwickTree.build_linear(arr)
    
    # Query range [2, 5] -> elements: 1, 3, 2, 3 -> Sum = 9
    assert bit.range_query(2, 5) == 9
    print(f"Range sum [2, 5] -> Expected: 9, Got: {bit.range_query(2, 5)}")
    
    # Add 5 to index 3 (value becomes 8). Array conceptual: [2, 1, 1, 8, 2, 3, 4, 5, ...]
    bit.add(3, 5)
    
    # Query range [2, 5] again -> elements: 1, 8, 2, 3 -> Sum = 14
    new_sum = bit.range_query(2, 5)
    assert new_sum == 14
    print(f"Range sum [2, 5] after adding 5 at index 3 -> Expected: 14, Got: {new_sum}")
    
    # 2. Test Count Inversions
    # Inversions in [8, 4, 2, 1] are (8,4), (8,2), (8,1), (4,2), (4,1), (2,1) = 6
    inv_arr = [8, 4, 2, 1]
    inv_count = count_inversions(inv_arr)
    assert inv_count == 6
    print(f"\nInversions in {inv_arr} -> Expected: 6, Got: {inv_count}")

    print("\nAll tests passed successfully! 🚀")

"""
Interview Challenge:
--------------------
Problem: "Range Update & Point Query"
We've seen Point Update and Range Query. But what if we need to do:
1. Add `val` to all elements from `L` to `R`.
2. Find the value of a specific element at index `i`.

Hint: You can use a standard Fenwick Tree (which calculates prefix sums) over an array of DIFFERENCES.
If you have an array `D` initialized to 0. 
To add `V` to range `[L, R]`, do `BIT.add(L, V)` and `BIT.add(R + 1, -V)`.
To get the value at index `i`, you simply query the prefix sum up to `i`: `BIT.prefix_sum(i)`.
The prefix sum will perfectly account for the overlapping additions!
"""
