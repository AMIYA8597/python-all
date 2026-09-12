"""
Python Standard Library: Interview Preparation

This module covers frequently asked questions about the Python Standard Library.
Topics include:
- collections (Counter, defaultdict, namedtuple, deque)
- itertools (combinations, permutations, groupby)
- functools (lru_cache, partial, reduce)
- datetime (parsing and formatting)

Beginner Explanation:
The Standard Library is a huge collection of built-in modules that come with Python. 
Instead of writing complex code from scratch, you can use these tools to solve common problems 
like counting items, caching results, or handling dates. "Batteries included!"

Technical Explanation:
Understanding standard library modules indicates a developer writes idiomatic and optimized Python.
`collections.Counter` is highly optimized for frequency counting. 
`functools.lru_cache` provides a thread-safe memoization decorator.
`itertools` provides memory-efficient C-level iterators for combinatorial operations.
"""
from collections import Counter, defaultdict, namedtuple, deque
from itertools import combinations, permutations, groupby
from functools import lru_cache, partial, reduce
from datetime import datetime, timedelta

def demonstrate_collections():
    """
    Demonstrates useful tools from the collections module.
    """
    # Counter: O(N) frequency counting
    words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    counts = Counter(words)
    assert counts['apple'] == 3
    assert counts.most_common(1) == [('apple', 3)]
    
    # defaultdict: handles missing keys automatically
    d = defaultdict(list)
    d['fruits'].append('apple')
    assert d['fruits'] == ['apple']
    assert d['vegetables'] == []  # creates the key with an empty list instead of KeyError
    
    # namedtuple: memory-efficient, readable classes
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, y=20)
    assert p.x == 10 and p.y == 20
    
    # deque: Double-ended queue, O(1) appends and pops from both ends
    q = deque([1, 2, 3])
    q.appendleft(0)
    q.append(4)
    assert q.popleft() == 0
    assert q.pop() == 4

def demonstrate_itertools():
    """
    Demonstrates combinatorial functions from itertools.
    """
    items = [1, 2, 3]
    
    # Permutations (order matters)
    perms = list(permutations(items, 2))
    assert perms == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
    
    # Combinations (order doesn't matter)
    combs = list(combinations(items, 2))
    assert combs == [(1, 2), (1, 3), (2, 3)]
    
    # Groupby: Groups adjacent elements
    # Data must be sorted by the grouping key first!
    data = [('animal', 'cat'), ('animal', 'dog'), ('bird', 'pigeon')]
    grouped = {k: [item[1] for item in g] for k, g in groupby(data, key=lambda x: x[0])}
    assert grouped['animal'] == ['cat', 'dog']

def demonstrate_functools():
    """
    Demonstrates tools from functools.
    """
    # lru_cache for memoization (caching return values of expensive functions)
    @lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    assert fibonacci(10) == 55
    
    # partial: freezing some arguments of a function
    def power(base: int, exp: int) -> int:
        return base ** exp
    
    square = partial(power, exp=2)
    cube = partial(power, exp=3)
    
    assert square(5) == 25
    assert cube(2) == 8
    
    # reduce: applies a rolling computation to sequential pairs of values
    numbers = [1, 2, 3, 4]
    product = reduce(lambda x, y: x * y, numbers)
    assert product == 24

def demonstrate_datetime():
    """
    Demonstrates date parsing and math using datetime.
    """
    # Parsing string to datetime
    date_string = "2023-10-31 15:30:00"
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    assert dt.year == 2023
    assert dt.month == 10
    
    # Formatting datetime to string
    formatted = dt.strftime("%B %d, %Y")
    assert formatted == "October 31, 2023"
    
    # Date arithmetic using timedelta
    future_date = dt + timedelta(days=5, hours=2)
    assert future_date.day == 5  # Nov 5
    assert future_date.hour == 17

if __name__ == "__main__":
    demonstrate_collections()
    demonstrate_itertools()
    demonstrate_functools()
    demonstrate_datetime()
    print("All standard library examples passed.")
