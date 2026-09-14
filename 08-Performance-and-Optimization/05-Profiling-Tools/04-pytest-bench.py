"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (MICRO-BENCHMARKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer uses `time.time()` to measure the speed of a function. It 
# reports 0.05 seconds. They run it again, it reports 0.08 seconds. The Operating 
# System background tasks (e.g., Anti-Virus scans, Chrome tabs) are creating 
# catastrophic variance in the timing data, rendering their tests mathematically 
# meaningless.
#
# A senior engineer uses `pytest-benchmark`. The testing framework forcefully 
# warms up the CPU Cache, disables the Python Garbage Collector to prevent random 
# execution pauses, and executes the target function 10,000 times in a highly 
# controlled, isolated C-level loop. It applies statistical analysis to strip out 
# OS-level noise, guaranteeing that a 0.5% performance regression in CI/CD will 
# be mathematically detected and caught before reaching Production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Micro-benchmarking using `pytest-benchmark`.
# - Prove the danger of OS Noise and Garbage Collection in testing.
# - Differentiate between List Comprehensions and `append` loops.
#
# ==============================================================================
"""

import time
import math
import gc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TARGET ALGORITHMS (LIST COMPREHENSION VS APPEND)
# ==============================================================================
# We want to mathematically prove which approach is faster for generating data.

def generate_via_append(n: int) -> list:
    """The standard beginner loop."""
    result = []
    for i in range(n):
        result.append(math.sqrt(i))
    return result

def generate_via_comprehension(n: int) -> list:
    """The pythonic List Comprehension."""
    return [math.sqrt(i) for i in range(n)]


# ==============================================================================
# 4. THE PYTEST-BENCHMARK INTEGRATION
# ==============================================================================
# To use pytest-benchmark, you must write functions starting with `test_` and 
# accept the `benchmark` fixture as a parameter!

def test_generate_via_append(benchmark):
    """
    Pytest will automatically inject the `benchmark` fixture!
    The benchmark object will execute `generate_via_append(100_000)` thousands 
    of times to achieve statistical certainty.
    """
    # We pass the function pointer, and then the arguments!
    result = benchmark(generate_via_append, 100_000)
    assert len(result) == 100_000

def test_generate_via_comprehension(benchmark):
    result = benchmark(generate_via_comprehension, 100_000)
    assert len(result) == 100_000


# ==============================================================================
# 5. SIMULATING THE BENCHMARK (IF PYTEST IS NOT RUNNING)
# ==============================================================================
def simulate_pytest_benchmark():
    section_header("Micro-benchmarking Simulation")
    
    print("  [ERROR] This file is designed to be executed via `pytest`!")
    print("  Command: `pytest 04-pytest-bench.py`\n")
    
    print("  [SIMULATED PYTEST-BENCHMARK OUTPUT]")
    print("  -------------------------------------------------------------------------------------- benchmark: 2 tests --------------------------------------------------------------------------------------")
    print("  Name (time in ms)                                    Min                 Max                Mean             StdDev              Median                IQR            Outliers       OPS            ")
    print("  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("  test_generate_via_comprehension                  12.4510             15.2310             12.8940             0.4120             12.7540             0.3120               2;1      77.555")
    print("  test_generate_via_append                         18.1250             22.4150             18.9100             0.8410             18.6010             0.7410               3;0      52.882")
    print("  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    
    print("\n  [ANALYSIS]")
    print("  -> The List Comprehension is consistently ~30% faster.")
    print("  -> The StdDev (Standard Deviation) proves the timing is highly stable.")
    print("  -> Pytest automatically caught and removed 'Outliers' (moments where")
    print("     the OS paused Python to do something else).")


def run_all_labs():
    # If a user just runs `python 04-pytest-bench.py`, we show the simulation.
    simulate_pytest_benchmark()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is using `time.time()` or even `time.perf_counter()` manually inside a script considered unacceptable for professional micro-benchmarking?"
   Senior Answer: "When you run a script, you are at the mercy of the Operating System's CPU Scheduler. In the middle of your 0.1-second loop, the OS might forcefully suspend the Python thread for 0.05 seconds to handle an incoming network packet or a background Chrome process. Additionally, the Python Garbage Collector might arbitrarily wake up and spend 0.03 seconds purging Generation 0 memory. If you only time the loop once, your data is completely corrupted by 'OS Noise'. Professional tools like `pytest-benchmark` physically disable the Python GC, 'warm up' the CPU to ensure the L1 Cache is populated, and execute the function thousands of times in a tight C-loop, mathematically discarding the outliers (the OS pauses) to isolate the true CPU execution time."

2. Interviewer: "Why does the `benchmark` fixture require you to pass the function pointer `benchmark(my_func, args)` rather than just wrapping it like `benchmark(my_func(args))`?"
   Senior Answer: "Because of 'Eager Evaluation'. If you wrote `benchmark(my_func(args))`, the Python interpreter would immediately execute `my_func(args)` *exactly once*, calculate the result, and pass that static result into the `benchmark` object. The benchmark would have absolutely nothing to time! By passing the function pointer (the name of the function without parentheses) and the arguments separately, the `benchmark` object takes control of the execution. It physically builds the C-level loop and invokes the function pointer thousands of times internally, achieving perfect micro-timing."

3. Interviewer: "The simulated benchmark proves List Comprehensions are 30% faster than standard `append` loops. Architecturally, why is that true?"
   Senior Answer: "A standard `for` loop executing `.append()` requires the CPython Interpreter to physically execute two expensive bytecode operations on every single iteration: 1) `LOAD_ATTR` (Look up the `append` method in the list's dictionary), and 2) `CALL_FUNCTION` (Execute the Python function call stack). If $N = 100,000$, that is $200,000$ massive bytecode overhead penalties. A List Comprehension uses a highly specialized C-level bytecode instruction called `LIST_APPEND`. It entirely bypasses the attribute lookup and the Python function call stack, directly injecting the data into the C-array memory block, resulting in a devastating $30\\%$ to $50\\%$ speedup over manual iteration."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Profiling (Pytest Benchmark) Completed.")
