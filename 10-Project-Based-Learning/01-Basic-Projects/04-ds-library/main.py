"""
Professional Data Structures Library - Main Execution & Testing
===============================================================

What is this?
-------------
This module serves as the primary entry point and test harness for our custom Data Structures (DS) library. 
It demonstrates the implementation and practical usage of fundamental data structures: 
Singly Linked Lists, Stacks, and Queues.

Why does it exist?
------------------
Understanding data structures under the hood is critical for any software engineer. While Python provides 
built-in types like `list` and `collections.deque` that abstract these concepts, building them from scratch 
teaches memory management (conceptually), algorithmic complexity (Big O notation), and Object-Oriented 
Programming (OOP) principles.

Industry Use Cases:
-------------------
- Stacks: Undo/Redo mechanisms, call stack management in recursive functions, parsing expressions.
- Queues: Task scheduling, message brokering (like RabbitMQ or Kafka at a high level), BFS traversal.
- Linked Lists: Dynamic memory allocation representation, foundation for complex structures like Hash Maps (chaining) or LRU caches.

Advanced Concepts Covered:
--------------------------
- Generics and Type Hinting (`typing.TypeVar`, `typing.Generic`) for type-safe collections.
- Dunder methods (`__str__`, `__len__`, `__iter__`) for Pythonic integration.
- Custom Exceptions for robust error handling.
"""

from typing import TypeVar, Generic, Optional, Iterator
from abc import ABC, abstractmethod

T = TypeVar('T')

class DSError(Exception):
    """Base class for Data Structure related errors."""
    pass

class EmptyStructureError(DSError):
    """Raised when attempting to access elements from an empty data structure."""
    pass


# -----------------------------------------------------------------------------
# 1. Singly Linked List
# -----------------------------------------------------------------------------

class Node(Generic[T]):
    """
    A single node in a linked list.
    
    Attributes:
        data (T): The value stored in the node.
        next_node (Optional[Node[T]]): Reference to the next node in the chain.
    """
    __slots__ = ['data', 'next_node']  # Memory optimization

    def __init__(self, data: T):
        self.data: T = data
        self.next_node: Optional['Node[T]'] = None

    def __str__(self) -> str:
        return str(self.data)


class LinkedList(Generic[T]):
    """
    A Singly Linked List implementation.
    
    Time Complexities:
    - Insertion at Head: O(1)
    - Insertion at Tail: O(n) (or O(1) if a tail pointer is maintained)
    - Deletion: O(n) (requires traversal to find previous node)
    - Search: O(n)
    """
    
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Returns True if the list contains no elements."""
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def append(self, data: T) -> None:
        """Appends an element to the end of the list. O(n) operation."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            # Ignore type error here as we know head is not None
            while current and current.next_node:
                current = current.next_node
            if current:
                current.next_node = new_node
        self._size += 1

    def prepend(self, data: T) -> None:
        """Inserts an element at the beginning of the list. O(1) operation."""
        new_node = Node(data)
        new_node.next_node = self.head
        self.head = new_node
        self._size += 1

    def delete(self, data: T) -> bool:
        """
        Deletes the first occurrence of data in the list.
        Returns True if successful, False if data not found. O(n) operation.
        """
        if self.is_empty():
            return False

        if self.head and self.head.data == data:
            self.head = self.head.next_node
            self._size -= 1
            return True

        current = self.head
        while current and current.next_node:
            if current.next_node.data == data:
                current.next_node = current.next_node.next_node
                self._size -= 1
                return True
            current = current.next_node
        return False

    def __iter__(self) -> Iterator[T]:
        """Allows iteration over the list in a pythonic way (e.g., `for item in list:`)."""
        current = self.head
        while current:
            yield current.data
            current = current.next_node

    def __str__(self) -> str:
        elements = [str(item) for item in self]
        return " -> ".join(elements) + (" -> None" if elements else "None")


# -----------------------------------------------------------------------------
# 2. Stack (LIFO - Last In, First Out)
# -----------------------------------------------------------------------------

class Stack(Generic[T]):
    """
    A Stack implementation using an underlying Python list.
    
    Time Complexities:
    - Push: O(1) amortized
    - Pop: O(1) amortized
    - Peek: O(1)
    """
    
    def __init__(self) -> None:
        self._items: list[T] = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def push(self, item: T) -> None:
        """Pushes an item onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Removes and returns the top item of the stack."""
        if self.is_empty():
            raise EmptyStructureError("Cannot pop from an empty Stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Returns the top item without removing it."""
        if self.is_empty():
            raise EmptyStructureError("Cannot peek into an empty Stack.")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Stack(top -> bottom): {self._items[::-1]}"


# -----------------------------------------------------------------------------
# 3. Queue (FIFO - First In, First Out)
# -----------------------------------------------------------------------------
# Note: Using a standard list for a queue is inefficient because `pop(0)` is O(n).
# In a professional setting, we wrap `collections.deque` or build one using a Linked List.
# Here, we will implement it using our custom LinkedList to demonstrate composition!

class Queue(Generic[T]):
    """
    A Queue implementation using Composition with our custom LinkedList.
    
    Time Complexities:
    - Enqueue: O(n) because our LinkedList append is O(n). 
      (Optimization exercise: Add a tail pointer to LinkedList to make this O(1)).
    - Dequeue: O(1) as we remove from the head.
    """
    
    def __init__(self) -> None:
        self._list: LinkedList[T] = LinkedList()

    def is_empty(self) -> bool:
        return self._list.is_empty()

    def enqueue(self, item: T) -> None:
        """Adds an item to the back of the queue."""
        self._list.append(item)

    def dequeue(self) -> T:
        """Removes and returns the front item of the queue."""
        if self.is_empty():
            raise EmptyStructureError("Cannot dequeue from an empty Queue.")
        
        # We know head is not None because is_empty() is False
        front_node = self._list.head
        if front_node is None:
            raise EmptyStructureError("Queue is corrupted.")
            
        data = front_node.data
        self._list.head = front_node.next_node
        self._list._size -= 1
        return data

    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        elements = [str(item) for item in self._list]
        return f"Queue(front -> back): [{', '.join(elements)}]"


# -----------------------------------------------------------------------------
# Test Harness / Main Guard
# -----------------------------------------------------------------------------

def run_tests() -> None:
    """Executes a suite of tests demonstrating the data structures."""
    print("=========================================")
    print("Testing Linked List")
    print("=========================================")
    ll = LinkedList[int]()
    ll.append(10)
    ll.append(20)
    ll.prepend(5)
    print(f"List after append/prepend: {ll}")
    assert len(ll) == 3
    
    ll.delete(10)
    print(f"List after deleting 10: {ll}")
    assert len(ll) == 2
    
    print("\n=========================================")
    print("Testing Stack")
    print("=========================================")
    stack = Stack[str]()
    stack.push("Undo 1")
    stack.push("Undo 2")
    stack.push("Undo 3")
    print(f"Stack state: {stack}")
    
    popped = stack.pop()
    print(f"Popped item: {popped}")
    assert popped == "Undo 3"
    print(f"Peek at top: {stack.peek()}")
    
    print("\n=========================================")
    print("Testing Queue")
    print("=========================================")
    queue = Queue[str]()
    queue.enqueue("Task A")
    queue.enqueue("Task B")
    queue.enqueue("Task C")
    print(f"Queue state: {queue}")
    
    completed = queue.dequeue()
    print(f"Completed task: {completed}")
    assert completed == "Task A"
    print(f"Queue after dequeue: {queue}")
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_tests()
