"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - SYSTEMS DESIGN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Design an In-Memory LRU (Least Recently Used) Cache that supports 
# both `get(key)` and `put(key, value)` in absolute O(1) Time."
#
# A junior engineer uses a standard Python Array or List. When the cache is full, 
# they use `list.pop(0)` to remove the oldest item. Because `pop(0)` forces a 
# physical memory shift of every remaining element in RAM, `put()` degrades to 
# O(N) time. Under high server load, the cache becomes the bottleneck and crashes.
#
# A senior engineer knows the master architecture: A Hash Map permanently fused 
# to a Doubly-Linked List. The Hash Map provides the O(1) instantaneous lookup. 
# The Doubly-Linked List provides O(1) pointer-swapping to instantly move any 
# accessed Node to the 'Most Recently Used' head of the list without shifting 
# any memory!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the physical architecture of the LRU Cache.
# - Understand the synergy between Hash Maps and Doubly-Linked Lists.
# - Master the mathematical manipulation of Pointers to achieve O(1) speed.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LRU CACHE (THE HASH-MAP + DOUBLY-LINKED LIST SYNERGY)
# ==============================================================================
class ListNode:
    """
    A single cell in the Doubly-Linked List.
    It MUST store BOTH Key and Value! If it only stored Value, we wouldn't know 
    which Key to delete from the Hash Map when removing the LRU node!
    """
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # The Hash Map for O(1) retrieval! Key -> ListNode
        self.cache = {}
        
        # Dummy Head (Most Recently Used / MRU)
        self.head = ListNode(0, 0)
        # Dummy Tail (Least Recently Used / LRU)
        self.tail = ListNode(0, 0)
        
        # Connect the dummies!
        self.head.next = self.tail
        self.tail.prev = self.head

    def _insert_right(self, node: ListNode) -> None:
        """
        O(1) Memory Pointer Manipulation.
        Inserts a node EXACTLY before the Tail (making it the Newest MRU).
        """
        prev_node = self.tail.prev
        
        # Wire the new node
        node.prev = prev_node
        node.next = self.tail
        
        # Wire the surroundings
        prev_node.next = node
        self.tail.prev = node
        
    def _remove(self, node: ListNode) -> None:
        """
        O(1) Memory Pointer Manipulation.
        Physically detaches a node from the Doubly-Linked List by wiring its 
        neighbors directly to each other.
        """
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def get(self, key: int) -> int:
        """Time: O(1)"""
        if key in self.cache:
            # We accessed it, so it is now the MOST recently used!
            node = self.cache[key]
            
            # 1. Remove it from its current physical position
            self._remove(node)
            # 2. Re-insert it at the very right (before the Tail)
            self._insert_right(node)
            
            print(f"    [GET] Key {key} retrieved! Value: {node.value}. Promoted to MRU.")
            return node.value
            
        print(f"    [GET] Key {key} NOT FOUND (Cache Miss).")
        return -1

    def put(self, key: int, value: int) -> None:
        """Time: O(1)"""
        if key in self.cache:
            # The key already exists! 
            # We must update the value AND promote it to MRU!
            node = self.cache[key]
            self._remove(node)
            del self.cache[key]
            
        # Create the new Node!
        new_node = ListNode(key, value)
        self.cache[key] = new_node
        self._insert_right(new_node)
        print(f"    [PUT] Key {key} inserted with Value {value}. Promoted to MRU.")
        
        # THE CAPACITY EVICTION ENGINE
        if len(self.cache) > self.capacity:
            # The true LRU node is the one immediately AFTER the Dummy Head!
            lru_node = self.head.next
            
            print(f"    [EVICT] Capacity {self.capacity} exceeded! Evicting LRU Key {lru_node.key}.")
            
            # Physically detach it from the list
            self._remove(lru_node)
            # Mathematically delete it from the Hash Map!
            del self.cache[lru_node.key]


def demonstrate_lru():
    section_header("LRU Cache Implementation")
    
    print("Initializing LRU Cache with Capacity = 2\n")
    lru = LRUCache(2)
    
    lru.put(1, 100) # Cache: [1]
    lru.put(2, 200) # Cache: [1, 2]
    
    # Retrieves 1, making it the MRU. Cache is now mathematically [2, 1]
    lru.get(1)
    
    # Capacity is exceeded! The LRU is 2. It will be brutally evicted.
    lru.put(3, 300) # Cache: [1, 3]
    
    # Returns -1 (Not Found)
    lru.get(2)
    
    lru.put(4, 400) # Evicts Key 1! Cache: [3, 4]
    
    lru.get(1) # Returns -1 (Not Found)
    lru.get(3) # Returns 300
    lru.get(4) # Returns 400


def run_all_labs():
    demonstrate_lru()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we absolutely need a Doubly-Linked List for the LRU Cache? Why not a Singly-Linked List?"
   Senior Answer: "If we used a Singly-Linked List, we could easily move the Head to the Tail. However, when we do `get(key)`, the Hash Map gives us the exact physical memory pointer to the Node. To promote this Node to the MRU position, we must physically detach it from the middle of the list. In a Singly-Linked List, you only have a `next` pointer. You have absolutely no way to access the node *behind* the current node to rewire its `next` pointer, forcing you to traverse the entire list from the Head to find it ($O(N)$). A Doubly-Linked List contains a `prev` pointer, allowing us to instantly rewire the surrounding nodes in strict $O(1)$ constant time without traversal."

2. Interviewer: "Why does the `ListNode` class need to store the `key`? Since the Hash Map already stores the mapping `Key -> Node`, isn't storing the `key` inside the Node redundant?"
   Senior Answer: "It is not redundant; it is structurally mandatory for the Eviction Engine. When the cache hits maximum capacity, we look at the Doubly-Linked List to find the LRU node (the one directly next to the Dummy Head). We easily physically detach it from the list in $O(1)$ time. However, to keep the cache consistent, we MUST also delete that entry from the Hash Map! The Hash Map requires a `key` to delete an entry (`del map[key]`). If the LRU node only stored its `value` and not its `key`, we would have absolutely no idea which Hash Map entry to delete! Storing the `key` inside the Node acts as a mathematical reverse-lookup."

3. Interviewer: "Why do we use two 'Dummy' nodes (Head and Tail) initialized to 0, instead of just using raw `head` and `tail` pointers that start as `None`?"
   Senior Answer: "If you don't use Dummy nodes, the pointer manipulation code (`_insert` and `_remove`) becomes a horrific mess of Edge Case `if/else` checks. You have to constantly ask: 'Is the list empty? Am I deleting the absolute Head? Am I inserting at the absolute Tail?' By permanently anchoring the list with unbreakable Dummy Head and Dummy Tail nodes, the list is *never* mathematically empty. The `prev` and `next` pointers are guaranteed to always exist. This brilliantly collapses the complex pointer rewiring logic into exactly 4 unconditional lines of code, mathematically immune to `NullReference` exceptions."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Systems Design Patterns) Completed.")
