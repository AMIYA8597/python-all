# Implementation Strategies for Advanced Data Structures

## 1. Why This Matters
Python provides Lists, Sets, Dicts, and Tuples out of the box. But what if you need a Graph to map a social network? Or a Priority Queue to schedule Kubernetes pods? Or a Binary Search Tree to maintain sorted streaming data? You must implement these yourself using Python's primitive objects. Mastering these implementations is the absolute core of Data Structures and Algorithms (DSA) interviews.

## 2. Prerequisites
- `01-DS-Fundamentals-Python.md`
- `03-Performance-Comparison.md`
- Strong understanding of Object-Oriented Programming (Classes and References).

## 3. The Core Problem Solved
Built-in structures are generalized for average use cases. Custom data structures solve domain-specific problems optimally. For example, finding the "shortest path" on a map is impossible with a standard List, but trivial with a Graph represented as an Adjacency List. 

---

## 4. Linked Lists
A Linked List is a sequence of objects where each object points to the next.
**Why use it?** Unlike a dynamic array (List), a linked list doesn't require contiguous memory. Inserting an item in the middle is $O(1)$ (if you already have the pointer), because no elements need to be shifted.

### Implementation Strategy
We define a `Node` class that holds `data` and a reference to the `next` Node.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Building: 1 -> 2 -> 3
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
```
**Traversal Pattern:**
```python
curr = head
while curr is not None:
    print(curr.val)
    curr = curr.next
```

---

## 5. Stacks (LIFO) and Queues (FIFO)

### 5.1 Stacks (Last-In, First-Out)
Think of a stack of plates. You add to the top, you take from the top.
**Strategy:** We can safely use a standard Python `list`. `append()` adds to the top ($O(1)$), and `pop()` removes from the top ($O(1)$).

### 5.2 Queues (First-In, First-Out)
Think of a line at a grocery store. You join at the back, you leave from the front.
**Strategy:** We **CANNOT** use a Python `list`. `pop(0)` is $O(N)$ and will destroy performance. We must use `collections.deque`.

```python
from collections import deque

queue = deque()
queue.append("Alice")   # Join the back
queue.append("Bob")
first_person = queue.popleft() # Alice leaves the front in O(1)
```

---

## 6. Priority Queues (Heaps)
A Priority Queue is a queue where elements are served based on priority (e.g., lowest number first), regardless of when they arrived.
**Why use it?** Finding the minimum element in an unsorted list is $O(N)$. A Min-Heap finds the minimum in $O(1)$ and extracts it in $O(\log N)$.

### Implementation Strategy
Python provides the `heapq` module, which transforms a standard `list` into a Min-Heap binary tree array.

```python
import heapq

# Start with an empty list
heap = []

# Push items (O(log N))
heapq.heappush(heap, 10)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

# The smallest item is ALWAYS at index 0 (O(1))
print(heap[0]) # 1

# Pop the smallest item (O(log N))
smallest = heapq.heappop(heap)
```
*Note: Python only has a Min-Heap. To make a Max-Heap, multiply your numbers by `-1` before pushing, and multiply by `-1` again when popping.*

---

## 7. Binary Trees
A tree where each node has at most two children. Used for hierarchical data, expression parsing, and (when sorted) Binary Search Trees (BST).

### Implementation Strategy
Similar to a Linked List, but with two pointers (`left` and `right`).

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(15)
```
**Traversal:** Trees are traversed using recursion (DFS: Pre-order, In-order, Post-order) or a Queue (BFS: Level-order).

---

## 8. Graphs
Graphs represent networks (cities connected by roads, friends on Facebook).

### 8.1 Adjacency Matrix
A 2D array (List of Lists). `matrix[i][j] == 1` means there is an edge between node $i$ and node $j$.
- **Pros:** Checking if an edge exists is $O(1)$.
- **Cons:** Takes $O(V^2)$ memory. Terrible for sparse graphs (most real-world graphs).

### 8.2 Adjacency List (The Pythonic Standard)
A Dictionary mapping a node to a List/Set of its neighbors.
- **Pros:** Memory efficient $O(V + E)$. Easy to iterate over a node's neighbors.

```python
# Graph: A -> B, A -> C, B -> D
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": [],
    "D": []
}

# Find neighbors of A
print(graph["A"]) # ['B', 'C']
```

---

## 9. Active Recall
1. Why must you use `collections.deque` instead of a `list` for a Queue?
   **Answer:** A queue requires removing items from the front (FIFO). Doing `list.pop(0)` takes $O(N)$ time because all other elements must shift left in memory. `deque.popleft()` takes $O(1)$ time.
2. How do you implement a Max-Heap in Python since `heapq` only provides a Min-Heap?
   **Answer:** Multiply all values by `-1` when calling `heappush`, and multiply by `-1` again when retrieving them with `heappop`.
3. What is the standard way to represent a sparse Graph in Python?
   **Answer:** An Adjacency List, implemented as a Dictionary where the keys are node IDs and the values are lists of neighbor node IDs.

## 10. Interview Scenarios
**Scenario:** You need to find the $K$-th largest element in an unsorted array of 1 million numbers. Sorting takes $O(N \log N)$. Can you do better?
**Answer:** Yes, use a Min-Heap of size $K$. Iterate through the array, pushing elements into the heap. If the heap size exceeds $K$, `heappop` the smallest element. At the end, the heap contains the $K$ largest elements, and the root (`heap[0]`) is the $K$-th largest. Time complexity: $O(N \log K)$.
