"""
=========================================================================================
PYTHON COMPETITIVE PROGRAMMING: THE ULTIMATE TEXTBOOK-GRADE TEMPLATE
=========================================================================================

Author: Python DSA Master
Target: Advanced Competitive Programmers & Algorithmic Problem Solvers

-----------------------------------------------------------------------------------------
1. INTRODUCTION & THEORETICAL FOUNDATION
-----------------------------------------------------------------------------------------
Competitive programming (CP) is the ultimate test of an engineer's command over 
algorithms, data structures, and mathematical problem-solving. Python, while not as 
fast as C++ natively, provides unmatched developer velocity and built-in large integer 
arithmetic. To succeed in CP using Python, one must compensate for interpreter overhead
by using optimal data structures and efficient input/output (I/O) handling.

This template is designed as an interactive, textbook-grade module that provides:
  1. Fast I/O configurations (crucial for passing strict time limits).
  2. Core Data Structures: DSU, Fenwick Trees, Segment Trees.
  3. Graph Algorithms: Shortest Paths, MST, LCA.
  4. Number Theory: Modular arithmetic, Sieve, Combinatorics.
  5. String Algorithms: Pattern matching techniques.

-----------------------------------------------------------------------------------------
2. BIG-O COMPLEXITY OVERVIEW
-----------------------------------------------------------------------------------------
For N = 10^5, aim for O(N log N) or O(N).
For N = 10^3, O(N^2) might pass in Python if highly optimized.
For N = 100, O(N^3) is acceptable.
For N = 20, O(2^N) is typical.

Python's built-in `list.sort()` (Timsort) is highly optimized and runs in O(N log N).
`list.append()` and `list.pop()` are O(1) amortized, but `list.insert(0, x)` is O(N).
Always use `collections.deque` for O(1) left appends/pops.

-----------------------------------------------------------------------------------------
3. REAL-WORLD APPLICATIONS
-----------------------------------------------------------------------------------------
The algorithms here power modern computing:
- DSU: Network connectivity, image processing components, Kruskal's MST.
- Segment Trees: Real-time analytics, database range queries.
- String Matching: Search engines, DNA sequencing.
- Shortest Paths: GPS routing (Google Maps), packet routing protocols (OSPF).

=========================================================================================
"""

import sys
import os
import math
import heapq
import collections
from collections import deque, Counter, defaultdict
from bisect import bisect_left, bisect_right
from functools import lru_cache
from typing import List, Tuple, Dict, Set, Optional, Any, Iterable

# =======================================================================================
#                               FAST I/O CONFIGURATION
# =======================================================================================
# In Python, standard `print` and `input` are relatively slow. For reading thousands of 
# integers, we use `sys.stdin.read` or `sys.stdin.readline`.
# `os.read(0, ...)` is even faster for pure raw byte processing.
# =======================================================================================

def get_ints() -> List[int]:
    """Reads a line of space-separated integers."""
    return list(map(int, sys.stdin.readline().split()))

def get_int() -> int:
    """Reads a single integer from a line."""
    return int(sys.stdin.readline().strip())

# Optional Fast I/O class for extremely strict time limits
class FastIO:
    """
    A utility class for buffering standard input and output.
    Useful when processing inputs over 10^6 elements.
    """
    def __init__(self):
        pass
    
    @staticmethod
    def read_all_tokens():
        return sys.stdin.read().split()


# =======================================================================================
#                           1. DISJOINT SET UNION (UNION-FIND)
# =======================================================================================
# Time Complexity: O(alpha(N)) per operation, where alpha is the Inverse Ackermann function.
# Space Complexity: O(N)
# 
# Mathematical Background:
# DSU maintains a partition of a set of elements into disjoint (non-overlapping) subsets.
# It supports two near-O(1) operations:
# - Find: Determine which subset a particular element is in (using Path Compression).
# - Union: Join two subsets into a single subset (using Union by Rank or Size).
# =======================================================================================

