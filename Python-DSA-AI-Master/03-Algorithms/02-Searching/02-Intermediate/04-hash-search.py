r"""
# Hash Search: Theory, Engineering Mechanics, and Practical Applications

## A. Concept Name
Hash Search (also known as Hash-Based Direct Searching or Hash Table Lookup).

## B. One-Sentence Definition
Hash Search is a constant expected-time, non-comparison search algorithm that maps arbitrary keys directly to bucket indices in a bounded array via a deterministic mathematical hash function, resolving key collisions through open addressing or separate chaining.

## C. Why Does This Exist? (What problem does it solve?)
Comparison-based search algorithms are mathematically bounded by the Information Theoretic Lower Bound:
- **Linear Search** requires $O(N)$ time because it inspects elements sequentially without pre-existing structural knowledge.
- **Binary Search** achieves $O(\log N)$ time, but strictly mandates that data be pre-sorted ($O(N \log N)$ upfront sorting cost) and stored in contiguous memory supporting $O(1)$ random access. Furthermore, updating a sorted array requires $O(N)$ element shifts.
- **Balanced Search Trees** (AVL, Red-Black Trees, B-Trees) support search, insertion, and deletion in $O(\log N)$ time, but still incur logarithmic pointer-chasing latency at scale.

**The Direct Addressing Dilemma:**
If we had infinite memory, we could assign every possible key $k$ directly to slot $T[k]$ in an array of size equal to the entire key universe $|U|$. For 64-bit integer keys or 20-character strings, $|U| \ge 2^{64}$ (or $26^{20}$), demanding billions of gigabytes of RAM—completely impossible.

**Hash Search solves this fundamental dilemma** by mapping the enormous key universe $|U|$ into a compact slot space $m = O(N)$ using a hash function $h: U \to \{0, 1, \dots, m-1\}$. By carefully managing the inevitable collisions (where $h(k_1) = h(k_2)$), Hash Search provides:
1. **$O(1)$ Average-Case Retrieval**: Search, insert, and delete operations execute in constant expected time regardless of the dataset size $N$.
2. **Unordered Storage**: Keys do not require a natural total ordering ($\le$), only a deterministic equality test ($==$) and a valid hash code.
3. **Dynamic Scalability**: Amortized dynamic rehashing allows the underlying storage to expand or shrink seamlessly as data volume fluctuates.

## D. Intuition & Real-Life Analogy
- **The Coat Check / Valet Parking Ticket**: When you hand your coat to an attendant at a theater, they do not scan through all 500 coats sequentially when you return ($O(N)$). Instead, they hand you a ticket numbered `42`. When you return, they look at ticket `42` and walk straight to hook `42` ($O(1)$). The ticket number is the hash index.
- **Post Office P.O. Boxes**: A town with 50,000 residents maps incoming mail to 2,000 physical P.O. boxes. The box number is computed from the recipient's identifier. If two people share a box (a collision), they both check the contents inside that specific box (separate chaining).
- **Dewey Decimal System**: Libraries categorize millions of books into distinct shelf classifications based on subject codes. Instead of wandering through the whole library, you compute the subject code and head straight to that aisle.

## E. Mental Model
The Hash Search pipeline functions as a three-stage deterministic transformer:
```text
  Raw Key: "apple"
      |
      v  Step 1: Deterministic Hash Function (e.g., SipHash / MurmurHash)
  Hash Code: 0x5a3b7c89 (Large 32-bit / 64-bit Integer)
      |
      v  Step 2: Compression Function (hash_code % Table_Capacity m)
  Bucket Index: 0x5a3b7c89 % 8 = 1
      |
      v  Step 3: Table Array Access & Collision Resolution
  Table Array [Size m = 8]
  +-------+
  | [0]   | -> Empty (None)
  +-------+
  | [1]   | -> [("apple", 100)] -> [("cherry", 250)]  <-- Separate Chaining
  +-------+    (Compare key == "apple" -> FOUND! Value = 100)
  | [2]   | -> Empty (None)
  +-------+
  | [3]   | -> [("banana", 200)]
  +-------+
  | [4]   | -> Empty (None)
  +-------+
  | [5]   | -> Empty (None)
  +-------+
  | [6]   | -> [("date", 400)]
  +-------+
  | [7]   | -> Empty (None)
  +-------+
```
If two distinct keys produce the same bucket index (e.g., $h(\text{"apple"}) \pmod 8 == h(\text{"cherry"}) \pmod 8 == 1$), they collide. The algorithm must resolve this collision either by chaining both items into an auxiliary list at bucket 1, or by probing to an alternate empty slot in the table array.

## F. Formal Technical Explanation
Hash search operates over a hash table comprising an array $T$ of $m$ buckets, a hash function $h: K \to \{0, \dots, m-1\}$, and an equality predicate $\sim$.

### 1. The Hash Function and Compression
A robust hash function satisfies two foundational properties:
- **Determinism**: For any key $k$, evaluating $h(k)$ multiple times during program execution must always yield the exact same integer value.
- **Uniform Distribution**: The function must distribute keys evenly across all $m$ slots, ensuring that each slot is equally likely to be selected independently of where other keys fall (the Simple Uniform Hashing Assumption, SUHA).

Typical compression maps a 64-bit integer hash code $H$ to slot index $i \in [0, m-1]$:
$$i = H \pmod m \quad \text{or} \quad i = H \ \& \ (m - 1) \quad (\text{when } m = 2^p)$$

### 2. Collision Resolution Strategies
Because the key universe $|U| \gg m$, Dirichlet's Box (Pigeonhole) Principle proves that collisions are mathematically guaranteed. Two primary paradigms resolve collisions:

#### Paradigm A: Separate Chaining (Open Hashing / Closed Addressing)
Each bucket in table $T$ contains a pointer to an auxiliary linked list (or balanced binary tree) storing all key-value entries that hashed to that bucket:
- **Search Algorithm**:
  1. Compute bucket index $i = h(k) \pmod m$.
  2. Sequentially scan the linked list at $T[i]$.
  3. If node key $k_{\text{node}} == k$, return the associated value (Successful Search).
  4. If the list terminates without a match, return Sentinel/KeyError (Unsuccessful Search).
- **Resizing**: When the load factor $\alpha = \frac{n}{m} > \alpha_{\max}$ (typically $0.75$), allocate a new array of size $2m$, recompute all bucket indices, and re-link all nodes.

#### Paradigm B: Open Addressing (Closed Hashing / Open Addressing)
All entries are stored directly inside the array $T$ itself ($m \ge n$). When collision occurs, a deterministic probe sequence $h(k, 0), h(k, 1), h(k, 2), \dots, h(k, m-1)$ systematically searches for the target key or an empty slot:
1. **Linear Probing**: $h(k, i) = (h(k) + i) \pmod m$.
   - *Advantage*: Exceptional CPU cache locality.
   - *Disadvantage*: Prone to **primary clustering** (long contiguous blocks of occupied cells build up, drastically increasing average probe lengths).
2. **Quadratic Probing**: $h(k, i) = (h(k) + c_1 i + c_2 i^2) \pmod m$.
   - Eliminates primary clustering, but suffers from **secondary clustering** (keys with identical initial hash values trace identical probe sequences).
3. **Double Hashing**: $h(k, i) = (h_1(k) + i \cdot h_2(k)) \pmod m$, where $h_2(k)$ is coprime to $m$.
   - Virtually eliminates both forms of clustering.
4. **Robin Hood Hashing**: An open-addressing variant where colliding keys are ordered by their Distance from Ideal Bucket (DIB). If an inserted key has a larger DIB than the current resident, the newcomer steals the slot and the resident is displaced, equalizing probe variance.

### 3. The Tombstone Invariant in Open Addressing
In open addressing, deleting an element by setting its cell to `None` destroys the probe sequence chain. Subsequent searches for elements inserted *after* that slot would encounter `None` and prematurely terminate, wrongly reporting that the existing element is missing. Therefore, deleted slots must be marked with a special sentinel called a **Tombstone** (`_DELETED`). A search continues past tombstones, whereas an insertion can overwrite tombstones.

## G. Mathematical Foundation
Let $n$ denote the number of stored keys, and $m$ denote the number of table slots.
The **Load Factor** is defined as:
$$\alpha = \frac{n}{m}$$

### 1. Separate Chaining Analysis (Under SUHA)
Under the Simple Uniform Hashing Assumption, the probability of any key hashing to bucket $i$ is $\frac{1}{m}$.
The expected length of the chain at bucket $i$ is:
$$E[n_i] = \sum_{j=1}^n \frac{1}{m} = \frac{n}{m} = \alpha$$

- **Unsuccessful Search**: The algorithm hashes to bucket $i$ ($O(1)$) and scans the entire chain of expected length $\alpha$:
  $$T_{\text{unsuccessful}}(\text{chaining}) = \Theta(1 + \alpha)$$
- **Successful Search**: The target key is equally likely to be any of the $n$ keys. The expected number of elements examined before reaching the target is $1 + \frac{\alpha}{2} - \frac{\alpha}{2n}$:
  $$T_{\text{successful}}(\text{chaining}) = \Theta\left(1 + \frac{\alpha}{2}\right) = \Theta(1 + \alpha)$$
As long as $m = \Omega(n)$, $\alpha = O(1)$, rendering both search operations $O(1)$ on average.

### 2. Open Addressing Analysis (Under Uniform Hashing)
In open addressing, each probe is an independent Bernoulli trial with success probability $1 - \alpha$ (finding an empty cell).
- **Unsuccessful Search**: The expected number of probes $E[P]$ is the mean of a geometric distribution:
  $$E[P] = \sum_{i=1}^\infty i \cdot \alpha^{i-1}(1 - \alpha) = \frac{1}{1 - \alpha}$$
  *Example*: At $\alpha = 0.5$, expected probes $\le \frac{1}{1 - 0.5} = 2$. At $\alpha = 0.9$, expected probes $\le 10$.
- **Successful Search**: By integrating over the insertion history:
  $$E[P] \le \frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$$
  *Example*: At $\alpha = 0.5$, expected probes $\le \frac{1}{0.5} \ln(2) \approx 1.386$.

### 3. The Birthday Paradox and Collision Frequency
Why do hash tables collide far sooner than intuition expects?
By the Birthday Problem, given $m$ slots and $k$ uniformly distributed keys, the probability of at least one collision is:
$$P(\text{collision}) \approx 1 - e^{-\frac{k(k-1)}{2m}}$$
For $P(\text{collision}) \ge 0.5$, we require:
$$k \approx \sqrt{2m \ln 2} \approx 1.177 \sqrt{m}$$
In a table with $m = 10,000$ slots, the probability of a collision exceeds 50% after inserting only **118 keys**! This mathematical reality proves that collision resolution is not a rare edge case—it is an intrinsic operational requirement.

## H. Complexity Analysis (Time, Space, Memory)
| Operation | Best Case | Average Case (SUHA) | Worst Case (All Collide) | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Search (Chaining)** | $O(1)$ | $O(1 + \alpha) = O(1)$ | $O(N)$ (degrades to linked list) | $O(N + m)$ |
| **Search (Open Addressing)**| $O(1)$ | $O\left(\frac{1}{1-\alpha}\right) = O(1)$ | $O(N)$ (scans full array) | $O(m)$ contiguous |
| **Insert** | $O(1)$ | $O(1)$ amortized | $O(N)$ (worst collision or resize) | $O(1)$ auxiliary |
| **Delete** | $O(1)$ | $O(1)$ | $O(N)$ | $O(1)$ auxiliary |

### Hardware & Cache Dynamics:
- **Separate Chaining**: Incurs substantial CPU cache misses because linked list nodes are allocated independently on the heap. Accessing each subsequent node in a chain requires traversing a raw heap pointer, triggering an L1/L2 cache stall.
- **Open Addressing (Linear Probing)**: Features near-perfect spatial cache locality. Because array slots are contiguous in virtual memory, reading slot $i$ triggers the hardware prefetcher to fetch the entire 64-byte cache line containing slots $i+1, i+2, \dots$. This makes linear probing substantially faster in wall-clock time on modern CPUs despite primary clustering.
- **CPython Dict Optimization (PEP 468 & Python 3.6+)**: Standard dictionaries use a compact representation consisting of a sparse index array (`indices`) of 8-bit, 16-bit, or 32-bit integers, pointing to a dense array (`entries`) storing `[hash, key, value]`. This reduced memory consumption by 20% to 25% while preserving key insertion order.

## I. Common Mistakes & Pitfalls
1. **Mutating Keys In-Place**:
   Using a mutable object (e.g., custom class without immutable hashing) as a key and then mutating an attribute that alters its `__hash__` value. The object's bucket location is now out of sync with its new hash, rendering it permanently unsearchable:
   ```python
   # DANGEROUS BUG
   class User:
       def __init__(self, uid): self.uid = uid
       def __hash__(self): return hash(self.uid)
       def __eq__(self, o): return isinstance(o, User) and self.uid == o.uid
   
   u = User(101)
   table[u] = "admin"
   u.uid = 999  # BUG: Mutating key! Hash changes, lookup table[u] now fails!
   ```
2. **Violating the Hash-Equality Invariant**:
   The golden rule of hashing in Python:
   $$\text{If } a == b \implies \text{hash}(a) == \text{hash}(b)$$
   If you override `__eq__` without overriding `__hash__`, Python sets `__hash__ = None` to protect you. If you provide custom implementations where two equal objects produce different hash codes, they land in different buckets, breaking search.
3. **Deleting Without Tombstones in Open Addressing**:
   Setting an array slot directly to `None` upon deletion breaks the probe sequence for keys placed further down the cluster, causing lookups to prematurely abort.
4. **Ignoring Load Factor Growth**:
   Failing to trigger dynamic rehashing as the load factor $\alpha \to 1.0$. In open addressing, search time approaches $\infty$ as $\alpha \to 1.0$.
5. **Hash Flooding DoS Vulnerability**:
   If an external adversary can predict the hash function (e.g., non-randomized polynomial string hash), they can submit $10,000$ keys that all hash to the same bucket. The hash table degenerates into an $O(N)$ linked list, degrading an entire web server from $10,000 \times O(1)$ lookups to $10,000 \times O(N) = O(N^2)$ operations, causing 100% CPU starvation. Python protects against this using **SipHash-2-4** with a secret per-process randomized seed.

## J. Common Confusions
- **Hash Search vs. Binary Search**: Hash search is $O(1)$ expected time and unordered; it cannot answer range queries ("find all users aged 20 to 30"), cannot find predecessors or successors, and cannot retrieve the minimum/maximum key without an $O(N)$ scan. Binary search requires sorted data ($O(\log N)$ time), but natively excels at range queries and order statistics.
- **Hash Search vs. Direct Addressing**: Direct addressing allocates an array index for every conceivable key in universe $U$ (massive memory waste). Hash search uses a hash function to compress $U$ into $m$ slots ($m \ll |U|$), accepting occasional collisions to achieve optimal memory utilization.
- **Hash Search vs. Trie**: A Trie searches in $O(L)$ time, where $L$ is the key length (number of characters), and natively supports prefix auto-completion. Hash search also takes $O(L)$ to compute the initial hash code of a string, but only takes $O(1)$ to look up the bucket, yet cannot perform prefix searches.
- **Hash Code vs. Bucket Index**: A hash code is an unbounded 32-bit or 64-bit integer produced by the hash function. The bucket index is the compressed slot number $0 \le i < m$ obtained via `hash_code % m` or `hash_code & (m - 1)`.

## K. When To Use It
- Exact key lookups where sub-millisecond $O(1)$ latency is critical.
- Associative dictionary mappings (key $\to$ value pairs).
- Set membership verification and deduplication (`x in seen_set`).
- Frequency counting, histograms, and caching (e.g., Memoization, LRU caches).
- Graph adjacency representations using hash maps of neighbor sets.

## L. When NOT To Use It
- **Ordered / Range Queries**: When queries involve inequalities ($k_1 \le \text{key} \le k_2$), finding nearest neighbors, or in-order traversals (use B+ Trees, AVL Trees, or Skip Lists).
- **Deterministic Worst-Case Hard Real-Time Systems**: In aerospace, medical robotics, or pacemakers, an occasional $O(N)$ collision spike or rehashing pause could violate hard real-time deadlines (use Perfect Hashing or Worst-Case $O(\log N)$ Red-Black Trees).
- **Ultra-Small Collections ($N \le 16$)**: The CPU instruction overhead of computing hashes and allocating bucket tables often makes a simple contiguous array scan (Linear Search) faster in wall-clock time.
- **Memory-Constrained Microcontrollers**: Hash tables maintain empty slots ($25\%-50\%$ load factor slack) and bucket pointers, consuming $2\times$ to $4\times$ the memory of packed arrays.

## M. Trade-offs
| Dimension | Separate Chaining | Linear Probing (Open Addressing) | Robin Hood Hashing | Balanced BST |
| :--- | :--- | :--- | :--- | :--- |
| **Cache Locality** | Poor (Heap pointer chasing) | Optimal (Contiguous memory) | Optimal (Contiguous memory) | Moderate to Poor |
| **Max Load Factor**| Can exceed $\alpha > 1.0$ | Strictly $\alpha < 1.0$ (rehash at $0.66$)| Strictly $\alpha < 1.0$ (rehash at $0.90$) | N/A |
| **Deletion Cost** | Simple list node unlinking | Complex (Requires Tombstones)| Complex (Backward shifting) | Moderate (Tree rebalancing) |
| **Variance of Probes**| High on collisions | Very High (Primary clustering) | Exceptionally Low | Guaranteed $O(\log N)$ |
| **Memory Overhead**| Node pointers per entry | Empty slot slack memory | Empty slot slack memory | Two child pointers per node |

## N. Debugging Tips
- **Inspect Bucket Collision Histograms**: If performance suddenly tanks, print `[len(bucket) for bucket in table.buckets]`. If one bucket has 500 items and the rest are empty, your hash function is defective or you are being subjected to a hash collision attack.
- **Verify `__eq__` and `__hash__` Synchrony**: Write automated test assertions ensuring that any two generated test objects that satisfy `a == b` also satisfy `hash(a) == hash(b)`.
- **Track Probe Sequences**: During open-addressing debugging, log each probe step: `[DEBUG] key='user_42', step=0, slot=3 (occupied) -> step=1, slot=4 (tombstone) -> step=2, slot=5 (EMPTY, inserted)`.
- **Tombstone Auditing**: Ensure that probe loops terminate on genuine `None` (empty), but continue traversing through `_DELETED` tombstones.

## O. Memory Hook
**"Hash to Index, Jump Direct — If Collided, Probe or Chain to Correct."**
Picture a coat-check attendant reading your ticket number, walking directly to the hook, and if someone else's coat is already hanging on the same hook, checking the tags attached along the hook's hanger chain.

## P. Active Recall Questions
1. Why does open addressing fail if deletions are performed by replacing the slot with `None` instead of a tombstone?
2. Under what condition does separate chaining achieve $O(1)$ expected time search, and what happens when all keys hash to the same value?
3. How does the Birthday Paradox explain why collisions occur when a hash table is only $\approx \sqrt{m}$ full?
4. What is the fundamental invariant between Python's `__eq__` and `__hash__` methods?
5. Why does Python use SipHash instead of a fast polynomial hash for string keys?

## Q. Interview Questions & Answers

### Question 1: How do you design and implement an LRU (Least Recently Used) Cache with $O(1)$ search, insert, and eviction?
**Answer**:
Combine a **Hash Map** with a **Doubly Linked List**:
1. The Doubly Linked List maintains chronological access order. The most recently accessed item sits at the `head`; the least recently accessed item sits at the `tail`.
2. The Hash Map stores `key -> NodeRef` pointers.
3. **Search (`get`)**: Look up the key in the Hash Map in $O(1)$ to retrieve the `NodeRef`. Unlink the node from its current position in the Doubly Linked List and splice it immediately behind the `head` ($O(1)$ pointer operations). Return node value.
4. **Insert (`put`)**: If key exists, update value and move node to head. If new, allocate node, put into Hash Map, and prepend to head. If capacity is exceeded, evict `tail.prev` from both the linked list and the Hash Map in $O(1)$.

### Question 2: What is Robin Hood Hashing, and why does it drastically improve search latency compared to standard linear probing?
**Answer**:
In standard linear probing, early-inserted keys stay close to their ideal bucket, while later-colliding keys are shoved far down the table, creating high variance in probe sequence lengths (some lookups take 1 probe, others take 30 probes).
Robin Hood Hashing equalizes probe lengths based on the principle of *"taking from the rich and giving to the poor"*:
- Each entry records its **Probe Count** (Distance from Ideal Bucket, DIB).
- When inserting a key with DIB $d_{\text{new}}$, if it encounters an occupied slot whose resident has a smaller DIB $d_{\text{resident}} < d_{\text{new}}$ ("richer" resident with fewer probes), the newcomer **steals** that slot and evicts the resident.
- The displaced resident now continues probing down the table with its updated DIB.
- **Result**: The maximum probe length and probe variance are drastically compressed, converting worst-case lookup spikes into predictable near-constant times and allowing table operation at up to 90% load factor without catastrophic degradation.

### Question 3: Given an array of integers `nums` and an integer `target`, explain how Hash Search achieves $O(N)$ time for the Two-Sum problem compared to $O(N^2)$ brute force or $O(N \log N)$ two-pointer search.
**Answer**:
For every element `x` at index `i`, we require its mathematical complement `complement = target - x`.
- Brute force checks all pairs via nested loops: $\frac{N(N-1)}{2} \implies O(N^2)$ comparisons.
- Sorting + Two-Pointer requires $O(N \log N)$ to sort, plus $O(N)$ pointer traversal.
- **Hash Search**: We maintain a hash table `seen: {value: index}`. In a single linear scan ($N$ iterations), we compute `complement = target - x` and perform an $O(1)$ hash search: `if complement in seen: return [seen[complement], i]`. If absent, we record `seen[x] = i`.
- Total time: $N \times O(1) = O(N)$. Space: $O(N)$ auxiliary hash table memory.

## R. Project Connections
- **CPython Core Engine**: Python's entire namespace system, global variables, local scopes, object attributes (`__dict__`), and module registries are built entirely on optimized C-level hash tables (`Objects/dictobject.c`).
- **Distributed In-Memory Stores (Redis / Memcached)**: Redis uses incremental rehashing (progressive background migration across two hash tables) to serve millions of $O(1)$ key-value operations per second without locking request threads.
- **Database Query Execution (Hash Join & Hash Index)**: Relational query planners (PostgreSQL, MySQL) execute inner joins by hashing the smaller table into memory (`HashJoin`) and scanning the larger table against it in $O(M + N)$ time instead of $O(M \times N)$ nested loops.
- **Git Version Control**: Git objects (commits, trees, blobs) are identified and searched via cryptographic SHA-1/SHA-256 hashes in a content-addressable hash database.

## S. Edge Cases & Boundary Conditions
1. **Empty Hash Table**: Searching any key returns `None` or raises `KeyError` gracefully without index crashes.
2. **Missing Key**: Search traces full probe sequence or list chain to termination and safely reports absence.
3. **Key Overwrite**: Inserting an existing key updates its value in-place without expanding size or creating duplicate entries.
4. **Collision Clumping**: Multiple keys mapping to the identical bucket index must all be retrievable and distinguishable via `key == target`.
5. **Tombstone Recycling**: In open addressing, inserting into a slot marked with a tombstone reuses the dead slot, conserving memory and halting probe expansion.
6. **Rehashing Boundary**: Crossing the load factor threshold triggers table doubling, re-evaluating all bucket positions under the new capacity.

## T. Algorithmic Variants & Paradigms
- **Separate Chaining with Trees (Java 8+ HashMap)**: When a linked list chain exceeds 8 nodes, it transforms into a Red-Black tree, ensuring $O(\log k)$ worst-case collision lookup instead of $O(k)$.
- **Cuckoo Hashing**: Uses two distinct hash functions $h_1$ and $h_2$ and two tables. A key always resides at either $T_1[h_1(k)]$ or $T_2[h_2(k)]$, guaranteeing strictly $O(1)$ worst-case search time.
- **Hopscotch Hashing**: Combines open addressing with neighborhood bounding, guaranteeing that each key is located within a bounded neighborhood of $H$ slots from its original hash bucket.
- **Consistent Hashing**: Used in distributed systems (Dynamo, Cassandra) where changing the number of servers $m$ only remaps $K/m$ keys on average rather than reshuffling all keys.

## U. Algorithmic Comparison Table
| Algorithm / Technique | Average Search | Worst-Case Search | Range Queries? | In-Place Memory? | Order Invariant? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | $O(N)$ | $O(N)$ | No | Yes ($O(1)$ space) | Unordered |
| **Binary Search** | $O(\log N)$ | $O(\log N)$ | Yes ($O(\log N)$) | Yes ($O(1)$ space) | Strictly Sorted |
| **Hash Search (Chaining)** | $O(1)$ | $O(N)$ | No | No ($O(N)$ nodes) | Unordered |
| **Hash Search (Linear Probe)**| $O(1)$ | $O(N)$ | No | Compact Array | Unordered |
| **B-Tree Search** | $O(\log N)$ | $O(\log N)$ | Yes ($O(\log N + K)$)| Node Pointers | Strictly Sorted |

## V. Practical Implementation Exercises
1. Implement a `CountingBloomFilter` that uses multiple hash functions to test set membership with zero false negatives.
2. Implement Robin Hood linear probing with backward-shift deletion to eliminate the need for tombstones entirely.
3. Benchmark separate chaining against open addressing under varying load factors from $\alpha = 0.1$ to $\alpha = 0.9$ and plot probe counts.

## W. Step-by-Step Execution Trace
Tracing a Hash Search for key `"cat"` in a table of capacity $m = 5$ using Linear Probing:
- Keys currently stored: `{"ant": 10, "bat": 20}`
- Hash calculations:
  - $h(\text{"ant"}) = 12 \implies 12 \pmod 5 = \text{Index } 2$
  - $h(\text{"bat"}) = 17 \implies 17 \pmod 5 = \text{Index } 2 \implies \text{Collision! Probe to Index } 3$
  - Target key: `"cat"`, where $h(\text{"cat"}) = 22 \implies 22 \pmod 5 = \text{Index } 2$

| Step | Probe $i$ | Examined Slot | Resident Entry | Comparison | Action |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | $(2 + 0) \pmod 5 = 2$ | `("ant", 10)` | `"ant" == "cat"` (False) | Collision! Continue probe sequence. |
| 2 | 1 | $(2 + 1) \pmod 5 = 3$ | `("bat", 20)` | `"bat" == "cat"` (False) | Collision! Continue probe sequence. |
| 3 | 2 | $(2 + 2) \pmod 5 = 4$ | `None` (Empty) | Cell is empty | Target absent! Terminate search, return `None`. |

## X. Key Takeaways & Summary Anchor
- Hash search trades bounded auxiliary memory for constant-time $O(1)$ expected search, insert, and delete performance.
- Collisions are an unavoidable mathematical certainty (Birthday Paradox); table correctness depends entirely on robust collision resolution.
- In Separate Chaining, deletions are trivial, but heap pointer chasing degrades CPU cache locality.
- In Open Addressing, linear probing maximizes cache locality, but requires Tombstones (`_DELETED`) to protect probe sequence integrity.
- Never mutate a key after inserting it into a hash table, and always preserve the invariant: $a == b \implies h(a) == h(b)$.
"""

