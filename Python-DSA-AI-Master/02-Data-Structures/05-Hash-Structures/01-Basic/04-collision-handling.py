"""
Hash Collision Handling: Separate Chaining & Open Addressing

## Intuition & Real-World Analogy
Imagine a busy parking lot where spaces are assigned based on the last digit of your license plate. 
What happens when two cars arrive with plates ending in '7'? Both are told to park in spot #7.
This is a **Hash Collision**.

We have two main ways to solve this:
1. **Separate Chaining (The Valet Approach)**: Spot #7 is instead a valet stand. The valet simply takes both cars and parks them in a private lot designated for "Spot 7". Everyone assigned to 7 just gets added to this private lot (a linked list or array).
2. **Open Addressing (The Searcher Approach)**: You drive to spot #7 and see it's full. You just keep driving to the next spot (#8, then #9, etc.) until you find an empty one, and park there. 

## Formal Explanation
A hash function maps an infinite set of possible keys to a finite number of indices. By the **Pigeonhole Principle**, if you have more keys than available indices (or even fewer, due to uneven distribution), collisions are mathematically inevitable.

### Separate Chaining
- Each bucket in the hash table array stores a pointer to a secondary data structure (often a Linked List or a dynamic array).
- When inserting, we append to the list at the hashed index.
- When searching, we traverse the list at the hashed index to find the exact key.

### Open Addressing (Linear Probing)
- All elements are stored directly in the hash table array (no pointers to secondary structures).
- When a collision occurs, we systematically probe the next slots in the array (e.g., `(index + 1) % capacity`, `(index + 2) % capacity`) until an empty slot is found.
- Deletion in Open Addressing is tricky: we cannot simply make a slot empty, as it would break the search chain for elements probed past it. We must use a special **Tombstone** marker.

## Load Factor & Resizing
- **Load Factor (α)** = Number of Elements / Number of Buckets.
- Separate chaining can technically support α > 1, but performance degrades to O(N).
- Open addressing requires α < 1 (typically kept under 0.7).
- When the load factor exceeds a threshold, the table must be **resized** (typically doubled), and all elements **rehashed**.

## Memory Anchor
- **Chaining**: "Grow outwards" (lists in buckets). Memory is allocated dynamically.
- **Open Addressing**: "Move over" (find next empty slot). Cache-friendly but prone to clustering.
"""

from typing import Any, List, Optional, Tuple

# =============================================================================
# 1. Implementation: Separate Chaining
# =============================================================================

class ChainingHashTable:
    """
    Hash Table using Separate Chaining for collision resolution.
    For simplicity, we use Python lists (dynamic arrays) instead of linked lists 
    for the chains, which provides better cache locality in practice.
    """
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(capacity)]

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        # Check for update
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
                
        # Insert new
        bucket.append((key, value))
        self.size += 1
        # Note: In a production system, we'd check load factor and resize here

    def get(self, key: str) -> Optional[Any]:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key: str) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False


# =============================================================================
# 2. Implementation: Open Addressing (Linear Probing)
# =============================================================================

class Tombstone:
    """A marker to indicate a deleted slot in Open Addressing."""
    pass

TOMBSTONE = Tombstone()

