"""
# ==============================================================================
# LABORATORY: THE COLLECTIONS MODULE
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The built-in list, dict, and tuple are great, but the `collections` module 
# provides high-performance alternatives for specific use cases. Using a `list` 
# as a queue is O(N) for pops, which ruins algorithm performance. Using `deque` 
# is O(1). Using `Counter` saves writing loops to count frequencies.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `Counter` for rapid frequency analysis (NLP/Data Science).
# - Master `defaultdict` to prevent KeyErrors and clean up dictionary initialization.
# - Understand `deque` (Double Ended Queue) and its O(1) performance benefits.
# - Use `namedtuple` for lightweight, readable data objects.
# - Understand `ChainMap` for cascaded configuration lookups.
#
# ==============================================================================
"""

import timeit
from collections import Counter, defaultdict, deque, namedtuple, ChainMap

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. COUNTER (FREQUENCY ANALYSIS)
# ==============================================================================
def demonstrate_counter():
    """
    Counter is a dictionary subclass designed specifically for counting hashable 
    objects. It is heavily used in NLP (bag of words) and algorithms.
    """
    section_header("collections.Counter")
    
    words = ["apple", "apple", "banana", "apple", "cherry", "banana"]
    
    # Standard Dict Approach
    counts_dict = {}
    for w in words:
        if w in counts_dict:
            counts_dict[w] += 1
        else:
            counts_dict[w] = 1
            
    # Counter Approach (One Line!)
    counts = Counter(words)
    
    print(f"Counter output: {counts}")
    
    # Most Common
    print("\nMost common 2 elements:")
    print(counts.most_common(2))
    
    # Math with Counters!
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    print(f"\nc1: {c1}")
    print(f"c2: {c2}")
    print(f"c1 + c2: {c1 + c2}")
    print(f"c1 - c2: {c1 - c2}")


# ==============================================================================
# 4. DEFAULTDICT (CLEAN DICTIONARY INIT)
# ==============================================================================
def demonstrate_defaultdict():
    """
    defaultdict automatically initializes missing keys using a factory function 
    (like `list` or `int`). This prevents KeyErrors and cleans up code.
    """
    section_header("collections.defaultdict")
    
    # Grouping data
    data = [("A", 1), ("B", 2), ("A", 3), ("C", 4)]
    
    # Standard dict approach requires checking if the key exists
    grouped_std = {}
    for key, val in data:
        if key not in grouped_std:
            grouped_std[key] = []
        grouped_std[key].append(val)
        
    # defaultdict approach
    # We pass 'list' as the factory function. If a key is missing, it calls list() 
    # to create an empty list automatically!
    grouped_dd = defaultdict(list)
    for key, val in data:
        grouped_dd[key].append(val)
        
    print(f"Grouped data: {dict(grouped_dd)}")


# ==============================================================================
# 5. DEQUE (O(1) QUEUE OPERATIONS)
# ==============================================================================
def demonstrate_deque():
    """
    A deque (Double-Ended Queue) is a doubly-linked list in C.
    Popping/inserting from the FRONT of a standard Python list is O(N) because 
    every other element must shift in memory.
    Popping/inserting from the FRONT of a deque is O(1).
    """
    section_header("collections.deque (Performance)")
    
    d = deque(["a", "b", "c"])
    
    d.append("d")       # O(1) Right append
    d.appendleft("z")   # O(1) Left append
    print(f"Deque after appends: {d}")
    
    d.pop()             # O(1) Right pop
    d.popleft()         # O(1) Left pop
    print(f"Deque after pops:    {d}")
    
    # MAXLEN feature: Great for keeping the "last N items" (e.g. log tailing)
    history = deque(maxlen=3)
    for i in range(5):
        history.append(i)
    print(f"\nMaxlen Deque (keeps only last 3): {history}")


# ==============================================================================
# 6. NAMEDTUPLE (READABLE DATA)
# ==============================================================================
def demonstrate_namedtuple():
    """
    namedtuple creates tuple subclasses with named fields.
    They use exactly the same amount of memory as a regular tuple, but allow 
    access via `obj.attribute` instead of `obj[0]`.
    """
    section_header("collections.namedtuple")
    
    # Creating the class
    Point = namedtuple('Point', ['x', 'y'])
    
    # Instantiation
    p = Point(10, 20)
    
    print(f"Point object: {p}")
    print(f"Access via index p[0]: {p[0]}")
    print(f"Access via name  p.x:  {p.x}")
    
    # Immutability remains
    try:
        p.x = 99
    except AttributeError as e:
        print(f"\nImmutability protected: {e}")


# ==============================================================================
# 7. CHAINMAP (CASCADING LOOKUPS)
# ==============================================================================
def demonstrate_chainmap():
    """
    ChainMap groups multiple dicts into a single view.
    If you look up a key, it searches the dicts in order until it finds it.
    This is PERFECT for configuration management (CLI args > Env Vars > Defaults).
    """
    section_header("collections.ChainMap")
    
    cli_args = {'debug': True}
    env_vars = {'port': 8080, 'debug': False}
    defaults = {'host': 'localhost', 'port': 80, 'timeout': 30}
    
    # Create a ChainMap prioritizing CLI, then ENV, then Defaults
    config = ChainMap(cli_args, env_vars, defaults)
    
    print(f"Debug:   {config['debug']} (Taken from CLI)")
    print(f"Port:    {config['port']} (Taken from ENV)")
    print(f"Timeout: {config['timeout']} (Taken from Defaults)")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `deque` better than `list` for a Queue?
   Answer: `list.pop(0)` is O(N) because it requires shifting all remaining elements in contiguous memory. `deque.popleft()` is O(1) because it simply updates the pointers of a doubly-linked list.

2. What does `defaultdict` do?
   Answer: It provides a default value for missing keys by calling a factory function (like `int` for 0, or `list` for []), preventing KeyErrors and simplifying code.

3. How does `Counter` make NLP tasks easier?
   Answer: `Counter(iterable)` instantly creates a frequency dictionary. It also provides mathematical operations (addition/subtraction of counts) and a highly optimized `most_common(n)` method.

4. What is the memory footprint of a `namedtuple` compared to a class or a dictionary?
   Answer: It is identical to a standard `tuple`, making it far more memory-efficient than a class with a `__dict__` or a standard dictionary, while maintaining readability via dot notation.
"""

if __name__ == "__main__":
    demonstrate_counter()
    demonstrate_defaultdict()
    demonstrate_deque()
    demonstrate_namedtuple()
    demonstrate_chainmap()
    print("\n[SUCCESS] Laboratory: Collections Module Completed.")
