"""
## A. Concept Name
Y-Fast Trie

## B. One-Sentence Definition
A Y-Fast Trie is a data structure for storing integers from a bounded domain that supports exact searches, predecessor, and successor queries in O(log log M) time using O(N) space by combining an X-Fast Trie with balanced Binary Search Trees.

## C. Why Does This Exist?
It exists to overcome the O(N log M) space complexity of the X-Fast Trie, reducing it to O(N) space while maintaining the incredibly fast O(log log M) time complexity for integer searches and predecessor/successor queries.

## D. Intuition
Instead of putting every single integer into a massive bitwise trie (which wastes space), group the sorted elements into small chunks. Build a standard binary search tree for each chunk, and only put a single "representative" from each chunk into the X-Fast Trie. Finding an element is just a matter of locating the correct chunk via the X-Fast Trie, then searching that small chunk.

## E. Real-Life Analogy
Imagine a massive library with millions of books (the integers). Instead of an index card for every single book in the central catalog (X-Fast Trie), you group books into small sections (BSTs) and only put a card for the *first book of each section* into the central catalog. To find a book, you quickly locate its section using the catalog, then walk over and browse that small section.

## F. Mental Model
- **Bottom Layer**: Elements grouped into balanced BSTs (chunks of size Θ(log M)).
- **Top Layer**: An X-Fast Trie storing only the maximum element (representative) of each BST chunk.
- **Querying**: 
  1. X-Fast Trie -> O(log log M) to find the correct chunk representative.
  2. BST -> O(log log M) to search within the chunk.
  Total Time = O(log log M).

## G. Visual Explanation
```text
X-Fast Trie (Representatives only)
      [*]
     /   \
   [15]  [56]   <-- Stores 1 representative per log M elements

Balanced BSTs (All actual elements)
   / \      / \
  8  12    45  72   <-- Chunks of size O(log M)
 / \      /  \
5  10    38  56
```

## H. Formal Explanation
A Y-Fast Trie leverages indirection. It divides N elements into N / log M groups, each of size O(log M). Each group is stored in a balanced weight-balanced tree or Red-Black tree. The maximum value of each group is inserted into an X-Fast Trie. 
- Space: The X-Fast Trie stores N / log M elements, taking O((N / log M) * log M) = O(N) space. The BSTs take O(N) space. Total Space: O(N).
- Time: Querying the X-Fast Trie takes O(log log M). Searching the BST of size log M takes O(log(log M)) = O(log log M). Total Time: O(log log M).

## I. Mathematical Foundation (if applicable)
Let $M$ be the universe size (e.g., $2^{32}$).
Let $N$ be the number of elements.
Number of bits $w = \log M$.
Chunk size $c = \Theta(w) = \Theta(\log M)$.
Number of representatives $R = N / w = N / \log M$.
Space of X-Fast Trie: $O(R \cdot w) = O((N / \log M) \cdot \log M) = O(N)$.

## J. From-Scratch Implementation (if applicable)
See the `SimplifiedYFastTrie` below, which uses a standard binary search array instead of an X-Fast Trie to demonstrate the indirection pattern.

## K. Library / Production Implementation (if applicable)
Y-Fast Tries are extremely rare in standard libraries due to hidden constants. They are occasionally found in custom network router software for IP prefix matching, or specialized high-frequency trading engines.

## L. Trace (walk through example)
For predecessor(15) in the provided code:
1. The `representatives` array is searched for the smallest representative >= 15.
2. It finds representative `16` (which represents the chunk `[12, 16]`).
3. It queries the BST for that chunk to find the predecessor of `15`.
4. The BST returns `12`.

## M. Complexity
- **Time Complexity:** 
  - Search, Predecessor, Successor: $O(\log \log M)$
  - Insert, Delete: $O(\log \log M)$ amortized
- **Space Complexity:** $O(N)$, where $N$ is the number of elements.

## N. Common Mistakes
1. Assuming Y-Fast Tries are always faster than BSTs. For 32-bit integers, $w=32$, and $\log \log M \approx 5$. However, the high constant factors for hashing and indirection mean standard B-Trees or arrays are often faster for small $N$.
2. Confusing the chunk size constraint. It *must* be $\Theta(\log M)$ to balance the space of the X-Fast Trie and the search time of the BSTs.

## O. Common Confusions
- **Why not just use an X-Fast Trie?** Because an X-Fast Trie uses $O(N \log M)$ space, which is too much for large datasets. Y-Fast Trie fixes this.
- **Why $\log \log M$ and not $\log N$?** Because the structure searches over the *bits* of the numbers (universe $M$), not the number of elements $N$.

## P. When To Use
- When dealing with large sets of bounded integers (e.g., 32-bit or 64-bit).
- When exact worst-case bounds of O(log log M) are strictly required for predecessor/successor queries.

## Q. When NOT To Use
- When dealing with arbitrary strings, objects, or unbounded precision integers.
- When $N$ is small enough that a standard array or B-Tree easily fits in the CPU cache.

## R. Trade-offs
- **Pros:** Optimal $O(\log \log M)$ query time, linear $O(N)$ space.
- **Cons:** Very complex to implement dynamic perfect hashing for the X-Fast Trie; high constant factors; poor cache locality.

## S. Debugging
- Ensure the representatives correctly represent the maximum (or minimum) of their respective chunks.
- When finding a predecessor, if the key is smaller than all elements in a chunk, you must check the maximum of the *previous* chunk.

## T. Memory Hook (a short memorable principle)
"X-Fast wastes space on every element; Y-Fast chunks them up to save space."

## U. Active Recall (questions before answers)
1. What is the space complexity of a Y-Fast Trie?
2. Why does a Y-Fast Trie group elements into chunks of size $\log M$?
3. How does the Y-Fast Trie find the predecessor of an element?

## V. Practice (exercises)
1. Modify the `SimplifiedYFastTrie` to support finding the *successor* of a key.
2. Implement a split/merge mechanism for the BST chunks to support dynamic insertions.

## W. Interview Question
Explain why Y-Fast Tries are rarely used in standard software engineering despite their impressive O(log log M) theoretical bounds.

**Answer:**
1. Hidden constants: The O(log log M) time bound hides large constant factors (due to hashing, tree traversals, and indirection).
2. Complexity: Implementing X-Fast Tries and Dynamic Perfect Hashing is highly non-trivial and error-prone.
3. Cache locality: Standard B-Trees or even simple arrays often outperform Y-Fast Tries in practice due to CPU caching, as Y-Fast Tries rely heavily on scattered pointer chasing and hashing.
4. Limited Domain: They only work on bounded integers, unlike string or object trees.

## X. Project Connection
- IP Routing tables (longest prefix match and fast routing lookups).
- High-frequency algorithmic trading (order book matching on integer prices).
- Real-time systems requiring predictable, bounded query times regardless of data size.
"""

