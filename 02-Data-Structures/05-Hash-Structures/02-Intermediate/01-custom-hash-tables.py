"""
# ==============================================================================
# LABORATORY: ORDERED HASH TABLES (PYTHON 3.7+ ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Hash Tables map keys to array indices using random mathematical 
# operations (`hash(key) % capacity`). Because the index is essentially random, 
# iterating through a standard Hash Table yields the keys in a completely 
# unpredictable, chaotic order.
#
# However, starting in Python 3.7, `dict` magically remembers the EXACT ORDER 
# you inserted the keys! How is this mathematically possible if the hash scatters 
# them randomly?
#
# It is achieved by combining TWO data structures:
# 1. A dense array (or Doubly Linked List) that stores the actual Key-Value pairs 
#    in strict sequential order of insertion.
# 2. A sparse Hash Table that ONLY stores the INTEGER INDEX (or pointer) of where 
#    that Key-Value pair lives in the dense array.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the memory layout of an Ordered Dictionary.
# - Implement a custom Ordered Hash Table using a Doubly Linked List backbone.
# - Achieve O(1) lookup, O(1) insertion, and O(1) ordered iteration!
#
# ==============================================================================
"""

from typing import Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DOUBLY LINKED LIST NODE (THE ORDER PRESERVER)
# ==============================================================================
class Node:
    """A node that stores a Key-Value pair, and points to the next/prev inserted items."""
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


# ==============================================================================
# 4. ORDERED HASH TABLE IMPLEMENTATION
# ==============================================================================
class OrderedHashTable:
    """
    Combines a Python `dict` (acting as the sparse Hash Table) with a Doubly Linked List 
    (acting as the dense, ordered storage).
    Note: Python's actual C implementation uses arrays, but a DLL perfectly models 
    the logic and allows O(1) deletions without complex array shifting.
    """
    def __init__(self):
        # The Hash Table mapping Key -> Node Object memory reference
        self.map: dict[str, Node] = {}
        
        # Dummy head and tail for the Doubly Linked List (Simplifies edge cases)
        self.head = Node("HEAD", None)
        self.tail = Node("TAIL", None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def put(self, key: str, value: Any) -> None:
        """Inserts or updates a key. If new, it is appended to the END of the order."""
        if key in self.map:
            # If it already exists, just update the value. It keeps its original position in the order!
            self.map[key].value = value
            return
            
        # 1. Create a new Node
        new_node = Node(key, value)
        
        # 2. Store the Node reference in the Hash Table for O(1) future lookups
        self.map[key] = new_node
        
        # 3. Append the Node to the very end of the Doubly Linked List (before the TAIL)
        last_node = self.tail.prev
        last_node.next = new_node
        new_node.prev = last_node
        new_node.next = self.tail
        self.tail.prev = new_node

    def get(self, key: str) -> Any:
        """Retrieves a value in O(1) time."""
        if key not in self.map:
            raise KeyError(f"Key '{key}' not found.")
            
        # The Hash Table instantly gives us the exact memory reference of the Node
        return self.map[key].value

    def delete(self, key: str) -> None:
        """Deletes a key in O(1) time while perfectly maintaining the order of everything else."""
        if key not in self.map:
            raise KeyError(f"Key '{key}' not found.")
            
        # 1. Get the Node from the Hash Table
        node_to_delete = self.map[key]
        
        # 2. Delete it from the Hash Table
        del self.map[key]
        
        # 3. Excise the Node from the Doubly Linked List in O(1) time!
        prev_node = node_to_delete.prev
        next_node = node_to_delete.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def iterate_in_order(self) -> None:
        """Iterates through all items in the EXACT order they were inserted."""
        curr = self.head.next
        while curr != self.tail:
            print(f"  Key: {curr.key:10} | Value: {curr.value}")
            curr = curr.next

def demonstrate_ordered_dict():
    section_header("Algorithm: Ordered Hash Table (Insertion Order)")
    
    odt = OrderedHashTable()
    
    print("Inserting keys in a specific chaotic sequence:")
    print(" 1. 'Zebra'")
    print(" 2. 'Apple'")
    print(" 3. 'Monkey'")
    print(" 4. 'Banana'")
    
    odt.put("Zebra", 1)
    odt.put("Apple", 2)
    odt.put("Monkey", 3)
    odt.put("Banana", 4)
    
    print("\nIterating through the Hash Table (O(N)):")
    odt.iterate_in_order()
    
    print("\nIf this were an old Hash Table, the order would be completely random.")
    print("Because we used a Doubly Linked List backbone, it perfectly remembered the insertion order!")
    
    print("\nLet's delete 'Apple' (O(1) operation):")
    odt.delete("Apple")
    odt.iterate_in_order()
    
    print("\nLet's update 'Zebra' to 999. It should NOT move to the end of the list!")
    odt.put("Zebra", 999)
    odt.iterate_in_order()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does Python 3.7+ implement ordered dictionaries using arrays instead of Linked Lists?
   Answer: It maintains two arrays. Array 1 is the sparse Hash Table, containing ONLY integers. Array 2 is a dense, contiguous array of `(Key, Value)` tuples. When you insert a key, the tuple is strictly appended to the end of Array 2. Array 1 simply maps the Hash of the key to the integer index in Array 2!

2. What is the downside of the Python 3.7 array approach when DELETING an item?
   Answer: If you delete an item from the middle of the dense array, you can't just shift all the other items down, because that would ruin the integer indices stored in the Hash Table array (and take O(N) time). Python handles this by putting a "Tombstone" in the dense array. Periodically, when the dense array has too many tombstones, Python runs an O(N) compaction algorithm to rebuild the arrays.

3. Why did we use a Doubly Linked List in our implementation instead of an Array?
   Answer: Because a Doubly Linked List allows us to excise (delete) a node from the middle of the order in strictly O(1) time by just updating two pointers. It doesn't require tombstones or compaction phases. However, the DLL is slightly worse for CPU Caches than the array approach.
"""

if __name__ == "__main__":
    demonstrate_ordered_dict()
    print("\n[SUCCESS] Laboratory: Ordered Hash Tables Completed.")
