# Algorithm Design Paradigms

## 1. Introduction: What are Design Paradigms?
Algorithm Design Paradigms are overarching strategies or blueprints for solving computational problems. Instead of starting from scratch every time, computer scientists map a new problem to an existing paradigm to find an efficient solution.

### Why do they exist?
- **Structure**: They provide a mental framework to approach complex logic problems.
- **Optimization**: By applying the right paradigm, an exponential time ($O(2^N)$) problem can often be reduced to polynomial time ($O(N^2)$).
- **Code Reusability**: Patterns like Divide and Conquer naturally map to recursive tree structures.

### Industry Use Cases
- **Dynamic Programming**: Sequence alignment in bioinformatics (DNA matching), diff tools (Git), text editors (Levenshtein distance).
- **Divide and Conquer**: Parallel processing frameworks (MapReduce, Apache Spark), sorting algorithms built into languages (Timsort, Quicksort).
- **Greedy Algorithms**: Network routing protocols (OSPF using Dijkstra's), data compression (Huffman coding for zip/jpeg).

---

## 2. Beginner Explanation: The Real-World Metaphors
- **Divide & Conquer**: You have a 1,000-page book to find a word. You split the book in half, give half to a friend. You both split your halves and give them to more friends, until everyone has 1 page. You search your page, then combine the results.
- **Dynamic Programming (DP)**: You need to calculate $1+1+1+1+1$. You count and say "5". If I add another $+1$ at the end, you don't recount from the start; you remember the past result (5) and just add 1 to say "6". (Remembering past results is called memoization).
- **Greedy Algorithms**: You are robbing a house and have a bag. To maximize profit, you always grab the single most valuable item that fits, then the next most valuable. (Note: this doesn't always yield the absolute best result, but it's fast).
- **Backtracking**: You are solving a maze. You go down a path until you hit a dead end, then you retrace your steps (backtrack) to the last intersection and try a different path.

---

## 3. Deep Technical Explanation & Python Examples

### 3.1 Divide and Conquer
**Concept**: Divide the problem into non-overlapping subproblems, solve them recursively, and merge the solutions.
**Key elements**: Divide, Conquer (Base Case), Combine.

**Example: Merge Sort in Python**
```python
def merge_sort(arr: list) -> list:
    """
    Sorts an array using Divide and Conquer.
    Time: O(N log N) | Space: O(N)
    """
    if len(arr) <= 1:
        return arr # Base case
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # Divide
    right = merge_sort(arr[mid:])  # Divide
    
    return merge(left, right)      # Combine

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    # Combine two sorted arrays
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### 3.2 Dynamic Programming (DP)
**Concept**: For problems with *Overlapping Subproblems* and *Optimal Substructure*. Instead of recomputing, store the results of subproblems.
- **Top-Down (Memoization)**: Recursive, cache results in a dictionary.
- **Bottom-Up (Tabulation)**: Iterative, build a table from base cases up.

**Example: Coin Change (Bottom-Up DP)**
```python
def coin_change(coins: list, amount: int) -> int:
    """
    Finds the minimum coins needed to make up an amount.
    Time: O(amount * len(coins)) | Space: O(amount)
    """
    # dp[i] represents minimum coins needed for amount i
    # Initialize with infinity, base case dp[0] = 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                # Minimum of what we have vs using this coin + previous best
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 3.3 Greedy Algorithms
**Concept**: Make the locally optimal choice at each step, hoping it leads to a global optimum. Only works if the problem has the *Greedy Choice Property*.

**Example: Activity Selection (Maximum meetings in a room)**
```python
def max_meetings(starts: list, ends: list) -> int:
    """
    Find max non-overlapping meetings.
    Time: O(N log N) due to sorting | Space: O(N)
    """
    # Pair starts and ends, then sort by END time (Greedy choice)
    meetings = sorted(zip(starts, ends), key=lambda x: x[1])
    
    count = 0
    last_end_time = -1
    
    for start, end in meetings:
        if start >= last_end_time: # No overlap
            count += 1
            last_end_time = end # Update the end time
            
    return count
```

### 3.4 Backtracking
**Concept**: Incrementally build candidates to the solutions, and abandon a candidate ("backtrack") as soon as it determines the candidate cannot lead to a valid solution.

**Example: N-Queens Problem (Snippets)**
```python
def solve_n_queens(n: int) -> list:
    """
    Places N queens on an NxN chessboard.
    Time: O(N!) | Space: O(N^2)
    """
    def backtrack(row, diagonals, anti_diagonals, cols, state):
        if row == n:
            res.append(state[:])
            return
            
        for col in range(n):
            curr_diag = row - col
            curr_anti = row + col
            # Valid placement check
            if col in cols or curr_diag in diagonals or curr_anti in anti_diagonals:
                continue
                
            # Place Queen
            cols.add(col)
            diagonals.add(curr_diag)
            anti_diagonals.add(curr_anti)
            
            # Recurse to next row
            backtrack(row + 1, diagonals, anti_diagonals, cols, state + [col])
            
            # Backtrack (Remove Queen)
            cols.remove(col)
            diagonals.remove(curr_diag)
            anti_diagonals.remove(curr_anti)
            
    res = []
    backtrack(0, set(), set(), set(), [])
    return res
```

---

## 4. Advanced Concepts: When to use what?
- **DP vs Divide & Conquer**: Both break problems down. If subproblems are independent (e.g., sorting left half doesn't affect right half), use Divide & Conquer. If subproblems overlap (e.g., calculating Fibonacci(4) requires Fib(3) and Fib(2); Fib(3) also requires Fib(2)), use DP.
- **DP vs Greedy**: Greedy is faster but doesn't always guarantee an optimal solution. If the problem exhibits the *greedy choice property* (local optimum leads to global optimum), use Greedy (e.g., Dijkstra). Otherwise, use DP (e.g., Bellman-Ford).

---

## 5. Common Mistakes and Performance Considerations
1. **Forgetting DP Base Cases**: A recursive DP without a base case will result in `RecursionError: maximum recursion depth exceeded`.
2. **Greedy Traps**: Assuming a greedy approach works for everything. (e.g., Using Greedy for Coin Change works for US currency [25, 10, 5, 1], but fails for arbitrary coin systems like [4, 3, 1] to make 6).
3. **State representation in DP**: Passing large mutable objects (like lists) as state parameters in DP recursion is slow. Use immutable types (tuples, integers) as state keys.

---

## 6. Interview Questions & Practical Exercises

### Interview Questions
1. How do you decide whether to use Dynamic Programming or a Greedy approach for an optimization problem?
2. Explain Top-Down Memoization vs Bottom-Up Tabulation. What are the space complexity trade-offs?
3. What is the fundamental difference between Backtracking and standard Recursion?
4. Why is sorting by 'end time' the optimal greedy strategy for the Activity Selection problem, rather than sorting by 'start time' or 'duration'?

### Exercises
1. **Divide and Conquer**: Implement Binary Search in Python recursively. What is the Big-O time and space complexity?
2. **DP Tabulation**: Write a Bottom-Up DP solution to find the Longest Common Subsequence of two strings `text1` and `text2`.
3. **Backtracking**: Implement a Sudoku solver using Backtracking. Define the base case, the valid check, and the backtrack step clearly.
