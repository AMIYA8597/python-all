"""
## A. Concept Name
Doubly Linked List

## B. One-Sentence Definition
A sequential data structure where each node contains data and two pointers, one pointing to the next node and one pointing to the previous node.

## C. Why Does This Exist?
To overcome the limitations of singly linked lists, specifically the inability to easily traverse backward or delete a node in O(1) time if only given the node itself (without the preceding node).

## D. Intuition
Imagine a conga line where every person is holding both the shoulder of the person in front of them and the hand of the person behind them, allowing messages to be passed both forward and backward seamlessly.

## E. Real-Life Analogy
A web browser's history: you can click "Back" to go to the previous page and "Forward" to go to the next page. Each page is a node, and the "Back"/"Forward" buttons traverse the `prev` and `next` pointers.

## F. Mental Model
Think of it as a chain of blocks where each block has three compartments: [Previous Address | Data | Next Address]. The chain can be pulled from either end (Head or Tail).

## G. Visual Explanation
None <- [Prev|Data|Next] <-> [Prev|Data|Next] <-> [Prev|Data|Next] -> None
            Head                                      Tail
Each arrow represents a pointer. The first node's `prev` points to None, and the last node's `next` points to None.

## H. Formal Explanation
A doubly linked list is a linked data structure that consists of a set of sequentially linked records called nodes. Each node contains three fields: two link fields (references to the previous and to the next node in the sequence of nodes) and one data field.

## I. Mathematical Foundation
Let a DLL of size $N$ be a sequence of nodes $v_1, v_2, ..., v_n$.
For any node $v_i$ ($1 < i < n$):
- $v_i.next = v_{i+1}$
- $v_i.prev = v_{i-1}$
- $v_1.prev = None$
- $v_n.next = None$

## J. From-Scratch Implementation
(See the `DoublyLinkedList` and `DNode` classes below)

## K. Library / Production Implementation
Python's `collections.deque` is implemented internally as a doubly linked list of blocks (arrays), allowing O(1) appends and pops from both ends.

## L. Trace (walk through example)
Appending 'C' to A <-> B:
1. Create new node DNode('C').
2. Set DNode('C').prev to Tail (B).
3. Set Tail.next to DNode('C').
4. Update Tail to DNode('C').
Result: A <-> B <-> C.

## M. Complexity
- Prepend/Append: O(1) (with head and tail pointers)
- Deletion (with node reference): O(1)
- Access/Search: O(N)
- Space: O(N) (higher constant factor than singly linked list due to `prev` pointer)

## N. Common Mistakes
- Forgetting to update the `prev` pointer of the `next` node when deleting a node.
- Losing the `head` or `tail` pointer when inserting or deleting at the ends of the list.
- Not handling the edge case of an empty list or a list with a single element.

## O. Common Confusions
- "Why use DLL if it takes more memory?" Because the O(1) deletion and bidirectional traversal often outweigh the small memory overhead in complex systems like LRU caches.

## P. When To Use
- When you need bidirectional traversal.
- When you need to frequently add or remove nodes from both ends (like a deque).
- In cache algorithms like LRU Cache.

## Q. When NOT To Use
- When memory is strictly constrained (embedded systems).
- When you only need to traverse in one direction (use a singly linked list).
- When you need fast random access by index (use an array/list).

## R. Trade-offs
- Time vs Space: Faster deletions and easier traversal at the cost of O(N) extra memory for the `prev` pointers and slightly more complex update logic.

## S. Debugging
- Print the list forward and backward. If they don't match, your `prev` and `next` pointers are out of sync.
- Check edge cases: inserting into an empty list, deleting the last remaining node.

## T. Memory Hook
"Double the links, double the directions." DLL = Double pointers, Left and right traversal.

## U. Active Recall
- What are the three components of a DLL node?
- What is the time complexity of deleting a node in a DLL if you have a reference to it?
- How does inserting a node in a DLL differ from a Singly Linked List?

## V. Practice
- Implement a method to reverse a doubly linked list in-place.
- Implement a Deque using a doubly linked list.

## W. Interview Question
"Design and implement an LRU (Least Recently Used) Cache." (This requires a DLL combined with a Hash Map).

## X. Project Connection
Used in text editors for Undo/Redo functionality, navigating through playlists in a music player, and browser history management.
"""

