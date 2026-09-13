"""
# ==============================================================================
# LABORATORY: PERSISTENT DATA STRUCTURES & IMMUTABILITY
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In highly concurrent systems or functional programming (e.g., Haskell, Clojure), 
# mutating data in place is considered dangerous because it causes race conditions 
# across threads. "Persistent" data structures (meaning Immutable, not database 
# persistence) solve this. When you "modify" a persistent list, it returns a 
# brand new list while leaving the old one untouched, but uses "Structural Sharing" 
# to ensure it takes O(1) time and minimal memory instead of O(N) copying.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Copying and Structural Sharing.
# - Implement an Immutable (Persistent) Singly Linked List.
# - Understand how "prepending" achieves O(1) immutability.
#
# ==============================================================================
"""

from typing import Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STRUCTURAL SHARING VS COPYING
# ==============================================================================

def demonstrate_structural_sharing_concept():
    """
    Standard Python lists do not support structural sharing. 
    If you want an immutable list modification, you must copy the entire array (O(N)).
    """
    section_header("The O(N) Copy Problem")
    
    version1 = [1, 2, 3, 4, 5]
    print(f"Version 1: {version1}")
    
    # We want to prepend '0' but keep version1 intact.
    # In Python arrays, we MUST allocate a brand new list and copy all elements.
    version2 = [0] + version1 
    print(f"Version 2: {version2}")
    
    print("\nThis requires O(N) time and O(N) extra memory.")
    print("If the list had 1 million items, this would be a catastrophic operation.")


# ==============================================================================
# 4. IMPLEMENTING A PERSISTENT LINKED LIST
# ==============================================================================
class PNode:
    """A Node for our Persistent List. Once created, it CANNOT be modified."""
    __slots__ = ['val', 'next'] # Memory optimization
    
    def __init__(self, val: Any, next_node: Optional['PNode'] = None):
        self.val = val
        self.next = next_node

class PersistentList:
    """
    An Immutable Singly Linked List.
    Notice there are NO methods that mutate the state (no `append`, no `remove`).
    Every operation returns a NEW PersistentList object.
    """
    def __init__(self, head: Optional[PNode] = None):
        self.head = head
        
    def prepend(self, val: Any) -> 'PersistentList':
        """
        O(1) Immutable Prepend using STRUCTURAL SHARING.
        We create a new node, point its `next` to the CURRENT list's head, 
        and return a new list wrapper. 
        The original list is untouched, and we only allocated 1 new Node!
        """
        new_node = PNode(val, self.head)
        return PersistentList(new_node)
        
    def tail(self) -> 'PersistentList':
        """
        O(1) Immutable slice. Returns a new list containing everything EXCEPT 
        the first element.
        """
        if not self.head:
            raise IndexError("tail of empty list")
        return PersistentList(self.head.next)
        
    def display(self) -> str:
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.val))
            curr = curr.next
        return " -> ".join(elements) + " -> None"

def demonstrate_persistent_list():
    section_header("Persistent List (Structural Sharing)")
    
    # We start with an empty list
    v0 = PersistentList()
    print(f"v0: {v0.display()}")
    
    # We "modify" the list. This returns a NEW list.
    v1 = v0.prepend(3)
    v2 = v1.prepend(2)
    v3 = v2.prepend(1)
    
    print("\nWe built the list up to v3:")
    print(f"v3: {v3.display()}")
    
    print("\nBut wait... do v1 and v2 still exist perfectly intact?")
    print(f"v1: {v1.display()}")
    print(f"v2: {v2.display()}")
    
    print("\nYes! They all share the exact same underlying memory nodes.")
    print("v3's node (1) simply points to v2's node (2).")
    
    print("\nTaking the tail of v3:")
    v4 = v3.tail()
    print(f"v4 (v3.tail): {v4.display()}")
    print(f"Notice that v4 is exactly identical to v2.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does it mean for a data structure to be "Persistent"?
   Answer: In the context of Functional Programming, a persistent data structure always preserves the previous version of itself when it is modified. It is immutable.

2. How do persistent data structures achieve O(1) performance if they must create a new version of the structure every time?
   Answer: They use Structural Sharing. Instead of copying the entire dataset, the new version only allocates memory for the single new element (e.g., prepending a Node), and then points to the existing, immutable data structure for the rest of the data.

3. Why can't you efficiently "append" to the end of a persistent singly linked list?
   Answer: Because structural sharing only works from the front. If you append to the end, you must alter the `next` pointer of the last node. Since nodes are immutable, you would have to recreate the last node, which means you have to recreate its parent, and its parent, all the way back to the head (O(N) copy).
"""

if __name__ == "__main__":
    demonstrate_structural_sharing_concept()
    demonstrate_persistent_list()
    print("\n[SUCCESS] Laboratory: Persistent Lists Completed.")
