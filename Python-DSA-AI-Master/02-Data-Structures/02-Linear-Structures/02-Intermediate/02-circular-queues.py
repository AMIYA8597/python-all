"""
## A. Concept Name
Circular Queue

## B. One-Sentence Definition
A circular queue is an array-based data structure where the end of the queue wraps around to the beginning, treating the array as a closed circle to reuse empty spaces.

## C. Why Does This Exist?
Standard array-based queues suffer from a "creeping" problem: when elements are dequeued, the space at the front becomes unusable unless all remaining elements are shifted (which is O(N)). Circular queues solve this by wrapping the tail pointer back to the front, reusing the empty spaces efficiently in O(1) time.

## D. Intuition
Imagine a clock face instead of a straight ruler. When the hour hand reaches 12, it doesn't fall off the clock; it wraps around to 1. Similarly, when the tail pointer reaches the end of the array, it wraps around to index 0, provided there is space.

## E. Real-Life Analogy
A revolving door or a merry-go-round. Also, buffering in streaming media (like a circular buffer), where new data constantly overwrites the oldest played data, going round and round.

## F. Mental Model
Think of an array `[ _ , _ , _ , _ ]` with two pointers: `head` (points to the first element) and `tail` (points to the last element). As you enqueue, `tail` moves forward. As you dequeue, `head` moves forward. The modulo operator `% capacity` is the magic glue that connects the end of the array back to the start.

## G. Visual Explanation
Capacity = 4.
Enqueue 1, 2, 3, 4:
[ 1 , 2 , 3 , 4 ] -> Head at 0 (value 1), Tail at 3 (value 4)
Dequeue twice:
[ _ , _ , 3 , 4 ] -> Head at 2 (value 3), Tail at 3 (value 4)
Enqueue 5 (Wraps around!):
[ 5 , _ , 3 , 4 ] -> Head at 2 (value 3), Tail at 0 (value 5)

## H. Formal Explanation
A Circular Queue is a linear data structure that operates by the First In First Out (FIFO) principle and the last position is connected back to the first position to make a circle. It is also called a "Ring Buffer". The pointers `head` and `tail` dictate the logical start and end. When `(tail + 1) % capacity == head`, the queue is full.

## I. Mathematical Foundation
The core mathematical operation is Modulo Arithmetic:
`next_index = (current_index + 1) % capacity`
This ensures that if `current_index == capacity - 1`, the `next_index` becomes `0`.

## J. From-Scratch Implementation
See `CircularQueue` and `AdvancedCircularQueue` classes below.

## K. Library / Production Implementation
In Python, `collections.deque` can be initialized with a `maxlen` argument, causing it to act like a circular queue/buffer. When the deque is full, appending an item causes the oldest item to be popped automatically.
Example: `q = collections.deque(maxlen=3)`

## L. Trace (walk through example)
1. Initialize queue of size 3. `head = -1`, `tail = -1`
2. Enqueue 'A': `head = 0`, `tail = 0`. Array: `['A', None, None]`
3. Enqueue 'B': `head = 0`, `tail = 1`. Array: `['A', 'B', None]`
4. Enqueue 'C': `head = 0`, `tail = 2`. Array: `['A', 'B', 'C']`
5. Enqueue 'D': `(2 + 1) % 3 == 0 (head)`. Return False (Full).
6. Dequeue(): Returns 'A'. `head = 1`, `tail = 2`. Array logically: `[_, 'B', 'C']`
7. Enqueue 'E': `tail = (2 + 1) % 3 = 0`. Array: `['E', 'B', 'C']`.

## M. Complexity
- Time Complexity:
  - Enqueue: O(1)
  - Dequeue: O(1)
- Space Complexity: O(N) where N is the fixed capacity of the circular queue.

## N. Common Mistakes
- Forgetting to handle the case when the queue becomes completely empty (setting both `head` and `tail` back to -1).
- Using `tail = tail + 1` instead of `tail = (tail + 1) % capacity`.
- Incorrectly determining if the queue is full. Full condition is `(tail + 1) % capacity == head`.

## O. Common Confusions
- Confusion between empty and full conditions. Empty is usually `head == -1`. Full is when the next position for tail hits the head.
- Why we initialize `head` and `tail` to -1 instead of 0. (-1 indicates that there are literally 0 elements, while 0 would indicate an element at index 0).

## P. When To Use
- Memory Management contexts where resources are limited and bounded.
- Traffic systems, CPU scheduling (Round Robin).
- Data streams / buffering (e.g., video streaming buffers, keyboard input buffers).

## Q. When NOT To Use
- When you need a queue that can grow infinitely (use a dynamic array or linked list instead).
- When you need random access to elements (use a standard array/list).

## R. Trade-offs
- Space Efficiency: Highly efficient reuse of space compared to simple array queues.
- Flexibility: Standard circular queues are fixed in size, meaning they can overflow if the peak load exceeds capacity. Resizing them (as in `AdvancedCircularQueue`) requires a full copy of the array (O(N) operation).

## S. Debugging
- Print both the array and the `head`/`tail` indices simultaneously.
- Check the state just before wrap-around (when `tail` is at the last index).
- Verify the behavior when exactly one element is enqueued and then dequeued.

## T. Memory Hook
"Modulo wraps the circle."
Any time you see the word "circular" in a data structure, immediately think of the `%` (modulo) operator.

## U. Active Recall
- What is the condition for a Circular Queue being full?
- How is the `head` pointer updated upon a dequeue?
- Why does a standard array queue waste space, and how does the circular queue fix it?

## V. Practice
1. Implement a Circular Deque (where you can insert/delete at both ends).
2. Design a system that logs the last K requests to a web server using a circular buffer.

## W. Interview Question
"Design a circular queue. After doing so, solve the 'Gas Station' (Circular Tour) problem, which conceptually relies on moving circularly through an array." (See `interview_challenge_circular_tour` below).

## X. Project Connection
In a multiplayer game server, network packets can be stored in a circular buffer. As the server processes updates (dequeue), it frees up space for incoming packets (enqueue), ensuring a strict memory limit is maintained without constant memory reallocation.
"""