from typing import Any, Optional

class DNode:
    """Doubly Linked List Node."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['DNode'] = None
        self.prev: Optional['DNode'] = None

class DoublyLinkedList:
    """Basic/Intermediate Implementation of Doubly Linked List."""
    def __init__(self) -> None:
        self.head: Optional[DNode] = None
        self.tail: Optional[DNode] = None

    def append(self, data: Any) -> None:
        new_node = DNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            if self.tail:
                self.tail.next = new_node
            self.tail = new_node

    def prepend(self, data: Any) -> None:
        new_node = DNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def delete_node(self, node: DNode) -> None:
        if self.head is None or node is None:
            return

        if self.head == node:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if node.prev is not None:
            node.prev.next = node.next
        if self.tail == node:
            self.tail = node.prev

    def display_forward(self) -> list:
        elems = []
        curr = self.head
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

    def display_backward(self) -> list:
        elems = []
        curr = self.tail
        while curr:
            elems.append(curr.data)
            curr = curr.prev
        return elems

class AdvancedDoublyLinkedList(DoublyLinkedList):
    """Advanced Operations on DLL."""
    def reverse(self) -> None:
        curr = self.head
        temp = None
        while curr:
            temp = curr.prev
            curr.prev = curr.next
            curr.next = temp
            curr = curr.prev
        if temp:
            self.head = temp.prev

def interview_challenge_lru_cache(capacity: int):
    """
    Interview Challenge: LRU Cache (Design).
    A standard interview question heavily relying on doubly linked lists combined with a hash map.
    (Simplified structure just to demonstrate concept).
    """
    class Node:
        def __init__(self, key, val):
            self.key, self.val = key, val
            self.prev = self.next = None

    class LRUCache:
        def __init__(self, cap: int):
            self.cap = cap
            self.cache = {}
            self.left = Node(0, 0)
            self.right = Node(0, 0)
            self.left.next, self.right.prev = self.right, self.left

        def remove(self, node):
            prev, nxt = node.prev, node.next
            prev.next, nxt.prev = nxt, prev

        def insert(self, node):
            prev, nxt = self.right.prev, self.right
            prev.next = nxt.prev = node
            node.prev, node.next = prev, nxt

        def get(self, key: int) -> int:
            if key in self.cache:
                self.remove(self.cache[key])
                self.insert(self.cache[key])
                return self.cache[key].val
            return -1

        def put(self, key: int, value: int) -> None:
            if key in self.cache:
                self.remove(self.cache[key])
            self.cache[key] = Node(key, value)
            self.insert(self.cache[key])
            if len(self.cache) > self.cap:
                lru = self.left.next
                self.remove(lru)
                del self.cache[lru.key]

    return LRUCache(capacity)


def run_tests() -> None:
    print("Testing DoublyLinkedList...")
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.prepend(0)
    assert dll.display_forward() == [0, 1, 2]
    assert dll.display_backward() == [2, 1, 0]

    dll.delete_node(dll.head.next)  # type: ignore # delete '1'
    assert dll.display_forward() == [0, 2]

    print("Testing AdvancedDoublyLinkedList...")
    adll = AdvancedDoublyLinkedList()
    adll.append(10)
    adll.append(20)
    adll.append(30)
    adll.reverse()
    assert adll.display_forward() == [30, 20, 10]

    print("Testing LRU Cache...")
    lru = interview_challenge_lru_cache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3) # evicts 2
    assert lru.get(2) == -1
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
