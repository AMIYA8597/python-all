"""
## A. Concept Name
Queue

## B. One-Sentence Definition
A Queue is a linear data structure that follows the First-In-First-Out (FIFO) principle, where elements are added at the rear and removed from the front.

## C. Why Does This Exist?
Queues exist to manage data in a fair, sequential order, ensuring that the first task or item to arrive is the first one to be processed, similar to waiting in a line.

## D. Intuition
Think of a queue as a pipe where water enters from one end and exits from the other. You cannot bypass the items currently in the pipe.

## E. Real-Life Analogy
A line of customers waiting at a grocery store checkout. The first person to get in line is the first person to be served and leave the line.

## F. Mental Model
Imagine a horizontal tube. You push elements into the right side (rear) and pop them out of the left side (front). 

## G. Visual Explanation
```
Enqueue (Add to Rear):
[ ] -> [A] -> [A, B] -> [A, B, C]
       Front      Rear

Dequeue (Remove from Front):
[A, B, C] -> [B, C] -> [C] -> [ ]
Front        Front
```

## H. Formal Explanation
A Queue is an Abstract Data Type (ADT) defined by two primary operations: enqueue (insert an element at the rear) and dequeue (remove and return the element at the front). It operates under the FIFO (First-In-First-Out) protocol.

## I. Mathematical Foundation
Let Q be a sequence of elements (e_1, e_2, ..., e_n).
Enqueue(e_n+1) results in Q' = (e_1, e_2, ..., e_n, e_n+1).
Dequeue() returns e_1 and results in Q' = (e_2, ..., e_n).

## J. From-Scratch Implementation
A simple queue can be implemented using Python's built-in `list`, but this is inefficient for dequeue operations (`O(N)`) because all subsequent elements must shift left.

## K. Library / Production Implementation
In production, use `collections.deque` which provides `O(1)` append and pop from both ends, or `queue.Queue` for thread-safe queues.

## L. Trace (walk through example)
1. Initialize an empty queue: `[]`
2. Enqueue 10: `[10]`
3. Enqueue 20: `[10, 20]`
4. Dequeue: removes and returns `10`, leaving `[20]`
5. Enqueue 30: `[20, 30]`

## M. Complexity
- Enqueue: O(1)
- Dequeue: O(1) (with collections.deque) / O(N) (with python list)
- Peek/Front: O(1)
- Space Complexity: O(N) where N is the number of elements

## N. Common Mistakes
- Using a standard Python `list` and `pop(0)` for queues in performance-critical code, leading to O(N^2) time for N operations.
- Forgetting to handle the "queue is empty" edge case during a dequeue or peek operation.

## O. Common Confusions
- Confusing Stack (LIFO) with Queue (FIFO).
- Mixing up the "Front" (where we remove) and the "Rear" (where we add).

## P. When To Use
- Breadth-First Search (BFS) in trees and graphs.
- Task scheduling and print spooling.
- Handling asynchronous data requests (e.g., message queues).

## Q. When NOT To Use
- When you need to access the most recently added item first (use a Stack).
- When you need fast random access to elements by index (use an Array/List).

## R. Trade-offs
- `collections.deque` provides O(1) ends but O(N) for middle operations. 
- Python `list` has O(1) random access but O(N) `pop(0)`.

## S. Debugging
- Print the queue to ensure elements are ordered from front to rear as expected.
- Verify `is_empty()` logic.

## T. Memory Hook
"First come, first served!" Just like a British queue.

## U. Active Recall
- What does FIFO stand for?
- Why is `collections.deque` better than a normal list for a queue?

## V. Practice
- Implement a Queue using two Stacks.
- Design a Circular Queue.

## W. Interview Question
- Implement a thread-safe Blocking Queue.
- First Unique Character in a String (using queue/hashmap).

## X. Project Connection
- Building a web scraper that processes URLs sequentially (BFS).
- Creating a basic task scheduler or background job worker (like Celery lite).
"""

from typing import Any, List, Optional
import collections
import queue

class ListQueue:
    """Basic Implementation: Using Python list (inefficient for dequeue)."""
    def __init__(self) -> None:
        self.items: List[Any] = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def enqueue(self, item: Any) -> None:
        self.items.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.pop(0)  # O(N) time complexity

    def size(self) -> int:
        return len(self.items)

class DequeQueue:
    """Intermediate Implementation: Using collections.deque (efficient)."""
    def __init__(self) -> None:
        self.items: collections.deque = collections.deque()

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def enqueue(self, item: Any) -> None:
        self.items.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()  # O(1) time complexity

class QueueWithStacks:
    """Advanced Implementation: Implementing a queue using two stacks."""
    def __init__(self) -> None:
        self.stack1: List[Any] = []
        self.stack2: List[Any] = []

    def enqueue(self, x: Any) -> None:
        self.stack1.append(x)

    def dequeue(self) -> Any:
        self.peek()
        return self.stack2.pop()

    def peek(self) -> Any:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        if not self.stack2:
            raise IndexError("peek from empty queue")
        return self.stack2[-1]

    def empty(self) -> bool:
        return not self.stack1 and not self.stack2

def interview_challenge_first_unique_character(s: str) -> int:
    """
    Interview Challenge: First Unique Character in a String.
    Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.
    """
    counts = collections.Counter(s)
    for idx, ch in enumerate(s):
        if counts[ch] == 1:
            return idx
    return -1

def run_tests() -> None:
    print("Testing ListQueue...")
    lq = ListQueue()
    lq.enqueue(1)
    lq.enqueue(2)
    assert lq.dequeue() == 1

    print("Testing DequeQueue...")
    dq = DequeQueue()
    dq.enqueue(10)
    dq.enqueue(20)
    assert dq.dequeue() == 10

    print("Testing QueueWithStacks...")
    qs = QueueWithStacks()
    qs.enqueue(100)
    qs.enqueue(200)
    assert qs.dequeue() == 100
    assert qs.peek() == 200

    print("Testing Interview Challenge...")
    assert interview_challenge_first_unique_character("leetcode") == 0
    assert interview_challenge_first_unique_character("loveleetcode") == 2
    assert interview_challenge_first_unique_character("aabb") == -1
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
