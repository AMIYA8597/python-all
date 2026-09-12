"""
Concurrent Data Structures in Python

# Learning Objectives
1. Understand the challenges of concurrent programming (race conditions).
2. Learn how to use locks to protect shared state.
3. Implement thread-safe data structures from scratch.
4. Utilize Python's built-in concurrent data structures (queue.Queue).

# Concept Explanation
In a multi-threaded environment, multiple threads might attempt to read and write to 
the same data structure simultaneously. If not properly synchronized, this leads to 
race conditions and data corruption. Concurrent data structures use synchronization 
primitives (like Locks, RLocks, Semaphores) to ensure thread safety.

# Industry Use Cases
- Connection pools for databases.
- Task queues in worker pools (e.g., Celery).
- In-memory caches shared across multiple request handling threads.
"""

import threading
import time
from typing import Any, Optional, Dict
from queue import Queue

# ==========================================
# 1. Unsafe Data Structure (Anti-pattern)
# ==========================================
class UnsafeCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        # Race condition: Read, Modify, Write is not atomic
        temp = self.count
        time.sleep(0.0001) # Simulate context switch
        self.count = temp + 1

# ==========================================
# 2. Thread-Safe Data Structure using Locks
# ==========================================
class ThreadSafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        # The lock ensures only one thread can execute this block at a time
        with self.lock:
            temp = self.count
            time.sleep(0.0001)
            self.count = temp + 1

    def get_count(self) -> int:
        with self.lock:
            return self.count

# ==========================================
# 3. Professional Implementation: Thread-Safe LRU Cache
# ==========================================
class ConcurrentLRUCache:
    """
    A thread-safe Least Recently Used (LRU) Cache.
    Uses a dictionary for O(1) lookups and an RLock to allow re-entrant locking if needed.
    (Note: A full LRU would use a doubly linked list, here we use Python 3.7+ dict ordering).
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[str, Any] = {}
        self.lock = threading.RLock()
        
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            # Move to end to mark as recently used
            val = self.cache.pop(key)
            self.cache[key] = val
            return val
            
    def put(self, key: str, value: Any) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
            elif len(self.cache) >= self.capacity:
                # Pop the first item (least recently used)
                # next(iter(dict)) is O(1)
                lru_key = next(iter(self.cache))
                self.cache.pop(lru_key)
            self.cache[key] = value

# ==========================================
# 4. Complexity Analysis & Built-ins
# ==========================================
"""
ConcurrentLRUCache:
- Time: O(1) for get and put, due to hash map and dict ordering properties.
- Space: O(N) where N is the capacity.
- Concurrency overhead: High contention on the single lock if heavily accessed.

# Interview Challenge
Q: How can we reduce lock contention in a highly concurrent cache?
A: Use Lock Striping (sharding). Instead of one global lock, divide the cache into 
   N segments (e.g., based on hash(key) % N), each with its own lock. This allows 
   concurrent access to different segments.

Python Built-in: `queue.Queue` is already thread-safe and perfect for producer-consumer patterns.
"""

def test_counter(counter_cls):
    counter = counter_cls()
    threads = []
    for _ in range(100):
        t = threading.Thread(target=counter.increment)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    return counter.count

if __name__ == "__main__":
    print("Running Concurrent Data Structure Tests...")
    
    # The unsafe counter will likely be < 100 due to race conditions
    unsafe_val = test_counter(UnsafeCounter)
    print(f"Unsafe Counter Result: {unsafe_val} (Expected 100, usually less)")
    
    # Thread-safe counter should always be exactly 100
    safe_val = test_counter(ThreadSafeCounter)
    assert safe_val == 100
    
    # Test Concurrent LRU Cache
    cache = ConcurrentLRUCache(2)
    cache.put("A", 1)
    cache.put("B", 2)
    assert cache.get("A") == 1
    cache.put("C", 3) # Evicts "B"
    assert cache.get("B") is None
    assert cache.get("C") == 3
    
    print("All concurrency tests passed!")
