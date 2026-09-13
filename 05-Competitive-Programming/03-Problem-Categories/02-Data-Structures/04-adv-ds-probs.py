"""
Advanced Data Structures in Competitive Programming

Welcome to the comprehensive, textbook-grade module on Advanced Data Structures! 
This module is designed to bridge the gap between theoretical computer science and 
practical, high-performance competitive programming.

================================================================================
TABLE OF CONTENTS
================================================================================
1. Tries (Prefix Trees)
2. Disjoint Set Union (DSU) / Union-Find
3. Fenwick Trees (Binary Indexed Trees)
4. Segment Trees (Point Updates)
5. Segment Trees with Lazy Propagation (Range Updates)

================================================================================
1. TRIES (PREFIX TREES)
================================================================================
A Trie is an ordered tree data structure used to store a dynamic set or associative 
array where the keys are usually strings. Unlike a binary search tree, no node in 
the tree stores the key associated with that node; instead, its position in the 
tree defines the key with which it is associated.

Applications:
- Autocomplete and spell-checking.
- IP routing (Longest Prefix Matching).
- Solving word games (Boggle) efficiently.

Complexity:
- Time: O(M) for insertion and search, where M is the length of the string.
- Space: O(N * M * K) where N is the number of strings, M is the average length, 
  and K is the alphabet size.

================================================================================
2. DISJOINT SET UNION (DSU)
================================================================================
DSU, or Union-Find, keeps track of a set of elements partitioned into a number 
of disjoint (non-overlapping) subsets. It provides near-constant-time operations 
to add new sets, to merge existing sets, and to determine whether elements are 
in the same set.

Optimizations:
- Path Compression: Flattens the structure of the tree whenever `find` is used.
- Union by Rank/Size: Always attaches the smaller tree to the root of the larger tree.

Mathematical Background:
With both optimizations, the amortized time complexity of operations is 
O(α(N)), where α(N) is the inverse Ackermann function, which grows so slowly 
that it is < 5 for all practical values of N.

================================================================================
3. FENWICK TREES (BINARY INDEXED TREES)
================================================================================
A Fenwick Tree provides a way to represent an array of numbers in an array, 
allowing prefix sums to be calculated and point elements to be updated in 
O(log N) time. It relies heavily on bitwise operations.

Mathematical Background:
Every integer can be represented as a sum of powers of 2 (its binary representation).
Similarly, a cumulative frequency can be represented as the sum of sub-frequencies.
In a BIT, index `i` is responsible for elements from `i - (i & -i) + 1` to `i`.
The bitwise operation `i & -i` extracts the lowest set bit of `i`.

================================================================================
4. SEGMENT TREES
================================================================================
A Segment Tree is a binary tree used for storing information about intervals 
or segments. It allows querying which of the stored segments contain a given 
point or range, such as finding the sum, minimum, or maximum of an array in 
a specific range.

Complexity:
- Build: O(N)
- Query: O(log N)
- Update: O(log N)
- Space: O(N) (typically 4*N array size)

================================================================================
5. LAZY PROPAGATION IN SEGMENT TREES
================================================================================
Standard Segment Trees support point updates. When updating a range of elements, 
updating one by one would take O(R * log N) where R is the range size.
Lazy Propagation defers the update to descendants until they are actually needed, 
maintaining O(log N) time complexity for range updates.

Let's dive into the implementations!
"""

from typing import List, Optional, Dict, Iterable, Tuple


# ==============================================================================
# 1. TRIE (PREFIX TREE)
# ==============================================================================

class TrieNode:
    """
    Represents a single node within the Trie.
    """
    def __init__(self):
        # Using a dictionary allows for dynamic character insertion and supports
        # full Unicode character sets without pre-allocating an array of fixed size.
        self.children: Dict[str, 'TrieNode'] = {}
        # Boolean flag to mark the end of a valid dictionary word
        self.is_end_of_word: bool = False
        # Optional metadata (e.g., word count or specific string identifier)
        self.count: int = 0


