"""
# Cache Optimized Structures

## A. Concept Name
Modern CPUs use caches (L1, L2, L3) to speed up memory access. Data is fetched in chunks (cache lines).
Structures that store elements contiguously (like Arrays) exhibit high Spatial Locality, leading to fewer cache misses.
Structures that scatter elements in memory (like Linked Lists) cause frequent cache misses.
An Unrolled Linked List combines the advantages of both: it's a linked list of small arrays, providing better cache performance than standard linked lists while retaining fast insertions/deletions.

## B. Real-world Analogy
Think of memory as a massive library. A standard Linked List is like a treasure hunt where every clue points to a random book across the library. Every step requires a long walk (cache miss).
An Array is like a single continuous bookshelf. You walk there once and read everything in order (cache hit).
An Unrolled Linked List is like having several small bookshelves scattered around. You read a chunk of books at a time before moving to the next shelf, balancing flexibility and reading speed.

## C. Time & Space Complexity
- Time Complexity: O(N/B) traversal where B is array block size. Significant reduction in cache misses. Insertion is O(1) amortized if adding at the end, up to O(B) for mid-block insertions.
- Space Complexity: O(N) overall. Slightly less overhead than standard linked lists because fewer pointers are stored per element, though there is some wasted space in partially filled blocks.

## D. Core Implementation
The core concept is implemented via `NodeBlock` which stores a fixed-capacity array and a pointer to the next block, and `UnrolledLinkedList` which manages the blocks.

## E. Common Pitfalls & Edge Cases
- Block size selection: Choosing a block size that is too small behaves like a standard linked list; choosing one too large behaves like a dynamic array and suffers on insertions/deletions.
- Mid-block operations: Inserting or deleting elements in the middle of a block requires shifting elements within that block, which can be slightly expensive.

## F. Advanced Patterns
- Cache-oblivious algorithms: Algorithms designed to take advantage of a CPU cache without having the cache size as an explicit parameter (e.g., van Emde Boas trees).
- Flattening nested iterators: Processing structured data efficiently by flattening it into linear formats that iterate with better cache locality.

## X. Project Connection
Cache-optimized structures are critical in high-performance computing, real-time gaming engines, and database systems where memory access patterns dominate execution time. When designing database indexes or building custom memory allocators in Python (using structures like arrays or memoryviews), understanding spatial locality allows you to maximize throughput and minimize latency.
"""

import array
from typing import Any, List, Optional

class NodeBlock:
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.num_elements = 0
        self.elements = [None] * capacity
        self.next: Optional['NodeBlock'] = None

class UnrolledLinkedList:
    """Advanced Implementation: Cache Optimized Unrolled Linked List."""
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.head = NodeBlock(capacity)

    def insert(self, item: Any) -> None:
        curr = self.head
        while curr.next and curr.num_elements == self.capacity:
            curr = curr.next

        if curr.num_elements < self.capacity:
            curr.elements[curr.num_elements] = item
            curr.num_elements += 1
        else:
            new_node = NodeBlock(self.capacity)
            new_node.elements[0] = item
            new_node.num_elements += 1
            curr.next = new_node

    def display(self) -> List[Any]:
        res = []
        curr = self.head
        while curr:
            for i in range(curr.num_elements):
                res.append(curr.elements[i])
            curr = curr.next  # type: ignore
        return res

def interview_challenge_flatten_nested_iterator():
    """
    Interview Challenge: Flatten Nested List Iterator.
    Often testing cache/memory awareness and recursive unwrapping.
    (Simplified structural concept).
    """
    class NestedIterator:
        def __init__(self, nestedList: List[Any]):
            self.res = []
            self.index = 0
            self._flatten(nestedList)
            
        def _flatten(self, nested: List[Any]):
            for item in nested:
                if isinstance(item, int):
                    self.res.append(item)
                else:
                    self._flatten(item)
                    
        def next(self) -> int:
            val = self.res[self.index]
            self.index += 1
            return val
            
        def hasNext(self) -> bool:
            return self.index < len(self.res)

    return NestedIterator([[1,1],2,[1,1]])


def run_tests() -> None:
    print("Testing UnrolledLinkedList...")
    ull = UnrolledLinkedList(3)
    for i in range(1, 9):
        ull.insert(i)
    assert ull.display() == [1, 2, 3, 4, 5, 6, 7, 8]
    assert ull.head.num_elements == 3
    assert ull.head.next.num_elements == 3 # type: ignore
    assert ull.head.next.next.num_elements == 2 # type: ignore

    print("Testing Interview Challenge...")
    iterator = interview_challenge_flatten_nested_iterator()
    res = []
    while iterator.hasNext():
        res.append(iterator.next())
    assert res == [1, 1, 2, 1, 1]
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
