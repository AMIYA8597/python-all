"""
## A. Concept Name
Heap (Min-Heap and Max-Heap)

## B. One-Sentence Definition
A heap is a specialized tree-based data structure that satisfies the heap property, where the parent is either greater than or equal to (max-heap) or less than or equal to (min-heap) its children.

## C. Why Does This Exist?
Heaps exist to efficiently find and extract the minimum or maximum element from a dynamically changing collection of elements in O(log n) time, which is critical for priority queues and scheduling algorithms.

## D. Intuition
Think of a hierarchy where the most important (or smallest/largest) element always bubbles up to the top. As new elements are added or the top element is removed, the structure quickly readjusts itself with minimal effort (only rearranging a single path from top to bottom or bottom to top).

## E. Real-Life Analogy
Imagine an ER waiting room (Priority Queue). Patients don't get treated in the exact order they arrive (FIFO). Instead, the doctor always treats the patient with the most severe condition first. A heap is the system keeping the most urgent patient at the very front at all times.

## F. Mental Model
A heap is visually a complete binary tree (filled left to right on every level), but it is physically stored as a flat array. To find a node's children or parent in this array, we use simple arithmetic (index * 2) rather than pointers.

## G. Visual Explanation
Array: [1, 3, 6, 5, 4]

Conceptually it forms this tree:
       1
     /   \
    3     6
   / \
  5   4

Parent(i) = (i - 1) // 2
Left(i) = 2*i + 1
Right(i) = 2*i + 2

## H. Formal Explanation
A Heap is a complete binary tree that maintains the heap invariant. In a Min-Heap, for every node $i$, the value of $i$ is $\le$ the values of its children. Because it is complete, it can be efficiently represented as an array without storing explicit pointers, reducing memory overhead and improving cache locality.

## I. Mathematical Foundation
For an element at index $i$ in a zero-indexed array:
- Parent: $\lfloor \frac{i - 1}{2} \rfloor$
- Left Child: $2i + 1$
- Right Child: $2i + 2$
The height of a heap of $n$ elements is always exactly $\lfloor \log_2 n \rfloor$ because it is a complete binary tree.

## J. From-Scratch Implementation
(See the `MinHeap` class in the code below for a full from-scratch array-based implementation).

## K. Library / Production Implementation
Python provides the `heapq` module, which implements a min-heap over a standard Python list.
Methods: `heapq.heapify(lst)`, `heapq.heappush(lst, item)`, `heapq.heappop(lst)`.

## L. Trace (walk through example)
Insert 2 into [1, 3, 6, 5, 4]:
1. Append 2 to array: [1, 3, 6, 5, 4, 2]
2. Visually, 2 is the left child of 6.
3. Heapify-Up: Compare 2 with parent 6. 2 < 6, so swap.
   Array: [1, 3, 2, 5, 4, 6]
4. Compare 2 with parent 1. 2 > 1, so stop. Heap property restored.

## M. Complexity
- Time Complexity:
  - Get Min/Max: O(1)
  - Insert: O(log n)
  - Extract Min/Max: O(log n)
  - Heapify (building from array): O(n)
- Space Complexity: O(n) for the array. O(1) auxiliary if done in-place.

## N. Common Mistakes
- Confusing the array index formulas for 0-indexed vs 1-indexed arrays.
- Assuming a heap is fully sorted. It is only partially ordered (parent < children), not a Binary Search Tree (left < parent < right).
- Using a heap when you need to frequently search for an arbitrary element (search is O(n)).

## O. Common Confusions
- "Why does `heapify` take O(n) instead of O(n log n)?" -> Most nodes are at the bottom of the tree and thus sift-down takes very few steps. The math converges to a bounded series summing to O(n).
- "Is Python's `heapq` a Max-Heap?" -> No, it's strictly a Min-Heap. To simulate a Max-Heap with numbers, you push negative values.

## P. When To Use
- Priority Queues (e.g., Dijkstra's algorithm, A* search).
- Finding the Kth largest/smallest element in a stream or large dataset.
- Scheduling systems (timers, task queues).
- Merging K sorted arrays.

## Q. When NOT To Use
- When you need fast arbitrary lookups or deletions (use a Hash Map or BST).
- When you need a fully sorted list (sorting takes O(n log n) anyway).
- When you just need to find the single minimum/maximum element ONCE (just do an O(n) scan).

## R. Trade-offs
- **Array implementation vs Node implementation**: Array uses less memory (no pointers) and has better CPU cache locality, but expanding the array might trigger an O(n) reallocation (amortized O(1)).
- **Heap vs BST**: Heap is faster and simpler for min/max operations, but BST supports in-order traversal and arbitrary searching.

## S. Debugging
- Print the array and draw it out on paper as a tree using the parent/child index rules.
- If elements aren't bubbling correctly, check if your `>` or `<` signs are flipped, or if your zero-index formulas are off by one.

## T. Memory Hook
"Heaps are a pile of laundry where the lightest (or heaviest) item magically floats to the exact top. But the rest of the pile is just loosely organized."

## U. Active Recall
- What are the array index formulas for left child, right child, and parent?
- Why is a heap a complete binary tree?
- What is the time complexity of building a heap from scratch?

## V. Practice
- Implement Max-Heap.
- Merge K Sorted Lists.
- Find K Pairs with Smallest Sums.

## W. Interview Question
"Given an integer array nums and an integer k, return the kth largest element in the array." (See `find_kth_largest` below).

## X. Project Connection
Heaps are used under the hood in Python's `asyncio` event loop to schedule timers and delayed callbacks efficiently.
"""

from typing import List, Optional
import heapq

class MinHeap:
    """Implementation of a Min-Heap using a Python list."""
    def __init__(self):
        self.heap: List[int] = []

    def parent(self, index: int) -> int:
        return (index - 1) // 2

    def left_child(self, index: int) -> int:
        return 2 * index + 1

    def right_child(self, index: int) -> int:
        return 2 * index + 2

    def insert(self, key: int) -> None:
        """Inserts a new key into the heap."""
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index: int) -> None:
        parent_index = self.parent(index)
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def extract_min(self) -> Optional[int]:
        """Removes and returns the minimum element from the heap."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index: int) -> None:
        smallest = index
        left = self.left_child(index)
        right = self.right_child(index)
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
            
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

def find_kth_largest(nums: List[int], k: int) -> int:
    # Using python's built-in heapq (which is a min-heap)
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heappushpop(min_heap, num)
            
    return min_heap[0]

def run_tests():
    print("Testing Min-Heap...")
    heap = MinHeap()
    elements = [3, 1, 6, 5, 2, 4]
    for el in elements:
        heap.insert(el)
        
    print(f"Extracted Min: {heap.extract_min()} (Expected: 1)")
    print(f"Extracted Min: {heap.extract_min()} (Expected: 2)")
    
    print("\nTesting Kth Largest Element Challenge...")
    nums = [3, 2, 1, 5, 6, 4]
    k = 2
    print(f"2nd largest in {nums}: {find_kth_largest(nums, k)} (Expected: 5)")

if __name__ == "__main__":
    run_tests()
