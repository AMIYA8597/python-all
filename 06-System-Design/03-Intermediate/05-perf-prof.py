"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (PERFORMANCE PROFILING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Your Python web server is running at 100% CPU. It is extremely slow.
# 
# A junior engineer looks at the code and guesses: "It must be the JSON parsing! 
# Let's spend 3 weeks rewriting the JSON parser in C++!"
# They deploy the C++ parser. The CPU remains at 100%. The server is still slow.
# They guessed wrong.
#
# Performance Optimization is a mathematical science, not a guessing game. 
# Before you optimize a single line of code, you MUST run a Profiler. 
# A Profiler intercepts the CPU thousands of times a second and records EXACTLY 
# which functions are consuming the most milliseconds.
#
# It turns out the JSON parser took 2% of the CPU. The real bottleneck was a 
# rogue O(N^2) `for` loop in a logging function that was silently eating 95% 
# of the CPU. By deleting one line of code, you fixed the server in 5 minutes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the scientific method of Optimization (Measure, Analyze, Fix).
# - Master Python's built-in `cProfile`.
# - Understand the concept of Flamegraphs and Bottlenecks.
#
# ==============================================================================
"""

import cProfile
import pstats
import time
import io

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MYSTERY BOTTLENECK (cProfile)
# ==============================================================================

def fast_database_query():
    """Simulates a perfectly optimized database query."""
    # Takes 0.01 seconds
    time.sleep(0.01)
    return [i for i in range(100)]

def innocent_looking_logging(data: list[int]):
    """
    A seemingly innocent function that actually contains a catastrophic 
    O(N^2) mathematical bottleneck!
    """
    # A terrible String Concatenation loop. 
    # Strings in Python are Immutable! Every time you do `s += str`, it forces 
    # the OS to allocate a brand new block of RAM and copy the entire string over!
    # This creates a massive hidden O(N^2) CPU and Memory explosion.
    log_string = ""
    for num in data:
        for _ in range(500): # Simulating terrible nested logic
            log_string += str(num)
    return log_string

def process_user_request():
    """The main entry point for the web server."""
    data = fast_database_query()
    log = innocent_looking_logging(data)
    return "Success"

def demonstrate_cprofile():
    section_header("Performance Profiling (Hunting the Bottleneck)")
    
    print("A user request takes way too long! We suspect the Database is slow.")
    print("Instead of guessing, we run the CPU Profiler (`cProfile`)...")
    print("-" * 60)
    
    # 1. Create the Profiler
    profiler = cProfile.Profile()
    
    # 2. Turn it on! (It starts injecting itself into the CPU)
    profiler.enable()
    
    # 3. Run the suspicious code
    process_user_request()
    
    # 4. Turn it off!
    profiler.disable()
    
    # 5. Extract and format the raw mathematical data
    s = io.StringIO()
    # Sort by 'cumulative' time to find the absolute worst offenders
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    
    # Print only the top 10 worst functions
    ps.print_stats(10)
    
    print(s.getvalue())
    print("-" * 60)
    
    print("ANALYSIS OF THE PROFILER DATA:")
    print("1. Look at 'fast_database_query'. It only took ~0.010 seconds (tottime).")
    print("2. Look at 'innocent_looking_logging'. It took astronomically more time!")
    print("3. Look at the built-in '{method 'sleep' of '_time.time' objects}'.")
    print("   The database spent its time sleeping (I/O). The logging spent its time ")
    print("   actively destroying the CPU with string allocations!")
    print("\nConclusion: The Database is completely innocent. We must fix the logger!")


def run_all_labs():
    demonstrate_cprofile()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the difference between `tottime` (Total Time) and `cumtime` (Cumulative Time) in cProfile.
   Answer: `tottime` measures the exact amount of time the CPU spent *physically inside that specific function's block of code*, excluding any time spent inside sub-functions that it called. `cumtime` measures the total time from the moment the function started to the moment it returned, *including* all the time spent inside any sub-functions it called. For example, `main()` might have a `tottime` of 0.001s, but a `cumtime` of 10.0s because it called `heavy_math()`, which took 9.999s. You sort by `cumtime` to trace the path down the execution tree, and you look for high `tottime` to find the physical function that is actually doing the damage.

2. Why is String Concatenation (`str += str`) in a `for` loop a catastrophic $O(N^2)$ bottleneck in Python/Java?
   Answer: Strings in high-level languages are strictly Immutable. They are etched into physical RAM and mathematically cannot be resized. When you execute `A += B`, the CPU does not append B to A. It requests a completely *brand new* block of RAM large enough to hold `A + B`. It then manually copies every single character from `A` into the new block, and then copies `B`. If you loop this $N$ times, the first loop copies 1 character. The 10,000th loop copies 10,000 characters. $1 + 2 + 3 ... + N = \frac{N(N+1)}{2}$. This transforms a simple $O(N)$ loop into a disastrous $O(N^2)$ CPU and Memory explosion. The solution is to use `.join()` (Python) or `StringBuilder` (Java).

3. What is a "Flamegraph" and why is it superior to raw cProfile text output?
   Answer: Raw text output from cProfile is chaotic, especially in massive codebases with 5,000 functions calling each other recursively. A Flamegraph is a visual, interactive HTML chart. The X-axis represents the CPU time (width = time spent). The Y-axis represents the Call Stack (who called whom). By simply looking at the chart, the widest physical block instantly identifies the ultimate CPU bottleneck. You can visually trace the block straight down the Y-axis to perfectly understand the exact chain of functions that triggered the catastrophic slowdown, eliminating all guesswork.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Performance Profiling) Completed.")
