r"""
# Van Emde Boas Trees: Theory, Recursive Mechanics, and Bit-Parallel Priority Search

## A. Concept Name
Van Emde Boas Tree (vEB Tree), also historically known as a Stratified Tree.

## B. One-Sentence Definition
A Van Emde Boas Tree is an advanced recursive integer priority queue and search data structure that executes search, insert, delete, minimum, maximum, successor, and predecessor operations in $O(\log \log U)$ worst-case time over a bounded integer universe $U = \{0, 1, \dots, u-1\}$.

## C. Why Does This Exist? (What problem does it solve?)
In classical computer science, comparison-based dictionary structures face well-established theoretical limits:
- **Comparison Lower Bound**: Any comparison-based priority queue or search tree (such as AVL Trees, Red-Black Trees, B-Trees, or Skip Lists) requires $\Omega(\log N)$ time per operation in the worst case, where $N$ is the number of stored items.
- **The Scalability Bottleneck**: When $N$ or the integer domain is large (e.g., 64-bit integer routing tables, memory allocation bitmaps, discrete event schedulers), $\log_2(2^{64}) = 64$ sequential comparisons and pointer dereferences are required per query.
- **Direct Bitmaps**: A naive flat bit array gives $O(1)$ membership search and insertion, but finding the successor or predecessor of an integer requires an $O(U)$ linear scan through the bits.

**The Van Emde Boas Breakthrough (1975)**:
Peter van Emde Boas asked: *Can we search faster than $\log N$ if keys are integers from a bounded universe $[0, u-1]$?*
By exploiting the binary structure of integers and dividing the key bits in half at each recursive level (taking the square root of the universe $\sqrt{u}$ rather than halving the elements $N/2$), the vEB tree achieves an astonishing operational time complexity of:
$$T(u) = O(\log \log u)$$

**Why this is mind-boggling:**
- If universe $u = 2^{64} \approx 1.84 \times 10^{19}$:
  - Balanced BST: $\log_2(2^{64}) = 64$ operations.
  - vEB Tree: $\log_2(\log_2(2^{64})) = \log_2(64) = 6$ operations!
Every single operation—including finding the immediate successor or predecessor among billions of scattered integers—completes in at most **6 recursive steps**!

## D. Intuition & Real-Life Analogy
- **The Telephone Area Code System**:
  Imagine looking up a phone number in a country of 100 million people ($u = 10^8$). You do not search all numbers linearly. A phone number is split into an area code (high digits) and a local number (low digits):
  `[Area Code: 3 digits] - [Local Number: 5 digits]`
  To find the next active phone number in the country, you first check if there is an active number in your current area code. If not, you check a top-level **Summary Registry** of active area codes to instantly skip to the next populated city, and then immediately inspect the lowest assigned number in that city.
- **The Two-Tier Calendar / Clock**:
  To find the next scheduled meeting, you don't scan all 1,440 minutes of the day. You inspect the current hour. If no meetings remain in this hour, you consult your high-level "hours summary" to find the next active hour, and then jump straight to the earliest minute in that hour.

## E. Mental Model
A vEB tree of universe size $u$ decomposes each integer $x$ into two halves:
- `high(x)`: The most significant bits (which cluster/sub-tree $x$ belongs to).
- `low(x)`: The least significant bits (the offset within that cluster).
$$\text{Given } u = 2^b, \quad \sqrt[\uparrow]{u} = 2^{\lceil b/2 \rceil}, \quad \sqrt[\downarrow]{u} = 2^{\lfloor b/2 \rfloor}$$
$$x = \text{high}(x) \times \sqrt[\downarrow]{u} + \text{low}(x)$$

```text
Universe u = 16 (4 bits: b3 b2 b1 b0)
Upper Sqrt = 4 (clusters 0..3), Lower Sqrt = 4 (offsets 0..3)

                         +-----------------------------------+
                         |         vEB Tree (u = 16)         |
                         |  min: 2            max: 14        |
                         +-----------------+-----------------+
                                           |
                  +------------------------+------------------------+
                  |                                                 |
                  v                                                 v
        +-------------------+                             +-------------------+
        | Summary (u = 4)   |                             | Clusters (4 of 4) |
        | Tracks non-empty  |                             | [0]: offset 0..3  |
        | clusters: {1, 3}  |                             | [1]: offset 0..3  |
        +-------------------+                             | [2]: empty (None) |
                                                          | [3]: offset 0..3  |
                                                          +-------------------+
```

### The Invariant of Pure Genius: Why `min` is NOT stored in clusters
The secret to achieving $O(\log \log u)$ rather than $O(\log u)$ is that **the minimum element (`min`) is stored ONLY at the root and is NEVER inserted into any sub-cluster**.
1. Because `min` is cached at the root, finding the minimum takes $O(1)$ time.
2. When inserting into an empty cluster, we simply set `min = max = x` in $O(1)$ without recursing into deeper clusters!
3. Therefore, inserting an element requires either:
   - Updating `summary` (if the cluster was empty, which takes $O(1)$ inside the cluster), OR
   - Recursing into the cluster (if the cluster was already registered in `summary`).
   In both cases, **at most ONE recursive call** is made.
   $$T(u) \le T(\sqrt{u}) + O(1) \implies O(\log \log u)$$

## F. Formal Technical Explanation

### 1. Structural Components of a vEB Node
A `VanEmdeBoasTree` for universe size $u = 2^b$ consists of:
- `u`: Universe size ($u \ge 2$).
- `min`: The smallest integer currently stored in this tree, or `None` if empty.
- `max`: The largest integer currently stored in this tree, or `None` if empty.
- `summary`: A pointer to a child `vEBTree` of universe size $\sqrt[\uparrow]{u}$. It stores an integer $h$ if and only if `cluster[h]` is non-empty.
- `cluster`: An array of $\sqrt[\uparrow]{u}$ pointers to child `vEBTrees`, each of universe size $\sqrt[\downarrow]{u}$.

### 2. Coordinate Functions
Let $u_{\downarrow} = \sqrt[\downarrow]{u} = 2^{\lfloor b/2 \rfloor}$.
- `high(x)` $= \lfloor x / u_{\downarrow} \rfloor = x \gg \lfloor b/2 \rfloor$
- `low(x)` $= x \pmod{u_{\downarrow}} = x \ \& \ (u_{\downarrow} - 1)$
- `index(h, l)` $= h \times u_{\downarrow} + l = (h \ll \lfloor b/2 \rfloor) \mid l$

### 3. Core Algorithms

#### Successor Search (`successor(x)`):
1. **Base Case ($u = 2$)**: If $x == 0$ and $max == 1$, return $1$; else return `None`.
2. **Lower Bound Check**: If $min \ne \text{None}$ and $x < min$, return $min$.
3. **Internal Cluster Check**: Let $h = high(x)$ and $l = low(x)$.
   If `cluster[h]` exists and $l < \text{cluster}[h].max$:
   The successor lies strictly within the same cluster!
   $\implies \text{offset} = \text{cluster}[h].\text{successor}(l)$
   $\implies \text{return } index(h, \text{offset})$.
4. **Cross-Cluster Jump (Summary Lookup)**:
   Otherwise, the successor must be in the next non-empty cluster!
   $\implies succ\_cluster = summary.\text{successor}(h)$
   If $succ\_cluster == \text{None}$, return `None`.
   Because `cluster[succ_cluster].min` is stored in $O(1)$, we do not need to search inside that cluster:
   $\implies \text{offset} = cluster[succ\_cluster].min$
   $\implies \text{return } index(succ\_cluster, \text{offset})$.

#### Insertion (`insert(x)`):
1. If tree is empty ($min == \text{None}$): set $min = max = x$, return.
2. If $x < min$: swap $x$ and $min$ (the old minimum must now be pushed into the clusters).
3. If $u > 2$:
   Let $h = high(x)$ and $l = low(x)$.
   If `cluster[h]` is empty:
   - Insert $h$ into `summary`.
   - Set `cluster[h].min = cluster[h].max = l` in $O(1)$!
   Else:
   - Recursively insert $l$ into `cluster[h]`.
4. If $x > max$: set $max = x$.

#### Deletion (`delete(x)`):
1. If $min == max$: only 1 element was stored. Set $min = max = \text{None}$, return.
2. If $u == 2$: if $x == 0$, $min = max = 1$; else $min = max = 0$. Return.
3. If $x == min$:
   The new minimum is the minimum of the first non-empty cluster:
   $first\_cluster = summary.min$
   $new\_min = index(first\_cluster, cluster[first\_cluster].min)$
   $min = new\_min$
   $x = new\_min$ (proceed to delete this element from the sub-cluster).
4. Delete $low(x)$ from `cluster[high(x)]`.
5. If `cluster[high(x)]` became empty:
   - Delete $high(x)$ from `summary`.
   - Update $max$ if necessary by consulting `summary.max`.
6. Else if $x == max$:
   - Update $max = index(high(x), cluster[high(x)].max)$.

## G. Mathematical Foundation
The runtime analysis of vEB operations rests on the master theorem applied to square-root recurrences.

### 1. The Recurrence Relation
Let $T(u)$ be the time complexity for universe size $u$. At each step, an operation executes $O(1)$ coordinate arithmetic and makes at most **one** recursive call on a universe of size $\sqrt{u}$:
$$T(u) = T(\sqrt{u}) + O(1)$$

Let $u = 2^b$, where $b$ is the number of bits in the integer representation:
$$T(2^b) = T(2^{b/2}) + O(1)$$

Let $S(b) = T(2^b)$. The recurrence becomes:
$$S(b) = S(b/2) + O(1)$$
By the Master Theorem (Case 2 with $a=1, b=2, c=0$), or simply recognizing this as the binary search recurrence on $b$:
$$S(b) = \Theta(\log b)$$

Substituting $b = \log_2 u$ back into the result:
$$T(u) = \Theta(\log b) = \Theta(\log \log u)$$

### 2. What happens if an operation makes TWO recursive calls?
Suppose an implementation accidentally calls recursion on both `summary` and `cluster`:
$$T(u) = 2 T(\sqrt{u}) + O(1) \implies S(b) = 2 S(b/2) + O(1)$$
By the Master Theorem ($a = 2, b = 2, c = 0 \implies \log_b a = 1 > c$):
$$S(b) = \Theta(b) = \Theta(\log u)$$
The time complexity degrades to $O(\log u)$, completely eliminating the vEB advantage over standard binary trees! This proves why the `min` caching optimization is mandatory.

## H. Complexity Analysis (Time, Space, Memory)
| Operation | Time Complexity | Notes |
| :--- | :--- | :--- |
| **Minimum / Maximum** | $O(1)$ | Directly stored in root variables `min` and `max`. |
| **Member / Search** | $O(\log \log u)$ | Recurses at most once down $\sqrt{u}$ clusters. |
| **Successor / Predecessor**| $O(\log \log u)$ | At most one recursive call (either cluster or summary). |
| **Insert** | $O(\log \log u)$ | Either cluster is empty ($O(1)$) or summary is untouched. |
| **Delete** | $O(\log \log u)$ | At most one recursive call down the active subtree. |

### Space Complexity & Memory Layout:
- **Naive Array-Backed Allocation**:
  A naive vEB tree eagerly allocates array pointers for all $\sqrt{u}$ clusters:
  $$S(u) = (\sqrt{u} + 1) S(\sqrt{u}) + O(\sqrt{u}) = O(u)$$
  Storing an integer set from a 64-bit universe ($u = 2^{64}$) would require $2^{64}$ pointer nodes—an impossible memory requirement ($\sim 1.84 \times 10^{19}$ bytes).
- **Space-Optimized Hash-Backed vEB (Stratified Hash Tree)**:
  By allocating clusters **lazily** using dynamic hash maps or hash tables (allocating `cluster[h]` only when key $h$ is inserted), empty subtrees consume zero memory.
  The total space drops to:
  $$S(N) = O(N \log \log u)$$
  where $N$ is the number of elements actually present in the tree.

## I. Common Mistakes & Pitfalls
1. **Storing `min` Inside Clusters**:
   Inserting `min` into the sub-clusters causes `insert` to make two recursive calls, degrading time complexity from $O(\log \log u)$ to $O(\log u)$.
2. **Missing the Value Swap on Insert**:
   When inserting $x < min$, one must swap $x$ and $min$ so that the new smaller value becomes the cached root $min$, and the old $min$ is passed downward into the cluster hierarchy. Forgetting this swap corrupts the tree's ordering invariant.
3. **Off-By-One & Non-Power-of-Two Universes**:
   vEB trees rely on clean bitwise splitting: $b = \lceil \log_2 u \rceil$. Failing to round universe size $u$ up to a clean power of 2 ($u = 2^b$) causes integer division truncation errors in `high()` and `low()` calculations.
4. **Summary Deletion Neglect**:
   When the last element of a cluster is deleted, that cluster's index $h$ MUST be removed from `summary`. Forgetting to delete $h$ leaves a ghost pointer in `summary`, causing subsequent `successor` calls to jump into an empty cluster and crash or return invalid results.

## J. Common Confusions
- **vEB Tree vs. Binary Search Tree (BST)**: BST complexity depends on the number of elements $N$ ($O(\log N)$). vEB complexity depends strictly on the **universe size** $u$ ($O(\log \log u)$), completely independent of how many elements $N$ are stored!
- **vEB Tree vs. Hash Table**: A hash table achieves $O(1)$ expected search, but CANNOT perform predecessor, successor, range queries, or minimum/maximum searches. A vEB tree performs all of these ordered queries in $O(\log \log u)$ worst-case time.
- **vEB Tree vs. Trie / Radix Tree**: A bitwise trie takes $O(b) = O(\log u)$ time to traverse bits sequentially. A vEB tree takes $O(\log b) = O(\log \log u)$ by using summary structures to binary search over the bit representation.
- **vEB Tree vs. X-Fast / Y-Fast Trie**: Y-fast tries combine a balanced BST with an X-fast trie to achieve $O(\log \log u)$ time while strictly guaranteeing $O(N)$ space. A standard vEB tree is simpler and faster in practice when universe sizes fit in RAM.

## K. When To Use It
- You have a bounded universe of integers (e.g., router port numbers $0..65535$, process IDs, memory frame addresses, discrete timestamps).
- You require blindingly fast predecessor and successor queries (e.g., "find the next active packet queue with traffic").
- $N$ is extremely large ($N > 10^6$) and balanced trees ($O(\log N)$) create CPU latency bottlenecks.
- Integer priority queue operations where keys are dynamically inserted, deleted, and extracted.

## L. When NOT To Use It
- **Unbounded or Non-Integer Keys**: Floating-point numbers, arbitrary strings, or general comparable objects cannot be decomposed into bitwise `high` and `low` coordinates without serialization.
- **Enormous Sparse Universes Without Lazy Allocation**: Eagerly allocating a 64-bit vEB tree exhausts all system memory instantly.
- **Tiny Datasets ($N \le 32$)**: The pointer overhead and multi-tier recursion are slower than a simple sorted flat array or bitmask on modern hardware with SIMD instructions (`_mm_popcnt_u64`, `_tzcnt_u64`).

## M. Trade-offs
| Attribute | Van Emde Boas Tree | Red-Black Tree / AVL | Hash Map (dict) | Flat Bitset |
| :--- | :--- | :--- | :--- | :--- |
| **Search Time** | $O(\log \log u)$ | $O(\log N)$ | $O(1)$ average | $O(1)$ |
| **Successor Time** | $O(\log \log u)$ | $O(\log N)$ | Impossible / $O(N)$ | $O(u / 64)$ |
| **Insert / Delete** | $O(\log \log u)$ | $O(\log N)$ | $O(1)$ average | $O(1)$ |
| **Min / Max** | $O(1)$ | $O(\log N)$ or $O(1)$ | $O(N)$ | $O(u / 64)$ |
| **Space Complexity**| $O(u)$ or $O(N \log \log u)$| $O(N)$ | $O(N)$ | $O(u)$ bits |
| **Key Type** | Bounded Integers | Any Comparable | Any Hashable | Integers |

## N. Debugging Tips
- **Print Subtree States Recursively**: Include an indented `dump()` method displaying `[u={self.u}, min={self.min}, max={self.max}, active_clusters={summary.members()}]`.
- **Audit Base Case Transitions**: Trace operations on $u = 2$ and $u = 4$ manually on paper before scaling to $u = 64$ or $1024$.
- **Compare Against Python's `bisect`**: Write automated property-based fuzz tests inserting thousands of random numbers into both a vEB tree and a Python `sorted` list, asserting identical results for `successor()`, `predecessor()`, `min`, and `max`.

## O. Memory Hook
**"Take the square root of the universe: Check the cluster; if not there, jump the summary stair."**
Think of an elevator in a skyscraper: rather than stopping on every single floor, you check the express summary panel to jump directly to the target tower section.

## P. Active Recall Questions
1. Why must the minimum element `min` NOT be stored in any sub-cluster?
2. What is the difference between $u_{\uparrow}$ and $u_{\downarrow}$ when universe bit length $b$ is odd?
3. How does `successor(x)` find the next element when $x$ is greater than or equal to the maximum element of its own cluster?
4. What is the recurrence relation of a vEB tree, and why does it solve to $O(\log \log u)$?
5. Why does eager allocation of a vEB tree over a 64-bit universe fail, and how does lazy hashing fix it?

## Q. Interview Questions & Answers

### Question 1: How does a Van Emde Boas tree achieve $O(1)$ time for `minimum()` and `maximum()`?
**Answer**:
Every vEB node maintains two dedicated attributes, `self.min` and `self.max`.
- When an element is inserted into an empty tree, `self.min` and `self.max` are both set to that value in $O(1)$.
- When elements are inserted into a non-empty tree, `self.min` is updated via a simple comparison, and `self.max` is updated if the new element exceeds the current maximum.
- Because `self.min` and `self.max` are maintained as cached fields at the root of the tree, querying `tree.minimum()` or `tree.maximum()` simply returns the cached values directly in $O(1)$ time without traversing any subtrees.

### Question 2: Walk through what happens during `successor(x)` when $low(x) \ge cluster[high(x)].max$.
**Answer**:
1. If $low(x) \ge cluster[high(x)].max$, the target integer's offset is already greater than or equal to every element present in its current cluster $high(x)$.
2. Therefore, no successor can possibly exist within cluster $high(x)$.
3. The algorithm immediately turns to the **Summary Tree**:
   $$succ\_cluster = summary.successor(high(x))$$
   This single recursive call finds the index of the next non-empty cluster in $O(\log \log u)$ time.
4. If $succ\_cluster$ is `None`, no larger element exists in the entire universe, so it returns `None`.
5. If a cluster index is found, the successor is simply the minimum element of that cluster! Because each cluster caches its minimum in $O(1)$ time (`cluster[succ_cluster].min`), no further search is required:
   $$\text{return } index(succ\_cluster, cluster[succ\_cluster].min)$$
   Total recursive calls: exactly one.

### Question 3: Why does standard binary search take $O(\log N)$ while Van Emde Boas takes $O(\log \log u)$? Could vEB ever be slower than binary search?
**Answer**:
- Binary search halves the **number of elements** $N$ at each step ($N \to N/2 \to N/4 \dots$), yielding $\log_2 N$ steps.
- vEB trees halve the **number of bits** in the universe at each step ($b \to b/2 \to b/4 \dots$), taking $\log_2(\log_2 u)$ steps.
- **When is vEB faster?** When universe size $u$ is fixed (e.g., 32-bit integers) and $N$ is large. For $u = 2^{32}$, $\log \log u = 5$, whereas $\log_2(10^6) \approx 20$.
- **When is vEB slower?** When $N$ is very small (e.g., $N = 4$), binary search takes $\approx 2$ steps, while vEB pointer overhead and recursive function calls will be slower in wall-clock time. Furthermore, if $u \gg 2^N$ (extremely sparse universe), $O(\log N)$ is smaller than $O(\log \log u)$.

## R. Project Connections
- **Linux Kernel Process Scheduler (O(1) Scheduler / CFS Bitmaps)**: The Linux kernel historically used multi-level bit arrays and priority bitmaps (analogous to 2-level vEB structures) to locate the highest-priority runnable process in $O(1)$ time using CPU bit-scan instructions.
- **Network Packet Scheduling & IP Route Lookups**: High-speed internet backbone routers use vEB and stratified trees to perform Longest Prefix Matching (LPM) and Quality of Service (QoS) fair queuing at 100 Gbps line rates.
- **Hardware Memory Allocators (Buddy Allocator / TLSF)**: Two-Level Segregated Fit (TLSF) memory allocators use hardware-accelerated vEB bitmap hierarchies to find the smallest available free memory block with bounded worst-case response time.

## S. Edge Cases & Boundary Conditions
1. **Empty Tree**: Calling `member`, `successor`, `predecessor`, `delete` on an empty tree returns `None` or `False` safely.
2. **Single Element ($min == max$)**: Correctly transitions to empty ($min = max = \text{None}$) upon deletion without corrupting subtrees.
3. **Base Case $u = 2$**: Directly handles binary values $\{0, 1\}$ without allocating clusters or summaries.
4. **Duplicate Insertions**: Inserting an element already present leaves the tree unchanged without creating duplicate entries.
5. **Successor of Maximum**: Querying `successor(x)` when $x \ge max$ immediately returns `None`.
6. **Predecessor of Minimum**: Querying `predecessor(x)` when $x \le min$ immediately returns `None`.

## T. Algorithmic Variants & Paradigms
- **Array-Backed vEB Tree**: Standard textbook structure with static cluster arrays; fastest access, but $O(u)$ space.
- **Hash-Backed (Sparse) vEB Tree**: Replaces cluster pointer arrays with hash tables, dynamically allocating clusters on-demand to achieve $O(N \log \log u)$ space.
- **X-Fast Trie**: Uses a bitwise trie where nodes at each level are indexed in a hash table; allows successor queries via binary search over levels in $O(\log \log u)$ time and $O(N \log u)$ space.
- **Y-Fast Trie**: Combines an X-fast trie with balanced BSTs (Red-Black trees) of size $O(\log u)$ to achieve $O(\log \log u)$ time and strictly linear $O(N)$ space.

## U. Algorithmic Comparison Table
| Algorithm | Insert | Delete | Search | Successor | Space |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Van Emde Boas (Array)** | $O(\log \log u)$ | $O(\log \log u)$ | $O(\log \log u)$ | $O(\log \log u)$ | $O(u)$ |
| **Van Emde Boas (Hash)**  | $O(\log \log u)^*$ | $O(\log \log u)^*$ | $O(\log \log u)^*$ | $O(\log \log u)^*$ | $O(N \log \log u)$ |
| **Red-Black Tree (BST)**  | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **Skip List**             | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **B-Tree**                | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **Binary Search on Array**| $O(N)$ | $O(N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
*\*Amortized / expected time due to hash table lookups.*

## V. Practical Implementation Exercises
1. Implement bitwise CPU acceleration using Python's `int.bit_length()` to compute $\sqrt{u}$ dynamically.
2. Implement a `y_fast_trie` hybrid and benchmark memory consumption against `VanEmdeBoasTree` for $u = 2^{20}$.
3. Create a discrete-event network traffic simulator that uses a vEB tree as the event scheduling queue.

## W. Step-by-Step Execution Trace
Tracing `insert(5)` into an empty vEB tree of universe size $u = 16$:
- $u = 16 = 2^4 \implies b = 4$.
- Upper square root $\sqrt[\uparrow]{16} = 4$; Lower square root $\sqrt[\downarrow]{16} = 4$.
1. Tree is empty: $min = None$.
2. Sets $min = 5, max = 5$. Done in $O(1)$! Notice: 5 is NOT inserted into any cluster!

Tracing `insert(14)` into the same tree:
1. $min = 5, max = 5$. Is $14 < min$? No ($14 > 5$).
2. Compute coordinates for $14$:
   - $high(14) = 14 \gg 2 = 3$ (Cluster 3).
   - $low(14) = 14 \ \& \ 3 = 2$ (Offset 2).
3. Inspect `cluster[3]`: Currently empty!
4. Since `cluster[3]` was empty:
   - Insert cluster index $3$ into `summary` (which inserts $3$ into a vEB of size 4).
   - Insert offset $2$ into `cluster[3]`: since `cluster[3]` is empty, it sets its own $min = 2, max = 2$ in $O(1)$!
5. Update root $max = 14$.
6. Final State: Root $min = 5, max = 14$; `summary` has $\{3\}$; `cluster[3]` has $min = 2, max = 2$.

Tracing `successor(5)`:
1. Is $5 < min$? No ($5 == min$).
2. $high(5) = 1, low(5) = 1$.
3. Cluster 1 is empty!
4. Search `summary.successor(1)`: Next non-empty cluster is cluster $3$!
5. Retrieve minimum of cluster $3$ in $O(1)$: `cluster[3].min == 2`.
6. Compute result: $index(3, 2) = 3 \times 4 + 2 = 14$.
7. Returns $14$! Total recursive steps: 1.

## X. Key Takeaways & Summary Anchor
- Van Emde Boas trees shatter the comparison-based $\Omega(\log N)$ barrier by recursing on the bits of the integer universe ($\sqrt{u}$ decomposition).
- Caching the minimum element at the root and omitting it from cluster subtrees guarantees that every recursive operation branches at most ONCE, ensuring strictly $O(\log \log u)$ runtime.
- For dense integer universes, vEB trees provide the fastest possible dynamic predecessor and priority queue queries in computer science.
"""

