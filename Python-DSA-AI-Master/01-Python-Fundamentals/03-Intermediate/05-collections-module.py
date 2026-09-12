"""
## A. Concept Name
Collections Module

## B. One-Sentence Definition
The `collections` module provides specialized, high-performance container datatypes that extend Python's built-in general-purpose containers (`dict`, `list`, `set`, and `tuple`).

## C. Why Does This Exist?
While standard Python collections (`list`, `dict`) are highly versatile, they aren't optimized for every specific use case (like fast appends/pops from the front of a list, or counting occurrences, or providing default dictionary values). The `collections` module exists to fill these gaps efficiently without forcing developers to implement them from scratch.

## D. Intuition
Imagine a toolbox. A hammer and screwdriver (like `list` and `dict`) can do 90% of jobs. But sometimes you need a specialized wrench (like `deque` or `Counter`) to do a specific job cleanly and 10x faster.

## E. Real-Life Analogy
- `list` is like a standard line of people waiting. Adding to the back is easy, but letting someone jump in at the front requires everyone else to step back. `deque` is a line with two open ends, where people can join or leave from the front or back instantly.
- `Counter` is like a bouncer with a clicker keeping track of how many people of each type entered.

## F. Mental Model
Think of `collections` as the "Standard Library Plus" for data structures. 
- Need a queue? Think `deque`. 
- Need to tally? Think `Counter`. 
- Need a dictionary that doesn't throw `KeyError`? Think `defaultdict`.
- Need a class just for data without writing `__init__`? Think `namedtuple`.

## G. Visual Explanation
`list` pop(0): [1, 2, 3, 4] -> pop(0) -> [x, 2, 3, 4] -> shift everyone -> [2, 3, 4] (O(n))
`deque` popleft(): (start) [1, 2, 3, 4] (end) -> popleft() -> (start) [2, 3, 4] (end) (O(1))

## H. Formal Explanation
The `collections` module implements specialized container types:
- `namedtuple()`: factory function for creating tuple subclasses with named fields.
- `deque`: list-like container with fast appends and pops on either end.
- `Counter`: dict subclass for counting hashable objects.
- `defaultdict`: dict subclass that calls a factory function to supply missing values.
- `OrderedDict`: dict subclass that remembers the order entries were added.
- `ChainMap`: dict-like class for creating a single view of multiple mappings.

## I. Mathematical Foundation (if applicable)
For `Counter`, it is essentially a multiset (or bag) mapping $S \rightarrow \mathbb{N}$, where $S$ is the set of distinct elements, and each element maps to its frequency.

## J. From-Scratch Implementation (if applicable)
Here is how `defaultdict` roughly works under the hood (conceptually):
```python
class MyDefaultDict(dict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory
        
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = self.default_factory()
        return self[key]
```

## K. Library / Production Implementation (if applicable)
Python's actual `deque` is implemented in C using a doubly-linked list of blocks (nodes), which provides O(1) append/pop at both ends but O(n) access in the middle.

## L. Trace (walk through example)
`Counter("swiss")`
1. Read 's' -> count is 1
2. Read 'w' -> count is 1
3. Read 'i' -> count is 1
4. Read 's' -> count is 2
5. Read 's' -> count is 3
Result: `{'s': 3, 'w': 1, 'i': 1}`

## M. Complexity
- `deque.append()` / `deque.popleft()`: Time O(1), Space O(1)
- `Counter(iterable)`: Time O(N) where N is items in iterable
- `list.pop(0)`: Time O(N) - why you should use `deque` instead!

## N. Common Mistakes
- Iterating through a `deque` while modifying it.
- Expecting `Counter.most_common(1)` to return just the element. It returns a list of tuples: `[('apple', 5)]`.
- Accessing a `defaultdict` just to check if a key exists; it will inadvertently create the key with the default value! Use `in` keyword instead.

## O. Common Confusions
- "Why use `OrderedDict` when standard dicts keep insertion order in Python 3.7+?" `OrderedDict` is still useful for its `.move_to_end()` method and because its equality testing checks the order, unlike standard dicts.

## P. When To Use
- `deque`: For queues, BFS algorithms, sliding windows.
- `Counter`: For tallying, histograms, anagram checks.
- `defaultdict`: For grouping items (e.g., adjacency lists in graphs).
- `namedtuple`: For simple data classes before Python 3.7's `@dataclass`.

## Q. When NOT To Use
- Don't use `deque` if you need fast random access (e.g., `d[50]`), as it takes O(n) time. Use `list`.
- Don't use `defaultdict` if you want to strictly fail (raise `KeyError`) on missing keys.

## R. Trade-offs
- `deque` consumes slightly more memory per element than `list` due to the linked block overhead.
- `namedtuple` is immutable, meaning you cannot change fields after creation (unlike a `dataclass`).

## S. Debugging
- If a `defaultdict` seems to be magically gaining empty keys, search your code for print statements or evaluations like `if my_defaultdict[key]:` which instantiate the default value.

## T. Memory Hook (a short memorable principle)
- DefaultDict: "Never KeyError again."
- Deque: "Deck of cards, deal from top or bottom."
- Counter: "The Bouncer's Clicker."

## U. Active Recall (questions before answers)
Q: What is the time complexity of popping the first element in a standard Python list?
A: O(N), because all subsequent elements must be shifted. Use `deque.popleft()` for O(1).

Q: How do you gracefully handle missing keys when building a list-based adjacency map?
A: `defaultdict(list)`

## V. Practice (exercises)
1. Write a function using `defaultdict` to group a list of strings by their lengths.
2. Use `deque` to implement a fixed-size moving average calculator (e.g., maxlen=5).

## W. Interview Question
Challenge: Find the first non-repeating character in a string using the collections module. (Implemented below).

## X. Project Connection
In web scrapers, `deque` is used as a fast queue of URLs to visit. In NLP, `Counter` is used to build frequency vocabularies for word embeddings. `defaultdict(list)` is standard for building inverted indexes for search engines.
"""

