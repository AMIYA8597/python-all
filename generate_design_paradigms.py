import os

def generate_markdown():
    content = """# Algorithm Design Paradigms: The Architect's Toolkit

## 1. Why This Matters

When faced with a new programming problem, you shouldn't just start writing code blindly. Every major algorithm in computer science follows one of a few distinct **Design Paradigms**. 

A paradigm is a mental framework. By recognizing the constraints of a problem, you can instantly categorize it and deploy the correct paradigm. Is the problem asking for an absolute optimal solution? Is the dataset too large? Does the problem have overlapping subproblems?

Mastering these 7 paradigms is the key to passing System Design and Data Structures & Algorithms interviews.

---

## 2. Brute Force (Exhaustive Search)

The simplest, most naive approach. Generate every single possible solution, evaluate them all, and pick the best one.

- **How it works:** Iterates through the entire search space without any mathematical shortcuts.
- **When to use it:** When the dataset is incredibly small, or when you are writing a baseline solution to test a more complex algorithm against.
- **Time Complexity:** Usually catastrophic ($O(N^2)$, $O(2^N)$, or $O(N!)$).
- **Classic Examples:** 
  - Linear Search in an array.
  - Bubble Sort.
  - Checking every permutation for the Traveling Salesperson.

---

## 3. Divide and Conquer

Break a massive problem into smaller, independent sub-problems. Solve the sub-problems recursively, and then merge the answers back together.

- **How it works:** 
  1. **Divide:** Split the dataset in half (or into $K$ pieces).
  2. **Conquer:** Recursively solve each half.
  3. **Combine:** Merge the two solved halves into a final answer.
- **When to use it:** When the sub-problems are completely **independent** (they don't overlap).
- **Time Complexity:** Usually $O(N \\log N)$ (Master Theorem).
- **Classic Examples:**
  - Merge Sort.
  - Quick Sort.
  - Binary Search.

---

## 4. Greedy Algorithms

Make the choice that looks absolutely best *right now* (locally optimal), and hope that it leads to the best overall solution (globally optimal).

- **How it works:** Never looks back. Never reconsiders a previous choice. Just grabs the best available option at the current step.
- **When to use it:** Only works if the problem has the **"Greedy-Choice Property"** (making a locally optimal choice guarantees a globally optimal solution). It fails on many problems (like the Knapsack problem).
- **Time Complexity:** Very fast. Usually $O(N)$ or $O(N \\log N)$ (if sorting is required first).
- **Classic Examples:**
  - Dijkstra's Algorithm (Shortest Path).
  - Prim's and Kruskal's Algorithms (Minimum Spanning Tree).
  - Huffman Coding (Data Compression).

---

## 5. Dynamic Programming (DP)

The most feared paradigm in interviews. It is essentially an optimization over plain recursion. When a recursive algorithm solves the exact same sub-problem over and over again, DP memorizes the answer so it never has to compute it twice.

- **How it works:** TRADES SPACE FOR TIME. It uses an array or hash map to store the results of expensive function calls.
- **When to use it:** The problem MUST have two properties:
  1. **Optimal Substructure:** The optimal solution can be built from optimal solutions of its sub-problems.
  2. **Overlapping Subproblems:** The algorithm asks the exact same question multiple times.
- **Approaches:**
  - **Top-Down (Memoization):** Write standard recursion, but add a cache (Hash Map).
  - **Bottom-Up (Tabulation):** Build an array from size 0 up to N using a `for` loop, avoiding recursion entirely.
- **Classic Examples:**
  - Fibonacci Sequence ($O(2^N)$ optimized to $O(N)$).
  - The Knapsack Problem.
  - Bellman-Ford Algorithm (Shortest Path with negative weights).

---

## 6. Backtracking

A refined Brute Force. It explores a potential solution path, but the moment it realizes the path is mathematically invalid, it **"backtracks"** (undoes the last choice) and tries a different path.

- **How it works:** Explores the decision tree using Depth First Search (DFS). If a constraint is violated, it immediately prunes that entire branch of the tree.
- **When to use it:** When you need to find *all* possible solutions, or when constraints make greedy/DP impossible.
- **Time Complexity:** Usually Exponential $O(2^N)$ or Factorial $O(N!)$, but much faster than raw brute force due to pruning.
- **Classic Examples:**
  - Solving a Sudoku puzzle.
  - The N-Queens Problem.
  - Generating permutations and combinations.

---

## 7. Randomized Algorithms

Algorithms that make random choices during their execution. They are highly resilient against malicious worst-case inputs.

- **Monte Carlo Algorithms:** 
  - **Guarantee:** Strict time limit (always fast).
  - **Risk:** Might return the WRONG answer.
  - **Use Case:** Machine Learning, determining Pi by throwing random darts at a board, probabilistic prime testing.
- **Las Vegas Algorithms:**
  - **Guarantee:** Always returns the CORRECT answer.
  - **Risk:** Might take a long time to finish (Time is random).
  - **Use Case:** Randomized QuickSort (picks a random pivot to avoid the $O(N^2)$ worst case).

---

## 8. Heuristics and Approximation Algorithms

When a problem is mathematically proven to be **NP-Hard** (e.g., the exact optimal Traveling Salesperson route for 1,000 cities), you cannot use DP or Backtracking because the universe will end before it finishes.

- **How it works:** Abandons the search for the "Absolute Best" answer. Instead, uses rules-of-thumb to find a "Good Enough" answer very quickly.
- **Approximation Algorithms:** Mathematically guarantee that the answer will be within a certain percentage (e.g., "This answer is guaranteed to be no worse than 2x the optimal answer").
- **Meta-Heuristics:** Emulate nature to find good solutions.
- **Classic Examples:**
  - **A* (A-Star) Search:** Uses a heuristic (like straight-line distance) to guide a pathfinding algorithm faster than Dijkstra's.
  - **Genetic Algorithms:** Simulates natural selection, mutating and breeding solutions over generations.
  - **Simulated Annealing:** Simulates the cooling of metal, allowing the algorithm to make intentionally "bad" choices early on to escape local optimum traps.

---

## 9. Active Recall & Interview Readiness

1. **What is the difference between Divide & Conquer and Dynamic Programming?**
   *Answer:* Both break problems down into sub-problems. However, Divide & Conquer sub-problems are completely *independent* (e.g., sorting the left half of an array has nothing to do with the right half). DP sub-problems *overlap* (e.g., calculating Fibonacci(5) requires calculating Fibonacci(3), and Fibonacci(4) ALSO requires calculating Fibonacci(3)). DP caches the overlap.

2. **When should you completely abandon Dynamic Programming and use Heuristics?**
   *Answer:* When the state space is too massive, or the problem is mathematically NP-Hard. DP requires creating an array/table to represent states. If the problem requires a 10-dimensional DP array that takes 5 Terabytes of RAM, DP is impossible. You must use Heuristics.

3. **Why does QuickSort use Randomization (Las Vegas paradigm)?**
   *Answer:* If you always pick the first element as the pivot, and someone feeds you an array that is already sorted, QuickSort degrades into $O(N^2)$ time. By picking a *random* pivot, you mathematically destroy any malicious input pattern, guaranteeing an expected runtime of $O(N \\log N)$.
"""
    with open(r"d:\work\python-all\03-Algorithms\01-Theory\03-Design-Paradigms.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_markdown()
    print("DONE")
