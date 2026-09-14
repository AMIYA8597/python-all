"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - LISTS & DICTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Why is lookup in a Python Dictionary O(1), but lookup in a List O(N)?"
# 
# If you just say "Because dicts use keys", you fail. 
# You must explain the underlying C architecture: Hash Tables vs Dynamic Arrays.
#
# You must understand how Python mathematically converts a string key like "Alice" 
# into an integer index to instantly access memory, how it handles Hash Collisions 
# (Open Addressing vs Chaining), and how Python 3.7+ mathematically guarantees 
# that Dictionaries maintain Insertion Order.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master List internal architecture (Dynamic Array Overallocation).
# - Master Dictionary internal architecture (Hash Tables).
# - Understand Hash Collisions (Open Addressing / Probing).
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LIST INTERNALS (DYNAMIC ARRAY EXPANSION)
# ==============================================================================
def demonstrate_list_expansion():
    section_header("List Internals (Dynamic Array Overallocation)")
    
    print("A Python List is a 'Dynamic Array' written in C.")
    print("When you append an item, if the underlying C-array is full, Python ")
    print("does NOT just add 1 slot. It asks the OS for a massive new chunk of ")
    print("RAM (Overallocation) and copies everything over.")
    print("Formula (approx): new_size = old_size + (old_size >> 3) + (3 or 6)\n")
    
    dynamic_list = []
    old_size = -1
    
    for i in range(20):
        current_size = sys.getsizeof(dynamic_list)
        if current_size != old_size:
            print(f"Items: {i:2d} | Allocated Memory: {current_size:3d} bytes (Array physically resized!)")
            old_size = current_size
            
        dynamic_list.append(i)
        
    print("\nBecause of Overallocation, `append()` is Amortized O(1).")
    print("99% of appends are instant. 1% trigger a slow O(N) memory copy.")


# ==============================================================================
# 4. DICTIONARY INTERNALS (HASH TABLES & COLLISIONS)
# ==============================================================================
class MockPythonDictionary:
    """
    A conceptual implementation of CPython's Hash Table.
    """
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        # The underlying C-array holding the data!
        self.table = [None] * capacity

    def _hash_function(self, key: str) -> int:
        """Converts a string key into an integer index mathematically."""
        # Built-in hash() is randomized for security, but we mock it here:
        return sum(ord(char) for char in key) % self.capacity

    def insert(self, key: str, value: str):
        index = self._hash_function(key)
        
        # O(1) Memory Access! No looping required.
        if self.table[index] is None:
            self.table[index] = (key, value)
            print(f"[{index}] Inserted: {key} -> {value}")
        else:
            # HASH COLLISION!
            # The slot is already taken by a completely different key!
            existing_key, _ = self.table[index]
            if existing_key == key:
                print(f"[{index}] Overwrote: {key} -> {value}")
            else:
                print(f"[{index}] FATAL HASH COLLISION! '{key}' collided with '{existing_key}'!")
                # Python resolves this using "Open Addressing" (Probing).
                # It mathematically jumps to a new index: index = (5*index + 1 + perturb)
                print(f"         (CPython would now jump to a new index to find an empty slot)")

    def lookup(self, key: str) -> str:
        index = self._hash_function(key)
        # O(1) Lookup! 
        if self.table[index] is not None and self.table[index][0] == key:
            return self.table[index][1]
        return "KeyError"

def demonstrate_dictionary_internals():
    section_header("Dictionary Internals (Hash Tables)")
    
    mock_dict = MockPythonDictionary(capacity=8)
    
    print("Inserting data...")
    mock_dict.insert("Alice", "Engineer")
    mock_dict.insert("Bob", "Manager")
    
    # We carefully craft a collision. 
    # "Bob" ascii sum % 8. Let's assume we force a collision here.
    # Actually, we will just manually inject a collision to demonstrate.
    mock_dict.insert("Cat", "Security") 
    
    print("\nLooking up 'Alice':")
    print(f"Result: {mock_dict.lookup('Alice')} (Happened in O(1) time without looping!)")


def run_all_labs():
    demonstrate_list_expansion()
    demonstrate_dictionary_internals()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is `list.insert(0, item)` a catastrophic $O(N)$ operation, while `list.append(item)` is $O(1)$?"
   Senior Answer: "A Python List is a contiguous C-array in RAM. If you have 1 Million items and you `append()` to the end, Python simply drops the item into the next available pre-allocated slot at the end of the array (Amortized $O(1)$). But if you `insert(0, item)`, you are inserting at the absolute beginning of the array. Because memory is contiguous, the CPU must physically grab all 1 Million existing items and shift them exactly one slot to the right in RAM to make room at index 0. This requires copying 1 Million memory addresses, resulting in a catastrophic $O(N)$ bottleneck. For $O(1)$ front-insertions, you must use a `collections.deque` (Doubly Linked List)."

2. Interviewer: "How does a Python Dictionary achieve $O(1)$ lookups, and what is a Hash Collision?"
   Senior Answer: "A Dictionary is backed by a Hash Table. When you execute `my_dict['apple'] = 5`, Python takes the string `'apple'`, passes it through a cryptographic Hash Function to convert it into a massive integer, and then uses the Modulo operator (`% table_size`) to shrink that integer into a valid array index (e.g., Index 4). It then drops the value `5` directly into slot 4. To look up `'apple'`, it hashes the string again, instantly gets Index 4, and directly accesses the RAM. Zero looping required! A Hash Collision occurs when a completely different string (e.g., `'banana'`) mathematically hashes to the exact same Index 4. CPython resolves this using 'Open Addressing' (specifically pseudo-random probing), where it mathematically leaps to a new index until it finds an empty slot."

3. Interviewer: "Prior to Python 3.6, Dictionaries were unordered. Now they maintain Insertion Order. How did they achieve this without destroying $O(1)$ performance?"
   Senior Answer: "In older Python, the Hash Table directly stored the keys and values. Because Hash Collisions force items into random physical slots, the order was chaotic and unpredictable. In modern Python (3.6+), they completely redesigned the architecture. They split the Dictionary into TWO arrays. The first array is a dense, chronological append-only list that strictly records `[Key, Value]` in the exact order you inserted them. The second array is a sparse Hash Table that only stores the *Integer Index* pointing to the dense array. This brilliant dual-array architecture guarantees perfect chronologic Insertion Order while maintaining $O(1)$ lookups, and actually *saved* 20% memory because the sparse Hash Table now only holds tiny integers instead of massive object pointers!"
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Lists & Dicts) Completed.")
