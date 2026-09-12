"""
## A. Concept Name
Priority Queues

## B. One-Sentence Definition
A priority queue is an abstract data type similar to a regular queue or stack, but where each element has an associated "priority" that determines its extraction order.

## C. Why Does This Exist?
To solve scheduling problems where certain tasks (like emergency room patients or critical system processes) must be handled before others, rather than strictly first-come-first-served.

## D. Intuition
Instead of forming a strict line based on arrival time, elements jump ahead in the line based on how important they are.

## E. Real-Life Analogy
An ER waiting room: patients are seen based on the severity of their condition (priority), not strictly by who arrived first. If two people have the same severity, the one who arrived first is seen first.

## F. Mental Model
Think of a VIP club line. There are regular people and VIPs. No matter how many regular people are waiting, as soon as a VIP arrives, they go to the front.

## G. Visual Explanation
Input: Insert(B, 3), Insert(C, 1), Insert(A, 2)
Queue internal state (Min-Priority):
[ (1, C), (2, A), (3, B) ]
Extract Min -> Returns C
Extract Min -> Returns A

## H. Formal Explanation
A Priority Queue is an abstract data type supporting at least two operations: insertion of an element with a priority, and extraction of the element with the highest priority (which could mean lowest numerical value, depending on convention).

## I. Mathematical Foundation
If implemented as a binary heap, it represents a complete binary tree where the parent node's priority is always greater than or equal to (or less than or equal to, for min-heaps) the priorities of its children. This enforces the heap property.

## J. From-Scratch Implementation
(See SimplePriorityQueue implementation below)

## K. Library / Production Implementation
Python's `heapq` module provides heap queue algorithm (a.k.a. priority queue) operations, specifically a min-heap implementation based on lists. (See HeapPriorityQueue implementation below)

## L. Trace (walk through example)
spq.insert(3, "Task 3") -> [(3, "Task 3")]
spq.insert(1, "Task 1") -> [(3, "Task 3"), (1, "Task 1")]
spq.extract_min() -> Searches array, finds min priority 1, removes and returns "Task 1".

## M. Complexity
- Unsorted Array: Insert O(1), Extract O(N)
- Sorted Array: Insert O(N), Extract O(1)
- Binary Heap: Insert O(log N), Extract O(log N), Peek O(1)

## N. Common Mistakes
- Confusing min-priority and max-priority (in Python, `heapq` is a min-heap, so smaller numbers pop first).
- Forgetting a tie-breaker mechanism when using tuples in `heapq` and the items themselves are not comparable.

## O. Common Confusions
- Priority Queue vs. Heap: A priority queue is an abstract data type. A heap is a specific concrete data structure often used to implement a priority queue efficiently.

## P. When To Use
- Dijkstra's Algorithm (finding shortest path)
- Huffman coding
- Process scheduling in OS
- Handling event-driven simulations

## Q. When NOT To Use
- When strict FIFO order is required (use a Queue).
- When LIFO order is required (use a Stack).
- When searching for specific elements is frequent (O(N) in a heap; use a BST or Hash Map).

## R. Trade-offs
Using a list is easy to implement but slow for either inserts or extracts. Using a heap balances the operations to O(log N), which is highly scalable for large datasets.

## S. Debugging
- Check if elements popped are actually in priority order. 
- Ensure tie-breaker counters are monotonically increasing to preserve FIFO for equal priorities.

## T. Memory Hook
"Important people first." Priority Queues = VIP line.

## U. Active Recall
- What is the time complexity of pushing to a heap-based priority queue?
- How does Python's `heapq` handle ties if the second tuple element is not comparable? (It throws an error unless handled with a tie-breaker counter).

## V. Practice
- Kth Largest Element in an Array
- Merge K Sorted Lists
- Top K Frequent Elements

## W. Interview Question
"Given a stream of numbers, how would you keep track of the median efficiently?" (Hint: use two priority queues/heaps: a max-heap and a min-heap).

## X. Project Connection
Used in AI systems for A* Pathfinding to decide which path node to explore next based on its heuristic cost priority.
"""

import heapq
from typing import Any, List, Tuple

class SimplePriorityQueue:
    """Basic Implementation using an unsorted list. O(1) insert, O(N) extract."""
    def __init__(self) -> None:
        self.queue: List[Tuple[int, Any]] = []

    def insert(self, priority: int, item: Any) -> None:
        self.queue.append((priority, item))

    def extract_min(self) -> Any:
        if not self.queue:
            raise IndexError("extract from empty queue")
        min_idx = 0
        for i in range(1, len(self.queue)):
            if self.queue[i][0] < self.queue[min_idx][0]:
                min_idx = i
        return self.queue.pop(min_idx)[1]

class HeapPriorityQueue:
    """Intermediate Implementation using Python's heapq (Min-Heap). O(log N) operations."""
    def __init__(self) -> None:
        self._queue: List[Tuple[int, int, Any]] = []
        self._index = 0  # To handle elements with the same priority

    def insert(self, priority: int, item: Any) -> None:
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def extract_min(self) -> Any:
        if not self._queue:
            raise IndexError("extract from empty queue")
        return heapq.heappop(self._queue)[-1]
        
    def peek(self) -> Any:
        if not self._queue:
            raise IndexError("peek from empty queue")
        return self._queue[0][-1]

def interview_challenge_k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Interview Challenge: K Closest Points to Origin
    Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k,
    return the k closest points to the origin (0, 0).
    Uses a max-heap of size K.
    """
    heap: List[Tuple[float, List[int]]] = []
    for x, y in points:
        dist = -(x*x + y*y)
        if len(heap) == k:
            heapq.heappushpop(heap, (dist, [x, y]))
        else:
            heapq.heappush(heap, (dist, [x, y]))
    return [point for _, point in heap]

def run_tests() -> None:
    print("Testing SimplePriorityQueue...")
    spq = SimplePriorityQueue()
    spq.insert(3, "Task 3")
    spq.insert(1, "Task 1")
    spq.insert(2, "Task 2")
    assert spq.extract_min() == "Task 1"
    
    print("Testing HeapPriorityQueue...")
    hpq = HeapPriorityQueue()
    hpq.insert(10, "A")
    hpq.insert(5, "B")
    hpq.insert(20, "C")
    assert hpq.extract_min() == "B"
    assert hpq.peek() == "A"

    print("Testing Interview Challenge...")
    res = interview_challenge_k_closest([[1,3],[-2,2]], 1)
    assert res == [[-2, 2]]
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
