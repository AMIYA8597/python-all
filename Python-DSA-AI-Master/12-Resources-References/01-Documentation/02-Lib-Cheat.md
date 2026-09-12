# Python Standard Library Cheat Sheet for DSA & CP

This document provides a comprehensive, professional-grade guide to the most essential Python Standard Library modules used in Data Structures and Algorithms (DSA) and Competitive Programming (CP). 

## Why Use the Standard Library?
In competitive programming and technical interviews, reinventing the wheel wastes precious time. Python's standard library provides highly optimized, C-level implementations of common algorithms and data structures. Knowing these modules intimately allows you to write concise, fast, and bug-free code.

---

## 1. `collections` - High-Performance Container Datatypes

### Beginner Explanation
The `collections` module provides specialized container datatypes providing alternatives to Python’s general-purpose built-in containers, `dict`, `list`, `set`, and `tuple`.

### Deep Technical Explanation
- **`deque`**: A double-ended queue. Internally implemented as a doubly-linked list of blocks. Provides $O(1)$ time complexity for append and pop operations from both ends, unlike lists which have $O(n)$ time complexity for `pop(0)` or `insert(0)`.
- **`Counter`**: A dict subclass for counting hashable objects. It's essentially a multiset.
- **`defaultdict`**: A dict subclass that calls a factory function to supply missing values. It avoids `KeyError`.

### Cheat Sheet & Real-World Examples

```python
from collections import deque, Counter, defaultdict

# --- deque ---
q = deque([1, 2, 3])
q.append(4)       # O(1) - Adds to right
q.appendleft(0)   # O(1) - Adds to left
q.pop()           # O(1) - Removes from right
q.popleft()       # O(1) - Removes from left
# Use Case: BFS, Sliding Window Maximum

# --- Counter ---
freq = Counter("abracadabra")
print(freq['a'])  # Output: 5
print(freq.most_common(2)) # Output: [('a', 5), ('r', 2), ('b', 2)] - O(n log k)
# Use Case: Anagram checking, frequency counting

# --- defaultdict ---
adj_list = defaultdict(list)
edges = [(1, 2), (1, 3), (2, 4)]
for u, v in edges:
    adj_list[u].append(v) 
# Use Case: Graph adjacency lists, grouping items
```

### Common Mistakes & Performance
- **Mistake**: Using `list.pop(0)` for queue operations. **Fix**: Always use `deque.popleft()`.
- **Performance**: `Counter` operations like `+` and `-` are convenient but can be slow for large counts. Sometimes iterating and updating a `defaultdict(int)` is faster in tight CP loops.

---

## 2. `heapq` - Heap Queue (Priority Queue) Algorithm

### Beginner Explanation
A heap is a special tree-based data structure where the parent node is always smaller than or equal to its children (Min-Heap). `heapq` provides functions to maintain a list as a heap.

### Deep Technical Explanation
`heapq` implements a binary min-heap over a standard Python list. The relationship holds: `heap[k] <= heap[2*k+1]` and `heap[k] <= heap[2*k+2]`. Pushing and popping take $O(\log n)$ time. To implement a max-heap, multiply values by `-1` before pushing and after popping.

### Cheat Sheet & Real-World Examples

```python
import heapq

# Min-Heap
min_heap = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(min_heap)  # O(n) - Transforms list into heap in-place
smallest = heapq.heappop(min_heap)  # O(log n)
heapq.heappush(min_heap, 0)         # O(log n)

# Max-Heap (using negative values)
max_heap = [-x for x in [3, 1, 4, 1, 5, 9, 2, 6]]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)

# Getting N smallest/largest (Faster than sorting if n is small)
top_3_smallest = heapq.nsmallest(3, [3, 1, 4, 1, 5, 9, 2, 6]) # O(N log k)
top_3_largest = heapq.nlargest(3, [3, 1, 4, 1, 5, 9, 2, 6])
```
### Security / Performance Concerns
- `heapify()` is $O(n)$, whereas pushing $n$ elements individually is $O(n \log n)$. Always use `heapify()` when starting with a fully populated list.

---

## 3. `bisect` - Array Bisection Algorithm

### Beginner Explanation
`bisect` helps you find where to insert an element into a sorted list to keep it sorted. It uses binary search under the hood.

### Deep Technical Explanation
Provides $O(\log n)$ binary search operations. 
- `bisect_left(a, x)`: Returns the index of the **first** element $\ge x$.
- `bisect_right(a, x)` (or `bisect`): Returns the index **after** the last element $\le x$.

### Cheat Sheet & Real-World Examples

```python
import bisect

arr = [1, 3, 3, 3, 5, 7]

# Find insertion points
left_idx = bisect.bisect_left(arr, 3)   # Output: 1
right_idx = bisect.bisect_right(arr, 3) # Output: 4

# Insert element maintaining sorted order
bisect.insort(arr, 4) # O(N) because list insertion is O(N)
```

---

## 4. `itertools` - Functions Creating Iterators for Efficient Looping

### Deep Technical Explanation
Provides fast, memory-efficient tools for creating iterators. `permutations` and `combinations` generate elements lazily, which is crucial for preventing MemoryErrors in CP when exploring large search spaces.

### Cheat Sheet & Examples

```python
import itertools

# Combinatorics
arr = [1, 2, 3]
perms = list(itertools.permutations(arr))       # N! items
combs = list(itertools.combinations(arr, 2))    # N C 2 items

# Accumulate (Prefix Sums)
arr = [1, 2, 3, 4]
prefix_sums = list(itertools.accumulate(arr)) # [1, 3, 6, 10]
```

---

## Interview Questions & Exercises

1. **Question**: You have a stream of numbers. How would you maintain the median of the numbers efficiently?
   **Answer**: Use two heaps. A max-heap for the lower half of the numbers and a min-heap for the upper half. Balance them so their sizes differ by at most 1.
2. **Question**: Explain the difference between `defaultdict` and `dict.setdefault()`. Which is more efficient and why?
   **Answer**: `defaultdict` calls its factory function only when a key is missing. `dict.setdefault(key, func())` evaluates `func()` every time, even if the key exists, which can be a performance killer if `func()` is expensive (unless passing a literal). `defaultdict` is faster for populating graphs/frequency maps.
3. **Exercise**: Use `collections.deque` to implement a Sliding Window Maximum algorithm in $O(N)$ time.
4. **Exercise**: Given a list of intervals, use `bisect` and a custom sort to find the maximum number of non-overlapping intervals.
