r"""
# Linear Search: Fundamentals, Mechanics, and Practical Applications

## A. Concept Name
Linear Search (also known as Sequential Search).

## B. One-Sentence Definition
Linear Search is a foundational search algorithm that sequentially inspects every element in a data sequence one by one from the beginning until the target value is discovered or the collection is exhausted.

## C. Why Does This Exist? (What problem does it solve?)
In software engineering, data is frequently unsorted, unindexed, or dynamically streamed. Binary search requires strict pre-sorting ($O(N \log N)$ cost), and hash tables require upfront memory allocation, hashing overhead, and hash collision resolution ($O(N)$ space). 

Linear Search solves the fundamental problem of locating an element when:
1. **The dataset is completely unsorted or unindexed**: No ordering invariants can be exploited.
2. **The data structure lacks random access**: Singly linked lists, file streams, network sockets, and generators only support forward sequential traversal ($O(1)$ to advance, $O(N)$ to seek).
3. **The collection is small ($N \le 64$)**: Hardware characteristics (cache line prefetching, branch prediction, zero preprocessing overhead) allow linear traversal to match or beat more complex algorithms in wall-clock time.
4. **Arbitrary predicate matching is required**: Searching by complex runtime conditions (e.g., "find the first user who logged in from an untrusted IP and has pending transactions") where pre-indexing on a single key is impossible.
5. **Zero-cost initialization is needed**: For one-off searches, sorting an array just to perform a single binary search takes $O(N \log N)$, whereas linear search takes only $O(N)$.

## D. Intuition & Real-Life Analogy
- **The Unmarked Keyring**: You arrive home in the dark with a ring of 10 unmarked keys. You cannot binary-search keys because they are not sorted. You try key 1; if it fails, you try key 2, then key 3, until the lock turns or you run out of keys.
- **The Disorganized Bookshelf**: Searching for a specific paperback novel on a friend's disorganized shelf. You scan each title with your eyes from left to right.
- **Lost Ticket in a Receipt Drawer**: You flip through receipts one after another from front to back until the target date appears.

## E. Mental Model
Imagine a flashlight illuminating a dark hallway lined with closed lockers. You start at locker 0, shine the light, open the door, and inspect the item:
```text
Target: 42

Index:      [0]     [1]     [2]     [3]     [4]     [5]
Values:    | 15 |  | 88 |  | 42 |  | 09 |  | 73 |  | 21 |
             ^
Step 1: Check index 0 -> 15 == 42 (False) -> Advance pointer

Index:      [0]     [1]     [2]     [3]     [4]     [5]
Values:    | 15 |  | 88 |  | 42 |  | 09 |  | 73 |  | 21 |
                     ^
Step 2: Check index 1 -> 88 == 42 (False) -> Advance pointer

Index:      [0]     [1]     [2]     [3]     [4]     [5]
Values:    | 15 |  | 88 |  | 42 |  | 09 |  | 73 |  | 21 |
                             ^
Step 3: Check index 2 -> 42 == 42 (True)  -> MATCH FOUND! Return index 2.
```

## F. Formal Technical Explanation
Linear search establishes a loop invariant over an array $A$ of size $N$ with respect to a target key $K$:
- **Loop Invariant**: At the start of iteration $i$ ($0 \le i < N$), the target $K$ does not exist within the prefix slice $A[0 \dots i-1]$.
- **Initialization**: At $i = 0$, the prefix $A[0 \dots -1]$ is the empty set $\emptyset$, so the invariant holds vacuously.
- **Maintenance**: During iteration $i$, if $A[i] \ne K$, then $K \notin A[0 \dots i]$, preserving the invariant for iteration $i + 1$.
- **Termination**: The loop terminates if:
  1. $A[i] == K$: Search succeeds; returns index $i$.
  2. $i == N$: Search fails; the invariant proves $K \notin A[0 \dots N-1]$. Returns sentinel value $-1$.

## G. Mathematical Foundation
Let $N$ denote the number of elements in array $A$.
1. **Best-Case Comparisons**:
   $$C_{\text{best}} = 1 \implies O(1)$$
   Occurs when $A[0] == \text{target}$.

2. **Worst-Case Comparisons**:
   $$C_{\text{worst}} = N \implies O(N)$$
   Occurs when the target is at index $N-1$ or is entirely absent from $A$.

3. **Average-Case (Expected) Comparisons**:
   Let $p$ be the probability that the target is present in $A$ ($0 \le p \le 1$), and assume a uniform distribution over the $N$ positions when present ($P(\text{index} = i) = \frac{p}{N}$ for all $0 \le i < N$).
   The expected number of comparisons $E[C]$ is:
   $$E[C] = \sum_{i=1}^N i \cdot \left(\frac{p}{N}\right) + N \cdot (1 - p)$$
   Using the arithmetic progression identity $\sum_{i=1}^N i = \frac{N(N + 1)}{2}$:
   $$E[C] = \frac{p}{N} \cdot \frac{N(N + 1)}{2} + N(1 - p) = \frac{p(N + 1)}{2} + N(1 - p)$$
   - If the element is guaranteed to be present ($p = 1$):
     $$E[C] = \frac{N + 1}{2} \approx \frac{N}{2} \implies O(N)$$
   - If the element is absent with 50% probability ($p = 0.5$):
     $$E[C] = \frac{N + 1}{4} + \frac{N}{2} = \frac{3N + 1}{4} \approx 0.75N \implies O(N)$$

## H. Complexity Analysis (Time, Space, Memory)
- **Time Complexity**:
  - Best Case: $O(1)$ (First element match).
  - Average Case: $O(N)$ ($\approx N/2$ checks).
  - Worst Case: $O(N)$ ($N$ checks).
- **Space Complexity**:
  - Iterative: $O(1)$ auxiliary space (only a loop index or pointer).
  - Recursive: $O(N)$ auxiliary space (due to $N$ call frames on the call stack, risking `RecursionError`).
- **Hardware & Cache Dynamics**:
  Linear Search over contiguous memory buffers (e.g., Python lists of references, C-arrays, NumPy ndarrays) leverages the CPU's **hardware prefetcher**. When the CPU reads address $X$, the L1/L2 cache controller automatically pre-fetches the entire 64-byte cache line containing $X+1, X+2, \dots$. This delivers high spatial locality and avoids random DRAM latency stalls that can degrade tree searches or hash lookups on small datasets.

## I. Common Mistakes & Pitfalls
1. **Premature Early Exit**: Placing `return -1` inside the loop body under an `else` branch, which causes the search to abort after checking only the first element:
   ```python
   # INCORRECT
   for i, val in enumerate(arr):
       if val == target:
           return i
       else:
           return -1  # BUG: Returns -1 immediately if arr[0] != target!
   ```
2. **Off-By-One Errors**: Using `while i < len(arr) - 1`, skipping the final element at index $N-1$.
3. **Recursion Stack Overflow**: Using naive recursive linear search in Python for large lists ($N > 1000$), crashing with `RecursionError: maximum recursion depth exceeded`.
4. **Floating-Point Equality Trap**: Checking `val == target` on floating-point values where arithmetic precision creates subtle mismatches (e.g., `0.1 + 0.2 == 0.3` evaluates to `False`). Always use `math.isclose()`.
5. **Mutating the Collection During Iteration**: Modifying or removing items while iterating shifts indices, leading to skipped elements.

## J. Common Confusions
- **Linear Search vs. Binary Search**: Linear search works on ANY collection without preconditions. Binary search strictly requires sorted data and $O(1)$ random access. For a one-off search on unsorted data, Linear Search ($O(N)$) is faster than Sorting + Binary Search ($O(N \log N) + O(\log N)$).
- **Linear Search vs. Hash Lookup**: Hash tables achieve $O(1)$ expected lookup, but require $O(N)$ auxiliary memory, hash calculation overhead, and hashable keys. Linear search requires zero auxiliary memory and works on unhashable types (e.g., lists of dictionaries).
- **Standard Linear Search vs. Sentinel Linear Search**: Standard linear search tests two conditions per iteration: loop bounds (`i < n`) and equality (`arr[i] == target`). Sentinel search appends the target to the end, removing the loop bounds check and cutting comparison operations in half in tight assembly loops.

## K. When To Use It
- The collection is small ($N < 64$) where cache locality and lack of algorithmic overhead dominate.
- The collection is unsorted and you only need to perform one or two searches.
- The collection is a stream, generator, iterator, or singly linked list where random access is impossible.
- The search predicate is dynamic or non-indexable (e.g., searching by lambda conditions).
- Memory constraints prohibit allocating hash tables or sorted indexes.

## L. When NOT To Use It
- The collection is large ($N > 1,000$) and queried frequently (use a Hash Map, B-Tree, or Sorted Array with Binary Search).
- Real-time, latency-critical systems where $O(N)$ worst-case delays breach Service Level Agreements (SLAs).
- The collection is already sorted (use Binary Search $O(\log N)$ or Jump Search $O(\sqrt{N})$).

## M. Trade-offs
| Attribute | Linear Search | Binary Search | Hash Table Lookup |
| :--- | :--- | :--- | :--- |
| **Prerequisite** | None | Sorted Array + Random Access | Hashable Keys |
| **Best Time** | $O(1)$ | $O(1)$ | $O(1)$ |
| **Average Time** | $O(N)$ | $O(\log N)$ | $O(1)$ |
| **Worst Time** | $O(N)$ | $O(\log N)$ | $O(N)$ (hash collisions) |
| **Auxiliary Space** | $O(1)$ | $O(1)$ iterative | $O(N)$ memory table |
| **Preprocessing** | $O(0)$ | $O(N \log N)$ sorting | $O(N)$ build time |
| **Data Types** | Any iterable | Ordered elements | Hashable elements |

## N. Debugging Tips
- Trace loop variables: Print `(index, current_value, target, comparison_result)` at each step.
- Verify terminal boundaries: Always test lists of length 0, 1, and 2, and test targets positioned at index 0 and index $N-1$.
- Ensure iterable reusability: If searching a Python generator or file object, remember that iterating consumes it.

## O. Memory Hook
**"Line by line, in single file — check each door, or walk the mile."**
Think of an inspector walking down a single corridor of doors, checking door numbers one after another in a straight line.

## P. Active Recall Questions
1. Why does Sentinel Linear Search reduce loop overhead, and how does it guarantee termination?
2. If sorting an array takes $O(N \log N)$ and binary search takes $O(\log N)$, what is the minimum number of searches $K$ required to make sorting worthwhile over repeated linear searches?
3. How does spatial cache locality make linear search faster than pointer-based lookups on tiny datasets ($N \le 32$)?
4. What happens when linear search is executed recursively on a list of 5,000 elements in standard Python?

## Q. Interview Questions & Answers
- **Q1: How can you implement a self-organizing linear search to improve average-case search time for non-uniform query distributions?**  
  *Answer:* By employing the **Move-to-Front (MTF)** heuristic or the **Transposition** heuristic. In MTF, whenever an element is successfully found, it is spliced and moved to index 0. If certain keys are requested disproportionately often (e.g., following a 80/20 Pareto distribution), those keys stay near the front of the list, reducing average lookup time toward $O(1)$.
- **Q2: Why is standard early-exit linear search dangerous when comparing secret strings (e.g., API keys, password hashes), and how do you fix it?**  
  *Answer:* Standard linear search exits early on the first mismatched byte, creating a **timing side-channel vulnerability**. An adversary can measure microscopic response latency to deduce how many initial bytes matched. The fix is a **constant-time linear search** (e.g., `hmac.compare_digest`), which inspects every single byte using bitwise accumulator operations regardless of early mismatches.
- **Q3: Given an unsorted $M \times N$ matrix, what is the optimal time complexity to locate a target element?**  
  *Answer:* $\Theta(M \cdot N)$ time. Because the matrix elements are unsorted and unindexed, any unexamined position could contain the target. By an adversary argument, any correct search algorithm must inspect up to all $M \cdot N$ cells in the worst case.

## R. Edge Cases & Boundary Conditions
1. Empty list (`[]`) $\rightarrow$ Return $-1$.
2. Single-element list matching (`[42]`, target `42`) $\rightarrow$ Return `0`.
3. Single-element list non-matching (`[42]`, target `99`) $\rightarrow$ Return `-1`.
4. Target at first index (`[10, 20, 30]`, target `10`) $\rightarrow$ Best case, 1 comparison.
5. Target at last index (`[10, 20, 30]`, target `30`) $\rightarrow$ Worst case found, $N$ comparisons.
6. Target missing entirely $\rightarrow$ Worst case, $N$ comparisons, returns $-1$.
7. Duplicate targets in list $\rightarrow$ Standard linear search returns first occurrence; multi-search returns all indices.

## S. Algorithmic Variants & Paradigms
- **Standard Iterative**: Simple forward iteration over the sequence.
- **Sentinel Search**: Appends target to bypass boundary condition `i < n`.
- **Bidirectional Linear Search**: Two pointers moving inward from both ends, halving loop iterations in worst-case searches.
- **Move-to-Front (Self-Organizing)**: Dynamic reordering optimizing for skewed access patterns.
- **Constant-Time Comparison**: Security-hardened byte comparison resistant to timing attacks.

## T. Algorithmic Comparison Table
| Algorithm | Ordering Required? | Random Access Required? | Best Time | Average Time | Worst Time | Space |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | No | No (Iterable) | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ |
| **Sentinel Linear Search** | No | Yes (Mutable Array) | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ |
| **Jump Search** | Yes | Yes (Indexable) | $O(1)$ | $O(\sqrt{N})$ | $O(\sqrt{N})$ | $O(1)$ |
| **Binary Search** | Yes | Yes (Indexable) | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ |
| **Hash Table** | No | No (Hashable keys) | $O(1)$ | $O(1)$ | $O(N)$ | $O(N)$ |

## U. Practical Implementation Exercises
1. Implement a generic linear search that accepts an optional `key` function (like Python's `min(arr, key=...)`).
2. Implement a streaming linear search over an infinite generator that stops after finding $K$ matches or inspecting $M$ elements.
3. Benchmark Sentinel Linear Search against Standard Linear Search in Python over $10^6$ integers and analyze why CPython's bytecode overhead affects the theoretical advantage.

## V. Step-by-Step Execution Trace
Search target `42` in array `[24, 13, 79, 42, 55]`:
| Step | Index ($i$) | Element ($A[i]$) | Evaluation ($A[i] == 42$) | Action | Invariant State |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0 | 24 | $24 == 42 \rightarrow \text{False}$ | Continue | $42 \notin \{24\}$ |
| 2 | 1 | 13 | $13 == 42 \rightarrow \text{False}$ | Continue | $42 \notin \{24, 13\}$ |
| 3 | 2 | 79 | $79 == 42 \rightarrow \text{False}$ | Continue | $42 \notin \{24, 13, 79\}$ |
| 4 | 3 | 42 | $42 == 42 \rightarrow \text{True}$ | Return index 3 | Target located! |

## W. Key Takeaways & Summary Anchor
- Linear search is the universal baseline of searching algorithms: zero prerequisites, zero auxiliary memory, works on all iterables.
- In hardware, sequential traversal maximizes CPU cache hit rates and hardware prefetching for small to medium buffers.
- For frequent queries on large datasets, amortize cost with hash tables ($O(1)$) or pre-sorting with binary search ($O(\log N)$).
- Always be mindful of timing attack vulnerabilities in authentication logic—use constant-time linear search for credentials.

## X. Project Connection
- **CPython Source Code**: The `in` operator on Python lists and `list.index()` compile down to C loops (`list_contains` and `list_index` in `Objects/listobject.c`) performing sequential memory dereferencing.
- **Database Query Planners**: PostgreSQL and MySQL query optimizers choose a "Sequential Table Scan" (Seq Scan) when tables fit into a single disk block or when the optimizer estimates that scanning all rows sequentially is cheaper than random I/O through a non-selective B-Tree index.
- **Linux Kernel**: The core kernel linked list macro `list_for_each_entry` implements a linear search through kernel data structures (e.g., task lists, open file descriptors, network interfaces).
"""

