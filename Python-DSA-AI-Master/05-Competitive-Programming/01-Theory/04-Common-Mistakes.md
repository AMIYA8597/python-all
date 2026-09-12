# Competitive Programming in Python: Common Mistakes & Pitfalls

Competitive Programming (CP) requires writing efficient, bug-free, and optimal code under strict time constraints. Python is highly expressive and readable, making it a great language for fast implementation. However, due to its interpreted nature, it is slower than C++ or Java. Writing idiomatic and optimized Python is crucial to avoiding common pitfalls like Time Limit Exceeded (TLE) and Memory Limit Exceeded (MLE).

This document covers the most common mistakes Python developers make in CP and provides professional solutions.

---

## 1. Time Limit Exceeded (TLE)

The most frequent error in Python CP is TLE. This happens when the algorithm is theoretically correct but practically too slow, or when Python overhead is too high.

### 1.1 Using `input()` and `print()` in Loops
**Mistake:** Using standard `input()` and `print()` for reading/writing large amounts of data. `input()` strips trailing newlines and has significant overhead.
**Solution:** Use `sys.stdin.readline` and `sys.stdout.write`.

```python
# MISTAKE
n = int(input())
for _ in range(n):
    val = input()
    print(val)

# SOLUTION
import sys
input = sys.stdin.readline
n = int(input())
for _ in range(n):
    val = input()
    sys.stdout.write(val)
```

### 1.2 String Concatenation in Loops
**Mistake:** Strings are immutable in Python. Using `+=` to build a string in a loop creates a new string object each time, leading to $O(N^2)$ complexity.
**Solution:** Use lists and `"".join()`.

```python
# MISTAKE (O(N^2))
s = ""
for char in "hello" * 10000:
    s += char

# SOLUTION (O(N))
chars = []
for char in "hello" * 10000:
    chars.append(char)
s = "".join(chars)
```

### 1.3 `list.pop(0)` or `list.insert(0, val)`
**Mistake:** Removing or inserting an element at the beginning of a Python list takes $O(N)$ time because all subsequent elements must be shifted. Doing this in a loop causes $O(N^2)$ complexity.
**Solution:** Use `collections.deque`, which provides $O(1)$ time complexity for appends and pops from both ends.

```python
# MISTAKE
queue = [1, 2, 3]
queue.pop(0) # O(N)

# SOLUTION
from collections import deque
queue = deque([1, 2, 3])
queue.popleft() # O(1)
```

---

## 2. Memory Limit Exceeded (MLE)

### 2.1 Storing Unnecessary Large Matrices
**Mistake:** Pre-allocating $N \times M$ lists for $10^5 \times 10^5$ constraints will instantly cause MLE.
**Solution:** Check constraints. If $N \times M$ is too large, use a dictionary for sparse graphs/matrices or process row-by-row.

### 2.2 Deep Recursion Limits
**Mistake:** Python has a default recursion limit of 1000. For tree/graph traversals (DFS) on large graphs, you will hit a `RecursionError`.
**Solution:** Increase the recursion limit manually using `sys.setrecursionlimit()`. Note that Python 3 handles stack limits differently in PyPy; you might still get MLE if the recursion depth is too high. An iterative DFS is always safer.

```python
import sys
# Set recursion limit higher for deep DFS
sys.setrecursionlimit(10**6)
```

---

## 3. Logical and Language Pitfalls

### 3.1 Mutable Default Arguments
**Mistake:** Using a list or dictionary as a default argument in a function. The default object is evaluated once at function definition, meaning it is shared across all function calls.
**Solution:** Use `None` and initialize inside the function.

```python
# MISTAKE
def add_to_graph(node, neighbors=[]):
    neighbors.append(node)
    return neighbors

# SOLUTION
def add_to_graph(node, neighbors=None):
    if neighbors is None:
        neighbors = []
    neighbors.append(node)
    return neighbors
```

### 3.2 Floating Point Precision Issues
**Mistake:** Python's floats are IEEE 754 double precision (64-bit). They are subject to rounding errors.
**Solution:** 
- Use integer arithmetic wherever possible (e.g., cross products for geometry instead of division).
- If division is necessary for large integers, use `//` for exact integer division.
- For precise decimals, use the `decimal` module, or `fractions.Fraction`.

```python
# MISTAKE
0.1 + 0.2 == 0.3 # False! It evaluates to 0.30000000000000004

# SOLUTION
from fractions import Fraction
Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10) # True
```

### 3.3 Overlooking the `mod` Requirement
**Mistake:** Problems often ask for the answer modulo $10^9 + 7$. Applying modulo only at the end can cause huge integers that slow down Python's BigInt operations.
**Solution:** Apply modulo at every step of addition, subtraction, or multiplication.

```python
MOD = 10**9 + 7
a = 10**18
b = 10**18
# MISTAKE: Computes massive number then mods
ans = (a * b) % MOD

# SOLUTION: Modulo early and often (though Python handles BigInt, it's slower)
ans = ((a % MOD) * (b % MOD)) % MOD
```

---

## 4. Algorithmic Misconceptions

### 4.1 $O(N)$ `in` Operator on Lists
**Mistake:** Using `if item in my_list:` inside a loop. The `in` operator on a list takes $O(N)$ time.
**Solution:** Use a `set` or `dict`. The `in` operator on sets/dicts takes $O(1)$ time on average.

```python
# MISTAKE
my_list = [1, 2, 3, 4, 5]
# O(N) lookup
if 3 in my_list:
    pass

# SOLUTION
my_set = {1, 2, 3, 4, 5}
# O(1) lookup
if 3 in my_set:
    pass
```

### 4.2 Recomputing Invariants inside Loops
**Mistake:** Calling `len(s)` or making the same computation inside a loop condition or body when it does not change.
**Solution:** Compute it once before the loop.

## Summary Checklist
- [ ] Swapped `input()` with `sys.stdin.readline`?
- [ ] Used `deque` instead of `list.pop(0)`?
- [ ] Used `set()` for fast lookups?
- [ ] Handled `sys.setrecursionlimit` for DFS?
- [ ] Checked for string concatenation in loops?
- [ ] Applied modulo arithmetic correctly?
- [ ] Handled large list allocations to prevent MLE?
