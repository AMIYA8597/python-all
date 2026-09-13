"""
# ==============================================================================
# LABORATORY: DOUBLY LINKED LISTS & LRU CACHE
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Singly Linked List is great, but you can only traverse it forward. If you 
# are at Node C and need to delete it, you don't know who Node B is! 
# Doubly Linked Lists (DLL) solve this by storing both `next` and `prev` pointers.
# This makes deletion O(1) if you have the node, which is the foundational secret 
# behind the famous LRU Cache algorithm used in databases and web browsers.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a Doubly Linked List Node (`prev`, `next`, `data`).
# - Master O(1) node deletion and insertion.
# - Combine a Hash Map and a Doubly Linked List to build an LRU Cache.
#
# ==============================================================================
"""

from typing import Any, Optional, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DOUBLY LINKED LIST IMPLEMENTATION
# ==============================================================================
class DNode:
    def __init__(self, key: Any, val: Any):
        self.key = key
        self.val = val
        self.prev: Optional['DNode'] = None
        self.next: Optional['DNode'] = None

class DoublyLinkedList:
    def __init__(self):
        # We use dummy Head and Tail nodes. This completely eliminates 
        # edge cases like "what if the list is empty?" or "what if we delete the head?"
        self.head = DNode(None, None)
        self.tail = DNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def add_to_front(self, node: DNode):
        """Adds a node immediately after the dummy head. (O(1))"""
        # Save the current first real node
        first_real = self.head.next
        
        # Wire the new node to the head
        self.head.next = node
        node.prev = self.head
        
        # Wire the new node to the old first node
        node.next = first_real
        if first_real:
            first_real.prev = node
            
    def remove_node(self, node: DNode):
        """Removes a SPECIFIC node from the list. (O(1))"""
        # Because we have `prev` and `next`, we don't need to traverse the list 
        # to find the node's parent! We just wire the neighbors together.
        prev_node = node.prev
        next_node = node.next
        
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node
            
    def pop_tail(self) -> Optional[DNode]:
        """Removes and returns the last real node (before the dummy tail)."""
        if self.head.next == self.tail:
            return None # List is empty
            
        last_real = self.tail.prev
        if last_real:
            self.remove_node(last_real)
        return last_real
        
    def display(self):
        elements = []
        curr = self.head.next
        while curr != self.tail and curr is not None:
            elements.append(f"[{curr.key}:{curr.val}]")
            curr = curr.next
        print(" <-> ".join(elements))

def demonstrate_dll():
    section_header("Doubly Linked List Mechanics")
    dll = DoublyLinkedList()
    
    n1 = DNode("A", 1)
    n2 = DNode("B", 2)
    n3 = DNode("C", 3)
    
    print("Adding A, B, C to the front:")
    dll.add_to_front(n1)
    dll.add_to_front(n2)
    dll.add_to_front(n3)
    dll.display() # Should be C <-> B <-> A
    
    print("\nRemoving middle node (B) in O(1) time:")
    dll.remove_node(n2)
    dll.display() # Should be C <-> A


# ==============================================================================
# 4. CLASSIC ALGORITHM: LRU CACHE
# ==============================================================================
class LRUCache:
    """
    LeetCode #146: LRU Cache (Hard)
    We must achieve O(1) get() and O(1) put().
    
    SECRET:
    - We use a Hash Map (Dictionary) for O(1) lookups.
    - We use a Doubly Linked List for O(1) ordering (Most Recently Used at the front, 
      Least Recently Used at the back).
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[Any, DNode] = {}
        self.dll = DoublyLinkedList()
        
    def get(self, key: Any) -> int:
        if key not in self.cache:
            return -1
            
        # 1. Fetch the node from the hash map (O(1))
        node = self.cache[key]
        
        # 2. Because it was just used, move it to the front of the DLL (O(1))
        self.dll.remove_node(node)
        self.dll.add_to_front(node)
        
        return node.val
        
    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.val = value
            self.dll.remove_node(node)
            self.dll.add_to_front(node)
        else:
            # Create new node
            new_node = DNode(key, value)
            self.cache[key] = new_node
            self.dll.add_to_front(new_node)
            
            # Check capacity
            if len(self.cache) > self.capacity:
                # Remove the Least Recently Used (LRU) node from the tail
                lru_node = self.dll.pop_tail()
                if lru_node:
                    del self.cache[lru_node.key]

    def display_cache(self):
        print(f"Cache state (Size: {len(self.cache)}/{self.capacity}):")
        self.dll.display()

def demonstrate_lru_cache():
    section_header("Algorithm: LRU Cache")
    
    lru = LRUCache(3)
    
    print("Putting A, B, C:")
    lru.put("A", 1)
    lru.put("B", 2)
    lru.put("C", 3)
    lru.display_cache()
    
    print("\nReading 'A' (moves A to the front):")
    print(f"Read A: {lru.get('A')}")
    lru.display_cache()
    
    print("\nPutting 'D' (Cache is full! Will evict the LRU, which is 'B'):")
    lru.put("D", 4)
    lru.display_cache()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the primary advantage of a Doubly Linked List over a Singly Linked List?
   Answer: In a Singly Linked List, if you are given a specific Node and told to delete it, you can't, because you don't know the Node BEFORE it to bypass it. You have to traverse from the head (O(N)). In a DLL, you have a `prev` pointer, so you can delete the node instantly in O(1) time.

2. Why do we use dummy Head and Tail nodes?
   Answer: It eliminates Edge Cases. You never have to write `if node == head:` or `if not head:`. You just insert between the dummy nodes safely.

3. How does an LRU Cache achieve O(1) reads and writes?
   Answer: It combines two structures. A Hash Map maps a key to a specific DNode in memory (providing O(1) lookups). A Doubly Linked List maintains the order of usage. When a node is accessed via the Hash Map, the DLL deletes it from its current position and moves it to the front in O(1) time.
"""

if __name__ == "__main__":
    demonstrate_dll()
    demonstrate_lru_cache()
    print("\n[SUCCESS] Laboratory: Doubly Linked Lists Completed.")
