"""
System Design Data Structures (LRU Cache)
=========================================

Learning Objectives:
1. Learn how to combine multiple basic data structures (Hash Map + Doubly Linked List) 
   to build complex, high-performance systems.
2. Implement a Least Recently Used (LRU) Cache with O(1) operations.

Concept Explanation:
System design patterns at the code level often revolve around specialized caches, 
thread-safe structures, or optimized custom collections.
An LRU Cache evicts the least recently accessed item when full. We need O(1) time for 
both GET and PUT operations. 
A Hash Map provides O(1) access to nodes. A Doubly Linked List provides O(1) additions 
and removals from anywhere, allowing us to maintain the usage order.
"""

from typing import Dict, Optional
import unittest

class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCache:
    """Advanced implementation of LRU Cache using HashMap + Doubly Linked List."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, Node] = {} # Map key to Node
        
        # Dummy head and tail to avoid edge cases during insertion/deletion
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node) -> None:
        """Add a node right after the head (most recently used)."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # Update to most recently used
            self._remove(node)
            self._add(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add(new_node)
        
        if len(self.cache) > self.capacity:
            # Evict LRU (which is right before the tail)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

# --- Performance Analysis ---
# Time Complexity: O(1) for both get and put.
# Space Complexity: O(capacity) for the hash map and linked list nodes.
# 
# Edge Cases: Capacity 0 (if allowed, needs handling), getting keys that don't exist, 
# putting keys that already exist.

class TestLRUCache(unittest.TestCase):
    def test_lru(self):
        lru = LRUCache(2)
        lru.put(1, 1)
        lru.put(2, 2)
        self.assertEqual(lru.get(1), 1)    # 1 is now most recently used
        lru.put(3, 3)                      # Evicts key 2
        self.assertEqual(lru.get(2), -1)   # 2 is not found
        lru.put(4, 4)                      # Evicts key 1
        self.assertEqual(lru.get(1), -1)   # 1 is not found
        self.assertEqual(lru.get(3), 3)
        self.assertEqual(lru.get(4), 4)

if __name__ == '__main__':
    unittest.main()
