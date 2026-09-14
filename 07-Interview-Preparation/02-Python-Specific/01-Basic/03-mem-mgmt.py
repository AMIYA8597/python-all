"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - MEMORY MANAGEMENT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "You wrote a long-running Python server. After 3 days, it crashes 
# with an Out-Of-Memory (OOM) error. Why did the Garbage Collector fail?"
#
# You cannot answer this if you think Python's Garbage Collector is magic.
# You must understand the CPython dual-engine memory architecture:
# 1. Primary Engine: Reference Counting (Instant, Deterministic).
# 2. Secondary Engine: Tracing Garbage Collector (Slow, Generation-based).
#
# The server crashed because of a "Reference Cycle" (e.g., Object A points to 
# Object B, and Object B points back to Object A). Even if the main program 
# deletes them, their internal counts never reach 0. They float in RAM forever 
# as an immortal island of leaked memory.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master CPython Reference Counting (`sys.getrefcount`).
# - Understand the Memory Leak of Circular References.
# - Understand how the Generational Tracing GC cleans up circular leaks.
#
# ==============================================================================
"""

import sys
import gc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. REFERENCE COUNTING (THE PRIMARY ENGINE)
# ==============================================================================
class HeavyObject:
    def __init__(self, name):
        self.name = name
        print(f"    [ALLOCATED] {self.name} created in RAM.")
        
    def __del__(self):
        # This magical dunder method fires the EXACT millisecond the object dies!
        print(f"    [DEALLOCATED] {self.name} violently purged from RAM.")

def demonstrate_ref_count():
    section_header("CPython Reference Counting")
    
    print("1. Creating object 'Alpha'...")
    alpha = HeavyObject("Alpha")
    
    # sys.getrefcount returns 2 (one for 'alpha' variable, one for passing it into the getrefcount function!)
    print(f"   Ref Count for Alpha: {sys.getrefcount(alpha) - 1}")
    
    print("2. Creating another pointer to the EXACT SAME object...")
    beta = alpha
    print(f"   Ref Count for Alpha: {sys.getrefcount(alpha) - 1}")
    
    print("3. Deleting 'alpha' variable...")
    del alpha
    # The object still exists because 'beta' points to it!
    print("   (Object survives! 'beta' is keeping it alive.)")
    
    print("4. Deleting 'beta' variable...")
    # The moment beta is deleted, the count drops to 0. CPython instantly triggers __del__!
    del beta
    print("   (Object is now truly dead.)")


# ==============================================================================
# 4. CIRCULAR REFERENCES (THE FATAL MEMORY LEAK)
# ==============================================================================
class Node:
    def __init__(self, value):
        self.value = value
        self.neighbor = None
        
    def __del__(self):
        print(f"    [GC CLEANUP] Node {self.value} purged from RAM.")

def simulate_memory_leak():
    section_header("Circular References (Memory Leak)")
    
    print("Creating two separate nodes...")
    node_A = Node("A")
    node_B = Node("B")
    
    print("Forcing them to point to each other (Circular Reference!)...")
    node_A.neighbor = node_B
    node_B.neighbor = node_A
    
    print("We will now explicitly delete BOTH variables from the main program.")
    del node_A
    del node_B
    
    print("...Notice how the [GC CLEANUP] print statements DID NOT FIRE?!")
    print("Even though the main program can no longer access them, Node A thinks ")
    print("Node B is keeping it alive, and Node B thinks Node A is keeping it alive.")
    print("They are an immortal island floating in RAM. A catastrophic Memory Leak!\n")
    
    print("To fix this, CPython runs a slow, heavy 'Tracing Garbage Collector' ")
    print("in the background. Let's physically trigger it now:")
    
    collected_objects = gc.collect()
    print(f"Background GC Sweep completed. It found and destroyed {collected_objects} leaked objects!")


def run_all_labs():
    demonstrate_ref_count()
    simulate_memory_leak()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "How exactly does CPython determine when to destroy an object in RAM?"
   Senior Answer: "CPython uses a dual-engine architecture. The primary engine is Reference Counting. Every single object contains a hidden integer tracking how many variables point to it. The exact microsecond this integer drops to 0, CPython violently and deterministically deallocates the RAM. However, Reference Counting mathematically fails if Object A points to Object B, and Object B points back to A (a Circular Reference). Their internal counts will never reach 0. To fix this, CPython has a secondary engine: the Generational Tracing Garbage Collector. It periodically freezes the application, traces all active references from the roots, finds isolated 'islands' of circular references, and manually destroys them."

2. Interviewer: "The Tracing Garbage Collector causes heavy CPU pauses. How can we write code to prevent circular references in the first place?"
   Senior Answer: "If you are building Graph data structures (like a Tree where the Child points to the Parent, and the Parent points to the Child), you must use the `weakref` module. A 'Weak Reference' allows you to point to an object WITHOUT incrementing its primary Reference Count. The Parent holds a strong reference to the Child, but the Child holds a `weakref` to the Parent. When the Parent goes out of scope, its reference count naturally hits 0 (because the weak reference doesn't count), and the entire Tree instantly collapses and deallocates gracefully, completely bypassing the need for the heavy background GC."

3. Interviewer: "What is the 'Generational' aspect of Python's GC? Why are there 3 generations?"
   Senior Answer: "Scanning the entire RAM of a 10 GB application to find circular references would take seconds, causing horrific application stutter. The 'Generational Hypothesis' states that 90% of objects die young (e.g., temporary variables inside a function). Python splits memory into 3 Generations (Gen 0, 1, and 2). All new objects spawn in Gen 0. The GC scans Gen 0 very frequently. If an object survives a Gen 0 scan, it is promoted to Gen 1. If it survives Gen 1, it is promoted to Gen 2 (Long-lived objects like global configs). The GC scans Gen 2 very rarely. This drastically reduces CPU overhead by mathematically focusing the GC's scanning power purely on the youngest, most volatile objects!"
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Memory Management) Completed.")
