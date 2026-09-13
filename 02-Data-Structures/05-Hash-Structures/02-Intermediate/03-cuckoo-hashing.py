"""
# ==============================================================================
# LABORATORY: CUCKOO HASHING (O(1) WORST-CASE LOOKUP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Standard Hash Tables (Separate Chaining and Open Addressing) 
# have an AVERAGE lookup time of O(1). However, if 100 items collide and form 
# a massive cluster or linked list, the lookup degrades to O(N).
# 
# For Real-Time Systems (like High-Frequency Trading or Aviation Software), 
# an O(N) lookup could cause a catastrophic freeze. They require a data structure 
# that guarantees absolute O(1) WORST-CASE lookup time.
#
# "Cuckoo Hashing" achieves this. It uses TWO Hash Functions and TWO underlying 
# arrays. Every key has exactly TWO possible locations. If you want to find a key, 
# you just check Array1[Hash1] and Array2[Hash2]. If it's not in either, it doesn't 
# exist. Maximum 2 lookups. Guaranteed O(1).
#
# But how does it handle insertions when both spots are taken? It forcefully 
# evicts (kicks out) the existing item, forcing that item to move to its alternate 
# location! (Like a Cuckoo bird kicking eggs out of a nest).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the dual-hash, dual-array architecture.
# - Understand the recursive eviction chain during insertion.
# - Implement Cuckoo Hashing from scratch.
#
# ==============================================================================
"""

import hashlib
from typing import Any, List, Optional, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CUCKOO HASHING IMPLEMENTATION
# ==============================================================================
class CuckooHashTable:
    def __init__(self, capacity: int = 11):
        # We use two separate arrays
        self.capacity = capacity
        self.table1: List[Optional[Tuple[str, Any]]] = [None] * capacity
        self.table2: List[Optional[Tuple[str, Any]]] = [None] * capacity
        self.size = 0
        
        # If an eviction chain goes on too long, we assume it's an infinite loop 
        # (a cycle) and the table must be rehashed with a larger capacity.
        self.MAX_EVICTIONS = capacity * 2

    def _hash1(self, key: str) -> int:
        """First hash function."""
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return h % self.capacity

    def _hash2(self, key: str) -> int:
        """Second hash function (Must be independent from the first!)."""
        h = int(hashlib.sha1(key.encode()).hexdigest(), 16)
        return h % self.capacity

    def get(self, key: str) -> Any:
        """
        Retrieval is incredibly fast and GUARANTEED O(1) worst-case.
        We only ever check exactly TWO memory locations. No probing!
        """
        idx1 = self._hash1(key)
        if self.table1[idx1] is not None and self.table1[idx1][0] == key:
            return self.table1[idx1][1]
            
        idx2 = self._hash2(key)
        if self.table2[idx2] is not None and self.table2[idx2][0] == key:
            return self.table2[idx2][1]
            
        raise KeyError(f"Key '{key}' not found.")

    def put(self, key: str, value: Any) -> None:
        """
        Insertion can trigger an eviction chain.
        """
        # First, check if the key already exists to just update its value
        idx1 = self._hash1(key)
        if self.table1[idx1] is not None and self.table1[idx1][0] == key:
            self.table1[idx1] = (key, value)
            return
            
        idx2 = self._hash2(key)
        if self.table2[idx2] is not None and self.table2[idx2][0] == key:
            self.table2[idx2] = (key, value)
            return
            
        # Key is new. Start the insertion/eviction process.
        current_key = key
        current_value = value
        
        for _ in range(self.MAX_EVICTIONS):
            # 1. ALWAYS try to insert into Table 1 first
            idx1 = self._hash1(current_key)
            
            # If it's empty, we are done!
            if self.table1[idx1] is None:
                self.table1[idx1] = (current_key, current_value)
                self.size += 1
                return
                
            # If it's FULL, we EVVICT the current resident!
            # The new item takes the spot. The old item becomes the "current" item 
            # that needs to find a new home.
            evicted_item = self.table1[idx1]
            self.table1[idx1] = (current_key, current_value)
            
            current_key, current_value = evicted_item[0], evicted_item[1]
            print(f" [Cuckoo] '{self.table1[idx1][0]}' kicked '{current_key}' out of Table 1!")
            
            # 2. The evicted item MUST now go to Table 2
            idx2 = self._hash2(current_key)
            
            if self.table2[idx2] is None:
                self.table2[idx2] = (current_key, current_value)
                self.size += 1
                return
                
            # If Table 2's spot is ALSO full, evict THAT resident!
            evicted_item = self.table2[idx2]
            self.table2[idx2] = (current_key, current_value)
            
            current_key, current_value = evicted_item[0], evicted_item[1]
            print(f" [Cuckoo] '{self.table2[idx2][0]}' kicked '{current_key}' out of Table 2!")
            
            # The loop continues. The newly evicted item will now try its Table 1 hash again!
            
        # If we loop `MAX_EVICTIONS` times, we assume we are caught in an infinite 
        # cycle of evictions. The Load Factor is too high, or we got unlucky.
        raise Exception("Eviction cycle detected! Table must be resized/rehashed.")

    def display(self):
        print("\n--- Cuckoo Hash Table State ---")
        for i in range(self.capacity):
            t1 = self.table1[i][0] if self.table1[i] else "Empty"
            t2 = self.table2[i][0] if self.table2[i] else "Empty"
            print(f"Index {i:2} | Table 1: {t1:10} | Table 2: {t2:10}")

def demonstrate_cuckoo():
    section_header("Algorithm: Cuckoo Hashing")
    
    ht = CuckooHashTable(capacity=5)
    
    print("Inserting 'Apple'...")
    ht.put("Apple", 100)
    
    print("Inserting 'Banana'...")
    ht.put("Banana", 200)
    
    print("Inserting 'Orange'...")
    # Because capacity is 5, the chances of collision are very high.
    # We will likely see a Cuckoo eviction happen!
    ht.put("Orange", 300)
    
    print("Inserting 'Grape'...")
    ht.put("Grape", 400)
    
    ht.display()
    
    print("\nRetrieving 'Banana'...")
    val = ht.get("Banana")
    print(f"Value: {val}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Cuckoo Hashing guarantee O(1) worst-case lookup time?
   Answer: Unlike Linear Probing (which might check 50 slots before finding the item or giving up), Cuckoo Hashing strictly restricts an item to exactly TWO possible indices (`Table1[Hash1]` or `Table2[Hash2]`). A search operation only ever checks exactly those two memory locations.

2. What is an Eviction Cycle?
   Answer: During insertion, A kicks out B. B kicks out C. C kicks out D. D hashes to the exact same spot that A currently occupies! So D kicks out A. Now A is homeless again. If this loop continues infinitely, it's an eviction cycle. The table MUST be rebuilt with a larger capacity or new hash functions.

3. If Cuckoo Hashing has O(1) worst-case lookups, why doesn't Python use it for `dict`?
   Answer: While *lookups* are guaranteed O(1), *insertions* can be very slow due to long eviction chains or the need to completely rebuild the table if a cycle is detected. Standard Open Addressing (which Python uses) provides a much better balance of average-case speed for both lookups and insertions.
"""

if __name__ == "__main__":
    demonstrate_cuckoo()
    print("\n[SUCCESS] Laboratory: Cuckoo Hashing Completed.")