class Trie:
    """
    Professional implementation of a Trie.
    Provides methods for insertion, full-word search, prefix search, and deletion.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        
        Time Complexity: O(M), where M is the length of the word.
        Space Complexity: O(M) in the worst case (if no common prefix exists).
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1  # Keep track of how many words share this prefix
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Returns True if the exact word exists in the trie.
        
        Time Complexity: O(M)
        Space Complexity: O(1)
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
        Returns True if there is ANY word in the trie that starts with the given prefix.
        
        Time Complexity: O(M), where M is the length of the prefix.
        Space Complexity: O(1)
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
        
    def delete(self, word: str) -> bool:
        """
        Deletes a word from the Trie if it exists.
        Returns True if the word was successfully deleted, False otherwise.
        """
        def _delete_helper(current: TrieNode, word: str, index: int) -> bool:
            if index == len(word):
                if not current.is_end_of_word:
                    return False # Word doesn't exist
                current.is_end_of_word = False
                return len(current.children) == 0 # Return True if node can be deleted
            
            char = word[index]
            if char not in current.children:
                return False
            
            should_delete_child = _delete_helper(current.children[char], word, index + 1)
            
            if should_delete_child:
                del current.children[char]
                # If current node is not an end of another word and has no other children,
                # signal that it can be deleted too.
                return len(current.children) == 0 and not current.is_end_of_word
            
            return False
            
        # First, ensure the word actually exists to maintain consistent counts
        if self.search(word):
            _delete_helper(self.root, word, 0)
            return True
        return False


# ==============================================================================
# 2. DISJOINT SET UNION (DSU)
# ==============================================================================

class DSU:
    """
    Disjoint Set Union (Union-Find) with Path Compression and Union by Rank.
    """
    def __init__(self, n: int):
        # parent[i] points to the parent of node i
        self.parent = list(range(n))
        # rank[i] is an upper bound on the height of the tree rooted at i
        self.rank = [0] * n
        # size[i] stores the size of the connected component (optional but useful)
        self.size = [1] * n
        self.components_count = n

    def find(self, i: int) -> int:
        """
        Finds the representative of the set containing `i` using Path Compression.
        
        Path compression flattens the tree structure by making every node in the 
        path point directly to the root.
        
        Amortized Time Complexity: O(α(N))
        """
        if self.parent[i] == i:
            return i
        # Recursively find the root, and perform path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """
        Unions the sets containing `i` and `j` using Union by Rank.
        Returns True if a union was performed, False if they were already connected.
        
        Amortized Time Complexity: O(α(N))
        """
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            # Union by rank: attach smaller tree under root of larger tree
            if self.rank[root_i] < self.rank[root_j]:
                root_i, root_j = root_j, root_i
            
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1
                
            self.components_count -= 1
            return True
        return False
        
    def get_size(self, i: int) -> int:
        """Returns the size of the component containing node i."""
        return self.size[self.find(i)]


# ==============================================================================
# 3. FENWICK TREE (BINARY INDEXED TREE)
# ==============================================================================

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for efficient 1D prefix sum queries 
    and point updates. It uses a 1-based indexing internally.
    """
    def __init__(self, size: int):
        self.n = size
        # 1-based index internally, so we allocate n + 1
        self.tree = [0] * (self.n + 1)

    @classmethod
    def from_array(cls, arr: List[int]) -> 'FenwickTree':
        """
        Constructs a Fenwick Tree from an existing array in O(N) time.
        """
        n = len(arr)
        bit = cls(n)
        for i in range(n):
            bit.tree[i + 1] = arr[i]
            
        # O(N) building algorithm
        for i in range(1, n + 1):
            parent = i + (i & -i)
            if parent <= n:
                bit.tree[parent] += bit.tree[i]
        return bit

    def update(self, i: int, delta: int) -> None:
        """
        Adds `delta` to the element at 0-based index `i`.
        
        Time Complexity: O(log N)
        """
        i += 1  # Convert to 1-based index
        while i <= self.n:
            self.tree[i] += delta
            # Move to the next node responsible for this element
            i += (i & -i)

    def query(self, i: int) -> int:
        """
        Computes the prefix sum from index 0 to `i` (0-based, inclusive).
        
        Time Complexity: O(log N)
        """
        i += 1  # Convert to 1-based index
        s = 0
        while i > 0:
            s += self.tree[i]
            # Move to the parent node
            i -= (i & -i)
        return s

    def query_range(self, left: int, right: int) -> int:
        """
        Computes the sum in the inclusive range [left, right] (0-based).
        """
        if left > right:
            return 0
        return self.query(right) - self.query(left - 1)