from typing import Any, Dict, List, Optional, Tuple
import bisect
import math


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION: VAN EMDE BOAS TREE
# ==============================================================================

class VanEmdeBoasTree:
    """
    Textbook implementation of a Van Emde Boas Tree.
    
    Supports:
    - insert(x): O(log log u)
    - delete(x): O(log log u)
    - member(x): O(log log u)
    - successor(x): O(log log u)
    - predecessor(x): O(log log u)
    - minimum(): O(1)
    - maximum(): O(1)
    
    Universe size u is rounded up to the nearest power of 2 for clean bitwise decomposition.
    """
    def __init__(self, universe_size: int) -> None:
        if universe_size < 2:
            raise ValueError("Universe size must be at least 2")

        # Compute number of bits b such that 2^b >= universe_size
        b = (universe_size - 1).bit_length()
        b = max(b, 1)
        self.u: int = 1 << b  # Normalized power-of-two universe
        self.b: int = b
        
        self.min: Optional[int] = None
        self.max: Optional[int] = None

        if self.u > 2:
            half_b = b // 2
            self.lower_bits: int = half_b
            self.lower_sqrt: int = 1 << half_b       # 2^(floor(b/2))
            self.upper_sqrt: int = 1 << (b - half_b) # 2^(ceil(b/2))

            # Lazy sub-structures
            self.summary: Optional["VanEmdeBoasTree"] = None
            self.cluster: List[Optional["VanEmdeBoasTree"]] = [None] * self.upper_sqrt
        else:
            self.lower_bits = 0
            self.lower_sqrt = 1
            self.upper_sqrt = 2
            self.summary = None
            self.cluster = []

    # --------------------------------------------------------------------------
    # Coordinate Arithmetic Functions (Bitwise Optimized)
    # --------------------------------------------------------------------------
    def high(self, x: int) -> int:
        """Returns the cluster index containing x."""
        return x >> self.lower_bits

    def low(self, x: int) -> int:
        """Returns the offset of x within its cluster."""
        return x & (self.lower_sqrt - 1)

    def index(self, h: int, l: int) -> int:
        """Reconstructs the original integer from cluster index and offset."""
        return (h << self.lower_bits) | l

    # --------------------------------------------------------------------------
    # Queries: Member, Min, Max, Successor, Predecessor
    # --------------------------------------------------------------------------
    def minimum(self) -> Optional[int]:
        """Returns the minimum element in O(1) time."""
        return self.min

    def maximum(self) -> Optional[int]:
        """Returns the maximum element in O(1) time."""
        return self.max

    def member(self, x: int) -> bool:
        """
        Tests if integer x is present in the tree.
        Time Complexity: O(log log u).
        """
        if x < 0 or x >= self.u:
            return False
        if x == self.min or x == self.max:
            return True
        if self.u == 2:
            return False
        
        h = self.high(x)
        if self.cluster[h] is None:
            return False
        return self.cluster[h].member(self.low(x))

    def successor(self, x: int) -> Optional[int]:
        """
        Finds the smallest integer in the tree strictly greater than x.
        Time Complexity: O(log log u).
        """
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            return None

        # If x is strictly smaller than tree's minimum, successor is min
        if self.min is not None and x < self.min:
            return self.min

        h = self.high(x)
        l = self.low(x)

        # 1. Check if successor lies within the same cluster
        target_cluster = self.cluster[h]
        if target_cluster is not None and target_cluster.max is not None and l < target_cluster.max:
            offset = target_cluster.successor(l)
            if offset is not None:
                return self.index(h, offset)
            return None

        # 2. Check summary to jump to next non-empty cluster
        if self.summary is None:
            return None
        succ_cluster = self.summary.successor(h)
        if succ_cluster is None:
            return None

        # The successor is the minimum of that next cluster (O(1) lookup!)
        offset = self.cluster[succ_cluster].min  # type: ignore
        return self.index(succ_cluster, offset)  # type: ignore

    def predecessor(self, x: int) -> Optional[int]:
        """
        Finds the largest integer in the tree strictly less than x.
        Time Complexity: O(log log u).
        """
        if self.u == 2:
            if x == 1 and self.min == 0:
                return 0
            return None

        # If x is strictly greater than tree's maximum, predecessor is max
        if self.max is not None and x > self.max:
            return self.max

        h = self.high(x)
        l = self.low(x)

        # 1. Check if predecessor lies within the same cluster
        target_cluster = self.cluster[h]
        if target_cluster is not None and target_cluster.min is not None and l > target_cluster.min:
            offset = target_cluster.predecessor(l)
            if offset is not None:
                return self.index(h, offset)
            return None

        # 2. Check summary to find preceding non-empty cluster
        pred_cluster: Optional[int] = None
        if self.summary is not None:
            pred_cluster = self.summary.predecessor(h)

        if pred_cluster is None:
            # Fallback to the root minimum if x is greater than it
            if self.min is not None and x > self.min:
                return self.min
            return None

        # The predecessor is the maximum of that preceding cluster (O(1) lookup!)
        offset = self.cluster[pred_cluster].max  # type: ignore
        return self.index(pred_cluster, offset)  # type: ignore

    # --------------------------------------------------------------------------
    # Mutations: Insert and Delete
    # --------------------------------------------------------------------------
    def insert(self, x: int) -> None:
        """
        Inserts integer x into the tree.
        Time Complexity: O(log log u).
        """
        if x < 0 or x >= self.u:
            raise ValueError(f"Value {x} out of universe bounds [0, {self.u - 1}]")

        # Base case 1: Tree is empty
        if self.min is None:
            self.min = self.max = x
            return

        # Avoid duplicate insertion
        if x == self.min or x == self.max:
            return

        # Invariant: x must be pushed into cluster if smaller than min
        if x < self.min:
            x, self.min = self.min, x

        if self.u > 2:
            h = self.high(x)
            l = self.low(x)

            # Lazy cluster allocation
            if self.cluster[h] is None:
                self.cluster[h] = VanEmdeBoasTree(self.lower_sqrt)

            target_cluster = self.cluster[h]
            if target_cluster.min is None:
                # Cluster was empty: insert cluster index into summary
                if self.summary is None:
                    self.summary = VanEmdeBoasTree(self.upper_sqrt)
                self.summary.insert(h)
                # Setting min/max in an empty cluster takes O(1) time
                target_cluster.insert(l)
            else:
                # Cluster was not empty: summary already has h, recurse into cluster
                target_cluster.insert(l)

        if x > self.max:
            self.max = x

    def delete(self, x: int) -> None:
        """
        Deletes integer x from the tree.
        Time Complexity: O(log log u).
        """
        if self.min is None or x < 0 or x >= self.u:
            return

        # Case 1: Tree contains only one single element
        if self.min == self.max:
            if x == self.min:
                self.min = self.max = None
            return

        # Case 2: Base universe u == 2
        if self.u == 2:
            if x == 0:
                self.min = self.max = 1
            elif x == 1:
                self.min = self.max = 0
            return

        # Case 3: Deleting the root minimum
        if x == self.min:
            # Find the new minimum from the first non-empty cluster
            if self.summary is None or self.summary.min is None:
                # No clusters exist; only max remains
                self.min = self.max
                return
            first_cluster = self.summary.min
            new_min = self.index(first_cluster, self.cluster[first_cluster].min)  # type: ignore
            self.min = new_min
            x = new_min  # Now proceed to remove new_min from the sub-cluster

        h = self.high(x)
        l = self.low(x)

        if self.cluster[h] is not None:
            self.cluster[h].delete(l)  # type: ignore

            # If the cluster became completely empty, deregister from summary
            if self.cluster[h].min is None:  # type: ignore
                if self.summary is not None:
                    self.summary.delete(h)

                # If x was also the global maximum, update max
                if x == self.max:
                    if self.summary is None or self.summary.max is None:
                        self.max = self.min
                    else:
                        summary_max = self.summary.max
                        self.max = self.index(summary_max, self.cluster[summary_max].max)  # type: ignore
            elif x == self.max:
                # Cluster still has elements; update max to this cluster's new max
                self.max = self.index(h, self.cluster[h].max)  # type: ignore


