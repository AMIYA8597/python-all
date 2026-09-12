"""
## A. Concept Name
Core Data Structures: Lists, Tuples, Sets, and Dictionaries

## B. One-Sentence Definition
Python's fundamental built-in collections designed for organizing, storing, and retrieving data with different performance and structural guarantees.

## C. Why Does This Exist?
Variables can only hold a single value. To process real-world data (like 10,000 user records, a vocabulary of words, or a mapping of IPs to locations), we need collections. However, no single collection is perfect for every task. We need specialized structures depending on whether we value order, speed of search, uniqueness, or relationships.

## D. Intuition
Imagine organizing your life. 
- Sometimes you need a sequential, modifiable checklist -> List.
- Sometimes you need a fixed, unchangeable record -> Tuple.
- Sometimes you need a bag of unique items where duplicates are ignored -> Set.
- Sometimes you need an address book to look up a name and get a phone number -> Dictionary.

## E. Real-Life Analogy
- List: A grocery list. You add items, cross them off, and the order in which you wrote them matters.
- Tuple: A printed GPS coordinate (Latitude, Longitude). It is what it is; you can't change the printed ink.
- Set: A nightclub's VIP guest list. You are either on the list or not. Writing your name twice doesn't get you in twice.
- Dictionary: A real-world dictionary or phonebook. You have a unique word/name (Key) mapped to a definition/number (Value).

## F. Mental Model
- List = Dynamic Array. Contiguous memory blocks that automatically resize when they get full.
- Tuple = Static Array. Fixed memory, immutable, highly optimized.
- Set = Hash Table (Keys only). Scatters elements in memory based on a mathematical hash for instant lookups.
- Dictionary = Hash Table (Key-Value pairs). Scatters keys in memory, each pointing to its associated value.

## G. Visual Explanation
Lists (Dynamic Arrays):
Index:    0       1       2       3
      +-------+-------+-------+-------+
Value:| "App" | "Bat" | "Cat" | "Dog" |
      +-------+-------+-------+-------+
Memory is contiguous. To find index 2, Python instantly jumps exactly 2 memory blocks forward.

Dictionaries/Sets (Hash Tables):
Key: "Alice" -> Hash Function -> 8492039 -> Modulo Array Size -> Index 2
      +-------------+
Idx 0 |             |
Idx 1 |             |
Idx 2 | -> 555-0199 | (O(1) instant jump, no need to search index 0 or 1!)
Idx 3 |             |
      +-------------+

## H. Formal Explanation
Lists and Tuples are sequence types holding elements via indexed, ordered positions. 
Sets and Dicts are mapping/collection types backed by hash tables, relying on the `hash()` value of their elements/keys to achieve O(1) average time complexity for lookups, insertions, and deletions.

## I. Mathematical Foundation (if applicable)
Hash functions map arbitrary data (strings, tuples) to fixed-size integers:
index = hash(key) % capacity
This allows Set/Dict to calculate the exact memory address of an item mathematically, rather than scanning through every item one by one. This is why Keys in a dict (and elements in a set) MUST be immutable (hashable). If they could change, their hash would change, and they would be lost in memory!

## J. From-Scratch Implementation (if applicable)
See the `MiniDictionary` class in the code below. It provides a bare-bones educational implementation of a Dictionary to show how hashing achieves O(1) lookups.

## K. Library / Production Implementation (if applicable)
Python's built-in `list`, `tuple`, `set`, and `dict` are implemented in C (CPython).
- `list`: C-level dynamic array of pointers to Python objects.
- `tuple`: C-level static array.
- `dict` and `set`: Highly optimized C-level hash tables. Modern Python (3.6+) dicts maintain insertion order by keeping a dense array of entries and a sparse array of hash table indices.

## L. Trace (walk through example)
If we do `md.put("Apple", 10)` in our `MiniDictionary`:
1. `hash("Apple")` might evaluate to 827361.
2. 827361 % 8 (capacity) = 1 (Index).
3. We place `("Apple", 10)` into the underlying array at index 1.
Instant retrieval works by repeating the same math.

## M. Complexity
Operation     | List             | Tuple            | Set              | Dictionary
--------------|------------------|------------------|------------------|------------------
Access (idx)  | O(1)             | O(1)             | N/A              | O(1) (by key)
Search (in)   | O(N)             | O(N)             | O(1)             | O(1) (by key)
Insert        | O(1) append      | N/A (Immutable)  | O(1)             | O(1)
Delete        | O(N) (mid list)  | N/A              | O(1)             | O(1)
Memory        | High             | Low              | High (Hash Map)  | High (Hash Map)

## N. Common Mistakes
- Using lists for frequent lookup/membership tests (`if target in my_list:`). Fix: Convert list to set first `my_set = set(my_list)`.
- Using mutable objects (lists, dicts) as dictionary keys (`d = {[1, 2]: "value"}`). Raises `TypeError`.
- Modifying a list while iterating over it, causing the loop to skip elements.

## O. Common Confusions
- Tuple vs List: Tuples aren't just "read-only lists". Semantically, Tuples usually store heterogeneous data (like a database row), while Lists store homogeneous data (like a column of numbers).
- Set vs List: Sets have no guaranteed order and do not support indexing (`my_set[0]` fails).

## P. When To Use
- List: You need to maintain the order of elements, and you will iterate over them.
- Tuple: You are returning multiple values from a function, or need a complex Dictionary Key.
- Set: You need to remove duplicates, or perform heavy membership testing (X in Y).
- Dictionary: You need to associate data (IDs to User Objects, Words to Counts).

## Q. When NOT To Use
- List: When you need to check if an element exists out of millions of items.
- Set/Dict: When memory is extremely constrained (hash tables trade space for speed).

## R. Trade-offs
- Lists/Tuples: Efficient memory usage and order preservation, but slow search (O(N)).
- Sets/Dicts: Blazing fast lookups and insertions (O(1)), but consume more memory due to hash table overhead and do not natively sort elements by value.

## S. Debugging
- Problem: `KeyError: 'admin'` in dictionary.
  Fix: Use `my_dict.get('admin', 'default_value')` or `collections.defaultdict`.
- Problem: `TypeError: 'tuple' object does not support item assignment`.
  Fix: Convert it to a list: `l = list(t)`, mutate `l`, convert back `t = tuple(l)`.

## T. Memory Hook (a short memorable principle)
"Lists Loop, Sets Search, Dicts Map, Tuples Lock."

## U. Active Recall (questions before answers)
- Q: Why is `x in my_set` faster than `x in my_list`?
- Q: What happens if two dictionary keys have the same hash value?
- Q: Can you use a Tuple as a dictionary key? What if the Tuple contains a List?

## V. Practice (exercises)
See `find_duplicates` in the code below for a practice exercise on frequency counting.
Exercise: Given a string of text, count the frequency of each word and return the unique words that appear more than once.

## W. Interview Question
See the `first_uniq_char` function implemented below.
Question: First Non-Repeating Character
Given a string, find the first non-repeating character and return its index. If it doesn't exist, return -1.

## X. Project Connection
In real-world AI/ML systems:
- Dictionaries: The backbone of data serialization (JSON, configs, hyperparameters).
- Sets: Used extensively in Natural Language Processing (NLP) to create vocabularies.
- Tuples: Used in PyTorch/TensorFlow to define tensor shapes, preventing pipeline bugs.
- Lists: Used for sequentially processing batches of inputs before feeding them to a neural network.
"""