from collections import namedtuple, deque, Counter, defaultdict, OrderedDict, ChainMap
from typing import List, Dict, Any
import timeit


def basic_collections() -> None:
    # namedtuple: memory-efficient classes without methods
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, y=20)
    print(f"Point: x={p.x}, y={p.y}")

    # Counter: dict subclass for counting hashable objects
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    word_counts = Counter(words)
    print(f"Most common word: {word_counts.most_common(1)}")


def intermediate_collections() -> None:
    # deque: Double-ended queue, O(1) append/pop from both sides
    d: deque = deque([1, 2, 3], maxlen=5)
    d.append(4)
    d.appendleft(0)
    print(f"Deque: {d}")

    # defaultdict: Provides a default value for missing keys
    graph: Dict[str, List[str]] = defaultdict(list)
    graph['A'].append('B')
    graph['A'].append('C')
    print(f"Graph nodes from A: {graph['A']}")
    print(f"Graph nodes from B (auto-created): {graph['B']}")


def advanced_collections() -> None:
    # OrderedDict: Remembers order (standard dicts do this in 3.7+ too, 
    # but OrderedDict has specialized methods like move_to_end)
    od: OrderedDict = OrderedDict()
    od['a'] = 1
    od['b'] = 2
    od.move_to_end('a')
    print(f"OrderedDict after move: {od}")

    # ChainMap: Groups multiple dicts into a single view
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 3, 'c': 4}
    chain = ChainMap(dict1, dict2)
    print(f"ChainMap value for 'b': {chain['b']}") # Takes from dict1 (first match)


def analyze_performance() -> None:
    print("--- Performance Analysis ---")
    setup = "from collections import deque; lst = list(range(10000)); dq = deque(range(10000))"
    
    # O(N) operation
    t_list = timeit.timeit("lst.pop(0) if lst else None", setup=setup, number=1000)
    # O(1) operation
    t_deque = timeit.timeit("dq.popleft() if dq else None", setup=setup, number=1000)
    
    print(f"List pop(0) time: {t_list:.6f}s")
    print(f"Deque popleft() time: {t_deque:.6f}s")
    print("Deque is vastly superior for queue-like FIFO operations.")


def handle_edge_cases() -> None:
    print("\n--- Edge Cases ---")
    # Counter with negative values
    c = Counter(a=3, b=1)
    c.subtract(Counter(a=1, b=2))
    print(f"Counter with negatives: {c}") # c['b'] becomes -1
    
    # Defaultdict trap
    d: Dict[str, int] = defaultdict(int)
    d['exists'] = 1
    if 'does_not_exist' in d: # Checking doesn't create
        pass
    print(f"Accessing creates: {d['does_not_exist']}") 
    print(f"Keys in d: {list(d.keys())}")


def first_non_repeating_char(s: str) -> str:
    """
    Challenge: Use collections to write a function that finds the first non-repeating character in a string.
    """
    counts = Counter(s)
    for char in s:
        if counts[char] == 1:
            return char
    return ""


def run_tests() -> None:
    assert first_non_repeating_char("swiss") == "w"
    assert first_non_repeating_char("aabb") == ""
    
    d: deque = deque(maxlen=2)
    d.extend([1, 2, 3])
    assert list(d) == [2, 3], "Deque maxlen failed"
    
    print("\nAll tests passed successfully.")


if __name__ == "__main__":
    print("--- Running Collections Examples ---")
    basic_collections()
    intermediate_collections()
    advanced_collections()
    analyze_performance()
    handle_edge_cases()
    run_tests()
