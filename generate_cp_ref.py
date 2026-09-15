import os

filepath = r"d:\work\python-all\12-Resources-References\01-Documentation\04-CP-Ref.md"
os.makedirs(os.path.dirname(filepath), exist_ok=True)

content = r"""# Competitive Programming in Python: The Master Reference

## 1. Introduction to Python in Competitive Programming
Competitive programming (CP) is fundamentally about problem-solving, but the environment imposes strict constraints on both time and memory. C++ has traditionally been the language of choice due to its execution speed and fine-grained control over resources. However, Python has seen a massive surge in popularity for CP, largely due to its succinctness, expressiveness, built-in large integer support, and rich standard library. The trade-off is execution speed. Standard CPython is significantly slower than compiled C++. To mitigate this, competitive programming platforms (like Codeforces, AtCoder, LeetCode, and HackerRank) provide PyPy—an alternative implementation of Python with a Just-In-Time (JIT) compiler. PyPy drastically reduces the performance gap, making Python a highly viable language for most contests.

This reference serves as a textbook-depth master cheat sheet for Python in Competitive Programming, covering everything from I/O optimization to advanced data structures, graph algorithms, and PyPy-specific idiosyncrasies. 

---

## 2. Fast I/O Strategies
In Python, standard `input()` and `print()` are notoriously slow and can cause Time Limit Exceeded (TLE) verdicts on problems with massive input or output. Efficient I/O is the first step to optimizing Python code for CP.

### 2.1 Reading Input
Instead of `input()`, use `sys.stdin.readline`. It reads an entire line, including the trailing newline character, much faster because it avoids the internal prompts and stripping inherent in `input()`.

```python
import sys
# Alias for fast reading
input = sys.stdin.readline

# Read a single integer
n = int(input())

# Read multiple integers on a single line
a, b, c = map(int, input().split())

# Read an array of integers
arr = list(map(int, input().split()))

# Read a string, stripping the trailing newline
s = input().rstrip('\n')
```

For problems with enormous inputs (e.g., millions of integers), reading the entire input into memory at once is the absolute fastest approach. This utilizes `sys.stdin.read().split()`:

```python
import sys

def solve():
    # Read everything from standard input as a single string and split by whitespace
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # We maintain an iterator over the input
    iterator = iter(input_data)
    
    # Now we can safely grab the next token
    try:
        n = int(next(iterator))
        arr = [int(next(iterator)) for _ in range(n)]
        # Process...
    except StopIteration:
        pass
```

### 2.2 Writing Output
Similarly, standard `print()` is slow because it formats strings, inserts spaces, and flushes the buffer frequently. `sys.stdout.write` is the preferred alternative for heavy output. Note that it only takes strings, so type conversion is mandatory.

```python
import sys
write = sys.stdout.write

# Output a string (must explicitly add newline)
write(str(n) + "\n")

# Fast output for an array of integers
write(" ".join(map(str, arr)) + "\n")
```

When dealing with a massive number of outputs on separate lines, it is often faster to collect the outputs in a list and print them joined by newlines at the end:

```python
results = [str(ans1), str(ans2), str(ans3)]
sys.stdout.write("\n".join(results) + "\n")
```

---

## 3. Recursion Limits and System Limits
Python restricts the recursion depth to prevent stack overflows, defaulting to 1000 in CPython. In graph problems (like deep DFS on a tree or linear graph), this limit is easily exceeded, leading to `RecursionError`.

### 3.1 CPython Recursion Limit
To bypass the default limit in CPython:

```python
import sys
sys.setrecursionlimit(1 << 25) # Set to ~33.5 million
```

### 3.2 PyPy Recursion Limit and Stack Size
PyPy handles recursion differently. Even if you increase the recursion limit via `sys.setrecursionlimit`, you might encounter a stack overflow at the OS level due to PyPy's internal memory management or the operating system's thread stack size limit (especially on Windows or restricted Linux containers like Codeforces). 

If you absolutely must use deep recursion in PyPy, you can spawn a new thread with an increased stack size. This is a common hack on Codeforces:

```python
import sys, threading
sys.setrecursionlimit(1 << 25)
threading.stack_size(1 << 27) # 128 MB stack

def main():
    # Your deep recursive DFS and logic here
    pass

if __name__ == '__main__':
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()
```

*Architectural advice:* The safest and most robust approach in CP is to convert recursive DFS to an iterative DFS using an explicit stack array. This entirely bypasses the recursion depth limits and avoids the PyPy thread stack overhead.

---

## 4. PyPy Compatibility and Python-Specific Optimization Hacks

### 4.1 Local vs. Global Variables
In Python, local variable access is significantly faster than global variable access. Locals are stored in a fixed-size array and accessed by index in the C backend, whereas globals require expensive dictionary lookups.

**Hack:** Wrap your entire solution inside a main function (e.g., `def solve():`) rather than writing it in the global scope. Pass necessary variables as arguments to helper functions.

### 4.2 List Comprehensions vs. For-Loops
List comprehensions are implemented purely in C and avoid the overhead of looking up and calling the `.append()` method repeatedly. They are significantly faster than equivalent for-loops.

```python
# Slow: Function call overhead on every iteration
res = []
for i in range(1000000):
    res.append(i * 2)

# Fast: Native C implementation
res = [i * 2 for i in range(1000000)]
```

### 4.3 Map and Filter
For applying a function to an entire list, `map()` is faster than a list comprehension. 

```python
# Very Fast
arr = list(map(int, string_array))
```

### 4.4 Multidimensional Arrays (1D vs 2D)
Initializing a 2D array requires care in Python:
```python
# CORRECT
grid = [[0] * M for _ in range(N)]

# WRONG (creates N references to the exact same row)
grid = [[0] * M] * N
```
For extreme performance, PyPy struggles to optimize lists of lists because they are fragmented in memory. Flattening a 2D array into a 1D array (`arr[r * M + c]` instead of `arr[r][c]`) yields significant speedups due to improved memory locality and fewer pointer dereferences.

### 4.5 Anti-Hash Tests in Codeforces
Python's built-in `hash()` function for integers is the identity function (`hash(x) == x`). Malicious test cases in Codeforces exploit this by feeding inputs that map to the same hash bucket in `set` or `dict`, degrading O(1) lookups to O(N) and causing TLE.

**Hack:** Use a randomized XOR wrapper around integers before hashing:
```python
import random
RANDOM_XOR = random.getrandbits(64)

class Wrapper:
    def __init__(self, val):
        self.val = val
    def __hash__(self):
        return self.val ^ RANDOM_XOR
    def __eq__(self, other):
        return self.val == other.val
```
Alternatively, avoid hash maps altogether by using sorting + binary search or direct array mapping if the domain is small enough.

---

## 5. Built-in Data Structures for CP

### 5.1 `collections.deque`
The Double-Ended Queue. Appending and popping from both ends is strictly O(1). Perfect for BFS. Never use a standard list `pop(0)` for BFS, as it is O(N) and will cause TLE.
```python
from collections import deque
q = deque([1, 2, 3])
q.append(4)      # O(1)
q.appendleft(0)  # O(1)
x = q.pop()      # O(1)
y = q.popleft()  # O(1)
```

### 5.2 `heapq` (Priority Queue)
Python provides an optimized min-heap implementation via the `heapq` module.
```python
import heapq
pq = []
heapq.heappush(pq, 5)
heapq.heappush(pq, 1)
min_val = heapq.heappop(pq) # Returns 1
```
To implement a max-heap, push the negation of the values:
```python
heapq.heappush(pq, -value)
max_val = -heapq.heappop(pq)
```
You can also push tuples to sort by multiple criteria: `heapq.heappush(pq, (distance, node_id))`.

### 5.3 `bisect` (Binary Search)
Provides O(log N) binary search on pre-sorted sequences.
```python
import bisect
arr = [1, 2, 4, 4, 5, 7]
# Find first position where to insert x to maintain sorted order
idx_left = bisect.bisect_left(arr, 4) # Returns 2

# Find rightmost position
idx_right = bisect.bisect_right(arr, 4) # Returns 4

# Number of occurrences of a target can be found via:
count = bisect.bisect_right(arr, 4) - bisect.bisect_left(arr, 4)
```

### 5.4 `collections.defaultdict` and `collections.Counter`
`defaultdict` initializes missing keys automatically. Crucial for building graph adjacency lists cleanly.
```python
from collections import defaultdict
adj = defaultdict(list)
adj[u].append(v)
adj[v].append(u)
```
`Counter` counts frequencies of elements in O(N).
```python
from collections import Counter
freq = Counter([1, 2, 2, 3]) # {2: 2, 1: 1, 3: 1}
```

---

## 6. Graph Algorithm Templates

### 6.1 Breadth-First Search (BFS)
Used for traversing graphs level by level, or finding unweighted shortest paths. Time: O(V + E).
```python
from collections import deque

def bfs(start, adj, n):
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

### 6.2 Iterative Depth-First Search (DFS)
Bypasses PyPy recursion limits natively. Time: O(V + E).
```python
def iterative_dfs(start, adj, n):
    visited = [False] * (n + 1)
    stack = [start]
    
    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            # Pre-order logic here
            for v in adj[u]:
                if not visited[v]:
                    stack.append(v)
```

### 6.3 Dijkstra's Algorithm
Single-source shortest path for graphs with non-negative edge weights. Time: O((V + E) log V).
```python
import heapq

def dijkstra(start, adj, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)] # (distance, node)
    
    while pq:
        d, u = heapq.heappop(pq)
        
        # Optimization: Ignore stale queue entries
        if d > dist[u]:
            continue
            
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    return dist
```

### 6.4 Bellman-Ford Algorithm
Detects negative weight cycles and finds shortest paths. Time: O(V * E).
```python
def bellman_ford(start, edges, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    
    # Relax all edges V - 1 times
    for _ in range(n - 1):
        for u, v, weight in edges:
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                
    # Detect negative cycle
    for u, v, weight in edges:
        if dist[u] != float('inf') and dist[u] + weight < dist[v]:
            return None # Negative cycle detected
            
    return dist
```

### 6.5 Floyd-Warshall Algorithm
All-pairs shortest path. Time: O(V^3). Best for dense graphs with V <= 400.
```python
def floyd_warshall(dist_matrix, n):
    # dist_matrix[i][j] is initialized to weight of edge(i, j), or float('inf')
    # dist_matrix[i][i] is initialized to 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i][k] + dist_matrix[k][j] < dist_matrix[i][j]:
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
```

### 6.6 Topological Sort (Kahn's Algorithm)
Used for scheduling tasks or checking for cycles in Directed Acyclic Graphs (DAGs). Time: O(V + E).
```python
from collections import deque

def topo_sort(adj, n):
    indegree = [0] * (n + 1)
    for u in range(1, n + 1):
        for v in adj[u]:
            indegree[v] += 1
            
    q = deque([i for i in range(1, n + 1) if indegree[i] == 0])
    order = []
    
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
                
    if len(order) != n:
        return [] # Cycle detected, not a DAG
    return order
```

### 6.7 Minimum Spanning Tree (Kruskal's Algorithm)
Uses DSU to greedily construct an MST. Time: O(E log E).
```python
def kruskal(edges, n):
    # edges is a list of tuples: (weight, u, v)
    edges.sort()
    dsu = DSU(n)
    mst_weight = 0
    mst_edges = []
    
    for weight, u, v in edges:
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            mst_weight += weight
            mst_edges.append((u, v, weight))
            
    return mst_weight, mst_edges
```

---

## 7. Trees and Advanced Data Structures

### 7.1 Disjoint Set Union (DSU) / Union-Find
Maintains a collection of disjoint sets. Supports union and find operations in almost O(1) time (amortized O(Inverse Ackermann)). This implementation uses path compression and union by size.
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.components = n
        
    def find(self, i):
        if self.parent[i] == i:
            return i
        # Path compression
        self.parent[i] = self.find(self.parent[i]) 
        return self.parent[i]
        
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by size
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.components -= 1
            return True
        return False
```

### 7.2 Fenwick Tree (Binary Indexed Tree)
Calculates prefix sums and point updates in O(log N). Highly memory efficient. Uses 1-based indexing.
```python
class FenwickTree:
    def __init__(self, size):
        # 1-based indexing
        self.tree = [0] * (size + 1)
        
    def add(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            # Add lowest set bit
            i += i & (-i)
            
    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            # Remove lowest set bit
            i -= i & (-i)
        return s
        
    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)
```

### 7.3 Segment Tree (Point Update, Range Query)
More versatile than Fenwick trees. Can handle arbitrary associative operations (e.g., Min, Max, GCD). Iterative segment trees are much faster in Python than recursive ones. Time: O(log N) per query/update.
```python
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        # Build the tree
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i << 1] + self.tree[i << 1 | 1]
            
    def update(self, pos, value):
        # Point update
        pos += self.n
        self.tree[pos] = value
        while pos > 1:
            self.tree[pos >> 1] = self.tree[pos] + self.tree[pos ^ 1]
            pos >>= 1
            
    def query(self, left, right):
        # Query interval [left, right]
        res = 0
        left += self.n
        right += self.n + 1 # +1 to make it inclusive
        while left < right:
            if left & 1:
                res += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                res += self.tree[right]
            left >>= 1
            right >>= 1
        return res
```

### 7.4 Segment Tree with Lazy Propagation (Range Update, Range Query)
Used when updates occur over an entire interval. This requires a recursive approach.
```python
class LazySegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(data, 1, 0, self.n - 1)

    def build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self.build(data, 2 * node, start, mid)
            self.build(data, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def push(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2 * node] += self.lazy[node]
                self.lazy[2 * node + 1] += self.lazy[node]
            self.lazy[node] = 0

    def update_range(self, node, start, end, l, r, val):
        self.push(node, start, end)
        if start > end or start > r or end < l:
            return
        if start >= l and end <= r:
            self.tree[node] += (end - start + 1) * val
            if start != end:
                self.lazy[2 * node] += val
                self.lazy[2 * node + 1] += val
            return
        mid = (start + end) // 2
        self.update_range(2 * node, start, mid, l, r, val)
        self.update_range(2 * node + 1, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, node, start, end, l, r):
        if start > end or start > r or end < l:
            return 0
        self.push(node, start, end)
        if start >= l and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self.query_range(2 * node, start, mid, l, r)
        p2 = self.query_range(2 * node + 1, mid + 1, end, l, r)
        return p1 + p2
```

### 7.5 Trie (Prefix Tree)
Efficient for string matching, dictionary prefix queries, and XOR-based bitwise queries on arrays. Time: O(L) where L is string length.
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0 # Number of words passing through this node

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True
        
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

---

## 8. Mathematics and Number Theory

### 8.1 Greatest Common Divisor and Least Common Multiple
Always use the built-in C-optimized functions.
```python
import math
gcd = math.gcd(a, b)
# For Python 3.9+
lcm = math.lcm(a, b)
# Pre-3.9 fallback: lcm = (a * b) // math.gcd(a, b)
```

### 8.2 Fast Modular Exponentiation
Python's built-in `pow(base, exp, mod)` is implemented in C using binary exponentiation and runs in O(log(exp)) time. It is highly optimized and should always be used for CP.
```python
ans = pow(base, exp, mod)
```

### 8.3 Modular Multiplicative Inverse
Used to perform division under a modulo. Based on Fermat's Little Theorem (requires `mod` to be prime):
`a^(p-2) ≡ a^-1 (mod p)`
```python
mod = 10**9 + 7
inverse = pow(a, mod - 2, mod)
```
In Python 3.8+, `pow()` directly supports modular inverse (even if mod is not prime, given they are coprime):
```python
inverse = pow(a, -1, mod)
```

### 8.4 Sieve of Eratosthenes
Generates primes up to `N` in O(N log log N) time.
```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            # Mark all multiples starting from i*i
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]
```

### 8.5 Prime Factorization (O(sqrt N))
```python
def prime_factors(n):
    factors = []
    # Divide out 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Divide odd numbers
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    # If n becomes a prime > 2
    if n > 2:
        factors.append(n)
    return factors
```

### 8.6 Combinatorics (nCr % MOD)
For competitive programming, combinatorial queries modulo `M` frequently require precomputing factorials and inverse factorials in O(N) to answer multiple `nCr` queries in O(1).
```python
MAX = 100005
MOD = 10**9 + 7

fact = [1] * MAX
invFact = [1] * MAX

# Precompute factorials
for i in range(1, MAX):
    fact[i] = (fact[i - 1] * i) % MOD
    
# Precompute inverse factorials
invFact[MAX - 1] = pow(fact[MAX - 1], MOD - 2, MOD)
for i in range(MAX - 2, -1, -1):
    invFact[i] = (invFact[i + 1] * (i + 1)) % MOD

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return fact[n] * invFact[r] % MOD * invFact[n - r] % MOD
```

---

## 9. String Algorithms

### 9.1 Z-Algorithm
Finds all occurrences of a pattern in a text in O(N + M). The Z-array stores the length of the longest substring starting from `i` which is also a prefix of the string.
```python
def get_z_array(s):
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z
```

### 9.2 Knuth-Morris-Pratt (KMP) Algorithm
O(N + M) substring search via the Longest Prefix Suffix (LPS) array.
```python
def compute_lps(pattern):
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

def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    i = j = 0
    occurrences = []
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return occurrences
```

---

## 10. Bitwise Operations for CP
Bitwise operations are incredibly fast and memory-efficient. They are extensively used for subset generation (bitmasking), state representation in Dynamic Programming (Bitmask DP), and low-level optimizations.

### 10.1 Bitwise Basics
- `x << y`: Shift left (equivalent to `x * 2^y`)
- `x >> y`: Shift right (equivalent to `x // 2^y`)
- `x & y`: Bitwise AND
- `x | y`: Bitwise OR
- `x ^ y`: Bitwise XOR
- `~x`: Bitwise NOT (in Python, `~x == -x - 1`)

### 10.2 Common Tricks and Bit Hacks
- **Check if i-th bit is set:** `(x & (1 << i)) != 0`
- **Set i-th bit:** `x |= (1 << i)`
- **Clear i-th bit:** `x &= ~(1 << i)`
- **Toggle i-th bit:** `x ^= (1 << i)`
- **Extract lowest set bit (LSB):** `x & -x` (Fundamental to Fenwick Trees)
- **Clear lowest set bit:** `x & (x - 1)` (Brian Kernighan's Algorithm)
- **Check if integer is power of 2:** `x > 0 and (x & (x - 1)) == 0`
- **Count set bits:** `x.bit_count()` (Available natively in Python 3.10+)

### 10.3 Bitmask Subsets Generation
Iterating over all subsets of an N-element set in O(2^N):
```python
n = 3 # Elements 0, 1, 2
for mask in range(1 << n):
    subset = []
    for i in range(n):
        if mask & (1 << i):
            subset.append(i)
    print(bin(mask), subset)
```

Iterating over all submasks of a given mask in O(3^N) across all masks:
```python
mask = 0b1011
submask = mask
while submask > 0:
    print(bin(submask))
    submask = (submask - 1) & mask
```

---

## 11. Useful Python Standard Library Modules

### 11.1 `itertools`
Provides highly optimized C functions for iterators.
- `itertools.permutations(iterable, r=None)`: O(N!) permutation generator.
- `itertools.combinations(iterable, r)`: O(nCr) combination generator.
- `itertools.accumulate(iterable, func=operator.add)`: Quick prefix sums or prefix max/min.

```python
from itertools import accumulate
arr = [1, 2, 3, 4]
pref_sum = list(accumulate(arr)) # [1, 3, 6, 10]
pref_max = list(accumulate(arr, max)) # Prefix maximums
```

### 11.2 `functools`
- `functools.lru_cache(maxsize=None)` and `functools.cache`: Memoization decorators that drastically simplify top-down Dynamic Programming.

```python
from functools import cache

@cache
def dp(i, w):
    if i == 0 or w == 0: return 0
    if weights[i-1] > w:
        return dp(i-1, w)
    return max(dp(i-1, w), values[i-1] + dp(i-1, w - weights[i-1]))
```
*Warning on Codeforces/PyPy:* While `@cache` is clean, in PyPy `sys.setrecursionlimit` combined with deep `@cache` recursive calls can cause heavy memory overhead and Time/Memory Limit Exceeded compared to iterative tabulation DP or manual dictionary memoization.

---

## 12. Conclusion and Final Advice
To succeed with Python in Competitive Programming, embrace the language's abstractions but respect the interpreter's limits:
1. **Always use Fast I/O:** Default to `sys.stdin.readline` and `sys.stdout.write`.
2. **Prefer PyPy:** Submit solutions via PyPy3 whenever available for an instant 5x-20x speedup.
3. **Write Iterative Algorithms:** Avoid deep recursion in Python. If you must use a deep DFS tree, simulate the call stack yourself or use iterative pre/post-order traversal structures.
4. **Local Variables are Kings:** Encapsulate your logic inside a `solve()` function. Global lookups kill performance.
5. **Leverage C-Backend Built-ins:** Operations like `sum()`, `max()`, `min()`, `map()`, and `list.sort()` (Timsort) are implemented in highly optimized C. Always prefer them over manual Python loops.
6. **Flatten Data Structures:** Use 1D arrays for multidimensional data when raw speed is critical.

Master these templates, recognize Python's computational bottlenecks, and you will find Python to be an exceptionally powerful, fast, and expressive language capable of solving the hardest algorithmic challenges.
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Generated CP Reference successfully.")