from typing import List, Tuple, Set, Dict, Any, Optional

class MiniDictionary:
    """
    A bare-bones educational implementation of a Dictionary to show how 
    hashing achieves O(1) lookups. (Python's real dict is much more complex 
    and handles collisions gracefully).
    """
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        # We start with empty buckets
        self.buckets: List[Optional[Tuple[Any, Any]]] = [None] * capacity

    def _hash_index(self, key: Any) -> int:
        # hash() is Python's built-in mathematical mapping function
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        index = self._hash_index(key)
        # Simplified collision handling: just overwrite
        self.buckets[index] = (key, value)

    def get(self, key: Any) -> Any:
        index = self._hash_index(key)
        # Instant mathematical jump. No loop required! (O(1) time)
        pair = self.buckets[index]
        if pair and pair[0] == key:
            return pair[1]
        raise KeyError(key)

# ---------------------------------------------------------
# Code Examples of Built-in Structures
# ---------------------------------------------------------
def list_operations() -> List[int]:
    """Lists: Dynamic, Mutable, Ordered"""
    # Comprehensions are the Pythonic, optimized C-level way to build lists
    squares = [x * x for x in range(10) if x % 2 == 0]
    
    squares.append(100)        # O(1) Amortized
    squares.insert(0, -1)      # O(N) - shifts everything right!
    return squares

