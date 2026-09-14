"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (GARBAGE COLLECTION TUNING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python uses Reference Counting as its primary memory management system. When a 
# variable's reference count drops to 0, it is instantly deleted from RAM.
#
# However, if Object A points to Object B, and Object B points back to Object A, 
# their reference counts will never reach 0, creating a "Cyclic Reference Leak".
# To solve this, CPython runs a background Garbage Collector (GC) that periodically 
# freezes the entire application ("Stop-The-World"), scans RAM, and destroys cycles.
#
# A junior engineer builds a massive real-time game. Every 10 seconds, the game 
# randomly stutters for 50ms. They blame the graphics engine.
#
# A senior engineer recognizes the GC "Stop-The-World" pauses. They import the 
# `gc` module, manually tune the GC thresholds, or selectively disable the GC 
# during high-performance combat loops, eliminating the stutter permanently.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master identifying Cyclic References.
# - Master manipulating the `gc` module (enable, disable, collect).
# - Understand Generational Garbage Collection thresholds.
#
# ==============================================================================
"""

import gc
import sys
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CREATING A CYCLIC REFERENCE MEMORY LEAK
# ==============================================================================
class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None
        
    def __del__(self):
        # This magic method fires when the object is physically destroyed from RAM!
        print(f"    [MEMORY FREED] Node '{self.name}' was destroyed.")

def demonstrate_reference_counting():
    section_header("Standard Reference Counting (No GC Required)")
    
    print("  Creating a single Node...")
    a = Node("Alpha")
    
    # sys.getrefcount always returns +1 because passing 'a' into the function itself 
    # creates a temporary reference!
    print(f"  Reference Count for 'Alpha': {sys.getrefcount(a) - 1}")
    
    print("  Deleting the reference to 'Alpha'...")
    # The moment we delete `a`, the count drops to 0. It is destroyed INSTANTLY.
    # The Garbage Collector is NOT involved here!
    del a
    print("  Standard Reference Counting executed flawlessly.")

def demonstrate_cyclic_leak():
    section_header("Cyclic Reference Leak (The GC steps in!)")
    
    print("  Creating Node A and Node B...")
    a = Node("A")
    b = Node("B")
    
    print("  Linking A to B, and B to A (Creating the Cycle!)...")
    a.ref = b
    b.ref = a
    
    print(f"  Reference Count for 'A': {sys.getrefcount(a) - 1}")
    print(f"  Reference Count for 'B': {sys.getrefcount(b) - 1}")
    
    print("  Deleting the local variables 'a' and 'b'...")
    del a
    del b
    
    print("  Variables deleted. But notice: The __del__ messages did NOT print!")
    print("  They are orphaned in RAM because they are keeping each other alive!")
    
    print("\n  [MANUAL INTERVENTION] Forcing a Garbage Collection Sweep...")
    # This manually triggers the Stop-The-World sweep!
    collected = gc.collect()
    print(f"  [GC SUMMARY] The GC found and destroyed {collected} orphaned objects!")


# ==============================================================================
# 4. TUNING THE GENERATIONAL THRESHOLDS
# ==============================================================================
def demonstrate_gc_tuning():
    section_header("Tuning the Generational Garbage Collector")
    
    # CPython's GC uses 3 "Generations".
    # Generation 0: Brand new objects.
    # Generation 1: Objects that survived a Gen 0 sweep.
    # Generation 2: Long-lived objects (the main application state).
    
    current_thresholds = gc.get_threshold()
    print(f"  Default GC Thresholds: {current_thresholds}")
    print("  (Gen 0 runs after 700 allocations. Gen 1 after 10 Gen-0 sweeps. Gen 2 after 10 Gen-1 sweeps.)")
    
    print("\n  [SCENARIO] We are entering a high-performance rendering loop!")
    print("  We cannot afford random 50ms stutters. We are going to aggressively raise the thresholds.")
    
    # We tell the GC to wait for 50,000 allocations before sweeping!
    gc.set_threshold(50000, 50, 50)
    print(f"  New GC Thresholds: {gc.get_threshold()}")
    
    # OR, the extreme approach: Disable it entirely during combat!
    print("  [EXTREME] Disabling the GC entirely...")
    gc.disable()
    
    print("  Executing 1,000,000 mathematical operations...")
    # Reference counting STILL works while the GC is disabled!
    # Non-cyclical objects will still be destroyed instantly!
    # Only cycles will leak during this time.
    dummy_list = [i for i in range(1_000_000)]
    del dummy_list
    print("  Operations complete. No stutters occurred.")
    
    print("  [RECOVERY] Re-enabling the GC and forcing a cleanup sweep.")
    gc.enable()
    gc.collect()


def run_all_labs():
    demonstrate_reference_counting()
    demonstrate_cyclic_leak()
    demonstrate_gc_tuning()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Python uses Reference Counting to manage memory, why does it even need a Garbage Collector?"
   Senior Answer: "Reference Counting is flawless and instantaneous for hierarchical data, but it mathematically breaks when dealing with Cyclical References (e.g., a Doubly-Linked List, or Object A storing a callback pointing to Object B, while B holds a reference to A). If both objects fall out of scope, their reference counts drop to $1$, not $0$. They become immortal memory leaks, completely inaccessible to the application but permanently occupying RAM. The Garbage Collector is specifically designed as a secondary fail-safe; its only job is to scan the memory graph, detect these isolated cycles, and forcefully terminate them."

2. Interviewer: "What is the performance penalty of `gc.collect()`, and why shouldn't we call it manually inside a loop?"
   Senior Answer: "`gc.collect()` triggers a 'Stop-The-World' event. To safely traverse the memory graph and determine what is alive and what is dead, the CPython interpreter must completely freeze the execution of all Python threads. If you have 500 MB of objects in RAM, sweeping Generation 2 requires the CPU to iterate over every single object pointer. Calling it manually inside a high-frequency loop (like a web request handler) will catastrophically spike your application latency. The GC is designed to run in the background; you should only manually invoke it during idle moments (e.g., after a level loads in a game, or between batch processing jobs)."

3. Interviewer: "Why does CPython use 3 different 'Generations' for its Garbage Collector instead of just scanning all memory at once?"
   Senior Answer: "This is based on the 'Generational Hypothesis' of Computer Science: *Most objects die young.* A temporary variable inside a function is created and destroyed in microseconds. It makes zero mathematical sense to scan the massive 10 GB Application State (Generation 2) every time a tiny temporary string is orphaned. By grouping memory into Generations, CPython aggressively and quickly scans only the youngest objects (Generation 0), which resolves $95\\%$ of memory garbage with almost zero CPU overhead. It only pays the massive cost of scanning the older Generations if absolutely necessary, protecting the application's overall throughput."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Memory Management (GC Tuning) Completed.")
