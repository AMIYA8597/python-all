# Competitive Programming Reference Guide (Python)

This document serves as an advanced reference for Competitive Programming (CP). It includes boilerplates, fast I/O configurations, and essential algorithm templates.

---

## 1. Fast I/O Configuration

### Why Fast I/O?
In CP, reading millions of lines of input using standard `input()` can cause Time Limit Exceeded (TLE) errors. Python's `sys.stdin.read` is drastically faster.

### The Standard CP Template

```python
import sys
import math
from collections import defaultdict, deque, Counter
import heapq

# Optimize recursion depth limit
sys.setrecursionlimit(1 << 25)

def solve():
    # Read all tokens from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # Process inputs here
    # Example: N = int(input_data[0])
    pass

if __name__ == '__main__':
    solve()
```

---

## 2. Bit Manipulation Cheat Sheet

Bit manipulation is crucial for optimizing subset generation, Fenwick trees, and low-level arithmetic.

- **Check if $i$-th bit is set**: `(n & (1 << i)) != 0`
- **Set $i$-th bit**: `n | (1 << i)`
- **Clear $i$-th bit**: `n & ~(1 << i)`
- **Toggle $i$-th bit**: `n ^ (1 << i)`
- **Check if power of 2**: `(n & (n - 1)) == 0` (and `n > 0`)
- **Isolate lowest set bit (LSB)**: `n & -n` (Core of Fenwick Tree)

---

## 3. Math Templates

### Sieve of Eratosthenes (Prime Generation)
Generates primes up to $N$ in $O(N \log \log N)$ time.

```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]
```

### Fast Exponentiation / Modular Arithmetic
Computes $x^y \pmod m$ in $O(\log y)$ time. (Python's built-in `pow(x, y, m)` does this efficiently in C, but it's good to know).

```python
def mod_pow(base, exp, mod):
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1: # If odd
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res
```

### Greatest Common Divisor (GCD)
$O(\log(\min(a, b)))$. Use `math.gcd(a, b)` normally, but this is the Euclidean algorithm:
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

---

## 4. Graph Templates

### Disjoint Set Union (DSU / Union-Find)
Essential for Kruskal's MST and cycle detection. $O(\alpha(N))$ nearly constant time per operation.

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
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
            return True
        return False
```

### Dijkstra's Shortest Path
Finds shortest paths from `start` to all other nodes. Time: $O(E \log V)$.

```python
def dijkstra(graph, start, n):
    # graph is a dict mapping node -> list of (neighbor, weight)
    distances = {node: float('inf') for node in range(n)}
    distances[start] = 0
    pq = [(0, start)] # (distance, node)
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Optimization: skip if we already found a shorter path
        if current_dist > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances
```

---

## Interview Questions & Advanced Concepts

1. **Question**: Why is path compression critical in Disjoint Set Union? What happens without it?
   **Answer**: Without path compression, the trees in the DSU can become degenerate (like a linked list), degrading `find` operations to $O(N)$ time. Path compression flattens the tree structure during `find` calls, dropping the amortized time to $O(\alpha(N))$ (inverse Ackermann function, effectively $O(1)$).
2. **Question**: Explain how you would find the lowest common ancestor (LCA) of two nodes in a tree efficiently in multiple queries.
   **Answer**: Use Binary Lifting. Precompute an array `up[u][i]` which stores the $2^i$-th ancestor of node $u$. This takes $O(N \log N)$ preprocessing. Each query can then be answered in $O(\log N)$ by jumping up in powers of 2.
3. **Common CP Mistake**: Modulo arithmetic on negative numbers.
   **Explanation**: In Python, `-5 % 3` is `1`. In C++/Java, it is `-2`. Always ensure you handle negative mods correctly if porting algorithms, though Python's implementation is often mathematically preferred.
