# COMMON MISTAKES AND DEADLY TRAPS IN COMPETITIVE PROGRAMMING

## 1. WHY THIS MATTERS
You write a brilliant $O(N \log N)$ algorithm. You run it on the sample test cases, and it passes perfectly. You click "Submit" with a smile on your face.

**Status: Time Limit Exceeded (TLE)** or **Wrong Answer (WA)**.

Why? Because Competitive Programming platforms test your code against extremely malicious, adversarial edge cases designed specifically to break your code. If you do not understand the hidden memory allocation rules of Python, or if you fail to account for integer overflows (in other languages), or if you make an off-by-one index error, you will fail the interview.

This chapter outlines the most deadly traps in Python Competitive Programming and how to architect your code to avoid them.

---

## 2. THE PYTHON LIST `.pop(0)` TRAP ($O(N)$ TIME KILLER)

This is the most common reason Python developers fail BFS (Breadth-First Search) questions.

**The Bad Code:**
```python
queue = [1, 2, 3, 4]
while queue:
    node = queue.pop(0) # REMOVES FROM THE FRONT
```

**Why it fails:**
A Python `list` is a dynamic array (a contiguous block of memory). When you call `pop(0)`, it deletes the first element. To prevent empty memory gaps, Python must physically shift *every single subsequent element* one space to the left. 
If your queue has 1,000,000 elements, a single `.pop(0)` takes 1 Million operations. An $O(N)$ BFS algorithm instantly degrades into an $O(N^2)$ algorithm, causing a catastrophic Time Limit Exceeded (TLE).

**The Solution:**
Always use `collections.deque` for Queues. It is implemented as a doubly-linked list.
```python
from collections import deque
queue = deque([1, 2, 3, 4])
while queue:
    node = queue.popleft() # EXACTLY O(1) TIME!
```

---

## 3. THE STRING CONCATENATION TRAP (MEMORY BLOAT)

Strings in Python are **Immutable**. They cannot be changed in place.

**The Bad Code:**
```python
result = ""
for char in large_array:
    result += char # VERY BAD!
```

**Why it fails:**
Because strings are immutable, `result += char` does not append the character. It asks the OS for a brand new chunk of RAM, physically copies the entire existing `result` string into the new RAM, and then adds the character. 
If the string is 100,000 characters long, this loop executes $O(N^2)$ copying operations, causing a Time Limit Exceeded and a massive Memory Spike.

**The Solution:**
Use an array (List) to collect the characters (since appending to a list is $O(1)$ amortized), and then `.join()` them at the very end.
```python
result_list = []
for char in large_array:
    result_list.append(char) # O(1)
final_string = "".join(result_list) # O(N) done exactly ONCE.
```

---

## 4. THE OFF-BY-ONE ERROR (BINARY SEARCH)

Binary search is notoriously difficult to code without bugs. You get stuck in an infinite loop because `left` and `right` overlap incorrectly.

**The Bad Code:**
```python
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target:
        left = mid # BUG! INFINITE LOOP RISK!
    else:
        right = mid # BUG!
```
If `left = 4` and `right = 5`, `mid = (4+5)//2 = 4`. 
If `arr[4] < target`, we set `left = mid = 4`. The loop repeats forever!

**The Solution:**
Always strictly isolate the `mid` element. Since we already checked `arr[mid]`, we know it is NOT the target. Therefore, we must exclude it completely from the next search space.
```python
    elif arr[mid] < target:
        left = mid + 1 # Strictly move past mid
    else:
        right = mid - 1 # Strictly move past mid
```

---

## 5. THE MUTABLE DEFAULT ARGUMENT TRAP

**The Bad Code:**
```python
def dfs(node, visited=set()):
    visited.add(node)
    # ...
```

**Why it fails:**
In Python, default arguments are evaluated **EXACTLY ONCE** when the function is defined, NOT every time the function is called! 
If LeetCode runs your `dfs()` function on Test Case 1, `visited` populates with nodes. When LeetCode runs your function on Test Case 2, it reuses the exact same `visited` set from Test Case 1! Your code will instantly fail Test Case 2 because it thinks all nodes are already visited.

**The Solution:**
Use `None` and initialize inside the function.
```python
def dfs(node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
```

---

## 6. ACTIVE RECALL & INTERVIEW SCENARIOS

### Scenario 1:
**Interviewer:** "You wrote `for i in range(len(arr)): arr.remove(arr[i])`. The code is throwing an IndexError. Why?"
**Your Thought Process:** "Modifying a list while actively iterating over it is a fatal flaw in Python. As elements are removed, the length of the list shrinks, and the internal indices shift left. Eventually, the `for` loop requests an index that no longer exists, crashing the program. The correct approach is to iterate backwards (`for i in range(len(arr)-1, -1, -1)`), iterate over a copy of the list (`for x in arr[:]`), or better yet, use a List Comprehension to generate a new filtered list."

### Scenario 2:
**Interviewer:** "Your recursive DFS solution works for small graphs, but on our massive $10^6$ node test case, it throws a `RecursionError: maximum recursion depth exceeded`. How do you fix this?"
**Your Thought Process:** "Python has a hardcoded limit on the Call Stack (usually 1,000 recursive calls) to prevent the OS from crashing due to Stack Overflow. A massive graph with a deep path exceeds this limit. To fix it, I have two choices: 
1. Artificially raise the limit using `sys.setrecursionlimit(2000000)` (which is a hack and often disallowed).
2. Rewrite the DFS algorithm iteratively using a manual `while` loop and a standard Python `list` acting as a Stack. This moves the memory burden from the OS Call Stack to the system Heap, allowing infinite depth."