# ==============================================================================
# 2. SPACE-EFFICIENT HASH-BACKED (SPARSE) VAN EMDE BOAS TREE
# ==============================================================================

class HashVanEmdeBoasTree:
    """
    Space-Optimized vEB Tree using Hash Maps for cluster storage.
    
    Reduces memory from O(u) to O(N log log u), allowing practical usage on large
    universes (e.g., u = 2^32 or u = 2^64).
    """
    def __init__(self, universe_size: int) -> None:
        b = (universe_size - 1).bit_length()
        b = max(b, 1)
        self.u: int = 1 << b
        self.b: int = b
        self.min: Optional[int] = None
        self.max: Optional[int] = None

        if self.u > 2:
            half_b = b // 2
            self.lower_bits = half_b
            self.lower_sqrt = 1 << half_b
            self.upper_sqrt = 1 << (b - half_b)
            self.summary: Optional["HashVanEmdeBoasTree"] = None
            # Dynamic dictionary instead of a pre-allocated array of size upper_sqrt
            self.cluster: Dict[int, "HashVanEmdeBoasTree"] = {}
        else:
            self.lower_bits = 0
            self.lower_sqrt = 1
            self.upper_sqrt = 2
            self.summary = None
            self.cluster = {}

    def high(self, x: int) -> int:
        return x >> self.lower_bits

    def low(self, x: int) -> int:
        return x & (self.lower_sqrt - 1)

    def index(self, h: int, l: int) -> int:
        return (h << self.lower_bits) | l

    def member(self, x: int) -> bool:
        if x == self.min or x == self.max:
            return True
        if self.u == 2 or x < 0 or x >= self.u:
            return False
        h = self.high(x)
        if h not in self.cluster:
            return False
        return self.cluster[h].member(self.low(x))

    def successor(self, x: int) -> Optional[int]:
        if self.u == 2:
            return 1 if (x == 0 and self.max == 1) else None
        if self.min is not None and x < self.min:
            return self.min

        h, l = self.high(x), self.low(x)
        if h in self.cluster and self.cluster[h].max is not None and l < self.cluster[h].max:
            offset = self.cluster[h].successor(l)
            return self.index(h, offset) if offset is not None else None

        if self.summary is None:
            return None
        succ_cluster = self.summary.successor(h)
        if succ_cluster is None:
            return None
        return self.index(succ_cluster, self.cluster[succ_cluster].min)  # type: ignore

    def insert(self, x: int) -> None:
        if self.min is None:
            self.min = self.max = x
            return
        if x == self.min or x == self.max:
            return
        if x < self.min:
            x, self.min = self.min, x

        if self.u > 2:
            h, l = self.high(x), self.low(x)
            if h not in self.cluster:
                self.cluster[h] = HashVanEmdeBoasTree(self.lower_sqrt)
                if self.summary is None:
                    self.summary = HashVanEmdeBoasTree(self.upper_sqrt)
                self.summary.insert(h)
                self.cluster[h].insert(l)
            else:
                self.cluster[h].insert(l)

        if x > self.max:
            self.max = x

    def delete(self, x: int) -> None:
        if self.min is None:
            return
        if self.min == self.max:
            if x == self.min:
                self.min = self.max = None
            return
        if self.u == 2:
            self.min = self.max = 1 if x == 0 else 0
            return

        if x == self.min:
            first_cluster = self.summary.min  # type: ignore
            new_min = self.index(first_cluster, self.cluster[first_cluster].min)  # type: ignore
            self.min = new_min
            x = new_min

        h, l = self.high(x), self.low(x)
        if h in self.cluster:
            self.cluster[h].delete(l)
            if self.cluster[h].min is None:
                del self.cluster[h]  # Free memory dynamically
                self.summary.delete(h)  # type: ignore
                if x == self.max:
                    if self.summary is None or self.summary.max is None:
                        self.max = self.min
                    else:
                        summary_max = self.summary.max
                        self.max = self.index(summary_max, self.cluster[summary_max].max)  # type: ignore
            elif x == self.max:
                self.max = self.index(h, self.cluster[h].max)  # type: ignore