from typing import Any, Callable, Iterable, List, Optional, Sequence, TypeVar
import math

T = TypeVar("T")


# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATIONS
# ==============================================================================

def linear_search(arr: Sequence[T], target: T) -> int:
    """
    Standard Iterative Linear Search.
    
    Sequentially traverses the sequence and returns the 0-based index of the
    first occurrence of `target`. If `target` is not found, returns -1.
    
    Args:
        arr (Sequence[T]): The collection of elements to search.
        target (T): The value to search for.
        
    Returns:
        int: The index of the first occurrence of target, or -1 if absent.
        
    Complexity:
        Time: O(1) Best, O(N) Average, O(N) Worst.
        Space: O(1) Auxiliary.
    """
    for index, item in enumerate(arr):
        if item == target:
            return index
    return -1


def linear_search_recursive(arr: Sequence[T], target: T, current_index: int = 0) -> int:
    """
    Recursive Linear Search.
    
    Demonstrates divide-and-conquer reduction of the search space.
    Note: Educational only. In production Python, recursion depth is bounded
    by sys.getrecursionlimit() (typically 1000).
    
    Args:
        arr (Sequence[T]): The collection of elements to search.
        target (T): The value to search for.
        current_index (int): The current index under evaluation (defaults to 0).
        
    Returns:
        int: The index of the first occurrence of target, or -1 if absent.
        
    Complexity:
        Time: O(N) Worst-case.
        Space: O(N) Auxiliary call stack frames.
    """
    # Base Case 1: Reached end of collection without a match
    if current_index >= len(arr):
        return -1
    
    # Base Case 2: Target found at current index
    if arr[current_index] == target:
        return current_index
    
    # Recursive Step: Check the rest of the array
    return linear_search_recursive(arr, target, current_index + 1)


