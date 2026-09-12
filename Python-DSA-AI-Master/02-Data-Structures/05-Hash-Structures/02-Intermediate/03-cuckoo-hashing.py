"""
## A. Concept Name
Cuckoo Hashing

## B. Learning Objectives
1. Understand the Cuckoo hashing algorithm.
2. Implement multiple hash tables for conflict resolution.
3. Handle cycle detection and resizing in Cuckoo hashing.

## C. Concept Explanation
Cuckoo hashing provides worst-case O(1) time complexity for lookups. It uses two hash functions and two tables. If an inserted item experiences a collision, it evicts the existing item, which is then moved to its alternative location, potentially causing a chain of evictions.

## D. Performance Analysis
- Time Complexity: O(1) worst-case lookup. O(1) amortized insertion.
- Space Complexity: O(N).

## E. Edge Cases
- Infinite loop during eviction (handled by max_kicks counter).
- Resizing the table when loops are detected.

## F. Interview Challenge
Implement a hash table with guaranteed O(1) lookup time.

## G. Common Pitfalls
- Failing to detect eviction cycles, leading to infinite loops.
- Choosing poorly suited hash functions that increase collision rates.

## H. Real-World Applications
- High-performance network routers (for fast routing table lookups).
- Database indexing and caching where strict O(1) reads are required.

## I. Step-by-step Tracing
1. Hash key using hash1, insert into table1.
2. If collision, evict existing element, insert new key.
3. Take evicted element, hash using hash2, insert into table2.
4. If collision, evict, move back to table1 using hash1. Repeat until success or max_kicks reached.

## J. Time/Space Tradeoffs
- Higher memory overhead compared to open addressing if load factor must be kept low (< 50%) to avoid cycles, though bucketized variants improve this.

## K. Mathematical Foundations
- Modeled via random bipartite graphs. High probability of success for insertion if load factor is < 50% for 2 hash functions.

## L. Parallelism & Concurrency
- Requires careful locking of both tables or slots during an eviction chain to maintain thread safety.

## M. Language-Specific Nuances
- Python's dynamic typing and object references mean the tables store pointers, not the actual values.

## N. Security Implications
- Vulnerable to algorithmic complexity attacks if hash functions are not cryptographically secure or seeded randomly.

## O. Alternatives Comparison
- Linear Probing: Better cache locality but lookup can degrade to O(N).
- Separate Chaining: Graceful degradation under high load but uses extra memory for pointers.

## P. Testing Strategies
- Insert elements known to collide under hash1 and hash2 to test eviction logic.
- Exceed max_kicks to test failure mode.

## Q. Historical Context
- Described by Rasmus Pagh and Flemming Friche Rodler in 2001.

## R. Ethical Considerations
- Ensuring unbiased and fair access to resources when used in critical routing infrastructure.

## S. Scaling & Distribution
- Can be expanded to d-ary cuckoo hashing (d hash functions) to achieve >90% load factors.

## T. Debugging Tips
- Trace the evicted keys and their computed hash indices to detect exactly when a cycle forms.

## U. Code Readability
- Modularize hash functions and eviction logic for clarity.

## V. Advanced Extensions
- Storing multiple items per bucket (Bucketized Cuckoo Hashing).
- Cuckoo filters for set membership (alternative to Bloom filters).

## W. Performance Benchmarking
- Measure 99th percentile latency of insertions under high load compared to average latency.

## X. Project Connection
Can be integrated into the Python-DSA-AI-Master project as the high-performance caching layer requiring strict O(1) read latency.
"""

from typing import Any, Optional

class CuckooHashing:
    def __init__(self, capacity: int = 11):
        self.capacity = capacity
        self.table1 = [None] * capacity
        self.table2 = [None] * capacity
        self.max_kicks = capacity # Simple cycle detection mechanism

    def _hash1(self, key: int) -> int:
        return key % self.capacity

    def _hash2(self, key: int) -> int:
        return (key // self.capacity) % self.capacity

    def insert(self, key: int) -> bool:
        if self.lookup(key):
            return True
        
        curr_key = key
        for _ in range(self.max_kicks):
            idx1 = self._hash1(curr_key)
            if self.table1[idx1] is None:
                self.table1[idx1] = curr_key
                return True
            
            # Evict from table1
            curr_key, self.table1[idx1] = self.table1[idx1], curr_key
            
            idx2 = self._hash2(curr_key)
            if self.table2[idx2] is None:
                self.table2[idx2] = curr_key
                return True
            
            # Evict from table2
            curr_key, self.table2[idx2] = self.table2[idx2], curr_key
            
        # Rehash required, but returning False for simplicity here
        return False

    def lookup(self, key: int) -> bool:
        if self.table1[self._hash1(key)] == key:
            return True
        if self.table2[self._hash2(key)] == key:
            return True
        return False

# Tests
def test_cuckoo_hashing():
    ch = CuckooHashing()
    assert ch.insert(10) is True
    assert ch.insert(21) is True # Collides with 10 on hash1 if capacity is 11
    
    assert ch.lookup(10) is True
    assert ch.lookup(21) is True
    assert ch.lookup(15) is False

if __name__ == "__main__":
    test_cuckoo_hashing()
    print("03-cuckoo-hashing.py tests passed successfully!")