# ==============================================================================
# 3. INDUSTRY-STANDARD LIBRARY COMPARISON (BISECT OVER SORTED CONTAINER)
# ==============================================================================

class LibrarySortedSetSearch:
    """
    Industry-standard approach in Python:
    Uses bisect over a sorted dynamic array to perform successor and predecessor queries.
    
    Time Complexity:
    - Search: O(log N)
    - Successor: O(log N)
    - Predecessor: O(log N)
    - Insert: O(N) (due to list shifting)
    - Delete: O(N)
    """
    def __init__(self) -> None:
        self._items: List[int] = []

    def insert(self, x: int) -> None:
        idx = bisect.bisect_left(self._items, x)
        if idx == len(self._items) or self._items[idx] != x:
            self._items.insert(idx, x)

    def delete(self, x: int) -> None:
        idx = bisect.bisect_left(self._items, x)
        if idx < len(self._items) and self._items[idx] == x:
            self._items.pop(idx)

    def member(self, x: int) -> bool:
        idx = bisect.bisect_left(self._items, x)
        return idx < len(self._items) and self._items[idx] == x

    def successor(self, x: int) -> Optional[int]:
        idx = bisect.bisect_right(self._items, x)
        return self._items[idx] if idx < len(self._items) else None

    def predecessor(self, x: int) -> Optional[int]:
        idx = bisect.bisect_left(self._items, x)
        return self._items[idx - 1] if idx > 0 else None

    def minimum(self) -> Optional[int]:
        return self._items[0] if self._items else None

    def maximum(self) -> Optional[int]:
        return self._items[-1] if self._items else None


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATION WITH DEBUGGING COMMENTARY
# ==============================================================================

