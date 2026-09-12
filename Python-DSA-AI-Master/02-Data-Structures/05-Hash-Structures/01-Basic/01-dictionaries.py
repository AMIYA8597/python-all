"""
# Hash Maps / Dictionaries in Python: From Beginner to Professional

## 1. Intuition and Real-World Analogy
Imagine a massive library with millions of books. If you had to search book by book to find a specific title, it would take a lifetime (O(N) time). Instead, the library uses a catalog system. You look up a book's unique identifier (the key), and the catalog immediately tells you exactly which shelf and row the book is on (the value). 
A Hash Map (Dictionary in Python) does exactly this. It maps "keys" to "values" using a mathematical function (the hash function) that instantly computes the exact memory location where the value is stored.

## 2. Formal Explanation
A Hash Map is a data structure that implements an associative array abstract data type, a structure that can map keys to values. A hash map uses a hash function to compute an index, also called a hash code, into an array of buckets or slots, from which the desired value can be found.

In Python, the `dict` type is implemented as a hash map. Since Python 3.7, dictionaries maintain the insertion order of items by storing the data in a dense array and keeping a separate sparse array of indices (the actual hash table).

### Key Constraints:
- Keys must be **hashable**: They must have a hash value that never changes during their lifetime (implemented via `__hash__()`) and can be compared to other objects (implemented via `__eq__()`). Mutable types like `list` or `dict` cannot be keys.

## 3. Complexity Analysis
- **Time Complexity:**
  - Average Case: O(1) for insertion, lookup, and deletion.
  - Worst Case: O(N) when multiple keys hash to the same bucket (Hash Collisions) and form a long chain or probe sequence, though Python's collision resolution (open addressing with pseudo-random probing) mitigates this effectively.
- **Space Complexity:** O(N) where N is the number of key-value pairs stored. Python dictionaries typically pre-allocate memory and double in size when 2/3 full to maintain a low load factor.

## 4. Common Mistakes & Debugging
- **Mistake 1:** Using mutable objects (like lists or sets) as keys. This will raise a `TypeError: unhashable type`. Use tuples or frozen sets instead.
- **Mistake 2:** Modifying a dictionary while iterating over it. This raises a `RuntimeError: dictionary changed size during iteration`. Instead, iterate over a copy of keys `list(d.keys())` or collect items to modify later.
- **Debugging Tip:** If order matters in your logic, remember that Python 3.7+ preserves insertion order, but relying on this for critical logic in legacy systems (Python <3.7) is a bug. Also, use `collections.defaultdict` to avoid `KeyError`s when accumulating values.

## 5. Active Recall & Memory Anchors
- **Memory Anchor:** The Hash Function is a "Teleporter" – you give it a key, it instantly teleports you to the value's address.
- **Active Recall:** 
  1. Q: Why can't a `list` be a key in a dictionary?
     A: Because lists are mutable. If a list changes, its hash value would change, meaning we'd lose track of where its corresponding value is stored in the hash table.
  2. Q: What happens when two keys hash to the same index?
     A: This is a collision. Python handles it using open addressing with a pseudo-random probe sequence.

"""

from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter

# ==========================================
# 1. Basic Dictionary Operations (Beginner)
# ==========================================

class BasicDictionaryOperations:
    """
    Demonstrates fundamental dictionary operations.
    """
    def __init__(self) -> None:
        # Initializing an empty dictionary
        self.data: Dict[str, Any] = {}

    def insert_or_update(self, key: str, value: Any) -> None:
        """O(1) average time insertion."""
        self.data[key] = value

    def fetch(self, key: str) -> Optional[Any]:
        """O(1) average time lookup. Using .get() prevents KeyError."""
        return self.data.get(key)

    def fetch_with_default(self, key: str, default: Any) -> Any:
        """Returns a default value if key is not found."""
        return self.data.get(key, default)

    def delete_key(self, key: str) -> bool:
        """O(1) average time deletion."""
        if key in self.data:
            del self.data[key]
            return True
        return False

    def iterate_items(self) -> List[Tuple[str, Any]]:
        """Iterates over key-value pairs."""
        return [(k, v) for k, v in self.data.items()]

# ==========================================
# 2. Advanced Dictionary Usage (Professional)
# ==========================================

