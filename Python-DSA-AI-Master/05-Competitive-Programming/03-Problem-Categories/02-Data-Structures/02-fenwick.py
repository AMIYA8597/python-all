"""
================================================================================
Fenwick Tree (Binary Indexed Tree) - Comprehensive Interactive Lesson
================================================================================

1. INTRODUCTION & MATHEMATICAL BACKGROUND
--------------------------------------------------------------------------------
A Fenwick Tree (or Binary Indexed Tree, BIT) is an elegant data structure that 
can efficiently update elements and calculate prefix sums in an array of numbers.
Proposed by Peter Fenwick in 1994, it was originally developed for data 
compression algorithms (arithmetic coding), but has since become a staple in 
competitive programming and real-time data processing.

The core philosophy of a Fenwick Tree relies on the binary representation of 
numbers. Every integer can be represented as a sum of distinct powers of two. 
Similarly, in a Fenwick Tree, every cumulative sum of a prefix can be represented 
as a sum of non-overlapping sub-arrays.

Let LSB(i) be the Least Significant Bit of `i`. 
Mathematically, LSB(i) = i & (-i) in two's complement representation.

For an index `i`, the Fenwick tree node `tree[i]` stores the sum of the original 
array `A` in the range `[i - LSB(i) + 1, i]`.
For example:
- `tree[12]` (1100 in binary): LSB(12) = 4. Range = [12 - 4 + 1, 12] = [9, 12].
- `tree[10]` (1010 in binary): LSB(10) = 2. Range = [10 - 2 + 1, 10] = [9, 10].
- `tree[8]`  (1000 in binary): LSB(8) = 8. Range = [8 - 8 + 1, 8] = [1, 8].

By leveraging this, we can perform both prefix sum queries and point updates 
in O(log N) time, whereas a standard array requires O(N) for prefix sums (if 
updates are O(1)) or O(N) for updates (if prefix sums are O(1) via a precomputed 
array).

2. BIG-O COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------
- Space Complexity: O(N)
- Build Time (Naïve via updates): O(N log N)
- Build Time (Optimized linear): O(N)
- Point Update: O(log N)
- Prefix Sum Query: O(log N)
- Range Sum Query: O(log N)

3. WHY 1-BASED INDEXING?
--------------------------------------------------------------------------------
The bitwise trick `i & (-i)` works perfectly for 1-based indexing. If we used 
0-based indexing, LSB(0) = 0 & -0 = 0. Adding 0 to 0 results in an infinite 
loop during updates. Thus, the underlying array is padded with a dummy 0th element.

4. ADVANCED VARIATIONS
--------------------------------------------------------------------------------
While standard Fenwick trees support Point Update and Range Query (PURQ), we can
extend the math to support:
- Range Update and Point Query (RUPQ)
- Range Update and Range Query (RURQ)
- 2D/Multi-dimensional Fenwick Trees

5. COMPARISON: FENWICK TREE VS. SEGMENT TREE
--------------------------------------------------------------------------------
- Code Complexity: Fenwick Trees are very short (10-15 lines) vs Segment Trees.
- Memory: Fenwick uses exactly O(N) memory. Segment Trees often use O(4N).
- Speed: Fenwick Trees have much smaller constant factors (faster in practice).
- Flexibility: Segment Trees can easily maintain Min/Max, GCD, string hashes, etc.
  Fenwick Trees primarily handle operations with an inverse (like addition). 
  (Min/Max in Fenwick is possible but restricted and complex).

Let's dive into the textbook-grade implementations!
"""

import math
from typing import List, Iterable

# ==============================================================================
# I. Basic Fenwick Tree: Point Update, Range Query (PURQ)
# ==============================================================================

