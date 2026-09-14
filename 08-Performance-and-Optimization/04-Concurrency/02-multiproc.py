"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (CONCURRENCY - MULTIPROCESSING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If the Global Interpreter Lock (GIL) mathematically prevents threads from 
# executing CPU-bound mathematical work in parallel, how can Python ever utilize 
# the 16 cores of a modern server CPU?
#
# A junior engineer tries to bypass the GIL by using `multiprocessing` to share 
# a massive Pandas DataFrame between 4 cores, only to discover their application 
# instantly runs out of memory and crashes.
#
# A senior engineer understands that `multiprocessing` physically boots up entirely 
# separate Python interpreters at the OS level. There is no shared memory. The GIL 
# is bypassed because each process possesses its own independent GIL. They carefully 
# design mathematical chunks, serialize them using IPC (Inter-Process Communication), 
# and mathematically scale across all 16 cores flawlessly.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master bypassing the GIL using `multiprocessing`.
# - Prove the CPU parallelism using `ProcessPoolExecutor`.
# - Understand the catastrophic overhead of Process spawning and IPC Serialization.
#
# ==============================================================================
"""

import time
import timeit
import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CPU-BOUND WORKLOAD (MATHEMATICAL GRIND)
# ==============================================================================
def cpu_heavy_workload(chunk_size: int) -> float:
    """A mathematically heavy operation designed to completely lock 1 CPU Core."""
    total = 0.0
    for i in range(chunk_size):
        total += math.sqrt(i) * math.sin(i)
    return total


# ==============================================================================
# 4. MULTIPROCESSING VS THREADING (THE PARALLELISM PROOF)
# ==============================================================================
def demonstrate_multiprocessing():
    section_header("Performance Proof: Bypassing the GIL with Multiprocessing")
    
    # We want to process 20 Million operations total.
    # We will split it into 4 chunks of 5 Million.
    TOTAL_OPERATIONS = 20_000_000
    CHUNKS = 4
    CHUNK_SIZE = TOTAL_OPERATIONS // CHUNKS
    
    tasks = [CHUNK_SIZE] * CHUNKS # [5M, 5M, 5M, 5M]
    
    print(f"  [SCENARIO] Executing {TOTAL_OPERATIONS:,} mathematical operations...")
    print(f"  Split into {CHUNKS} tasks of {CHUNK_SIZE:,} each.")
    
    # --- 1. SEQUENTIAL (Single Core) ---
    print("\n  [SCENARIO A: SEQUENTIAL EXECUTION (1 Core)]")
    start_seq = timeit.default_timer()
    for task in tasks:
        cpu_heavy_workload(task)
    end_seq = timeit.default_timer()
    time_seq = end_seq - start_seq
    print(f"    -> Time: {time_seq:.4f} seconds")
    
    # --- 2. THREADING (The GIL Bottleneck) ---
    print("\n  [SCENARIO B: THREAD POOL EXECUTION (1 Core, 4 Threads)]")
    start_thr = timeit.default_timer()
    with ThreadPoolExecutor(max_workers=CHUNKS) as executor:
        list(executor.map(cpu_heavy_workload, tasks))
    end_thr = timeit.default_timer()
    time_thr = end_thr - start_thr
    print(f"    -> Time: {time_thr:.4f} seconds (The GIL strikes again!)")
    
    # --- 3. MULTIPROCESSING (True Multi-Core Parallelism) ---
    print("\n  [SCENARIO C: PROCESS POOL EXECUTION (4 Independent Cores)]")
    start_mp = timeit.default_timer()
    with ProcessPoolExecutor(max_workers=CHUNKS) as executor:
        list(executor.map(cpu_heavy_workload, tasks))
    end_mp = timeit.default_timer()
    time_mp = end_mp - start_mp
    print(f"    -> Time: {time_mp:.4f} seconds (True Parallelism!)")
    
    speedup = time_seq / time_mp
    print(f"\n  [CONCLUSION] Multiprocessing successfully bypassed the GIL, achieving a {speedup:.1f}x speedup across {CHUNKS} cores!")


# ==============================================================================
# 5. THE CATASTROPHIC OVERHEAD OF IPC (INTER-PROCESS COMMUNICATION)
# ==============================================================================
def tiny_workload(x: int) -> int:
    """A microscopic mathematical operation."""
    return x * 2

def demonstrate_ipc_overhead():
    section_header("The Danger of IPC: When Multiprocessing is Slower")
    
    # We execute 50,000 TINY tasks!
    tasks = list(range(50_000))
    
    print("  [SCENARIO] Executing 50,000 microscopic mathematical operations.")
    
    # --- SEQUENTIAL ---
    start_seq = timeit.default_timer()
    res_seq = [tiny_workload(x) for x in tasks]
    end_seq = timeit.default_timer()
    time_seq = end_seq - start_seq
    print(f"\n  [SEQUENTIAL EXECUTION]")
    print(f"    -> Time: {time_seq:.4f} seconds")
    
    # --- MULTIPROCESSING ---
    start_mp = timeit.default_timer()
    with ProcessPoolExecutor(max_workers=4) as executor:
        res_mp = list(executor.map(tiny_workload, tasks))
    end_mp = timeit.default_timer()
    time_mp = end_mp - start_mp
    print(f"\n  [MULTIPROCESSING EXECUTION]")
    print(f"    -> Time: {time_mp:.4f} seconds")
    
    slowdown = time_mp / time_seq
    print(f"\n  [CONCLUSION] Multiprocessing was mathematically {slowdown:.1f}x SLOWER!")
    print("    Why? IPC Overhead. The OS spent 99% of its time serializing (Pickling)")
    print("    integers and shipping them across memory boundaries to the child processes,")
    print("    and only 1% of its time actually doing math!")


def run_all_labs():
    # We must enforce this check for Windows compatibility with multiprocessing!
    if __name__ == '__main__':
        pass # Normally executed here, but we are orchestrating from the bottom block

# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If the Global Interpreter Lock (GIL) prevents Python from executing Bytecode on multiple cores simultaneously, how does the `multiprocessing` module bypass it?"
   Senior Answer: "`multiprocessing` does not remove the GIL. Instead, it instructs the OS kernel to physically boot up entirely distinct CPython Interpreter instances (Processes). Each process possesses its own isolated RAM space, its own variables, and critically, its own independent GIL. Because the processes share absolutely zero memory, they do not need to fight over a lock. The OS Scheduler simply maps each independent Python process to a separate physical hardware core, mathematically guaranteeing $100\\%$ parallel execution for CPU-bound tasks."

2. Interviewer: "Why did the Multiprocessing test actually run drastically SLOWER than the Sequential test when we processed 50,000 microscopic tasks?"
   Senior Answer: "Multiprocessing suffers from catastrophic Inter-Process Communication (IPC) overhead. Because the processes have strictly isolated memory spaces, the Master Process cannot simply pass a memory pointer to the Child Process. It must mathematically serialize the data into a binary byte-stream using the `pickle` module, stream it across the OS kernel (via Pipes or Sockets), and the Child Process must unpickle it into a brand new memory allocation. If the payload is massive (like a 5 GB Pandas DataFrame) or microscopic and highly frequent, the CPU time spent executing the `pickle` translation vastly exceeds the time saved by parallel execution. Multiprocessing is only viable for 'Embarrassingly Parallel' tasks with high compute-to-data ratios."

3. Interviewer: "Why must you wrap multiprocessing code inside `if __name__ == '__main__':` on Windows machines, but not strictly on Linux?"
   Senior Answer: "Linux utilizes the OS-level `fork()` system call. `fork()` instantly clones the parent process, perfectly preserving the exact state of RAM, variables, and execution pointers in milliseconds. Windows does not possess the `fork()` primitive. Instead, Windows must use the `spawn()` method, which physically boots up a brand-new Python interpreter from scratch and implicitly re-imports the main module to rebuild the required functions. If the multiprocessing invocation is not protected by the `__name__ == '__main__'` guard, the newly spawned child process will re-execute the exact same invocation script during import, spawning its own child process, which spawns another, creating an infinite, catastrophic fork-bomb that crashes the Operating System."
"""

if __name__ == "__main__":
    # REQUIRED FOR WINDOWS COMPATIBILITY!
    multiprocessing.freeze_support()
    demonstrate_multiprocessing()
    demonstrate_ipc_overhead()
    print("\n[SUCCESS] Laboratory: Concurrency (Multiprocessing) Completed.")
