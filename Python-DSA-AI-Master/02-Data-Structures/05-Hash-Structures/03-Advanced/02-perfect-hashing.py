"""
# 02 - Perfect Hashing

## A. Concept Name
Perfect Hashing

## B. One-Sentence Definition
Perfect hashing is a hashing technique that guarantees O(1) worst-case lookup time for a static set of keys by completely eliminating collisions using a two-level hashing scheme.

## C. Why Does This Exist?
Standard hash tables have an average-case lookup time of O(1), but a worst-case of O(N) when many elements collide. For static sets of data (like reserved keywords in a compiler, or a fixed dictionary), we want an absolute guarantee of O(1) time without massive memory waste.

## D. Intuition
Instead of using linked lists (chaining) or probing when a collision happens, what if we just built a second, tiny, custom hash table *specifically* for the items that collided in that bucket? Since we know exactly which items collide, we can choose a perfect secondary hash function for them.

## E. Real-Life Analogy
Imagine assigning parking spaces (level 1 hash) to employees. Sometimes multiple employees are assigned the same lot (collision). Instead of making them park in the street (chaining), you buy a small private lot (level 2 hash) *just* for those specific colliding employees. You ensure this private lot is just big enough and numbered in a way that none of those specific employees collide again.

## F. Mental Model
Level 1 Hash Table maps N items into N buckets. (Some collisions occur).
Level 2 Hash Tables map the items within each bucket `i` into a smaller table of size `m = k_i^2`, where `k_i` is the number of collisions. By squaring the size, the probability of collisions drops so low that we can easily find a perfect collision-free secondary hash function.

## G. Visual Explanation
```text
Keys: [10, 22, 37, 40, 52, 60]

Level 1 Table (Size N=6):
Bucket 0: []
Bucket 1: []
Bucket 2: [22, 52] ---> Collided! Build Level 2 table of size 2^2 = 4.
Bucket 3: []
Bucket 4: [10, 40] ---> Collided! Build Level 2 table of size 2^2 = 4.
Bucket 5: [37, 60] ---> Collided! Build Level 2 table of size 2^2 = 4.

Level 2 Table for Bucket 2:
[ None, 52, 22, None ] (using custom secondary hash function)
```

## H. Formal Explanation
The FKS (Fredman, Komlós, and Szemerédi) scheme uses universal hashing. 
1. Choose a hash function $h_1$ from a universal family to map $N$ keys to $N$ buckets.
2. Let $n_i$ be the number of keys hashed to bucket $i$.
3. If $\sum_{i} n_i^2 > cN$ (for some constant $c$, usually 3 or 4), pick a different $h_1$ (this takes expected $O(1)$ tries).
4. For each bucket $i$, create a secondary hash table of size $n_i^2$.
5. Choose a secondary hash function $h_{2,i}$ that has zero collisions for those $n_i$ keys. Since the table size is squared, finding a collision-free function takes expected $O(1)$ tries.

## I. Mathematical Foundation (if applicable)
The birthday paradox tells us that a hash table of size $M$ will have collisions if we insert roughly $\sqrt{M}$ items. Inversely, if we have $n$ items, a table of size $n^2$ has a $>50\\%$ chance of being completely collision-free with a random hash function.
The total space is $\sum_{i=1}^{N} n_i^2$. Because $h_1$ is chosen from a universal family, the expected value of $\sum n_i^2$ is bounded by $2N$. Therefore, the total space is $O(N)$.

## J. From-Scratch Implementation (if applicable)
(See code below)

## K. Library / Production Implementation (if applicable)
GNU `gperf` is a widely used C/C++ program that generates perfect hash functions from a list of keywords. `cmph` (C Minimal Perfect Hashing Library) is another. Python's `dict` does not use perfect hashing because it is designed for dynamic data, not static.

## L. Trace (walk through example)
For keys `[10, 22, 37]`, `size = 3`.
1. `h1(k) = k % 3`. 
   `10 % 3 = 1` -> Bucket 1
   `22 % 3 = 1` -> Bucket 1
   `37 % 3 = 1` -> Bucket 1
   All 3 collided! `n_1 = 3`.
2. Bucket 1 gets a Level 2 table of size $3^2 = 9$.
3. We pick `h2(k) = k % 9` (simplified).
   `10 % 9 = 1`
   `22 % 9 = 4`
   `37 % 9 = 1` -> Collision! In real FKS, we would pick a different `h2` multiplier until no collisions occur.

## M. Complexity
- **Time**: 
  - Construction: Expected $O(N)$.
  - Lookup: Strict Worst-case $O(1)$ (exactly 2 hash evaluations).
- **Space**: 
  - Worst-case $O(N)$. Even though secondary tables are squared in size, the sum of squares of collisions across all buckets is bounded by $O(N)$ on average, and we enforce this during construction.

## N. Common Mistakes
- Trying to add or delete elements from a perfect hash table. Perfect hashing only works efficiently for **static** sets.
- Thinking the $O(N^2)$ space for a bucket makes the total space $O(N^2)$. The *sum* of those squares is bounded by $O(N)$.

## O. Common Confusions
- **Perfect vs Minimal Perfect Hashing**: Perfect hashing uses $O(N)$ space but the table size might be slightly larger than $N$ (empty slots exist). *Minimal* Perfect Hashing (MPHF) guarantees exactly $N$ slots for $N$ keys (no empty slots), saving even more space, but is harder to compute.

## P. When To Use
- Static dictionaries (e.g., spell checking).
- Reserved word lookups in compilers (lexers).
- Embedded systems with strict real-time guarantees where O(1) worst-case is mandatory.
- Routing tables in networking.

## Q. When NOT To Use
- Dynamic data (where you need to `insert()` or `delete()` after initialization).
- Extremely memory-constrained environments where the $O(N)$ overhead of the two-level structure and empty slots in secondary tables is unacceptable.

## R. Trade-offs
- **Construction Time vs Lookup Guarantee**: We spend expected $O(N)$ time (and sometimes more if unlucky with random hash functions) during initialization to gain a strict $O(1)$ guarantee for all future lookups.

## S. Debugging
- If lookups are failing, ensure that the exact secondary hash function $h_{2,i}$ chosen during construction is stored and used for bucket $i$ during lookup.

## T. Memory Hook
"Square the bucket for a perfect fit." (Level 2 tables are size $n^2$ to easily find a collision-free hash).

## U. Active Recall
1. Why do Level 2 tables have a size of $n^2$?
2. Does FKS perfect hashing require $O(N^2)$ memory overall?
3. Can I use perfect hashing for a database that frequently adds new users?

## V. Practice
Modify the provided implementation to actually pick a random `h2` function of the form `((a*k + b) % p) % m` until no collisions occur in Level 2.

## W. Interview Question
Q: Explain how the FKS (Fredman-Komlós-Szemerédi) scheme achieves O(N) total space despite using quadratic space ($n^2$) for the secondary hash tables.
A: By using a universal hash function for the first level, the probability of collisions is distributed such that the expected sum of the squares of the bucket sizes ($\sum n_i^2$) is bounded by $O(N)$. If we randomly pick a first-level hash function and the sum exceeds a threshold (like $3N$), we simply throw it away and pick another one. This takes expected $O(1)$ tries.

## X. Project Connection
In high-frequency trading or embedded systems programming, guaranteeing maximum latency is critical. A standard hash table's $O(N)$ worst-case lookup could cause a missed trade or system fault. Using a perfect hash table for static configurations ensures a strict, mathematical bound on lookup latency.
"""

