"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (LINE-BY-LINE MEMORY PROFILING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# `tracemalloc` is incredible for finding memory leaks across a massive application, 
# but it requires manual differential snapshots. Sometimes, an engineer knows 
# exactly *which* function is crashing the server with an OOM (Out-Of-Memory) error, 
# but they have no idea *which line* inside the 500-line function is the culprit.
#
# A senior engineer installs the `memory_profiler` library. By simply adding an 
# `@profile` decorator to the suspect function, they generate a mathematical, 
# line-by-line breakdown showing the exact Megabyte consumption of every single 
# variable assignment, instantly identifying the massive List Comprehension that 
# is devouring 4 Gigabytes of RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master line-by-line memory profiling using `memory_profiler`.
# - Prove the memory behavior of List Comprehensions vs Generator Expressions.
# - Understand the extreme performance overhead of line-by-line profiling.
#
# ==============================================================================
"""

import sys

# We gracefully handle the absence of the third-party memory_profiler library!
try:
    from memory_profiler import profile
    HAS_MEM_PROF = True
except ImportError:
    HAS_MEM_PROF = False
    # Create a dummy decorator so the code doesn't crash if it's missing!
    def profile(func):
        return func

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TARGET SCRIPT: THE MEMORY HOG
# ==============================================================================
# By adding the @profile decorator, the memory_profiler hooks into the C-API.
# It mathematically queries the Operating System for the process's RAM usage 
# BEFORE and AFTER every single line of code in this function!

@profile
def memory_intensive_function():
    """
    We will mathematically prove the difference between creating a physical list 
    in RAM, and creating a lazy generator.
    """
    # 1. Base State
    base_string = "Hello World!"
    
    # 2. Massive Allocation (The RAM Spike!)
    # A list comprehension immediately evaluates and physically constructs 
    # all 5,000,000 strings in RAM simultaneously!
    massive_list = [f"Data_{i}" * 10 for i in range(5_000_000)]
    
    # 3. Deletion (The RAM Drop!)
    # We explicitly free the memory to prove the profiler can track deallocations!
    del massive_list
    
    # 4. Lazy Allocation (Zero RAM Spike!)
    # A Generator Expression `(...)` creates a mathematical rule, not physical data. 
    # It takes up almost zero bytes, regardless of the 5,000,000 iterations!
    lazy_generator = (f"Data_{i}" * 10 for i in range(5_000_000))
    
    return base_string


# ==============================================================================
# 4. EXECUTING THE PROFILER
# ==============================================================================
def demonstrate_memory_profiler():
    section_header("Line-by-Line Memory Profiling (@profile)")
    
    if not HAS_MEM_PROF:
        print("  [ERROR] `memory_profiler` is not installed.")
        print("  Run `pip install memory_profiler` to execute this lab!")
        print("  (We will simulate the expected output below instead.)")
        print("\n  [SIMULATED OUTPUT]")
        print("  Line #    Mem usage    Increment  Occurrences   Line Contents")
        print("  =============================================================")
        print("      46     40.2 MiB     40.2 MiB           1   @profile")
        print("      47                                         def memory_intensive_function():")
        print("      52     40.2 MiB      0.0 MiB           1       base_string = 'Hello World!'")
        print("      57    420.5 MiB    380.3 MiB           1       massive_list = [f'Data_{i}' * 10 for i in range(5_000_000)]")
        print("      61     40.2 MiB   -380.3 MiB           1       del massive_list")
        print("      66     40.2 MiB      0.0 MiB           1       lazy_generator = (f'Data_{i}' * 10 for i in range(5_000_000))")
        print("      68     40.2 MiB      0.0 MiB           1       return base_string")
        return
        
    print("  [EXECUTION] Running the Memory Profiler...")
    print("  (This will take slightly longer than normal due to Profiler overhead!)")
    print("  The report will print automatically to stdout!\n")
    
    memory_intensive_function()


def run_all_labs():
    demonstrate_memory_profiler()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "How does `memory_profiler` mathematically track memory line-by-line, and why is this technique considered catastrophically slow?"
   Senior Answer: "The `memory_profiler` leverages Python's `sys.settrace()` facility. It injects a callback function that is triggered *before every single line of bytecode* is executed. Inside this callback, it executes an OS-level system call (like reading `/proc/self/stat` on Linux) to ask the Operating System exactly how many Megabytes the Python Process is currently consuming. Making an OS Kernel System Call after *every single line of code* is mathematically devastating to performance. A function that normally takes 0.1 seconds to execute might take 15.0 seconds when run under `memory_profiler`. It is an extreme diagnostic tool, never to be used in production."

2. Interviewer: "In the profile output, what is the mathematical difference between the 'Mem usage' column and the 'Increment' column?"
   Senior Answer: "The 'Mem usage' column displays the *Total Absolute RAM* consumed by the entire Python OS Process at the exact moment that line finished executing (e.g., $420$ MiB). The 'Increment' column is the mathematical delta. It subtracts the Mem usage of the *previous* line from the current line, showing exactly how much RAM that specific line of code allocated (e.g., $+380$ MiB) or freed (e.g., $-380$ MiB). The Increment column is what engineers actually look at to instantly identify the line causing the OOM crash."

3. Interviewer: "If the 'massive_list' caused a 380 MiB RAM spike, why did the 'lazy_generator' (which looped the exact same 5,000,000 times) show an Increment of 0.0 MiB?"
   Senior Answer: "Because of Eager vs. Lazy Evaluation. A List Comprehension `[...]` forces the CPU to physically calculate all 5,000,000 strings and permanently lock them into RAM simultaneously, demanding 380 MiB of space. A Generator Expression `(...)` calculates absolutely nothing. It physically allocates a tiny state machine (a generator object) in RAM (usually $\\approx 120$ bytes) that mathematically remembers the *instructions* on how to build the strings. The strings are only materialized into RAM one by one, if and only if the generator is iterated over (e.g., using `next()`), resulting in a constant $O(1)$ memory footprint regardless of N."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling (Memory Profiler) Completed.")