class FenwickTreePURQ:
    """
    Standard Fenwick Tree: Point Update, Range Query.
    Maintains a 1-based array internally but provides a clear interface.
    """
    def __init__(self, size: int):
        """
        Initializes an empty Fenwick Tree of a given size.
        O(N) space, O(N) initialization time.
        """
        self.size = size
        # 1-indexed, so we allocate size + 1
        self.tree: List[int] = [0] * (size + 1)
        
    @classmethod
    def from_array(cls, arr: Iterable[int]) -> 'FenwickTreePURQ':
        """
        Constructs a Fenwick Tree from an existing array in O(N) time.
        This is an optimization over calling add() N times (which takes O(N log N)).
        
        Mathematical reasoning:
        Every node i contributes to its immediate parent i + LSB(i).
        We can just propagate the current node's value to its parent directly
        during a single linear pass.
        """
        array = list(arr)
        size = len(array)
        fenwick = cls(size)
        
        # 1-based array copy
        for i in range(size):
            fenwick.tree[i + 1] = array[i]
            
        # Linear construction: O(N)
        for i in range(1, size + 1):
            parent = i + (i & (-i))
            if parent <= size:
                fenwick.tree[parent] += fenwick.tree[i]
                
        return fenwick

    def add(self, index: int, delta: int) -> None:
        """
        Adds `delta` to the element at `index` (1-based).
        Time Complexity: O(log N)
        
        How it works:
        To update index i, we must also update all nodes in the tree that enclose
        index i in their range. We find the next enclosing range by adding the
        Least Significant Bit (LSB).
        """
        if index <= 0 or index > self.size:
            raise IndexError("Index out of bounds for 1-based Fenwick Tree.")
            
        while index <= self.size:
            self.tree[index] += delta
            # Move to the next node that is responsible for our current index
            index += index & (-index)

    def query_prefix(self, index: int) -> int:
        """
        Calculates the sum of elements from 1 to `index` (1-based).
        Time Complexity: O(log N)
        
        How it works:
        To get the prefix sum up to i, we add the value at node i, and then
        move to the node that represents the prefix immediately preceding the
        range of i. We do this by subtracting the LSB.
        """
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds for 1-based Fenwick Tree.")
            
        prefix_sum = 0
        while index > 0:
            prefix_sum += self.tree[index]
            # Strip the least significant bit
            index -= index & (-index)
        return prefix_sum

    def query_range(self, left: int, right: int) -> int:
        """
        Calculates the sum of elements in the range [left, right] (1-based, inclusive).
        Time Complexity: O(log N)
        """
        if left > right:
            return 0
        return self.query_prefix(right) - self.query_prefix(left - 1)
        
    def find_kth_smallest(self, k: int) -> int:
        """
        If the Fenwick tree is used as a frequency map, this finds the index
        of the k-th smallest element.
        Time Complexity: O(log N) via binary lifting.
        """
        index = 0
        bit_mask = 1 << int(math.log2(self.size))
        
        while bit_mask > 0:
            next_index = index + bit_mask
            # If next_index is valid and its cumulative frequency is less than k
            if next_index <= self.size and self.tree[next_index] < k:
                index = next_index
                k -= self.tree[index]
            bit_mask >>= 1
            
        return index + 1


# ==============================================================================
# II. Range Update, Point Query (RUPQ)
# ==============================================================================

class FenwickTreeRUPQ:
    """
    Fenwick Tree for Range Updates and Point Queries.
    
    Trick: Instead of storing the array elements, we store the DIFFERENCE array.
    If we want to add `V` to range [L, R], we:
    - Add `V` at index `L`.
    - Subtract `V` at index `R + 1`.
    Then, to find the value at index `i`, we just compute the prefix sum up to `i`.
    """
    def __init__(self, size: int):
        self.purq = FenwickTreePURQ(size)
        
    def range_add(self, left: int, right: int, delta: int) -> None:
        """
        Adds `delta` to all elements in the range [left, right] (1-based).
        Time Complexity: O(log N)
        """
        self.purq.add(left, delta)
        # Avoid out-of-bounds error if right == size
        if right + 1 <= self.purq.size:
            self.purq.add(right + 1, -delta)
            
    def point_query(self, index: int) -> int:
        """
        Returns the value of the element at `index` (1-based).
        Time Complexity: O(log N)
        """
        return self.purq.query_prefix(index)


# ==============================================================================
# III. Range Update, Range Query (RURQ)
# ==============================================================================