import math
import random
from typing import List, Optional

class PerfectHashing:
    # A simplified conceptual demonstration
    def __init__(self, keys: List[int]):
        self.size = len(keys)
        # First level table: lists of elements that hashed to the same bucket
        self.level1: List[List[int]] = [[] for _ in range(self.size)]
        
        # Hash all keys to level 1
        for k in keys:
            idx = k % self.size
            self.level1[idx].append(k)

        # Second level table: each bucket has a size of square of number of elements to avoid collision
        self.level2: List[Optional[List[Optional[int]]]] = [None] * self.size
        
        for i, bucket in enumerate(self.level1):
            if bucket:
                m = len(bucket) ** 2
                self.level2[i] = [None] * m
                for k in bucket:
                    # In a real FKS, we find a hash function without collisions. Here we use modulo.
                    # This is a simplification and may fail if collisions still occur in secondary hash.
                    idx2 = k % m
                    self.level2[i][idx2] = k # type: ignore

    def lookup(self, key: int) -> bool:
        idx1 = key % self.size
        if self.level2[idx1] is None:
            return False
        
        m = len(self.level1[idx1]) ** 2
        idx2 = key % m
        return self.level2[idx1][idx2] == key # type: ignore

# Tests
def test_perfect_hashing():
    keys = [10, 22, 37, 40, 52, 60]
    ph = PerfectHashing(keys)
    
    assert ph.lookup(10) is True
    assert ph.lookup(37) is True
    assert ph.lookup(100) is False

if __name__ == "__main__":
    test_perfect_hashing()
    print("02-perfect-hashing.py tests passed successfully!")
