"""
# ==============================================================================
# LABORATORY: CONCURRENT HASH TABLES & LOCK STRIPING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you build a multi-threaded web server, multiple threads might try to read 
# and write to a shared dictionary at the exact same time. 
#
# Python's built-in `dict` is *mostly* thread-safe due to the Global Interpreter 
# Lock (GIL). A single `dict.update()` or `dict[key] = val` is atomic. 
# However, "Check-Then-Act" operations (e.g., "If key not in dict, add it") are NOT 
# atomic! Thread A checks, pauses. Thread B checks, adds it. Thread A wakes up 
# and overwrites it! This is a Race Condition.
#
# To fix this, you can wrap the dictionary in a `threading.Lock()`. But this creates 
# a massive bottleneck. If Thread A is updating "Apple", it locks the ENTIRE 
# dictionary, forcing Thread B to wait even if B just wants to read "Banana"!
#
# The advanced solution is "Lock Striping" (used in Java's ConcurrentHashMap). 
# Instead of 1 giant lock, we use an array of 16 smaller locks. We hash the key 
# to figure out which "stripe" (bucket) it belongs to, and only lock that specific 
# section of the dictionary!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Check-Then-Act race conditions.
# - Understand the bottleneck of a single Coarse-Grained Lock.
# - Implement a highly concurrent Hash Table using Lock Striping (Fine-Grained).
#
# ==============================================================================
"""

import threading
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RACE CONDITIONS IN STANDARD DICTS
# ==============================================================================
def explain_race_conditions():
    section_header("Concept: The Check-Then-Act Race Condition")
    print("""
Even with Python's GIL, this common code pattern is DANGEROUS in multi-threading:

```python
if key not in cache:            <-- Context Switch happens here!
    cache[key] = expensive_db_query()
```

1. Thread 1 checks if "User_123" is in the cache. It's not.
2. The OS pauses Thread 1.
3. Thread 2 checks if "User_123" is in the cache. It's not.
4. Thread 2 runs the expensive DB query and caches the result.
5. Thread 1 wakes up. It doesn't check the cache again! It runs the expensive 
   DB query a SECOND time, completely defeating the purpose of the cache!

To fix this, the check AND the write must be wrapped in a single Lock.
    """)


# ==============================================================================
# 4. IMPLEMENTING LOCK STRIPING (CONCURRENTHASHMAP)
# ==============================================================================
class ConcurrentHashMap:
    """
    A highly concurrent Hash Table using Lock Striping.
    We maintain a standard Python dictionary, but we protect it with multiple locks.
    """
    def __init__(self, num_stripes: int = 16):
        self.dict: dict[str, int] = {}
        self.num_stripes = num_stripes
        
        # An array of individual locks!
        self.locks = [threading.Lock() for _ in range(num_stripes)]

    def _get_lock(self, key: str) -> threading.Lock:
        """Hashes the key to find out WHICH specific lock protects it."""
        lock_index = hash(key) % self.num_stripes
        return self.locks[lock_index]

    def safe_increment(self, key: str) -> None:
        """
        Thread-safe Check-Then-Act increment.
        Crucially, if Thread A locks "Apple" (Stripe 2), Thread B can simultaneously 
        increment "Banana" if it hashes to Stripe 7! Zero waiting!
        """
        lock = self._get_lock(key)
        
        with lock:
            # We are now in a perfectly atomic block, but ONLY for this specific stripe!
            if key in self.dict:
                # Simulate a tiny delay that would normally cause massive race conditions
                current = self.dict[key]
                time.sleep(0.0001) 
                self.dict[key] = current + 1
            else:
                self.dict[key] = 1

def demonstrate_lock_striping():
    section_header("Algorithm: Lock Striping (Fine-Grained Locking)")
    
    # We will simulate 10 threads trying to increment the exact same keys
    chm = ConcurrentHashMap(num_stripes=8)
    keys_to_increment = ["Apple", "Banana", "Orange", "Apple", "Banana", "Orange"]
    
    def worker(worker_id: int, iterations: int):
        for _ in range(iterations):
            for key in keys_to_increment:
                chm.safe_increment(key)
                
    threads = []
    print("Launching 10 threads. Each thread will increment Apple, Banana, Orange 100 times.")
    print("Expected final count for each fruit: 10 * 100 * (occurrences in list).")
    print("Apple should be 2000. Banana should be 2000. Orange should be 2000.\n")
    
    # Launch threads
    for i in range(10):
        t = threading.Thread(target=worker, args=(i, 100))
        threads.append(t)
        t.start()
        
    # Wait for all to finish
    for t in threads:
        t.join()
        
    print("Final Dictionary State:")
    for k, v in chm.dict.items():
        print(f" {k:10}: {v}")
        
    print("\nBecause we used Lock Striping, the counts are absolutely perfect, AND")
    print("the threads didn't bottleneck each other when accessing different fruits!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between Coarse-Grained and Fine-Grained Locking?
   Answer: Coarse-grained locking uses a single `threading.Lock()` to protect an entire data structure (like Python's GIL). It is easy to write, but creates massive bottlenecks because Thread B must wait for Thread A, even if they are touching completely unrelated data. Fine-grained locking uses an array of locks, allowing parallel modifications as long as the hashes map to different locks.

2. Why is Python's standard `dict[key] = value` considered thread-safe?
   Answer: The Global Interpreter Lock (GIL) physically prevents two Python bytecodes from executing at the same time. Variable assignment maps to a single bytecode instruction in CPython. Therefore, simple writes can never be interrupted halfway through. However, compound operations (Check-Then-Act) map to multiple bytecodes, allowing context switches between them.

3. How does Java's `ConcurrentHashMap` work?
   Answer: It uses exactly this Lock Striping technique! It breaks the internal array into segments (typically 16). When a thread writes to the map, it only locks the specific segment the key belongs to, allowing up to 16 threads to write to the map completely in parallel.
"""

if __name__ == "__main__":
    explain_race_conditions()
    demonstrate_lock_striping()
    print("\n[SUCCESS] Laboratory: Concurrent Hash Tables Completed.")