# ==============================================================================
# 4. SEGMENT TREE (POINT UPDATES)
# ==============================================================================

class SegmentTree:
    """
    Segment Tree implementation supporting generic associative functions
    (e.g., min, max, sum) with Point Updates.
    
    This uses the 1-based array representation:
    - Left child of `v` is `2*v`
    - Right child of `v` is `2*v + 1`
    """
    def __init__(self, data: List[int], func=sum, default_val=0):
        self.n = len(data)
        self.func = func
        self.default_val = default_val
        # 4*N is guaranteed to be enough space for the segment tree array
        self.tree = [default_val] * (4 * self.n)
        
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        """
        Recursively builds the segment tree.
        Time Complexity: O(N)
        """
        if start == end:
            # Leaf node will have a single element
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node
            right_child = 2 * node + 1
            
            self._build(data, left_child, start, mid)
            self._build(data, right_child, mid + 1, end)
            
            # Internal node will have the merge of both children
            self.tree[node] = self.func(self.tree[left_child], self.tree[right_child])

    def update(self, index: int, val: int) -> None:
        """Public method for point update."""
        if self.n > 0:
            self._update(1, 0, self.n - 1, index, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: int) -> None:
        """
        Updates the value at `idx` to `val` and recomputes ancestor values.
        Time Complexity: O(log N)
        """
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            left_child = 2 * node
            right_child = 2 * node + 1
            
            if start <= idx <= mid:
                # Target is in the left half
                self._update(left_child, start, mid, idx, val)
            else:
                # Target is in the right half
                self._update(right_child, mid + 1, end, idx, val)
                
            # Recompute the current node
            self.tree[node] = self.func(self.tree[left_child], self.tree[right_child])

    def query(self, l: int, r: int) -> int:
        """Public method for range query [l, r] (inclusive)."""
        if self.n == 0:
            return self.default_val
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """
        Answers the range query.
        Time Complexity: O(log N)
        """
        # Case 1: The current segment is completely outside the query range
        if r < start or end < l:
            return self.default_val
            
        # Case 2: The current segment is completely inside the query range
        if l <= start and end <= r:
            return self.tree[node]
            
        # Case 3: Partial overlap
        mid = (start + end) // 2
        p1 = self._query(2 * node, start, mid, l, r)
        p2 = self._query(2 * node + 1, mid + 1, end, l, r)
        
        return self.func(p1, p2)


# ==============================================================================
# 5. SEGMENT TREE WITH LAZY PROPAGATION (RANGE UPDATES)
# ==============================================================================

class LazySegmentTree:
    """
    Segment Tree with Lazy Propagation.
    This implementation handles Range Addition Updates and Range Sum Queries.
    
    Lazy Propagation defers updates to descendants to avoid an O(N) penalty 
    when updating a large range, maintaining O(log N) per update operation.
    """
    def __init__(self, data: List[int]):
        self.n = len(data)
        # Main tree stores the sum of intervals
        self.tree = [0] * (4 * self.n)
        # Lazy array stores pending updates for descendants
        self.lazy = [0] * (4 * self.n)
        
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)
            
    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2 * node, start, mid)
            self._build(data, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _propagate(self, node: int, start: int, end: int) -> None:
        """
        Propagates the lazy value to the children and clears the current lazy value.
        """
        if self.lazy[node] != 0:
            # If there's a pending update for this node, apply it
            # The sum increases by lazy_value * number_of_elements_in_interval
            self.tree[node] += self.lazy[node] * (end - start + 1)
            
            # If not a leaf node, propagate the lazy value downwards
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
                
            # Clear the lazy value for the current node
            self.lazy[node] = 0

    def update_range(self, l: int, r: int, val: int) -> None:
        """Public method for range addition [l, r]."""
        if self.n > 0:
            self._update_range(1, 0, self.n - 1, l, r, val)

    def _update_range(self, node: int, start: int, end: int, l: int, r: int, val: int) -> None:
        """
        Adds `val` to all elements in the range [l, r].
        Time Complexity: O(log N)
        """
        # Always propagate any pending updates before proceeding
        self._propagate(node, start, end)
        
        # Out of bounds
        if start > end or start > r or end < l:
            return
            
        # Current segment is fully within update range
        if l <= start and end <= r:
            self.lazy[node] += val
            self._propagate(node, start, end)
            return
            
        # Partial overlap, update children
        mid = (start + end) // 2
        self._update_range(2 * node, start, mid, l, r, val)
        self._update_range(2 * node + 1, mid + 1, end, l, r, val)
        
        # Update current node based on children
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, l: int, r: int) -> int:
        """Public method for range sum query."""
        if self.n == 0:
            return 0
        return self._query_range(1, 0, self.n - 1, l, r)

    def _query_range(self, node: int, start: int, end: int, l: int, r: int) -> int:
        """
        Queries the sum in the range [l, r].
        Time Complexity: O(log N)
        """
        # Always propagate before querying
        self._propagate(node, start, end)
        
        # Out of bounds
        if start > end or start > r or end < l:
            return 0
            
        # Fully within range
        if l <= start and end <= r:
            return self.tree[node]
            
        # Partial overlap
        mid = (start + end) // 2
        p1 = self._query_range(2 * node, start, mid, l, r)
        p2 = self._query_range(2 * node + 1, mid + 1, end, l, r)
        
        return p1 + p2


