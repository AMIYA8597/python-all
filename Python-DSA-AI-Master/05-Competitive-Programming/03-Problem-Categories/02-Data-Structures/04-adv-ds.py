'''
================================================================================
Advanced Data Structures in Competitive Programming
================================================================================

Welcome to the "Python DSA Master" interactive lesson on Advanced Data Structures.

This module provides textbook-grade, production-ready implementations of the
most powerful advanced data structures used in competitive programming,
algorithmic interviews, and high-performance real-world systems.

Data Structures Covered:
1. Disjoint Set Union (DSU) / Union-Find
2. Fenwick Tree (Binary Indexed Tree / BIT)
3. Segment Tree (with Lazy Propagation)
4. Trie (Prefix Tree)

--------------------------------------------------------------------------------
Mathematical Background & Big-O Analysis
--------------------------------------------------------------------------------

1. Disjoint Set Union (DSU)
   - Purpose: Maintains a collection of disjoint dynamic sets.
   - Core Operations: Find (finds the representative of a set) and Union (merges two sets).
   - Mathematical Insight: The Inverse Ackermann function α(N) grows so slowly that
     for all practical values of N (even N = 2^65536), α(N) ≤ 5.
   - Time Complexity:
     - Find: O(α(N)) amortized
     - Union: O(α(N)) amortized
   - Space Complexity: O(N)

2. Fenwick Tree (Binary Indexed Tree)
   - Purpose: Efficiently updates elements and calculates prefix sums in an array of numbers.
   - Mathematical Insight: Any integer can be represented as sum of powers of 2.
     Each node in a BIT stores the sum of a specific range of elements.
     The length of this range is determined by the lowest set bit (LSB) of the index:
     LSB(x) = x & (-x).
   - Time Complexity:
     - Point Update: O(log N)
     - Range Query: O(log N)
   - Space Complexity: O(N)

3. Segment Tree (with Lazy Propagation)
   - Purpose: Allows answering range queries over an array effectively, while still
     being flexible enough to allow modification of the array.
   - Mathematical Insight: A binary tree where each node represents an interval.
     The root represents the whole array [0, N-1]. Its children represent
     [0, N/2] and [N/2+1, N-1].
     Lazy propagation defers updates to descendants until strictly necessary,
     maintaining O(log N) for range updates.
   - Time Complexity:
     - Range Update: O(log N)
     - Range Query: O(log N)
   - Space Complexity: O(N) (specifically 4*N)

4. Trie (Prefix Tree)
   - Purpose: An ordered tree data structure used to store a dynamic set or
     associative array where the keys are usually strings.
   - Mathematical Insight: Radix-based structural sharing. The height of the
     tree is bounded by the maximum string length L.
   - Time Complexity:
     - Insert: O(L), where L is the length of the string.
     - Search: O(L)
     - Prefix Match: O(L)
   - Space Complexity: O(N * L * Σ), where Σ is the alphabet size.

--------------------------------------------------------------------------------
Real-World Applications
--------------------------------------------------------------------------------
- DSU: Kruskal's Minimum Spanning Tree algorithm, network connectivity routing,
  image segmentation (connected components), equivalence class resolution in compilers.
- Fenwick Tree: Arithmetic coding, cumulative frequency tables in databases,
  fast counting of inversions in arrays (used in recommendation engines).
- Segment Tree: Computational geometry (sweepline algorithms), rendering engines
  (bounding volume hierarchies), financial data analysis (range min/max queries).
- Trie: Autocomplete systems, spell checkers, IP routing (Longest Prefix Match),
  Boggle/Wordle solvers.

================================================================================
'''

import unittest
from typing import List, Optional, TypeVar, Generic, Callable, Dict

# Type variable for generics if needed
T = TypeVar('T')

# ==============================================================================
# 1. Disjoint Set Union (DSU) / Union-Find
# ==============================================================================

