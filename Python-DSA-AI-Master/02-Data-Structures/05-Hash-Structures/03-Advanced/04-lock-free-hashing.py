"""
Module: Lock-Free Hashing

## A. Concept Name
Lock-Free Hashing

## B. Prerequisites
Understanding of hash tables, concurrent programming, and atomic operations.

## C. Learning Objectives
1. Understand the limitations of lock-based concurrent data structures.
2. Explore lock-free mechanisms using Compare-And-Swap (CAS).
3. Grasp the complexity of lock-free hash table implementations.

## D. Concept Explanation
Lock-free hashing avoids traditional locks to prevent deadlocks and reduce thread contention. It relies on atomic operations like Compare-And-Swap (CAS). In Python, true lock-free operations aren't easily exposed at the language level due to the GIL, but we can simulate the logic using threading primitives or multi-processing arrays.

## E. Real-World Analogy
Imagine a fast-food counter where instead of locking the entire counter so only one customer can be served, each customer prepares their order slip. If the spot is free when they try to place it, they place it. If someone else just placed one, they check again and retry.

## F. Python Specifics
Python's Global Interpreter Lock (GIL) limits true parallelism for CPU-bound threads. However, lock-free logic is essential for scalable applications that might circumvent the GIL using multiprocessing, C-extensions, or other parallel models.

## G. Algorithmic Steps
1. Compute the hash of the key to find the index.
2. Read the current value at the index.
3. If empty, attempt to CAS the new key into the slot.
4. If CAS fails (another thread wrote to it), retry or probe.

## H. Complexity Analysis
- Time Complexity: Expected O(1), but CAS can loop infinitely in extreme high-contention scenarios.
- Space Complexity: O(N) where N is the size of the table.

## I. Edge Cases
- The ABA problem (classic in lock-free programming).
- Memory reclamation (hazard pointers are usually required in C/C++).

## J. Common Mistakes
Assuming standard Python locks are lock-free. Using CAS without understanding contention penalties.

## K. Interview Questions
Explain the ABA problem and how it affects lock-free data structures.
How does CAS work?

## L. Performance Considerations
Lock-free algorithms can perform worse than lock-based ones under very high contention due to continuous retry loops (cache line bouncing).

## M. Best Practices
Use established lock-free libraries rather than implementing from scratch in production.

## N. Alternatives
Fine-grained locking, Read-Write locks, or Partitioned locks.

## O. Historical Context
Lock-free data structures grew in importance as multi-core processors became ubiquitous, highlighting the bottlenecks of traditional mutexes.

## P. Security Implications
Less prone to denial-of-service via deadlock, though susceptible to livelock.

## Q. Testing Strategies
Stress testing with high thread counts to expose race conditions and ABA vulnerabilities.

## R. Debugging Tips
Use logging and thread analyzers. Lock-free bugs are notorious for being difficult to reproduce.

## S. API Design
Keep the lock-free mechanics hidden behind standard interfaces like `insert`, `get`, `delete`.

## T. Code Structure
Separate the atomic primitive mocks from the higher-level data structure logic.

## U. Scalability
Highly scalable in read-heavy or low-contention environments.

## V. Maintenance
Requires deep understanding of memory models and atomic operations for maintenance.

## W. Further Reading
"The Art of Multiprocessor Programming" by Maurice Herlihy and Nir Shavit.

## X. Project Connection
Understanding lock-free hashing is critical for building high-throughput, low-latency AI pipelines and distributed caches that can't afford lock contention.
"""

import threading

class MockCAS:
    """A mocked Compare-And-Swap to illustrate lock-free logic."""
    def __init__(self, initial_value=None):
        self._val = initial_value
        self._lock = threading.Lock() # Using lock to simulate atomic hardware instruction

    def compare_and_swap(self, expected, new) -> bool:
        with self._lock:
            if self._val == expected:
                self._val = new
                return True
            return False

    def get(self):
        with self._lock:
            return self._val

class SimpleLockFreeHashTable:
    """Conceptual demonstration of lock-free insertion logic."""
    def __init__(self, size: int):
        self.table = [MockCAS() for _ in range(size)]
        self.size = size

    def _hash(self, key: int) -> int:
        return key % self.size

    def insert(self, key: int) -> bool:
        idx = self._hash(key)
        cas_cell = self.table[idx]
        
        while True:
            current = cas_cell.get()
            if current == key:
                return True # Already exists
            if current is not None:
                # Collision handling omitted for simplicity; in reality, we'd probe or chain.
                return False 
            
            if cas_cell.compare_and_swap(None, key):
                return True

# Performance Analysis:
# - Time Complexity: Expected O(1), but CAS can loop infinitely in extreme high-contention scenarios.
# - Space Complexity: O(N).

# Edge Cases:
# - The ABA problem (classic in lock-free programming).
# - Memory reclamation (hazard pointers are usually required in C++).

# Interview Challenge:
# Explain the ABA problem and how it affects lock-free data structures.

# Tests
def test_lock_free():
    lfht = SimpleLockFreeHashTable(10)
    
    def worker(val):
        lfht.insert(val)
        
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    assert lfht.table[2].get() == 2
    assert lfht.table[4].get() == 4

if __name__ == "__main__":
    test_lock_free()
    print("04-lock-free-hashing.py tests passed successfully!")
