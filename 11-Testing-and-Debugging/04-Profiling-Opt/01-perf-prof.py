"""
# ==============================================================================
# LABORATORY: PROFILING & OPTIMIZATION (LINE PROFILER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses `cProfile` and determines that the `process_data()` 
# function takes 5 seconds to run. But `process_data()` is a 100-line function! 
# `cProfile` mathematically cannot tell you *which line* inside the function is 
# slow. The developer guesses that the database query is slow, spends a day 
# optimizing SQL, and the function still takes 5 seconds.
#
# A senior software engineer uses `@profile` from the `line_profiler` library. 
# They execute a micro-level static analysis pass on the bytecode. The line 
# profiler prints the exact execution time for every single line of code in the 
# function. It mathematically proves that the SQL query took 0.001 seconds, but 
# a rogue `for` loop executing an `append()` 10 million times took 4.999 seconds. 
# They replace the loop with a List Comprehension, and the function drops to 
# 0.5 seconds immediately.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master granular execution tracking via `line_profiler`.
# - Execute algorithmic optimization (List Comprehensions vs `append`).
# - Architect micro-benchmarking pipelines.
#
# ==============================================================================
"""

import time
import timeit

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE BOTTLENECK)
# ==============================================================================
# In a real environment, you run `kernprof -l -v script.py` and put the 
# @profile decorator on the function you want to measure.

class DataOptimizer:
    
    # @profile (Requires line_profiler installed)
    @staticmethod
    def process_data_slow(data: list) -> list:
        """
        The Junior Approach.
        This function contains a massive, hidden performance bottleneck.
        """
        results = []
        
        # Line A: Basic math (Extremely Fast)
        x = 100 * 50
        
        # Line B: The Bottleneck! (Extremely Slow)
        for item in data:
            # Calling `.append()` on a list inside a massive loop forces Python
            # to do millions of dictionary lookups and function pointer evaluations.
            results.append(item * 2 + x)
            
        return results

    # @profile
    @staticmethod
    def process_data_fast(data: list) -> list:
        """
        The Senior Approach (List Comprehension).
        By moving the logic into a List Comprehension, Python bypasses the 
        `.append()` lookup and executes the loop directly in highly optimized C-code.
        """
        x = 100 * 50
        
        # Line B: The Optimization!
        return [item * 2 + x for item in data]


# ==============================================================================
# 4. THE LINE PROFILER SIMULATOR
# ==============================================================================
class LineProfilerSimulator:
    """
    Simulates the exact output of the `line_profiler` library.
    It shows you exactly how a senior engineer reads the terminal output.
    """
    @staticmethod
    def display_mock_output():
        print("  [INIT] Executing kernprof (Line Profiler)...\n")
        
        output = """
        Timer unit: 1e-06 s

        Total time: 1.25 s
        File: main.py
        Function: process_data_slow at line 42

        Line #      Hits         Time  Per Hit   % Time  Line Contents
        ==============================================================
            42                                           @profile
            43                                           def process_data_slow(data: list) -> list:
            44         1          2.0      2.0      0.0      results = []
            45         1          1.0      1.0      0.0      x = 100 * 50
            46   1000001     250000.0      0.2     20.0      for item in data:
            47   1000000    1000000.0      1.0     80.0          results.append(item * 2 + x)
            48         1          1.0      1.0      0.0      return results
        """
        print(output)
        
        print("  [ANALYSIS]")
        print("  Notice the `% Time` column. It mathematically proves that 80% of the ")
        print("  CPU's time was spent purely evaluating the `.append()` function.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_optimization():
    section_header("Profiling & Optimization: Line Profiler")
    
    LineProfilerSimulator.display_mock_output()
    
    print("\n  [EXECUTION] Running live benchmark on 5,000,000 items to prove the optimization...")
    
    # We generate a massive dataset!
    massive_dataset = list(range(5_000_000))
    
    # BENCHMARK 1: The Slow Loop
    print("  -> Testing `for loop` with `.append()`...")
    start_slow = timeit.default_timer()
    DataOptimizer.process_data_slow(massive_dataset)
    time_slow = timeit.default_timer() - start_slow
    
    # BENCHMARK 2: The List Comprehension
    print("  -> Testing List Comprehension...")
    start_fast = timeit.default_timer()
    DataOptimizer.process_data_fast(massive_dataset)
    time_fast = timeit.default_timer() - start_fast
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Slow Time: {time_slow:.4f} seconds")
    print(f"  Fast Time: {time_fast:.4f} seconds")
    
    if time_fast > 0:
        speedup = time_slow / time_fast
        print(f"  -> [FLAWLESS] The List Comprehension was mathematically {speedup:.1f}x faster!")
        print("  By eliminating the `append` function call overhead, we reclaimed massive CPU cycles.")


def run_all_labs():
    demonstrate_optimization()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does calling `results.append()` inside a loop execute so much slower than writing a List Comprehension `[x for x in data]`?"
   Senior Answer: "Global/Attribute Lookup Overhead. In Python, everything is a dictionary under the hood. When the interpreter sees `results.append()`, it must execute a mathematically expensive `getattr()` call. It hashes the string 'append', searches the `results` object's dictionary for that key, extracts the C-function pointer, and *then* executes the math. If the loop runs $5$ million times, Python wastes CPU cycles doing $5$ million dictionary lookups for a method that never changes. A List Comprehension mathematically bypasses this entirely. The CPython interpreter compiles it into a specialized bytecode instruction (`LIST_APPEND`), which pushes the data directly into the C-array without ever executing a Python-level attribute lookup."

2. Interviewer: "If `line_profiler` gives us such granular, line-by-line data, why don't we just use it everywhere instead of `cProfile`?"
   Senior Answer: "Massive Tracing Overhead. `cProfile` only intercepts the interpreter at the exact moment a function is entered or exited. `line_profiler` is mathematically invasive; it forces the CPython interpreter to halt and record a timestamp before executing *every single line of code*. If you run `line_profiler` on an entire application, the application will run $10\\times$ to $50\\times$ slower, making it impossible to benchmark realistically. The architectural workflow is: Use `cProfile` to quickly find the $1$ broken function out of $1,000$. Then, apply `@profile` *only* to that single broken function to find the exact broken line."

3. Interviewer: "In our benchmark, we moved `x = 100 * 50` outside the loop. Why is this mathematically important for performance?"
   Senior Answer: "Loop Invariant Code Motion. If you put `100 * 50` inside the loop, the CPU will mathematically calculate $5000$ over and over again, $5$ million times. A smart C++ compiler (like GCC or LLVM) will detect this 'Loop Invariant' and automatically move the calculation outside the loop during compilation. However, CPython does *not* do aggressive static optimization; it interprets the bytecode exactly as written. Therefore, the Python developer must manually execute 'Loop Invariant Code Motion', hoisting static calculations out of the loop to prevent millions of wasted CPU cycles."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Optimization (Line Profiler) Completed.")