def tuple_operations() -> Tuple[str, int, float]:
    """Tuples: Fixed, Immutable, Ordered"""
    record = ("Alice", 28, 75000.50)
    
    # record[0] = "Bob" # This would crash! TypeError: does not support item assignment
    # Tuples are used heavily in Python for returning multiple values
    return record

def set_operations() -> Set[int]:
    """Sets: Fast, Mutable, Unordered, Unique"""
    # Extremely fast deduplication
    raw_data = [1, 2, 2, 3, 3, 3, 4]
    unique_items = set(raw_data)
    
    # O(1) membership testing!
    # "if 3 in unique_items:" is much faster than "if 3 in raw_data:"
    
    # Mathematical operations
    evens = {2, 4, 6}
    intersection = unique_items & evens  # O(min(len(s1), len(s2)))
    return intersection

def dict_operations() -> Dict[str, int]:
    """Dicts: Fast, Mutable, Key-Value mappings"""
    # Dictionary comprehension
    scores = {char: i * 10 for i, char in enumerate("ABC")}
    
    # Fetching with default to prevent KeyError
    b_score = scores.get("B", 0)
    d_score = scores.get("D", -1) 
    
    # Merging (Python 3.9+)
    scores |= {"D": 40, "E": 50}
    
    return scores

def find_duplicates(text: str) -> Set[str]:
    """
    Practice Solution: Given a string of text, count the frequency of each word 
    and return the unique words that appear more than once.
    """
    words = text.split()
    counts: Dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return {w for w, count in counts.items() if count > 1}

def first_uniq_char(s: str) -> int:
    """
    Interview Question: First Non-Repeating Character
    Since Python 3.7+, standard Dictionaries maintain insertion order.
    We can use a Dict to count character frequencies in O(N) time.
    """
    counts: Dict[str, int] = {}
    
    # Pass 1: Build the hash map (O(N) time)
    for char in s:
        counts[char] = counts.get(char, 0) + 1
        
    # Pass 2: Find the first char with count 1
    # Because dictionaries keep insertion order, the first one we find
    # in the dict with count == 1 is guaranteed to be the first in the string.
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
            
    return -1

def main() -> None:
    print("--- Core Data Structures Lesson ---\n")
    
    print("1. Lists (Squares + append/insert):", list_operations())
    print("2. Tuples (Unchangeable record):", tuple_operations())
    print("3. Sets (Intersection):", set_operations())
    print("4. Dicts (Char scores):", dict_operations())
    
    test_str = "leetcode"
    print(f"\nInterview Q: First unique char in '{test_str}' is at index: {first_uniq_char(test_str)}")
    
    # Demo MiniDictionary
    md = MiniDictionary(capacity=8)
    md.put("AI", "Artificial Intelligence")
    print(f"\nMiniDictionary lookup for 'AI': {md.get('AI')}")
    
    print("\nLesson complete!")

if __name__ == "__main__":
    main()
