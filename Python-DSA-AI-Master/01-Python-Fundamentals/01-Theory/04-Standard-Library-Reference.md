# Python Standard Library Reference

## Learning Objectives
- Understand the "batteries included" philosophy of Python.
- Learn to utilize advanced data structures from `collections`.
- Process streams of data efficiently using `itertools`.
- Apply higher-order function utilities from `functools`.
- Master date and time manipulation using the `datetime` module.
- Manage operating system and environment interactions with `os` and `sys`.
- Handle file paths elegantly using `pathlib`.

## Prerequisites
- Basic understanding of Python syntax and control flow.
- Familiarity with standard Python data structures (`list`, `dict`, `set`, `tuple`).
- Understanding of basic functions and arguments.

## Concept
The Python Standard Library is a vast collection of modules that come pre-packaged with Python, providing standardized solutions for everyday programming problems. It eliminates the need to install third-party packages for common tasks, such as file I/O, mathematical operations, network protocols, or complex data manipulation.

## Intuition
Imagine building a house. While you *could* forge your own nails and cut your own wood from trees (writing everything from scratch), it's far faster and safer to go to a hardware store (the Standard Library) and buy standardized, pre-made, high-quality materials. Whether you need a specialized tool for counting (`Counter`), a double-ended queue (`deque`), or a way to handle time zones (`datetime`), the tools are already waiting in your toolkit.

