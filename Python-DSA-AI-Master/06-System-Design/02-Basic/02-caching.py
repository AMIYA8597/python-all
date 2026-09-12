"""
## A. Concept Name
Caching in System Design

## B. Problem Statement
Databases are often the bottleneck in web applications due to slow disk I/O. Without caching, repeated requests for the same data waste resources and increase latency.

## C. Solution / Strategy
Caching is the technique of storing copies of frequently accessed data in a temporary, high-speed storage layer (usually RAM). This ensures future requests for that data are served significantly faster, reducing latency, database load, and improving scalability.

## D. Caching Strategies
1. Cache-Aside (Lazy Loading): The application first checks the cache. If a cache miss occurs, it queries the database, updates the cache, and returns the data.
2. Write-Through: Data is written to the cache and the database simultaneously.
3. Write-Behind (Write-Back): Data is written to the cache and asynchronously synced to the database.

## E. Eviction Policies
- LRU (Least Recently Used): Discards the least recently accessed items first.
- LFU (Least Frequently Used): Discards items accessed least often.
- TTL (Time-To-Live): Items automatically expire after a certain time.

## F. Learning Objectives
1. Understand the purpose and mechanics of a cache.
2. Implement an LRU cache from scratch using a doubly linked list and a hash map for O(1) operations.
3. Incorporate TTL (Time-To-Live) support into the cache.

## X. Project Connection
Caching is used extensively in industry for user session management, storing frequent database query results (like product catalogs), powering Content Delivery Networks (CDNs) for static assets, rate limiting, and web page fragment caching.
"""

import time
from typing import Generic, TypeVar, Dict, Optional, Any

K = TypeVar('K')
V = TypeVar('V')

# ============================================================================
# Basic Concept: Simple Dictionary Cache (Naïve)
# ============================================================================
class NaiveCache(Generic[K, V]):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[K, V] = {}
        
    def get(self, key: K) -> Optional[V]:
        return self.cache.get(key)
        
    def put(self, key: K, value: V) -> None:
        if len(self.cache) >= self.capacity and key not in self.cache:
            # Naive eviction: just remove a random key (first one from iterator)
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        self.cache[key] = value

# ============================================================================
# Professional Implementation: LRU Cache with TTL
# ============================================================================
class Node(Generic[K, V]):
    """Doubly Linked List Node for LRU Cache."""
    def __init__(self, key: K, value: V, ttl_seconds: Optional[float] = None):
        self.key = key
        self.value = value
        self.expiry_time = time.time() + ttl_seconds if ttl_seconds else float('inf')
        self.prev: Optional['Node[K, V]'] = None
        self.next: Optional['Node[K, V]'] = None

    def is_expired(self) -> bool:
        """Check if the node has expired based on its TTL."""
        return time.time() > self.expiry_time


class LRUCache(Generic[K, V]):
    """
    A professional-grade Least Recently Used (LRU) Cache with TTL support.
    Achieves O(1) time complexity for both `get` and `put` operations by combining
    a Hash Map and a Doubly Linked List.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.cache: Dict[K, Node[K, V]] = {}
        
        # Dummy head and tail to simplify edge cases during insertion and deletion
        self.head = Node(key=None, value=None)  # type: ignore
        self.tail = Node(key=None, value=None)  # type: ignore
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: Node[K, V]) -> None:
        """Remove a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_node_to_front(self, node: Node[K, V]) -> None:
        """Add a node right after the dummy head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _evict_lru(self) -> None:
        """Evict the least recently used item (the one right before the dummy tail)."""
        lru_node = self.tail.prev
        if lru_node and lru_node != self.head:
            self._remove_node(lru_node)
            del self.cache[lru_node.key]

    def _cleanup_expired(self) -> None:
        """Lazy cleanup of expired items. 
        In a production system, this could also be driven by a background thread.
        """
        # We only check lazily on access for simplicity in this implementation.
        pass

    def get(self, key: K) -> Optional[V]:
        """
        Retrieve an item from the cache.
        If found and not expired, moves it to the front and returns the value.
        If expired, removes it and returns None.
        Time Complexity: O(1)
        """
        if key not in self.cache:
            return None
        
        node = self.cache[key]
        if node.is_expired():
            self._remove_node(node)
            del self.cache[key]
            return None
            
        # Move accessed node to front (most recently used)
        self._remove_node(node)
        self._add_node_to_front(node)
        return node.value

    def put(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> None:
        """
        Add or update an item in the cache.
        If capacity is reached, evicts the least recently used item.
        Time Complexity: O(1)
        """
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            self._remove_node(node)
            node.value = value
            node.expiry_time = time.time() + ttl_seconds if ttl_seconds else float('inf')
            self._add_node_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                self._evict_lru()
            
            new_node = Node(key, value, ttl_seconds)
            self.cache[key] = new_node
            self._add_node_to_front(new_node)


# ============================================================================
# Advanced Concepts & Interview Focus
# ============================================================================
"""
Common Interview Questions:
1. How does an LRU Cache achieve O(1) time complexity?
   Answer: By using a Hash Map for O(1) key lookups to find the node, and a Doubly 
   Linked List to allow O(1) node removal and insertion (moving the accessed node to the front).

2. How would you handle a distributed cache (e.g., Redis, Memcached)?
   Answer: Instead of in-memory on a single machine, we'd use consistent hashing to 
   distribute keys across multiple cache nodes. Network latency becomes a factor.

3. What are the pitfalls of Write-Through caching?
   Answer: Every write operation involves writing to both cache and DB, increasing write 
   latency. However, read latency is extremely low and data consistency is guaranteed.

Complexity Analysis:
- Space Complexity: O(N) where N is the capacity of the cache (Hash Map + Doubly Linked List nodes).
- Time Complexity: O(1) for both `get()` and `put()` operations.

Security/Performance Considerations:
- Memory leaks: An unbounded cache will consume all memory. Always enforce a capacity limit.
- Cache Stampede (Thundering Herd): When a popular cache key expires, multiple requests might hit 
  the database simultaneously. Mitigation: Use distributed locking or probabilistic early expiration.
"""

# ============================================================================
# Tests / Example Usage
# ============================================================================
def test_lru_cache() -> None:
    print("Testing LRU Cache...")
    cache: LRUCache[str, str] = LRUCache(capacity=3)
    
    cache.put("A", "Alpha")
    cache.put("B", "Bravo")
    cache.put("C", "Charlie")
    
    # State: A, B, C (C is MRU, A is LRU)
    assert cache.get("A") == "Alpha", "A should be in cache"
    # State: B, C, A (A is MRU, B is LRU)
    
    cache.put("D", "Delta")
    # State: C, A, D (D is MRU, C is LRU, B should be evicted)
    
    assert cache.get("B") is None, "B should have been evicted"
    assert cache.get("C") == "Charlie", "C should be in cache"
    
    # TTL Test
    cache.put("E", "Echo", ttl_seconds=0.5)
    assert cache.get("E") == "Echo", "E should be in cache"
    time.sleep(0.6)
    assert cache.get("E") is None, "E should have expired"
    
    print("All LRU Cache tests passed!\\n")

if __name__ == "__main__":
    test_lru_cache()
