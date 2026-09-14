"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (CACHE EVICTION & LRU)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, we built a Cache-Aside mechanism. It was fast.
# But there is a fatal physical reality: A SQL Database uses Hard Drives (SSD/HDD), 
# which can easily store 10,000 GB of data. 
# A Cache (Redis/Memcached) uses pure RAM. RAM is incredibly expensive. You 
# might only have 16 GB of RAM available.
#
# What happens when you try to cache 17 GB of data into 16 GB of RAM?
# The server crashes with an Out-Of-Memory (OOM) error.
#
# To prevent this, Caches MUST have an "Eviction Policy". When the cache is 
# mathematically full, it must intelligently delete old data to make room for 
# new data.
#
# The most famous algorithm in the world for this is LRU (Least Recently Used). 
# It deletes whatever data has not been touched in the longest amount of time.
# To implement LRU in strict O(1) time, you cannot use a simple array. You MUST 
# combine a Hash Map with a Doubly Linked List!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Cache Eviction limits.
# - Master the architecture of the O(1) LRU Cache (Hash Map + Doubly Linked List).
# - Differentiate Write-Through vs Write-Back caching.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LRU CACHE (LEAST RECENTLY USED) O(1)
# ==============================================================================
class ListNode:
    """A Node in our Doubly Linked List."""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Combines a Hash Map (for O(1) lookups) with a Doubly Linked List (for O(1) 
    order manipulation) to achieve an unbreakable O(1) Eviction engine.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        # Hash Map: Key -> ListNode pointer
        self.cache = {}
        
        # Dummy Head and Tail to avoid complex Edge Case null-checks
        self.head = ListNode(-1, -1)
        self.tail = ListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node_to_front(self, node: ListNode) -> None:
        """Always insert new or recently used nodes right after the Dummy Head!"""
        node.prev = self.head
        node.next = self.head.next
        
        # Wire the surrounding nodes to point to our new node
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: ListNode) -> None:
        """Rips a node out of the Linked List in O(1) time."""
        prev_node = node.prev
        next_node = node.next
        
        # Stitch the surrounding nodes together, bypassing the target node!
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_front(self, node: ListNode) -> None:
        """When a node is accessed, it must be violently moved to the front!"""
        self._remove_node(node)
        self._add_node_to_front(node)

    def _pop_tail(self) -> ListNode:
        """The absolute oldest, least recently used node is right before the Dummy Tail."""
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
            
        node = self.cache[key]
        # Because we accessed it, it is no longer the "Least Recently Used"!
        # Move it to the front of the line!
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # It already exists! Update the value and move to front!
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            # It's a brand new piece of data!
            new_node = ListNode(key, value)
            self.cache[key] = new_node
            self._add_node_to_front(new_node)
            
            # THE EVICTION TRIGGER!
            # Did we just exceed our physical RAM capacity?
            if len(self.cache) > self.capacity:
                # We must evict the Least Recently Used node (The Tail!)
                evicted_node = self._pop_tail()
                # We MUST also delete it from the Hash Map!
                del self.cache[evicted_node.key]

def demonstrate_lru_cache():
    section_header("LRU Cache Architecture")
    
    # We only have enough RAM for exactly 2 items!
    cache = LRUCache(2)
    print("LRU Cache initialized with Capacity = 2")
    
    print("\nAction: put(1, 100)")
    cache.put(1, 100)
    print("Action: put(2, 200)")
    cache.put(2, 200)
    
    # State: [2, 1]. 2 is the most recent.
    
    print(f"\nAction: get(1) -> Returns: {cache.get(1)}")
    # By GETTING 1, 1 is violently moved to the front! 
    # State: [1, 2]. 2 is now the Least Recently Used!
    print("[Internal Engine]: Key 1 was moved to the front. Key 2 is now the LRU at the back!")
    
    print("\nAction: put(3, 300) -> CACHE IS FULL! EVICTION TRIGGERED!")
    cache.put(3, 300)
    # State: [3, 1]. 2 was evicted!
    
    print(f"Action: get(2) -> Returns: {cache.get(2)}")
    print("Why -1? Because Key 2 was evicted to make room for Key 3!")


# ==============================================================================
# 4. WRITE-THROUGH VS WRITE-BACK
# ==============================================================================
def write_through_strategy(cache, database, key, value):
    """
    Write-Through:
    When the user saves data, we write it to the Cache AND the Database simultaneously.
    Pro: Data is 100% mathematically consistent. If the Cache crashes, no data is lost.
    Con: It is SLOW. The user must wait for the slow SQL disk write to finish.
    """
    cache.put(key, value)      # Fast (RAM)
    database.write(key, value) # Slow (Disk)
    return "Saved Successfully (Slow but Safe!)"

def write_back_strategy(cache, database, key, value):
    """
    Write-Back:
    When the user saves data, we ONLY write it to the Cache! We immediately return Success!
    A background asynchronous thread eventually writes the Cache data to the Database.
    Pro: Blindingly FAST. User experiences 0ms latency.
    Con: DANGEROUS. If the Cache server loses power before the background thread runs, 
         the data is permanently destroyed.
    """
    cache.put(key, value) # Fast (RAM)
    # Async process takes over later...
    return "Saved Successfully (Instant but Dangerous!)"


def run_all_labs():
    demonstrate_lru_cache()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a Hash Map alone mathematically insufficient to build an LRU Cache?
   Answer: A standard Hash Map provides $O(1)$ lookup time, but Hash Maps completely lack the concept of chronologically ordered "Time". They cannot track *when* an item was accessed relative to other items. To find the "Least Recently Used" item in a pure Hash Map, you would have to attach a timestamp to every entry, and then write an $O(N)$ `for` loop to scan the entire Map and find the oldest timestamp. By fusing the Hash Map with a Doubly Linked List, the List mathematically tracks the chronological order (Head = Newest, Tail = Oldest). The Hash Map stores direct pointers to the List Nodes, allowing $O(1)$ teleportation into the middle of the List to pull nodes to the front.

2. In the LRU Doubly Linked List, why do we initialize a "Dummy Head" and a "Dummy Tail"?
   Answer: Edge Case Elimination! If the Linked List is completely empty, and you try to insert the first node, you have to write complex `if head is None: head = node; tail = node` logic. If you delete the last node, you have to handle `head = None`. This creates spaghetti code prone to Null Pointer Exceptions. By initializing a Dummy Head and a Dummy Tail that are permanently glued to the ends of the list, the list is *never* physically empty. Every real node you insert is mathematically guaranteed to have a valid `prev` and `next` node. You never have to write a single `if node is None:` check in your $O(1)$ removal logic!

3. Compare Write-Through and Write-Back caching strategies. When would you use Write-Back?
   Answer: Write-Through writes to both the Cache (RAM) and the Database (Disk) synchronously. The user waits for the Disk. This guarantees strict Consistency and durability (e.g., Banking transactions). Write-Back writes ONLY to the Cache (RAM), immediately tells the user "Success!", and syncs to Disk later in the background. Write-Back is incredibly fast but risks catastrophic data loss if the RAM loses power. You use Write-Back for extremely high-volume, low-criticality systems—for example, updating a YouTube video's View Count. If a server crashes and we permanently lose 50 views out of 10 Million, no one cares, and the server handled the massive burst of traffic efficiently.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Cache Eviction) Completed.")
