import os

markdown_content = r"""# Competitive Programming Sites & Ecosystems: A Comprehensive Guide for Python Programmers

Competitive programming (CP) is the ultimate test of a programmer's algorithmic problem-solving abilities, mathematical insight, and implementation speed. While languages like C++ have historically dominated the competitive programming landscape due to their bare-metal performance, manual memory management, and extensive Standard Template Library (STL), Python has rapidly grown in popularity. Its clean syntax, immense built-in data structure capabilities, and built-in arbitrary-precision arithmetic make it an outstanding language for algorithmic interviews, educational problem solving, and many competitive programming platforms.

However, training for olympiad-level programming in Python requires more than just knowing language basics. It demands a deep understanding of standard algorithms, precise time and space complexity analysis, Python's internal interpreter workings, and advanced strategies to mitigate Python's relatively slow execution speed compared to compiled languages. An algorithm that passes effortlessly in C++ might hit a Time Limit Exceeded (TLE) or Memory Limit Exceeded (MLE) verdict in Python if not implemented with extreme care and optimization.

This reference guide provides a deep, textbook-level exploration of the most critical competitive programming resources, wikis, and ecosystems. We will explore how to extract the maximum value from **CP-Algorithms**, the **CSES Problem Set**, **Project Euler**, and the **USACO Guide**. Furthermore, we will detail specifically how to train for olympiad-level problem solving using Python, covering language quirks, fast I/O optimizations, memory profiling, and standard library mastery.

---

## 1. CP-Algorithms: The Russian Olympiad Bible

[CP-Algorithms](https://cp-algorithms.com/) is the English translation of the legendary Russian competitive programming wiki, E-Maxx (e-maxx.ru). It is widely regarded as one of the most comprehensive, rigorous, and high-quality repositories of algorithmic knowledge available on the internet. For years, the Russian CP community has dominated international competitions like the ACM ICPC and IOI, and CP-Algorithms distills the strategies and data structures that fuel that dominance.

### 1.1. Core Philosophy and Structure
Unlike interactive online judges or highly curated syllabi that hold the student's hand, CP-Algorithms operates as a pure academic encyclopedia. It is categorized by broad mathematical and computer science domains:

- **Algebra:** Fast Fourier Transform (FFT) for polynomial multiplication, Modular Arithmetic, Prime Sieves (Sieve of Eratosthenes and Linear Sieve), Matrix Exponentiation for linear recurrence relations, and Diophantine Equations.
- **Data Structures:** Fenwick Trees (Binary Indexed Trees) for dynamic prefix sums, Segment Trees for arbitrary range queries and lazy propagation, Disjoint Set Union (DSU) for connected components, Sparse Tables for static RMQ (Range Minimum Query), and Treaps (Cartesian Trees) for balanced binary search trees.
- **String Processing:** Z-Function and Prefix Function (KMP) for pattern matching, Suffix Arrays for lexicographical sorting of suffixes, Aho-Corasick automaton for multi-pattern search, and Suffix Automaton for advanced string structures.
- **Graph Theory:** Breadth-First Search (BFS), Depth-First Search (DFS), Shortest Paths (Dijkstra, Bellman-Ford, Floyd-Warshall), Minimum Spanning Trees (Kruskal, Prim), Strongly Connected Components (Tarjan, Kosaraju), and Flow Networks (Dinic's Algorithm, Push-Relabel).
- **Geometry:** Convex Hull (Graham Scan, Monotone Chain), Line Intersections, Polygon Area, and Half-plane intersections.

For each topic, CP-Algorithms provides a strong mathematical and theoretical foundation, rigorous time and space complexity analysis, edge-case considerations, and highly optimized implementation details. 

### 1.2. Utilizing CP-Algorithms as a Python Programmer
A unique challenge for Python programmers using CP-Algorithms is that **almost all implementation examples are written in C++**. The C++ implementations are often highly stylized, using bitwise operations, pointer arithmetic, and compiler-specific macros. To use CP-Algorithms effectively, you must learn to "read C++ and write Python."

When translating C++ CP concepts to Python, consider the following critical adaptations and hidden pitfalls:

**1. Translating Arrays, Pointers, and Memory Layouts**
C++ code heavily relies on static arrays and contiguous memory blocks. In Python, these translate to dynamic lists which are arrays of object references. Pre-allocating lists using `[0] * N` is crucial for performance. Never use `.append()` iteratively in a tight loop when the size of the array is known beforehand. This is especially true for implementing structures like Segment Trees, where an array of size $4N$ is required.
```python
# BAD: Dynamic reallocation overhead
tree = []
for _ in range(4 * N):
    tree.append(0)

# GOOD: Contiguous pre-allocation
tree = [0] * (4 * N)
```

**2. Handling 32-bit and 64-bit Integer Overflow**
C++ implementations meticulously manage `int` (32-bit, up to $\approx 2 \times 10^9$) and `long long` (64-bit, up to $\approx 9 \times 10^{18}$) to avoid arithmetic overflow. Python 3 seamlessly handles arbitrarily large integers, abstracting away the bit-width limitations. While this frees you from frustrating overflow bugs (e.g., when multiplying two large modulo results), it introduces a hidden algorithmic overhead. Exceedingly large integer operations in Python take $O(L^2)$ time (where $L$ is the number of digits) rather than $O(1)$. In modular arithmetic problems (like calculating $A^B \pmod M$), you must still rigorously take the modulo at every intermediate step (`a = (a * b) % M`) to keep the integer sizes small and the operations operating in true $O(1)$ time.

**3. Data Structure Equivalents and Polyfills**
- `std::vector` $\rightarrow$ Python `list`.
- `std::set` $\rightarrow$ Python `set` (which is Hash-based). Note that C++ `set` is a Red-Black Tree, maintaining elements in sorted order. Python lacks a built-in balanced Binary Search Tree. If you need ordered set functionality, you must either use the `bisect` module over a sorted list (if insertions are rare), or implement a custom Fenwick tree / Treap.
- `std::priority_queue` $\rightarrow$ Python's `heapq` module.
- `std::deque` $\rightarrow$ Python's `collections.deque`.
- `std::pair` and `std::tuple` $\rightarrow$ Python tuples `(a, b)`.

### 1.3. Recommended Study Path
If you are new to competitive algorithms, do not read CP-Algorithms linearly from top to bottom. It is far too dense. Start with the fundamental building blocks that appear in 80% of contest problems:
1. **Algebra:** Sieve of Eratosthenes, Binary Exponentiation (fast power), and Greatest Common Divisor (Euclidean algorithm).
2. **Graphs:** Graph representation (Adjacency Lists using lists of lists), DFS, BFS, Dijkstra's Algorithm, and Disjoint Set Union (DSU) with path compression and union by rank.
3. **Data Structures:** Segment Tree (point update, range query), and Fenwick Tree.

---

## 2. CSES Problem Set: The Standard Task Library

The [CSES Problem Set](https://cses.fi/problemset/) (Code Submission Evaluation System), maintained by the University of Helsinki and authored by Antti Laaksonen (author of the excellent "Competitive Programmer's Handbook"), is a beautifully curated collection of around 300 classic competitive programming problems. 

### 2.1. The Value of CSES
Unlike Codeforces or AtCoder problems, which often shroud the underlying algorithm in complex stories, ad-hoc observations, and tricky edge cases, the CSES problem set is designed to test your bare-metal knowledge of standard algorithms. If you want to know "Do I actually know how to implement a Range Minimum Query Segment Tree correctly without bugs?", CSES has a problem that asks you to do exactly that, and nothing more. It serves as the perfect proving ground for testing and refining the implementations you learn from CP-Algorithms or the USACO Guide.

The categories progress highly logically:
- **Introductory Problems:** Basic recursion, bit strings, gray codes, and math.
- **Sorting and Searching:** Binary search, two pointers, sliding windows, and coordinate compression.
- **Dynamic Programming:** Knapsack variants, Longest Increasing Subsequence, coin change, and path counting.
- **Graph Algorithms:** Shortest paths, spanning trees, topological sorting, Eulerian circuits.
- **Range Queries:** Fenwick trees, Segment trees, Lazy propagation.
- **Tree Algorithms:** Tree diameter, lowest common ancestor (LCA), subtree queries.
- **Mathematics:** Combinatorics, modular exponentiation, game theory (Nim).
- **String Algorithms:** Hashing, Trie, Suffix arrays.
- **Geometry:** Polygon processing, sweeps.
- **Advanced Techniques:** Meet in the middle, CDQ divide and conquer.

### 2.2. Approaching CSES in Python
CSES is notorious for its extremely strict time limits (usually 1.00s for an input size of $N=2 \cdot 10^5$). While C++ solutions can pass with suboptimal implementations (e.g., $O(N \log^2 N)$ when $O(N \log N)$ is expected), Python solutions must be highly optimized, both algorithmically and practically.

**1. Fast I/O is Absolutely Mandatory**
Python's built-in `input()` function is heavily buffered, strips trailing newlines, and is extremely slow for large inputs. If a problem requires reading an array of $2 \times 10^5$ integers, using `input().split()` in a loop will cause a TLE before the algorithm even begins. You must replace them with `sys.stdin.read` and `sys.stdout.write`.

```python
import sys

def solve():
    # Read all input from standard input as a single string, then split into a list of tokens
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # input_data is now an iterator-like list of strings
    # Parsing becomes highly efficient
    n = int(input_data[0])
    arr = [int(x) for x in input_data[1:n+1]]
    
    # Algorithm execution...
    result = sum(arr)
    
    # Fast output (must be cast to string)
    sys.stdout.write(str(result) + "\\n")

if __name__ == '__main__':
    solve()
```

**2. The Recursion Limit Trap**
Many graph problems on CSES (like Tree Traversals, finding connected components, or Kosaraju's SCC algorithm) require Deep Depth First Search (DFS). Python's default recursion depth is conservatively set to around 1,000 to prevent C stack overflows. For a graph with $10^5$ vertices, a straight-line graph will immediately trigger a `RecursionError`.

You must explicitly increase the recursion limit at the top of your file:
```python
import sys
# Set recursion limit high enough for CSES graph problems
sys.setrecursionlimit(1 << 20)
```
*Note on System Architecture:* Increasing the recursion limit tells the Python interpreter to allow deeper calls, but it does not magically grant the OS process more thread stack memory. On some platforms (like Codeforces), a deep recursion can still result in Memory-Limit-Exceeded (MLE) or Segmentation Faults. In extreme cases, you must learn to simulate the recursion iteratively using an explicit stack (a `while` loop with a `list`), though this is rarely required on CSES.

**3. PyPy3 over CPython3**
Whenever a platform offers PyPy3, you must select it. PyPy is an alternative implementation of Python that uses a Just-In-Time (JIT) compiler. Instead of interpreting bytecode instruction by instruction, PyPy compiles frequently executed code paths into highly optimized machine code at runtime. It is consistently 3x to 10x faster than standard CPython for loops, integer arithmetic, and heavy array manipulation—exactly the workloads found in CP. CSES fully supports PyPy3, and it is highly recommended you use it to avoid TLE verdicts.

---

## 3. Project Euler: The Intersection of Math and Code

[Project Euler](https://projecteuler.net/) offers a radically different flavor of problem-solving. Instead of typical algorithmic puzzles involving graphs, queries, or string manipulation, Project Euler focuses heavily on pure mathematics, number theory, advanced combinatorics, and computational efficiency. 

### 3.1. The Project Euler Paradigm
A typical Project Euler problem presents a deceptively simple mathematical premise and asks for the solution to a massive instance of that premise. For example, Problem 1 asks for the sum of all multiples of 3 or 5 below 1000. Problem 10 asks for the sum of all primes below two million. 

The problems are designed with a specific philosophy: a naive brute-force approach might take years of CPU time to execute, but with profound mathematical insight, algebraic manipulation, and an efficient algorithm, the solution can compute in under a second. The platform operates on a "submit the answer" basis rather than a "submit the code" basis, meaning execution time is bounded only by your own patience.

### 3.2. Why Python Dominates Project Euler
While C++ is the king of standard IOI-style competitive programming, Python is undeniably the king of Project Euler. The reasons are intrinsic to the language's design:

**1. Arbitrary-Precision Arithmetic (Bignum)**
A vast number of Project Euler problems require calculating extremely large numbers (e.g., $1000!$, or the sum of the digits of $2^{10000}$). In C++, Java, or Rust, you would need to manually implement a BigInteger class (handling string-based arithmetic) or rely on external libraries like GMP. In Python, large integers are a native built-in primitive. You can calculate `2**10000` instantaneously without a second thought. Python handles the transition from 32-bit registers to dynamically allocated arrays of digits in C seamlessly under the hood.

**2. The `math` and `itertools` Standard Libraries**
Python's standard libraries feel almost explicitly tailored for Project Euler challenges.
- `math.gcd()`, `math.lcm()`, `math.isqrt()` (integer square root), `math.comb()` (binomial coefficients), and `math.factorial()` handle heavy mathematical lifting natively in optimized C code.
- `itertools.permutations()`, `itertools.combinations()`, `itertools.product()`, and `itertools.count()` make generating and exploring vast combinatorial spaces mathematically elegant and memory-efficient via generators.
- `fractions.Fraction` allows for exact rational number arithmetic, bypassing catastrophic floating-point inaccuracies.

### 3.3. Training with Project Euler
Project Euler is not the best resource if your goal is to master Graph Theory or Range Queries. However, it is **unmatched** for mastering Number Theory and Mathematics.

Key theoretical topics to master via Project Euler:
- **Prime Number Theory:** Sieve of Eratosthenes, Segmented Sieves, Prime Factorization (Pollard's rho algorithm), Primality Testing (Miller-Rabin).
- **Modular Arithmetic:** Euler's Totient Function ($\phi$), Modular Multiplicative Inverse, Chinese Remainder Theorem (CRT), and Fermat's Little Theorem.
- **Diophantine Equations:** Linear Diophantine equations, Pell's Equation, and continued fractions.
- **Dynamic Programming on Digits:** Counting numbers with specific digit properties up to $10^{18}$.

---

## 4. USACO Guide: The Structured Roadmap

The [USACO Guide](https://usaco.guide/) (USA Computing Olympiad Guide) is a relatively modern addition to the CP ecosystem, but it is unequivocally the finest structured, open-source curriculum available today. Created by top competitive programmers (including IOI gold medalists and ICPC world finalists), it provides a comprehensive roadmap taking a student from complete beginner to IOI-level mastery.

### 4.1. Structure of the USACO Guide
The guide is divided into tiers matching the official USACO contest divisions. Each module contains readings, interactive implementations, and curated problem sets from various platforms (USACO, Codeforces, CSES).

1. **Bronze (Complete Beginner):** Complete search (brute force), basic greedy algorithms, simulation, basic sorting, and basic data structures (sets, dictionaries).
2. **Silver (Intermediate):** Prefix sums, two pointers, sliding window, binary search (specifically, binary searching the answer), Depth-First Search (DFS) and Flood Fill on grids, basic tree traversals.
3. **Gold (Advanced):** Shortest paths (Dijkstra, Bellman-Ford), Disjoint Set Union (DSU), Minimum Spanning Trees (MST), advanced dynamic programming (Bitmask DP, Knapsack DP), string hashing, and basic range query structures (Fenwick Trees, Segment Trees).
4. **Platinum (Olympiad/Camp Level):** Advanced trees (Heavy-Light Decomposition, Centroid Decomposition), advanced data structures (Persistent Segment Trees, 2D Segment Trees), advanced string algorithms (Suffix Arrays), and DP optimizations (Convex Hull Trick, Divide and Conquer DP).

### 4.2. Navigating the USACO Guide with Python
The USACO Guide officially supports C++, Java, and Python. For most modules, especially in Bronze and Silver, it provides excellent code snippets and solution walk-throughs natively in Python.

However, as you reach the **Gold and Platinum** divisions, using Python becomes exceedingly difficult. The USACO judging servers often have tight time limits that do not afford enough leniency to interpreted languages, even when the algorithm's time complexity is perfectly optimal. In USACO Gold, an $O(N \log N)$ algorithm in PyPy might pass, while an $O(N \log^2 N)$ algorithm will certainly TLE, whereas a C++ solution might pass with both.

If your ultimate goal is to make the USACO Platinum division or the US IOI Camp, you will likely need to transition to C++. However, for Bronze and Silver, Python is a massive strategic advantage due to its development speed, rapid debugging, and syntactic sugar.

**USACO Python Survival Tactics:**
- **Grid Representations (2D Arrays):** USACO problems heavily feature 2D grids (representing pastures, farms, etc.). Initialize them carefully. Never do `grid = [[0] * M] * N`. This creates $N$ references to the *same* inner list. If you modify `grid[0][0]`, you modify `grid[1][0]`, `grid[2][0]`, etc. Always initialize via list comprehension: `grid = [[0 for _ in range(M)] for _ in range(N)]`.
- **Custom Hashing and Hash Collisions:** In competitive programming, malicious anti-hash test cases are sometimes generated by problem setters to induce worst-case $O(N)$ lookup times in hash maps. While Python 3's `dict` uses a randomized hash seed per process (preventing targeted cross-process attacks), deterministic hash collisions can still theoretically cause TLE. If you use tuples as dictionary keys, be aware of the hashing overhead.
- **Memory Management:** Python objects have significant memory overhead. A list of $10^6$ integers in C++ takes exactly 4MB. In Python, a list of $10^6$ integer objects takes roughly 8MB for the array of pointers, plus 28 bytes for every integer object, totaling over 36MB. In memory-tight USACO problems (256MB limit), storing multiple large lists or deep objects can trigger an MLE.

---

## 5. Developing an Olympiad-Level Python Toolkit

To consistently succeed at olympiad-level programming using Python, you must build mental muscle memory around a core set of Python paradigms and standard libraries. You must write code that is not just correct, but *pythonically optimal*.

### 5.1. The `collections` Module
- **`deque` (Double-Ended Queue):** Never use `list.pop(0)` for a queue (e.g., in Breadth-First Search). Removing from the front of a standard Python list takes $O(N)$ time because all subsequent elements must shift left in memory. `collections.deque` is implemented as a doubly-linked list under the hood, providing true $O(1)$ `append()` and `popleft()` operations.
- **`Counter`:** A heavily optimized dictionary subclass for counting hashable objects. `freq = Counter(arr)` takes $O(N)$ time in C and is incredibly useful for frequency arrays, anagram checking, and combinatorics.
- **`defaultdict`:** Absolutely essential for graph representation. `adj = defaultdict(list)` allows you to do `adj[u].append(v)` without having to explicitly check if `u` exists in the dictionary and initializing an empty list for every node.

### 5.2. The `heapq` Module
Python does not have a generalized `PriorityQueue` class suitable for fast CP (the `queue.PriorityQueue` module is thread-safe and incredibly slow due to mutex locking overhead). Instead, you must use the `heapq` module, which provides functions that operate directly on standard lists, maintaining the heap invariant.
- `heapq.heappush(heap, item)`: $O(\log N)$ insertion.
- `heapq.heappop(heap)`: $O(\log N)$ extraction of the smallest element.
- `heapq.heapify(list)`: Transforms an unsorted list into a valid heap in $O(N)$ time (much faster than pushing elements one by one).

*Crucial Note:* `heapq` only implements a **Min-Heap**. To simulate a Max-Heap with numerical values, you must invert the values by multiplying them by `-1` before pushing, and multiplying by `-1` again after popping. For objects, you may need to define custom `__lt__` methods.

### 5.3. Binary Search with `bisect`
Writing custom binary search loops is notoriously prone to off-by-one errors and infinite loops. Python's `bisect` module implements binary search flawlessly and highly efficiently in C.
- `bisect.bisect_left(arr, x)`: Returns the index of the first element $\ge x$.
- `bisect.bisect_right(arr, x)`: Returns the index of the first element $> x$.

These are the direct, highly optimized equivalents of C++'s `std::lower_bound` and `std::upper_bound`.

### 5.4. Advanced Output Formatting and String Construction
Sometimes you need to print massive arrays separated by spaces.
Instead of an iterative loop:
```python
# SLOW: Triggers I/O interrupts N times
for x in arr:
    print(x, end=" ")
print()
```
Use string joining for significantly better performance (as it constructs a single string in memory and minimizes I/O syscalls):
```python
sys.stdout.write(" ".join(map(str, arr)) + "\\n")
```
Alternatively, using the asterisk operator with fast `print` (if `print` is not overridden, or if using PyPy):
```python
print(*arr)
```
String concatenation using `+=` inside a loop can also be slow ($O(N^2)$ in worst cases historically, though optimized in modern Python). Always prefer `.join()` for building large strings from parts.

### 5.5. Decorators for Memoization (Dynamic Programming)
Python makes top-down Dynamic Programming (Memoization) incredibly elegant via decorators. Instead of manually maintaining a 2D or 3D memoization array, passing state variables, and checking for `-1` unvisited flags, you can use:

```python
from functools import lru_cache
import sys

sys.setrecursionlimit(200000)

# Memoizes the function return values based on arguments
@lru_cache(maxsize=None)
def dp(i, w):
    if i == 0 or w == 0:
        return 0
    if weights[i-1] <= w:
        return max(values[i-1] + dp(i-1, w-weights[i-1]), dp(i-1, w))
    else:
        return dp(i-1, w)
```
In Python 3.9+, you can use `@cache`, which is synonymous with `@lru_cache(maxsize=None)` but slightly faster as it skips the size limitation logic.

*Extreme Warning:* While `@cache` is beautiful and saves development time, the function call overhead in Python is significant. Furthermore, dictionary-based memoization consumes a massive amount of memory compared to a flat 1D or 2D array. For problems with tight time/memory limits, **Bottom-Up Iterative DP** (using a simple 1D or 2D list) is always faster and more memory-efficient than Top-Down Recursive DP in Python.

---

## 6. Training Methodology: A Blueprint for Mastery

If you aspire to reach expert tiers (e.g., Codeforces Candidate Master, USACO Gold, Google Code Jam/Kickstart top percentiles) using Python, follow this structured roadmap:

### Phase 1: Syntax, Primitives, and Speed
- **Goal:** Become absolutely fluent in Python's standard library. Never write a manual loop for something `bisect`, `Counter`, or `heapq` can do. Master list comprehensions.
- **Resource:** Hackerrank, LeetCode (Easy/Medium), Codeforces (Div 3 A & B).
- **Milestone:** You can implement a BFS graph traversal or binary search bug-free in under 3 minutes.

### Phase 2: Algorithm Fundamentals and Identification
- **Goal:** Understand standard algorithms and data structures without looking at reference code. Learn to read a problem statement and immediately identify the required algorithmic paradigm.
- **Resource:** USACO Guide (Bronze & Silver), CSES Problem Set (first 75 problems).
- **Focus:** Prefix Sums, Coordinate Compression, Two Pointers, Binary Search on Answer, Basic Graph Traversals (Connected Components, Flood Fill), standard Dynamic Programming (Knapsack, LIS, LCS).

### Phase 3: Advanced Data Structures, Range Queries, and Math
- **Goal:** Tackle complex range queries, tree algorithms, and number theory.
- **Resource:** CP-Algorithms, CSES Problem Set (Range Queries & Tree Algorithms), Project Euler.
- **Focus:** Segment Trees (Iterative implementations are vastly faster in Python than recursive ones), Fenwick Trees, Sieve of Eratosthenes, Modulo Arithmetic, DSU with Path Compression, Tree Diameter and Lowest Common Ancestor (LCA).

### Phase 4: Competitive Simulation and Proofs
- **Goal:** Perform flawlessly under intense time pressure.
- **Resource:** Codeforces (Div 2 and Div 3 virtual contests), AtCoder Beginner Contests (ABC).
- **Focus:** Virtual contests. Speed matters. Learn to quickly identify whether a problem is Greedy, DP, or Graph-based. More importantly, train yourself to formulate a rigorous mathematical proof of correctness (or convincing intuition) before typing a single line of Python. Debugging logical errors during a contest is devastating to your rank.

## Conclusion

Engaging in competitive programming using Python is a deeply rewarding intellectual endeavor. While the language imposes strict performance and architectural limitations that C++ programmers do not typically face, overcoming these very limitations forces you to write cleaner, algorithmically superior, and more deeply optimized code. By systematically leveraging the rigorous theoretical depth of **CP-Algorithms**, the standard implementation testing of **CSES**, the profound mathematical exploration of **Project Euler**, and the highly structured, competitive curriculum of the **USACO Guide**, you can build a formidable algorithmic toolkit. This toolkit will not only allow you to dominate coding interviews but will also render you capable of tackling the hardest algorithmic olympiad challenges in the world.
"""

# Define the absolute path for the target file
target_path = r"d:\work\python-all\12-Resources-References\02-External-Resources\03-cp-sites.md"

# Ensure the directory exists
os.makedirs(os.path.dirname(target_path), exist_ok=True)

# Write the content to the file
with open(target_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Successfully generated and wrote {len(markdown_content)} characters to {target_path}.")