class ProfessionalDictionaryUsage:
    """
    Demonstrates advanced standard library usage which professionals 
    use to write cleaner and more efficient code.
    """
    @staticmethod
    def group_anagrams(words: List[str]) -> List[List[str]]:
        """
        Uses defaultdict to group words by their character frequencies.
        Avoids checking if a key exists before appending.
        """
        # defaultdict automatically creates an empty list for a new key
        anagram_map = defaultdict(list)
        for word in words:
            # Sorted word is a tuple of chars, which is hashable and usable as a key
            sorted_word = tuple(sorted(word)) 
            anagram_map[sorted_word].append(word)
        return list(anagram_map.values())
        
    @staticmethod
    def count_frequencies(elements: List[Any]) -> Dict[Any, int]:
        """
        Using collections.Counter for O(N) frequency counting,
        which is highly optimized in C.
        """
        return dict(Counter(elements))

    @staticmethod
    def merge_dictionaries(d1: Dict[str, int], d2: Dict[str, int]) -> Dict[str, int]:
        """
        Python 3.9+ dictionary merge operator (|).
        If keys overlap, values from d2 overwrite values from d1.
        """
        # For older versions, one would use {**d1, **d2}
        return d1 | d2

# ==========================================
# 3. Interview Challenge: Two Sum
# ==========================================

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Finds two numbers in 'nums' that sum up to 'target'.
    
    Intuition:
    Instead of checking every pair (O(N^2) time), we can use a hash map to 
    remember the numbers we've seen so far and their indices.
    For every number `x`, we check if `target - x` is in our hash map.
    
    Time Complexity: O(N) because we iterate through the list once.
    Space Complexity: O(N) for storing up to N elements in the dictionary.
    """
    seen: Dict[int, int] = {} # Maps value to its index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
        
    return [] # Return empty if no solution exists


# ==========================================
# 4. Under The Hood: Custom Hash Map Implementation (Educational)
# ==========================================

class SimpleHashMap:
    """
    A simplified version of a Hash Map to demonstrate the internals:
    - Array of buckets
    - Hash function using modulo arithmetic
    - Collision resolution via Chaining (Lists in buckets)
    """
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        # Each bucket contains a list of (key, value) tuples for chaining
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self.capacity)]
        self.size = 0

    def _hash(self, key: str) -> int:
        """Calculates the bucket index for a given key."""
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        """Inserts or updates a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update existing key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
                
        # Insert new key
        bucket.append((key, value))
        self.size += 1

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value by key."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
        
    def remove(self, key: str) -> bool:
        """Removes a key-value pair. Returns True if removed, else False."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False


# ==========================================
# Tests
# ==========================================

def test_basic_operations():
    d = BasicDictionaryOperations()
    d.insert_or_update("apple", 5)
    assert d.fetch("apple") == 5
    assert d.fetch("banana") is None
    assert d.fetch_with_default("banana", 0) == 0
    assert d.delete_key("apple") is True
    assert d.fetch("apple") is None

def test_professional_usage():
    # Test defaultdict
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped = ProfessionalDictionaryUsage.group_anagrams(words)
    assert len(grouped) == 3  # ["eat", "tea", "ate"], ["tan", "nat"], ["bat"]
    
    # Test Counter
    freqs = ProfessionalDictionaryUsage.count_frequencies(['a', 'a', 'b'])
    assert freqs == {'a': 2, 'b': 1}
    
    # Test merge
    d1 = {"x": 1, "y": 2}
    d2 = {"y": 3, "z": 4}
    merged = ProfessionalDictionaryUsage.merge_dictionaries(d1, d2)
    assert merged == {"x": 1, "y": 3, "z": 4}

def test_two_sum():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]

def test_custom_hash_map():
    h = SimpleHashMap(capacity=4)
    h.put("apple", 100)
    h.put("banana", 200)
    # Force potential collisions by small capacity
    h.put("cherry", 300) 
    h.put("date", 400)
    h.put("elderberry", 500)
    
    assert h.get("apple") == 100
    assert h.get("cherry") == 300
    
    # Update existing
    h.put("apple", 150)
    assert h.get("apple") == 150
    
    # Remove
    assert h.remove("banana") is True
    assert h.get("banana") is None
    assert h.remove("nonexistent") is False

if __name__ == "__main__":
    test_basic_operations()
    test_professional_usage()
    test_two_sum()
    test_custom_hash_map()
    print("01-dictionaries.py: All advanced tests passed successfully!")