class BuggyVanEmdeBoasTree:
    """
    DELIBERATELY BUGGY vEB TREE
    
    BUG 1: Forgetting to swap min and x when x < self.min.
           When an element smaller than self.min is inserted, if you don't swap,
           the old self.min is lost and never inserted into the clusters!
           
    BUG 2: Storing min inside the sub-clusters.
           This causes insert to recurse into clusters even when self.min is updated,
           making TWO recursive calls and destroying the O(log log u) complexity.
    """
    def __init__(self, u: int):
        self.u = u
        self.min = None
        self.max = None
        self.summary = None
        self.lower_sqrt = int(math.isqrt(u)) if u > 2 else 1
        self.upper_sqrt = (u + self.lower_sqrt - 1) // self.lower_sqrt if u > 2 else 2
        self.cluster = [None] * self.upper_sqrt if u > 2 else []

    def high(self, x): return x // self.lower_sqrt
    def low(self, x): return x % self.lower_sqrt
    def index(self, h, l): return h * self.lower_sqrt + l

    def insert(self, x: int) -> None:
        if self.min is None:
            self.min = self.max = x
            return
        
        # FATAL BUG 1: Forgot to swap x and self.min!
        # If x < self.min, self.min is simply overwritten and the old minimum
        # is lost forever because it was never pushed down into the clusters!
        if x < self.min:
            self.min = x
            # Missed: x, self.min = self.min, x (old min should have been pushed down!)
            return  # Bug: returns immediately without storing the old min!

        if self.u > 2:
            h, l = self.high(x), self.low(x)
            if self.cluster[h] is None:
                self.cluster[h] = BuggyVanEmdeBoasTree(self.lower_sqrt)
            if self.cluster[h].min is None:
                if self.summary is None:
                    self.summary = BuggyVanEmdeBoasTree(self.upper_sqrt)
                self.summary.insert(h)
            self.cluster[h].insert(l)

        if x > self.max:
            self.max = x

    def member(self, x: int) -> bool:
        if x == self.min or x == self.max:
            return True
        if self.u <= 2:
            return False
        h = self.high(x)
        if self.cluster[h] is None:
            return False
        return self.cluster[h].member(self.low(x))


