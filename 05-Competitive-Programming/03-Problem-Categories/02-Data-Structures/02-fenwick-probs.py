"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (FENWICK TREES / BIT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Segment Tree is the ultimate weapon for Range Queries, but it takes 50 lines 
# of recursive code to write, and requires O(4*N) memory.
#
# In a high-speed contest, if a problem ONLY requires Point Updates and Range 
# Prefix Sums, a Segment Tree is complete overkill.
#
# You should use a Fenwick Tree (Binary Indexed Tree).
# A Fenwick Tree achieves the exact same O(log N) Time Complexity for updates 
# and queries, but it requires exactly O(N) memory, and the entire algorithm 
# can be written in 10 lines of code using purely Bitwise Operations!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Bitwise architecture of a Fenwick Tree (`x & -x`).
# - Implement the `add()` and `query()` functions in 5 lines each.
# - Solve a Point-Update / Range-Sum problem.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FENWICK TREE ARCHITECTURE
# ==============================================================================
class FenwickTree:
    """
    A 1-indexed Binary Indexed Tree for Point Updates and Range Prefix Sums.
    Space Complexity: O(N)
    Time Complexity: O(log N) for Queries and Updates.
    """
    def __init__(self, size: int):
        # Fenwick Trees are STRICTLY 1-indexed.
        # Index 0 is a dummy node and is mathematically ignored.
        self.n = size
        self.tree = [0] * (self.n + 1)
        
    def add(self, i: int, delta: int) -> None:
        """
        Adds `delta` to element at index `i` (1-indexed).
        Updates all subsequent nodes in the tree that are "responsible" for `i`.
        """
        while i <= self.n:
            self.tree[i] += delta
            # BITWISE MAGIC: Extract the lowest set bit, and ADD it to the index
            # This mathematically hops to the "parent" node in the Fenwick hierarchy!
            i += i & (-i)
            
    def query_prefix(self, i: int) -> int:
        """
        Calculates the sum of all elements from index 1 to `i`.
        """
        total = 0
        while i > 0:
            total += self.tree[i]
            # BITWISE MAGIC: Extract the lowest set bit, and SUBTRACT it
            # This mathematically hops back, skipping over ranges we already summed!
            i -= i & (-i)
        return total
        
    def query_range(self, left: int, right: int) -> int:
        """
        Calculates the sum from `left` to `right` using Prefix Math!
        Sum(L to R) = PrefixSum(R) - PrefixSum(L - 1)
        """
        return self.query_prefix(right) - self.query_prefix(left - 1)


# ==============================================================================
# 4. EXECUTING THE FENWICK TREE
# ==============================================================================
def demonstrate_fenwick():
    section_header("Executing a Fenwick Tree")
    
    # Raw 0-indexed array
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    print(f"Original Array: {arr}")
    
    # 1. Initialize the Tree
    n = len(arr)
    bit = FenwickTree(n)
    
    # 2. Build the Tree
    # A Fenwick tree is built by calling `add` on every single element.
    # Time to build: N * O(log N) = O(N log N)
    # (Note: There is an O(N) build trick, but O(N log N) is standard for contests)
    for idx, val in enumerate(arr):
        # bit.add requires 1-indexed arrays! So we pass idx + 1.
        bit.add(idx + 1, val)
        
    print("Fenwick Tree built successfully.")
    
    # 3. Range Query
    # Query sum from indices 2 to 6 (0-indexed).
    # In 1-indexed math, this is left=3, right=7.
    # Sum: -1 + 6 + 5 + 4 + -3 = 11
    l, r = 3, 7
    result = bit.query_range(l, r)
    print(f"\nQuery Sum (1-indexed) [{l} to {r}]: {result}")
    
    # 4. Point Update
    # Update index 4 (0-indexed) from 5 to 10. (A delta of +5)
    # In 1-indexed math, we update index 5 with delta +5.
    update_idx = 5
    delta = +5
    print(f"\nUpdating 1-indexed {update_idx} with a delta of {delta}...")
    bit.add(update_idx, delta)
    
    # Query again
    result2 = bit.query_range(l, r)
    print(f"Query Sum (1-indexed) [{l} to {r}] after update: {result2}")
    
    print("\nNotice how the entire algorithm is less than 15 lines of code, ")
    print("compared to the 50+ lines of a Segment Tree!")


def run_all_labs():
    demonstrate_fenwick()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the bitwise magic trick `i & (-i)`. What does it mathematically achieve in a Fenwick Tree?
   Answer: In a computer, `-i` is calculated using Two's Complement (flip all bits, add 1). If you take a binary number (like $12$, which is `1100`) and perform a bitwise AND with its negative (`12 & -12`), the math mathematically isolates the Lowest Set Bit (the rightmost `1`). For `1100`, the lowest set bit is `0100` (which is $4$). A Fenwick Tree relies entirely on this isolation. When jumping backwards during a query, subtracting the lowest set bit (`i -= i & (-i)`) perfectly traverses the array chunks in exactly $O(\log N)$ hops.

2. A Segment Tree uses $O(4 \times N)$ space, but a Fenwick Tree uses exactly $O(N)$ space. How does a Fenwick Tree store a tree structure inside a flat array without allocating extra nodes for the parents?
   Answer: A Segment Tree builds an explicit, physical Binary Tree where parent nodes are stored in separate array indices. A Fenwick Tree does not build an explicit tree; it maps the "tree" dynamically over the physical indices of the original array using binary arithmetic. The node at index $8$ (`1000`) mathematically "owns" the sum of indices 1 through 8. The node at index $6$ (`0110`) owns the sum of indices 5 and 6. Because every physical index mathematically encodes its own hierarchical range using its binary bits, there are zero "parent nodes" to store, resulting in perfect $O(N)$ Space Complexity.

3. If Fenwick Trees are shorter to code and use less memory than Segment Trees, why would you ever use a Segment Tree?
   Answer: Flexibility. A Fenwick Tree relies on the mathematical concept of an "Inverse Operation" to calculate Range Queries. To find the sum of $[L, R]$, it calculates $PrefixSum(R) - PrefixSum(L-1)$. It uses Subtraction to cancel out the left side. What if the problem asks for the "Range Minimum"? The Minimum function does *not* have an inverse (you cannot "subtract" a minimum). Because Fenwick Trees strictly require inversions for arbitrary range queries, they completely fail at Range Minimum/Maximum problems. A Segment Tree does not rely on prefix inversion; it traverses strict geometric bounds, meaning it can easily handle Sum, Minimum, Maximum, GCD, and LCM.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Fenwick Trees Completed.")
