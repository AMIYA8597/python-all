"""
# ==============================================================================
# LABORATORY: PROFILING, DEBUGGING, AND MEMORY LEAKS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Premature optimization is the root of all evil." Before optimizing a program 
# (e.g., rewriting it in Cython), you MUST prove where the bottleneck is. 
# `cProfile` identifies slow functions. `tracemalloc` identifies memory leaks.
# `pdb` allows you to freeze execution and inspect the stack when things crash.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `cProfile` and `pstats` to find CPU bottlenecks.
# - Master `tracemalloc` to find memory leaks.
# - Understand the Python Debugger (`pdb`).
#
# ==============================================================================
"""

import time
import cProfile
import pstats
import tracemalloc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CPU PROFILING (cProfile)
# ==============================================================================

def slow_function():
    # Simulate a slow operation
    time.sleep(0.1)
    
def fast_but_frequent_function():
    # Extremely fast, but called many times
    return sum(i for i in range(100))

def main_app_simulation():
    for _ in range(5):
        slow_function()
    for _ in range(1000):
        fast_but_frequent_function()

def demonstrate_cprofile():
    """
    cProfile is a C-extension that hooks into the Python interpreter to track
    every single function call, how many times it was called, and how long it took.
    """
    section_header("CPU Profiling (cProfile)")
    
    print("Profiling the main_app_simulation()...")
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    main_app_simulation()
    
    profiler.disable()
    
    # We use pstats to sort the output so we can actually read it
    stats = pstats.Stats(profiler)
    
    # Sort by cumulative time (time spent in the function AND its sub-functions)
    stats.sort_stats(pstats.SortKey.CUMULATIVE)
    
    print("\n--- Profiling Results (Top 10) ---")
    stats.print_stats(10)
    
    print("Analyze the output: ")
    print(" - ncalls: Number of times the function was called.")
    print(" - tottime: Total time spent in the function ALONE.")
    print(" - cumtime: Total time spent in the function AND all functions it called.")


# ==============================================================================
# 4. MEMORY PROFILING (tracemalloc)
# ==============================================================================

def memory_leak_simulation():
    # We create a massive list of strings
    _leak = [f"Memory leak item {i}" for i in range(100_000)]
    return _leak

def demonstrate_tracemalloc():
    """
    tracemalloc hooks into Python's memory allocator to track exactly which 
    line of code allocated which block of memory.
    """
    section_header("Memory Profiling (tracemalloc)")
    
    print("Starting tracemalloc...")
    tracemalloc.start()
    
    # Take a snapshot BEFORE the leak
    snapshot1 = tracemalloc.take_snapshot()
    
    print("Executing leaky function...")
    _leaked_data = memory_leak_simulation()
    
    # Take a snapshot AFTER the leak
    snapshot2 = tracemalloc.take_snapshot()
    
    print("\n--- Memory Allocation Differences ---")
    # Compare the two snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    for stat in top_stats[:3]:
        print(stat)
        
    print("\nNotice how tracemalloc points EXACTLY to the line of code that allocated the RAM!")
    
    tracemalloc.stop()


# ==============================================================================
# 5. THE PYTHON DEBUGGER (PDB)
# ==============================================================================

def demonstrate_pdb():
    """
    Python 3.7+ includes the built-in `breakpoint()` function.
    When Python hits this line, it freezes the program and drops you into 
    an interactive console where you can inspect variables and step through code.
    """
    section_header("Python Debugger (pdb)")
    
    print("To use the debugger, place the `breakpoint()` function in your code.")
    print("Useful PDB commands:")
    print(" - l (list): Shows the code around the current line.")
    print(" - n (next): Executes the current line and goes to the next.")
    print(" - s (step): Steps INTO the function call on the current line.")
    print(" - c (continue): Resumes execution until the next breakpoint.")
    print(" - p var (print): Prints the value of a variable.")
    print("\nExample:")
    print("def calculate(x, y):")
    print("    breakpoint()  <-- Program freezes here")
    print("    return x / y")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `tottime` and `cumtime` in cProfile?
   Answer: `tottime` is the time spent executing the code in that specific function alone. `cumtime` (cumulative time) includes `tottime` PLUS the time spent inside any other functions that were called by this function.

2. Why use `tracemalloc` instead of just checking OS RAM usage?
   Answer: Checking OS RAM only tells you THAT the application is leaking memory. `tracemalloc` hooks into Python's allocator and tells you EXACTLY WHICH LINE of code is responsible for allocating the memory that hasn't been freed.

3. How do you trigger the Python debugger in modern Python?
   Answer: Simply call `breakpoint()` anywhere in your code.
"""

if __name__ == "__main__":
    demonstrate_cprofile()
    demonstrate_tracemalloc()
    demonstrate_pdb()
    print("\n[SUCCESS] Laboratory: Profiling & Debugging Completed.")