# ==============================================================================
# 5. COMPREHENSIVE TEST SUITE
# ==============================================================================

def run_tests():
    """Exhaustively tests vEB trees against invariants, edge cases, and bisect ground truth."""
    print("--- Running Van Emde Boas Tree Base Tests (u = 2) ---")
    v2 = VanEmdeBoasTree(2)
    assert v2.minimum() is None
    assert v2.maximum() is None
    assert not v2.member(0)
    assert not v2.member(1)

    v2.insert(0)
    assert v2.minimum() == 0
    assert v2.maximum() == 0
    assert v2.member(0)
    assert not v2.member(1)
    assert v2.successor(0) is None

    v2.insert(1)
    assert v2.minimum() == 0
    assert v2.maximum() == 1
    assert v2.member(0)
    assert v2.member(1)
    assert v2.successor(0) == 1
    assert v2.predecessor(1) == 0

    v2.delete(0)
    assert v2.minimum() == 1
    assert v2.maximum() == 1
    assert not v2.member(0)
    assert v2.member(1)
    print("Base Case (u = 2): Passed!")

    print("\n--- Running Intermediate Tests (u = 16) ---")
    v16 = VanEmdeBoasTree(16)
    elements = [2, 3, 7, 10, 14]
    for x in elements:
        v16.insert(x)

    # Validate membership
    for x in range(16):
        assert v16.member(x) == (x in elements), f"Member check failed for {x}"

    # Validate min / max
    assert v16.minimum() == 2
    assert v16.maximum() == 14

    # Validate successors
    assert v16.successor(2) == 3
    assert v16.successor(3) == 7
    assert v16.successor(7) == 10
    assert v16.successor(10) == 14
    assert v16.successor(14) is None
    assert v16.successor(1) == 2  # Outside set successor
    assert v16.successor(8) == 10

    # Validate predecessors
    assert v16.predecessor(14) == 10
    assert v16.predecessor(10) == 7
    assert v16.predecessor(7) == 3
    assert v16.predecessor(3) == 2
    assert v16.predecessor(2) is None
    assert v16.predecessor(15) == 14
    assert v16.predecessor(9) == 7

    # Validate deletions
    v16.delete(7)
    assert not v16.member(7)
    assert v16.successor(3) == 10
    assert v16.predecessor(10) == 3

    v16.delete(2)  # Delete minimum
    assert v16.minimum() == 3
    assert not v16.member(2)

    v16.delete(14) # Delete maximum
    assert v16.maximum() == 10
    assert not v16.member(14)
    print("Intermediate (u = 16): Passed!")

    print("\n--- Running Hash-Backed vEB Tree Tests (u = 256) ---")
    hveb = HashVanEmdeBoasTree(256)
    test_set = [15, 30, 45, 90, 180, 240]
    for x in test_set:
        hveb.insert(x)

    assert hveb.min == 15
    assert hveb.max == 240
    assert hveb.successor(45) == 90
    assert hveb.successor(90) == 180
    assert hveb.successor(240) is None
    assert hveb.successor(100) == 180

    hveb.delete(15)  # Delete min
    assert hveb.min == 30
    assert hveb.successor(30) == 45

    hveb.delete(240) # Delete max
    assert hveb.max == 180
    print("Hash-Backed vEB (u = 256): Passed!")

    print("\n--- Randomized Stress & Comparison Test against Bisect Ground Truth ---")
    import random
    rng = random.Random(42)
    universe = 1024
    veb_test = VanEmdeBoasTree(universe)
    lib_test = LibrarySortedSetSearch()

    active_items = set()
    for step in range(300):
        action = rng.choice(["insert", "insert", "delete", "query"])
        val = rng.randint(0, universe - 1)

        if action == "insert":
            veb_test.insert(val)
            lib_test.insert(val)
            active_items.add(val)
        elif action == "delete" and active_items:
            target = rng.choice(list(active_items))
            veb_test.delete(target)
            lib_test.delete(target)
            active_items.remove(target)
        else:
            # Query random value
            q = rng.randint(0, universe - 1)
            assert veb_test.member(q) == lib_test.member(q)
            assert veb_test.successor(q) == lib_test.successor(q)
            assert veb_test.predecessor(q) == lib_test.predecessor(q)

        # Invariant checks
        assert veb_test.minimum() == lib_test.minimum()
        assert veb_test.maximum() == lib_test.maximum()

    print("Randomized Stress Test (300 ops against bisect): All assertions passed!")

    print("\n--- Demonstrating Deliberately Buggy Implementation Failure ---")
    buggy = BuggyVanEmdeBoasTree(16)
    # Insert 10, then insert 5 (which is smaller than 10)
    buggy.insert(10)
    buggy.insert(5)  # Due to Bug 1, 10 is wiped and lost!
    
    print(f"Buggy vEB member(5): {buggy.member(5)}")
    print(f"Buggy vEB member(10): {buggy.member(10)}")
    assert not buggy.member(10), "Expected bug to manifest: 10 was lost when 5 was inserted without swap!"
    print("Bug confirmed: Omitting swap on smaller insert caused permanent data loss.")

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")


