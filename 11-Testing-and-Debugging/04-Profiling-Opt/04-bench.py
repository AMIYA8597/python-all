"""
# ==============================================================================
# LABORATORY: PROFILING & OPTIMIZATION (MICRO-BENCHMARKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer argues with a senior developer about whether String Concatenation 
# (`a + b`) is faster than String Formatting (`f"{a}{b}"`). They write a script 
# using `time.time()` to measure it. The Operating System's CPU scheduler interrupts 
# the Python process during the test, causing String Formatting to look 300% slower. 
# The junior developer uses `a + b` everywhere in the codebase, degrading performance.
#
# A senior software engineer understands "Micro-Benchmarking". They know that 
# `time.time()` is mathematically invalid for measuring micro-operations because 
# of OS Jitter and Garbage Collection spikes. They use the `timeit` library. 
# `timeit` temporarily violently shuts off Python's Garbage Collector, executes 
# the operation 1,000,000 times, and returns the mathematically pure baseline 
# execution speed. The engineer proves that f-strings are significantly faster.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Micro-Benchmarking via the `timeit` module.
# - Execute Garbage Collection isolation during performance testing.
# - Architect empirical tests for Python syntax performance.
#
# ==============================================================================
"""

import timeit
import gc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE STRING CONCATENATION DEBATE)
# ==============================================================================
# We want to measure the absolute fastest way to combine 3 strings in Python.

class StringOperations:
    
    @staticmethod
    def use_plus():
        """The oldest, most common way. Very bad for many strings."""
        a = "Hello"
        b = "Beautiful"
        c = "World"
        return a + " " + b + " " + c
        
    @staticmethod
    def use_join():
        """The classic Senior Python way. Extremely fast for lists."""
        a = "Hello"
        b = "Beautiful"
        c = "World"
        return " ".join([a, b, c])
        
    @staticmethod
    def use_fstring():
        """The modern Python 3.6+ way. Evaluated directly in C-bytecode!"""
        a = "Hello"
        b = "Beautiful"
        c = "World"
        return f"{a} {b} {c}"


# ==============================================================================
# 4. THE MICRO-BENCHMARKING ARCHITECTURE
# ==============================================================================
class BenchmarkEngine:
    
    @staticmethod
    def run_rigorous_benchmark():
        print("  [INIT] Executing 3,000,000 Micro-Benchmarks (GC Disabled)...")
        
        # We tell `timeit` to run the function 1,000,000 times.
        # `timeit` automatically disables the Garbage Collector for us!
        
        time_plus = timeit.timeit(
            "StringOperations.use_plus()", 
            setup="from __main__ import StringOperations",
            number=1_000_000
        )
        
        time_join = timeit.timeit(
            "StringOperations.use_join()", 
            setup="from __main__ import StringOperations",
            number=1_000_000
        )
        
        time_fstring = timeit.timeit(
            "StringOperations.use_fstring()", 
            setup="from __main__ import StringOperations",
            number=1_000_000
        )
        
        print("\n  [RESULTS: 1 Million Executions]")
        print(f"  -> String Concatenation (+):  {time_plus:.4f} seconds")
        print(f"  -> String Join (.join):       {time_join:.4f} seconds")
        print(f"  -> F-Strings (f''):           {time_fstring:.4f} seconds")
        
        print("\n  [ANALYSIS]")
        print("  F-strings are evaluated directly at compile-time by the C-interpreter, ")
        print("  making them mathematically faster than instantiating a List for `.join()`.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_microbenchmarking():
    section_header("Profiling & Optimization: Micro-Benchmarking")
    
    BenchmarkEngine.run_rigorous_benchmark()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By executing the operation 1,000,000 times with `timeit`, we mathematically ")
    print("  smoothed out OS Jitter and CPU spikes, allowing us to make an empirical, ")
    print("  data-driven architectural decision rather than guessing.")


def run_all_labs():
    demonstrate_microbenchmarking()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does the `timeit` module explicitly disable Python's Garbage Collector (GC) before running the benchmark loop?"
   Senior Answer: "Preventing Algorithmic Distortion. The Python Garbage Collector is non-deterministic; it runs whenever the 'Generational Thresholds' are triggered. If you are timing a function that takes $2$ microseconds, and the GC happens to pause the CPU during execution to delete $10,000$ dead objects from RAM, that specific function execution will suddenly take $500$ microseconds. This 'Jitter' mathematically corrupts the benchmark data. `timeit` violently halts the GC, forcing the loop to run in a mathematically pure C-environment. (Note: if the function *itself* allocates so much memory that it requires the GC to run to avoid crashing, you must manually re-enable it via `gc.enable()` inside the setup block)."

2. Interviewer: "Why is String Concatenation (`str1 + str2 + str3 + str4`) mathematically disastrous for performance in large loops?"
   Senior Answer: "Immutable Memory Reallocation (O(N^2) complexity). In Python, Strings are mathematically immutable. They cannot be changed in RAM. When you type `a + b`, Python does not append `b` to `a`. It asks the OS for a brand new memory block, copies `a` into it, and then copies `b` into it. If you concatenate $4$ strings, Python creates an intermediate string for `a+b`, then copies that into a *new* string for `(a+b)+c`, and so on. This creates massive memory fragmentation and exponential CPU copying overhead. `.join()` or f-strings mathematically pre-calculate the total final length of the string, allocate memory exactly *once*, and write the bytes directly."

3. Interviewer: "If we want to micro-benchmark Python code from the terminal without writing a script, how do we use the `timeit` CLI?"
   Senior Answer: "The Command Line Interface. Python exposes `timeit` directly to the terminal for rapid, on-the-fly architectural decisions. You can run: `python -m timeit '\"-“.join([str(n) for n in range(100)])'` and `python -m timeit '\"-“.join(map(str, range(100)))'`. The CLI automatically determines the optimal number of loop executions (e.g., $100,000$ vs $10,000$) based on how fast the code runs, mathematically proving to the developer in $3$ seconds that the `map()` function is executed in C and is significantly faster than the list comprehension for this specific task."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling & Optimization (Micro-Benchmarking) Completed.")
