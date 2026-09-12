"""
Online Greedy Algorithms

Learning Objectives:
1. Understand the difference between online and offline algorithms.
2. Implement competitive analysis concepts.
3. Solve problems like Online Bipartite Matching or Caching using greedy strategies.

Concept Explanation:
In an online algorithm, the input is revealed piece by piece, and the algorithm must make irrevocable decisions 
at each step without knowledge of future inputs. 
Greedy is a natural choice for online algorithms. For example, in online caching (like LRU), 
we greedily evict the least recently used item. In online bipartite matching, we greedily match arriving 
nodes to available neighbors.

Performance Analysis:
- Time Complexity: O(1) or O(N) per step.
- Space Complexity: O(N) to store states/caches.

Edge Cases:
- Cache size 0.
- All requests are for the same item.

Interview Challenge:
"Implement an LRU Cache and explain its greedy nature in online environments."
"""

from collections import OrderedDict
import unittest

class LRUCache_Basic:
    """Basic LRU Cache using an OrderedDict for O(1) operations."""
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache_Intermediate:
    """Intermediate LRU Cache using Doubly Linked List and Hash Map."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    def _add(self, node):
        prev = self.tail.prev
        prev.next = node
        self.tail.prev = node
        node.prev = prev
        node.next = self.tail

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self._remove(lru)
            del self.cache[lru.key]

class TestOnlineAlgo(unittest.TestCase):
    def test_basic_lru(self):
        lru = LRUCache_Basic(2)
        lru.put(1, 1)
        lru.put(2, 2)
        self.assertEqual(lru.get(1), 1)
        lru.put(3, 3) # evicts 2
        self.assertEqual(lru.get(2), -1)
        
    def test_intermediate_lru(self):
        lru = LRUCache_Intermediate(2)
        lru.put(1, 1)
        lru.put(2, 2)
        self.assertEqual(lru.get(1), 1)
        lru.put(3, 3) # evicts 2
        self.assertEqual(lru.get(2), -1)

if __name__ == "__main__":
    unittest.main()
