r"""
# Big O Notation & Asymptotic Analysis: Complete Pedagogical Reference

## A. Concept Name
Big O Notation and Asymptotic Analysis (The Bachmann–Landau Notational Family: $O, \Omega, \Theta, o, \omega$).

## B. One-Sentence Definition
Big O notation is a formal mathematical framework that characterizes the limiting behavior and asymptotic upper bound of an algorithm's resource consumption (time or space) as input size $N$ approaches infinity, abstracting away hardware-dependent constants and lower-order terms.

## C. Why Does This Exist? (What problem does it solve?)
In software engineering, benchmarking raw execution time (wall-clock seconds) is fundamentally unreliable:
1. **Hardware Disparity**: A linear search on an overclocked 5.0 GHz AMD Ryzen CPU running an optimized C routine may beat an $O(\log N)$ binary search in interpreted Python on a vintage Raspberry Pi for small-to-medium inputs. Wall-clock timing benchmarks the machine, not the algorithm.
2. **The Scalability Trap**: An algorithm with an enormous constant factor (e.g., $10^6 N$) outperforms an $O(N^2)$ algorithm when $N < 10^6$, but catastrophic divergence occurs when $N = 10^9$. Production systems fail when data scales beyond initial benchmarks unless asymptotic complexity is known.
3. **Input Scaling Invariance**: Engineers need to predict how latency scales when traffic doubles, 10x-es, or 1,000x-es. Big O provides exact scaling multipliers (e.g., doubling $N$ in an $O(N^2)$ routine quadruples latency, whereas in an $O(N)$ routine it only doubles latency).
4. **Defensive Engineering & SLA Guarantees**: Knowing upper bounds ($O$) prevents Algorithmic Complexity Denial-of-Service attacks (HashDoS), where adversaries construct worst-case inputs to push $O(1)$ average-case systems into $O(N^2)$ stalls.

## D. Intuition & Real-Life Analogy
- **Transportation Scaling**:
  - $O(1)$ [Constant]: Walking to your driveway to get in your car. Time is invariant to travel distance.
  - $O(\log N)$ [Logarithmic]: Navigating a phone book with thumb tabs. Each split discards half the remaining names.
  - $O(N)$ [Linear]: Reading a book cover to cover. Doubling the page count doubles reading time.
  - $O(N \log N)$ [Linearithmic]: Sorting a deck of cards using divide-and-conquer piles.
  - $O(N^2)$ [Quadratic]: Every guest at an $N$-person party shaking hands with every other guest ($N(N-1)/2$ handshakes).
  - $O(2^N)$ [Exponential]: Cracking an $N$-digit binary combination padlock by brute-forcing every subset of switches ($2^N$ states).
  - $O(N!)$ [Factorial]: The Traveling Salesperson visiting $N$ cities by enumerating all possible permutations.

## E. Mental Model
Imagine observing the graph of an algorithm's step count through a telescope focused on the infinite horizon ($N \to \infty$):
```text
Operations
  ^
  |                                                  .. O(N!)
  |                                              ..  .  O(2^N)
  |                                          ..     .
  |                                      ..         .  O(N^2)
  |                                  ..             .
  |                             ..                  .  O(N log N)
  |                        ...                      .
  |                  ..''                           .  O(N)
  |            ...'''                               .
  |     ..''''                                      .  O(log N)
  |  -----------------------------------------------.  O(1)
  +----------------------------------------------------> Input Size (N)
```
As $N$ expands toward infinity, lower-order terms shrink to mathematical insignificance. In $f(N) = 3N^2 + 500N + 1,000,000$, when $N = 10^8$:
- $3N^2 = 3 \times 10^{16}$ (99.998% of total operations)
- $500N = 5 \times 10^{10}$ (0.00016%)
- $1,000,000 = 10^6$ (0.000000003%)
Hence, the highest-order term dictates the computational destiny of the system.

## F. Formal Technical Explanation
Asymptotic analysis classifies functions according to their rates of growth using five classical Bachmann–Landau notations:

1. **Big O (Asymptotic Upper Bound - Worst-Case Envelope)**:
   $$f(N) \in O(g(N)) \iff \exists\, c > 0, N_0 > 0 \quad \text{such that} \quad 0 \le f(N) \le c \cdot g(N), \quad \forall N \ge N_0$$
   Meaning: Beyond threshold $N_0$, $f(N)$ will never grow faster than $c \cdot g(N)$.

2. **Big Omega ($\Omega$) (Asymptotic Lower Bound - Best-Case Floor)**:
   $$f(N) \in \Omega(g(N)) \iff \exists\, c > 0, N_0 > 0 \quad \text{such that} \quad 0 \le c \cdot g(N) \le f(N), \quad \forall N \ge N_0$$
   Meaning: Beyond $N_0$, the algorithm requires at least $c \cdot g(N)$ operations.

3. **Big Theta ($\Theta$) (Asymptotically Tight Bound)**:
   $$f(N) \in \Theta(g(N)) \iff f(N) \in O(g(N)) \quad \text{and} \quad f(N) \in \Omega(g(N))$$
   $$\exists\, c_1 > 0, c_2 > 0, N_0 > 0 \quad \text{such that} \quad c_1 \cdot g(N) \le f(N) \le c_2 \cdot g(N), \quad \forall N \ge N_0$$
   Meaning: $f(N)$ is sandwiched tightly between $c_1 g(N)$ and $c_2 g(N)$.

4. **Little o ($o$) (Strict Upper Bound)**:
   $$f(N) \in o(g(N)) \iff \lim_{N \to \infty} \frac{f(N)}{g(N)} = 0$$

5. **Little omega ($\omega$) (Strict Lower Bound)**:
   $$f(N) \in \omega(g(N)) \iff \lim_{N \to \infty} \frac{f(N)}{g(N)} = \infty$$

## G. Mathematical Foundation
1. **Summation Identities for Code Analysis**:
   - Arithmetic Series (Single nested loop dependent on outer):
     $$\sum_{i=1}^N i = \frac{N(N + 1)}{2} = \frac{1}{2}N^2 + \frac{1}{2}N \in \Theta(N^2)$$
   - Geometric Series (Doubling/Halving loop or heap tree levels):
     $$\sum_{i=0}^{k} 2^i = 2^{k+1} - 1 \implies \text{When } k = \log_2 N: \sum_{i=0}^{\log_2 N} 2^i = 2N - 1 \in \Theta(N)$$
   - Harmonic Series (Inner loop step $N/i$):
     $$\sum_{i=1}^N \frac{1}{i} = \ln N + \gamma + O\left(\frac{1}{N}\right) \in \Theta(\log N)$$
     *(Appears in Sieve of Eratosthenes analysis: $\sum_{p \le N} \frac{N}{p} \in O(N \log \log N)$).*

2. **Master Theorem for Divide-and-Conquer Recurrences**:
   For recurrences of the form $T(N) = a T(N/b) + f(N)$, with $a \ge 1, b > 1$:
   - **Case 1**: If $f(N) \in O(N^{\log_b a - \epsilon})$ for some $\epsilon > 0$, then $T(N) \in \Theta(N^{\log_b a})$.
   - **Case 2**: If $f(N) \in \Theta(N^{\log_b a} \log^k N)$ for $k \ge 0$, then $T(N) \in \Theta(N^{\log_b a} \log^{k+1} N)$.
     *(Example: Merge Sort: $T(N) = 2T(N/2) + O(N) \implies a=2, b=2, \log_2 2 = 1 \implies T(N) \in \Theta(N \log N)$).*
   - **Case 3**: If $f(N) \in \Omega(N^{\log_b a + \epsilon})$ and regularity condition holds ($a f(N/b) \le c f(N)$), then $T(N) \in \Theta(f(N))$.

3. **Stirling's Approximation (Comparison Sort Lower Bound)**:
   $$N! \approx \sqrt{2 \pi N} \left(\frac{N}{e}\right)^N \implies \log_2(N!) \in \Theta(N \log N)$$
   Since any comparison-based sort corresponds to a binary decision tree with $N!$ leaves, the minimum height is $\lceil \log_2(N!) \rceil = \Omega(N \log N)$.

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**: Quantifies CPU cycles and primitive operations (comparisons, arithmetic, variable assignments, memory dereferences) as a function of input size $N$.
- **Auxiliary Space vs. Total Space**:
  - Total Space = Input Space + Auxiliary Space.
  - Auxiliary space measures only the *additional* memory allocated by the algorithm during its execution (excluding the input data itself).
  - An algorithm is called *in-place* if its auxiliary space is $O(1)$ (or $O(\log N)$ for recursion stack frames).
- **Call Stack Overhead**: Every recursive invocation allocates a stack frame storing local variables, parameters, and return addresses. Recursive depth $D$ creates $O(D)$ auxiliary space.
- **Python-Specific Memory Overhead**:
  - Python integers are arbitrary-precision objects (`sys.getsizeof(0)` $\approx 28$ bytes).
  - Python `list` is an over-allocated array of pointers ($8$ bytes per pointer on 64-bit OS), expanding with an amortization ratio of $\approx 1.125 \times + 6$.

## I. Common Mistakes & Pitfalls
1. **Conflating Big O with Worst Case**:
   Big O is an *upper bound*, NOT a synonym for worst case! An algorithm has a best-case, an average-case, and a worst-case. Each case has its own Big O, Big Omega, and Big Theta.
   *Example*: QuickSort's best-case time is $\Theta(N \log N)$ and $O(N \log N)$. Its worst-case time is $\Theta(N^2)$ and $O(N^2)$.
2. **Dropping Variables in Multi-Input Problems**:
   Searching an $M \times N$ matrix is $O(M \cdot N)$, not $O(N^2)$. Breadth-First Search on a graph $(V, E)$ is $O(V + E)$, not $O(V)$ or $O(E)$.
3. **Hidden High-Level Language Costs**:
   - `val in python_list` is $O(N)$, not $O(1)$.
   - `python_list.pop(0)` is $O(N)$ (requires memory shift of all elements).
   - String concatenation in a loop (`s += char`) is $O(N^2)$ due to string immutability requiring a full copy of string $s$ at each step.
   - `list(set(arr))` takes $O(N)$ time and $O(N)$ space.
4. **Ignoring Small-$N$ Constant Factors**:
   Strassen's matrix multiplication ($O(N^{2.807})$) has a constant factor so massive that standard $O(N^3)$ multiplication is faster for $N \le 500-1000$.
5. **Miscalculating Sliced Iterations**:
   In Python, `arr[a:b]` creates a *shallow copy* in $O(b - a)$ time and space. Doing `foo(arr[1:])` recursively creates an $O(N^2)$ time disaster!

## J. Common Confusions
- **$O(1)$ vs. "Instantaneous"**: $O(1)$ means the runtime is independent of $N$. An $O(1)$ operation can take 10 picoseconds (bitwise AND) or 5 minutes (a fixed 10-million-iteration cryptographic hash).
- **$O(\log N)$ vs. Base of Logarithm**: By the change of base formula, $\log_b N = \frac{\log_a N}{\log_a b}$. Because $\frac{1}{\log_a b}$ is a constant, all logarithmic bases belong to the same complexity class: $O(\log_2 N) = O(\log_{10} N) = O(\ln N)$.
- **Amortized Time vs. Average Time**: Average time assumes a probability distribution over possible inputs. Amortized time guarantees an average cost over a guaranteed sequence of operations in the *worst case* (e.g., dynamic array appends).

## K. When To Use It
- Conducting architectural design reviews to choose database indexes, search structures, and caching layers.
- Formulating performance budgets and capacity planning models for microservices.
- Identifying and eliminating asymptotic bottlenecks during code reviews.
- Formally defending algorithmic choices in technical whitepapers and technical interviews.

## L. When NOT To Use It
- Micro-optimizing code when $N$ is strictly bounded and small ($N \le 32$). Here, CPU cache line alignment, branch predictor accuracy, SIMD vectorization, and instruction-level parallelism dominate.
- Real-time hard embedded systems (e.g., flight control, pacemaker firmware) where worst-case execution time (WCET) must be measured in absolute CPU clock cycles, not asymptotic limits.

## M. Trade-offs
| Complexity Class | Growth Multiplier ($2 \times N$) | Scalability Limit ($10^9$ ops/sec CPU) | Practical Domain |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | $1 \times$ (Zero change) | $N = \infty$ (Instant) | Hash lookups, array indexing, stack push/pop |
| **$O(\log N)$** | $+1$ operation step | $N = 10^{18}$ (Essentially infinite) | Binary search, balanced BSTs, skip lists |
| **$O(N)$** | $2 \times$ | $N = 10^8 - 10^9$ ($\approx 1$ sec) | Linear scan, counting sort, two-pointer sweeps |
| **$O(N \log N)$** | $\approx 2 \times$ | $N = 10^7 - 10^8$ ($\approx 2$ sec) | Merge sort, Timsort, QuickSort, FFT |
| **$O(N^2)$** | $4 \times$ | $N \approx 30,000$ ($\approx 1$ sec) | Nested comparison loops, bubble sort, pairwise distance |
| **$O(N^3)$** | $8 \times$ | $N \approx 1,000$ ($\approx 1$ sec) | Floyd-Warshall, naive matrix multiplication |
| **$O(2^N)$** | Squared ($T \to T^2$) | $N \approx 30$ ($\approx 1$ sec) | Power sets, naive recursive backtracking |
| **$O(N!)$** | $\times (N+1)$ | $N \approx 12$ ($\approx 0.5$ sec) | Traveling Salesperson, all permutations |

## N. Debugging Tips
1. **The Doubling Hypothesis**: Run your code on input size $N$, then on $2N$. Measure the ratio $R = T(2N) / T(N)$:
   - If $R \approx 1 \implies O(\log N)$ or $O(1)$
   - If $R \approx 2 \implies O(N)$
   - If $R \approx 4 \implies O(N^2)$
   - If $R \approx 8 \implies O(N^3)$
   - If $R \ge 2^N \implies O(2^N)$
2. **Empirical Curve Fitting**: Log-log plots: Graphing $\log(T)$ vs $\log(N)$ converts polynomial growth $T = c N^k$ into a straight line with slope $k = \frac{\Delta \log T}{\Delta \log N}$.
3. **Use Profilers**: Profile with `cProfile` and sort by `cumtime` to pinpoint the inner loop executing $O(N^2)$ times.

## O. Memory Hook
**"Drop the constant, drop the low; watch the highest power grow!
Double N and check the score: two is linear, quadratic four!"**

## P. Active Recall Questions
1. Why is $O(N + \log N)$ simplified to $O(N)$, but $O(N \cdot \log N)$ cannot be simplified?
2. If an algorithm takes $f(N) = 100N^2 + 0.001N^3$ operations, at what exact threshold $N_0$ does the cubic term surpass the quadratic term?
3. What is the difference between an algorithm with $O(1)$ amortized time vs. $O(1)$ worst-case time? Give an example of each.
4. Why does Python's `s = s + char` inside an $N$-step loop result in $O(N^2)$ time, and how does `''.join(list_of_chars)` fix it?
5. True or False: If $f(N) = O(N)$, then $f(N) = O(N^2)$. Explain why using the formal mathematical definition.

## Q. Interview Questions & Answers
- **Q1: Explain the time and space complexity of appending $N$ elements to a dynamic array (like Python's `list` or C++'s `std::vector`).**
  *Answer:* Appending a single element takes $O(1)$ when space is available, but $O(N)$ when the internal array is full and must be reallocated and copied. Using geometric resizing (growth factor $g \approx 1.5 - 2.0$), the array resizes after $1, 2, 4, 8, \dots, N$ elements. The total copy operations across $N$ insertions sum to $\sum_{i=0}^{\log_2 N} 2^i = 2N - 1 < 2N$. Dividing total work by $N$ gives $\frac{2N}{N} = O(1)$ **amortized time** per append. Auxiliary space is $O(N)$ for the allocated capacity.
- **Q2: What is the difference between Big-O, Big-Omega, and Big-Theta? When an interviewer asks 'What is the Big O of this function?', what do they usually mean?**
  *Answer:* Formally, Big O ($O$) provides an asymptotic upper bound, Big Omega ($\Omega$) provides an asymptotic lower bound, and Big Theta ($\Theta$) provides a tight bound where upper and lower bounds coincide. In industry interviews, when an engineer asks for the "Big O", they almost universally mean the **tight worst-case bound** ($\Theta$ of the worst-case scenario).
- **Q3: What is the time complexity of building a binary heap from an unsorted array of $N$ elements? Naively it seems $O(N \log N)$, but is it faster?**
  *Answer:* Building a heap via bottom-up `sift_down` (Floyd's algorithm) takes $\Theta(N)$ time, not $O(N \log N)$. There are $\lceil N / 2^{h+1} \rceil$ nodes at height $h$. The total work is $\sum_{h=0}^{\lfloor \log_2 N \rfloor} \frac{N}{2^{h+1}} O(h) = \frac{N}{2} \sum_{h=0}^\infty \frac{h}{2^h}$. Since the infinite series $\sum_{h=0}^\infty \frac{h}{2^h} = 2$, the total operations evaluate to $\frac{N}{2} \times 2 = O(N)$.

## R. Project Connections
- **CPython Source**: `Objects/listobject.c` implements list over-allocation strategy: `new_allocated = (size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6);` ensuring $O(1)$ amortized append.
- **Database Indexing**: B-Tree indices provide $O(\log_B N)$ page reads, where disk fan-out $B \approx 512-1024$, keeping tree depth $\le 4$ even for billions of records.
- **Garbage Collection**: Tracing garbage collectors (like Go's or Java's CMS/G1) have time complexity proportional to the number of live pointers ($O(\text{Live})$), rather than total heap memory ($O(\text{Heap})$).

## S. Edge Cases & Boundary Conditions
1. **$N = 0$ or $N = 1$**: Asymptotic bounds describe behavior as $N \to \infty$. Boundary behavior at $N \in \{0, 1\}$ must handle divide-by-zero or empty-structure exceptions without invalidating asymptotic claims.
2. **Multiple Independent Inputs**: For two arrays of lengths $A$ and $B$, an algorithm that iterates $A$ inside $B$ is $O(A \cdot B)$. Do not reduce to $O(N^2)$ unless $A = \Theta(B)$.
3. **Worst-Case vs. Average-Case Mismatch**: Hash table lookups are $O(1)$ average, but $O(N)$ worst-case under deliberate hash collisions.
4. **Strict Integer Limits**: In languages with fixed-size 32-bit or 64-bit integers, operations might appear $O(1)$, but in arbitrary-precision arithmetic (Python's `int`), multiplying two $N$-digit numbers takes $O(N^{\log_2 3}) \approx O(N^{1.585})$ via Karatsuba.

## T. Algorithmic Growth Order Hierarchy & Taxonomy
```text
Class Name        Notation      Example Algorithm                      Scaling on 10x Input
--------------------------------------------------------------------------------------------
Constant          O(1)          Array index, Hash map get              1x (No change)
Inverse Ackermann O(alpha(N))   Disjoint Set Union (Union-Find)        Practically constant (<= 4)
Iterated Log      O(log* N)     Distributed graph coloring             Practically constant (<= 5)
Log-Log           O(log log N)  Interpolation search (uniform), vEB    Extremely slow growth
Logarithmic       O(log N)      Binary search, BST operations          +3.3 operations
Polylogarithmic   O(log^k N)    Fractional cascading, matrix rank      Modest growth
Sublinear         O(N^c), c<1   Jump search (O(sqrt(N)))               sqrt(10)x (~3.16x)
Linear            O(N)          Linear scan, Kadane's algorithm        10x
Linearithmic      O(N log N)    Merge sort, QuickSort (avg), FFT       ~13.3x
Quadratic         O(N^2)        Bubble sort, nested pairwise loop      100x
Cubic             O(N^3)        Naive matrix multiplication            1,000x
Polynomial        O(N^k)        Gaussian elimination (O(N^3))          10^k x
Exponential       O(2^N)        Subset generation, 0/1 knapsack brute  2^(10)x = 1,024x
Factorial         O(N!)         Traveling Salesperson brute force      >> 10^6 x
```

## U. Algorithmic Complexity Comparison Table
| Operation / Algorithm | Best Case | Average Case | Worst Case | Auxiliary Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Array Indexing** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ | N/A |
| **Linear Search** | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ | N/A |
| **Binary Search** | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ | N/A |
| **Hash Map Lookup**| $O(1)$ | $O(1)$ | $O(N)$ | $O(N)$ | N/A |
| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |
| **Merge Sort**     | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes |
| **QuickSort**      | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | No |
| **Heap Sort**      | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No |
| **Timsort**       | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes |

## V. Practical Implementation Exercises
1. Implement an automated **Doubling Ratio Tester** that executes a callable function on exponentially increasing sizes of $N$ and estimates the polynomial power $k$.
2. Implement a step-counting **Dynamic Array** that logs every pointer write and relocation to prove that amortized append is strictly $< 3$ operations per element.
3. Construct a benchmark demonstrating how Python's `''.join()` is $O(N)$ while naive `+=` string concatenation behaves as $O(N^2)$ for large $N$.

## W. Step-by-Step Execution Trace
Theoretical operation counts across common complexity classes for various $N$:
```text
+-----------+--------+------------+----------+--------------+------------+-------------+
|     N     |  O(1)  |  O(log2 N) |   O(N)   |  O(N log2 N) |   O(N^2)   |    O(2^N)   |
+-----------+--------+------------+----------+--------------+------------+-------------+
| 1         |   1    |     0      |    1     |      0       |     1      |      2      |
| 10        |   1    |     3.3    |    10    |     33.2     |    100     |    1,024    |
| 100       |   1    |     6.6    |   100    |     664.4    |   10,000   | 1.27 x 10^30|
| 1,000     |   1    |    10.0    |  1,000   |    9,965.8   |  1,000,000 |  Overflow   |
| 10,000    |   1    |    13.3    |  10,000  |   132,877.1  | 100,000,000|  Overflow   |
| 1,000,000 |   1    |    19.9    | 1,000,000| 19,931,568.6 |  10^12     |  Overflow   |
+-----------+--------+------------+----------+--------------+------------+-------------+
```

## X. Key Takeaways & Summary Anchor
- Big O is an upper bound on asymptotic growth, not a synonym for worst-case time.
- Always drop multiplicative constants and lower-order terms when describing asymptotic complexity.
- Beware hidden high-level costs in Python: slices copy, list `in` scans linearly, and `pop(0)` shifts elements.
- The Doubling Hypothesis ($T(2N) / T(N)$) is an empirical superpower for discovering runtime complexity in the wild.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, TypeVar
import cProfile
import math
import pstats
import time
import tracemalloc

T = TypeVar("T")


# ==============================================================================
# 1. STEP COUNTER & INSTRUMENTED COMPLEXITY CLASSES
# ==============================================================================

class StepCounter:
    """
    Deterministic step counter for algorithmic analysis.
    Tracks primitive operations (comparisons, writes, allocations) independently
    of CPU frequency and system load.
    """
    def __init__(self) -> None:
        self.count: int = 0

    def tick(self, amount: int = 1) -> None:
        """Increment the step counter by the specified number of operations."""
        self.count += amount

    def reset(self) -> None:
        """Reset the step counter to zero."""
        self.count = 0


def constant_time_demo(data: Sequence[Any], counter: Optional[StepCounter] = None) -> Any:
    """
    O(1) - Constant Time.
    Executes a fixed number of operations regardless of collection size N.
    """
    if counter:
        counter.tick(1)  # Length inspection
    if not data:
        return None
    if counter:
        counter.tick(1)  # Index dereference
    return data[0]


def logarithmic_time_demo(
    arr: Sequence[int], target: int, counter: Optional[StepCounter] = None
) -> Tuple[int, int]:
    """
    O(log N) - Logarithmic Time (Iterative Binary Search).
    Halves the search space on each iteration.
    
    Returns:
        Tuple[int, int]: (index_found, operations_count)
    """
    steps = 0
    low = 0
    high = len(arr) - 1

    while low <= high:
        steps += 1
        if counter:
            counter.tick(1)
        mid = low + (high - low) // 2
        
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, steps


def linear_time_demo(
    arr: Sequence[int], counter: Optional[StepCounter] = None
) -> Tuple[int, int]:
    """
    O(N) - Linear Time.
    Inspects each element in the sequence exactly once to find the maximum value.
    
    Returns:
        Tuple[int, int]: (max_value, operations_count)
    """
    if not arr:
        raise ValueError("Cannot find maximum of empty sequence.")

    steps = 1
    max_val = arr[0]
    if counter:
        counter.tick(1)

    for i in range(1, len(arr)):
        steps += 1
        if counter:
            counter.tick(1)
        if arr[i] > max_val:
            max_val = arr[i]

    return max_val, steps


def linearithmic_time_demo(
    arr: List[int], counter: Optional[StepCounter] = None
) -> Tuple[List[int], int]:
    """
    O(N log N) - Linearithmic Time (Merge Sort).
    Recursively divides the array into halves (log N levels) and merges them in linear time.
    
    Returns:
        Tuple[List[int], int]: (sorted_list, total_operations_count)
    """
    local_steps = [0]

    def _merge_sort(sub: List[int]) -> List[int]:
        local_steps[0] += 1
        if counter:
            counter.tick(1)
        if len(sub) <= 1:
            return sub

        mid = len(sub) // 2
        left = _merge_sort(sub[:mid])
        right = _merge_sort(sub[mid:])

        # Merge step
        merged: List[int] = []
        i = j = 0
        while i < len(left) and j < len(right):
            local_steps[0] += 1
            if counter:
                counter.tick(1)
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        while i < len(left):
            local_steps[0] += 1
            if counter:
                counter.tick(1)
            merged.append(left[i])
            i += 1

        while j < len(right):
            local_steps[0] += 1
            if counter:
                counter.tick(1)
            merged.append(right[j])
            j += 1

        return merged

    sorted_arr = _merge_sort(arr)
    return sorted_arr, local_steps[0]


def quadratic_time_demo(
    arr: Sequence[int], counter: Optional[StepCounter] = None
) -> Tuple[int, int]:
    """
    O(N^2) - Quadratic Time (All-Pairs Comparison / Handshake Problem).
    Counts how many ordered pairs (a, b) satisfy a < b.
    
    Returns:
        Tuple[int, int]: (matching_pairs_count, operations_count)
    """
    steps = 0
    n = len(arr)
    valid_pairs = 0

    for i in range(n):
        for j in range(n):
            steps += 1
            if counter:
                counter.tick(1)
            if arr[i] < arr[j]:
                valid_pairs += 1

    return valid_pairs, steps


def cubic_time_demo(
    matrix_a: List[List[int]],
    matrix_b: List[List[int]],
    counter: Optional[StepCounter] = None,
) -> Tuple[List[List[int]], int]:
    """
    O(N^3) - Cubic Time (Naive Matrix Multiplication).
    Multiplies two N x N matrices with three nested loops.
    
    Returns:
        Tuple[List[List[int]], int]: (result_matrix, operations_count)
    """
    n = len(matrix_a)
    result = [[0] * n for _ in range(n)]
    steps = 0

    for i in range(n):
        for j in range(n):
            for k in range(n):
                steps += 1
                if counter:
                    counter.tick(1)
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    return result, steps


def exponential_time_demo(
    n: int, counter: Optional[StepCounter] = None
) -> Tuple[int, int]:
    """
    O(2^N) - Exponential Time (Naive Recursive Fibonacci).
    Each call branches into two recursive calls without memoization.
    
    Returns:
        Tuple[int, int]: (fibonacci_number, recursive_calls_count)
    """
    call_count = [0]

    def _fib(k: int) -> int:
        call_count[0] += 1
        if counter:
            counter.tick(1)
        if k <= 0:
            return 0
        if k == 1:
            return 1
        return _fib(k - 1) + _fib(k - 2)

    val = _fib(n)
    return val, call_count[0]


def factorial_time_demo(
    elements: List[T], counter: Optional[StepCounter] = None
) -> Tuple[List[List[T]], int]:
    """
    O(N!) - Factorial Time (All Permutations Generator).
    Generates all N! arrangements of the given elements via backtracking.
    
    Returns:
        Tuple[List[List[T]], int]: (all_permutations, total_backtracking_steps)
    """
    steps = [0]
    result: List[List[T]] = []

    def _permute(current: List[T], remaining: List[T]) -> None:
        steps[0] += 1
        if counter:
            counter.tick(1)
        if not remaining:
            result.append(list(current))
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            _permute(current, remaining[:i] + remaining[i + 1:])
            current.pop()

    _permute([], elements)
    return result, steps[0]


# ==============================================================================
# 2. AMORTIZED COMPLEXITY DEMONSTRATION: EDUCATIONAL DYNAMIC ARRAY
# ==============================================================================

class EducationalDynamicArray:
    """
    From-scratch simulation of a dynamically resizing array (like Python's list or C++ vector).
    Demonstrates that while an occasional resize costs O(N), the amortized cost per
    append operation is strictly O(1).
    """

    def __init__(self, initial_capacity: int = 1) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.buffer: List[Optional[Any]] = [None] * self.capacity
        self.total_copy_operations: int = 0
        self.total_appends: int = 0

    def append(self, value: Any) -> int:
        """
        Appends an element. If capacity is exceeded, doubles the buffer.
        
        Returns:
            int: The number of element copies triggered by this specific append.
        """
        copies_this_append = 0
        if self.size == self.capacity:
            # Reallocation and copy required: O(N) event
            new_capacity = self.capacity * 2
            new_buffer: List[Optional[Any]] = [None] * new_capacity
            for i in range(self.size):
                new_buffer[i] = self.buffer[i]
                copies_this_append += 1
            self.buffer = new_buffer
            self.capacity = new_capacity

        self.buffer[self.size] = value
        self.size += 1
        self.total_appends += 1
        self.total_copy_operations += copies_this_append
        return copies_this_append

    @property
    def amortized_copies_per_append(self) -> float:
        """Calculates total copies divided by total appends (proves < 2.0)."""
        if self.total_appends == 0:
            return 0.0
        return self.total_copy_operations / self.total_appends


# ==============================================================================
# 3. EMPIRICAL DOUBLING HYPOTHESIS & SCIENTIFIC PROFILING
# ==============================================================================

def doubling_hypothesis_analysis(
    algorithm_fn: Callable[[List[int]], Any],
    base_n: int = 500,
    rounds: int = 5,
) -> List[Dict[str, Any]]:
    """
    Applies the Doubling Hypothesis to empirically determine the power-law exponent k.
    If T(N) = c * N^k, then T(2N) / T(N) = 2^k, so k = log2(T(2N) / T(N)).
    
    Args:
        algorithm_fn: Function to test taking a List[int] input.
        base_n: Starting input size N.
        rounds: Number of doubling rounds to conduct.
        
    Returns:
        List[Dict[str, Any]]: Table of empirical execution times, ratios, and estimated exponents.
    """
    results = []
    n = base_n
    prev_time: Optional[float] = None

    for _ in range(rounds):
        data = list(range(n, 0, -1))  # Worst-case reversed data
        
        start_time = time.perf_counter()
        algorithm_fn(data)
        elapsed = time.perf_counter() - start_time

        ratio = (elapsed / prev_time) if prev_time and prev_time > 0 else 1.0
        estimated_k = math.log2(ratio) if ratio > 0 and prev_time else 0.0

        results.append({
            "N": n,
            "ElapsedSeconds": elapsed,
            "Ratio_T2N_over_TN": ratio,
            "Estimated_Exponent_k": estimated_k,
        })

        prev_time = elapsed
        n *= 2

    return results


def profile_algorithm_memory_and_cpu(
    fn: Callable[..., Any], *args: Any, **kwargs: Any
) -> Tuple[Any, float, float]:
    """
    Standard profiling tool using Python's `tracemalloc` and `perf_counter`.
    
    Returns:
        Tuple[Any, float, float]: (function_result, elapsed_seconds, peak_memory_kb)
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    result = fn(*args, **kwargs)

    elapsed = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_kb = peak_bytes / 1024.0
    return result, elapsed, peak_kb


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DEBUGGING COMMENTARY
# ==============================================================================

def buggy_string_concatenation_quadratic(strings: List[str]) -> str:
    """
    BUGGY COMPLEXITY PATTERN #1: Accidental O(N^2) String Concatenation.
    
    In Python, strings are immutable. Using `+=` repeatedly in a loop allocates
    a completely new string buffer of size (current_length + len(s)) on each iteration,
    copying all previous characters.
    
    Diagnostic Analysis:
    - Time Complexity: O(L * N^2) where N is string count and L is average string length.
    - Resolution: Use `''.join(strings)` which pre-allocates the exact memory needed in O(N).
    """
    result = ""
    for s in strings:
        result += s  # <- BUG: Reallocates and copies entire prefix string on every step!
    return result


def fixed_string_concatenation_linear(strings: List[str]) -> str:
    """Fixed version: O(N) using Python's optimized built-in join."""
    return "".join(strings)


def buggy_membership_check_quadratic(queries: List[int], data_pool: List[int]) -> int:
    """
    BUGGY COMPLEXITY PATTERN #2: Hidden O(N * M) Linear Search Inside a Loop.
    
    Calling `x in data_pool` on a standard Python `list` executes a sequential O(M)
    linear scan. Repeating this for N queries results in O(N * M) total time!
    
    Diagnostic Analysis:
    - Failing Behavior: Stalls production when queries = 100,000 and data_pool = 100,000 (10^10 ops).
    - Resolution: Pre-convert `data_pool` to a `set` (hash table) in O(M) time, making
      each subsequent query O(1) average time, reducing total time to O(N + M).
    """
    found_count = 0
    for q in queries:
        if q in data_pool:  # <- BUG: O(M) linear scan executed N times = O(N * M)!
            found_count += 1
    return found_count


def fixed_membership_check_linear(queries: List[int], data_pool: List[int]) -> int:
    """Fixed version: O(N + M) using a HashSet lookup."""
    pool_set = set(data_pool)  # O(M) build
    return sum(1 for q in queries if q in pool_set)  # N * O(1) lookups


def buggy_queue_pop_from_front(items: List[int]) -> List[int]:
    """
    BUGGY COMPLEXITY PATTERN #3: Using List as a FIFO Queue.
    
    Calling `items.pop(0)` removes the first element, requiring Python to shift
    all remaining (N - 1) pointers in contiguous memory leftward by 8 bytes.
    Emptying an array of size N using `pop(0)` takes O(N^2) time!
    
    Diagnostic Analysis:
    - Resolution: Use `collections.deque` (a doubly linked ring-buffer of fixed-size blocks),
      which provides strictly O(1) `popleft()`.
    """
    result: List[int] = []
    temp_list = list(items)
    while temp_list:
        val = temp_list.pop(0)  # <- BUG: O(N) memory shift on every single element!
        result.append(val)
    return result


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite validating functional correctness and asymptotic bounds.
    """
    print(">>> Executing Big O & Asymptotic Analysis Test Suite...")

    # 1. Constant Time O(1) Tests
    counter = StepCounter()
    small_list = [10, 20, 30]
    large_list = list(range(100_000))
    assert constant_time_demo(small_list, counter) == 10
    steps_small = counter.count
    counter.reset()
    assert constant_time_demo(large_list, counter) == 0
    steps_large = counter.count
    assert steps_small == steps_large == 2, f"O(1) failed: {steps_small} != {steps_large}"
    assert constant_time_demo([]) is None

    # 2. Logarithmic Time O(log N) Tests
    sorted_1000 = list(range(1000))
    idx, steps = logarithmic_time_demo(sorted_1000, 500)
    assert idx == 500
    # log2(1000) ~ 9.96. Maximum comparisons in binary search is ceil(log2(N)) + 1 <= 11
    assert steps <= 11, f"O(log N) exceeded expected comparisons: {steps}"
    idx_absent, steps_absent = logarithmic_time_demo(sorted_1000, 9999)
    assert idx_absent == -1
    assert steps_absent <= 11

    # 3. Linear Time O(N) Tests
    data_100 = list(range(100))
    data_100[42] = 9999
    max_val, steps_linear = linear_time_demo(data_100)
    assert max_val == 9999
    assert steps_linear == 100, f"O(N) step count mismatch: {steps_linear} != 100"

    # 4. Linearithmic Time O(N log N) Tests (Merge Sort)
    unsorted = [64, 34, 25, 12, 22, 11, 90, 80]
    sorted_res, steps_sort = linearithmic_time_demo(unsorted)
    assert sorted_res == sorted(unsorted)
    # For N=8, N log2 N = 8 * 3 = 24. Merge sort operations bounded by c * N log N
    assert steps_sort <= 40, f"O(N log N) step count anomaly: {steps_sort}"

    # 5. Quadratic Time O(N^2) Tests
    pairs_data = [1, 5, 2, 8]  # N=4
    pairs_count, pairs_steps = quadratic_time_demo(pairs_data)
    assert pairs_steps == 16, f"Expected 4^2 = 16 operations, got {pairs_steps}"

    # 6. Cubic Time O(N^3) Tests
    mat_a = [[1, 2], [3, 4]]  # N=2
    mat_b = [[5, 6], [7, 8]]
    mat_res, cubic_steps = cubic_time_demo(mat_a, mat_b)
    assert cubic_steps == 8, f"Expected 2^3 = 8 operations, got {cubic_steps}"
    assert mat_res == [[19, 22], [43, 50]]

    # 7. Exponential Time O(2^N) Tests
    fib_res, fib_calls = exponential_time_demo(6)
    assert fib_res == 8  # Fib(6) = 8: 0, 1, 1, 2, 3, 5, 8
    # Fib(6) call count in naive recursion is 2 * Fib(7) - 1 = 2 * 13 - 1 = 25 calls
    assert fib_calls == 25, f"Expected 25 recursive calls, got {fib_calls}"

    # 8. Factorial Time O(N!) Tests
    perms, perm_steps = factorial_time_demo([1, 2, 3])  # N=3
    assert len(perms) == 6, f"Expected 3! = 6 permutations, got {len(perms)}"
    assert [1, 2, 3] in perms and [3, 2, 1] in perms

    # 9. Dynamic Array Amortized O(1) Proof
    dyn_arr = EducationalDynamicArray(initial_capacity=1)
    for i in range(1024):
        dyn_arr.append(i)
    assert dyn_arr.size == 1024
    # The sum of all copies for 1024 elements with geometric doubling is exactly 1023!
    assert dyn_arr.total_copy_operations == 1023, f"Copy sum error: {dyn_arr.total_copy_operations}"
    assert dyn_arr.amortized_copies_per_append < 1.0, "Amortized copies must be < 1.0!"

    # 10. Buggy vs Fixed Correctness & Relative Equivalence
    test_strings = ["hello", " ", "world", "!"]
    assert buggy_string_concatenation_quadratic(test_strings) == fixed_string_concatenation_linear(test_strings)

    queries = [1, 5, 99]
    pool = [5, 10, 15, 20, 1]
    assert buggy_membership_check_quadratic(queries, pool) == fixed_membership_check_linear(queries, pool)

    assert buggy_queue_pop_from_front([1, 2, 3]) == [1, 2, 3]

    print("[+] All 10 unit test suites passed successfully with exact theoretical validation!")


# ==============================================================================
# 6. MAIN EXECUTION & VISUAL EDUCATIONAL TRACE
# ==============================================================================

def main() -> None:
    """
    Main driver running unit tests and printing formatted educational complexity comparisons.
    """
    run_tests()

    print("\n" + "=" * 80)
    print("EDUCATIONAL TRACE: ASYMPTOTIC GROWTH IN ACTION")
    print("=" * 80)

    # Theoretical Operations Table
    sizes = [1, 10, 100, 1_000, 10_000]
    print(f"{'N':<8} | {'O(1)':<6} | {'O(log2 N)':<10} | {'O(N)':<8} | {'O(N log2 N)':<14} | {'O(N^2)':<12} | {'O(2^N)':<12}")
    print("-" * 80)

    for n in sizes:
        c_1 = 1
        c_log = f"{math.log2(n):.1f}" if n > 0 else "0.0"
        c_n = n
        c_nlogn = f"{n * math.log2(n):.1f}" if n > 0 else "0.0"
        c_n2 = f"{n**2:,}"
        c_2n = f"{2**n:,}" if n <= 20 else "Overflow"
        print(f"{n:<8} | {c_1:<6} | {c_log:<10} | {c_n:<8} | {c_nlogn:<14} | {c_n2:<12} | {c_2n:<12}")

    print("=" * 80)
    print("\n" + "=" * 80)
    print("EMPIRICAL DOUBLING HYPOTHESIS ANALYSIS (Quadratic Algorithm Verification)")
    print("=" * 80)

    # Run Doubling Hypothesis on quadratic pairs demo
    doubling_results = doubling_hypothesis_analysis(
        algorithm_fn=lambda arr: quadratic_time_demo(arr),
        base_n=100,
        rounds=4,
    )

    print(f"{'N':<8} | {'Elapsed (s)':<14} | {'T(2N) / T(N)':<14} | {'Estimated k (Power Exponent)'}")
    print("-" * 80)
    for row in doubling_results:
        print(
            f"{row['N']:<8} | "
            f"{row['ElapsedSeconds']:<14.6f} | "
            f"{row['Ratio_T2N_over_TN']:<14.2f} | "
            f"k ~ {row['Estimated_Exponent_k']:.2f} (Expected k ~ 2 for O(N^2))"
        )
    print("=" * 80)

    # Dynamic Array Amortization Trace
    print("\n" + "=" * 80)
    print("DYNAMIC ARRAY AMORTIZATION TRACE (Geometric Doubling)")
    print("=" * 80)
    trace_array = EducationalDynamicArray(initial_capacity=1)
    milestones = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    print(f"{'Appends (N)':<14} | {'Capacity':<10} | {'Total Copies':<14} | {'Amortized Copies/Append'}")
    print("-" * 80)
    for i in range(1, 1025):
        trace_array.append(i)
        if i in milestones:
            print(
                f"{trace_array.size:<14} | "
                f"{trace_array.capacity:<10} | "
                f"{trace_array.total_copy_operations:<14} | "
                f"{trace_array.amortized_copies_per_append:.4f} copies/op"
            )
    print("=" * 80)
    print("Notice: As N -> infinity, Amortized Copies/Append strictly approaches < 1.0!")
    print("This mathematically proves that Dynamic Array append is amortized O(1).")
    print("=" * 80)


if __name__ == "__main__":
    main()
