"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (PROFILING - CPROFILE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive Python application is running too slow. 
#
# A junior engineer uses `time.time()` to randomly wrap suspected functions, 
# guessing wildly at where the bottleneck might be. They spend 3 days optimizing 
# a loop that only accounted for 1% of the total execution time, achieving zero 
# measurable impact.
#
# A senior engineer understands "Deterministic Profiling". They deploy `cProfile`, 
# a C-level extension built into Python. In 5 seconds, the profiler mathematically 
# hooks into the CPython interpreter, records the exact microsecond every single 
# function was called, how many times it was called, and its exact aggregate 
# execution time. The engineer instantly sorts the report by "Cumulative Time", 
# mathematically identifying the exact function causing 90% of the delay.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Deterministic Profiling using the `cProfile` module.
# - Master analyzing Profile output using the `pstats` module.
# - Differentiate between "Total Time" (tottime) and "Cumulative Time" (cumtime).
#
# ==============================================================================
"""

import time
import math
import cProfile
import pstats
import io

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MYSTERY BOTTLENECK (THE TARGET SCRIPT)
# ==============================================================================
def fast_function():
    """Executes very quickly, but is called 1,000,000 times!"""
    total = 0
    for _ in range(10):
        total += 1
    return total

def slow_function():
    """Executes only once, but contains a massive hidden delay."""
    time.sleep(1.2) # Simulating a slow database query or API call
    return 0

def CPU_heavy_function():
    """Burns massive CPU cycles executing raw math."""
    total = 0.0
    for i in range(3_000_000):
        total += math.sqrt(i)
    return total

def master_application():
    """The main entry point. Where is the bottleneck?!"""
    # 1. The fast function (Called 1,000,000 times!)
    for _ in range(1_000_000):
        fast_function()
        
    # 2. The slow I/O function
    slow_function()
    
    # 3. The CPU heavy function
    CPU_heavy_function()


# ==============================================================================
# 4. EXECUTING CPROFILE PROGRAMMATICALLY
# ==============================================================================
def demonstrate_cprofile():
    section_header("Deterministic Profiling: CProfile & PStats")
    
    print("  [INIT] Engaging C-Level Profiler Hook...")
    
    # 1. Create the Profiler Object
    profiler = cProfile.Profile()
    
    # 2. Start the Profiler! It now tracks EVERY SINGLE FUNCTION CALL.
    profiler.enable()
    
    print("  [EXECUTION] Running the Master Application...")
    master_application()
    
    # 3. Stop the Profiler!
    profiler.disable()
    
    print("  [ANALYSIS] Generating the Mathematical Report...\n")
    
    # We use `io.StringIO` to capture the print output for clean formatting.
    s = io.StringIO()
    
    # The `pstats` module reads the raw binary profile data and formats it!
    sortby = pstats.SortKey.CUMULATIVE # We sort by TOTAL time spent in the function!
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    
    # We only want to see the Top 10 worst offenders!
    ps.print_stats(10)
    
    # Output the result
    print(s.getvalue())


def run_all_labs():
    demonstrate_cprofile()
    
    print("\n  [PRO-TIP] You can also run cProfile directly from the CLI without changing code!")
    print("  Command: `python -m cProfile -s cumtime your_script.py`")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In a cProfile report, what is the mathematical distinction between `tottime` (Total Time) and `cumtime` (Cumulative Time), and why is it critical for finding bottlenecks?"
   Senior Answer: "`tottime` (Total Time) is the exact time the CPU spent executing the internal code of a specific function, *excluding* any time spent waiting for sub-functions to finish. `cumtime` (Cumulative Time) is the total time spent in a function *including* all of its sub-functions. For example, if `master_application()` does nothing but call `slow_function()`, `master_application` will have a `tottime` of $0.00$ seconds, but a `cumtime` of $1.20$ seconds! If you sort by `tottime`, you find the exact 'leaf' nodes (the loops or I/O calls) burning CPU. If you sort by `cumtime`, you trace the high-level architectural path that led to the bottleneck."

2. Interviewer: "What does 'Deterministic Profiling' mean in the context of cProfile, and what is its primary disadvantage?"
   Senior Answer: "Deterministic Profiling means that `cProfile` hooks directly into the CPython Interpreter's C-API and mathematically logs an event for every single function `call`, `return`, and `exception`. It is $100\\%$ mathematically accurate and misses absolutely nothing. The catastrophic disadvantage is the Observer Effect (Overhead). If a function is microscopic and called $10,000,000$ times, the time spent logging the $10,000,000$ `call/return` events inside the C-Profiler will massively distort the execution time, making the fast function falsely appear as a massive bottleneck! Deterministic profiling heavily penalizes high-frequency function calls."

3. Interviewer: "If `cProfile` introduces massive overhead on high-frequency function calls, how do Senior Engineers profile massive production web servers without crashing them?"
   Senior Answer: "They completely abandon Deterministic Profilers (`cProfile`) and switch to 'Statistical Profilers' (like `py-spy` or `Austin`). A Statistical Profiler runs as a completely separate OS Process. Instead of hooking into Python's function calls, it simply wakes up $100$ times a second, aggressively inspects the OS RAM to read the Python Interpreter's execution stack, records what line of code is currently executing, and goes back to sleep. Because it operates externally by sampling RAM, it incurs a mathematically fixed $<1\\%$ overhead, making it incredibly safe to attach to a live Production server handling 10,000 requests a second."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling (cProfile) Completed.")
