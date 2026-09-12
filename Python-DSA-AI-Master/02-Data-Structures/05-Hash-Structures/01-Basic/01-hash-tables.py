"""
## A. Concept Name
Hash Tables (Hash Maps, Dictionaries)

## B. One-Sentence Definition
A hash table is a data structure that implements an associative array abstract data type, a structure that can map keys to values using a hash function.

## C. Why Does This Exist?
To provide extremely fast (O(1) average case) data retrieval, insertion, and deletion by using a key, rather than searching through all elements sequentially.

## D. Intuition
Imagine you have a magic filing cabinet. Instead of looking through every folder to find a document, you put the document's name into a magic calculator (hash function), and it instantly tells you exactly which drawer the document is in.

## E. Real-Life Analogy
A library's catalog system where each book's unique ISBN tells you the exact floor, aisle, and shelf where the book is located, allowing you to walk straight to it without checking any other books.

## F. Mental Model
Array of buckets + Hash Function.
Key -> [Hash Function] -> Integer Index -> Bucket in Array.

## G. Visual Explanation
Key: "apple" -> Hash("apple") % 5 -> Index 2
[0] -> empty
[1] -> empty
[2] -> ("apple", "red")
[3] -> empty
[4] -> empty

## H. Formal Explanation
A hash table uses a hash function to compute an index (also called a hash code) into an array of buckets or slots, from which the desired value can be found. During lookup, the key is hashed, and the resulting hash indicates where the corresponding value is stored. Collisions (when two keys hash to the same index) are typically handled via chaining (linked lists at each bucket) or open addressing (probing for the next empty slot).

## I. Mathematical Foundation
Index = h(k) % m
where:
- h(k) is the hash function applied to key k
- m is the size of the hash table (number of buckets)

## J. From-Scratch Implementation
(See code below)

## K. Library / Production Implementation
In Python, the built-in `dict` (and `set`) is a highly optimized hash table.
```python
my_dict = {"apple": 1, "banana": 2}
```

## L. Trace (walk through example)
1. insert("apple", 100): hash("apple") = 12345 % 10 = 5. Store at index 5.
2. insert("banana", 200): hash("banana") = 54321 % 10 = 1. Store at index 1.
3. get("apple"): hash("apple") = 5. Go to index 5, return 100.

## M. Complexity
- Time Complexity:
  - Average Case: O(1) for search, insert, delete
  - Worst Case: O(N) (all keys hash to the same bucket)
- Space Complexity: O(N) where N is the number of items stored.

## N. Common Mistakes
- Using mutable objects (like lists) as keys. Keys must be immutable (hashable).
- Ignoring load factor, causing the table to become too full and degrading performance to O(N).

## O. Common Confusions
- "Hash Table vs. Dictionary": In Python, `dict` is the specific implementation of the Hash Table concept.
- "How does it handle collisions?": Through chaining (lists in buckets) or open addressing (finding next available slot). Python's `dict` uses a form of open addressing.

## P. When To Use
- When you need fast lookups, insertions, or deletions by key.
- Caching/Memoization.
- Counting frequencies of items.

## Q. When NOT To Use
- When you need data to be ordered or sorted (though Python 3.7+ dicts preserve insertion order, they aren't meant for sorted operations like a Binary Search Tree).
- When you need to find the "closest" key or perform range queries.
- When memory space is extremely constrained (hash tables have memory overhead for empty buckets).

## R. Trade-offs
- Time vs. Space: Faster lookups require more memory (to keep the load factor low and prevent collisions).
- Unordered: Traditional hash tables do not maintain order (unlike Arrays or Linked Lists).

## S. Debugging
- Print the hash of keys if you suspect collision issues.
- Check if keys are actually hashable using `hash(key)`.

## T. Memory Hook
"Hash = Dash" - Hash tables let you dash directly to your data instead of walking through it.

## U. Active Recall
1. What is the average and worst-case time complexity of a hash table lookup?
2. What are the two primary ways to handle hash collisions?

## V. Practice
- Two Sum (LeetCode #1)
- Valid Anagram (LeetCode #242)

## W. Interview Question
"Design a Hash Map from scratch without using any built-in hash table libraries."

## X. Project Connection
Used heavily in database indexing, caching layers (Redis), and symbol tables in compilers.
"""

class HashTable:
    def __init__(self, capacity=10):
        """Initialize the hash table with a given capacity."""
        self.capacity = capacity
        # Using chaining (list of lists) to handle collisions
        self.table = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, key):
        """Simple hash function returning an index within bounds."""
        return hash(key) % self.capacity

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table."""
        index = self._hash(key)
        
        # Check if key already exists, if so update it
        for i, kv in enumerate(self.table[index]):
            k, v = kv
            if key == k:
                self.table[index][i] = (key, value)
                return
        
        # Key not found, append to the bucket (chaining)
        self.table[index].append((key, value))
        self.size += 1

    def get(self, key):
        """Retrieves a value by key."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found.")

    def delete(self, key):
        """Deletes a key-value pair from the hash table."""
        index = self._hash(key)
        for i, kv in enumerate(self.table[index]):
            k, v = kv
            if k == key:
                del self.table[index][i]
                self.size -= 1
                return
        raise KeyError(f"Key '{key}' not found.")

    def __str__(self):
        """String representation showing buckets."""
        return str(self.table)


# --- Example Usage ---
if __name__ == "__main__":
    ht = HashTable(5)
    ht.insert("apple", 100)
    ht.insert("banana", 200)
    ht.insert("orange", 300)
    ht.insert("grape", 400)
    
    print("Hash Table after insertions:", ht)
    print("Value for 'apple':", ht.get("apple"))
    
    ht.delete("banana")
    print("Hash Table after deleting 'banana':", ht)
