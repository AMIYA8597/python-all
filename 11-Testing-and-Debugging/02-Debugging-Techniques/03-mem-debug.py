"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (MEMORY LEAKS & TRACEMALLOC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a long-running background worker that processes 
# streaming data. After 48 hours in Production, the Linux Kernel's OOM (Out Of 
# Memory) Killer violently terminates the Python process. The developer has no 
# idea why. They assume Python's Garbage Collector handles everything perfectly.
#
# A senior software engineer understands that "Memory Leaks" exist in Python 
# when strong object references are never deleted. They use the built-in 
# `tracemalloc` library to mathematically snapshot the RAM usage at Time A and 
# Time B. They execute a diff calculation, proving that a global list named 
# `cache` is illegally growing by 5,000 objects every hour. They fix the bug, 
# and the RAM line mathematically flatlines at a perfect 45 MB forever.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Python Memory Management (Garbage Collection vs Leaks).
# - Execute `tracemalloc` to snapshot and diff RAM allocations.
# - Architect memory-safe long-running processes.
#
# ==============================================================================
"""

import tracemalloc
import time
import gc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE MEMORY LEAK)
# ==============================================================================
class GlobalState:
    # A dangerous architectural pattern!
    # Global variables live forever. If you append to this, RAM goes up forever.
    illegally_growing_cache = []


class DataStreamProcessor:
    @staticmethod
    def process_chunk(chunk_id: int):
        """
        Simulates processing a chunk of data.
        It mathematically leaks memory by storing a heavy string in the global cache.
        """
        # We generate a massive 100 KB string of garbage data
        heavy_payload = "X" * 100_000 
        
        # FATAL BUG: We append it to a global list and never remove it!
        # The Garbage Collector is mathematically powerless because the global 
        # list maintains a strong reference to the string.
        GlobalState.illegally_growing_cache.append(heavy_payload)
        
        # Simulate CPU work
        time.sleep(0.01)


# ==============================================================================
# 4. THE TRACEMALLOC ARCHITECTURE (THE DEBUGGER)
# ==============================================================================
class MemoryDebugger:
    """A highly analytical engine for finding RAM leaks."""
    
    @staticmethod
    def run_memory_analysis():
        print("  [INIT] Booting tracemalloc engine...")
        
        # 1. We mathematically command Python to track every single memory allocation!
        tracemalloc.start()
        
        # 2. We take SNAPSHOT A (The Baseline)
        print("  [SNAPSHOT A] Taking baseline memory snapshot.")
        snapshot1 = tracemalloc.take_snapshot()
        
        # 3. We simulate 48 hours of background processing!
        print("  [EXECUTION] Simulating data stream processing (Triggering the bug)...")
        for i in range(50):
            DataStreamProcessor.process_chunk(i)
            
        # 4. We force the Garbage Collector to run immediately, proving 
        # that the memory leak survives GC!
        gc.collect()
            
        # 5. We take SNAPSHOT B (The Aftermath)
        print("  [SNAPSHOT B] Taking post-execution memory snapshot.")
        snapshot2 = tracemalloc.take_snapshot()
        
        # 6. We execute a Mathematical Diff!
        print("\n  [ANALYSIS] Calculating Memory Allocation Diff...")
        
        # We compare Snapshot B to Snapshot A, grouped by exactly which filename 
        # and line number allocated the RAM!
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        
        print("\n  [TOP 3 MEMORY OFFENDERS]")
        for stat in top_stats[:3]:
            # Size in KiB (Kilobytes)
            size = stat.size_diff / 1024
            
            # The exact file and line number
            trace = stat.traceback[0]
            
            print(f"    -> Leaked {size:,.1f} KiB at {trace.filename}:{trace.lineno}")
            
        # We mathematically shut down the tracker to free CPU overhead
        tracemalloc.stop()


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_memory_debugging():
    section_header("Debugging: tracemalloc & Memory Leaks")
    
    MemoryDebugger.run_memory_analysis()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  `tracemalloc` mathematically proved that a massive block of memory ")
    print("  was allocated inside `process_chunk` and never released. The developer ")
    print("  can now instantly navigate to that exact line number and fix the bug.")


def run_all_labs():
    demonstrate_memory_debugging()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Python has an automatic Garbage Collector (GC), how is it mathematically possible to create a Memory Leak in pure Python without using C-extensions?"
   Senior Answer: "Strong Reference Retention. Python's Garbage Collector uses Reference Counting. If the Reference Count of an object hits $0$, the RAM is instantly freed. A Memory Leak in Python occurs when you accidentally maintain a strong reference to an object forever, preventing the count from reaching zero. The most common architectural failure is a global `cache = {}` dictionary. If a web server appends every user session to that dictionary and forgets to implement a Time-To-Live (TTL) eviction policy, the objects are mathematically immortal. The GC will ignore them, and the RAM usage will strictly increase until the Linux Kernel kills the process."

2. Interviewer: "Why did we execute `gc.collect()` manually right before taking Snapshot B?"
   Senior Answer: "Eliminating False Positives (Generational GC). Python's Garbage Collector does not run instantly on cyclic references (e.g., Object A points to Object B, and Object B points to Object A). It runs periodically based on the 'Generational' threshold. If we take Snapshot B immediately after the loop, we might accidentally capture 'dead' objects that the GC simply hasn't had time to clean up yet. This creates a False Positive memory leak. By manually executing `gc.collect()`, we mathematically force Python to annihilate all dead objects in RAM. Anything that survives `gc.collect()` is mathematically guaranteed to be a true, immortal memory leak."

3. Interviewer: "How does `tracemalloc` mathematically trace the exact line number of the code that allocated the RAM?"
   Senior Answer: "OS-Level Hook Injection. When you execute `tracemalloc.start()`, it hooks deeply into the CPython memory allocator (the C-level `pymalloc` engine). Every single time Python requests a new block of RAM from the Operating System, `tracemalloc` intercepts the request. It looks at the current Python Execution Frame, extracts the filename and line number, and stores that metadata in a separate hash table alongside the memory address. When you take a snapshot, it aggregates all the active memory addresses by their origin line number, providing unparalleled architectural visibility."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Memory Debugging) Completed.")
