"""
## A. Concept Name
Deque (Double-Ended Queue)

## B. One-Sentence Definition
A deque is a linear data structure that allows insertion and deletion of elements from both ends (front and rear) in O(1) time.

## C. Why Does This Exist?
Standard queues only allow operations at opposite ends (FIFO) and stacks only at one end (LIFO). Deques exist to combine these capabilities, offering maximum flexibility when we need to add or remove items from both ends of a sequence quickly.

## D. Intuition
Imagine a hybrid between a stack and a queue. If you only use one end, it behaves exactly like a stack. If you use opposite ends for inserting and removing, it behaves exactly like a queue. By allowing operations on both ends, you get both in one structure.

## E. Real-Life Analogy
Think of a line of people waiting to buy tickets where VIPs can cut to the front of the line (insert front), regular people join at the back (insert rear), people get served from the front (remove front), and people who get tired of waiting leave from the back of the line (remove rear).

## F. Mental Model
Picture a horizontal tube open at both ends. You can push balls into the left opening or the right opening, and you can pull balls out of the left opening or the right opening. 

## G. Visual Explanation
Initial:      [ ]
add_rear(1):  [1]
add_front(0): [0, 1]
add_rear(2):  [0, 1, 2]
rem_front():  [1, 2]  (returns 0)
rem_rear():   [1]     (returns 2)

## H. Formal Explanation
A double-ended queue is an abstract data type that generalizes a queue. Operations are defined for adding and removing elements from either the front or the back. It can be implemented using a doubly linked list or a dynamic array (circular buffer).

## I. Mathematical Foundation
Let D be a sequence of elements (e_1, e_2, ..., e_n).
- add_front(x): D becomes (x, e_1, ..., e_n)
- add_rear(x): D becomes (e_1, ..., e_n, x)
- remove_front(): returns e_1, D becomes (e_2, ..., e_n)
- remove_rear(): returns e_n, D becomes (e_1, ..., e_{n-1})

## J. From-Scratch Implementation
Can be done using Python lists, though adding/removing at index 0 takes O(N) time. For O(1) time, a doubly linked list or a circular array is used.

## K. Library / Production Implementation
Python provides `collections.deque`, which is implemented in C as a doubly linked list of blocks, providing O(1) time complexity for operations on both ends.

## L. Trace (walk through example)
Given `q = collections.deque([1, 2, 3])`
1. `q.appendleft(0)` -> `[0, 1, 2, 3]`
2. `q.append(4)` -> `[0, 1, 2, 3, 4]`
3. `q.popleft()` -> returns 0, `q = [1, 2, 3, 4]`
4. `q.pop()` -> returns 4, `q = [1, 2, 3]`

## M. Complexity
- Time:
  - add_front / appendleft: O(1)
  - add_rear / append: O(1)
  - remove_front / popleft: O(1)
  - remove_rear / pop: O(1)
  - index access (in `collections.deque`): O(N) in worst case
- Space: O(N) where N is number of elements.

## N. Common Mistakes
- Using a Python `list` instead of `collections.deque` for FIFO operations, resulting in O(N) pop(0) or insert(0, x) operations.
- Assuming random access `deque[i]` is O(1). In Python's deque, accessing elements in the middle is O(N).

## O. Common Confusions
- "Is it a stack or a queue?" It can be both. A deque can perfectly emulate a stack or a queue.
- Pronunciation: It is usually pronounced "deck", not "dee-queue".

## P. When To Use
- When you need fast O(1) appends and pops from both ends.
- Implementing sliding window algorithms (e.g., sliding window maximum).
- Managing undo/redo histories.
- Breadth-First Search (BFS) queues.
- Work stealing algorithms.

## Q. When NOT To Use
- When you need fast random access to elements (use a list/array).
- When you only need to add/remove from the end (a simple list is faster and more cache-friendly).

## R. Trade-offs
- Fast ends operations vs Slow middle operations (random access).
- Slightly higher memory overhead than a standard list due to linked node pointers (if implemented as a doubly linked list).

## S. Debugging
- Check if you accidentally used a standard Python list when you needed O(1) front operations.
- Remember `pop()` removes from the right, `popleft()` removes from the left.

## T. Memory Hook
"Deque = Deck of cards" – you can draw from the top or the bottom, and you can place cards on the top or the bottom.

## U. Active Recall
- What is the time complexity of `collections.deque.popleft()`?
- How does a deque differ from a standard queue?
- Why is `list.insert(0, x)` slower than `deque.appendleft(x)`?

## V. Practice
- Implement a palindrome checker using a deque.
- Given a string, remove adjacent duplicate characters.

## W. Interview Question
Sliding Window Maximum (Hard): Given an array of integers and a window size k, return the maximum element in the sliding window as it moves from left to right.
Hint: Use a deque to store indices, maintaining elements in decreasing order.

## X. Project Connection
Can be used in a web crawler to maintain the queue of URLs to visit, allowing items to be processed front-to-back while enabling prioritized items to be pushed to the front.
"""

from typing import Any, List
import collections

class ListDeque:
    """Basic Implementation using Python lists (suboptimal)."""
    def __init__(self) -> None:
        self.items: List[Any] = []

    def is_empty(self) -> bool:
        return self.items == []

    def add_front(self, item: Any) -> None:
        self.items.insert(0, item)  # O(N)

    def add_rear(self, item: Any) -> None:
        self.items.append(item)     # O(1) amortized

    def remove_front(self) -> Any:
        return self.items.pop(0)    # O(N)

    def remove_rear(self) -> Any:
        return self.items.pop()     # O(1)

    def size(self) -> int:
        return len(self.items)

class StandardDeque:
    """Intermediate Implementation using collections.deque."""
    def __init__(self) -> None:
        self.items: collections.deque = collections.deque()

    def add_front(self, item: Any) -> None:
        self.items.appendleft(item)

    def add_rear(self, item: Any) -> None:
        self.items.append(item)

    def remove_front(self) -> Any:
        return self.items.popleft()

    def remove_rear(self) -> Any:
        return self.items.pop()

def interview_challenge_sliding_window_max(nums: List[int], k: int) -> List[int]:
    """
    Interview Challenge: Sliding Window Maximum.
    Given an array of integers nums, there is a sliding window of size k which is moving from the very left
    of the array to the very right. Return the max sliding window.
    """
    if not nums: return []
    res = []
    q = collections.deque()
    for i in range(len(nums)):
        # remove indices that are out of bound
        while q and q[0] < i - k + 1:
            q.popleft()
        # remove smaller elements in k range as they are useless
        while q and nums[q[-1]] < nums[i]:
            q.pop()
        q.append(i)
        # add to result once window is formed
        if i >= k - 1:
            res.append(nums[q[0]])
    return res

def run_tests() -> None:
    print("Testing ListDeque...")
    ld = ListDeque()
    ld.add_rear(1)
    ld.add_front(0)
    ld.add_rear(2)
    assert ld.remove_front() == 0
    assert ld.remove_rear() == 2

    print("Testing StandardDeque...")
    sd = StandardDeque()
    sd.add_front(10)
    sd.add_rear(20)
    assert sd.remove_front() == 10

    print("Testing Interview Challenge...")
    assert interview_challenge_sliding_window_max([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
    assert interview_challenge_sliding_window_max([1], 1) == [1]

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
