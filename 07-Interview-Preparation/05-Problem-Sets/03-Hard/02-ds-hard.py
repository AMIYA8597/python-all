"""
Hard Data Structure Problems - Interview Preparation

Learning Objectives:
1. Implement complex and composite data structures (e.g., LFU Cache, Segment Trees).
2. Understand performance trade-offs in specialized data structures.
3. Master bit manipulation techniques used in data structures (e.g., Fenwick Tree).

This module covers advanced data structures often asked in FAANG interviews.
"""

from collections import defaultdict
import heapq

# 1. Least Frequently Used (LFU) Cache
class Node:
    def __init__(self, key: int, value: int, freq: int = 1):
        self.key = key
        self.value = value
        self.freq = freq
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_tail(self) -> Node:
        if self.size == 0:
            return None
        tail_node = self.tail.prev
        self.remove_node(tail_node)
        return tail_node

class LFUCache:
    """
    Time Complexity: O(1) for both get and put operations.
    Space Complexity: O(capacity)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.key_node = {} # key -> Node
        self.freq_list = defaultdict(DoublyLinkedList) # freq -> DoublyLinkedList

    def _update_freq(self, node: Node):
        freq = node.freq
        self.freq_list[freq].remove_node(node)
        if self.min_freq == freq and self.freq_list[freq].size == 0:
            self.min_freq += 1
        
        node.freq += 1
        self.freq_list[node.freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.key_node:
            return -1
        node = self.key_node[key]
        self._update_freq(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return

        if key in self.key_node:
            node = self.key_node[key]
            node.value = value
            self._update_freq(node)
        else:
            if self.size == self.capacity:
                tail_node = self.freq_list[self.min_freq].pop_tail()
                del self.key_node[tail_node.key]
                self.size -= 1
            
            new_node = Node(key, value)
            self.key_node[key] = new_node
            self.min_freq = 1
            self.freq_list[1].add_node(new_node)
            self.size += 1

# 2. Fenwick Tree / Binary Indexed Tree
class FenwickTree:
    """
    Supports range sum queries and point updates in O(log N).
    Space Complexity: O(N)
    """
    def __init__(self, size: int):
        self.tree = [0] * (size + 1)

    def update(self, i: int, delta: int):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
        
    def range_query(self, i: int, j: int) -> int:
        return self.query(j) - self.query(i - 1)


def test_data_structures():
    print("Testing LFUCache:")
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    assert lfu.get(1) == 1
    lfu.put(3, 3)    # evicts key 2
    assert lfu.get(2) == -1
    assert lfu.get(3) == 3
    lfu.put(4, 4)    # evicts key 1
    assert lfu.get(1) == -1
    assert lfu.get(3) == 3
    assert lfu.get(4) == 4
    print("LFUCache tests passed!")

    print("\nTesting FenwickTree:")
    ft = FenwickTree(5)
    ft.update(1, 1)
    ft.update(2, 2)
    ft.update(3, 3)
    assert ft.range_query(1, 3) == 6
    assert ft.range_query(2, 3) == 5
    print("FenwickTree tests passed!")

if __name__ == "__main__":
    test_data_structures()
    print("\nAll data structure tests passed!")