from typing import List, Optional, Tuple
import math

class TreeNode:
    """A basic Binary Search Tree node used for the bottom layer of the Y-Fast Trie."""
    def __init__(self, key: int):
        self.key = key
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class BST:
    """A simple Binary Search Tree to manage chunks in the Y-Fast Trie."""
    def __init__(self):
        self.root: Optional[TreeNode] = None
        self.min_val: float = float('inf')
        self.max_val: float = float('-inf')
        
    def insert(self, key: int):
        self.min_val = min(self.min_val, key)
        self.max_val = max(self.max_val, key)
        if not self.root:
            self.root = TreeNode(key)
            return
            
        curr = self.root
        while True:
            if key < curr.key:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = TreeNode(key)
                    break
            elif key > curr.key:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = TreeNode(key)
                    break
            else:
                break # Duplicate

    def predecessor(self, key: int) -> Optional[int]:
        """Find the greatest element <= key."""
        curr = self.root
        pred = None
        while curr:
            if curr.key <= key:
                pred = curr.key
                curr = curr.right
            else:
                curr = curr.left
        return pred

class SimplifiedYFastTrie:
    """
    A professional, simplified implementation of a Y-Fast Trie concept.
    
    Instead of a full X-Fast Trie at the top level (which is complex and requires 
    perfect hashing for optimal bounds), we use a standard binary search on the 
    representatives for demonstration purposes, alongside BSTs for the buckets.
    This demonstrates the *indirection* concept of the Y-Fast Trie.
    """
    def __init__(self, w: int):
        """
        w: Number of bits for the integers (domain [0, 2^w - 1])
        """
        self.w = w
        # Optimal chunk size is log M = w
        self.chunk_size = w
        # Representatives (in a real Y-Fast Trie, this would be an X-Fast Trie)
        self.representatives: List[int] = [] 
        # Map representative -> BST
        self.buckets = {} 

    def build_from_sorted(self, arr: List[int]):
        """Builds the structure from a sorted array in O(N) time."""
        n = len(arr)
        for i in range(0, n, self.chunk_size):
            chunk = arr[i:i + self.chunk_size]
            rep = chunk[-1] # Choose max of chunk as representative
            
            bst = BST()
            for val in chunk:
                bst.insert(val)
                
            self.representatives.append(rep)
            self.buckets[rep] = bst

    def predecessor(self, key: int) -> Optional[int]:
        """
        Finds the predecessor of a key.
        1. Find the smallest representative >= key.
        2. Search in its bucket.
        3. If not found, look at the max value of the previous bucket.
        """
        if not self.representatives:
            return None
            
        # Binary search for the right bucket (representing the X-Fast Trie query)
        left, right = 0, len(self.representatives) - 1
        bucket_idx = -1
        
        while left <= right:
            mid = (left + right) // 2
            if self.representatives[mid] >= key:
                bucket_idx = mid
                right = mid - 1
            else:
                left = mid + 1
                
        if bucket_idx == -1:
            # Key is greater than all representatives, search the last bucket
            bucket_idx = len(self.representatives) - 1
            
        rep = self.representatives[bucket_idx]
        bst = self.buckets[rep]
        
        pred = bst.predecessor(key)
        
        if pred is not None:
            return pred
        elif bucket_idx > 0:
            # If not in this bucket, it must be the max of the previous bucket
            prev_rep = self.representatives[bucket_idx - 1]
            return self.buckets[prev_rep].max_val
            
        return None

if __name__ == "__main__":
    print("Running Y-Fast Trie (Simplified) Tests...")
    
    # 32-bit integers (w=32)
    y_fast = SimplifiedYFastTrie(w=32)
    
    # Given sorted data
    data = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91, 105, 120]
    y_fast.build_from_sorted(data)
    
    # Test Predecessor
    assert y_fast.predecessor(15) == 12
    assert y_fast.predecessor(23) == 23
    assert y_fast.predecessor(1) is None
    assert y_fast.predecessor(130) == 120
    assert y_fast.predecessor(56) == 56
    
    print("All tests passed successfully!")