class OpenAddressingHashTable:
    """
    Hash Table using Open Addressing (Linear Probing).
    Demonstrates the necessity of tombstones for deletion.
    """
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.keys: List[Optional[Any]] = [None] * capacity
        self.values: List[Optional[Any]] = [None] * capacity

    def _hash(self, key: str) -> int:
        return hash(key) % self.capacity

    def put(self, key: str, value: Any) -> None:
        if self.size >= self.capacity * 0.7:  # Resize threshold
            self._resize()

        idx = self._hash(key)
        first_tombstone_idx = None
        
        # Linear probing
        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                # Update existing
                self.values[idx] = value
                return
            
            if self.keys[idx] is TOMBSTONE and first_tombstone_idx is None:
                first_tombstone_idx = idx
                
            idx = (idx + 1) % self.capacity

        # Insert at the first found tombstone, or the empty slot we stopped at
        insert_idx = first_tombstone_idx if first_tombstone_idx is not None else idx
        
        self.keys[insert_idx] = key
        self.values[insert_idx] = value
        self.size += 1

    def get(self, key: str) -> Optional[Any]:
        idx = self._hash(key)
        
        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                return self.values[idx]
            idx = (idx + 1) % self.capacity
            
        return None

    def remove(self, key: str) -> bool:
        idx = self._hash(key)
        
        while self.keys[idx] is not None:
            if self.keys[idx] == key:
                # Replace with tombstone, NOT None!
                self.keys[idx] = TOMBSTONE
                self.values[idx] = None
                self.size -= 1
                return True
            idx = (idx + 1) % self.capacity
            
        return False

    def _resize(self) -> None:
        """Doubles capacity and rehashes all elements."""
        old_keys = self.keys
        old_values = self.values
        
        self.capacity *= 2
        self.size = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        
        for k, v in zip(old_keys, old_values):
            if k is not None and k is not TOMBSTONE:
                self.put(k, v)


# =============================================================================
# 3. Complexity Analysis
# =============================================================================
# | Approach           | Time (Average) | Time (Worst Case) | Space         |
# |--------------------|----------------|-------------------|---------------|
# | Separate Chaining  | O(1)           | O(N)              | O(N + M)      |
# | Open Addressing    | O(1)           | O(N)              | O(M)          |
# (Where N = number of keys, M = number of buckets/slots)
#
# Note on Worst Case: Occurs if the hash function maps all keys to the same bucket (Chaining) 
# or causes severe clustering (Open Addressing).

# =============================================================================
# 4. Common Mistakes & Debugging
# =============================================================================
# 1. Forgetting Tombstones in Open Addressing: If you set a deleted slot to `None`,
#    future searches for items that probed past this slot will prematurely stop!
# 2. Infinite Loops in Open Addressing: If the table becomes completely full, 
#    linear probing will loop infinitely. Always enforce a max Load Factor (e.g., 0.7).
# 3. Un-hashable Keys: Trying to use a mutable object (like a list) as a key 
#    violates the hash contract, as its hash would change upon mutation.

# =============================================================================
# 5. Active Recall & Self-Test
# =============================================================================
# Q: Why does Open Addressing have better CPU cache performance than Chaining?
# A: Elements are stored sequentially in memory (arrays), minimizing cache misses.
#    Chaining requires pointer hopping to disjoint memory locations.
#
# Q: When is Separate Chaining preferred over Open Addressing?
# A: When the size of the dataset is unknown/highly variable, and deletion is frequent.

def run_tests():
    print("Testing Separate Chaining...")
    chain_ht = ChainingHashTable(capacity=5)
    chain_ht.put("Alice", 90)
    chain_ht.put("Bob", 85)
    chain_ht.put("Charlie", 95)
    
    assert chain_ht.get("Alice") == 90
    assert chain_ht.get("Bob") == 85
    assert chain_ht.get("Dave") is None
    
    chain_ht.put("Alice", 100)  # Update
    assert chain_ht.get("Alice") == 100
    
    assert chain_ht.remove("Bob") is True
    assert chain_ht.get("Bob") is None
    print("Separate Chaining tests passed.")

    print("Testing Open Addressing...")
    oa_ht = OpenAddressingHashTable(capacity=4)  # Small capacity to force resize
    oa_ht.put("X", 1)
    oa_ht.put("Y", 2)
    oa_ht.put("Z", 3)
    
    # Should have triggered a resize since 3/4 = 0.75 > 0.7
    assert oa_ht.capacity == 8
    
    assert oa_ht.get("X") == 1
    assert oa_ht.get("Y") == 2
    
    # Test Tombstone mechanics
    oa_ht.remove("X")
    assert oa_ht.get("X") is None
    # Y and Z should still be accessible even if they probed past X initially
    assert oa_ht.get("Y") == 2
    assert oa_ht.get("Z") == 3
    
    oa_ht.put("W", 4)
    assert oa_ht.get("W") == 4
    print("Open Addressing tests passed.")

if __name__ == "__main__":
    run_tests()
    print("\nAll collision handling tests passed successfully!")
