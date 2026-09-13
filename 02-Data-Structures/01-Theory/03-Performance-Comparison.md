# Performance Comparison and Big-O in Python

## 1. Why This Matters
If you write an algorithm that iterates over a list of 100,000 items and checks `if item in list2` (where `list2` also has 100,000 items), your code will perform 10,000,000,000 operations. It will freeze. If you simply convert `list2` to a `set` beforehand, the same algorithm performs 100,000 operations and finishes in milliseconds. Understanding the performance profiles of Python's data structures is the absolute difference between junior code that crashes in production and senior code that scales infinitely.

## 2. Prerequisites
- `01-DS-Fundamentals-Python.md`
- `02-Memory-Layout-Analysis.md`

## 3. The Core Problem Solved
Data structures are trade-offs. You cannot have a structure that is perfectly ordered, instantly searchable, and memory-efficient all at once. Performance comparison solves the problem of "Algorithm Selection" by providing a map of these trade-offs, ensuring you select the correct tool for your specific bottleneck (e.g., read-heavy vs write-heavy workloads).

---

## 4. The List (Dynamic Array) Performance
Lists are highly optimized for sequential access and appending to the end. They are terrible for searching and modifying the front.

| Operation | Average Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Index Access** `lst[5]` | $O(1)$ | $O(1)$ | Direct memory offset calculation. Instant. |
| **Append** `lst.append(x)` | $O(1)$ | $O(N)$ | $O(1)$ Amortized. When the over-allocated array fills, Python must allocate a new, larger array and copy all $N$ pointers over. |
| **Pop Last** `lst.pop()` | $O(1)$ | $O(1)$ | Instant. Just reduces the internal size counter. |
| **Pop Front** `lst.pop(0)`| $O(N)$ | $O(N)$ | **DANGER.** Every remaining item must shift left by one slot. Do not use lists for queues! |
| **Insert** `lst.insert(0, x)`| $O(N)$ | $O(N)$ | **DANGER.** Every item must shift right by one slot. |
| **Search** `x in lst` | $O(N)$ | $O(N)$ | Must scan the entire list item by item until found. |

---

## 5. The Dictionary / Set (Hash Table) Performance
Dictionaries and Sets are backed by Hash Tables. They trade massive amounts of memory overhead to provide near-instant lookups.

| Operation | Average Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Search** `x in dict` | $O(1)$ | $O(N)$ | Hashes the key and jumps directly to the bucket. |
| **Insert** `dict[x] = 1` | $O(1)$ | $O(N)$ | Hashes the key and writes to the bucket. Resizing the table occasionally triggers an $O(N)$ rebuild. |
| **Delete** `del dict[x]` | $O(1)$ | $O(N)$ | Hashes and marks the bucket as deleted (dummy). |

### 5.1 The $O(N)$ Worst-Case Trap (Hash Collisions)
Why do hash tables have an $O(N)$ worst case?
If you insert objects that have terrible hash functions (e.g., they all hash to the same integer, or you are subjected to a hash-collision Denial of Service attack), every item ends up in the EXACT SAME BUCKET. The hash table degenerates into a Linked List, and finding an item requires scanning every item in that bucket, resulting in $O(N)$ time.

Python protects against Hash DoS attacks by randomizing string hashes on startup (`PYTHONHASHSEED`).

---

## 6. The Deque (Double-Ended Queue) Performance
Provided by `collections.deque`. A deque is implemented as a block-based Doubly Linked List in C. It is optimized for adding and removing from BOTH ends.

| Operation | Average Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Append/Pop Right** | $O(1)$ | $O(1)$ | Same as list, but never triggers a massive array copy. |
| **Append/Pop Left** | $O(1)$ | $O(1)$ | **The primary reason to use deque.** Perfect for Queues. |
| **Search** `x in dq` | $O(N)$ | $O(N)$ | Must traverse the linked list pointers. |
| **Index Access** `dq[50]`| $O(N)$ | $O(N)$ | **DANGER.** It is not an array! To find the 50th item, it must traverse 50 pointers. (Technically $O(N)$ bounded by the distance from the closest end). |

---

## 7. The Performance Decision Tree
When architecting a solution, use this matrix:

1. **Do I need to maintain order?**
   - No: Use `set` or `dict`.
   - Yes: Use `list`, `deque`, or (Python 3.7+) `dict`.
2. **Am I searching for items constantly (`if x in ds:`)?**
   - Yes: **MUST** use `set` or `dict`.
3. **Am I removing/adding items to the front (FIFO Queue)?**
   - Yes: **MUST** use `collections.deque`.
4. **Do I need to access items by arbitrary index (`ds[99]`)?**
   - Yes: **MUST** use `list` or `tuple`.
5. **Is the data fixed and read-only?**
   - Yes: Use `tuple`. It is faster and lighter than a list.

---

## 8. Active Recall
1. Why is `lst.pop(0)` an $O(N)$ operation?
   **Answer:** Because a list is a contiguous array. Removing the first item leaves a hole at the front of memory. To maintain contiguity, all remaining $N-1$ items must be shifted one slot to the left.
2. Under what condition does a Dictionary lookup degrade to $O(N)$?
   **Answer:** When there are massive Hash Collisions. If the hash function maps many keys to the same bucket, Python must linearly scan that bucket to find the exact match.
3. If you need to implement a Queue, which data structure should you use and why?
   **Answer:** `collections.deque`. It allows $O(1)$ pops from the left side (`popleft()`), whereas a standard list takes $O(N)$ time.

## 9. Interview Scenarios
**Scenario:** You are writing an anagram grouping algorithm. You iterate through 10,000 words. For each word, you sort the characters (e.g., "eat" -> "aet") and append it to a structure. How do you group them optimally?
**Answer:** Use a `defaultdict(list)`. The sorted string "aet" is the key ($O(1)$ lookup). The value is a list of original words. `groups["aet"].append("eat")`. This achieves $O(N \cdot K \log K)$ overall time, where $K$ is the max word length.