def linear_search_all(arr: Sequence[T], target: T) -> List[int]:
    """
    Multi-Match Linear Search.
    
    Traverses the entire sequence and returns all indices where `target` appears.
    
    Args:
        arr (Sequence[T]): The collection of elements to search.
        target (T): The value to search for.
        
    Returns:
        List[int]: A list containing all indices where target appears.
    """
    matching_indices: List[int] = []
    for index, item in enumerate(arr):
        if item == target:
            matching_indices.append(index)
    return matching_indices


def linear_search_predicate(
    arr: Iterable[T], 
    predicate: Callable[[T], bool]
) -> Optional[int]:
    """
    Predicate-Based Linear Search.
    
    Finds the index of the first element that satisfies an arbitrary boolean predicate.
    Works on any iterable (including generators, streams, and sets).
    
    Args:
        arr (Iterable[T]): Any iterable collection or stream.
        predicate (Callable[[T], bool]): Function returning True when an item matches.
        
    Returns:
        Optional[int]: The index of the first matching item, or None if no match.
    """
    for index, item in enumerate(arr):
        if predicate(item):
            return index
    return None


# ==============================================================================
# 2. OPTIMIZED & ADVANCED ALGORITHMIC VARIANTS
# ==============================================================================

def sentinel_linear_search(arr: List[T], target: T) -> int:
    """
    Sentinel Linear Search.
    
    Eliminates the loop-termination comparison (i < len(arr)) on every iteration
    by temporarily appending the target element as a 'sentinel' at the array's end.
    Guarantees that the target will always be found, reducing CPU branch evaluations.
    
    Args:
        arr (List[T]): A mutable list of elements.
        target (T): The value to search for.
        
    Returns:
        int: The index of the first occurrence of target, or -1 if absent.
    """
    n = len(arr)
    if n == 0:
        return -1
    
    # Check if the last element is already the target
    last_element = arr[-1]
    if last_element == target:
        return n - 1
    
    # Set sentinel: Overwrite the last element temporarily
    arr[-1] = target
    i = 0
    while arr[i] != target:
        i += 1
        
    # Restore the original last element
    arr[-1] = last_element
    
    # If the match was found before the last element, or if the original last element matched
    if i < n - 1 or last_element == target:
        return i
    
    return -1