class DSU:
    """
    Disjoint Set Union (Union-Find) with Path Compression and Union by Rank/Size.
    
    This data structure keeps track of a set of elements partitioned into a
    number of disjoint (non-overlapping) subsets.
    
    Techniques used:
    1. Path Compression: Flattens the structure of the tree whenever `find` is used,
       making future operations faster.
    2. Union by Size: Attaches the smaller tree to the root of the larger tree,
       keeping the tree shallow.
    """
    
    def __init__(self, n: int) -> None:
        """
        Initializes the DSU with `n` individual elements, each in its own set.
        
        Args:
            n (int): The number of elements (from 0 to n-1).
        """
        # Initially, each element is its own parent (representing its own set)
        self.parent: List[int] = list(range(n))
        
        # Initially, each set contains exactly 1 element
        self.size: List[int] = [1] * n
        
        # Keep track of the number of connected components
        self.components: int = n

    def find(self, i: int) -> int:
        """
        Finds the representative (root) of the set that contains element `i`.
        Applies path compression to optimize future queries.
        
        Args:
            i (int): The element to find.
            
        Returns:
            int: The representative of the set.
        """
        # Base case: if an element is its own parent, it is the root of its set.
        if self.parent[i] == i:
            return i
            
        # Path Compression: recursively find the root, and update the parent
        # of the current element to point directly to the root.
        self.parent[i] = self.find(self.parent[i])
        
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Merges the set containing element `i` with the set containing element `j`.
        Uses union by size.
        
        Args:
            i (int): The first element.
            j (int): The second element.
            
        Returns:
            bool: True if they were merged, False if they were already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        
        # Elements are already in the same set
        if root_i == root_j:
            return False
            
        # Union by Size: attach the smaller tree to the larger tree
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i
            
        # root_i is now guaranteed to be the root of the larger tree
        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        self.components -= 1
        
        return True

    def connected(self, i: int, j: int) -> bool:
        """
        Checks if elements `i` and `j` are in the same set.
        """
        return self.find(i) == self.find(j)

    def get_component_size(self, i: int) -> int:
        """
        Returns the size of the set containing element `i`.
        """
        return self.size[self.find(i)]

