import os

md_content = """# COMPETITIVE PROGRAMMING STRATEGY IN PYTHON

## 1. WHY THIS MATTERS (THE META-GAME)
Competitive Programming (CP) and LeetCode interviews are not about software engineering; they are about **Pattern Recognition** and **Algorithmic Complexity**.

If you memorize 500 LeetCode solutions, you will fail the interview when they ask a question you haven't seen. 
If you memorize the **15 Core Patterns** (Two Pointers, Sliding Window, Fast/Slow Pointers, Merge Intervals, Cyclic Sort, BFS, DFS, Topological Sort, Two Heaps, Subsets, Binary Search, Top 'K' Elements, K-way Merge, 0/1 Knapsack, Topological Sort), you will realize that every "new" question is just a disguise for a pattern you already know.

Python is the absolute best language for Technical Interviews because:
1. **Brevity**: You can write a Graph DFS in 5 lines of Python, whereas Java requires 20 lines of boilerplate. Less code = fewer bugs on the whiteboard.
2. **Built-in Data Structures**: Lists act as Stacks, `collections.deque` acts as a perfect $O(1)$ Queue, and `heapq` acts as a Min-Heap.
3. **Big-Integer Math**: Python handles infinitely large integers natively. No need for `long long` or `BigInteger` overflow checks!

---

## 2. LEARNING OBJECTIVES
- Master the Big-O Time and Space Complexity of Python's built-in data structures.
- Master the absolute critical Python modules (`collections`, `heapq`, `itertools`, `bisect`).
- Understand the blueprint for deconstructing an unseen algorithm problem.

---

## 3. BIG-O COMPLEXITY OF PYTHON STRUCTURES

Before writing any code, you must know the mathematical cost of your operations.

### Lists (Dynamic Arrays)
- `append(x)`: $O(1)$ amortized.
- `pop()`: $O(1)$ (removes from the end).
- `pop(0)`: **$O(N)$ (CRITICAL TRAP)**. Removing from the front of a Python List forces every subsequent element to shift left. Never use a List as a Queue!
- `insert(i, x)`: $O(N)$.
- `x in list`: $O(N)$ (Linear scan).

### Dictionaries (Hash Maps)
- Get Item `dict[key]`: $O(1)$ average.
- Set Item `dict[key] = val`: $O(1)$ average.
- `key in dict`: $O(1)$ average. (Use Sets/Dicts for fast lookups, NEVER Lists).

### Sets (Hash Sets)
- `add(x)`: $O(1)$.
- `remove(x)`: $O(1)$.
- `x in set`: $O(1)$.

### Deque (Double-Ended Queue)
- `append(x)` / `appendleft(x)`: **$O(1)$**
- `pop()` / `popleft()`: **$O(1)$**
- **Rule**: If you need a Queue (FIFO) for Breadth-First Search (BFS), you MUST use `collections.deque`.

---

## 4. THE 4 PILLARS OF PYTHON COMPETITIVE PROGRAMMING

### Pillar 1: `collections.deque` (Queues & BFS)
```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)      # O(1) Add to right
queue.appendleft(0)  # O(1) Add to left
val = queue.popleft() # O(1) Remove from left (CRITICAL FOR BFS!)
```

### Pillar 2: `collections.defaultdict` and `Counter` (Hash Maps)
```python
from collections import defaultdict, Counter

# defaultdict prevents KeyError. If the key doesn't exist, it defaults to an empty list!
adj_list = defaultdict(list)
adj_list['Node_A'].append('Node_B')

# Counter automatically tallies frequencies in O(N) time.
freq = Counter("abracadabra")
# freq = {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
```

### Pillar 3: `heapq` (Priority Queues & Top K Elements)
```python
import heapq

# Python's heapq is a MIN-HEAP by default. The smallest element is always at index 0.
min_heap = []
heapq.heappush(min_heap, 5)
heapq.heappush(min_heap, 1)
heapq.heappush(min_heap, 10)

smallest = heapq.heappop(min_heap) # Returns 1 in O(log N) time.

# TRAP: To simulate a MAX-HEAP, multiply all numbers by -1 before pushing!
max_heap = []
heapq.heappush(max_heap, -5)
largest = -heapq.heappop(max_heap)
```

### Pillar 4: `bisect` (Binary Search)
```python
import bisect

arr = [10, 20, 30, 40, 50]

# bisect_left finds the exact index where '25' should be inserted to maintain sorting.
# It runs in O(log N) time without you needing to write a custom Binary Search loop!
idx = bisect.bisect_left(arr, 25) # Returns 2
```

---

## 5. PROBLEM DECONSTRUCTION BLUEPRINT

When faced with a LeetCode problem, do not touch the keyboard. Ask yourself these questions:

1. **Is the input array SORTED?**
   - Yes -> It is almost certainly **Two Pointers** or **Binary Search**.
2. **Are you asked to find the TOP K / Kth SMALLEST / Kth LARGEST?**
   - Yes -> It is almost certainly a **Heap (Priority Queue)**.
3. **Are you asked to find all PERMUTATIONS or SUBSETS?**
   - Yes -> It is a **Backtracking (DFS)** problem.
4. **Are you dealing with Trees or Graphs?**
   - Is it finding the "Shortest Path"? -> **Breadth-First Search (BFS)** using a Queue.
   - Is it traversing every node? -> **Depth-First Search (DFS)** using recursion/Stack.
5. **Are you asked for a "Maximum Subarray" or "Longest Substring" mathematically?**
   - Yes -> It is a **Sliding Window** or **Dynamic Programming** problem.
6. **Does the problem involve Dependencies (e.g., Course A must be taken before Course B)?**
   - Yes -> It is **Topological Sort** (Graph Theory).

---

## 6. ACTIVE RECALL & INTERVIEW SCENARIOS

### Scenario 1:
**Interviewer:** "Write an algorithm to find the longest substring without repeating characters."
**Your Thought Process:** "The problem asks for the 'Longest Substring' satisfying a specific constraint. This screams **Sliding Window**. I will use two pointers (left and right) and a `set` to track seen characters. If the `right` pointer sees a duplicate, I will advance the `left` pointer until the duplicate is removed from the set. Time Complexity: $O(N)$."

### Scenario 2:
**Interviewer:** "Given a massive stream of millions of numbers, design a data structure to instantly return the Median value at any time."
**Your Thought Process:** "The median is the middle number. I need to keep the smaller half of numbers separated from the larger half. This screams **Two Heaps**. I will use a Max-Heap to store the smaller half, and a Min-Heap to store the larger half. The median will always be the root of the heaps. Insertion is $O(\log N)$, finding the median is $O(1)$!"

### Scenario 3:
**Interviewer:** "Given an unsorted array, find the pair of elements that sum to a target."
**Your Thought Process:** "If it was sorted, I would use Two Pointers. Since it is unsorted, sorting it takes $O(N \log N)$. I can do better. I will use a **Hash Map (Dictionary)**. As I iterate through the array, I will calculate `complement = target - current_num`. If the complement is in the Hash Map, I've found the pair! Time Complexity: $O(N)$, Space Complexity: $O(N)$."
"""

with open(r"d:\work\python-all\05-Competitive-Programming\01-Theory\01-CP-Strategy-Python.md", "w", encoding="utf-8") as f:
    f.write(md_content)
    
print("Successfully generated 01-CP-Strategy-Python.md")
