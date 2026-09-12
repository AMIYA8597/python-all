"""
## A. Concept Name
Profiling and Debugging in Python

## B. One-Sentence Definition
Profiling measures where a program spends its time and memory, while debugging is the process of identifying and fixing flaws that cause incorrect behavior.

## C. Why Does This Exist?
To help developers transition from "it works" to "it works efficiently and correctly" by providing tools to pinpoint performance bottlenecks and logical errors without relying solely on print statements.

## D. Intuition
If your code is slow, you don't want to guess which part is slow—you want a stopwatch that times every function. If your code is broken, you don't want to guess the variable state—you want to freeze time and look around.

## E. Real-Life Analogy
Profiling is like a financial audit: it tells you exactly where you spend most of your money (time/memory). Debugging is like a mechanic diagnosing a car: pausing the engine (execution) to check the spark plugs (variables) to see why it won't start.

## F. Mental Model
- Profiling: A top-down map of function calls with attached execution times.
- Debugging: A freeze-frame controller (play, pause, step) for your code execution.

## G. Visual Explanation
```text
Profiling Output (cProfile):
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    0.050    0.050    0.050    0.050 main.py:10(slow_function)
     1    0.001    0.001    0.001    0.001 main.py:15(fast_function)

Debugger Flow (pdb):
[Line 10] -> Run to here -> *Pause* -> Inspect `x` -> Step to [Line 11]
```

## H. Formal Explanation
Profiling involves dynamic program analysis to measure space (memory) or time complexity, often using tools like `cProfile` (deterministic profiling) or `timeit`. Debugging involves interactive tracing using tools like `pdb`, allowing breakpoints (`breakpoint()`), stepping (`s`, `n`), and variable inspection.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
Writing a custom timing decorator provides a basic "from-scratch" profiler, wrapping a function and calculating `end_time - start_time`.

## K. Library / Production Implementation (if applicable)
Python provides `cProfile` and `pstats` for time profiling, `timeit` for micro-benchmarking, and `pdb` for interactive debugging. For memory, external tools like `memory_profiler` are used.

## L. Trace (walk through example)
1. Decorator `time_it` wraps `main_workload()`.
2. `main_workload()` calls `slow_function()`, taking ~0.03s.
3. It then calls `fast_function()`, taking ~0.005s.
4. `cProfile` tracks these calls and outputs cumulative times.
5. In `buggy_function()`, `pdb.set_trace()` (or `breakpoint()`) would pause execution right before a potential ZeroDivisionError.

## M. Complexity
- Profiling Overhead: `cProfile` adds a small overhead, slightly skewing absolute times but preserving relative bottlenecks.
- Time Complexity of profiling: O(N) where N is the number of function calls, as it tracks every call.

## N. Common Mistakes
- Leaving profiling or `breakpoint()` calls in production code.
- Profiling multi-threaded applications without realizing `cProfile` only tracks the main thread by default.
- Trying to optimize code before profiling it (premature optimization).

## O. Common Confusions
- Profiling vs. Benchmarking: Profiling finds *where* the code is slow. Benchmarking (like `timeit`) finds *how fast* a specific piece of code is.
- `cProfile` vs `profile`: `cProfile` is implemented in C and has much less overhead; `profile` is pure Python.

## P. When To Use
- Use profiling when an application is failing latency SLAs or feeling sluggish.
- Use `pdb` when `print()` debugging becomes too complex, or when state needs to be inspected interactively.

## Q. When NOT To Use
- Don't run profilers in production environments under heavy load due to the overhead.
- Don't use `pdb` for asynchronous code debugging without specialized tools (it can block the event loop).

## R. Trade-offs
- Granularity vs. Overhead: Higher granularity profiling (line-by-line vs function-by-function) introduces significantly more overhead.

## S. Debugging
- In `pdb`: Use `c` (continue), `n` (next line), `s` (step into function), `l` (list code), and `p <var>` (print variable).
- If your profiler shows `built-in method exec` taking all the time, you need to dig deeper into the actual Python function calls.

## T. Memory Hook (a short memorable principle)
"Profile before you optimize, breakpoint before you guess."

## U. Active Recall (questions before answers)
1. What built-in module provides deterministic C-based profiling? (cProfile)
2. How do you trigger the interactive debugger in Python 3.7+? (breakpoint())
3. Why shouldn't you use the pure Python `profile` module? (Too much overhead)

## V. Practice (exercises)
1. Write a script, run `cProfile` via the CLI (`python -m cProfile script.py`), and sort the output by cumulative time.
2. Place a `breakpoint()` in a loop, step through iterations, and modify a variable dynamically from the interactive console.

## W. Interview Question
"How would you profile a Python application, and what is the difference between Wall Time and CPU Time?"
*Answer*: Use `cProfile` to find the slowest functions. Wall time is real-world elapsed time (including I/O waits); CPU time is time the CPU actively spent processing the code.

## X. Project Connection
In large data processing pipelines, profiling identifies slow transformations, allowing developers to replace slow `for` loops with vectorized `numpy` operations, drastically reducing execution time.
"""

import cProfile
import pstats
import time
import io
from functools import wraps
from typing import Any, Callable


# --- J. From-Scratch Implementation (Timing Decorator) ---
def time_it(func: Callable) -> Callable:
    """A simple decorator to print the execution time of a function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"[Profiling] {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper


# --- K. Library / Production Implementation (Using cProfile) ---
def slow_function() -> None:
    """A function that simulates some slow CPU-bound work."""
    total = 0
    for i in range(1000000):
        total += i

def fast_function() -> None:
    """A function that performs work quickly using built-ins."""
    total = sum(range(1000000))

@time_it
def main_workload() -> None:
    """A function calling both fast and slow functions to be profiled."""
    slow_function()
    fast_function()

def profile_code() -> None:
    """Runs cProfile on the main_workload and prints statistics."""
    print("--- Running cProfile ---")
    pr = cProfile.Profile()
    pr.enable()
    
    main_workload()
    
    pr.disable()
    s = io.StringIO()
    # Sort by cumulative time
    ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats(10)  # Print top 10 lines
    print(s.getvalue())


# --- Debugging (Programmatic pdb) ---
def buggy_function(divisor: int) -> int:
    """A function with a potential bug, demonstrating pdb usage."""
    result = 0
    data = [10, 20, 30]
    for val in data:
        # If divisor is 0, this will raise a ZeroDivisionError.
        # Uncomment the line below to trigger the debugger interactively:
        # breakpoint()                 # Python 3.7+
        
        try:
            result += val // divisor
        except ZeroDivisionError:
            print("[Debugger Note] Caught ZeroDivisionError. Divisor is 0.")
            return -1
    return result


# --- W. Interview Question Implementation ---
class ProfileContext:
    """
    Context manager that profiles any block of code inside it 
    and prints the top 3 functions by execution time.
    """
    def __enter__(self) -> "ProfileContext":
        self.pr = cProfile.Profile()
        self.pr.enable()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats(pstats.SortKey.TIME)
        ps.print_stats(3)
        print("--- Context Manager Profiling ---")
        print(s.getvalue())


# --- Tests ---
def run_tests() -> None:
    print("Testing Profiling and Debugging...")

    # Test time_it decorator and cProfile
    profile_code()

    # Test buggy function (without triggering interactive debugger)
    assert buggy_function(2) == 30  # 5 + 10 + 15
    assert buggy_function(0) == -1  # Handles ZeroDivisionError

    # Test ProfileContext challenge
    with ProfileContext():
        sum(i * i for i in range(100000))

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
