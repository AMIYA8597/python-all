"""
Module: Performance Interview Questions
Learning Objectives:
1. Understand how to optimize Python code for time and space complexity.
2. Implement a Least Recently Used (LRU) Cache from scratch.
3. Understand the use of Doubly Linked Lists combined with Hash Maps for O(1) cache operations.

Concept Explanation:
Performance questions ask you to optimize an algorithm. Caching is a primary strategy.
An LRU Cache evicts the least recently used items when full.
To achieve O(1) time complexity for both get and put operations, we use a combination of a
Hash Map (for O(1) access) and a Doubly Linked List (for O(1) removal and insertion at ends).
"""

from typing import Optional, Dict

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCache:
    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.
        """
        self.capacity = capacity
        self.cache: Dict[int, Node] = {}
        
        # Dummy head and tail to simplify linked list operations
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_head(self, node: Node):
        """Add a new node right after the head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        """
        Return the value of the key if it exists, otherwise return -1.
        """
        if key in self.cache:
            node = self.cache[key]
            # Move to head since it's recently used
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Update the value of the key if it exists. Otherwise, add the key-value pair.
        If the cache exceeds capacity, remove the least recently used item.
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used (node just before tail)
                lru_node = self.tail.prev
                if lru_node and lru_node != self.head:
                    self._remove(lru_node)
                    del self.cache[lru_node.key]
            
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

def main():
    print("Initializing LRU Cache with capacity 2.")
    lru = LRUCache(2)
    
    print("Putting (1, 1)")
    lru.put(1, 1)
    
    print("Putting (2, 2)")
    lru.put(2, 2)
    
    print("Getting 1:", lru.get(1)) # returns 1, makes 1 most recently used
    
    print("Putting (3, 3) - should evict 2")
    lru.put(3, 3) # evicts key 2
    
    print("Getting 2:", lru.get(2)) # returns -1 (not found)
    
    print("Putting (4, 4) - should evict 1")
    lru.put(4, 4) # evicts key 1
    
    print("Getting 1:", lru.get(1)) # returns -1 (not found)
    print("Getting 3:", lru.get(3)) # returns 3
    print("Getting 4:", lru.get(4)) # returns 4

if __name__ == "__main__":
    main()
