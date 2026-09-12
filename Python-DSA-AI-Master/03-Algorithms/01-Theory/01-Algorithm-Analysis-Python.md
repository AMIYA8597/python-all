# Algorithm Analysis in Python

## 1. Introduction: What is Algorithm Analysis and Why Does it Exist?
Algorithm analysis is the process of evaluating the computational complexity of algorithms—specifically, the amount of time, storage, or other resources necessary to execute them. 

### Why does it exist?
- **Scalability**: As data grows, an algorithm that works well for 100 items might take years for 1,000,000 items. Analysis helps us predict scalability.
- **Resource Management**: In constrained environments (embedded systems, high-frequency trading), memory and CPU cycles are at a premium.
- **Objective Comparison**: It provides a mathematical way to compare two algorithms independently of hardware, programming language, or OS.

### Industry Use Cases
- **Database Query Optimizers**: Choosing the fastest execution plan out of thousands of possibilities.
- **Web Servers**: Managing connection handling and routing efficiently under heavy load.
- **Data Engineering Pipelines**: Processing terabytes of data within a daily window.

---

## 2. Beginner Explanation: The Intuition
Imagine you have to find a specific book in a library. 
- **Approach 1 (Linear Search)**: You check every single book on every shelf. If there are $N$ books, worst case, you check $N$ books.
- **Approach 2 (Binary Search)**: If the books are sorted alphabetically, you go to the middle, check if your book is in the left or right half, and repeat. You eliminate half the books at each step. This takes at most $\approx \log_2(N)$ steps.

Algorithm analysis formalizes this intuitive idea of "how many steps" into Big-O notation.

---

## 3. Deep Technical Explanation: Big-O, Big-Omega, Big-Theta
When we analyze algorithms, we generally look at three bounds:
- **Big-O ($O$)**: Upper bound. "The algorithm will take *at most* this much time." (Most common in interviews).
- **Big-Omega ($\Omega$)**: Lower bound. "The algorithm will take *at least* this much time."
- **Big-Theta ($\Theta$)**: Tight bound. "The algorithm will take *exactly* this much time."

### 3.1 Common Big-O Complexities (Best to Worst)
1. **$O(1)$ Constant Time**: Array index access, hash map lookup.
2. **$O(\log N)$ Logarithmic Time**: Binary search, operations on balanced binary search trees.
3. **$O(N)$ Linear Time**: Iterating through an array.
4. **$O(N \log N)$ Linearithmic Time**: Merge sort, quicksort (average).
5. **$O(N^2)$ Quadratic Time**: Nested loops, bubble sort.
6. **$O(2^N)$ Exponential Time**: Recursive Fibonacci without memoization, subsets.
7. **$O(N!)$ Factorial Time**: Generating permutations, Traveling Salesperson Problem (naive).

### 3.2 Time vs Space Complexity
- **Time Complexity**: How the runtime grows as input grows.
- **Space Complexity**: How the extra memory used grows as input grows. (Note: output space is sometimes excluded, but auxiliary space is always counted).

---

## 4. Practical Python Examples

### Example 1: $O(1)$ vs $O(N)$

```python
# O(1) Time, O(1) Space
def get_first_element(arr: list) -> int:
    """Returns the first element of the list."""
    if arr:
        return arr[0]
    return -1

# O(N) Time, O(1) Space
def find_max(arr: list) -> int:
    """Finds the maximum value in a list."""
    if not arr:
        return -1
    max_val = arr[0]
    # Iterating through N elements
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

### Example 2: $O(N^2)$ Quadratic Time

```python
# O(N^2) Time, O(1) Space
def has_duplicate_naive(arr: list) -> bool:
    """Checks for duplicates using nested loops."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False

# Optimization: O(N) Time, O(N) Space
def has_duplicate_optimized(arr: list) -> bool:
    """Checks for duplicates using a hash set."""
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```

### Example 3: Python Built-in Complexities
In Python, you must know the complexities of built-in data structures:
- `list.append(x)`: $O(1)$ amortized
- `list.insert(0, x)`: $O(N)$ - shifts all elements
- `set.add(x)` / `x in set`: $O(1)$ average, $O(N)$ worst
- `dict[key] = value` / `key in dict`: $O(1)$ average, $O(N)$ worst

---

## 5. Advanced Concepts & Internal Details

### Amortized Analysis
Sometimes, an operation is usually $O(1)$, but occasionally $O(N)$. For example, appending to a Python `list` (which is a dynamic array under the hood). When the underlying array is full, Python allocates a new, larger array and copies all elements over (an $O(N)$ operation). However, because this happens rarely, the *average* time per append across many operations is $O(1)$. This is amortized $O(1)$.

### Empirical Analysis in Python
Theoretical analysis (Big-O) is crucial, but empirical analysis (profiling) is practical. Python provides tools for this:
- **`timeit`**: For micro-benchmarking small snippets.
- **`cProfile`**: For profiling entire scripts.

```python
import timeit

# Measuring list comprehension vs for loop
setup = "n = 10000"
stmt1 = "[i * 2 for i in range(n)]"
stmt2 = "res = []\nfor i in range(n):\n    res.append(i * 2)"

print(timeit.timeit(stmt1, setup=setup, number=1000))
print(timeit.timeit(stmt2, setup=setup, number=1000))
```

---

## 6. Common Mistakes and Performance Considerations
1. **Hidden $O(N)$ operations in loops**: 
   ```python
   for item in my_list:
       if item in my_other_list: # O(N) lookup inside O(N) loop = O(N^2)!
           pass
   ```
   *Fix*: Convert `my_other_list` to a `set` first.
2. **String Concatenation**: Using `+` in a loop to build a string creates a new string each time, leading to $O(N^2)$.
   *Fix*: Use `list.append()` and `"".join()`.
3. **Using `list.pop(0)`**: This is $O(N)$ because it shifts all remaining elements.
   *Fix*: Use `collections.deque.popleft()` which is $O(1)$.

---

## 7. Interview Questions & Practical Exercises

### Interview Questions
1. What is the difference between worst-case and amortized time complexity? Give an example.
2. Why is looking up an element in a Hash Map $O(1)$ on average, but $O(N)$ in the worst case?
3. What is the time complexity of slicing a list in Python, e.g., `arr[k:n]`? *(Answer: $O(n-k)$)*
4. If an algorithm takes $O(N)$ time and you double the input size, how does the runtime change? What if it's $O(2^N)$?

### Exercises
1. **Analyze this code**: What is the time and space complexity?
   ```python
   def matrix_sum(matrix):
       total = 0
       for row in matrix:
           for val in row:
               total += val
       return total
   ```
2. **Optimize**: You are given two lists, A and B. Return a list of elements that appear in both. Write an $O(N \times M)$ solution, then optimize it to $O(N + M)$ time.
3. **Space Complexity**: Write a recursive function to compute the Nth Fibonacci number. What is the time complexity? What is the *space* complexity due to the call stack?
