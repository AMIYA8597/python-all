r"""
# Fractional Cascading: Algorithmic Mechanics, Mathematical Proofs, and Geometric Applications

## A. Concept Name
Fractional Cascading (Chazelle-Guibas Technique).

## B. One-Sentence Definition
Fractional Cascading is an algorithmic technique that reduces the time required to locate a single query element across $k$ separate sorted lists from $O(k \log N)$ down to an optimal $O(\log N + k)$ by propagating fractional samples and precomputed bridge pointers between adjacent lists in $O(N)$ linear space.

## C. Why Does This Exist? (What problem does it solve?)
In computational geometry, multi-attribute database indexing, and spatial data structures (such as Layered Range Trees, Segment Trees, and Interval Trees), a system must frequently search for the **exact same query value** $q$ across a collection of $k$ distinct sorted lists $L_0, L_1, \dots, L_{k-1}$, containing a combined total of $N = \sum |L_i|$ elements.

Consider the naive and extreme alternatives:
1. **Naive Independent Binary Searches**:
   - Perform a separate binary search for $q$ in each of the $k$ lists.
   - Time: $O(\sum_{i=0}^{k-1} \log |L_i|) = O(k \log(N/k))$ or $O(k \log N)$.
   - When $k$ is large—for instance, in a 2D Range Tree where $k = O(\log N)$—query time degrades to $O(\log^2 N)$.
2. **Full Merge Duplication**:
   - Copy every element from list $i+1$ up into list $i$ with direct pointers.
   - While query time drops to $O(\log N + k)$, memory consumption explodes to $O(k \cdot N)$, rendering it impractical for large datasets.

Fractional Cascading solves this fundamental tension. By propagating only a carefully chosen **fraction** $\alpha$ (typically $\alpha = 1/2$) of elements from list $i+1$ up to list $i$, it guarantees:
- **Optimal Query Time**: $O(\log N + k)$—a single initial binary search in list 0 followed by $O(1)$ pointer dereferences and comparisons per subsequent list.
- **Linear Space**: $O(N)$ total space, because the sizes of the augmented lists form a convergent geometric series bounded by $2N$.

## D. Intuition & Real-Life Analogy
- **The Airport Express Connections**: Imagine landing at an enormous international hub with $k$ terminal buildings. In each terminal, you must locate the gate closest to your flight time $q$.
  - *Naive Approach*: You exit into the main lobby of Terminal 0, consult the giant flight monitor ($O(\log N)$ binary search), and walk to your gate. Then you take a shuttle to Terminal 1, stand in front of Terminal 1's monitor, read the entire board again ($O(\log N)$), and repeat this for all $k$ terminals ($O(k \log N)$).
  - *Fractional Cascading*: When leaving your gate in Terminal 0, the gate agent hands you a transfer slip with a direct express pointer into Terminal 1's corridor. Because Terminal 0 already displayed sample gates from Terminal 1, your transfer slip drops you within **at most one or two doors** of your exact destination gate in Terminal 1 ($O(1)$ adjustment). You walk directly to the next gate without ever looking at another master flight monitor.
- **The Mountain Trail Mile-Markers**: Climbing down a series of $k$ layered mountain ridges. Instead of consulting a full topographical map on every single ridge, each ridge has markers pointing directly to the closest path on the ridge below.

## E. Mental Model
We augment each original list $L_i$ into an augmented list $M_i$.
Construction proceeds backwards from level $k-1$ down to 0:
- $M_{k-1} = L_{k-1}$.
- For each level $i = k-2$ down to 0:
  1. Extract sample $S_{i+1}$ containing every second element (odd indices) of $M_{i+1}$.
  2. Merge the original list $L_i$ with the sample $S_{i+1}$ to form $M_i$.
  3. Every node in $M_i$ stores:
     - `val`: The numeric value.
     - `orig_idx`: The index of the first element in the original list $L_i$ that is $\ge val$.
     - `down_ptr`: The index of the first element in $M_{i+1}$ that is $\ge val$.

```text
Level 0: M_0 = Merge(L_0, Sample(M_1))
Index:        [0]        [1]        [2]        [3]        [4]
Values:     | 24 |     | 25 |     | 64 |     | 65 |     | 80 |
             |          |          |          |          |
  orig_idx:  0          1          1          2          3     (Pointers into L_0)
  down_ptr:  1          1          3          3          4     (Pointers into M_1)
             |          |          |          |          |
             v          v          v          v          v
Level 1: M_1 = Merge(L_1, Sample(M_2))
Index:        [0]        [1]        [2]        [3]        [4]
Values:     | 23 |     | 25*|     | 26 |     | 44*|     | 66*|
                         ^                     ^          ^
                         |-- (Sampled into M_0) |          |
```

When querying for target $q = 25$:
1. Binary search in $M_0$ finds index 1 (`val = 25`).
2. Read `orig_idx = 1` $\rightarrow$ Result for $L_0$ is at index 1 (`val = 64`).
3. Follow `down_ptr = 1` into $M_1$.
4. Check candidates in $M_1$: index 1 has `val = 25`. At most 1 step back check $\rightarrow$ Result for $L_1$ found in $O(1)$!
5. Repeat for all subsequent levels!

## F. Formal Technical Explanation
Formally introduced by Bernard Chazelle and Leonidas J. Guibas in their landmark 1986 paper *"Fractional Cascading: I. Basic Components and Extensions"*, fractional cascading operates on a **catalog graph** $G = (V, E)$. In the linear chain configuration:
- Vertices $v_0, v_1, \dots, v_{k-1}$ each store a sorted catalog (list) $L_i \subset \mathcal{U}$.
- The edges form a directed path $(v_0, v_1), (v_1, v_2), \dots, (v_{k-2}, v_{k-1})$.

### The Invariant and Bounded-Gap Property
Let $S_{i+1} \subset M_{i+1}$ be formed by sampling every $d$-th element of $M_{i+1}$ (typically $d = 2$, fraction $\alpha = 1/2$).
Between any two consecutive sampled elements $s_a, s_{a+1} \in S_{i+1}$, there are at most $d - 1 = 1$ unsampled elements in $M_{i+1}$.
Because $S_{i+1} \subseteq M_i$, when binary search locates the successor of query $q$ in $M_i$ at index $pos$:
- Let $s$ be the smallest sampled element in $S_{i+1}$ such that $s \ge q$.
- The element $M_i[pos]$ satisfies $q \le M_i[pos] \le s$.
- Consequently, the bridge pointer $cand = M_i[pos].down\_ptr$ points to an element in $M_{i+1}$ such that $cand \le \text{index}(s)$.
- Because at most $d - 1$ elements in $M_{i+1}$ lie between the predecessor of $s$ in $S_{i+1}$ and $s$ itself, the true successor of $q$ in $M_{i+1}$ must reside in the index window $[cand - (d - 1), cand]$.
- For $d = 2$, this window contains at most 2 elements! Thus, finding the exact successor of $q$ in $M_{i+1}$ requires at most **one or two comparisons** ($O(1)$ time).

## G. Mathematical Foundation
### 1. Space Convergence Proof (Geometric Series)
Let $|L_i| = n_i$ be the size of original list $L_i$, and let $|M_i| = m_i$ be the size of augmented list $M_i$.
For fraction $\alpha = 1/2$:
$$m_{k-1} = n_{k-1}$$
$$m_{k-2} = n_{k-2} + \left\lfloor \frac{1}{2} m_{k-1} \right\rfloor \le n_{k-2} + \frac{1}{2} n_{k-1}$$
$$m_i \le n_i + \frac{1}{2} m_{i+1} \le \sum_{j=i}^{k-1} \left(\frac{1}{2}\right)^{j-i} n_j$$

Summing the sizes of all augmented lists across all $k$ levels:
$$\sum_{i=0}^{k-1} m_i \le \sum_{i=0}^{k-1} \sum_{j=i}^{k-1} \left(\frac{1}{2}\right)^{j-i} n_j = \sum_{j=0}^{k-1} n_j \sum_{l=0}^j \left(\frac{1}{2}\right)^l < \sum_{j=0}^{k-1} n_j \sum_{l=0}^\infty \left(\frac{1}{2}\right)^l = 2 \sum_{j=0}^{k-1} n_j = 2N$$

Therefore, the total auxiliary memory is strictly bounded by $2N = O(N)$. Linear space is guaranteed.

### 2. Query Time Bound
- Binary search in $M_0$: $O(\log m_0) \le O(\log 2N) = O(\log N)$.
- Traversal across levels $1, \dots, k-1$:
  At each level $i$, the algorithm performs $O(1)$ pointer dereferencing and at most $\le 2$ scalar comparisons to adjust the candidate pointer.
- Total query time:
  $$T(N, k) = O(\log N) + \sum_{i=1}^{k-1} O(1) = O(\log N + k)$$

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - **Preprocessing / Build**: $O(N)$ if lists are pre-sorted; $O(N \log N)$ if input lists require sorting. Each merge operation takes linear time in the size of the lists being merged.
  - **Query (Best Case)**: $O(1 + k)$ when the target matches the very first element of $M_0$.
  - **Query (Average & Worst Case)**: $O(\log N + k)$ optimal time.
- **Space Complexity**:
  - Total Memory: $O(N)$ total storage ($\le 2N$ total nodes across all augmented arrays).
  - Auxiliary Memory during Query: $O(1)$ working space (aside from the $O(k)$ output array).
- **Cache & Memory Architecture**:
  - Nodes in $M_i$ are laid out contiguously in memory arrays.
  - The initial binary search enjoys standard cache-line prefetching.
  - While traversing downward across levels $i \to i+1$, only a single memory jump is made per list, minimizing cache-line misses compared to performing $k$ full binary searches with $\log N$ cache misses each!

## I. Common Mistakes & Pitfalls
1. **Direction Confusion in Down Pointers**:
   Storing a pointer to the *predecessor* instead of the *successor* (or vice versa), and scanning in the wrong direction during the $O(1)$ adjustment step.
2. **Missing the Reverse Adjustment Step**:
   Assuming `cand = M_i[pos].down_ptr` is already the exact answer in $M_{i+1}$. Because $M_i[pos]$ could be an element from $L_i$ (not sampled from $M_{i+1}$), $M_{i+1}[cand]$ is merely an upper bound; one must step backwards while $M_{i+1}[cand - 1].val \ge q$.
3. **Improper Sampling Stride during Merge**:
   Sampling elements *during* the merge loop rather than pre-extracting every second element of $M_{i+1}$. This easily corrupts the density guarantee and causes unbounded step adjustments.
4. **Out-of-Bounds Queries**:
   When $q > \max(L_i)$ or $q > \max(M_i)$, `pos` equals $\text{len}(M_i)$. The algorithm must safely handle end-of-list sentinels without raising `IndexError`.
5. **Ignoring Duplicates**:
   If identical values exist across or within lists, inconsistent tie-breaking can lead to misaligned bridge pointers. Using strict `bisect_left` lower-bound invariants prevents duplicates from breaking the chain.

## J. Common Confusions
- **Fractional Cascading vs. Skip Lists**:
  Skip Lists use probabilistic coin-flips to create multi-level fast-lanes within a *single* dynamic sorted set. Fractional Cascading is a *deterministic* static indexing technique that bridges *multiple distinct* sorted lists.
- **Fractional Cascading vs. Layered Range Trees**:
  A Layered Range Tree is a specific data structure for 2D orthogonal range searching. Fractional Cascading is the underlying algorithmic technique that reduces the 2D range query time from $O(\log^2 N + K)$ to $O(\log N + K)$.
- **Fractional Cascading vs. Merge-Sort**:
  Merge-sort merges lists to combine them into a single sorted output. Fractional Cascading augments the individual lists while keeping their identities separate, so individual membership and rankings are preserved.

## K. When To Use It
- You need to search for the same target key $q$ across $k \ge 3$ sorted lists repeatedly.
- Implementing 2D and multi-dimensional orthogonal range trees, segment trees, or interval stabbing queries.
- Read-heavy systems where datasets are static or batch-updated, and query latency must strictly obey an $O(\log N + k)$ SLA.

## L. When NOT To Use It
- The collection undergoes high-frequency real-time insertions and deletions. Rebuilding or rebalancing cascading bridge pointers in dynamic settings is notoriously complex (though dynamic fractional cascading exists, its constant factors are heavy).
- Small number of lists ($k \le 2$). For $k = 2$, two standard binary searches take $2 \log N$ comparisons, which is faster in practice than the overhead of augmented node structures.
- Uncorrelated queries where each list is queried with a different search key $q_i$.

## M. Trade-offs
| Strategy | Query Time | Preprocessing Time | Auxiliary Space | Dynamic Updates |
| :--- | :--- | :--- | :--- | :--- |
| **Independent Binary Searches** | $O(k \log N)$ | $O(N \log N)$ | $O(1)$ | Easy ($O(\log N)$ per list) |
| **Full List Duplication** | $O(\log N + k)$ | $O(k \cdot N)$ | $O(k \cdot N)$ | Very Difficult |
| **Fractional Cascading** | $O(\log N + k)$ | $O(N)$ (if sorted) | $O(N)$ ($\le 2N$ nodes) | Complex |

## N. Debugging Tips
- **Assert Bounded Step-Back**: In the query adjustment loop `while cand > 0 and M[i+1][cand-1].val >= q: cand -= 1`, assert that the loop executes at most 2 times. If it ever executes $\ge 3$ times, the sample stride invariant has broken!
- **Parity Test Suite**: Validate query results against naive `[bisect.bisect_left(L, q) for L in lists]` across random integer sets.
- **Inspect Edge Keys**: Explicitly test $q = \min - 1$, $q = \max + 1$, exact member keys, and empty list entries.

## O. Memory Hook
**"Cascade half the stairs, step once everywhere else!"**
Remember: take half the elements from the floor below, merge them into your current floor, and after one initial binary search, you only ever take a single step on each flight of stairs.

## P. Active Recall Questions
1. Why does sampling every second element ($\alpha = 1/2$) guarantee that total space across all augmented lists converges to $\le 2N$?
2. During a query, why does the candidate pointer in $M_{i+1}$ need at most two backward step adjustments to find the exact lower bound of $q$?
3. How does fractional cascading accelerate 2D orthogonal range searching in a range tree from $O(\log^2 N + K)$ to $O(\log N + K)$?
4. What happens to the space complexity if you choose a sample fraction $\alpha = 1/3$ versus $\alpha = 1/2$?

## Q. Interview Questions & Answers
- **Q1: What is the exact role of the `orig_idx` field in each node of an augmented list $M_i$?**  
  *Answer:* Because $M_i$ contains both original elements of $L_i$ and sampled elements from $M_{i+1}$, locating an element in $M_i$ does not directly yield an index in $L_i$. The `orig_idx` pointer precomputes the index of the first element in $L_i$ with value $\ge node.val$. This allows an instantaneous $O(1)$ translation from the augmented search space back to the original client list.
- **Q2: Can Fractional Cascading be generalized to tree structures instead of linear chains?**  
  *Answer:* Yes. In a catalog tree (e.g., a Segment Tree), each node $v$ has children $u_1, u_2$. Node $v$ receives a fractional sample (e.g., fraction $1/4$) from each of its children. Because each node has bounded degree $d$, the geometric series still converges to $O(N)$ space, allowing a query to traverse from root to leaf in $O(\log N + \text{depth}) = O(\log N)$ time.
- **Q3: Why is naive forward linear searching (`while val < q: idx += 1`) incorrect when using successor bridge pointers?**  
  *Answer:* A successor bridge pointer from $M_i$ to $M_{i+1}$ targets the first element in $M_{i+1}$ that is $\ge M_i[pos].val$. Because $M_i[pos].val \ge q$, the pointed element in $M_{i+1}$ is guaranteed to be $\ge q$. Thus, the true lower bound of $q$ in $M_{i+1}$ can never lie *forward* (to the right); it can only lie *backward* (to the left) by at most 1 or 2 elements. Scanning forward will either miss elements or move away from the true successor.

## R. Project Connections
- **CGAL (Computational Geometry Algorithms Library)**: Implements fractional cascading in multi-dimensional range trees and polygon stabbing algorithms.
- **GIS and Spatial Databases (PostGIS, GeoPandas)**: Accelerates window and bounding-box queries across layered spatial partitionings.
- **Network Packet Classification**: Speeds up multidimensional IP filter rule lookups where packets are matched against source/destination IP ranges and port intervals.

## S. Edge Cases & Boundary Conditions
1. **Empty Lists**: Any list in the collection may be empty (`[]`). The cascading structure must gracefully propagate empty samples without crashing.
2. **Target Below All Elements**: Query $q < \min(L_i)$ for all $i$. Returns index 0 for all lists.
3. **Target Above All Elements**: Query $q > \max(L_i)$ for all $i$. Returns $\text{len}(L_i)$ (or `None` sentinel) for all lists.
4. **Duplicate Values**: Lists containing identical values. `bisect_left` semantics must consistently find the first occurrence.
5. **Single-List Collection ($k = 1$)**: Degenerates gracefully into a single standard binary search.

## T. Algorithmic Variants & Paradigms
- **Linear Chain Fractional Cascading**: Classic sequence of catalogs $L_0 \to L_1 \to \dots \to L_{k-1}$.
- **Tree-Structured Fractional Cascading**: Propagates fractions up binary trees (Segment Trees, Range Trees).
- **Graph Fractional Cascading**: General catalog graphs with bounded in-degree and out-degree.
- **Dynamic Fractional Cascading**: Mehlhorn & Näher's variant supporting insertions and deletions using amortized rebuilding and red-black balancing.

## U. Algorithmic Comparison Table
| Feature | Naive Multi-Binary Search | Fractional Cascading | 2D Range Tree (Standard) | 2D Range Tree (Layered with FC) |
| :--- | :--- | :--- | :--- | :--- |
| **Lists Queried** | $k$ lists | $k$ lists | $\log N$ canonical nodes | $\log N$ canonical nodes |
| **Query Complexity** | $O(k \log(N/k))$ | $O(\log N + k)$ | $O(\log^2 N + K)$ | $O(\log N + K)$ |
| **Space Overhead** | $O(1)$ auxiliary | $O(N)$ ($\le 2N$ nodes) | $O(N \log N)$ | $O(N \log N)$ |
| **Implementation Complexity** | Trivial | Moderate | High | Advanced |

## V. Practical Implementation Exercises
1. Extend `FractionalCascading` to return both the lower bound (first element $\ge q$) and the upper bound (first element $> q$) simultaneously.
2. Implement a 2D Layered Range Tree utilizing fractional cascading to perform orthogonal range reporting in $O(\log N + K)$ time.
3. Profile memory cache misses of Fractional Cascading against naive binary searches on an array of 50 sorted lists with $10^5$ integers.

## W. Step-by-Step Execution Trace
Let $L_0 = [24, 64, 65, 80, 93]$, $L_1 = [23, 25, 26]$, $L_2 = [13, 44, 62, 66]$, $L_3 = [11, 35, 46, 79, 81]$.
Query target: $q = 25$.

| Level | List Size | Augmented List ($M_i$ Values) | Binary / Bridge Pos | Node Val | Orig Idx in $L_i$ | Step-Backs | Target Result in $L_i$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | $|M_0|=8$ | $[24, 25, 26, 44, 64, 65, 80, 93]$ | Pos 1 (Binary Search) | 25 | 1 | 0 | $L_0[1] = 64$ |
| **1** | $|M_1|=5$ | $[23, 25, 26, 44, 66]$ | Pos 1 (Bridge from $M_0$) | 25 | 1 | 0 | $L_1[1] = 25$ |
| **2** | $|M_2|=6$ | $[13, 35, 44, 62, 66, 79]$ | Pos 1 (Bridge from $M_1$) | 35 | 1 | 0 | $L_2[1] = 44$ |
| **3** | $|M_3|=5$ | $[11, 35, 46, 79, 81]$ | Pos 1 (Bridge from $M_2$) | 35 | 1 | 0 | $L_3[1] = 35$ |

Total Comparisons: $\log_2(8) = 3$ comparisons in Level 0, plus $0$ step-back comparisons in subsequent levels. Total = 3 comparisons vs Naive = $3 + 2 + 2 + 3 = 10$ comparisons!

## X. Key Takeaways & Summary Anchor
- Fractional Cascading trades a modest $2\times$ space constant for an asymptotic speedup from $O(k \log N)$ to $O(\log N + k)$.
- The $1/2$ sampling invariant mathematically guarantees that between any two sampled nodes, at most one unsampled node exists, bounding pointer adjustment to at most 2 checks per level.
- It is the gold standard theoretical and practical engine powering optimal multi-dimensional range searching in computational geometry.
"""