from typing import Any, List

class CircularQueue:
    """Intermediate Implementation: Fixed size array-based circular queue."""
    def __init__(self, k: int):
        self.k = k
        self.queue = [None] * k
        self.head = self.tail = -1

    def enqueue(self, data: Any) -> bool:
        if ((self.tail + 1) % self.k == self.head):
            return False  # Full
        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.k
            self.queue[self.tail] = data
        return True

    def dequeue(self) -> Any:
        if (self.head == -1):
            return None  # Empty
        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.k
            return temp

    def display(self) -> List[Any]:
        if self.head == -1:
            return []
        elif self.tail >= self.head:
            return self.queue[self.head:self.tail + 1]
        else:
            return self.queue[self.head:] + self.queue[:self.tail + 1]

class AdvancedCircularQueue(CircularQueue):
    """Advanced concept: dynamically resizing circular queue."""
    def resize(self) -> None:
        old_k = self.k
        self.k = self.k * 2
        new_queue = [None] * self.k
        if self.head == -1:
            self.queue = new_queue
            return
        
        idx = 0
        curr = self.head
        while True:
            new_queue[idx] = self.queue[curr]
            idx += 1
            if curr == self.tail:
                break
            curr = (curr + 1) % old_k
            
        self.head = 0
        self.tail = idx - 1
        self.queue = new_queue

    def enqueue_dynamic(self, data: Any) -> None:
        if ((self.tail + 1) % self.k == self.head):
            self.resize()
        self.enqueue(data)


def interview_challenge_circular_tour(gas: List[int], cost: List[int]) -> int:
    """
    Interview Challenge: Gas Station / Circular Tour.
    There are n gas stations along a circular route. Return starting index if possible to travel around circuit once.
    """
    total_tank, curr_tank = 0, 0
    starting_station = 0
    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        curr_tank += gas[i] - cost[i]
        if curr_tank < 0:
            starting_station = i + 1
            curr_tank = 0
    return starting_station if total_tank >= 0 else -1

def run_tests() -> None:
    print("Testing CircularQueue...")
    cq = CircularQueue(3)
    assert cq.enqueue(1) == True
    assert cq.enqueue(2) == True
    assert cq.enqueue(3) == True
    assert cq.enqueue(4) == False # Full
    assert cq.dequeue() == 1
    assert cq.enqueue(4) == True # Wrap around
    assert cq.display() == [2, 3, 4]

    print("Testing AdvancedCircularQueue...")
    acq = AdvancedCircularQueue(2)
    acq.enqueue_dynamic(10)
    acq.enqueue_dynamic(20)
    acq.enqueue_dynamic(30) # triggers resize
    assert acq.display() == [10, 20, 30]

    print("Testing Interview Challenge...")
    assert interview_challenge_circular_tour([1,2,3,4,5], [3,4,5,1,2]) == 3
    assert interview_challenge_circular_tour([2,3,4], [3,4,3]) == -1
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
