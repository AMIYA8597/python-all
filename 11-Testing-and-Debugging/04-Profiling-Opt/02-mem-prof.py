"""
# ==============================================================================
# LABORATORY: PROFILING & OPTIMIZATION (MEMORY PROFILER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a script to read a 5-Gigabyte CSV file containing 
# 10 million rows of log data. They write `data = file.readlines()`. When they 
# run the script, the RAM usage mathematically skyrockets from 50 MB to 18 GB. 
# The Operating System immediately kills the script (OOM Killer) to prevent the 
# entire server from crashing.
#
# A senior software engineer uses `memory_profiler`. They execute a line-by-line 
# static analysis of RAM consumption. The profiler mathematically proves that 
# instantiating 10 million Object instances inside a massive List is destroying 
# the heap. The engineer refactors the List into a `Generator` (`yield`), and 
# implements `__slots__` on the class to eradicate the hidden `__dict__` overhead. 
# The RAM usage violently collapses from 18 GB down to a perfectly flat 50 MB, 
# and the script executes flawlessly on a cheap $5/month cloud server.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master granular RAM tracking via `memory_profiler`.
# - Execute architectural memory optimization via `__slots__`.
# - Architect O(1) Memory Streaming via Generators (`yield`).
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE MEMORY HOG)
# ==============================================================================
# In a real environment, you run `mprof run script.py` and put the 
# @profile decorator on the function you want to measure.

class StandardUser:
    """
    The Junior Approach.
    Every standard Python object mathematically contains a hidden `__dict__` 
    to store its attributes. A dictionary is a massive Hash Table.
    If you make 1,000,000 users, you make 1,000,000 Hash Tables!
    """
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name


class OptimizedUser:
    """
    The Senior Approach.
    By declaring `__slots__`, we mathematically command the CPython interpreter 
    to DESTROY the hidden `__dict__`. The object is now a rigid C-struct.
    It uses 60% less RAM and instantiates 20% faster.
    """
    __slots__ = ['uid', 'name']
    
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name


# ==============================================================================
# 4. THE MEMORY PROFILER SIMULATOR
# ==============================================================================
class MemoryProfilerSimulator:
    """
    Simulates the exact output of the `memory_profiler` library.
    It shows you exactly how a senior engineer tracks RAM per line of code.
    """
    @staticmethod
    def display_mock_output():
        print("  [INIT] Executing mprof (Memory Profiler)...\n")
        
        output = """
        Filename: main.py

        Line #    Mem usage    Increment  Occurrences   Line Contents
        =============================================================
            40     50.0 MiB     50.0 MiB           1   @profile
            41                                         def process_massive_data():
            42                                             # [THE DISASTER] Loading everything into RAM at once!
            43   1050.0 MiB   1000.0 MiB           1       massive_list = [StandardUser(i, "Bob") for i in range(5_000_000)]
            44                                             
            45                                             # [THE FIX] Using __slots__
            46    450.0 MiB   -600.0 MiB           1       optimized_list = [OptimizedUser(i, "Bob") for i in range(5_000_000)]
            47                                             
            48                                             # [THE ARCHITECTURE] Using a Generator!
            49     50.0 MiB   -400.0 MiB           1       stream = (OptimizedUser(i, "Bob") for i in range(5_000_000))
            50     50.0 MiB      0.0 MiB     5000001       for user in stream:
            51     50.0 MiB      0.0 MiB     5000000           pass # RAM is mathematically flat!
        """
        print(output)
        
        print("  [ANALYSIS]")
        print("  Notice the `Increment` column. It proves exactly how much RAM ")
        print("  was mathematically allocated by the Operating System on that exact line.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_optimization():
    section_header("Profiling & Optimization: Memory Profiler")
    
    MemoryProfilerSimulator.display_mock_output()
    
    print("\n  [EXECUTION] Running live `sys.getsizeof` calculations to prove the math...")
    
    # 1. Proving the __slots__ Optimization
    u1 = StandardUser(99, "Alice")
    u2 = OptimizedUser(99, "Alice")
    
    # We must measure the Object AND its hidden dictionary!
    size1 = sys.getsizeof(u1) + sys.getsizeof(u1.__dict__)
    size2 = sys.getsizeof(u2) # No dictionary exists!
    
    print(f"  -> Standard Object RAM:  {size1} bytes")
    print(f"  -> __slots__ Object RAM: {size2} bytes")
    
    saved = ((size1 - size2) / size1) * 100
    print(f"  -> [FLAWLESS] `__slots__` mathematically eliminated {saved:.0f}% of the RAM overhead.")
    
    # 2. Proving the Generator Optimization
    massive_list = [i for i in range(1_000_000)]
    massive_generator = (i for i in range(1_000_000))
    
    list_size = sys.getsizeof(massive_list) / 1024 / 1024 # MB
    gen_size = sys.getsizeof(massive_generator) # Bytes
    
    print(f"\n  -> List of 1M Ints RAM: {list_size:.2f} MB")
    print(f"  -> Generator of 1M Ints RAM: {gen_size} bytes (Flat O(1) Memory)")
    print("  -> [FLAWLESS] The Generator mathematically evaluates data lazily, averting OOM crashes.")


def run_all_labs():
    demonstrate_optimization()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does Python attach a hidden `__dict__` to almost every Object by default, and how does `__slots__` structurally change the Object in C memory?"
   Senior Answer: "Dynamic Metaprogramming. Python is designed to be highly dynamic. By attaching a Hash Table (`__dict__`) to every object, developers can randomly do `user.favorite_color = 'Blue'` at runtime, even if `favorite_color` wasn't defined in the `__init__`. The cost of this flexibility is massive RAM overhead. When you declare `__slots__ = ['uid', 'name']`, you mathematically command the CPython compiler to deny metaprogramming. The object is instantiated as a rigid C-struct with exactly two fixed pointers. If a developer tries `user.color = 'Blue'`, the interpreter violently crashes with an AttributeError, mathematically protecting the system's memory constraints."

2. Interviewer: "If `memory_profiler` gives us such granular, line-by-line data, how does it physically hook into the Operating System to measure the RAM?"
   Senior Answer: "The `/proc` Filesystem (psutil). Unlike `tracemalloc`, which hooks into Python's internal memory allocator, `memory_profiler` relies on the external `psutil` library. Before executing a line of code, the profiler queries the Linux Kernel (via `/proc/self/statm` or equivalent) to check the physical RSS (Resident Set Size) of the Python process. It executes the line of Python code, queries the OS again, and computes the mathematical Delta (the `Increment` column). Because it queries the OS on every single line, it causes massive execution latency, which is why it is strictly used for debugging and never in Production."

3. Interviewer: "If a developer writes a function to read a $50$ GB log file, how do Generators (`yield`) mathematically prevent the server from crashing?"
   Senior Answer: "Lazy Evaluation vs Eager Evaluation. If the developer uses `.readlines()`, the interpreter executes Eager Evaluation. It commands the Hard Drive to read all $50$ GBs, loads it entirely into RAM as a massive List of strings, and then begins processing. The server crashes. If the developer writes `for line in file: yield line`, they architect a Generator. This is Lazy Evaluation. The script reads exactly *one* line from the Hard Drive (e.g., $100$ bytes), processes it, discards it, and then yields the next line. The memory consumption is mathematically locked at $O(1)$ ($100$ bytes) regardless of whether the file is $50$ MB or $500$ Terabytes."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Optimization (Memory Profiler) Completed.")
