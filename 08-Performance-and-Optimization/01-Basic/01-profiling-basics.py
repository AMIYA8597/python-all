"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (PROFILING BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# "Premature optimization is the root of all evil" (Donald Knuth). 
# Before you optimize code, you MUST mathematically prove exactly where the 
# bottleneck is. Guessing wastes engineering hours.
#
# A junior engineer guesses that a specific `for` loop is slow, spends 3 days 
# writing a C-extension for it, and the application only speeds up by 1%.
#
# A senior engineer deploys `cProfile` and discovers that 98% of the execution 
# time is actually being blocked by an invisible I/O bottleneck during logging. 
# They fix the logger in 5 minutes, doubling the speed of the entire application.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master deterministic profiling (`cProfile`).
# - Master interpreting execution statistics (tottime vs cumtime).
# - Understand the overhead of `time.sleep` vs CPU-bound math.
#
# ==============================================================================
"""

import cProfile
import pstats
import time
import math
import io

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TARGET FUNCTIONS (CPU-BOUND VS I/O-BOUND)
# ==============================================================================
def cpu_heavy_function(n: int) -> float:
    """A CPU-bound function doing raw mathematical calculations."""
    result = 0.0
    for i in range(1, n):
        # Math operations physically lock the CPU cores!
        result += math.sqrt(i) * math.sin(i)
    return result

def io_heavy_function() -> None:
    """An I/O-bound function simulating database calls or network requests."""
    # Sleeping doesn't use the CPU at all! It physically blocks the thread 
    # and waits for the OS scheduler to wake it up.
    time.sleep(0.5)

def monolithic_application():
    """A master function calling multiple sub-systems."""
    print("  [APP] Starting application execution...")
    
    # Fast loop
    cpu_heavy_function(100_000)
    
    # Slow loop (The mathematical bottleneck!)
    cpu_heavy_function(5_000_000)
    
    # Network request simulation (The I/O bottleneck!)
    io_heavy_function()
    
    print("  [APP] Application execution complete.")


# ==============================================================================
# 4. EXECUTING THE PROFILER (`cProfile`)
# ==============================================================================
def demonstrate_cprofile():
    section_header("Performance Profiling (cProfile)")
    
    # 1. Initialize the Profiler Engine
    profiler = cProfile.Profile()
    
    # 2. Activate tracking!
    profiler.enable()
    
    # 3. Execute the code we want to measure!
    monolithic_application()
    
    # 4. Deactivate tracking!
    profiler.disable()
    
    # 5. Format and Export the Statistics!
    # We use io.StringIO to capture the report in memory so we can print it cleanly.
    s = io.StringIO()
    # Sort the results by 'cumulative time' (cumtime) to instantly surface the slowest functions!
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    
    # Print only the top 10 most expensive function calls!
    ps.print_stats(10)
    
    print("\n--- PROFILER REPORT ---")
    print(s.getvalue())
    print("-----------------------")


def run_all_labs():
    demonstrate_cprofile()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In a `cProfile` report, what is the critical mathematical difference between `tottime` and `cumtime`?"
   Senior Answer: "`tottime` (Total Time) is the exact amount of time the CPU spent executing the specific logic *exclusively inside that function*, ignoring the time spent inside sub-functions that it called. `cumtime` (Cumulative Time) is the total elapsed time from the moment the function was entered to the moment it returned, which *includes* the execution time of every single sub-function it invoked. If `main()` takes 5 seconds, but 4.9 seconds of that was spent waiting for `database_query()` to finish, `main()` will have a `cumtime` of 5.0, but a `tottime` of only 0.1."

2. Interviewer: "Why is `cProfile` implemented in C rather than pure Python, and what is 'Profiler Overhead'?"
   Senior Answer: "Deterministic profiling mathematically injects tracking hooks into every single function call and return event across the entire Python interpreter. If the profiler was written in pure Python, executing those tracking hooks would take longer than the actual code being measured, severely distorting the statistical reality of the application (Profiler Overhead). `cProfile` is a C-extension module physically compiled into the Python interpreter, allowing the tracking hooks to execute at native C speeds, drastically minimizing the observational distortion on the CPU."

3. Interviewer: "If an application is heavily I/O bound (lots of `time.sleep` or network requests), will a CPU profiler accurately measure the bottleneck?"
   Senior Answer: "Standard CPU profilers primarily measure the time the thread is actively burning CPU cycles. When a thread executes an I/O operation (like `time.sleep` or waiting on a socket), the OS physically evicts the thread from the CPU core (Thread Yielding). The thread is doing absolutely zero work; it is just waiting. `cProfile` tracks Wall-Clock time (elapsed time), so it *will* show the sleep delay in `cumtime`, but advanced CPU-instruction profilers (like `perf` on Linux) might ignore it completely because the CPU was physically idle. For I/O bottlenecks, Distributed Tracing (like OpenTelemetry) or Network Profiling is vastly superior."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Performance (Profiling Basics) Completed.")
