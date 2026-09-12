"""
## A. Concept Name
Linked List

## B. One-Sentence Definition
A linear data structure where elements are not stored in contiguous memory locations; instead, each element points to the next.

## C. Why Does This Exist?
To allow efficient insertion and deletion of elements without needing to shift other elements or allocate large contiguous blocks of memory, as required by arrays.

## D. Intuition
Imagine a treasure hunt where each clue leads you to the location of the next clue. You can't just skip to the 5th clue; you must follow them in order.

## E. Real-Life Analogy
A conga line. Each person holds the waist of the person in front of them. To add someone in the middle, they just let go, insert the new person, and hold on again.

## F. Mental Model
A chain of nodes, where each node has two compartments: one for data, and one for a reference (or pointer) to the next node in the chain.

## G. Visual Explanation
Head -> [Data|Next] -> [Data|Next] -> [Data|Next] -> None

## H. Formal Explanation
A linked list is a linear collection of data elements whose order is not given by their physical placement in memory. It consists of nodes, where each node contains data and a reference (link) to the next node. 

## I. Mathematical Foundation
Linked lists can be modeled algebraically as a recursive data type. For instance, a list L is either empty (None), or a pair (head, tail) where head is an element and tail is a list L.

## J. From-Scratch Implementation
Implemented in this module using a `Node` class and a `SinglyLinkedList` class with operations like prepend, append, and delete.

## K. Library / Production Implementation
In Python, `collections.deque` is a doubly linked list under the hood and is highly optimized for production use when fast appends/pops from both ends are needed.

## L. Trace (walk through example)
To append 'C' to A -> B -> None:
1. Create new node with 'C'.
2. Start at Head (A).
3. Follow next to B.
4. B's next is None (it's the last node).
5. Change B's next to point to 'C'.
Result: A -> B -> C -> None.

## M. Complexity
- Prepend (Insert at head): O(1)
- Append (Insert at tail): O(N) or O(1) if tail pointer is kept
- Delete/Insert at arbitrary position: O(N) search + O(1) modification
- Access: O(N)

## N. Common Mistakes
- Forgetting to handle the edge case when the list is empty (Head is None).
- Losing the reference to the rest of the list when inserting or deleting (Memory leak or truncated list).
- Forgetting to advance the current node pointer in loops, causing infinite loops.

## O. Common Confusions
- "Why use linked lists if arrays are faster to access?" Arrays offer O(1) random access but O(N) insertions/deletions. Linked lists offer fast insertions/deletions if you already have the pointer, but O(N) access.

## P. When To Use
- When you have frequent insertions and deletions.
- When you don't know the size of the data structure in advance.
- When implementing other structures like stacks, queues, or graphs (adjacency lists).

## Q. When NOT To Use
- When you need fast, random access to elements (use arrays).
- When memory is very constrained (each node requires extra memory for the pointer).

## R. Trade-offs
- Time: Fast insertions/deletions vs slow random access.
- Space: No pre-allocation needed vs extra memory for pointers.
- Cache Locality: Poor spatial locality (nodes scattered in memory) vs arrays (contiguous memory).

## S. Debugging
- Print the list as an array to visualize the current state.
- Always check what happens if the head is deleted, or if the list has 0 or 1 elements.

## T. Memory Hook
"Links in a chain" - each link connects to exactly one next link.

## U. Active Recall
- What is the time complexity of prepending a node?
- How does a node reference the next element?
- Why do linked lists have poor cache locality compared to arrays?

## V. Practice
- Implement a Doubly Linked List.
- Find the middle element of a linked list in one pass.
- Merge two sorted linked lists.

## W. Interview Question
Given the head of a linked list, determine if the linked list has a cycle in it (Floyd's Tortoise and Hare algorithm).

## X. Project Connection
Used heavily in system programming, dynamic memory allocation structures, maintaining a history of actions (undo functionality), and in the internal implementation of hash tables (chaining).
"""

from typing import Any, Optional

class Node:
    """Basic building block of a linked list."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None

class SinglyLinkedList:
    """Basic/Intermediate Implementation of Singly Linked List."""
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def is_empty(self) -> bool:
        return self.head is None

    def prepend(self, data: Any) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data: Any) -> None:
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        last = self.head
        while last.next:  # type: ignore
            last = last.next  # type: ignore
        last.next = new_node  # type: ignore

    def delete(self, key: Any) -> None:
        temp = self.head
        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                temp = None
                return

        prev = None
        while temp is not None:
            if temp.data == key:
                break
            prev = temp
            temp = temp.next

        if temp is None:
            return

        prev.next = temp.next  # type: ignore
        temp = None

    def display(self) -> list:
        elems = []
        curr = self.head
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

class AdvancedLinkedListOps(SinglyLinkedList):
    """Advanced Operations on Linked Lists."""
    def reverse(self) -> None:
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

def interview_challenge_has_cycle(head: Optional[Node]) -> bool:
    """
    Interview Challenge: Linked List Cycle.
    Given head, the head of a linked list, determine if the linked list has a cycle in it.
    """
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def run_tests() -> None:
    print("Testing SinglyLinkedList...")
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    sll.prepend(0)
    assert sll.display() == [0, 1, 2]
    sll.delete(1)
    assert sll.display() == [0, 2]

    print("Testing AdvancedLinkedListOps...")
    all_ops = AdvancedLinkedListOps()
    all_ops.append(1)
    all_ops.append(2)
    all_ops.append(3)
    all_ops.reverse()
    assert all_ops.display() == [3, 2, 1]

    print("Testing Interview Challenge...")
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node2.next = node1  # create cycle
    assert interview_challenge_has_cycle(node1) == True

    node3 = Node(3)
    assert interview_challenge_has_cycle(node3) == False

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