class DSU:
    def __init__(self, n: int):
        """
        Initializes the DSU with `n` elements (0 to n-1).
        """
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        """
        Finds the representative of the set that `x` belongs to.
        Applies path compression for accelerated future queries.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Unites the sets containing `x` and `y`.
        Returns True if they were in different sets, False if already in the same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by size: attach smaller tree under root of larger tree
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.components -= 1
        return True


# =======================================================================================
#                           2. FENWICK TREE (BINARY INDEXED TREE)
# =======================================================================================
# Time Complexity: O(log N) for both point update and prefix sum query.
# Space Complexity: O(N)
# 
# Mathematical Background:
# Any integer can be represented as a sum of powers of 2 (binary representation).
# A Fenwick Tree stores the sum of intervals of length equal to the least significant
# bit (LSB) of the index. LSB(i) = i & (-i).
# =======================================================================================

class FenwickTree:
    def __init__(self, size: int):
        """1-based indexing is typically used for Fenwick Trees."""
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index: int, delta: int) -> None:
        """Adds `delta` to element at `index`."""
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index) # Add LSB

    def query(self, index: int) -> int:
        """Returns the sum from index 1 to `index`."""
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & (-index) # Subtract LSB
        return total
    
    def range_query(self, left: int, right: int) -> int:
        """Returns the sum in the range [left, right]."""
        return self.query(right) - self.query(left - 1)


# =======================================================================================
#                           3. SEGMENT TREE
# =======================================================================================
# Time Complexity: O(log N) for updates and queries. Build is O(N).
# Space Complexity: O(4 * N)
# 
# Mathematical Background:
# A perfectly balanced binary tree where each node represents an interval of the array.
# The root represents [0, N-1]. Children of node representing [L, R] are [L, mid] and 
# [mid+1, R]. Used for associative operations like sum, min, max, gcd.
# =======================================================================================

class SegmentTree:
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        self.tree[node] = self.tree[left_child] + self.tree[right_child] # Change for min/max

    def update(self, index: int, val: int) -> None:
        self._update(0, 0, self.n - 1, index, val)

    def _update(self, node: int, start: int, end: int, index: int, val: int) -> None:
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        if start <= index <= mid:
            self._update(left_child, start, mid, index, val)
        else:
            self._update(right_child, mid + 1, end, index, val)
            
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query(self, l: int, r: int) -> int:
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        # Completely outside
        if r < start or end < l:
            return 0 # Return infinity for min, 0 for sum
            
        # Completely inside
        if l <= start and end <= r:
            return self.tree[node]
            
        # Partial overlap
        mid = (start + end) // 2
        left_val = self._query(2 * node + 1, start, mid, l, r)
        right_val = self._query(2 * node + 2, mid + 1, end, l, r)
        return left_val + right_val


# =======================================================================================
#                           4. GRAPH ALGORITHMS
# =======================================================================================
# Dijkstra's Algorithm: Shortest path on a weighted graph with non-negative edges.
# Time Complexity: O(E log V) using a binary heap.
# =======================================================================================

def dijkstra(n: int, adj: List[List[Tuple[int, int]]], start: int) -> List[int]:
    """
    Computes shortest paths from `start` to all other nodes.
    `adj` is an adjacency list where adj[u] = [(v, weight), ...]
    """
    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0
    pq = [(0, start)] # (distance, node)
    
    while pq:
        d, u = heapq.heappop(pq)
        
        # If we found a longer path, ignore
        if d > dist[u]:
            continue
            
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
                
    return dist

# =======================================================================================
# Lowest Common Ancestor (LCA) using Binary Lifting
# Time Complexity: Build O(N log N), Query O(log N)
# =======================================================================================

class LCA:
    def __init__(self, n: int, adj: List[List[int]], root: int = 0):
        self.n = n
        self.LOG = math.ceil(math.log2(n)) + 1
        self.up = [[-1] * self.LOG for _ in range(n)]
        self.depth = [0] * n
        self._dfs(root, -1, 0, adj)
        self._build()

    def _dfs(self, u: int, p: int, d: int, adj: List[List[int]]):
        self.up[u][0] = p
        self.depth[u] = d
        for v in adj[u]:
            if v != p:
                self._dfs(v, u, d + 1, adj)

    def _build(self):
        for j in range(1, self.LOG):
            for i in range(self.n):
                if self.up[i][j-1] != -1:
                    self.up[i][j] = self.up[self.up[i][j-1]][j-1]

    def query(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
            
        # Bring them to the same depth
        diff = self.depth[u] - self.depth[v]
        for j in range(self.LOG - 1, -1, -1):
            if (diff & (1 << j)):
                u = self.up[u][j]
                
        if u == v:
            return u
            
        # Lift them together
        for j in range(self.LOG - 1, -1, -1):
            if self.up[u][j] != self.up[v][j]:
                u = self.up[u][j]
                v = self.up[v][j]
                
        return self.up[u][0]


# =======================================================================================
#                           5. MATHEMATICS & NUMBER THEORY
# =======================================================================================
# Combinatorics: nCr modulo P
# Sieve of Eratosthenes: Finding all primes up to N in O(N log log N).
# =======================================================================================

MOD = 10**9 + 7

def sieve(limit: int) -> List[int]:
    """Returns a list of primes up to `limit`."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]

