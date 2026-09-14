"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (STARTUPS - SYSTEMS PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Advanced startups (AI, FinTech, Data Infra) demand Systems Programming skills 
# in Python. You must understand how to bypass the Global Interpreter Lock (GIL) 
# for CPU-bound tasks, how to perform Inter-Process Communication (IPC), and 
# how to safely read massive files that exceed physical RAM using Memory Mapped 
# files (mmap).
#
# A junior engineer tries to use `threading` to parallelize a massive mathematical 
# computation. Because of the GIL, the threads fight for execution time, and the 
# code actually runs SLOWER than a single thread.
# 
# A senior engineer deploys `multiprocessing`. They spawn physical OS-level 
# processes, each with their own isolated GIL and Memory space, achieving true 
# mathematical parallelism across multiple CPU cores.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `multiprocessing` for CPU-bound architectural scale.
# - Master Memory-Mapped files (`mmap`) for O(1) RAM file streaming.
# - Understand IPC (Inter-Process Communication) safely.
#
# ==============================================================================
"""

import os
import mmap
import time
import multiprocessing

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BYPASSING THE GIL (MULTIPROCESSING)
# ==============================================================================
def heavy_computation(target: int) -> int:
    """A mathematically heavy CPU-bound task."""
    result = 0
    for i in range(target):
        result += (i * i)
    return result

def demonstrate_multiprocessing():
    section_header("Systems Programming: Multiprocessing (Bypassing GIL)")
    
    # We will compute 3 massive numbers.
    targets = [20_000_000, 20_000_000, 20_000_000]
    
    # --- BAD (SEQUENTIAL) ---
    print("  [SEQUENTIAL] Executing on a single core...")
    start = time.perf_counter()
    seq_results = [heavy_computation(t) for t in targets]
    end = time.perf_counter()
    seq_time = end - start
    print(f"    -> Time: {seq_time:.2f} seconds")
    
    # --- GOOD (PARALLEL PROCESSES) ---
    print("\n  [MULTIPROCESSING] Spawning OS-level processes across cores...")
    start = time.perf_counter()
    
    # We create a Pool of worker processes. 
    # Python serializes the function and arguments, blasts them across the CPU 
    # cores, runs them simultaneously, and aggregates the results!
    with multiprocessing.Pool(processes=3) as pool:
        par_results = pool.map(heavy_computation, targets)
        
    end = time.perf_counter()
    par_time = end - start
    print(f"    -> Time: {par_time:.2f} seconds")
    
    if par_time < seq_time:
        print(f"\n  Result: Multiprocessing was {seq_time/par_time:.1f}x faster!")
    else:
        print("\n  Result: Overhead exceeded gains (Normal on small datasets or few cores).")


# ==============================================================================
# 4. MEMORY MAPPED FILES (MMAP) - EXTREME FILE I/O
# ==============================================================================
def demonstrate_mmap():
    section_header("Systems Programming: Memory-Mapped Files (mmap)")
    
    filename = "temp_massive_file.txt"
    
    # 1. Create a dummy file
    print(f"  Creating dummy file '{filename}'...")
    with open(filename, "w") as f:
        # 100,000 bytes of data
        f.write("A" * 50_000 + "TARGET" + "B" * 49_994)
        
    print("  Simulating: File is 500 GB and exceeds our physical RAM.")
    
    # 2. Open it using Memory Mapping!
    # mmap DOES NOT read the file into RAM. It maps the physical Hard Drive sectors 
    # directly into Virtual Memory addresses. The OS pages the data in and out 
    # automatically in tiny chunks, preventing Out-Of-Memory (OOM) crashes!
    with open(filename, "r+b") as f:
        # 0 means map the whole file. length must be a multiple of page size.
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            
            # We can search the 500GB file EXACTLY like a standard Python string!
            # The OS handles the underlying disk I/O paging mathematically.
            print("  Searching for 'TARGET' directly on the hard drive via mmap...")
            index = mm.find(b"TARGET")
            
            if index != -1:
                print(f"    -> [FOUND] Target string exists at byte offset {index}!")
                
    # Cleanup
    os.remove(filename)
    print("  Cleaned up temp file.")


def run_all_labs():
    # Due to Windows/Linux multiprocessing quirks, we must wrap it in __main__
    # This check is actually physically present below!
    pass


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does Python's `threading` module fail to speed up CPU-bound mathematical computations, but `multiprocessing` succeeds?"
   Senior Answer: "The CPython interpreter is fundamentally protected by the Global Interpreter Lock (GIL). The GIL physically prevents multiple native threads from executing Python bytecodes simultaneously in the same memory space. If you spawn 4 threads to do heavy math, the GIL forces them to take turns, resulting in zero mathematical parallelism and introducing horrific Context Switching overhead. `multiprocessing` bypasses the GIL completely by forking the entire Python interpreter into 4 entirely independent OS-level processes. Because each process has its own isolated Memory Space and its own isolated GIL, the OS schedules them across 4 physical CPU cores simultaneously, achieving true parallel execution."

2. Interviewer: "If `multiprocessing` is so fast, why don't we use it for everything? What is the architectural cost?"
   Senior Answer: "The architectural cost is Inter-Process Communication (IPC) and Memory allocation. Spawning an OS-level process is incredibly slow and heavy compared to a lightweight thread. More critically, processes do not share memory! If Process A calculates a massive 1GB DataFrame and needs to pass it to Process B, it must mathematically Serialize (Pickle) the 1GB object, stream it across an OS pipe or socket, and Process B must Deserialize it. This IPC serialization overhead can completely obliterate the time saved by parallel execution. Threads, conversely, share the exact same memory space and can pass data instantly."

3. Interviewer: "If I need to search for a specific string inside a 1-Terabyte log file, and my server only has 16GB of RAM, how does `mmap` solve this without crashing?"
   Senior Answer: "If you call `file.read()`, Python attempts to load the entire 1-Terabyte file into physical RAM, instantly triggering an Out-Of-Memory (OOM) crash. `mmap` (Memory-Mapped File) uses the Operating System's Virtual Memory manager. It maps the physical hard drive sectors of the file into the application's memory address space. When you execute a search like `mm.find()`, the OS lazily loads only the exact tiny 'Pages' (usually 4KB chunks) from the disk into RAM that are currently being scanned. As the scan moves forward, the OS flushes old pages back to the disk. It allows you to treat a 1TB file exactly like a giant string, utilizing strict $O(1)$ RAM limits."
"""

if __name__ == "__main__":
    # CRITICAL: Multiprocessing on Windows requires this protection!
    demonstrate_multiprocessing()
    demonstrate_mmap()
    print("\n[SUCCESS] Laboratory: Startup Prep (Systems Programming) Completed.")
