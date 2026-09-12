# Data Structures and Algorithms: Complexity Cheat Sheet

This document is a comprehensive reference for Big-O time and space complexities of standard data structures and algorithms. Mastery of these complexities is strictly required for technical interviews and competitive programming.

---

## 1. What is Big-O Notation?

### Beginner Explanation
Big-O notation describes how the runtime or memory requirements of an algorithm grow as the input size ($N$) grows. It gives us the "worst-case" scenario.

### Deep Technical Explanation
Big-O ($O$) defines the asymptotic upper bound of an algorithm. Mathematically, $f(n) = O(g(n))$ if there exist positive constants $c$ and $n_0$ such that $0 \le f(n) \le c \cdot g(n)$ for all $n \ge n_0$. In technical interviews, Big-O is used to classify algorithms into equivalence classes of performance (e.g., linear, logarithmic, quadratic).

---

## 2. Data Structures Complexity

### Array / Dynamic Array (Python `list`)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Access | $O(1)$ | $O(1)$ | $O(N)$ | Direct memory address arithmetic. |
| Search | $O(N)$ | $O(N)$ | - | Linear scan required. |
| Insert (End) | $O(1)$ | $O(N)$ | - | Amortized $O(1)$. Worst case $O(N)$ when reallocation is triggered. |
| Insert/Delete (Middle)| $O(N)$ | $O(N)$ | - | Requires shifting all subsequent elements. |

### Linked List (Singly / Doubly)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Access | $O(N)$ | $O(N)$ | $O(N)$ | Must traverse from the head. |
| Search | $O(N)$ | $O(N)$ | - | |
| Insert/Delete (Head) | $O(1)$ | $O(1)$ | - | Simply update pointers. |
| Insert/Delete (Middle)| $O(N)$ | $O(N)$ | - | $O(N)$ to find the node, $O(1)$ to rewire pointers. |

### Hash Table (Python `dict` / `set`)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Search / Access | $O(1)$ | $O(N)$ | $O(N)$ | Worst case occurs on massive hash collisions. |
| Insert | $O(1)$ | $O(N)$ | - | Amortized $O(1)$. Worst case on resize or collision. |
| Delete | $O(1)$ | $O(N)$ | - | |

*Security Note: Denial of Service (DoS) attacks can exploit predictable hash functions to force $O(N)$ behavior (Hash collision attack). Python mitigates this using randomized hash seeds.*

### Binary Search Tree (BST)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Access / Search | $O(\log N)$ | $O(N)$ | $O(N)$ | Worst case is a degenerate (linked-list-like) tree. |
| Insert / Delete | $O(\log N)$ | $O(N)$ | - | |

### Balanced BST (AVL, Red-Black Tree)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Access / Search | $O(\log N)$ | $O(\log N)$ | $O(N)$ | Tree height is strictly maintained at $\approx \log N$. |
| Insert / Delete | $O(\log N)$ | $O(\log N)$ | - | Rotations ensure balance. |
*(Note: Python standard library does not include a balanced BST. Use `bisect` on a sorted list, or external packages like `sortedcontainers`)*

### Heap / Priority Queue (`heapq`)
| Operation | Average Time | Worst Time | Space | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Find Min/Max | $O(1)$ | $O(1)$ | $O(N)$ | Root of the heap. |
| Insert | $O(\log N)$ | $O(\log N)$ | - | Bubble up. |
| Delete Min/Max | $O(\log N)$ | $O(\log N)$ | - | Swap with last, pop, and bubble down. |
| Heapify | $O(N)$ | $O(N)$ | - | Bottom-up heap construction. |

---

## 3. Sorting Algorithms Complexity

| Algorithm | Best Time | Average Time | Worst Time | Space | Stable? | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Quicksort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | No | Worst case happens on sorted data with poor pivot choices. |
| **Mergesort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Requires auxiliary space. |
| **Timsort** | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | Python's built-in `sort()`. Highly optimized for partially sorted data. |
| **Heapsort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No | Excellent worst-case, in-place sorting. |
| **Counting Sort**| $O(N+K)$ | $O(N+K)$ | $O(N+K)$ | $O(K)$ | Yes | $K$ is the range of inputs. Best when $K \approx N$. |

---

## 4. Graph Algorithms Complexity

Let $V$ = number of Vertices, $E$ = number of Edges.

| Algorithm | Time Complexity | Space Complexity | Use Case |
| :--- | :--- | :--- | :--- |
| **BFS / DFS** | $O(V + E)$ | $O(V)$ | Traversal, shortest path on unweighted graphs, connected components. |
| **Dijkstra** (Min-Heap)| $O((V + E) \log V)$| $O(V)$ | Single-source shortest path (no negative weights). |
| **Bellman-Ford** | $O(V \cdot E)$ | $O(V)$ | Single-source shortest path (handles negative weights, detects cycles). |
| **Floyd-Warshall** | $O(V^3)$ | $O(V^2)$ | All-pairs shortest path. |
| **Kruskal (MST)** | $O(E \log E)$ | $O(V)$ | Minimum Spanning Tree (using Union-Find). |

---

## Interview Questions & Exercises

1. **Question**: Why does Python's `sort()` use Timsort instead of Quicksort?
   **Answer**: Timsort is a hybrid of Mergesort and Insertion Sort. Real-world data is often partially sorted. Timsort detects these "runs" and merges them in $O(N)$ best-case time. It is also a **stable** sort (maintains relative order of equal elements), which is critical for object sorting, unlike standard Quicksort.
2. **Question**: You have a 2D matrix of size $M \times N$. What is the time and space complexity of running DFS to find an island?
   **Answer**: Time is $O(M \times N)$ because we visit every cell at most once. Space is $O(M \times N)$ in the worst case for the call stack if the entire grid is one island.
3. **Question**: How can you achieve $O(1)$ amortized time for dynamic array insertion?
   **Answer**: By allocating extra capacity (e.g., doubling the array size) whenever the array fills up. The $O(N)$ cost of copying elements is spread across the $N$ insertions that led up to it.
