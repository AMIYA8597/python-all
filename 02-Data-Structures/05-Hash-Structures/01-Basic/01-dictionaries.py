"""
# ==============================================================================
# LABORATORY: HASH TABLES (DICTIONARIES UNDER THE HOOD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In Python, the `dict` (Dictionary) is the most important data structure. 
# It allows you to look up a value by its key in O(1) time. 
# But how does it actually work? An array only allows O(1) lookups if the key 
# is an INTEGER index. How can `my_dict["Alice"]` instantly find the memory 
# location associated with the string "Alice"?
#
# A Hash Table solves this by passing the key through a "Hash Function". The 
# function converts the string into a massive integer. We then use the Modulo 
# operator (`%`) to compress that integer into a valid array index.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how a Hash Function converts arbitrary data into array indices.
# - Understand Hash Collisions (when two keys hash to the same index).
# - Build a Custom Hash Table from scratch using Separate Chaining.
#
# ==============================================================================
"""

from typing import Any, List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MAGIC OF HASH FUNCTIONS
# ==============================================================================
def explain_hash_functions():
    section_header("Concept: The Hash Function")
    
    print("Python has a built-in `hash()` function.")
    print("It takes an immutable object (like a string, tuple, or int) and returns a large integer.")
    
    key1 = "Alice"
    key2 = "Bob"
    
    h1 = hash(key1)
    h2 = hash(key2)
    
    print(f"\nHash of 'Alice': {h1}")
    print(f"Hash of 'Bob'  : {h2}")
    
    print("\nIf we have an underlying array of size 10, we compress the hash using Modulo 10:")
    print(f"'Alice' belongs at index: {h1 % 10}")
    print(f"'Bob'   belongs at index: {h2 % 10}")
    
    print("\nBecause this math operation takes O(1) time, we can instantly jump to")
    print("the correct array index without scanning the array!")


# ==============================================================================
# 4. BUILDING A CUSTOM HASH TABLE (SEPARATE CHAINING)
# ==============================================================================
class CustomHashTable:
    """
    A Hash Table built from scratch to demonstrate Separate Chaining.
    When two keys hash to the same index (Collision), we store them in a Linked List 
    (or in Python's case, a simple List) at that index.
    """
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.size = 0
        # The underlying array. Each bucket is initialized as an empty list.
        # We store tuples of (Key, Value) in the buckets.
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]
        
    def _get_index(self, key: str) -> int:
        """The internal hashing mechanism."""
        # hash() returns a massive integer. Modulo ensures it fits in our array.
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        """Inserts or updates a key-value pair."""
        index = self._get_index(key)
        bucket = self.buckets[index]
        
        # 1. Check if the key already exists in this bucket (Collision handling)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                # Key exists! Update the value.
                bucket[i] = (key, value)
                return
                
        # 2. Key does not exist. Append it to the bucket (Separate Chaining)
        bucket.append((key, value))
        self.size += 1

    def get(self, key: str) -> Any:
        """Retrieves a value by key. Raises KeyError if not found."""
        index = self._get_index(key)
        bucket = self.buckets[index]
        
        # Scan the bucket for the key
        for k, v in bucket:
            if k == key:
                return v
                
        raise KeyError(f"Key '{key}' not found.")

    def delete(self, key: str) -> None:
        """Removes a key-value pair."""
        index = self._get_index(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
                
        raise KeyError(f"Key '{key}' not found.")

    def display(self):
        """Visualizes the underlying array and collisions."""
        print(f"Hash Table (Size: {self.size}, Capacity: {self.capacity})")
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"  Bucket {i:2}: {bucket}")
            else:
                print(f"  Bucket {i:2}: [Empty]")


def demonstrate_custom_hash_table():
    section_header("Algorithm: Custom Hash Table Execution")
    
    # We use a very small capacity (5) to INTENTIONALLY force collisions
    ht = CustomHashTable(capacity=5)
    
    print("Inserting 6 items into a table of capacity 5.")
    print("By the Pigeonhole Principle, at least one bucket MUST have a collision!\n")
    
    ht.put("Apple", 100)
    ht.put("Banana", 200)
    ht.put("Orange", 300)
    ht.put("Grape", 400)
    ht.put("Melon", 500)
    ht.put("Peach", 600)
    
    ht.display()
    
    print("\nNotice how multiple (Key, Value) tuples might be stored in a single bucket.")
    print("When we call `ht.get('Apple')`, the Hash Table instantly jumps to the correct")
    print("bucket index in O(1) time. It then scans that small bucket (List) to find")
    print("the exact key 'Apple' and return its value.")
    
    print(f"\nValue of 'Orange': {ht.get('Orange')}")
    
    print("\nUpdating 'Apple' to 999...")
    ht.put("Apple", 999)
    print(f"Value of 'Apple': {ht.get('Apple')}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a Hash Collision?
   Answer: A collision occurs when the Hash Function maps two completely different keys to the exact same index in the underlying array.

2. How does Separate Chaining resolve Hash Collisions?
   Answer: Instead of storing the value directly in the array index, the array index holds a reference to a Linked List (or dynamic array). When a collision occurs, the new key-value pair is simply appended to that Linked List. During retrieval, the algorithm hashes to the index, and then linearly scans the small list to find the matching key.

3. If many collisions occur, what happens to the O(1) lookup time?
   Answer: It degrades to O(N). If all 1,000 keys hash to index 0, the Hash Table effectively becomes a single Linked List, taking O(N) to scan. To prevent this, professional Hash Tables (like Python's `dict`) track their "Load Factor" (Size / Capacity). When the table gets ~66% full, it creates a brand new underlying array that is 2x larger, and recalculates the hash indices for all elements to spread them out.
"""

if __name__ == "__main__":
    explain_hash_functions()
    demonstrate_custom_hash_table()
    print("\n[SUCCESS] Laboratory: Hash Tables Completed.")
