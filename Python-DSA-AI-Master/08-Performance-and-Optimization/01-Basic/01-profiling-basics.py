"""
## A. Concept Name
Profiling Basics

## B. Motivation
Optimization without profiling is just guessing. Profiling allows developers to measure exactly where time and memory are being spent.

## C. Key Components
- `cProfile`: Built-in C extension for deterministic profiling.
- `timeit`: Module for timing small code snippets.
- `pstats`: Module for formatting and sorting profile data.

## D. Best Practices
- Measure before optimizing.
- Profile in an environment as close to production as possible.
- Focus on the bottlenecks (the 20% of code causing 80% of delay).

## E. Real-world Examples
- Identifying a slow database query.
- Finding an inefficient sorting algorithm (e.g., O(N^2) instead of O(N log N)).

## X. Project Connection
In large-scale AI and DSA projects, data preprocessing and matrix operations can be extremely slow if implemented naively. By utilizing profiling, you can systematically uncover bottlenecks and apply the correct optimizations to accelerate training and inference.
"""

import cProfile
import pstats
import timeit
import time

def slow_function():
    """A sample slow function simulating heavy computation."""
    total = 0
    for i in range(1000000):
        total += i
    return total

def fast_function():
    """A sample fast function using math instead of a loop."""
    n = 999999
    return n * (n + 1) // 2

def main():
    print("--- Using timeit ---")
    slow_time = timeit.timeit(slow_function, number=10)
    fast_time = timeit.timeit(fast_function, number=10)
    print(f"Slow function took: {slow_time:.5f} seconds (10 runs)")
    print(f"Fast function took: {fast_time:.5f} seconds (10 runs)")
    
    print("\n--- Using cProfile ---")
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run functions
    for _ in range(5):
        slow_function()
        fast_function()
    
    profiler.disable()
    
    print("\n--- Profiling Stats ---")
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(10)

if __name__ == "__main__":
    main()
