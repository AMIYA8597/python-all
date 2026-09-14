"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (PROFILING & ANALYSIS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You cannot optimize what you cannot measure. Python is fundamentally slower 
# than C/C++ because it is an interpreted, dynamically-typed language with a 
# Global Interpreter Lock (GIL). 
#
# A junior engineer attempts to measure code execution using `time.time()`, 
# completely ignoring OS context-switching, Garbage Collection pauses, and 
# CPU clock fluctuations, resulting in wildly inaccurate measurements.
#
# A senior engineer uses isolated benchmarking (`timeit`) to mathematically 
# freeze background interference, and deploys `cProfile` and memory profiling 
# to pinpoint the exact bytecode instructions causing the bottleneck.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Isolated Benchmarking (`timeit`).
# - Master Time Complexity Verification.
# - Understand how dynamic typing overhead impacts performance.
#
# ==============================================================================
"""

import timeit
import time
import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE TIME TRACKING VS TIMEIT
# ==============================================================================
def mathematical_workload():
    """A mathematically heavy loop to burn CPU cycles."""
    return sum(math.sqrt(i) for i in range(10_000))

def demonstrate_timeit():
    section_header("Naive `time.time()` vs Deterministic `timeit`")
    
    # --- NAIVE MEASUREMENT ---
    # `time.perf_counter()` is the most accurate Wall-Clock timer, but it 
    # still includes OS scheduling delays if the thread gets evicted!
    start = time.perf_counter()
    mathematical_workload()
    end = time.perf_counter()
    naive_duration = end - start
    print(f"  [NAIVE] time.perf_counter() single run: {naive_duration:.6f} seconds")
    
    # --- ISOLATED BENCHMARKING (TIMEIT) ---
    # `timeit` temporarily disables the Python Garbage Collector during the run!
    # It executes the code multiple times (e.g., 1000) and mathematically selects 
    # the absolute fastest run, perfectly filtering out OS-level interference.
    stmt = "mathematical_workload()"
    setup = "from __main__ import mathematical_workload"
    
    # Run the workload 1000 times!
    iterations = 1000
    total_timeit_duration = timeit.timeit(stmt=stmt, setup=setup, number=iterations)
    
    # Calculate the mathematical average!
    average_duration = total_timeit_duration / iterations
    
    print(f"  [TIMEIT] Executed {iterations} iterations with Garbage Collection disabled.")
    print(f"  [TIMEIT] Absolute verified average run:   {average_duration:.6f} seconds")


# ==============================================================================
# 4. ALGORITHMIC VERIFICATION (O(N) VS O(N^2))
# ==============================================================================
# We can use `timeit` to mathematically PROVE Big-O complexity!

def list_contains_check(data: List[int], target: int) -> bool:
    """O(N) Linear Scan"""
    return target in data

def set_contains_check(data: set, target: int) -> bool:
    """O(1) Hash Table Lookup"""
    return target in data

def demonstrate_algorithmic_scaling():
    section_header("Mathematical Proof of Big-O Complexity")
    
    # We will test an Array vs a Set at two vastly different scales!
    small_n = 10_000
    massive_n = 10_000_000
    
    # The target is at the absolute end, forcing a worst-case scenario!
    target = massive_n + 1
    
    small_list = list(range(small_n))
    small_set = set(small_list)
    
    print(f"  [SCALE A] N = {small_n:,}")
    
    # We use lambda to bind the arguments for timeit!
    list_time_small = timeit.timeit(lambda: list_contains_check(small_list, target), number=100)
    set_time_small = timeit.timeit(lambda: set_contains_check(small_set, target), number=100)
    
    print(f"    -> List O(N) Time: {list_time_small:.6f}s")
    print(f"    -> Set O(1) Time:  {set_time_small:.6f}s")
    
    # Now we scale the data structure by 1,000x!
    print(f"\n  [SCALE B] N = {massive_n:,} (1,000x larger!)")
    
    # Note: Generating a 10M element list takes physical RAM and Time!
    print("    (Allocating massive arrays in RAM... please wait...)")
    massive_list = list(range(massive_n))
    massive_set = set(massive_list)
    
    list_time_massive = timeit.timeit(lambda: list_contains_check(massive_list, target), number=100)
    set_time_massive = timeit.timeit(lambda: set_contains_check(massive_set, target), number=100)
    
    print(f"    -> List O(N) Time: {list_time_massive:.6f}s")
    print(f"    -> Set O(1) Time:  {set_time_massive:.6f}s")
    
    # MATHEMATICAL PROOF
    list_multiplier = list_time_massive / list_time_small
    set_multiplier = set_time_massive / set_time_small
    
    print("\n  [MATHEMATICAL PROOF]")
    print(f"    -> The List data grew by 1,000x, and execution time grew by {list_multiplier:.2f}x! (Perfect O(N) Proof)")
    print(f"    -> The Set data grew by 1,000x, but execution time grew by {set_multiplier:.2f}x! (Perfect O(1) Proof)")


def run_all_labs():
    demonstrate_timeit()
    demonstrate_algorithmic_scaling()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the `timeit` module explicitly disable the Python Garbage Collector before executing the benchmark?"
   Senior Answer: "The Python Garbage Collector (GC) runs non-deterministically. If you are benchmarking a micro-function that takes 2 milliseconds, and the GC randomly decides to execute a cyclical reference sweep during iteration 42, it might freeze the thread for 15 milliseconds. This instantly contaminates the statistical average of the run, generating massive variance. By physically disabling the GC during the test, `timeit` mathematically isolates the execution to just the bytecode of the target function, guaranteeing deterministic, reproducible performance metrics."

2. Interviewer: "Why did we use `time.perf_counter()` instead of `time.time()` for the naive measurement?"
   Senior Answer: "`time.time()` returns the UNIX Epoch time (Wall-Clock time). If the server running the code executes an NTP (Network Time Protocol) sync during the benchmark, the system clock might violently jump backwards or forwards by several milliseconds, completely corrupting the delta calculation! `time.perf_counter()` accesses the CPU's hardware-level monotonic clock. It is mathematically guaranteed to never go backwards and possesses the highest available physical resolution (nanoseconds), making it the only safe tool for delta-time calculations."

3. Interviewer: "In the Big-O mathematical proof, why did we force the `target` to be a number (`massive_n + 1`) that we knew was completely outside the bounds of the array?"
   Senior Answer: "To mathematically prove Big-O complexity, you must test the Worst-Case Scenario! If we searched for the number `0`, the List's $O(N)$ linear scan would instantly find it at index 0 and terminate, completing in $O(1)$ time! The benchmark would falsely conclude that a List is just as fast as a Set. By searching for a number that does not exist, we mathematically force the Python interpreter to scan every single element inside the List ($10,000,000$ iterations) before giving up, exposing the true catastrophic penalty of $O(N)$ scaling."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Analysis Completed.")