## Formal Explanation
The modules in the Python Standard Library are often written in C, heavily optimized, and thoroughly tested. They provide specific time and space complexity guarantees:
- **`collections`**: Extends the standard types. For example, `deque` (double-ended queue) is implemented as a doubly-linked list, ensuring O(1) time complexity for appends and pops from both ends, whereas standard lists have O(N) complexity for insertions at the start.
- **`itertools`**: Provides lazy evaluation tools that generate values on-the-fly (generators), maintaining an O(1) space complexity regardless of the dataset size.
- **`functools`**: Implements functional programming paradigms like memoization (`lru_cache`) which trades space for time complexity by caching function results.
- **`datetime`**: Distinguishes between "naive" (no timezone context) and "aware" (timezone integrated) datetime objects, strictly managing ISO representations and arithmetic rules.
- **`pathlib`**: Employs an object-oriented approach to represent filesystem paths, dynamically abstracting away OS-specific path resolution (e.g., `\` vs `/`).

## Examples
- **Data Engineering**: Processing gigabytes of logs utilizing `itertools` and `collections.Counter` without exceeding memory limits.
- **Backend Development**: Adding caching to slow database query functions via `functools.lru_cache`, and storing timestamp events in UTC with `datetime`.
- **DevOps Scripting**: Writing cross-platform automation scripts utilizing `os.environ` for secrets, `sys.argv` for CLI arguments, and `pathlib` for managing directories.

## Visuals

### List vs Deque Memory Structure

```mermaid
graph TD
    subgraph Python List (Contiguous Array)
        L1[Index 0] --- L2[Index 1] --- L3[Index 2] --- L4[Index 3]
        style L1 fill:#ff9999
        noteL["O(N) to insert at Index 0 because all elements must shift right"]
    end

    subgraph Collections Deque (Doubly-Linked List)
        D1((Val)) <--> D2((Val)) <--> D3((Val))
        style D1 fill:#99ff99
        noteD["O(1) to insert/pop at either end. Pointers are simply updated."]
    end
```

### Itertools Chain (Lazy Evaluation)

```ascii
Memory Usage: Minimal (O(1))

[Iterable A: 1, 2, 3] \
                       ---> itertools.chain() ---> yields 1, then 2, then 3, then 4...
[Iterable B: 4, 5, 6] /
```

## Derivation
*(Not applicable for standard library usage)*

## Code

### Collections (`collections`)

```python
from collections import Counter, defaultdict, deque, namedtuple

# 1. Counter (Highly optimized frequency counting)
log_entries = ['INFO', 'ERROR', 'INFO', 'WARN', 'ERROR', 'INFO']
frequency = Counter(log_entries)
print(frequency)  # Counter({'INFO': 3, 'ERROR': 2, 'WARN': 1})
print(frequency.most_common(1))  # [('INFO', 3)]

# 2. defaultdict (Avoids KeyError)
employees = [('Sales', 'Alice'), ('Engineering', 'Bob'), ('Sales', 'Charlie')]
dept_groups = defaultdict(list)
for dept, emp in employees:
    dept_groups[dept].append(emp)
print(dict(dept_groups)) # {'Sales': ['Alice', 'Charlie'], 'Engineering': ['Bob']}

# 3. deque (Double-ended queue, O(1) appends/pops)
action_history = deque(maxlen=3)
for action in ['login', 'view_profile', 'edit_settings', 'logout']:
    action_history.append(action)
print(action_history) # deque(['view_profile', 'edit_settings', 'logout'], maxlen=3)

# 4. namedtuple (Memory efficient tuple with named fields)
DatabaseConfig = namedtuple('DatabaseConfig', ['host', 'port', 'user'])
config = DatabaseConfig('localhost', 5432, 'admin')
print(config.host) # localhost
```

### Itertools (`itertools`)

```python
from itertools import groupby, chain, combinations

# 1. groupby (Note: Data must be sorted by key first)
data = [{'date': '2023-10-01', 'sales': 100}, {'date': '2023-10-01', 'sales': 150}]
for date, group in groupby(data, key=lambda x: x['date']):
    print(f"Total sales on {date}: {sum(item['sales'] for item in group)}")

# 2. chain (Process multiple sequences lazily)
active, inactive = ['alice', 'bob'], ['charlie']
for user in chain(active, inactive):
    print(f"Processing {user}...")

# 3. combinations
teams = ['Team A', 'Team B', 'Team C']
print(list(combinations(teams, 2))) # All unique pairings
```

### Functools (`functools`)

```python
from functools import lru_cache, partial, wraps
import time

# 1. lru_cache (Memoization)
@lru_cache(maxsize=128)
def fetch_data(user_id):
    time.sleep(1) # Simulates slow I/O
    return {"id": user_id}

print(fetch_data(1)) # Takes 1 second
print(fetch_data(1)) # Instant (cached)

# 2. partial (Freeze arguments)
def multiply(x, y): return x * y
double = partial(multiply, 2)
print(double(4)) # 8

# 3. wraps (Preserve metadata in decorators)
def my_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Datetime, OS/Sys, Pathlib

```python
from datetime import datetime, timedelta, timezone
import os
import sys
from pathlib import Path

# Datetime: Always use UTC for storage!
now_utc = datetime.now(timezone.utc)
future_date = now_utc + timedelta(days=30)
print(f"UTC Now: {now_utc.isoformat()}")

# OS/Sys
api_key = os.environ.get('API_KEY', 'default_dev_key')
cpu_cores = os.cpu_count()
print(f"Arguments passed to script: {sys.argv}")

# Pathlib: Object-oriented path handling
base_dir = Path('/tmp/data')
log_file = base_dir / 'app.log' # Elegant path joining
```

## Practice

### Exercise 1: Log Analyzer
Given a string of server logs (one entry per line), use `collections.Counter` to find the top 3 most frequent IP addresses.

### Exercise 2: Date Math
Write a function that takes a date string (e.g., "2024-01-01") and an integer `N`, and returns the date `N` days prior as a string using the `datetime` module.

### Exercise 3: File System Organizer
Using `pathlib`, write a script that scans a hypothetical 'Downloads' directory and creates subdirectories named 'Images' and 'Documents'. Move files based on their extensions (.jpg/.png -> Images, .pdf -> Documents).

### Exercise 4: Efficient Data Pipelines
Use `itertools.chain` to iterate over two massive lists of integers without creating new lists in memory, and yield only the even numbers.

## Recall
- `deque` gives O(1) complexity at both ends; standard lists give O(N) when inserting at the front.
- `itertools` functions process items lazily (one at a time) yielding highly efficient O(1) memory usage.
- `datetime` objects should be timezone-aware (preferably UTC) when calculating or saving timestamps.
- `pathlib` utilizes the `/` operator to easily and safely join paths across OS platforms.

## Common Errors
- **Mutable Default Arguments**: E.g., `def append_to(item, target=[])`. Default arguments evaluate once, creating shared state. Fix: use `target=None`.
- **Modifying a list while iterating**: Attempting to `.remove()` or `.append()` items to a sequence you are currently iterating through. Use list comprehensions or a copy.
- **Using naive datetime objects for calculations**: Can lead to catastrophic bugs due to Daylight Saving Time shifts.
- **Using `os.path.join` instead of `pathlib`**: While not strictly an error, it is verbose and prone to string manipulation bugs.
- **Not using `@wraps` in decorators**: Makes debugging incredibly difficult by masking function names (`__name__`) and docstrings.

## Summary
The Python Standard Library equips you with highly optimized, C-backed modules. Implementing specialized data types via `collections`, memory-efficient looping with `itertools`, functional components using `functools`, robust timestamps via `datetime`, and elegant file manipulation with `pathlib` allows you to write clean, Pythonic, and enterprise-grade code without needing external dependencies.

## Interview Questions
1. **What is the difference between a `list` and a `deque` in Python?**
   *Answer:* A `list` is a dynamically sized contiguous array in memory, making indexing O(1) but insertions/deletions at the start O(N). A `deque` is a doubly-linked list, making insertions/deletions at both ends O(1) but random access (indexing) O(N).
2. **Explain `defaultdict` and provide a use case.**
   *Answer:* `defaultdict` takes a factory function. If a key is missing, it calls the factory to initialize the value rather than raising a `KeyError`. Use case: Grouping elements or building adjacency lists for graphs.
3. **How does `@lru_cache` work and what kind of arguments must the cached function take?**
   *Answer:* It caches return values based on function arguments. Arguments must be *hashable* (immutable) because the internal caching mechanism utilizes a dictionary.
4. **Why should you use `pathlib` over `os.path`?**
   *Answer:* `pathlib` offers an object-oriented approach. Path joining is done using the `/` operator, and it includes built-in methods like `.exists()` and `.read_text()`, significantly increasing code readability.
5. **How do you safely store timezone-aware data in a database?**
   *Answer:* Always convert the datetimes to UTC (`datetime.now(timezone.utc)`) before storage. Conversions to local user timezones should happen at the presentation/UI layer.

## Further Reading
- [Python Official Documentation - The Python Standard Library](https://docs.python.org/3/library/index.html)
- [collections — Container datatypes](https://docs.python.org/3/library/collections.html)
- [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html)
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