# ==============================================================================
# 6. MAIN EXECUTION BLOCK WITH EDUCATIONAL TRACES
# ==============================================================================

def main():
    print("=" * 70)
    print("   VAN EMDE BOAS TREE: THEORY, RECURSION & TRACES")
    print("=" * 70)

    # 1. Run all unit tests
    run_tests()

    # 2. Educational Step-by-Step Visualization of Universe Decomposition
    print("\n" + "=" * 70)
    print("   STEP-BY-STEP VISUAL TRACE: SQUARE ROOT DECOMPOSITION")
    print("=" * 70)

    u_example = 16
    veb = VanEmdeBoasTree(u_example)
    print(f"\nConstructing VanEmdeBoasTree for universe u = {u_example}:")
    print(f"  Universe Size u: {veb.u} (Bits b = {veb.b})")
    print(f"  Upper Sqrt (Clusters): {veb.upper_sqrt}")
    print(f"  Lower Sqrt (Offsets):  {veb.lower_sqrt}")

    demo_keys = [2, 5, 8, 12, 14]
    print(f"\nInserting keys {demo_keys} into the vEB Tree:")
    for k in demo_keys:
        h = veb.high(k)
        l = veb.low(k)
        print(f"  Insert({k:>2}) -> Cluster (high): {h}, Offset (low): {l}")
        veb.insert(k)

    print(f"\nTree Summary State:")
    print(f"  Global Minimum: {veb.minimum()}")
    print(f"  Global Maximum: {veb.maximum()}")
    if veb.summary:
        print(f"  Active Cluster Indices in Summary: min={veb.summary.min}, max={veb.summary.max}")

    print("\nTesting Successor Searches across cluster boundaries:")
    test_queries = [2, 4, 5, 8, 12, 14]
    for q in test_queries:
        succ = veb.successor(q)
        pred = veb.predecessor(q)
        print(f"  Target: {q:>2} -> Predecessor: {str(pred):>4} | Successor: {str(succ):>4}")


if __name__ == "__main__":
    main()
