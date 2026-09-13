"""
# ==============================================================================
# LABORATORY: LOCK-FREE HASH TABLES & COMPARE-AND-SWAP (CAS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that `threading.Lock` protects dictionaries from race conditions. 
# Even with "Lock Striping", if a thread acquires a lock and then gets paused 
# by the OS, ALL other threads trying to access that stripe are completely blocked!
#
# High-performance systems (like OS kernels, Java's NonBlockingHashMap, or Redis 
# internals) cannot tolerate threads being blocked. They use "Lock-Free" algorithms.
#
# Lock-Free algorithms rely on a hardware-level CPU instruction called 
# Compare-And-Swap (CAS). CAS atomically says: "Update this memory address to 
# X, but ONLY if its current value is still exactly Y."
# If another thread modified the memory first, CAS fails, and our thread just 
# tries again in a tiny `while` loop. No threads are ever put to sleep!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the hardware-level Compare-And-Swap (CAS) instruction.
# - Understand how to build a Lock-Free Hash Table using Linear Probing.
# - Understand the "ABA Problem".
#
# ==============================================================================
"""

import threading
import time
from typing import Any, List, Optional, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COMPARE-AND-SWAP (SIMULATION)
# ==============================================================================
class AtomicReferenceArray:
    """
    Python does not expose the raw CPU CAS instruction. 
    We simulate it using a very tiny lock that only lasts for microseconds.
    In C++ (std::atomic) or Java (AtomicReferenceArray), this happens directly on 
    the CPU silicon with zero OS involvement.
    """
    def __init__(self, size: int):
        self.array: List[Any] = [None] * size
        self.lock = threading.Lock()
        
    def compare_and_swap(self, index: int, expected_val: Any, new_val: Any) -> bool:
        """
        ATOMIC CPU INSTRUCTION:
        "Update the array at `index` to `new_val`, but ONLY if it still holds `expected_val`."
        Returns True if successful, False if another thread beat us to it.
        """
        with self.lock:
            if self.array[index] is expected_val:
                self.array[index] = new_val
                return True
            return False
            
    def get(self, index: int) -> Any:
        return self.array[index]


# ==============================================================================
# 4. LOCK-FREE HASH TABLE (LINEAR PROBING)
# ==============================================================================
class LockFreeHashTable:
    """
    A Lock-Free Hash Table using Open Addressing (Linear Probing).
    """
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        
        # We store keys and values in two parallel atomic arrays to keep the CAS 
        # operations simple. In C, you would CAS a 64-bit pointer to a KeyValue struct.
        self.keys = AtomicReferenceArray(capacity)
        self.values = AtomicReferenceArray(capacity)

    def put(self, key: str, value: Any) -> None:
        """
        Lock-Free Insertion!
        We NEVER lock the table. If a collision or race condition occurs, we just 
        loop and try again!
        """
        idx = hash(key) % self.capacity
        
        while True:
            current_key = self.keys.get(idx)
            
            # Case 1: The slot is EMPTY. Try to claim it!
            if current_key is None:
                # Attempt to CAS the key. 
                # If another thread claimed it a microsecond before us, CAS will 
                # return False, and the loop will continue!
                if self.keys.compare_and_swap(idx, None, key):
                    # We successfully claimed the slot! Now set the value.
                    # We don't need CAS here because we exclusively own this key slot.
                    self.values.array[idx] = value
                    return
                    
            # Case 2: The slot is ALREADY OUR KEY. Update the value!
            elif current_key == key:
                # In a perfectly lock-free system, updating the value also requires CAS 
                # to prevent two threads overwriting the same value simultaneously.
                while True:
                    current_val = self.values.get(idx)
                    if self.values.compare_and_swap(idx, current_val, value):
                        return # Value updated!
                        
            # Case 3: The slot is taken by a DIFFERENT key. (Hash Collision)
            # Standard Linear Probing: Move to the next index and try again.
            idx = (idx + 1) % self.capacity

    def get(self, key: str) -> Any:
        """Lock-Free Retrieval. Just read the memory!"""
        idx = hash(key) % self.capacity
        
        while True:
            current_key = self.keys.get(idx)
            
            if current_key is None:
                raise KeyError(f"Key '{key}' not found.")
                
            if current_key == key:
                return self.values.get(idx)
                
            idx = (idx + 1) % self.capacity

def demonstrate_lock_free():
    section_header("Algorithm: Lock-Free Hashing (CAS)")
    
    lf_hash = LockFreeHashTable(capacity=16)
    
    def worker(thread_id: int):
        # Multiple threads inserting keys simultaneously without ANY locks!
        lf_hash.put(f"Key_{thread_id}", f"Value_{thread_id}")
        
        # Multiple threads trying to update the EXACT SAME KEY simultaneously!
        # The CAS loop will force them to serialize perfectly.
        lf_hash.put("Shared_Counter", thread_id)

    print("Launching 10 threads to hammer the Lock-Free Hash Table...")
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\nFinal State of the Lock-Free Table:")
    for i in range(16):
        k = lf_hash.keys.get(i)
        v = lf_hash.values.get(i)
        if k is not None:
            print(f" Index {i:2}: {k:15} -> {v}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a `while` loop used with Compare-And-Swap?
   Answer: CAS only attempts the swap ONCE. If it fails (because another thread modified the memory first), it returns False immediately. The `while` loop allows the thread to re-read the new memory state and try the calculation again. This is called a "Spin-Wait". Because it happens purely on the CPU, it is orders of magnitude faster than the OS putting the thread to sleep.

2. What is the ABA Problem in Lock-Free algorithms?
   Answer: Imagine Thread 1 reads memory and sees `A`. It pauses. Thread 2 changes `A` to `B`, and then changes `B` back to `A`. Thread 1 wakes up, runs CAS comparing to `A`, and succeeds! But the memory DID change, and pointers might have been deleted/recycled in the background, causing massive memory corruption. This is usually solved by attaching a hidden version counter to the memory (`A_version1`, `A_version3`).

3. Why don't we use Lock-Free structures for everything?
   Answer: They are incredibly difficult to write correctly. The ABA problem, memory reclamation (Hazard Pointers in C++), and CPU cache-line bouncing (when 10 threads spam CAS on the exact same variable, burning CPU cycles) make them highly complex. For 99% of applications, Lock Striping is fast enough and much safer.
"""

if __name__ == "__main__":
    demonstrate_lock_free()
    print("\n[SUCCESS] Laboratory: Lock-Free Hashing Completed.")