from typing import List, Tuple, Optional, Sequence, Any
import bisect


# ==============================================================================
# 1. DATA STRUCTURE DEFINITIONS
# ==============================================================================

class CascadeNode:
    """
    A single element within an augmented fractional cascading list.
    
    Attributes:
        val (int): The numerical key of the element.
        orig_idx (int): The index of the smallest element in the original list L_i
                        that is >= val (the lower bound in L_i).
        down_ptr (int): The index of the smallest element in augmented list M_{i+1}
                        that is >= val (the bridge pointer to the next level).
    """
    __slots__ = ('val', 'orig_idx', 'down_ptr')

    def __init__(self, val: int, orig_idx: int, down_ptr: int) -> None:
        self.val: int = val
        self.orig_idx: int = orig_idx
        self.down_ptr: int = down_ptr

    def __repr__(self) -> str:
        return f"Node(val={self.val}, orig={self.orig_idx}, down={self.down_ptr})"


# ==============================================================================
# 2. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION: FRACTIONAL CASCADING
# ==============================================================================

class FractionalCascading:
    """
    Production-grade, educational implementation of Chazelle-Guibas Fractional Cascading.
    
    Coordinates search for a target key `q` across `k` sorted lists in O(log N + k)
    query time and O(N) total space.
    """

    def __init__(self, lists: Sequence[Sequence[int]]) -> None:
        """
        Initializes and constructs the augmented fractional cascading data structure.
        
        Args:
            lists: A sequence of k sorted integer lists.
        """
        # Defensive copy of input lists to enforce immutability
        self._orig_lists: List[List[int]] = [list(lst) for lst in lists]
        self._k: int = len(self._orig_lists)
        self._augmented_lists: List[List[CascadeNode]] = []
        
        # Verify sorted invariant
        for idx, lst in enumerate(self._orig_lists):
            for j in range(1, len(lst)):
                if lst[j] < lst[j - 1]:
                    raise ValueError(f"Input list at index {idx} is not sorted: {lst}")
                    
        self._build()

    @property
    def k(self) -> int:
        """Returns the number of lists in the cascade."""
        return self._k

    @property
    def augmented_lists(self) -> List[List[CascadeNode]]:
        """Returns the augmented cascading lists."""
        return self._augmented_lists

    def _build(self) -> None:
        """
        Builds the augmented lists M_0, M_1, ..., M_{k-1} from bottom to top.
        
        Time Complexity: O(N) where N is the total number of elements.
        Space Complexity: O(N) bounded by 2N total nodes.
        """
        if self._k == 0:
            self._augmented_lists = []
            return

        self._augmented_lists = [[] for _ in range(self._k)]

        # Base level M_{k-1} is constructed directly from original list L_{k-1}
        last_idx = self._k - 1
        self._augmented_lists[last_idx] = [
            CascadeNode(val=v, orig_idx=j, down_ptr=0)
            for j, v in enumerate(self._orig_lists[last_idx])
        ]

        # Propagate samples upward from level k-2 down to 0
        for i in range(self._k - 2, -1, -1):
            next_m = self._augmented_lists[i + 1]
            # Sample every second element (odd indices: 1, 3, 5, ...)
            # This ensures at most 1 unsampled element lies between consecutive sampled items
            sampled_nodes = [next_m[j] for j in range(1, len(next_m), 2)]

            curr_l = self._orig_lists[i]
            merged_vals: List[int] = []
            
            # Linear two-way merge of curr_l and sampled_nodes
            p_orig = 0
            p_samp = 0
            len_orig = len(curr_l)
            len_samp = len(sampled_nodes)

            while p_orig < len_orig and p_samp < len_samp:
                if curr_l[p_orig] <= sampled_nodes[p_samp].val:
                    merged_vals.append(curr_l[p_orig])
                    p_orig += 1
                else:
                    merged_vals.append(sampled_nodes[p_samp].val)
                    p_samp += 1

            while p_orig < len_orig:
                merged_vals.append(curr_l[p_orig])
                p_orig += 1

            while p_samp < len_samp:
                merged_vals.append(sampled_nodes[p_samp].val)
                p_samp += 1

            # Compute orig_idx and down_ptr for each merged element via two monotonic sweeps
            idx_orig = 0
            idx_down = 0
            augmented_level: List[CascadeNode] = []
            len_next_m = len(next_m)

            for val in merged_vals:
                # Find first element in curr_l >= val
                while idx_orig < len_orig and curr_l[idx_orig] < val:
                    idx_orig += 1
                # Find first element in next_m >= val
                while idx_down < len_next_m and next_m[idx_down].val < val:
                    idx_down += 1

                augmented_level.append(CascadeNode(val=val, orig_idx=idx_orig, down_ptr=idx_down))

            self._augmented_lists[i] = augmented_level

    def search(self, query: int) -> List[Tuple[int, Optional[int]]]:
        """
        Searches for the lower bound (first element >= query) across all k lists.
        
        Args:
            query (int): The target search key.
            
        Returns:
            List[Tuple[int, Optional[int]]]: A list of length k containing (index, value)
            tuples for each original list. If no element in list i is >= query,
            returns (len(L_i), None).
            
        Complexity:
            Time: O(log N + k)
            Space: O(k) for the result list.
        """
        if self._k == 0:
            return []

        results: List[Tuple[int, Optional[int]]] = []
        m0 = self._augmented_lists[0]

        # Step 1: Perform the single binary search at level 0 (O(log |M_0|))
        pos = bisect.bisect_left(m0, query, key=lambda node: node.val) if m0 else 0

        # Step 2: Cascade down through all levels using bridge pointers (O(1) per level)
        for i in range(self._k):
            curr_augmented = self._augmented_lists[i]
            curr_original = self._orig_lists[i]

            # Determine the lower-bound index in the original list L_i
            if pos < len(curr_augmented):
                orig_index = curr_augmented[pos].orig_idx
            else:
                orig_index = len(curr_original)

            # Retrieve corresponding value if within range
            if orig_index < len(curr_original):
                val: Optional[int] = curr_original[orig_index]
            else:
                val = None

            results.append((orig_index, val))

            # Advance to level i + 1 if not at the final list
            if i < self._k - 1:
                next_augmented = self._augmented_lists[i + 1]
                if pos < len(curr_augmented):
                    cand_pos = curr_augmented[pos].down_ptr
                else:
                    cand_pos = len(next_augmented)

                # Adjust candidate pointer: cand_pos is guaranteed to be within at most
                # 2 steps to the right of the true lower bound in next_augmented.
                # Step backwards while previous element is still >= query.
                step_count = 0
                while cand_pos > 0 and next_augmented[cand_pos - 1].val >= query:
                    cand_pos -= 1
                    step_count += 1
                    # Invariant Check: Fractional cascading mathematically guarantees step_count <= 2
                    if step_count > 2:
                        raise RuntimeError(
                            f"Fractional cascading invariant violated! Step count {step_count} > 2."
                        )

                pos = cand_pos

        return results

    def search_indices_only(self, query: int) -> List[int]:
        """Convenience method returning strictly the lower-bound indices."""
        return [res[0] for res in self.search(query)]