def bidirectional_linear_search(arr: Sequence[T], target: T) -> int:
    """
    Bidirectional (Two-Pointer) Linear Search.
    
    Searches from both the front (left) and the back (right) simultaneously.
    If the target is located near the end of the array, this discovers it in O(1)
    time rather than waiting for an entire O(N) forward sweep.
    
    Args:
        arr (Sequence[T]): The collection of elements to search.
        target (T): The value to search for.
        
    Returns:
        int: The index of the first matching occurrence discovered, or -1 if absent.
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        if arr[left] == target:
            return left
        if arr[right] == target:
            return right
        left += 1
        right -= 1
        
    return -1


def move_to_front_linear_search(arr: List[T], target: T) -> int:
    """
    Self-Organizing Linear Search (Move-to-Front Heuristic).
    
    When an item is found, it is spliced out and inserted at index 0. Over repeated
    queries, frequently accessed items cluster at the front of the list, reducing
    amortized search time to near O(1) for skewed Pareto/Zipf access patterns.
    
    Args:
        arr (List[T]): A mutable list of elements.
        target (T): The value to search for.
        
    Returns:
        int: The original index where target was found, or -1 if absent.
    """
    for index, item in enumerate(arr):
        if item == target:
            if index > 0:
                # Pop and move to head
                matched_item = arr.pop(index)
                arr.insert(0, matched_item)
            return index
    return -1


def constant_time_linear_search(secret: bytes, candidate: bytes) -> bool:
    """
    Cryptographic Constant-Time Linear Search / Equality Comparison.
    
    Examines EVERY byte of the candidate against the secret without early termination.
    Prevents timing side-channel attacks where an attacker deduces token characters
    by observing CPU latency variations.
    
    Args:
        secret (bytes): The authentic reference secret (e.g., token, password hash).
        candidate (bytes): The user-supplied candidate token to authenticate.
        
    Returns:
        bool: True if secret and candidate match identically, False otherwise.
    """
    if len(secret) != len(candidate):
        return False
    
    mismatch_accumulator = 0
    # Process every single byte, accumulating bitwise differences
    for b1, b2 in zip(secret, candidate):
        mismatch_accumulator |= (b1 ^ b2)
        
    return mismatch_accumulator == 0


# ==============================================================================
# 3. INDUSTRY-STANDARD / PYTHONIC IMPLEMENTATION
# ==============================================================================

def linear_search_pythonic(arr: Sequence[T], target: T) -> int:
    """
    Production-grade Pythonic implementation using sequence built-ins.
    
    Leverages CPython's highly optimized C-level search via `Sequence.index()`.
    
    Args:
        arr (Sequence[T]): The collection of elements to search.
        target (T): The value to search for.
        
    Returns:
        int: The index of the first occurrence of target, or -1 if absent.
    """
    try:
        return arr.index(target)
    except ValueError:
        return -1


# ==============================================================================
# 4. DELIBERATELY BUGGY IMPLEMENTATIONS & DEBUGGING COMMENTARY
# ==============================================================================

def linear_search_buggy_early_exit(arr: Sequence[T], target: T) -> int:
    """
    BUGGY IMPLEMENTATION #1: Premature Return in Loop.
    
    This classic beginner bug places `return -1` inside the loop's `else` branch.
    As a result, if the very first element (index 0) does not match `target`,
    the function terminates immediately and incorrectly reports -1!
    
    Diagnostic Analysis:
    - Failing Case: arr = [10, 20, 30], target = 20
    - Trace: i=0, arr[0]=10 != 20 -> falls into 'else' -> returns -1!
    - Resolution: Move `return -1` outside and after the loop body.
    """
    for index, value in enumerate(arr):
        if value == target:
            return index
        else:
            return -1  # <- BUG: Exits after checking only the first item!
    return -1


def linear_search_buggy_off_by_one(arr: Sequence[T], target: T) -> int:
    """
    BUGGY IMPLEMENTATION #2: Off-By-One Boundary Error.
    
    The loop condition `i < len(arr) - 1` fails to inspect the final element
    located at index `len(arr) - 1`.
    
    Diagnostic Analysis:
    - Failing Case: arr = [1, 2, 3], target = 3
    - Trace: len(arr)=3. Condition `i < 2` stops at i=1. Index 2 is never inspected!
    - Resolution: Change condition to `i < len(arr)` or use `range(len(arr))`.
    """
    i = 0
    while i < len(arr) - 1:  # <- BUG: Ignores the last element!
        if arr[i] == target:
            return i
        i += 1
    return -1


# ==============================================================================
# 5. COMPREHENSIVE UNIT TESTS
# ==============================================================================

def run_tests() -> None:
    """
    Comprehensive test suite executing assert validations on all implementations.
    """
    print(">>> Running Linear Search Test Suite...")
    
    # Test Data
    empty_list: List[int] = []
    single_element_list: List[int] = [42]
    standard_list: List[int] = [10, 25, 30, 45, 50, 75, 90]
    duplicates_list: List[int] = [5, 12, 5, 27, 5, 42]
    strings_list: List[str] = ["apple", "banana", "cherry", "date"]
    
    # 1. Standard Iterative Tests
    assert linear_search(standard_list, 45) == 3, "Failed standard middle search"
    assert linear_search(standard_list, 10) == 0, "Failed to find element at index 0 (best case)"
    assert linear_search(standard_list, 90) == 6, "Failed to find element at last index"
    assert linear_search(standard_list, 999) == -1, "Failed on missing element"
    assert linear_search(empty_list, 1) == -1, "Failed on empty list"
    assert linear_search(single_element_list, 42) == 0, "Failed on matching single element"
    assert linear_search(single_element_list, 99) == -1, "Failed on missing single element"
    assert linear_search(strings_list, "cherry") == 2, "Failed on string search"
    assert linear_search(strings_list, "mango") == -1, "Failed on missing string"
    assert linear_search(duplicates_list, 5) == 0, "Failed to return first occurrence of duplicate"
    
    # 2. Recursive Tests
    assert linear_search_recursive(standard_list, 45) == 3, "Recursive search failed on middle element"
    assert linear_search_recursive(standard_list, 10) == 0, "Recursive search failed on first element"
    assert linear_search_recursive(standard_list, 90) == 6, "Recursive search failed on last element"
    assert linear_search_recursive(standard_list, 999) == -1, "Recursive search failed on missing element"
    assert linear_search_recursive(empty_list, 5) == -1, "Recursive search failed on empty list"
    
    # 3. Multi-Match Tests
    assert linear_search_all(duplicates_list, 5) == [0, 2, 4], "Failed to return all duplicate indices"
    assert linear_search_all(duplicates_list, 99) == [], "Failed to return empty list when no matches"
    
    # 4. Predicate Tests
    assert linear_search_predicate(standard_list, lambda x: x > 40) == 3, "Predicate search failed on x > 40"
    assert linear_search_predicate(standard_list, lambda x: x % 7 == 0) == -1 or \
           linear_search_predicate(standard_list, lambda x: x % 7 == 0) is None, "Predicate search failed on no match"
    assert linear_search_predicate(["cat", "elephant", "dog"], lambda s: len(s) > 5) == 1, "Predicate string search failed"
    
    # 5. Sentinel Search Tests
    mut_arr1 = [10, 25, 30, 45, 50, 75, 90]
    assert sentinel_linear_search(mut_arr1, 45) == 3, "Sentinel search failed on middle element"
    assert sentinel_linear_search(mut_arr1, 90) == 6, "Sentinel search failed on last element"
    assert sentinel_linear_search(mut_arr1, 10) == 0, "Sentinel search failed on first element"
    assert sentinel_linear_search(mut_arr1, 999) == -1, "Sentinel search failed on missing element"
    assert sentinel_linear_search([], 5) == -1, "Sentinel search failed on empty list"
    
    # 6. Bidirectional Search Tests
    assert bidirectional_linear_search(standard_list, 10) == 0, "Bidirectional failed on first element"
    assert bidirectional_linear_search(standard_list, 90) == 6, "Bidirectional failed on last element"
    assert bidirectional_linear_search(standard_list, 30) == 2, "Bidirectional failed on middle element"
    assert bidirectional_linear_search(standard_list, 999) == -1, "Bidirectional failed on missing element"
    
    # 7. Move-to-Front Tests
    mtf_list = [100, 200, 300, 400]
    original_idx = move_to_front_linear_search(mtf_list, 300)
    assert original_idx == 2, "MTF returned incorrect initial index"
    assert mtf_list == [300, 100, 200, 400], "MTF failed to move found item to index 0"
    assert move_to_front_linear_search(mtf_list, 300) == 0, "MTF failed on second consecutive lookup"
    assert move_to_front_linear_search(mtf_list, 999) == -1, "MTF failed on missing item"
    
    # 8. Constant-Time Security Search Tests
    assert constant_time_linear_search(b"secret_token_123", b"secret_token_123") is True
    assert constant_time_linear_search(b"secret_token_123", b"secret_token_999") is False
    assert constant_time_linear_search(b"short", b"longer_candidate") is False
    
    # 9. Pythonic Library Tests
    assert linear_search_pythonic(standard_list, 45) == 3
    assert linear_search_pythonic(standard_list, 999) == -1
    assert linear_search_pythonic(empty_list, 1) == -1
    
    # 10. Buggy Implementations Verification (Demonstrating failure cases)
    # Buggy early exit fails when target is not at index 0
    assert linear_search_buggy_early_exit([10, 20, 30], 20) == -1, "Expected buggy function to fail"
    # Buggy off-by-one fails when target is at the very last index
    assert linear_search_buggy_off_by_one([10, 20, 30], 30) == -1, "Expected buggy function to miss last item"
    
    print("[+] All 10 test suites passed successfully!")


# ==============================================================================
# 6. MAIN EXECUTION & VISUAL EDUCATIONAL TRACE
# ==============================================================================

def main() -> None:
    """
    Main driver executing tests and rendering educational visual execution traces.
    """
    run_tests()
    
    print("\n" + "=" * 70)
    print("EDUCATIONAL TRACE: LINEAR SEARCH IN ACTION")
    print("=" * 70)
    
    demo_array = [17, 84, 32, 91, 45, 63]
    target_value = 45
    
    print(f"Target Value: {target_value}")
    print(f"Input Array:  {demo_array}")
    print("-" * 70)
    print(f"{'Step':<6} | {'Index':<6} | {'Value':<6} | {'Check (Value == Target)':<24} | {'Action'}")
    print("-" * 70)
    
    found_idx = -1
    for step, (idx, val) in enumerate(enumerate(demo_array), start=1):
        is_match = (val == target_value)
        status = f"{val} == {target_value} ({is_match})"
        if is_match:
            action = f"MATCH FOUND! Return index {idx}."
            print(f"{step:<6} | {idx:<6} | {val:<6} | {status:<24} | {action}")
            found_idx = idx
            break
        else:
            action = "No match. Advance pointer to next index."
            print(f"{step:<6} | {idx:<6} | {val:<6} | {status:<24} | {action}")
            
    print("-" * 70)
    print(f"Result: Target {target_value} successfully located at index {found_idx}.")
    print("Total Comparisons Made:", found_idx + 1)
    print("=" * 70)


if __name__ == "__main__":
    main()
