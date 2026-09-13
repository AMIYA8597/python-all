import os

def generate_markdown():
    content = """# Algorithm Analysis in Python: The Definitive Guide

## 1. Why This Matters

When writing software, there are usually dozens of ways to solve the same problem. 
How do you know which solution is the "best"? 

In computer science, "best" is defined by two physical constraints:
1. **Time:** How long does the CPU take to process the algorithm?
2. **Space:** How much RAM does the algorithm consume while running?

If you write an algorithm to sort 10 items, it doesn't matter if it takes 1 millisecond or 5 milliseconds. But what if the dataset scales to 1 Billion items? A badly designed algorithm might take **400 years** to finish, while a well-designed algorithm could finish in **2 seconds** on the exact same hardware.

Understanding **Asymptotic Analysis (Big-O Notation)** is the difference between writing code that collapses under load and writing code that scales to billions of users.

---

## 2. The Big-O Notation: Time Complexity

Big-O notation describes the **Upper Bound** (worst-case scenario) of an algorithm's growth rate as the input size ($N$) approaches infinity. We completely ignore constants and smaller terms because, at massive scales, only the highest order term matters.

For example, if an algorithm takes $3N^2 + 5N + 100$ operations:
- At $N = 1,000,000$, the $N^2$ term is $1,000,000,000,000$.
- The $5N + 100$ term is completely irrelevant.
- We drop the constant $3$.
- The Time Complexity is simply **$O(N^2)$**.

### The Big-O Hierarchy (From Fastest to Slowest)

1. **$O(1)$ - Constant Time**
   - The algorithm takes the exact same number of steps regardless of input size.
   - **Example:** Looking up a value in a Python `dict` by its key. Popping the last element from a `list`.

2. **$O(\\log N)$ - Logarithmic Time**
   - The dataset is halved at every step. Extremely fast. Even for $N = 1$ Billion, it takes ~30 steps.
   - **Example:** Binary Search in a sorted array. Searching in a Balanced Binary Search Tree (AVL/Red-Black).

3. **$O(N)$ - Linear Time**
   - The time grows directly in proportion to the input.
   - **Example:** Iterating through a Python `list` using a `for` loop. Searching for an item in an unsorted array.

4. **$O(N \\log N)$ - Linearithmic Time**
   - The standard time for highly optimized sorting algorithms.
   - **Example:** Python's built-in `list.sort()` (Timsort), Merge Sort, Heap Sort.

5. **$O(N^2)$ - Quadratic Time**
   - Usually involves nested loops (a loop inside a loop). It collapses on large datasets.
   - **Example:** Bubble Sort, Insertion Sort, comparing every element in an array to every other element.

6. **$O(2^N)$ - Exponential Time**
   - The time doubles with every single additional item. Mathematically impossible to compute for $N > 50$.
   - **Example:** Naive recursive calculation of the Fibonacci sequence. The Traveling Salesperson Problem (without DP).

7. **$O(N!)$ - Factorial Time**
   - The slowest known complexity.
   - **Example:** Generating all possible permutations of a string.

---

## 3. Beyond Big-O: Omega and Theta

Big-O is the most famous, but it only describes the **Worst-Case** scenario (Upper Bound).
Computer Scientists use three Greek letters to describe algorithms completely:

### Big-O ($O$) - The Upper Bound (Worst Case)
- "The algorithm will take no longer than this."
- If you use Linear Search to find an item in an array, the worst case is that the item is at the very end. The time is $O(N)$.

### Big-Omega ($\\Omega$) - The Lower Bound (Best Case)
- "The algorithm will take at least this long."
- If you use Linear Search, the best case is that the item is the very first one you check! The time is $\\Omega(1)$.

### Big-Theta ($\\Theta$) - The Tight Bound (Exact Average Case)
- "The algorithm scales exactly like this on average."
- If you use Linear Search and look for a random item, on average, you will search half the array ($N/2$). Dropping the constant, the average time is $\\Theta(N)$.

> [!NOTE]
> In industry interviews, when someone asks for the "Big-O", they are almost always asking for the **Worst-Case** scenario, unless they specify otherwise.

---

## 4. Space Complexity and Auxiliary Space

Time is only half the battle. **Space Complexity** measures how much memory (RAM) the algorithm requires as the input grows.

- **$O(1)$ Space (In-Place):** The algorithm uses a fixed amount of memory (a few variables) regardless of the input size. Example: Bubble Sort.
- **$O(N)$ Space:** The algorithm creates a new copy of the data, or uses recursion that fills the call stack linearly. Example: Merge Sort.

> [!WARNING]
> **Auxiliary Space vs. Total Space**
> "Total Space" includes the memory taken by the input array itself. "Auxiliary Space" is the EXTRA memory the algorithm requests. When analyzing algorithms, we care about Auxiliary Space.

---

## 5. Amortized Analysis in Python

Sometimes, an operation is usually $O(1)$, but occasionally takes $O(N)$. How do we classify it? We use **Amortized Analysis**.

### The Python `list.append()`
A Python list is a dynamic array. Under the hood, it allocates a fixed block of memory (e.g., space for 4 items).
- `.append()` item 1: $O(1)$
- `.append()` item 2: $O(1)$
- `.append()` item 3: $O(1)$
- `.append()` item 4: $O(1)$

Now the array is full. What happens when we `.append()` item 5?
Python must allocate a brand new block of memory that is twice as large (8 slots). It then copies all 4 existing items to the new block. This resizing operation takes **$O(N)$ time**.

However, because the array doubles in size, the expensive $O(N)$ resize happens so rarely that if you average the cost across thousands of appends, the cost approaches $O(1)$. Therefore, we say `list.append()` is **Amortized $O(1)$**.

---

## 6. The Master Theorem

When analyzing recursive algorithms (like Divide and Conquer), the time complexity isn't obvious. You must solve the recurrence relation.

The recurrence is usually written as:
$$ T(N) = aT(N/b) + O(N^d) $$
- **$a$**: Number of recursive calls (branches).
- **$b$**: How much the input shrinks at every step.
- **$O(N^d)$**: The work done outside the recursion (e.g., merging arrays).

### The Master Theorem Rules:
1. If $a > b^d$, the recursion tree dominates the work. Time is **$O(N^{\\log_b a})$**.
2. If $a = b^d$, the work is perfectly balanced across all levels. Time is **$O(N^d \\log N)$**.
3. If $a < b^d$, the root level dominates the work. Time is **$O(N^d)$**.

**Example: Merge Sort**
Merge sort splits the array into 2 halves ($b=2$), makes 2 recursive calls ($a=2$), and merges them in linear time ($d=1$).
$$ T(N) = 2T(N/2) + O(N^1) $$
Here, $a = 2$, and $b^d = 2^1 = 2$.
Since $a = b^d$ (Rule 2), the time complexity is **$O(N \\log N)$**.

---

## 7. Python-Specific Complexities (The Cheat Sheet)

If you are using Python in a system design interview or competitive programming, you MUST memorize the time complexities of the built-in C-optimized functions.

### Lists (Dynamic Arrays)
- `append(x)`: Amortized $O(1)$
- `pop()`: $O(1)$
- `pop(0)`: **$O(N)$** (Massive bottleneck! All elements must shift left. Use `collections.deque` instead).
- `insert(i, x)`: $O(N)$
- `sort()`: $O(N \\log N)$ (Timsort)

### Dictionaries (Hash Tables)
- `dict[key] = value`: Amortized $O(1)$
- `dict[key]`: $O(1)$
- `del dict[key]`: $O(1)$
- *Worst Case:* $O(N)$ if a catastrophic hash collision Hash DoS attack occurs.

### Sets (Hash Tables)
- `set.add(x)`: Amortized $O(1)$
- `x in set`: $O(1)$
- `setA | setB` (Union): $O(len(A) + len(B))$
- `setA & setB` (Intersection): $O(\\min(len(A), len(B)))$

---

## 8. Profiling Python Code

Theory is great, but how do you measure performance in the real world?

### Measuring Time (`timeit`)
Do not use `time.time()`. It is affected by OS background tasks and garbage collection. Use `timeit` for micro-benchmarking.
```python
import timeit
# Tests how fast a list comprehension runs
print(timeit.timeit('[x**2 for x in range(1000)]', number=1000))
```

### Measuring Space (`sys.getsizeof`)
Find exactly how many bytes an object consumes.
```python
import sys
my_list = [1, 2, 3]
print(sys.getsizeof(my_list)) # e.g., 88 bytes
```

### Full Program Profiling (`cProfile`)
Identifies exactly which functions are consuming the most CPU time.
```bash
python -m cProfile -s time my_script.py
```

---

## 9. Active Recall & Interview Readiness

1. **Why is `list.pop(0)` a terrible idea in Python?**
   *Answer:* A Python list is a contiguous C array. If you remove the 0th element, every single remaining element in the array must be copied and shifted exactly one slot to the left in RAM. If the list has 1 Million items, this takes 1 Million operations. Use `collections.deque.popleft()` instead, which is $O(1)$.

2. **If an algorithm takes $O(2^N)$ time, what is the maximum feasible $N$ before the universe ends?**
   *Answer:* Around $N = 50$. $2^{50}$ is over 1 Quadrillion operations. Even a fast CPU doing 1 Billion operations a second would take two weeks to finish. At $N=100$, it exceeds the estimated age of the universe.

3. **What is the difference between $O(1)$ and Amortized $O(1)$?**
   *Answer:* Strict $O(1)$ guarantees the operation will NEVER exceed a fixed time bound (e.g., retrieving from an array by index). Amortized $O(1)$ means the operation usually takes $O(1)$, but periodically takes $O(N)$ to resize or rehash. However, mathematically, the average cost over time remains constant.
"""
    with open(r"d:\work\python-all\03-Algorithms\01-Theory\01-Algorithm-Analysis-Python.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_markdown()
    print("DONE")