# ==============================================================================
# 3. INDUSTRY BASELINE IMPLEMENTATION (NAIVE MULTI-BINARY SEARCH)
# ==============================================================================

class NaiveMultiBinarySearch:
    """
    Standard industry baseline: Executes independent binary searches across each list.
    
    Complexity:
        Time: O(k * log(N / k)) or O(k * log N) per query.
        Space: O(1) auxiliary space.
    """

    def __init__(self, lists: Sequence[Sequence[int]]) -> None:
        self._lists = [list(lst) for lst in lists]

    def search(self, query: int) -> List[Tuple[int, Optional[int]]]:
        """Searches each list independently using bisect.bisect_left."""
        results: List[Tuple[int, Optional[int]]] = []
        for lst in self._lists:
            idx = bisect.bisect_left(lst, query)
            val = lst[idx] if idx < len(lst) else None
            results.append((idx, val))
        return results

    def search_indices_only(self, query: int) -> List[int]:
        return [bisect.bisect_left(lst, query) for lst in self._lists]


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATION (EDUCATIONAL / DEBUGGING PURPOSES)
# ==============================================================================

class BuggyFractionalCascading:
    """
    Deliberately flawed Fractional Cascading implementation reproducing common traps:
    
    1. Bug #1: Stride increment inside the merge loop's else block (`p2 += 2`).
       If original list L_i has multiple smaller elements, p2 does not advance.
       When an element from L_{i+1} is selected, jumping by 2 skips alternate elements
       without ever inspecting them, destroying the bounded-gap invariant!
    2. Bug #2: Directional confusion during query: scanning forward instead of backward
       (`while val < query: cand += 1`). Since the bridge pointer is an upper bound,
       scanning forward moves away from the lower bound, returning incorrect answers
       or running off the end of the array.
    """

    def __init__(self, lists: List[List[int]]) -> None:
        self.k = len(lists)
        self.lists = lists
        self.cascaded_lists: List[List[Any]] = []
        self._buggy_build()

    def _buggy_build(self) -> None:
        if not self.lists:
            return
        self.cascaded_lists = [[] for _ in range(self.k)]
        self.cascaded_lists[-1] = [CascadeNode(v, j, 0) for j, v in enumerate(self.lists[-1])]

        for i in range(self.k - 2, -1, -1):
            l1 = self.lists[i]
            l2 = self.cascaded_lists[i + 1]
            merged = []
            p1, p2 = 0, 0

            # BUG #1: Mixing sampling directly into merge loop
            while p1 < len(l1) or p2 < len(l2):
                if p2 >= len(l2) or (p1 < len(l1) and l1[p1] <= l2[p2].val):
                    node = CascadeNode(l1[p1], p1, p2)
                    merged.append(node)
                    p1 += 1
                else:
                    node = CascadeNode(l2[p2].val, p1, p2)
                    merged.append(node)
                    p2 += 2  # BUG: Jumps by 2 only when l2 is chosen!
            self.cascaded_lists[i] = merged

    def search(self, val: int) -> List[int]:
        if not self.cascaded_lists:
            return []
        arr = [n.val for n in self.cascaded_lists[0]]
        idx = bisect.bisect_left(arr, val)
        results = []
        curr_idx = idx

        for i in range(self.k):
            # BUG #2: Scans forward instead of backward
            while curr_idx < len(self.cascaded_lists[i]) and self.cascaded_lists[i][curr_idx].val < val:
                curr_idx += 1

            if curr_idx < len(self.cascaded_lists[i]):
                results.append(self.cascaded_lists[i][curr_idx].orig_idx)
            else:
                results.append(len(self.lists[i]))

            if i < self.k - 1 and curr_idx < len(self.cascaded_lists[i]):
                curr_idx = self.cascaded_lists[i][curr_idx].down_ptr
            else:
                curr_idx = len(self.cascaded_lists[i + 1]) if i < self.k - 1 else 0

        return results


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive assert-based test suite verifying all invariants and edge cases.
    """
    print(">>> Running Fractional Cascading Test Suite...")

    # Test Case 1: Standard Literature Example
    lists_standard = [
        [24, 64, 65, 80, 93],
        [23, 25, 26],
        [13, 44, 62, 66],
        [11, 35, 46, 79, 81]
    ]
    fc = FractionalCascading(lists_standard)
    naive = NaiveMultiBinarySearch(lists_standard)

    # Validate space bound: total augmented nodes <= 2 * total elements
    total_orig_elements = sum(len(lst) for lst in lists_standard)
    total_augmented_nodes = sum(len(m) for m in fc.augmented_lists)
    assert total_augmented_nodes <= 2 * total_orig_elements, (
        f"Space bound violated: {total_augmented_nodes} > 2 * {total_orig_elements}"
    )

    # Test query q = 25
    expected_q25 = [(1, 64), (1, 25), (1, 44), (1, 35)]
    assert fc.search(25) == expected_q25, f"Search(25) failed: {fc.search(25)}"
    assert naive.search(25) == expected_q25

    # Test query q = 10 (smaller than all elements in all lists)
    expected_q10 = [(0, 24), (0, 23), (0, 13), (0, 11)]
    assert fc.search(10) == expected_q10, f"Search(10) failed: {fc.search(10)}"

    # Test query q = 100 (larger than all elements in all lists)
    expected_q100 = [(5, None), (3, None), (4, None), (5, None)]
    assert fc.search(100) == expected_q100, f"Search(100) failed: {fc.search(100)}"

    # Test Case 2: Boundary and Exact Match Keys
    for key in [11, 13, 23, 24, 25, 26, 35, 44, 46, 62, 64, 65, 66, 79, 80, 81, 93]:
        assert fc.search(key) == naive.search(key), f"Mismatch on exact key {key}"

    # Test Case 3: Empty Lists and Edge Case Configurations
    # 3a: Fully empty collection
    fc_empty = FractionalCascading([])
    assert fc_empty.search(42) == []

    # 3b: Collection containing empty lists
    lists_with_empty = [[], [10, 20, 30], [], [5, 15, 25], []]
    fc_we = FractionalCascading(lists_with_empty)
    naive_we = NaiveMultiBinarySearch(lists_with_empty)
    for q in [0, 10, 12, 20, 25, 35]:
        assert fc_we.search(q) == naive_we.search(q), f"Mismatch on list with empty lists, q={q}"

    # 3c: Single list collection (k = 1)
    lists_single = [[5, 10, 15, 20]]
    fc_single = FractionalCascading(lists_single)
    naive_single = NaiveMultiBinarySearch(lists_single)
    assert fc_single.search(10) == [(1, 10)]
    assert fc_single.search(12) == [(2, 15)]
    assert fc_single.search(0) == [(0, 5)]
    assert fc_single.search(99) == [(4, None)]

    # Test Case 4: Lists with Duplicate Elements
    lists_duplicates = [
        [10, 10, 20, 20, 30],
        [5, 10, 10, 15],
        [10, 20, 20, 40]
    ]
    fc_dup = FractionalCascading(lists_duplicates)
    naive_dup = NaiveMultiBinarySearch(lists_duplicates)
    for q in [5, 10, 15, 20, 30, 35]:
        assert fc_dup.search(q) == naive_dup.search(q), f"Duplicate test mismatch for q={q}"

    # Test Case 5: Randomized Stress Testing
    import random
    random.seed(2026)
    for trial in range(50):
        k = random.randint(1, 6)
        test_lists = [
            sorted(random.sample(range(-100, 100), random.randint(0, 15)))
            for _ in range(k)
        ]
        fc_rand = FractionalCascading(test_lists)
        naive_rand = NaiveMultiBinarySearch(test_lists)

        for _ in range(20):
            target = random.randint(-120, 120)
            assert fc_rand.search(target) == naive_rand.search(target), (
                f"Random stress test failed in trial {trial} for target {target}"
            )

    # Test Case 6: Demonstrate Buggy Implementation Flaws
    buggy_fc = BuggyFractionalCascading(lists_standard)
    # The buggy implementation fails on various targets due to broken strides and forward scanning
    buggy_results = buggy_fc.search(25)
    correct_results = [res[0] for res in expected_q25]
    # We assert that the buggy version indeed exhibits flawed behavior
    is_buggy = (buggy_results != correct_results)
    assert is_buggy, "Expected BuggyFractionalCascading to produce flawed results"

    print("[+] All Fractional Cascading tests passed successfully!")


# ==============================================================================
# 6. MAIN EXECUTION & EDUCATIONAL TRACE
# ==============================================================================

def main() -> None:
    """
    Main driver running unit tests and demonstrating educational execution traces.
    """
    run_tests()

    print("\n" + "=" * 80)
    print("EDUCATIONAL TRACE: FRACTIONAL CASCADING IN ACTION")
    print("=" * 80)

    lists = [
        [24, 64, 65, 80, 93],
        [23, 25, 26],
        [13, 44, 62, 66],
        [11, 35, 46, 79, 81]
    ]

    print("Input Lists (k = 4):")
    for i, lst in enumerate(lists):
        print(f"  L_{i} (size {len(lst):>2}): {lst}")

    fc = FractionalCascading(lists)

    print("\nAugmented Lists (M_i) with Fractional Samples:")
    for i, m in enumerate(fc.augmented_lists):
        vals = [node.val for node in m]
        print(f"  M_{i} (size {len(m):>2}): {vals}")

    query = 25
    print(f"\nSearching for Target Key: {query}")
    print("-" * 80)
    print(f"{'Level':<6} | {'M_i Size':<8} | {'Pos in M_i':<10} | {'Node Val':<8} | {'Orig Idx':<8} | {'Result Val':<10} | {'Method'}")
    print("-" * 80)

    # Manual step-through for trace visualization
    m0 = fc.augmented_lists[0]
    pos = bisect.bisect_left(m0, query, key=lambda n: n.val)
    print(f"{'0':<6} | {len(m0):<8} | {pos:<10} | {m0[pos].val:<8} | {m0[pos].orig_idx:<8} | {str(lists[0][m0[pos].orig_idx]):<10} | Binary Search O(log N)")

    curr_pos = pos
    for i in range(1, fc.k):
        cand = fc.augmented_lists[i - 1][curr_pos].down_ptr
        steps = 0
        while cand > 0 and fc.augmented_lists[i][cand - 1].val >= query:
            cand -= 1
            steps += 1
        curr_pos = cand
        node = fc.augmented_lists[i][curr_pos]
        orig_val = lists[i][node.orig_idx] if node.orig_idx < len(lists[i]) else "None"
        print(f"{i:<6} | {len(fc.augmented_lists[i]):<8} | {curr_pos:<10} | {node.val:<8} | {node.orig_idx:<8} | {str(orig_val):<10} | Bridge Ptr + {steps} steps (O(1))")

    print("-" * 80)
    print(f"Result across all lists for q = {query}:")
    for i, (idx, val) in enumerate(fc.search(query)):
        print(f"  List L_{i} -> Lower-bound Index: {idx}, Value: {val}")
    print("=" * 80)


if __name__ == "__main__":
    main()
