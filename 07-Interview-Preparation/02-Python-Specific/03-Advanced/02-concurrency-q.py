"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - ADVANCED CONCURRENCY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have an array of 1 Billion integers. I need to sum them. 
# I want to use all 8 cores of my CPU. Should I use ThreadPoolExecutor or 
# ProcessPoolExecutor?"
#
# If you say ThreadPoolExecutor, you instantly fail. Summing integers is a 
# pure CPU-bound mathematical operation. Threads in Python are choked by the GIL. 
# ThreadPoolExecutor will actually be SLOWER than a single thread due to context 
# switching overhead. You MUST use ProcessPoolExecutor.
#
# Interviewer: "Python 3.13 introduces the 'NoGIL' (Free-Threading) build. 
# If the GIL is removed, does my multi-threaded code automatically become 
# safely concurrent?"
# 
# A junior engineer says: "Yes, now it runs like C++!"
# A senior engineer says: "No! The GIL was protecting the CPython internal memory 
# from corruption, but it NEVER protected your application logic from Race 
# Conditions! If the GIL is removed, Threading becomes infinitely more dangerous 
# because now you have true parallelism, requiring brutal Mutex lock management 
# everywhere in your Python code."
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master ThreadPoolExecutor (I/O Bound) vs ProcessPoolExecutor (CPU Bound).
# - Understand the architecture of the upcoming 'NoGIL' (PEP 703) free-threading.
# - Understand Race Conditions in Python (Atomic vs Non-Atomic operations).
#
# ==============================================================================
"""

import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXECUTORS (THREAD VS PROCESS)
# ==============================================================================
def cpu_bound_task(task_id: int):
    """Pure math. No sleeping. No I/O. The GIL is never dropped."""
    total = 0
    for i in range(15_000_000):
        total += 1
    return total

def demonstrate_executors():
    section_header("ThreadPoolExecutor vs ProcessPoolExecutor")
    
    print("Task: Execute 4 massive mathematical calculations.")
    
    # 1. ThreadPoolExecutor (The GIL Disaster)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit 4 tasks
        results = list(executor.map(cpu_bound_task, range(4)))
    end = time.perf_counter()
    print(f"  -> ThreadPool Time: {end - start:.4f} seconds (Choked by the GIL)")
    
    # 2. ProcessPoolExecutor (True Parallelism)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, range(4)))
    end = time.perf_counter()
    print(f"  -> ProcessPool Time: {end - start:.4f} seconds (True Parallelism!)")
    
    print("\nConclusion: Multiprocessing physically bypasses the GIL by spawning ")
    print("4 separate OS Processes, each with their own isolated Memory and GIL, ")
    print("allowing true 100% utilization of a multi-core CPU.")


# ==============================================================================
# 4. RACE CONDITIONS (ATOMIC VS NON-ATOMIC)
# ==============================================================================
class SharedCounter:
    def __init__(self):
        self.count = 0
        # A Mutex Lock to fix the Race Condition
        self.lock = threading.Lock()
        
    def unsafe_increment(self):
        """
        NON-ATOMIC!
        In Python, `self.count += 1` is actually THREE separate bytecode instructions:
        1. LOAD_ATTR (Read memory)
        2. BINARY_ADD (Do math)
        3. STORE_ATTR (Write memory)
        The GIL can drop BETWEEN these instructions, causing data corruption!
        """
        for _ in range(100_000):
            self.count += 1
            
    def safe_increment(self):
        """ATOMIC! We mathematically freeze the thread with a Mutex."""
        for _ in range(100_000):
            with self.lock:
                self.count += 1

def demonstrate_race_conditions():
    section_header("Race Conditions (Even with the GIL!)")
    
    print("The GIL protects Python's *internal* C-structures, but it does NOT ")
    print("protect your Python logic from Race Conditions!")
    
    # 1. UNSAFE
    unsafe = SharedCounter()
    threads = [threading.Thread(target=unsafe.unsafe_increment) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    print(f"\nUnsafe Count: {unsafe.count} (Expected 500,000)")
    print("Notice the data is corrupted! Threads overwrote each other's memory.")
    
    # 2. SAFE
    safe = SharedCounter()
    threads = [threading.Thread(target=safe.safe_increment) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    print(f"\nSafe Count  : {safe.count} (Perfect!)")
    print("We manually used a Mutex Lock (`with self.lock`) to mathematically ")
    print("guarantee atomic execution of the block.")


def run_all_labs():
    # Only run the executor test if safe for multiprocessing
    demonstrate_executors()
    demonstrate_race_conditions()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Explain exactly why `self.count += 1` is vulnerable to a Race Condition, even though the GIL exists."
   Senior Answer: "The GIL guarantees that only one thread can execute *a single Python bytecode instruction* at a time. However, `x += 1` is NOT a single instruction! The CPython compiler translates it into three bytecode ops: `LOAD` the value into register, `ADD` one, and `STORE` the new value in memory. The OS scheduler can brutally pause Thread A right after it performs the `ADD`, drop the GIL, and hand it to Thread B. Thread B performs a full `LOAD, ADD, STORE`, and then Thread A resumes and performs its `STORE`, violently overwriting Thread B's work. The GIL protects C-level memory, but it does absolutely nothing to protect multi-step Python logic."

2. Interviewer: "What is the penalty of using `ProcessPoolExecutor` instead of `ThreadPoolExecutor`?"
   Senior Answer: "When you spawn a Thread, it exists within the same OS Process, meaning it shares the exact same physical RAM space. Spawning a thread takes microseconds and costs almost zero memory. When you spawn a Process, the OS mathematically duplicates the entire Python interpreter, allocating a massive, brand-new chunk of physical RAM. Furthermore, because Processes cannot see each other's memory, if Process A wants to send a string to Process B, it must 'Pickle' (serialize) the data into raw binary, push it through an OS-level Pipe (IPC), and unpickle it on the other side. This serialization overhead is devastatingly slow."

3. Interviewer: "Python 3.13 introduces an experimental 'NoGIL' (Free-Threading) build (PEP 703). How does it achieve thread safety for its internal C-structures without the GIL?"
   Senior Answer: "Historically, the GIL was a giant, single Mutex wrapped around the entire interpreter to protect Reference Counting. If you remove the GIL, two threads updating a Reference Count simultaneously will cause a Segfault. PEP 703 replaces the giant GIL with 'Biased Reference Counting' and highly localized, granular locks. It uses specialized atomic hardware instructions to safely increment reference counts concurrently. However, while this solves Python's internal safety and allows true parallelism, it completely exposes the user's Python code to brutal race conditions, requiring engineers to become highly disciplined with manual Mutex lock management."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced Concurrency) Completed.")
