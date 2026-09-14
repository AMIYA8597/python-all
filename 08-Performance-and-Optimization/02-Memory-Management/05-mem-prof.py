"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (MEMORY PROFILING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When a Python application crashes with a `MemoryError`, or an OS-level OOM 
# (Out of Memory) Killer terminates your Docker container, finding the leak 
# is incredibly difficult. You cannot use `print()` statements to track gigabytes 
# of RAM allocation across hundreds of thousands of dynamic objects.
#
# A junior engineer restarts the server every 24 hours to "fix" the memory leak.
#
# A senior engineer deploys `tracemalloc`. They take a cryptographic snapshot of 
# RAM before a workload, and a second snapshot after. They mathematically 
# calculate the exact byte-level difference between the two snapshots, instantly 
# isolating the exact line of code in the exact file that is leaking memory.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the `tracemalloc` standard library module.
# - Master differential memory snapshots (Snap1 vs Snap2).
# - Understand the architecture of tracing Python memory blocks.
#
# ==============================================================================
"""

import tracemalloc
import gc
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CREATING A MEMORY LEAK IN A SPECIFIC FUNCTION
# ==============================================================================
# A global list simulating an accidental memory leak (e.g., caching database 
# results but forgetting to implement an eviction strategy like LRU!)
GLOBAL_CACHE = []

def leaking_function(n: int):
    """
    This function accidentally appends 10,000 massive strings to a global cache, 
    permanently locking them in RAM.
    """
    for i in range(n):
        # A massive string!
        massive_data = f"DATA_BLOCK_{i}" * 100
        GLOBAL_CACHE.append(massive_data)

def safe_function(n: int):
    """
    This function processes data safely. It creates massive strings, but 
    lets them fall out of scope, allowing the Garbage Collector to destroy them.
    """
    for i in range(n):
        massive_data = f"DATA_BLOCK_{i}" * 100
        # Data is processed, but NOT appended to a global scope!


# ==============================================================================
# 4. DIFFERENTIAL MEMORY PROFILING (`tracemalloc`)
# ==============================================================================
def demonstrate_tracemalloc():
    section_header("Differential Memory Profiling (tracemalloc)")
    
    print("  [INIT] Starting memory tracking...")
    # The parameter (e.g., 10) tells the tracker how many frames of the traceback 
    # to store for each allocation. A deeper traceback costs more memory, but 
    # gives better context!
    tracemalloc.start(10)
    
    # 1. Take a baseline snapshot of the pristine RAM state!
    snapshot_1 = tracemalloc.take_snapshot()
    
    print("\n  [EXECUTION] Running Safe Function...")
    safe_function(10_000)
    
    # Force Garbage Collection to destroy the safe function's local variables!
    gc.collect()
    
    # 2. Take a snapshot after the safe execution.
    snapshot_2 = tracemalloc.take_snapshot()
    
    print("  [EXECUTION] Running Leaking Function...")
    leaking_function(10_000)
    
    # Force Garbage Collection (This will fail to destroy the leaked data!)
    gc.collect()
    
    # 3. Take a final snapshot after the catastrophic leak!
    snapshot_3 = tracemalloc.take_snapshot()
    
    print("\n  [ANALYSIS] Calculating Memory Differences...")
    
    # We compare Snapshot 2 vs Snapshot 1
    stats_safe = snapshot_2.compare_to(snapshot_1, 'lineno')
    
    # We compare Snapshot 3 vs Snapshot 2
    stats_leak = snapshot_3.compare_to(snapshot_2, 'lineno')
    
    print("\n  [RESULT: SAFE FUNCTION]")
    for stat in stats_safe[:3]: # Only print top 3
        # It should show negligible changes!
        print(f"    {stat}")
        
    print("\n  [RESULT: LEAKING FUNCTION]")
    for stat in stats_leak[:3]: # Top 3
        # It will explicitly point to the line inside `leaking_function`!
        print(f"    {stat}")
        
    print("\n  [SHUTDOWN] Stopping memory tracking...")
    tracemalloc.stop()


def run_all_labs():
    demonstrate_tracemalloc()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why must we explicitly call `gc.collect()` before taking a `tracemalloc` snapshot in a professional debugging session?"
   Senior Answer: "`tracemalloc` blindly logs the exact state of allocated memory at the exact microsecond the snapshot is taken. If you execute a massive function, it might leave behind thousands of orphaned cyclical references that are *scheduled* for destruction, but the Garbage Collector hasn't executed its background sweep yet. If you take a snapshot at that exact moment, `tracemalloc` will falsely report a catastrophic memory leak! By manually invoking `gc.collect()` right before `take_snapshot()`, we mathematically guarantee that all pending garbage is purged, ensuring that any memory remaining in the snapshot is a true, undeniable memory leak."

2. Interviewer: "What is the architectural difference between `sys.getsizeof()` and `tracemalloc`, and when would you use each?"
   Senior Answer: "`sys.getsizeof()` is an investigative tool for a *single, known object*. It queries the C-struct of a specific Python variable to see how many bytes it physically occupies. It is useless for finding a system-wide leak because you must already know which variable to inspect. `tracemalloc` is a systemic hooking engine. It overrides the underlying C memory allocators (`malloc`/`free`) for the entire Python interpreter. It logs every single byte requested by any function, anywhere in the codebase, mapping those allocations back to the specific line of Python code that requested them. You use `tracemalloc` to *find* the leak, and `getsizeof` to mathematically analyze it once found."

3. Interviewer: "If `tracemalloc` is so powerful, why don't we just leave it running permanently in our Production servers to automatically log leaks?"
   Senior Answer: "Tracing every single memory allocation at the C-level incurs a massive architectural overhead. Every time any line of code requests memory (which happens millions of times a second in Python), `tracemalloc` must pause, capture the execution stack trace, and log the allocation into a massive internal Hash Table. Leaving `tracemalloc` enabled in Production will catastrophically degrade the CPU throughput of the web server (often by 20% to 50%), and the tracker's internal Hash Table will eventually consume all available RAM itself! It is strictly a diagnostic tool meant for controlled staging environments, or to be toggled dynamically for short 60-second bursts in production."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Memory Management (Memory Profiling) Completed.")
