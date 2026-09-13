"""
Module: 01-tech-mocks
Learning Objectives:
- Understand the format of typical technical mock interviews.
- Practice fundamental data structures and algorithms commonly asked.
- Implement basic, intermediate, and advanced solutions with performance analysis.
- Understand how to structure a mock interview session.

This script simulates a technical mock interview with a classic problem: LRU Cache.
"""

from typing import Dict, Optional
import time

# --- Concept Explanation ---
# A typical technical interview involves solving an algorithmic problem.
# One of the most frequently asked design questions is implementing an LRU Cache.
# LRU (Least Recently Used) cache evicts the least recently used item when it reaches capacity.

# --- Basic / Intermediate Implementation ---
# We can implement an LRU cache using an OrderedDict in Python, but typically 
# interviewers want to see a Doubly Linked List paired with a Hash Map.

class ListNode:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional['ListNode'] = None
        self.next: Optional['ListNode'] = None

class LRUCache:
    """
    LRU Cache implementation using a Doubly Linked List and a Hash Map.
    Time Complexity: O(1) for both get and put operations.
    Space Complexity: O(capacity) for storing the elements.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, ListNode] = {}
        
        # Dummy head and tail nodes to avoid edge cases with empty list
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: ListNode):
        """Always add the new node right after head."""
        node.prev = self.head
        node.next = self.head.next
        
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: ListNode):
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _move_to_head(self, node: ListNode):
        """Move certain node in between to the head."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> ListNode:
        """Pop the current tail."""
        res = self.tail.prev
        if res and res != self.head:
            self._remove_node(res)
            return res
        return ListNode() # fallback

    def get(self, key: int) -> int:
        node = self.cache.get(key)
        if not node:
            return -1
        
        # move the accessed node to the head;
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.cache.get(key)

        if not node:
            newNode = ListNode(key, value)
            self.cache[key] = newNode
            self._add_node(newNode)

            if len(self.cache) > self.capacity:
                # pop the tail
                tail = self._pop_tail()
                if tail.key in self.cache:
                    del self.cache[tail.key]
        else:
            # update the value
            node.value = value
            self._move_to_head(node)

# --- Performance Analysis ---
# Time: O(1) for GET and PUT.
# Space: O(C) where C is the capacity.

# --- Edge Cases ---
# 1. Capacity is 0 (though normally constraints say capacity >= 1)
# 2. Putting the same key multiple times (updates value and moves to front)
# 3. Getting a non-existent key

# --- Interview Challenge ---
# Challenge: Implement an LFU (Least Frequently Used) Cache.
# Hint: Use two hash maps and a doubly linked list or a min-heap.

# --- Tests ---
def test_lru_cache():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "Test 1 failed"
    cache.put(3, 3)    # evicts key 2
    assert cache.get(2) == -1, "Test 2 failed"
    cache.put(4, 4)    # evicts key 1
    assert cache.get(1) == -1, "Test 3 failed"
    assert cache.get(3) == 3, "Test 4 failed"
    assert cache.get(4) == 4, "Test 5 failed"
    print("All tests passed!")

if __name__ == "__main__":
    test_lru_cache()