class FenwickTreeRURQ:
    """
    Fenwick Tree for Range Updates and Range Queries.
    
    Mathematical Derivation:
    Consider the difference array D used in RUPQ. 
    The value at index i is: A[i] = D[1] + D[2] + ... + D[i]
    
    The prefix sum S[p] = sum_{i=1 to p} A[i]
    S[p] = (D[1]) + (D[1]+D[2]) + (D[1]+D[2]+D[3]) + ... + (D[1]+...+D[p])
    Rearranging terms:
    S[p] = D[1]*p + D[2]*(p-1) + D[3]*(p-2) + ... + D[p]*1
    S[p] = sum_{i=1 to p} [ D[i] * (p - i + 1) ]
    S[p] = (p + 1) * sum_{i=1 to p} D[i] - sum_{i=1 to p} (D[i] * i)
    
    Thus, we can maintain two PURQ Fenwick Trees:
    1. B1 to maintain sum of D[i]
    2. B2 to maintain sum of D[i] * i
    """
    def __init__(self, size: int):
        self.size = size
        self.b1 = FenwickTreePURQ(size)
        self.b2 = FenwickTreePURQ(size)
        
    def range_add(self, left: int, right: int, delta: int) -> None:
        """
        Adds `delta` to all elements in [left, right].
        """
        self._add(self.b1, left, delta)
        self._add(self.b1, right + 1, -delta)
        
        self._add(self.b2, left, delta * (left - 1))
        self._add(self.b2, right + 1, -delta * right)
        
    def _add(self, b: FenwickTreePURQ, index: int, value: int) -> None:
        if index <= self.size:
            b.add(index, value)
            
    def prefix_query(self, index: int) -> int:
        """
        Returns the sum of elements from 1 to `index`.
        """
        return self.b1.query_prefix(index) * index - self.b2.query_prefix(index)
        
    def range_query(self, left: int, right: int) -> int:
        """
        Returns the sum of elements in [left, right].
        """
        return self.prefix_query(right) - self.prefix_query(left - 1)


# ==============================================================================
# IV. 2D Fenwick Tree
# ==============================================================================

