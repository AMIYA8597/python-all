# Profiling Techniques in Python

Before optimizing your code, you must know what to optimize. A common pitfall for developers is "premature optimization"—guessing where the bottlenecks are and optimizing the wrong things. 

**Profiling** is the process of measuring the performance of an application (time complexity, memory usage, function call frequency) to identify the true bottlenecks.

This document covers the essential profiling tools available in the Python ecosystem.

## 1. Macro-Profiling: `timeit`

When you need to test small snippets of code to see which approach is faster, the `timeit` module is the gold standard.

### Why not just use `time.time()`?
Using `time.time()` can be inaccurate for very fast operations due to OS scheduling, background processes, and low timer resolution. `timeit` temporarily disables the garbage collector and runs the code snippet thousands or millions of times to get a statistically significant average.

### Code Example
```python
import timeit

# Testing list comprehension vs append
setup = "my_list = []"

stmt1 = "[x * 2 for x in range(1000)]"
stmt2 = """
for x in range(1000):
    my_list.append(x * 2)
"""

time1 = timeit.timeit(stmt=stmt1, number=10000)
time2 = timeit.timeit(stmt=stmt2, setup=setup, number=10000)

print(f"List Comprehension: {time1:.4f}s")
print(f"For Loop + Append:  {time2:.4f}s")
```
*Note: In Jupyter notebooks or IPython, you can use the magical `%timeit` command.*

## 2. Deterministic Profiling: `cProfile`

`cProfile` is a built-in module that provides a deterministic profiling of a Python program. It tracks every single function call, how many times it was called, and how long it took.

### Usage
You can run it from the command line on an entire script:
```bash
python -m cProfile -s cumtime my_script.py
```
*(The `-s cumtime` flag sorts the output by cumulative time, which is usually the most useful metric).*

### Understanding the Output
`cProfile` generates a table with the following columns:
- **ncalls**: Number of times the function was called.
- **tottime**: Total time spent *inside* this function (excluding time spent in sub-functions).
- **percall**: `tottime` divided by `ncalls`.
- **cumtime**: Cumulative time spent in this function *including* all sub-functions it called.
- **percall**: `cumtime` divided by `ncalls`.
- **filename:lineno(function)**: The location of the function.

### Limitations of cProfile
- **Overhead**: Because it intercepts every function call, it adds overhead, making the program run slower.
- **Blind spots**: It only profiles at the function level. If you have a single function with 500 lines of code, `cProfile` will tell you the function is slow, but not *which line* inside the function is the culprit.

## 3. Micro-Profiling: `line_profiler`

When `cProfile` identifies a slow function, you use `line_profiler` to see exactly which line inside that function is causing the slowdown.

### Installation
```bash
pip install line_profiler
```

### Usage
You must add the `@profile` decorator to the functions you want to inspect. (No need to import it, it is injected by the runner).

```python
# math_ops.py
@profile
def slow_function():
    total = 0
    for i in range(100000):
        total += i
    
    # This line is intentionally slow
    squares = [x**2 for x in range(10000)]
    return total
```

Run it via the command line:
```bash
kernprof -l -v math_ops.py
```

### Output
The output gives you line-by-line metrics: `Hits`, `Time`, `Per Hit`, `% Time`, and the `Line Contents`. You can instantly see that the list comprehension takes up the majority of the time.

## 4. Memory Profiling: `memory_profiler`

Performance isn't just about speed; it's also about memory usage. If your program uses too much RAM, the OS will start swapping to the hard drive, drastically killing performance.

### Installation
```bash
pip install memory_profiler
```

### Usage
Like `line_profiler`, add `@profile` to the function.
```python
# mem_test.py
@profile
def memory_heavy_task():
    a = [1] * (10 ** 6) # Allocates a large list
    b = [2] * (2 * 10 ** 7) # Allocates a much larger list
    del b # Frees the memory
    return a
```

Run it:
```bash
python -m memory_profiler mem_test.py
```

### Output
It shows the memory usage of the Python process at each line, and the increment/decrement in memory caused by that specific line.

## 5. Statistical Profiling: `Py-Spy`

Deterministic profilers (like `cProfile`) add significant overhead and require modifying how you run the code. In a production environment, this is often unacceptable.

**Py-Spy** is a sampling (statistical) profiler. Instead of intercepting every function call, it periodically "peeks" into the running Python process (e.g., 100 times a second) to see what the stack trace looks like.

### Advantages of Py-Spy
- **Zero Overhead**: It runs as a separate process and reads the memory of the Python process. It barely impacts the performance of your running app.
- **Production Ready**: You can attach it to an already running, live production server.
- **C-Extensions**: It can profile code running in C-extensions (like NumPy), whereas `cProfile` only sees Python functions.

### Installation
```bash
pip install py-spy
```

### Usage: Flame Graphs
Flame graphs are the best way to visualize sampling profiles.
```bash
# Attach to a running process by PID and generate a flame graph
py-spy record -o profile.svg --pid 12345
```
Open `profile.svg` in a web browser.
- The **x-axis** shows the percentage of time spent (wider bars = more time).
- The **y-axis** shows the call stack (functions calling functions).

## Summary Workflow
1. Use **`cProfile`** or **`Py-Spy`** to find the slow functions in your application.
2. Use **`line_profiler`** on those specific functions to find the exact slow lines of code.
3. If dealing with large datasets, use **`memory_profiler`** to detect memory leaks or inefficient allocations.
4. Once you write an optimization, use **`timeit`** to prove your new code is actually faster than the old code.