class Combinatorics:
    def __init__(self, n: int, mod: int = MOD):
        self.mod = mod
        self.fact = [1] * (n + 1)
        self.inv = [1] * (n + 1)
        
        # Precompute factorials
        for i in range(1, n + 1):
            self.fact[i] = (self.fact[i - 1] * i) % mod
            
        # Precompute inverses using Fermat's Little Theorem (O(log MOD))
        self.inv[n] = pow(self.fact[n], mod - 2, mod)
        for i in range(n - 1, -1, -1):
            self.inv[i] = (self.inv[i + 1] * (i + 1)) % mod

    def nCr(self, n: int, r: int) -> int:
        if r < 0 or r > n:
            return 0
        ans = self.fact[n] * self.inv[r] % self.mod
        ans = ans * self.inv[n - r] % self.mod
        return ans


# =======================================================================================
#                           6. STRING ALGORITHMS
# =======================================================================================
# Knuth-Morris-Pratt (KMP): String matching in O(N + M) time.
# Mathematical background: Uses an LPS (Longest Prefix Suffix) array to avoid redundant 
# comparisons by skipping over segments that we already know match.
# =======================================================================================

def compute_lps(pattern: str) -> List[int]:
    """Computes the Longest Prefix which is also Suffix array for KMP."""
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Finds all starting indices of `pattern` in `text`.
    Time Complexity: O(N + M) where N = len(text) and M = len(pattern).
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []
        
    lps = compute_lps(pattern)
    res = []
    
    i = 0 # index for text
    j = 0 # index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            res.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return res


# =======================================================================================
#                           7. TEST CASES & EXAMPLES
# =======================================================================================
def main():
    """
    Execution entry point demonstrating usage of all textbook templates.
    """
    print("=== DSU Demonstration ===")
    dsu = DSU(5)
    dsu.union(0, 1)
    dsu.union(2, 3)
    dsu.union(1, 2)
    print(f"Are 0 and 3 connected? {'Yes' if dsu.find(0) == dsu.find(3) else 'No'}")
    print(f"Are 0 and 4 connected? {'Yes' if dsu.find(0) == dsu.find(4) else 'No'}")
    print(f"Number of components: {dsu.components}")
    print()

    print("=== Fenwick Tree Demonstration ===")
    arr = [0, 1, 3, 5, 7, 9, 11] # 1-based logic internally
    fenwick = FenwickTree(len(arr))
    for i in range(1, len(arr) + 1):
        fenwick.update(i, arr[i-1])
    print(f"Sum of first 4 elements (1-3-5-7): {fenwick.query(4)}")
    print(f"Range sum [2, 5] (3-5-7-9): {fenwick.range_query(2, 5)}")
    print()

    print("=== Segment Tree Demonstration ===")
    data = [1, 3, 5, 7, 9, 11]
    seg_tree = SegmentTree(data)
    print(f"Sum of range [1, 3] (3+5+7): {seg_tree.query(1, 3)}")
    seg_tree.update(2, 10) # Change 5 to 10
    print(f"Sum of range [1, 3] after update (3+10+7): {seg_tree.query(1, 3)}")
    print()

    print("=== Dijkstra Demonstration ===")
    graph = [
        [(1, 4), (2, 1)],       # Node 0
        [(3, 1)],               # Node 1
        [(1, 2), (3, 5)],       # Node 2
        []                      # Node 3
    ]
    distances = dijkstra(4, graph, 0)
    print(f"Shortest distances from node 0: {distances}")
    print()
    
    print("=== Sieve of Eratosthenes ===")
    primes = sieve(30)
    print(f"Primes up to 30: {primes}")
    print()
    
    print("=== Combinatorics Demonstration ===")
    combo = Combinatorics(100)
    print(f"5 C 2 is: {combo.nCr(5, 2)}")
    print(f"10 C 3 modulo {MOD} is: {combo.nCr(10, 3)}")
    print()
    
    print("=== KMP String Search Demonstration ===")
    txt = "ABABDABACDABABCABAB"
    pat = "ABABCABAB"
    matches = kmp_search(txt, pat)
    print(f"Text: {txt}")
    print(f"Pattern: {pat}")
    print(f"Pattern found at indices: {matches}")
    print()


if __name__ == '__main__':
    # Uncomment the following line in a real competition to speed up I/O:
    # sys.setrecursionlimit(10**6)
    main()
