"""
Module: Custom Hash Tables

## A. Concept Name
Custom Hash Table with Dynamic Resizing

## B. Learning Objectives
1. Implement a complete hash table from scratch.
2. Manage dynamic resizing and load factor.
3. Understand performance implications of resizing.

## C. Concept Explanation
A production-ready hash table needs to resize itself when the number of elements grows beyond a certain threshold (load factor). This maintains O(1) average performance. Resizing involves creating a larger array and rehashing all existing elements.

## D. Time Complexity
O(1) amortized for put. Rehashing takes O(N), but it happens infrequently. Get operations are O(1) on average.

## E. Space Complexity
O(N) where N is the number of stored elements, due to the array of buckets scaling with the number of inserted elements.

## F. Edge Cases
- Rehashing empty or very sparse tables.
- Frequent updates vs insertions.
- Handling collisions efficiently using separate chaining.

## G. Interview Challenge
Implement resizing logically and explain amortized complexity to an interviewer. Be prepared to discuss alternative collision resolution strategies (e.g., open addressing).

## H. Real-World Applications
Used in implementing caching mechanisms (LRU), symbol tables in compilers, and fast lookup structures in databases.

## I. Code Implementation
Provided below using Python classes and type hinting.

## J. Testing Strategy
Unit tests to verify capacity scaling, insertion of elements triggering resize, and correct retrieval post-resize.

## K. Best Practices
Maintain a load factor around 0.7 - 0.75 to balance memory usage and lookup speed.

## L. Common Pitfalls
Forgetting to rehash all existing elements during a resize, leading to inaccessible data.

## M. Alternatives
Trees (like AVL or Red-Black Trees) can be used for O(log N) worst-case performance without resizing pauses.

## N. Data Structure Trade-offs
Hash tables trade space overhead (empty buckets) and unpredictable resize latency for blazing fast average-case lookups.

## O. Algorithmic Patterns
Array backing with hashing and chaining (or probing).

## P. Advanced Variations
Concurrent Hash Maps with bucket-level locking or lock-free implementations.

## Q. Memory Management
Pre-allocate arrays to capacity. Monitor memory spikes during the resizing phase where both old and new buckets exist.

## R. Concurrency Considerations
Standard implementations are not thread-safe. Concurrent modifications can lead to lost updates or infinite loops during resizing.

## S. Security Implications
Hash collision attacks where malicious keys are designed to hash to the same bucket, degrading performance to O(N).

## T. Historical Context
First described in the 1950s, hash tables have become a fundamental data structure in almost all high-level programming languages.

## U. Related Data Structures
Sets, Hash Trees, Bloom Filters, Dictionaries (Python `dict`).

## V. Further Reading
Introduction to Algorithms (CLRS) chapter on Hash Tables.

## W. Practice Problems
1. Implement open addressing (linear probing).
2. Create a generic Hash Table that supports arbitrary object keys.

## X. Project Connection
This fundamental building block is essential for any larger project requiring fast, associative data retrieval, such as our AI memory cache system or in-memory key-value store.
"""

from typing import Any, List, Optional, Tuple

class CustomHashTable:
    def __init__(self, initial_capacity: int = 8, load_factor_threshold: float = 0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.threshold = load_factor_threshold
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        if self.size / self.capacity >= self.threshold:
            self._resize()

        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))
        self.size += 1

    def get(self, key: str) -> Optional[Any]:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)

# Tests
def test_custom_hash_table():
    ht = CustomHashTable(initial_capacity=2)
    ht.put("a", 1)
    ht.put("b", 2)
    ht.put("c", 3) # This will trigger a resize
    
    assert ht.capacity >= 4
    assert ht.size == 3
    assert ht.get("a") == 1
    assert ht.get("c") == 3

if __name__ == "__main__":
    test_custom_hash_table()
    print("01-custom-hash-tables.py tests passed successfully!")
