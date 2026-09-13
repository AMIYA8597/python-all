"""
# ==============================================================================
# LABORATORY: HASH TABLES (OPEN ADDRESSING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that "Separate Chaining" resolves hash collisions by putting multiple 
# elements into a Linked List at a single array index.
# However, Linked Lists are terrible for modern CPU Caches because the memory 
# is scattered across RAM. 
# 
# "Open Addressing" solves collisions WITHOUT using Linked Lists. If an index 
# is already taken, the algorithm simply probes (searches) for the NEXT available 
# empty slot in the SAME array!
# Because all data is stored contiguously in a single array, Open Addressing is 
# incredibly cache-friendly. This is exactly how Python's built-in `dict` works 
# under the hood!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Open Addressing and Linear Probing.
# - Understand the "Tombstone" problem during deletion.
# - Build a Custom Hash Table from scratch using Open Addressing.
#
# ==============================================================================
"""

from typing import Any, List, Optional, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. OPEN ADDRESSING & TOMBSTONES
# ==============================================================================
def explain_tombstones():
    section_header("Concept: The Tombstone Problem")
    print("""
Imagine an array of size 5.
1. 'Apple' hashes to index 2. We put it there. Array: [_, _, Apple, _, _]
2. 'Banana' hashes to index 2. It's full! We "probe" to the next slot (index 3) 
   and put it there. Array: [_, _, Apple, Banana, _]

Now, what happens if we DELETE 'Apple'?
Array: [_, _, _, Banana, _]

If we search for 'Banana', it hashes to index 2. We look at index 2, see that 
it's EMPTY, and the algorithm assumes 'Banana' is not in the table! It stops 
searching and fails to find it at index 3.

To fix this, we cannot truly delete 'Apple'. We must replace it with a special 
marker called a "Tombstone" (e.g., `<DELETED>`). 
When the search algorithm sees a Tombstone, it knows to KEEP PROBING.
    """)


# ==============================================================================
# 4. BUILDING A CUSTOM HASH TABLE (LINEAR PROBING)
# ==============================================================================
class OpenAddressingHashTable:
    """
    A Hash Table built from scratch using Linear Probing.
    """
    # Unique sentinel object to represent a Tombstone
    TOMBSTONE = object()
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.size = 0
        # The underlying array stores tuples of (Key, Value) directly.
        # None means completely empty. TOMBSTONE means deleted.
        self.buckets: List[Optional[Tuple[str, Any]]] = [None] * capacity
        
    def _get_hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        if self.size == self.capacity:
            raise Exception("Hash Table is completely full! (Needs resizing)")
            
        index = self._get_hash(key)
        
        # Linear Probing: While the current slot is occupied...
        while self.buckets[index] is not None and self.buckets[index] is not self.TOMBSTONE:
            # Check if it's the exact same key (Update value)
            if self.buckets[index][0] == key:
                self.buckets[index] = (key, value)
                return
                
            # Collision! Probe to the NEXT index, wrapping around via modulo
            index = (index + 1) % self.capacity
            
        # We found an empty slot or a Tombstone! Insert it.
        self.buckets[index] = (key, value)
        self.size += 1

    def get(self, key: str) -> Any:
        index = self._get_hash(key)
        
        # Linear Probing: While the slot is NOT completely empty...
        while self.buckets[index] is not None:
            # If it's a Tombstone, skip it. If it's a real tuple, check the key.
            if self.buckets[index] is not self.TOMBSTONE:
                if self.buckets[index][0] == key:
                    return self.buckets[index][1] # Found it!
                    
            # Keep probing
            index = (index + 1) % self.capacity
            
        # We hit a `None` slot. The probe sequence is broken. The key doesn't exist.
        raise KeyError(f"Key '{key}' not found.")

    def delete(self, key: str) -> None:
        index = self._get_hash(key)
        
        while self.buckets[index] is not None:
            if self.buckets[index] is not self.TOMBSTONE:
                if self.buckets[index][0] == key:
                    # Found it! Mark it as a Tombstone. Do NOT set to None.
                    self.buckets[index] = self.TOMBSTONE
                    self.size -= 1
                    return
            index = (index + 1) % self.capacity
            
        raise KeyError(f"Key '{key}' not found.")

    def display(self):
        print(f"Hash Table (Size: {self.size}, Capacity: {self.capacity})")
        for i, item in enumerate(self.buckets):
            if item is None:
                print(f"  [{i:2}]: Empty")
            elif item is self.TOMBSTONE:
                print(f"  [{i:2}]: <TOMBSTONE>")
            else:
                print(f"  [{i:2}]: {item}")

def demonstrate_open_addressing():
    section_header("Algorithm: Open Addressing (Linear Probing)")
    
    ht = OpenAddressingHashTable(capacity=7)
    
    # Intentionally forcing collisions by inserting strings that hash differently
    # but we will assume they collide for the sake of the algorithm flow.
    print("Inserting Apple, Banana, Orange, Grape, Melon...")
    ht.put("Apple", 100)
    ht.put("Banana", 200)
    ht.put("Orange", 300)
    ht.put("Grape", 400)
    ht.put("Melon", 500)
    
    ht.display()
    
    print("\nLet's delete 'Apple' (which might be blocking 'Banana' or 'Orange' from their true hash index)")
    ht.delete("Apple")
    
    ht.display()
    
    print("\nBecause we used a <TOMBSTONE>, calling `get('Orange')` will successfully")
    print("skip the Tombstone and keep probing until it finds 'Orange'!")
    
    val = ht.get("Orange")
    print(f"\nValue of Orange: {val} (Expected: 300)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Linear Probing and Quadratic Probing?
   Answer: In Linear Probing, if index `i` is full, you check `i+1`, `i+2`, `i+3`. This leads to "Primary Clustering" (large blocks of occupied slots forming). In Quadratic Probing, you check `i + 1^2`, `i + 2^2`, `i + 3^2` (i+1, i+4, i+9). This spreads out the collisions and prevents clustering.

2. Why is Open Addressing much faster in practice than Separate Chaining?
   Answer: CPU Cache! Modern CPUs load memory in chunks (Cache Lines). Since Open Addressing stores everything in a single, contiguous array, checking `i`, `i+1`, and `i+2` guarantees cache hits (incredibly fast). Separate Chaining requires following pointers to random memory locations (Linked Lists), which guarantees cache misses (slow).

3. Why do Python dictionaries use Open Addressing?
   Answer: For the exact cache reasons above. Python's `dict` is highly optimized in C using Open Addressing with a pseudo-random probing sequence. It guarantees near O(1) performance and extremely high cache locality.
"""

if __name__ == "__main__":
    explain_tombstones()
    demonstrate_open_addressing()
    print("\n[SUCCESS] Laboratory: Open Addressing Completed.")
