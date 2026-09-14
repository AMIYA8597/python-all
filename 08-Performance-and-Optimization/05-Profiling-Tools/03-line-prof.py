"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (LINE-BY-LINE TIME PROFILING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# `cProfile` proves that `calculate_trajectory()` takes 12 seconds to run. 
# But `calculate_trajectory()` is 300 lines long. Where exactly in those 300 
# lines is the CPU burning time?
#
# A junior engineer resorts to breaking the function into 20 sub-functions just 
# to get `cProfile` to show more detail, ruining the architecture of the code.
#
# A senior engineer installs `line_profiler`. By placing an `@profile` decorator 
# on the exact 300-line function, they generate a mathematical breakdown showing 
# the exact microseconds spent on every single line of code. They instantly 
# discover that a seemingly innocent `if x in massive_list` (O(N) operation) on 
# line 142 is consuming 11.8 seconds of the 12-second total.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master line-by-line CPU time profiling using `line_profiler`.
# - Prove the CPU time difference between O(N) list lookups and O(1) set lookups.
# - Understand the architecture of the `kernprof` execution engine.
#
# ==============================================================================
"""

import time
import math
import sys

# We gracefully handle the absence of the third-party line_profiler library!
try:
    from line_profiler import profile
    HAS_LINE_PROF = True
except ImportError:
    HAS_LINE_PROF = False
    # If missing, we create a dummy decorator to prevent syntax errors.
    # We will simulate the output instead!
    def profile(func):
        return func

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TARGET SCRIPT: THE HIDDEN BOTTLENECK
# ==============================================================================
# We apply the @profile decorator!
# Note: `line_profiler` does NOT automatically run when executing the script via `python`.
# You must execute it via the `kernprof` CLI tool!

@profile
def mathematical_trajectory_simulation():
    """
    Simulates calculating paths. 
    It contains a massive, hidden architectural mistake on line 64.
    """
    total = 0.0
    
    # 1. Fast math!
    for i in range(10_000):
        total += math.sqrt(i)
        
    # 2. Setup some data
    massive_dataset = list(range(100_000))
    search_targets = [99_999, 50_000, 10_000]
    
    # 3. THE BOTTLENECK (O(N) search inside a loop!)
    # A junior engineer used a List for the dataset instead of a Set!
    for target in search_targets:
        # The CPU must linearly scan up to 100,000 elements for EVERY target!
        if target in massive_dataset:
            total += target
            
    # 4. Final fast math!
    for i in range(10_000):
        total += math.sin(i)
        
    return total


# ==============================================================================
# 4. EXECUTING THE LINE PROFILER (OR SIMULATING)
# ==============================================================================
def demonstrate_line_profiler():
    section_header("Line-by-Line Time Profiling (line_profiler)")
    
    if not HAS_LINE_PROF:
        print("  [ERROR] `line_profiler` is not installed.")
        print("  Run `pip install line_profiler` to execute this lab properly.")
        print("  (We will simulate the expected `kernprof` output below instead.)")
        print("\n  [SIMULATED KERNPROF OUTPUT]")
        print("  Timer unit: 1e-06 s")
        print("\n  Total time: 0.04153 s")
        print("  File: 03-line-prof.py")
        print("  Function: mathematical_trajectory_simulation at line 50")
        print("\n  Line #      Hits         Time  Per Hit   % Time  Line Contents")
        print("  ==============================================================")
        print("      50                                           @profile")
        print("      51                                           def mathematical_trajectory_simulation():")
        print("      56         1          1.0      1.0      0.0      total = 0.0")
        print("      59     10001        450.0      0.0      1.1      for i in range(10_000):")
        print("      60     10000       1200.0      0.1      2.9          total += math.sqrt(i)")
        print("      63         1       2100.0   2100.0      5.1      massive_dataset = list(range(100_000))")
        print("      64         1          2.0      2.0      0.0      search_targets = [99_999, 50_000, 10_000]")
        print("      68         4          4.0      1.0      0.0      for target in search_targets:")
        print("      70         3      36000.0  12000.0     86.7          if target in massive_dataset:")
        print("      71         3          3.0      1.0      0.0              total += target")
        print("      74     10001        450.0      0.0      1.1      for i in range(10_000):")
        print("      75     10000       1320.0      0.1      3.2          total += math.sin(i)")
        print("      77         1          0.0      0.0      0.0      return total")
        return
        
    print("  [WARNING] You must run this script via the `kernprof` CLI tool to see the real output!")
    print("  Execute this command in your terminal:")
    print("  `kernprof -l -v 03-line-prof.py`")
    
    # We execute it so `kernprof` can trace it when run from the CLI!
    mathematical_trajectory_simulation()


def run_all_labs():
    demonstrate_line_profiler()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why doesn't `cProfile` provide line-by-line profiling out of the box? Why must we install a separate library like `line_profiler`?"
   Senior Answer: "Because of the catastrophic mathematical overhead of hooking into the C-API. `cProfile` operates at the *function* level. If a function is called once, `cProfile` logs two events: the `call` and the `return`. If that function contains 100,000 lines of code, `cProfile` doesn't care; it remains perfectly performant. If you force a profiler to operate at the *line* level, the profiler must violently intercept the CPython Interpreter before executing EVERY SINGLE LINE OF BYTECODE. If a loop executes 1,000,000 times, `line_profiler` must intercept the CPU 1,000,000 times to log the timestamp! This generates such astronomical overhead that line-profiling is physically excluded from standard libraries and must be manually injected via specialized C-extensions like `kernprof`."

2. Interviewer: "In the simulated output, the line `if target in massive_dataset:` took $86.7\\%$ of the total CPU time, while the 10,000 `math.sqrt()` calculations only took $2.9\\%$. Why?"
   Senior Answer: "This proves the mathematical dominance of Big-O Notation over raw instruction counts. `math.sqrt()` is mathematically $O(1)$; it executes directly in the C-layer FPU (Floating Point Unit) in hardware. Calling it 10,000 times is 10,000 fast operations. The `in` operator on a Python `list` is $O(N)$. Because `massive_dataset` contains 100,000 elements, checking if $99,999$ is inside it forces the CPU to execute a linear loop, sequentially comparing $99,999$ elements one by one. Calling that $O(N)$ lookup 3 times physically forced the CPU to execute $\\approx 150,000$ sequential comparisons! Changing `massive_dataset` to a `set()` would change the lookup to $O(1)$, instantly dropping the time from $86.7\\%$ down to $<0.1\\%$."

3. Interviewer: "What is `kernprof`, and why do we use it instead of running the script normally with `python script.py`?"
   Senior Answer: "`kernprof` is the underlying execution engine/CLI tool that ships with the `line_profiler` library. If you run the script normally with `python script.py`, the `@profile` decorator simply executes as a 'dummy' decorator, doing absolutely nothing, so your production code doesn't crash if the library isn't installed. When you execute via `kernprof -l -v script.py`, `kernprof` physically injects the C-level tracing hooks into the Python built-in namespace, activates the `@profile` decorators, runs the script in a heavily monitored C-sandbox, and then mathematically formats and dumps the line-by-line statistics to the terminal (`-v` for view) and a binary `.lprof` file."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling (Line Profiler) Completed.")
