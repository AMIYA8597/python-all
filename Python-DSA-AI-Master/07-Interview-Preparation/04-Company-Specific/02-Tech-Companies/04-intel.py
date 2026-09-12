"""
Intel Specific Interview Preparation Guide

This module covers common technical questions asked in Intel software engineering interviews.
Intel interviews often focus on low-level fundamentals, system design, hardware-software interaction,
bit manipulation, and performance optimization. Candidates are expected to write efficient code
and demonstrate a deep understanding of memory management, concurrency, and algorithmic complexity.

Beginner Explanation:
When interviewing at Intel, you will likely encounter problems that require you to manipulate data
at the bit or byte level. This reflects the nature of their work with hardware interfaces, drivers,
and embedded systems. You should also be comfortable with classical data structures and algorithms,
particularly those where space and time efficiency are paramount.

Advanced Technical Explanation:
At the system level, understanding how data is represented (e.g., endianness, two's complement) and
how CPU architectures handle memory (e.g., caching, paging, branch prediction) can set you apart.
The problems included here represent a mix of bitwise operations, cache simulations, and
algorithmic optimizations that map closely to real-world challenges faced by Intel engineers.

Topics Covered:
1. Bit Manipulation (Hamming Weight, Endianness swapping)
2. Hardware/Cache Simulation (LRU Cache)
3. Performance-oriented Array Operations
"""

from typing import List, Optional

# ==============================================================================
# Problem 1: Number of 1 Bits (Hamming Weight)
# ==============================================================================
"""
Industry Use Case:
Counting set bits is a fundamental operation in hardware diagnostics, error detection/correction codes
(like Hamming codes), and cryptography.

Description:
Write a function that takes an unsigned integer and returns the number of '1' bits it has.

Common Mistakes:
- Using a loop that iterates 32 or 64 times regardless of the number of set bits.

Performance Considerations:
- Brian Kernighan's Algorithm runs in O(k) time, where k is the number of set bits, which is more
  efficient than checking every bit.
"""

def hamming_weight(n: int) -> int:
    """
    Counts the number of set bits (1s) in the binary representation of an integer.
    
    Args:
        n (int): The non-negative integer.
        
    Returns:
        int: The number of '1' bits.
    """
    count = 0
    while n:
        # n & (n - 1) drops the lowest set bit.
        # Example: n = 12 (1100), n-1 = 11 (1011). 1100 & 1011 = 1000 (8).
        n &= n - 1
        count += 1
    return count

# ==============================================================================
# Problem 2: Swap Endianness (32-bit Integer)
# ==============================================================================
"""
Industry Use Case:
When writing network drivers or interfacing with different hardware architectures (e.g., x86 is Little-Endian,
while many network protocols are Big-Endian), developers must frequently swap the byte order of data.

Description:
Write a function to swap the endianness of a 32-bit integer.
"""

def swap_endianness_32(n: int) -> int:
    """
    Swaps the byte order of a 32-bit unsigned integer.
    
    Args:
        n (int): A 32-bit unsigned integer.
        
    Returns:
        int: The integer with its byte order reversed.
    """
    # Extract each byte using bitwise AND and shifts
    byte0 = (n & 0x000000FF) << 24
    byte1 = (n & 0x0000FF00) << 8
    byte2 = (n & 0x00FF0000) >> 8
    byte3 = (n & 0xFF000000) >> 24
    
    # Combine the bytes
    return byte0 | byte1 | byte2 | byte3

# ==============================================================================
# Problem 3: LRU (Least Recently Used) Cache
# ==============================================================================
"""
Industry Use Case:
Hardware caches (L1, L2, L3) and software caches (database query caches, web caches)
often rely on the LRU eviction policy to discard the least recently accessed items when
memory is full.

Description:
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
It should support `get` and `put` operations in O(1) average time complexity.
"""

class ListNode:
    """A doubly linked list node."""
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional['ListNode'] = None
        self.next: Optional['ListNode'] = None

class LRUCache:
    """
    LRU Cache implementation using a Hash Map and Doubly Linked List.
    The hash map provides O(1) access to nodes, while the doubly linked list
    allows O(1) removals and insertions.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Map key -> ListNode
        
        # Dummy head and tail to simplify edge cases in linked list operations
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: ListNode) -> None:
        """Removes a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_head(self, node: ListNode) -> None:
        """Adds a node right after the dummy head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        """
        Retrieves the value of the key if it exists, otherwise returns -1.
        Moves the accessed node to the head of the list.
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            self._add_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Updates the value of the key if it exists, or inserts the key-value pair.
        If the capacity is reached, evicts the least recently used item (before tail).
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict LRU (node just before tail)
                lru = self.tail.prev
                if lru:
                    self._remove_node(lru)
                    del self.cache[lru.key]
            
            new_node = ListNode(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

# ==============================================================================
# Tests
# ==============================================================================

def run_tests():
    """Executes the test suite for the Intel interview problems."""
    # Test Problem 1
    assert hamming_weight(11) == 3, "11 (1011) has 3 set bits"
    assert hamming_weight(128) == 1, "128 (10000000) has 1 set bit"
    
    # Test Problem 2
    assert swap_endianness_32(0x12345678) == 0x78563412
    assert swap_endianness_32(0xAABBCCDD) == 0xDDCCBBAA
    
    # Test Problem 3
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1       # returns 1
    lru.put(3, 3)                # evicts key 2
    assert lru.get(2) == -1      # returns -1 (not found)
    lru.put(4, 4)                # evicts key 1
    assert lru.get(1) == -1      # returns -1 (not found)
    assert lru.get(3) == 3       # returns 3
    assert lru.get(4) == 4       # returns 4
    
    print("All Intel specific tests passed successfully!")

if __name__ == "__main__":
    run_tests()
