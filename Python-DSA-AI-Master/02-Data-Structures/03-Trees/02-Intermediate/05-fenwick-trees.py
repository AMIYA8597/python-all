"""
## A. Concept Name
Fenwick Tree (Binary Indexed Tree)

## B. Core Idea
A data structure that provides efficient methods for calculation and manipulation of prefix sums in an array of numbers.

## C. Key Properties
- It implicitly represents a tree in a flat array.
- Relies heavily on bitwise operations (specifically the lowest set bit).
- Typically uses 1-based indexing for the bitwise logic to operate correctly.

## D. Real-World Analogy
Consider a financial dashboard that needs to query the total expenses from January to the current month. Instead of summing each month individually every time or recalculating all subsequent prefix sums upon a past month's correction, a Fenwick Tree updates only a specific chain of cumulative totals, balancing update and query times.

## E. Common Applications
- Calculating and querying prefix sums efficiently.
- Tracking frequencies or cumulative counts in data streams.
- Finding inversion counts in an array.

## F. Time & Space Complexity
- Time Complexity: O(log n) for queries and O(log n) for point updates. O(n) for building from an array using the linear method.
- Space Complexity: O(n) to store the underlying tree array explicitly.

## G. Basic Operations
- `update(index, delta)`: Adds `delta` to the element at the 1-based `index` and propagates the change.
- `query(index)`: Computes the sum from the first element up to the 1-based `index`.
- `range_query(left, right)`: Computes the sum in the inclusive range `[left, right]`.

## H. Implementation Details
The lowest set bit (LSB) isolates the segment size each index is responsible for. It can be computed using `index & (-index)`.
- During `query(index)`, we remove the lowest set bit to traverse up the prefix intervals: `index -= index & (-index)`.
- During `update(index, delta)`, we add the lowest set bit to traverse up to nodes that contain this index: `index += index & (-index)`.

## I. Code Example
The complete `FenwickTree` implementation in Python is provided in the module below, including a linear-time build method `from_array`.

## J. Common Pitfalls
- Using 0-based indexing which causes an infinite loop because `0 & (-0)` is 0.
- Misunderstanding that `update` applies a `delta` (addition/subtraction), not an absolute assignment of a new value.
- Forgetting to offset input indices by 1 when interfacing with 0-based application arrays.

## K. Best Practices
- Consistently use 1-based indexing inside the class.
- When creating the tree, size the internal array to `n + 1`.
- Expose a 0-based interface to the outside if needed, wrapping the +1 logic inside the methods.

## L. Advanced Variations
- Range Updates with Point Queries.
- Range Updates with Range Queries (requires two Fenwick Trees).
- 2D or Multi-dimensional Fenwick Trees for grid-based prefix sums.

## M. Related Concepts
- Segment Trees (more versatile, can do arbitrary range queries like Min/Max but require more space/code).
- Prefix Sum Arrays (O(1) queries but O(n) updates).
- Lowest Set Bit (Bit Manipulation).

## N. Practice Problems
- LeetCode 307: Range Sum Query - Mutable
- LeetCode 315: Count of Smaller Numbers After Self
- SPOJ INVCNT: Inversion Count

## O. Interview Questions
- "How can you compute prefix sums dynamically if the array elements are continuously being updated?"
- "Explain the difference in space and constant-factor time overhead between Fenwick Trees and Segment Trees."

## P. Debugging Tips
- Check your bounds. Is `index > 0` and `index <= size`?
- Print the bitwise progression for an index to ensure it behaves correctly (e.g., `3 -> 4 -> 8`).
- Verify that your initial array elements were correctly populated, either via `O(n log n)` repeated updates or `O(n)` bottom-up propagation.

## Q. Visualization
Index `12` (binary `1100`) stores the sum of elements from index `9` to `12`.
To get the prefix sum of `12`, we take `tree[12]` and then query `12 - 4 = 8`.
Then `tree[8]` (binary `1000`) stores the sum from `1` to `8`.
So `query(12)` = `tree[12] + tree[8]`.

## R. Historical Context
Also known as the Binary Indexed Tree (BIT), it was proposed by Peter Fenwick in 1994, originally for improving data compression algorithms (arithmetic coding) where dynamic cumulative frequency tables were heavily used.

## S. Alternative Approaches
- Segment Trees: Provide broader applicability (like min, max, gcd) at the cost of being slightly slower and using 2-4x more memory.
- Square Root Decomposition: O(sqrt(n)) updates and queries, which is conceptually simpler but slower than O(log n).

## T. Pros & Cons
- **Pros:** Minimal memory footprint (exactly `n+1` array), very short and easy to implement, low constant-factor overhead.
- **Cons:** Less flexible than Segment Trees (difficult to query for non-invertible operations like `max` or `min`).

## U. Optimization Techniques
- **Linear-Time Construction:** Instead of inserting elements one by one (`O(n log n)`), we can initialize the array and ripple values up to their direct parent in `O(n)` time (implemented in `from_array` below).

## V. Language Specifics
- In Python, negative numbers in bitwise operations `(-index)` behave identically to two's complement in languages like C/C++ due to Python's infinite-precision integer abstraction, making `index & (-index)` perfectly safe and correct.

## W. Quick Review
- **Query (Sum down):** `index -= index & (-index)`
- **Update (Propagate up):** `index += index & (-index)`
- Keep it 1-based!

## X. Project Connection
In AI or Data Science pipelines, Fenwick Trees can efficiently maintain dynamic histograms or running frequency distributions for streaming data. In competitive programming, it is a staple structure for inversion counting and dynamic querying without incurring the heavy implementation cost of full Segment Trees.
"""

from typing import List

class FenwickTree:
    """Implementation of a Fenwick Tree (Binary Indexed Tree) for Prefix Sums."""
    
    def __init__(self, size: int):
        # 1-based indexing is preferred for Fenwick trees
        self.tree = [0] * (size + 1)
        self.size = size

    @classmethod
    def from_array(cls, arr: List[int]) -> 'FenwickTree':
        """Advanced: Build tree in O(n) instead of O(n log n)."""
        ft = cls(len(arr))
        for i in range(1, len(arr) + 1):
            ft.tree[i] += arr[i - 1]
            parent = i + (i & -i)
            if parent <= ft.size:
                ft.tree[parent] += ft.tree[i]
        return ft

    def update(self, index: int, delta: int):
        """Adds delta to element at index (1-based)."""
        while index <= self.size:
            self.tree[index] += delta
            # Add lowest set bit
            index += index & (-index)

    def query(self, index: int) -> int:
        """Returns sum of elements from 1 to index (1-based)."""
        total = 0
        while index > 0:
            total += self.tree[index]
            # Remove lowest set bit
            index -= index & (-index)
        return total

    def range_query(self, left: int, right: int) -> int:
        """Returns sum of elements from left to right (inclusive, 1-based)."""
        if left > right:
            return 0
        return self.query(right) - self.query(left - 1)

def test_fenwick_tree():
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    ft = FenwickTree.from_array(arr)
    
    # Prefix sum up to index 5 (3 + 2 + -1 + 6 + 5 = 15)
    assert ft.query(5) == 15
    
    # Range sum from index 2 to 6 (2 + -1 + 6 + 5 + 4 = 16)
    assert ft.range_query(2, 6) == 16
    
    # Update element at index 3 by adding 2 (making it 1)
    ft.update(3, 2)
    assert ft.query(5) == 17
    assert ft.range_query(2, 6) == 18

    print("Fenwick Tree basic tests passed!")

if __name__ == "__main__":
    test_fenwick_tree()