from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar
import collections
import types

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION: SEPARATE CHAINING HASH TABLE
# ==============================================================================

class _ChainNode(Generic[K, V]):
    """Singly-linked list node for separate chaining collision resolution."""
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V, next_node: Optional["_ChainNode[K, V]"] = None) -> None:
        self.key: K = key
        self.value: V = value
        self.next: Optional["_ChainNode[K, V]"] = next_node


class SeparateChainingHashTable(Generic[K, V]):
    """
    Textbook implementation of a Hash Table using Separate Chaining.
    
    Features:
    - Modulo compression using prime table capacities.
    - Dynamic expansion when load factor alpha > 0.75.
    - Dynamic contraction when load factor alpha < 0.15.
    - Detailed statistics tracking for educational inspection.
    """
    _PRIMES: List[int] = [7, 17, 37, 79, 163, 331, 673, 1361, 2729, 5471, 10949]

    def __init__(self, initial_capacity_idx: int = 1) -> None:
        self._prime_idx: int = initial_capacity_idx
        self._capacity: int = self._PRIMES[self._prime_idx]
        self._buckets: List[Optional[_ChainNode[K, V]]] = [None] * self._capacity
        self._size: int = 0
        self._total_collisions: int = 0

    def _hash(self, key: K) -> int:
        """
        Computes the bucket index for a key using Python's hash() and prime modulo.
        Masking with 0x7FFFFFFF ensures positive values across architectures.
        """
        return (hash(key) & 0x7FFFFFFF) % self._capacity

    @property
    def load_factor(self) -> float:
        """Returns the current load factor alpha = n / m."""
        return self._size / self._capacity

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: K) -> bool:
        return self.search(key) is not None

    def search(self, key: K) -> Optional[V]:
        """
        Searches for a key in the hash table.
        
        Algorithm:
        1. Compute bucket index i = hash(key) % capacity.
        2. Walk the linked list at bucket i.
        3. Compare each node's key using equality ==.
        4. Return value if found, else None.
        
        Complexity:
            Time: O(1) Best, O(1 + alpha) Average, O(N) Worst.
            Space: O(1) Auxiliary.
        """
        index = self._hash(key)
        current = self._buckets[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def insert(self, key: K, value: V) -> None:
        """
        Inserts or updates a key-value pair.
        If key exists, updates value in-place.
        If load factor exceeds 0.75, automatically rehashes to next prime capacity.
        """
        index = self._hash(key)
        current = self._buckets[index]

        # 1. Search existing chain for key update
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # 2. Insert new node at head of chain (O(1))
        if self._buckets[index] is not None:
            self._total_collisions += 1
        new_node = _ChainNode(key, value, next_node=self._buckets[index])
        self._buckets[index] = new_node
        self._size += 1

        # 3. Dynamic resizing check
        if self.load_factor > 0.75 and self._prime_idx + 1 < len(self._PRIMES):
            self._rehash(self._prime_idx + 1)

    def delete(self, key: K) -> bool:
        """
        Deletes a key from the table.
        Returns True if key was deleted, False if key was not found.
        """
        index = self._hash(key)
        current = self._buckets[index]
        prev: Optional[_ChainNode[K, V]] = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    self._buckets[index] = current.next
                else:
                    prev.next = current.next
                self._size -= 1

                # Dynamic shrink check
                if self.load_factor < 0.15 and self._prime_idx > 0:
                    self._rehash(self._prime_idx - 1)
                return True
            prev = current
            current = current.next
        return False

    def _rehash(self, new_prime_idx: int) -> None:
        """Rehashes all existing entries into a newly sized bucket array."""
        old_buckets = self._buckets
        self._prime_idx = new_prime_idx
        self._capacity = self._PRIMES[self._prime_idx]
        self._buckets = [None] * self._capacity
        self._size = 0  # Re-incremented during re-insertion

        for head in old_buckets:
            curr = head
            while curr is not None:
                self.insert(curr.key, curr.value)
                curr = curr.next

    def bucket_distribution(self) -> List[int]:
        """Returns the length of the chain in each bucket (useful for histogram inspection)."""
        lengths = []
        for head in self._buckets:
            length = 0
            curr = head
            while curr is not None:
                length += 1
                curr = curr.next
            lengths.append(length)
        return lengths


# ==============================================================================
# 2. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION: OPEN ADDRESSING (LINEAR PROBING)
# ==============================================================================

class LinearProbingHashTable(Generic[K, V]):
    """
    Open Addressing Hash Table with Linear Probing and Tombstone Deletion.
    
    Invariants:
    - Empty slots are None.
    - Deleted slots hold the sentinel _TOMBSTONE.
    - Probing advances via (hash + i) % capacity.
    - Searches terminate only upon encountering genuine None, skipping tombstones.
    """
    _TOMBSTONE = object()  # Unique sentinel object

    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity: int = initial_capacity
        self._keys: List[Any] = [None] * self._capacity
        self._values: List[Any] = [None] * self._capacity
        self._size: int = 0
        self._tombstones: int = 0

    @property
    def load_factor(self) -> float:
        """Load factor including active elements and dead tombstones."""
        return (self._size + self._tombstones) / self._capacity

    def __len__(self) -> int:
        return self._size

    def _hash(self, key: K) -> int:
        return (hash(key) & 0x7FFFFFFF) % self._capacity

    def search(self, key: K) -> Optional[V]:
        """
        Searches for target key via linear probing.
        Continues past tombstones; terminates on genuine None or table cycle.
        """
        start_idx = self._hash(key)
        for i in range(self._capacity):
            idx = (start_idx + i) % self._capacity
            slot_key = self._keys[idx]

            if slot_key is None:
                # Key is guaranteed absent
                return None
            if slot_key is not self._TOMBSTONE and slot_key == key:
                return self._values[idx]
        return None

    def insert(self, key: K, value: V) -> None:
        """
        Inserts or updates key. Reuses tombstones if available.
        Triggers doubling rehash when load factor >= 0.66.
        """
        if self.load_factor >= 0.66:
            self._rehash(self._capacity * 2)

        start_idx = self._hash(key)
        first_tombstone_idx: Optional[int] = None

        for i in range(self._capacity):
            idx = (start_idx + i) % self._capacity
            slot_key = self._keys[idx]

            if slot_key is None:
                # Target slot found. Prefer first observed tombstone for slot reuse.
                target_idx = first_tombstone_idx if first_tombstone_idx is not None else idx
                if first_tombstone_idx is not None:
                    self._tombstones -= 1
                self._keys[target_idx] = key
                self._values[target_idx] = value
                self._size += 1
                return

            if slot_key is self._TOMBSTONE:
                if first_tombstone_idx is None:
                    first_tombstone_idx = idx
            elif slot_key == key:
                # Update existing key
                self._values[idx] = value
                return

        # If table was full of tombstones and loop finished
        if first_tombstone_idx is not None:
            self._keys[first_tombstone_idx] = key
            self._values[first_tombstone_idx] = value
            self._tombstones -= 1
            self._size += 1

    def delete(self, key: K) -> bool:
        """
        Deletes key by converting slot into a Tombstone sentinel.
        Returns True on success, False if key was not found.
        """
        start_idx = self._hash(key)
        for i in range(self._capacity):
            idx = (start_idx + i) % self._capacity
            slot_key = self._keys[idx]

            if slot_key is None:
                return False
            if slot_key is not self._TOMBSTONE and slot_key == key:
                self._keys[idx] = self._TOMBSTONE
                self._values[idx] = None
                self._size -= 1
                self._tombstones += 1
                return True
        return False

    def _rehash(self, new_capacity: int) -> None:
        """Allocates new table, drops all tombstones, and re-inserts active keys."""
        old_keys = self._keys
        old_values = self._values

        self._capacity = new_capacity
        self._keys = [None] * self._capacity
        self._values = [None] * self._capacity
        self._size = 0
        self._tombstones = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._TOMBSTONE:
                self.insert(k, v)


# ==============================================================================
# 3. CLASSIC HASH SEARCH ALGORITHMIC PATTERNS
# ==============================================================================

def two_sum_hash_search(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Finds indices of two numbers that add up to target using Hash Search in O(N) time.
    
    Args:
        nums: List of integers.
        target: Target sum.
        
    Returns:
        Tuple of (index1, index2) or None if no pair exists.
    """
    seen: Dict[int, int] = {}  # complement -> original index
    for current_idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], current_idx)
        seen[num] = current_idx
    return None


def hash_search_membership(collection: List[T], target: T) -> bool:
    """Demonstrates O(1) membership search by pre-hashing a list into a set."""
    hash_set = set(collection)
    return target in hash_set


# ==============================================================================
# 4. INDUSTRY-STANDARD LIBRARY IMPLEMENTATION
# ==============================================================================

def industry_standard_hash_search_demo():
    """
    Demonstration of production Python hashing capabilities:
    1. Built-in dict (compact ordered hash map written in C).
    2. collections.defaultdict (automatic missing key initialization).
    3. collections.Counter (high-performance multiset frequency table).
    4. types.MappingProxyType (read-only immutable hash map wrapper).
    """
    # 1. Standard Dictionary
    cache: Dict[str, int] = {"cpu_usage": 45, "mem_usage": 72, "disk_io": 120}
    # O(1) safe retrieval with default fallback
    val = cache.get("mem_usage", 0)

    # 2. Defaultdict for grouping/multi-maps
    grouped_by_len: collections.defaultdict = collections.defaultdict(list)
    words = ["apple", "bat", "cherry", "ant", "bear"]
    for word in words:
        grouped_by_len[len(word)].append(word)

    # 3. Frequency Counter
    counts = collections.Counter("abracadabra")
    most_common_char = counts.most_common(1)[0]

    # 4. Immutable Hash Map (Read-Only Defense)
    read_only_view = types.MappingProxyType(cache)

    return val, dict(grouped_by_len), most_common_char, read_only_view


# ==============================================================================
# 5. DELIBERATELY BUGGY IMPLEMENTATION WITH DEBUGGING COMMENTARY
# ==============================================================================

class BuggyOpenAddressingHashTable:
    """
    DELIBERATELY BUGGY HASH TABLE
    Contains two fatal architectural flaws commonly seen in faulty implementations.
    
    BUG 1: Deletion sets the slot to None instead of a Tombstone.
           This breaks probe sequences: any subsequent search for keys that
           were probed past this deleted slot will terminate prematurely on None!
           
    BUG 2: Insertion overwrites without checking key equality.
           If a collision occurs and we just probe to the next slot, an update
           operation on an existing key might duplicate it instead of updating.
    """
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.table: List[Optional[Tuple[Any, Any]]] = [None] * capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def insert(self, key: Any, value: Any) -> None:
        idx = self._hash(key)
        for i in range(self.capacity):
            curr_idx = (idx + i) % self.capacity
            # BUG: Overwrites any slot without properly distinguishing update vs insert!
            if self.table[curr_idx] is None:
                self.table[curr_idx] = (key, value)
                return
            elif self.table[curr_idx][0] == key:
                self.table[curr_idx] = (key, value)
                return
        raise RuntimeError("Table is full")

    def search(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        for i in range(self.capacity):
            curr_idx = (idx + i) % self.capacity
            # Because delete() writes None, this loop halts prematurely!
            if self.table[curr_idx] is None:
                return None
            if self.table[curr_idx][0] == key:
                return self.table[curr_idx][1]
        return None

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        for i in range(self.capacity):
            curr_idx = (idx + i) % self.capacity
            if self.table[curr_idx] is None:
                return False
            if self.table[curr_idx][0] == key:
                # FATAL BUG 1: Wiping to None breaks the linear probe chain for all downstream keys!
                self.table[curr_idx] = None
                return True
        return False


# ==============================================================================
# 6. COMPREHENSIVE TEST SUITE
# ==============================================================================

def run_tests():
    """Validates all implementations against standard invariants and edge cases."""
    print("--- Running Separate Chaining Tests ---")
    ht = SeparateChainingHashTable[str, int]()
    
    # Test Empty
    assert ht.search("missing") is None
    assert len(ht) == 0
    assert not ht.delete("nonexistent")

    # Test Insertion & Retrieval
    ht.insert("alpha", 10)
    ht.insert("beta", 20)
    ht.insert("gamma", 30)
    assert len(ht) == 3
    assert ht.search("alpha") == 10
    assert ht.search("beta") == 20
    assert ht.search("gamma") == 30
    assert "alpha" in ht
    assert "delta" not in ht

    # Test Update In-Place
    ht.insert("alpha", 999)
    assert ht.search("alpha") == 999
    assert len(ht) == 3  # Size must not increment on update

    # Test Deletion
    assert ht.delete("beta") is True
    assert ht.search("beta") is None
    assert len(ht) == 2
    assert ht.delete("beta") is False  # Second delete returns False

    # Test Collision & Dynamic Rehashing Stress
    for i in range(100):
        ht.insert(f"key_{i}", i * 10)
    assert len(ht) == 102
    for i in range(100):
        assert ht.search(f"key_{i}") == i * 10

    print("Separate Chaining: All assertions passed!")

    print("\n--- Running Linear Probing Tests ---")
    lp = LinearProbingHashTable[str, int](initial_capacity=8)
    
    # Test Basic CRUD
    lp.insert("k1", 100)
    lp.insert("k2", 200)
    assert lp.search("k1") == 100
    assert lp.search("k2") == 200
    assert lp.search("k3") is None
    assert len(lp) == 2

    # Test Tombstone Mechanism & Probe Continuity
    # Force collision by finding keys with matching hash % 8
    # Using integer keys makes collision testing deterministic
    lp_int = LinearProbingHashTable[int, str](initial_capacity=8)
    # 0, 8, 16 all hash to bucket 0 in capacity 8
    lp_int.insert(0, "val0")   # slot 0
    lp_int.insert(8, "val8")   # slot 1 (probed)
    lp_int.insert(16, "val16") # slot 2 (probed)

    assert lp_int.search(0) == "val0"
    assert lp_int.search(8) == "val8"
    assert lp_int.search(16) == "val16"

    # Delete the middle link in the probe sequence (8 at slot 1)
    assert lp_int.delete(8) is True
    assert lp_int.search(8) is None
    # CRUCIAL TEST: 16 must STILL be found even though slot 1 was deleted!
    assert lp_int.search(16) == "val16", "Linear Probing failed to search past tombstone!"

    # Reuse tombstone slot
    lp_int.insert(24, "val24") # Should reuse slot 1
    assert lp_int.search(24) == "val24"
    assert lp_int.search(16) == "val16"
    print("Linear Probing: All assertions passed!")

    print("\n--- Demonstrating Buggy Implementation Flaw ---")
    buggy = BuggyOpenAddressingHashTable(capacity=8)
    # Deterministic keys that collide on modulo 8:
    # 0 % 8 = 0 -> placed in slot 0
    # 8 % 8 = 0 -> placed in slot 1 (probed)
    # 16 % 8 = 0 -> placed in slot 2 (probed)
    buggy.insert(0, "A")
    buggy.insert(8, "B")
    buggy.insert(16, "C")

    # Verify all 3 can initially be found
    assert buggy.search(0) == "A"
    assert buggy.search(8) == "B"
    assert buggy.search(16) == "C"

    # Delete middle key (8)
    buggy.delete(8)

    # Key 16 is STILL in the table, but searching for it will FAIL because slot 1 was wiped to None!
    missing_result = buggy.search(16)
    print(f"Buggy Table Result for key 16 after deleting key 8: {missing_result}")
    assert missing_result is None, "Expected bug to manifest: search prematurely halted on None!"
    print("Bug confirmed: Deleting without tombstones broke the probe sequence chain as predicted.")

    print("\n--- Running Two-Sum Hash Search Tests ---")
    nums = [2, 7, 11, 15]
    result = two_sum_hash_search(nums, 9)
    assert result == (0, 1), f"Expected (0, 1), got {result}"

    result_none = two_sum_hash_search(nums, 100)
    assert result_none is None

    print("\n--- Running Library Capabilities Demo ---")
    val, grouped, common, ro_view = industry_standard_hash_search_demo()
    assert val == 72
    assert grouped[3] == ["bat", "ant"]
    assert common == ("a", 5)
    assert ro_view["cpu_usage"] == 45
    print("Library Features: All assertions passed!")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")


# ==============================================================================
# 7. MAIN EXECUTION BLOCK WITH EDUCATIONAL TRACES
# ==============================================================================

def main():
    print("=" * 70)
    print("   HASH SEARCH: DEEP DIVE, MECHANICS & TRACES")
    print("=" * 70)

    # 1. Execute full test suite
    run_tests()

    # 2. Educational Step-by-Step Trace of Hash Collision & Probing
    print("\n" + "=" * 70)
    print("   STEP-BY-STEP VISUAL TRACE: SEPARATE CHAINING vs PROBING")
    print("=" * 70)

    sample_keys = ["apple", "orange", "banana", "pear", "peach"]
    print(f"\nSample Keys: {sample_keys}")
    print("\nComputing Hashes and Bucket Indices (Table Size = 5):")
    for key in sample_keys:
        h = hash(key) & 0x7FFFFFFF
        idx = h % 5
        print(f"  Key: {key:<8} -> Hash: 0x{h:08x} -> Index (Hash % 5): {idx}")

    print("\nPopulating SeparateChainingHashTable with fruits...")
    fruit_table = SeparateChainingHashTable[str, str](initial_capacity_idx=0) # Cap = 7
    for fruit in sample_keys:
        fruit_table.insert(fruit, f"{fruit.upper()}_JUICE")

    print(f"Current Size: {len(fruit_table)}, Capacity: {fruit_table._capacity}")
    print(f"Current Load Factor: {fruit_table.load_factor:.2f}")
    print(f"Bucket Chain Lengths: {fruit_table.bucket_distribution()}")

    print("\nExecuting Searches:")
    for query in ["apple", "grape"]:
        res = fruit_table.search(query)
        status = f"FOUND -> {res}" if res else "NOT FOUND"
        print(f"  Search('{query}'): {status}")


if __name__ == "__main__":
    main()