# ==============================================================================
# INTERACTIVE LESSON / TESTING MODULE
# ==============================================================================
if __name__ == "__main__":
    import sys

    print("="*60)
    print(" ADVANCED DATA STRUCTURES - INTERACTIVE TEST SUITE")
    print("="*60)
    print()

    # --------------------------------------------------------------------------
    # 1. TRIE TESTS
    # --------------------------------------------------------------------------
    print(">>> 1. Testing Trie (Prefix Tree)")
    trie = Trie()
    words = ["apple", "app", "application", "apt", "bat", "batch"]
    for w in words:
        trie.insert(w)
    
    print(f"Inserted words: {words}")
    
    # Exact Match Tests
    assert trie.search("apple") is True, "Failed: 'apple' should be found"
    assert trie.search("app") is True, "Failed: 'app' should be found"
    assert trie.search("aptitude") is False, "Failed: 'aptitude' should not be found"
    print(" - Exact Match Search: PASSED")
    
    # Prefix Match Tests
    assert trie.startsWith("app") is True, "Failed: prefix 'app' should be found"
    assert trie.startsWith("batc") is True, "Failed: prefix 'batc' should be found"
    assert trie.startsWith("cat") is False, "Failed: prefix 'cat' should not be found"
    print(" - Prefix Search: PASSED")
    
    # Delete Tests
    assert trie.delete("app") is True, "Failed: 'app' should be deleted"
    assert trie.search("app") is False, "Failed: 'app' should no longer be found"
    assert trie.search("apple") is True, "Failed: 'apple' should still exist!"
    assert trie.startsWith("app") is True, "Failed: prefix 'app' should still exist due to 'apple'"
    print(" - Deletion operations: PASSED")
    print("Trie tests fully passed!\\n")

    # --------------------------------------------------------------------------
    # 2. DSU TESTS
    # --------------------------------------------------------------------------
    print(">>> 2. Testing Disjoint Set Union (DSU)")
    dsu = DSU(5) # Nodes 0 to 4
    
    # Union operations
    dsu.union(0, 1)
    dsu.union(2, 3)
    dsu.union(1, 2)
    
    print("Edges added: (0,1), (2,3), (1,2)")
    
    # Connectivity Checks
    assert dsu.find(0) == dsu.find(3), "Failed: 0 and 3 should be connected"
    assert dsu.find(0) != dsu.find(4), "Failed: 0 and 4 should NOT be connected"
    
    print(" - Connectivity Checks: PASSED")
    print(f" - Size of component containing 0: {dsu.get_size(0)}")
    print(f" - Total connected components: {dsu.components_count}")
    assert dsu.get_size(0) == 4, "Failed: Component size should be 4"
    assert dsu.components_count == 2, "Failed: Should be 2 components (0,1,2,3) and (4)"
    print("DSU tests fully passed!\\n")

    # --------------------------------------------------------------------------
    # 3. FENWICK TREE TESTS
    # --------------------------------------------------------------------------
    print(">>> 3. Testing Fenwick Tree (Binary Indexed Tree)")
    arr = [2, 1, 1, 3, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Original Array: {arr}")
    
    bit = FenwickTree.from_array(arr)
    
    # Query Tests
    sum_0_to_4 = bit.query_range(0, 4)
    expected_sum = sum(arr[0:5])
    assert sum_0_to_4 == expected_sum, f"Failed: Expected {expected_sum}, got {sum_0_to_4}"
    
    sum_2_to_7 = bit.query_range(2, 7)
    expected_sum_2 = sum(arr[2:8])
    assert sum_2_to_7 == expected_sum_2, f"Failed: Expected {expected_sum_2}, got {sum_2_to_7}"
    
    print(" - Range Queries: PASSED")
    
    # Update Tests
    # Update arr[3] from 3 to 10 (delta = 7)
    print("Updating index 3 by adding +7...")
    bit.update(3, 7)
    arr[3] += 7
    
    new_sum_0_to_4 = bit.query_range(0, 4)
    expected_new_sum = sum(arr[0:5])
    assert new_sum_0_to_4 == expected_new_sum, f"Failed: Expected {expected_new_sum}, got {new_sum_0_to_4}"
    print(" - Point Updates & Re-Queries: PASSED")
    print("Fenwick Tree tests fully passed!\\n")

    # --------------------------------------------------------------------------
    # 4. SEGMENT TREE TESTS
    # --------------------------------------------------------------------------
    print(">>> 4. Testing Segment Tree (Point Updates, Range Minimum Query)")
    st_arr = [5, 2, 9, -1, 7, 3, 1, 4]
    print(f"Original Array: {st_arr}")
    
    # Initialize for Range Minimum Query (RMQ)
    st = SegmentTree(st_arr, func=min, default_val=float('inf'))
    
    min_0_to_3 = st.query(0, 3)
    assert min_0_to_3 == -1, f"Failed: Expected -1, got {min_0_to_3}"
    
    min_4_to_7 = st.query(4, 7)
    assert min_4_to_7 == 1, f"Failed: Expected 1, got {min_4_to_7}"
    print(" - RMQ Range Queries: PASSED")
    
    # Update Tests
    print("Updating index 3 from -1 to 10...")
    st.update(3, 10)
    
    new_min_0_to_3 = st.query(0, 3)
    assert new_min_0_to_3 == 2, f"Failed: Expected 2, got {new_min_0_to_3}"
    print(" - RMQ Point Updates & Re-Queries: PASSED")
    print("Segment Tree tests fully passed!\\n")

    # --------------------------------------------------------------------------
    # 5. LAZY SEGMENT TREE TESTS
    # --------------------------------------------------------------------------
    print(">>> 5. Testing Lazy Segment Tree (Range Updates, Range Sum Query)")
    lazy_arr = [1, 2, 3, 4, 5]
    print(f"Original Array: {lazy_arr}")
    
    lst = LazySegmentTree(lazy_arr)
    
    # Initial Queries
    assert lst.query_range(0, 4) == 15, "Failed: Initial sum should be 15"
    assert lst.query_range(1, 3) == 9, "Failed: Initial sub-sum should be 9"
    
    print(" - Initial Queries: PASSED")
    
    # Range Update
    print("Applying Range Update: add 2 to indices [1..3]")
    lst.update_range(1, 3, 2)
    # Conceptual Array is now: [1, 4, 5, 6, 5]
    
    assert lst.query_range(0, 4) == 21, f"Failed: Expected 21, got {lst.query_range(0, 4)}"
    assert lst.query_range(1, 3) == 15, f"Failed: Expected 15, got {lst.query_range(1, 3)}"
    assert lst.query_range(0, 1) == 5, f"Failed: Expected 5, got {lst.query_range(0, 1)}"
    
    print(" - Range Updates & Re-Queries: PASSED")
    print("Lazy Segment Tree tests fully passed!\\n")
    
    print("="*60)
    print(" ALL TESTS PASSED SUCCESSFULLY! ")
    print("="*60)
