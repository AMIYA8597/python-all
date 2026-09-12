"""
## A. Concept Name
Concurrent Dictionaries

## B. Motivation
Standard dictionaries in Python are not strictly thread-safe for complex operations. 

## C. Learning Objectives
1. Understand the problems with using standard dictionaries in multithreaded environments.
2. Implement a thread-safe concurrent dictionary using locks.
3. Understand Reader-Writer locks for optimization.

## D. Concept Explanation
Standard dictionaries in Python are not strictly thread-safe for complex operations despite the GIL. To safely access and modify a dictionary across multiple threads, we need synchronization mechanisms like Locks or RLock to prevent race conditions.

## E. Real-World Applications
Caching, shared state in multithreaded servers, and concurrent counting.

## F. Performance Analysis
- Time Complexity: O(1) for dictionary operations, but overhead is added by acquiring/releasing the lock.
- Space Complexity: O(N).
- Concurrency: Thread contention can become a bottleneck under high load.

## G. Edge Cases
- Deadlocks if not careful with nested lock acquisition (RLock helps mitigate this).
- High contention performance degradation.

## H. Interview Challenge
Implement a thread-safe LRU cache using a concurrent dictionary.

## I. Architecture & Design
Uses a coarse-grained lock (RLock) around a standard Python dictionary.

## J. Advantages
Simple to implement and guarantees thread safety for individual operations.

## K. Disadvantages
Coarse-grained locking can lead to contention and reduce throughput under heavy concurrent access.

## L. Alternative Approaches
Fine-grained locking (locking per bucket/key), lock-free data structures, or using built-in thread-safe queues.

## M. Common Pitfalls
Forgetting to lock during compound operations (e.g., read-modify-write).

## N. Best Practices
Keep the critical section (code inside the lock) as small as possible.

## O. Time Complexity
O(1) average case for get/set/delete.

## P. Space Complexity
O(N) where N is the number of keys.

## Q. Concurrency Considerations
RLock is used to allow re-entrant locks from the same thread without deadlocking.

## R. Scalability
Limited by the single lock. For high scalability, sharded dictionaries are better.

## S. Error Handling
Locking in `with` block ensures the lock is released even if an exception occurs.

## T. Testing Strategy
Use multiple threads to mutate the dictionary simultaneously and verify data integrity.

## U. Debugging Tips
Look out for race conditions in tests and ensure threads are properly joined.

## V. Related Topics
Threading, Multiprocessing, AsyncIO, Read-Write Locks.

## W. Further Reading
Python `threading` module documentation, GIL implications.

## X. Project Connection
Can be used as a shared caching layer for AI data fetching workers in the project.
"""

import threading
from typing import Any, Optional

class ConcurrentDict:
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._data.get(key)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

# Tests
def test_concurrent_dict():
    cd = ConcurrentDict()
    
    def worker(d, k, v):
        d.set(k, v)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(cd, f"key{i}", i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert cd.get("key5") == 5
    assert cd.get("key9") == 9

if __name__ == "__main__":
    test_concurrent_dict()
    print("01-concurrent-dicts.py tests passed successfully!")