class FenwickTree2D:
    """
    2D Fenwick Tree for Range Updates (point) and 2D Range Queries.
    Useful for matrix sub-grid sums (e.g., image processing or game maps).
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.tree = [[0] * (cols + 1) for _ in range(rows + 1)]
        
    def add(self, r: int, c: int, delta: int) -> None:
        """
        Adds `delta` to matrix[r][c] (1-based indices).
        Time Complexity: O(log(R) * log(C))
        """
        i = r
        while i <= self.rows:
            j = c
            while j <= self.cols:
                self.tree[i][j] += delta
                j += j & (-j)
            i += i & (-i)
            
    def query_prefix(self, r: int, c: int) -> int:
        """
        Sum of elements in the rectangle from (1,1) to (r,c).
        """
        total = 0
        i = r
        while i > 0:
            j = c
            while j > 0:
                total += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return total
        
    def query_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """
        Sum of elements in the rectangle (r1, c1) to (r2, c2) inclusive.
        Uses 2D Inclusion-Exclusion principle.
        """
        return (self.query_prefix(r2, c2) 
              - self.query_prefix(r1 - 1, c2) 
              - self.query_prefix(r2, c1 - 1) 
              + self.query_prefix(r1 - 1, c1 - 1))


# ==============================================================================
# V. Practical Applications & Real-World Use Cases
# ==============================================================================

def count_inversions(arr: List[int]) -> int:
    """
    Counts the number of inversions in an array using a Fenwick Tree.
    An inversion is a pair (i, j) such that i < j and arr[i] > arr[j].
    
    Time Complexity: O(N log N) with Coordinate Compression.
    """
    # Coordinate Compression
    sorted_unique = sorted(list(set(arr)))
    rank = {val: i + 1 for i, val in enumerate(sorted_unique)}
    
    max_rank = len(sorted_unique)
    fenwick = FenwickTreePURQ(max_rank)
    
    inversions = 0
    # Process from right to left
    for num in reversed(arr):
        r = rank[num]
        # Count how many elements smaller than 'num' have been seen so far
        inversions += fenwick.query_prefix(r - 1)
        # Add the current element to the Fenwick Tree
        fenwick.add(r, 1)
        
    return inversions


# ==============================================================================
# VI. Interactive Textbook Test Suite
# ==============================================================================

def run_interactive_lesson_tests():
    print("="*60)
    print("🎓 FENWICK TREE (BINARY INDEXED TREE) INTERACTIVE LESSON 🎓")
    print("="*60)
    
    print("\n[1] Testing Standard PURQ (Point Update, Range Query)...")
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    print(f"Original Array: {arr}")
    
    # O(N) Construction
    ft = FenwickTreePURQ.from_array(arr)
    
    # Query prefix sum of first 5 elements (indices 1 to 5)
    # 3 + 2 - 1 + 6 + 5 = 15
    q1 = ft.query_prefix(5)
    print(f"Prefix Sum (1 to 5): Expected=15, Got={q1}")
    assert q1 == 15, "PURQ Prefix Sum Failed"
    
    # Range Query [3, 7]: -1 + 6 + 5 + 4 - 3 = 11
    q2 = ft.query_range(3, 7)
    print(f"Range Sum (3 to 7): Expected=11, Got={q2}")
    assert q2 == 11, "PURQ Range Query Failed"
    
    # Point Update: Add 2 to index 4 (value goes from 6 to 8)
    ft.add(4, 2)
    q3 = ft.query_range(3, 7)
    print(f"After adding 2 to index 4, Range Sum (3 to 7): Expected=13, Got={q3}")
    assert q3 == 13, "PURQ Point Update Failed"
    print("✅ PURQ Tests Passed!\n")
    
    print("[2] Testing Binary Lifting (Find k-th smallest)...")
    freq = FenwickTreePURQ(5)
    freq.add(1, 1) # One '1'
    freq.add(3, 2) # Two '3's
    freq.add(5, 1) # One '5'
    # Elements logically: {1, 3, 3, 5}
    kth = freq.find_kth_smallest(3)
    print(f"Logical Multi-set: {{1, 3, 3, 5}}")
    print(f"3rd smallest element: Expected=3, Got={kth}")
    assert kth == 3, "Binary Lifting Failed"
    print("✅ Binary Lifting Tests Passed!\n")
    
    print("[3] Testing RUPQ (Range Update, Point Query)...")
    rupq = FenwickTreeRUPQ(5)
    rupq.range_add(2, 4, 10)  # Array becomes: 0, 10, 10, 10, 0
    rupq.range_add(3, 5, 5)   # Array becomes: 0, 10, 15, 15, 5
    p1 = rupq.point_query(1)
    p2 = rupq.point_query(3)
    p3 = rupq.point_query(5)
    print(f"Values at indices 1, 3, 5: Got=({p1}, {p2}, {p3}), Expected=(0, 15, 5)")
    assert (p1, p2, p3) == (0, 15, 5), "RUPQ Failed"
    print("✅ RUPQ Tests Passed!\n")
    
    print("[4] Testing RURQ (Range Update, Range Query)...")
    rurq = FenwickTreeRURQ(5)
    rurq.range_add(1, 3, 5)   # Add 5 to [1,3]: 5, 5, 5, 0, 0
    rurq.range_add(2, 4, 3)   # Add 3 to [2,4]: 5, 8, 8, 3, 0
    q4 = rurq.range_query(2, 3) # Sum of indices 2, 3 = 8 + 8 = 16
    q5 = rurq.range_query(1, 5) # Sum all = 5 + 8 + 8 + 3 + 0 = 24
    print(f"Range Sum (2 to 3): Expected=16, Got={q4}")
    print(f"Range Sum (1 to 5): Expected=24, Got={q5}")
    assert q4 == 16 and q5 == 24, "RURQ Failed"
    print("✅ RURQ Tests Passed!\n")
    
    print("[5] Testing 2D Fenwick Tree...")
    ft2d = FenwickTree2D(4, 4)
    ft2d.add(2, 3, 5)
    ft2d.add(3, 3, 2)
    ft2d.add(4, 4, 10)
    q6 = ft2d.query_region(2, 2, 3, 4)
    print(f"2D Region Sum (2,2) to (3,4): Expected=7, Got={q6}")
    assert q6 == 7, "2D Fenwick Tree Failed"
    print("✅ 2D Fenwick Tree Tests Passed!\n")
    
    print("[6] Testing Real-World Application: Inversion Count...")
    arr2 = [8, 4, 2, 1]
    arr3 = [1, 20, 6, 4, 5]
    inv2 = count_inversions(arr2)
    inv3 = count_inversions(arr3)
    print(f"Inversions in {arr2}: Expected=6, Got={inv2}")
    print(f"Inversions in {arr3}: Expected=5, Got={inv3}")
    assert inv2 == 6 and inv3 == 5, "Inversion Count Failed"
    print("✅ Inversion Count Application Passed!\n")

    print("="*60)
    print("🚀 All Textbook Tests Successfully Executed! 🚀")
    print("="*60)

if __name__ == "__main__":
    run_interactive_lesson_tests()
