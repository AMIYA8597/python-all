import os

md_content = r"""# CONTEST PREPARATION AND EXECUTION STRATEGY

## 1. WHY THIS MATTERS
Participating in a Live Contest (like LeetCode Weekly, Codeforces, or HackerRank) is a completely different psychological environment than practicing casually on a Sunday afternoon.

You are fighting a clock. The anxiety causes you to misread the problem statement, jump straight to coding without a plan, write buggy code, and fail edge cases. 

To succeed, you must treat a contest like a tactical military operation. You need a rigidly configured IDE, pre-written code snippets, and a strict mental protocol for debugging and submitting.

---

## 2. THE LOCAL IDE SETUP (VSCODE)

Do NOT write code directly in the browser during a contest. The browser lacks deep IntelliSense, powerful linting, and rapid debugging.

### A. The Snippet System
In competitive programming, you type the same boilerplate code 100 times. You must configure VSCode Snippets to generate this code in 2 keystrokes.

**Example `python.json` Snippets:**
- Type `bfs` -> Generates a full `collections.deque` Breadth-First Search template.
- Type `dfs` -> Generates a recursive Depth-First Search function signature.
- Type `uf` -> Generates a complete Union-Find (Disjoint Set) class with Path Compression.
- Type `trie` -> Generates a Prefix Tree node and insert/search methods.

### B. The Local Testing Harness
Never submit without testing locally. Create a `template.py` file that automatically parses inputs:

```python
import sys
from collections import deque, defaultdict
import heapq
import bisect

def solve():
    # YOUR CODE HERE
    pass

if __name__ == "__main__":
    # If using standard input (Codeforces)
    # lines = sys.stdin.read().splitlines()
    solve()
```

---

## 3. THE 4-PHASE CONTEST PROTOCOL

When the timer starts, follow this protocol rigidly.

### Phase 1: The Reading Phase (Minutes 0-2)
- Read the entire problem statement twice.
- **CRITICAL:** Look at the Constraints immediately.
  - If $N \le 20$, the algorithm is likely Backtracking or $O(2^N)$ Bitmasking.
  - If $N \le 500$, it might be an $O(N^3)$ dynamic programming solution.
  - If $N \le 10^4$, it requires an $O(N^2)$ algorithm.
  - If $N \le 10^5$ or $10^6$, it **MUST** be $O(N \log N)$ or $O(N)$ (Two Pointers, Sliding Window, Binary Search, Heaps).
  - If $N \ge 10^9$, it must be $O(\log N)$ (Binary Search) or $O(1)$ (Math).

### Phase 2: The Architecture Phase (Minutes 2-5)
- Do not touch the keyboard.
- Grab a piece of paper (or iPad).
- Manually trace the Example 1 inputs with a pen. 
- Identify the algorithmic Pattern. (Is this a Graph? Is it a Sliding Window?)
- Define the Time and Space Complexity of your proposed solution before writing it.

### Phase 3: The Coding Phase (Minutes 5-15)
- Write the code. 
- Because you already proved the logic on paper, you are just translating thoughts to Python syntax.
- Use explicit variable names (`left`, `right`, `max_so_far`, `visited_set`). Do not use `i`, `j`, `k` unless they are simple loop counters.

### Phase 4: The Edge Case Verification (Minutes 15-18)
- Before hitting Submit, verify the absolute worst-case inputs:
  - What if the array is empty? `[]`
  - What if the array has only 1 element? `[42]`
  - What if all elements are negative? `[-5, -10, -3]`
  - What if there are duplicates? `[2, 2, 2]`
  - Does the index go out of bounds? (Off-by-one errors).

---

## 4. SPEED DEBUGGING

If your local test fails, do not panic. Use the "Print Debugging" binary search protocol.

1. **Do not use a slow step-debugger.** Stepping through 100 iterations of a `for` loop takes too much time in a 90-minute contest.
2. **Print the state.** 
   `print(f"Index: {i}, Window: {arr[left:right]}, Current Max: {ans}")`
3. If the output is correct halfway through the array, the bug is in the second half.

---

## 5. ACTIVE RECALL & MENTAL CHECKLIST

### Question: Why should you look at the Constraints ($N$) before reading the story of the problem?
**Answer:** The story is often designed to distract you. The constraints mathematically dictate the required Time Complexity. If a problem asks you to find pairs of numbers, and $N = 10^5$, you know instantly that an $O(N^2)$ nested loop will result in a Time Limit Exceeded (TLE) error. You are mathematically forced to find an $O(N \log N)$ sorting solution or an $O(N)$ Hash Map solution. The constraints act as a massive hint to the underlying algorithm.

### Question: What is a "Time Limit Exceeded" (TLE) error, and how do you fix it?
**Answer:** Online judges (like LeetCode) allocate a strict time limit (usually 1-2 seconds) for your Python code to execute against massive hidden test cases. If you get a TLE, your logic might be 100% correct, but your Big-O algorithm is too slow. To fix it, you must analyze your loops. Can you replace an $O(N)$ list `.pop(0)` with an $O(1)$ `deque.popleft()`? Can you replace an $O(N)$ list search (`if x in my_list`) with an $O(1)$ set search (`if x in my_set`)? 

### Question: What is a "Memory Limit Exceeded" (MLE) error?
**Answer:** Your code used too much RAM. This usually happens in Depth-First Search (DFS) or Dynamic Programming (DP). If you use a recursive DFS on a massive graph without a `visited` set to track where you have been, the recursion will get stuck in an infinite loop, crashing the Call Stack. Alternatively, if you build a massive 3D matrix for DP, you might run out of memory. You can fix DP memory limits using "State Reduction" (only storing the previous row instead of the entire matrix).
"""

with open(r"d:\work\python-all\05-Competitive-Programming\01-Theory\02-Contest-Prep.md", "w", encoding="utf-8") as f:
    f.write(md_content)
    
print("Successfully generated 02-Contest-Prep.md")