# ==============================================================================
# 2. Fenwick Tree (Binary Indexed Tree / BIT)
# ==============================================================================

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for efficient prefix sums and point updates.
    
    A Fenwick tree implicitly represents an array `A` of size `N`.
    It uses a 1-based internal array `tree` where each index `i` stores
    the sum of a specific range: from `i - LSB(i) + 1` to `i`.
    
    LSB (Least Significant Bit) can be isolated using `i & (-i)`.
    """
    
    def __init__(self, size: int) -> None:
        """
        Initializes an empty Fenwick Tree of the given size.
        
        Args:
            size (int): The number of elements (1-indexed conceptually, though 
                        often exposed as 0-indexed to users via a wrapper).
        """
        self.size = size
        # 1-indexed tree array, initialized to 0.
        # tree[0] is a dummy element that is never used.
        self.tree: List[int] = [0] * (size + 1)
        
    @classmethod
    def from_array(cls, arr: List[int]) -> 'FenwickTree':
        """
        Builds a Fenwick tree from an existing array in O(N) time.
        """
        size = len(arr)
        bit = cls(size)
        
        # 1-based indexing for internal tree construction
        for i in range(size):
            bit.tree[i + 1] = arr[i]
            
        # Linear time construction trick: 
        # Add the current node's value to its immediate parent
        for i in range(1, size + 1):
            parent = i + (i & -i)
            if parent <= size:
                bit.tree[parent] += bit.tree[i]
                
        return bit

    def add(self, index: int, delta: int) -> None:
        """
        Adds `delta` to element at `index`. (0-indexed internally mapped to 1-indexed)
        
        Time Complexity: O(log N)
        
        Args:
            index (int): The 0-based index of the element to update.
            delta (int): The value to add to the element.
        """
        # Convert to 1-based index
        i = index + 1
        
        # Traverse up the tree to update the ancestors
        while i <= self.size:
            self.tree[i] += delta
            # Move to the next parent by adding the LSB
            i += (i & -i)

    def prefix_sum(self, index: int) -> int:
        """
        Computes the sum of elements from 0 up to `index` (inclusive).
        
        Time Complexity: O(log N)
        
        Args:
            index (int): The 0-based index.
            
        Returns:
            int: The prefix sum.
        """
        # Convert to 1-based index
        i = index + 1
        total = 0
        
        # Traverse down the tree to accumulate the sum
        while i > 0:
            total += self.tree[i]
            # Move to the previous range by subtracting the LSB
            i -= (i & -i)
            
        return total

    def range_sum(self, left: int, right: int) -> int:
        """
        Computes the sum of elements in the range [left, right] inclusive.
        
        Args:
            left (int): The 0-based starting index.
            right (int): The 0-based ending index.
            
        Returns:
            int: The range sum.
        """
        if left > right:
            return 0
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


# ==============================================================================
# 3. Segment Tree (with Lazy Propagation)
# ==============================================================================

class SegmentTree:
    """
    Segment Tree with Lazy Propagation for Range Updates and Range Queries.
    
    This implementation supports Range Add updates and Range Sum queries.
    It can be easily adapted for Range Min/Max by changing the combiner function.
    """
    
    def __init__(self, data: List[int]) -> None:
        """
        Builds the Segment Tree from the provided array.
        
        Args:
            data (List[int]): The initial array of values.
        """
        self.n = len(data)
        self.data = data
        
        # The tree size is bounded by 4 * N
        self.tree: List[int] = [0] * (4 * self.n)
        self.lazy: List[int] = [0] * (4 * self.n)
        
        if self.n > 0:
            self._build(0, 0, self.n - 1)
            
    def _build(self, node: int, start: int, end: int) -> None:
        """
        Recursively builds the segment tree.
        """
        if start == end:
            # Leaf node
            self.tree[node] = self.data[start]
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build(left_child, start, mid)
        self._build(right_child, mid + 1, end)
        
        # Internal node maintains the sum of its children
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
        
    def _push_down(self, node: int, start: int, end: int) -> None:
        """
        Pushes pending lazy updates down to the children.
        """
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            
            # Apply lazy value to left child
            self.tree[left_child] += self.lazy[node] * (mid - start + 1)
            self.lazy[left_child] += self.lazy[node]
            
            # Apply lazy value to right child
            self.tree[right_child] += self.lazy[node] * (end - mid)
            self.lazy[right_child] += self.lazy[node]
            
            # Clear current node's lazy value
            self.lazy[node] = 0

    def _update_range(self, node: int, start: int, end: int, l: int, r: int, val: int) -> None:
        """
        Internal recursive function for range updates.
        """
        # No overlap
        if start > r or end < l:
            return
            
        # Total overlap
        if start >= l and end <= r:
            self.tree[node] += val * (end - start + 1)
            self.lazy[node] += val
            return
            
        # Partial overlap: push down lazy updates first
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._update_range(left_child, start, mid, l, r, val)
        self._update_range(right_child, mid + 1, end, l, r, val)
        
        # Re-calculate current node value after updating children
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update_range(self, l: int, r: int, val: int) -> None:
        """
        Adds `val` to all elements in the range [l, r] inclusive.
        
        Time Complexity: O(log N)
        """
        if self.n > 0:
            self._update_range(0, 0, self.n - 1, l, r, val)

    def _query_range(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """
        Internal recursive function for range queries.
        """
        # No overlap
        if start > r or end < l:
            return 0
            
        # Total overlap
        if start >= l and end <= r:
            return self.tree[node]
            
        # Partial overlap: push down lazy updates first
        self._push_down(node, start, end)
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_sum = self._query_range(left_child, start, mid, l, r)
        right_sum = self._query_range(right_child, mid + 1, end, l, r)
        
        return left_sum + right_sum

    def query_range(self, l: int, r: int) -> int:
        """
        Computes the sum of elements in the range [l, r] inclusive.
        
        Time Complexity: O(log N)
        """
        if self.n == 0:
            return 0
        return self._query_range(0, 0, self.n - 1, l, r)


# ==============================================================================
# 4. Trie (Prefix Tree)
# ==============================================================================

class TrieNode:
    """
    A single node in a Trie structure.
    """
    def __init__(self):
        # Maps a character to the next TrieNode
        self.children: Dict[str, 'TrieNode'] = {}
        # Indicates if a word ends at this node
        self.is_end_of_word: bool = False
        # (Optional) Count of words passing through this node, useful for deletion
        # or counting words with a specific prefix.
        self.prefix_count: int = 0

class Trie:
    """
    Trie (Prefix Tree) data structure for efficient string storage and prefix retrieval.
    
    Tries are exceptional for problems involving string matching, autocomplete,
    and IP routing algorithms.
    """
    
    def __init__(self) -> None:
        """
        Initializes an empty Trie.
        """
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the Trie.
        
        Time Complexity: O(L), where L is the length of the word.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Searches for a complete word in the Trie.
        
        Time Complexity: O(L)
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Checks if there is any word in the Trie that starts with the given prefix.
        
        Time Complexity: O(L)
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """
        Helper method to traverse the Trie and return the node corresponding 
        to the end of the prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Counts how many words in the Trie start with the given prefix.
        
        Time Complexity: O(L)
        """
        node = self._find_node(prefix)
        if node is None:
            return 0
        return node.prefix_count


# ==============================================================================
# Comprehensive Test Suite
# ==============================================================================

class TestAdvancedDataStructures(unittest.TestCase):
    
    def test_dsu(self):
        dsu = DSU(5)
        self.assertEqual(dsu.components, 5)
        
        dsu.union(0, 1)
        self.assertTrue(dsu.connected(0, 1))
        self.assertEqual(dsu.components, 4)
        
        dsu.union(1, 2)
        self.assertTrue(dsu.connected(0, 2))
        
        # Test union by size / find
        self.assertEqual(dsu.get_component_size(0), 3)
        self.assertFalse(dsu.connected(0, 3))
        
        dsu.union(3, 4)
        self.assertEqual(dsu.components, 2)
        dsu.union(2, 4)
        self.assertEqual(dsu.components, 1)
        
        # All connected now
        self.assertTrue(dsu.connected(0, 4))

    def test_fenwick_tree(self):
        arr = [1, 2, 3, 4, 5]
        bit = FenwickTree.from_array(arr)
        
        # Prefix sum of up to index 2 (1+2+3) = 6
        self.assertEqual(bit.prefix_sum(2), 6)
        
        # Range sum from index 1 to 3 (2+3+4) = 9
        self.assertEqual(bit.range_sum(1, 3), 9)
        
        # Update index 2 by adding 5
        bit.add(2, 5) # arr becomes [1, 2, 8, 4, 5]
        
        self.assertEqual(bit.range_sum(1, 3), 14)
        self.assertEqual(bit.range_sum(0, 4), 20)
        
    def test_segment_tree(self):
        arr = [1, 3, 5, 7, 9, 11]
        seg_tree = SegmentTree(arr)
        
        # Initial queries
        self.assertEqual(seg_tree.query_range(1, 3), 15) # 3 + 5 + 7 = 15
        self.assertEqual(seg_tree.query_range(0, 5), 36) # sum of all
        
        # Range Update: Add 2 to range [1, 3]
        # arr conceptually becomes [1, 5, 7, 9, 9, 11]
        seg_tree.update_range(1, 3, 2)
        
        self.assertEqual(seg_tree.query_range(1, 3), 21) # 5 + 7 + 9 = 21
        self.assertEqual(seg_tree.query_range(0, 5), 42)
        
        # Overlapping update
        seg_tree.update_range(3, 5, 1)
        # arr conceptually becomes [1, 5, 7, 10, 10, 12]
        self.assertEqual(seg_tree.query_range(3, 5), 32)
        
    def test_trie(self):
        trie = Trie()
        trie.insert("apple")
        self.assertTrue(trie.search("apple"))
        self.assertFalse(trie.search("app"))
        self.assertTrue(trie.starts_with("app"))
        
        trie.insert("app")
        self.assertTrue(trie.search("app"))
        
        trie.insert("application")
        self.assertEqual(trie.count_words_with_prefix("app"), 3)
        self.assertEqual(trie.count_words_with_prefix("apple"), 1)


if __name__ == '__main__':
    print("=" * 80)
    print("Running Interactive Lesson Tests: Advanced Data Structures")
    print("=" * 80)
    
    # Run the standard unittests
    unittest.main(verbosity=2)
