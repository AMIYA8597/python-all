# Comprehensive Guide to Debugging & Profiling Tools in Python

Writing code is only half the battle; fixing and optimizing it is the other half. This guide covers professional debugging techniques, moving beyond simple `print()` statements to advanced interactive debuggers and performance profilers.

## 1. Introduction: The Art of Debugging

Debugging is the process of identifying and removing errors (bugs) from hardware or software. Profiling is the process of analyzing the program's execution to determine bottlenecks (CPU time, memory usage).

### Industry Use Cases
- **Production Incident Response**: Using stack traces and logging to identify why a live service crashed.
- **Performance Optimization**: Using profilers to reduce an API endpoint's response time from 2 seconds to 50 milliseconds.
- **Memory Leaks**: Using `tracemalloc` to find why a long-running background worker is slowly consuming all system RAM.

---

## 2. Debugging Tools

### 2.1 The Built-in Debugger: `pdb`
Python comes with a built-in interactive debugger called `pdb`.

**Basic Usage:**
In Python 3.7+, you can invoke the debugger anywhere in your code using the `breakpoint()` function.

```python
def calculate_discount(price, discount_rate):
    discount = price * discount_rate
    breakpoint()  # Execution pauses here, dropping you into the pdb REPL
    return price - discount

calculate_discount(100, 0.2)
```

**Common `pdb` Commands:**
- `l` (list): Shows the code around the current line.
- `n` (next): Executes the current line and goes to the next one.
- `s` (step): Steps *into* a function call.
- `c` (continue): Continues execution until the next breakpoint.
- `p <var>` (print): Evaluates and prints the value of an expression/variable.
- `q` (quit): Aborts the program.

> **Pro Tip**: Use `ipdb` (IPython PDB) for a much better experience with syntax highlighting and tab completion. (`pip install ipdb`, then `import ipdb; ipdb.set_trace()`).

### 2.2 IDE Graphical Debuggers
VS Code and PyCharm both have excellent visual debuggers.
1. Click to the left of the line numbers to set a red "Breakpoint".
2. Run the code in "Debug Mode" (F5 in VS Code).
3. The IDE will pause execution and provide panels for Variables, Watch expressions, and the Call Stack.

### 2.3 PySnooper (The "Print on Steroids")
When you cannot use an interactive debugger (e.g., in a complex loop or remote server), `PySnooper` logs execution lines and variable changes automatically.

```python
# pip install pysnooper
import pysnooper

@pysnooper.snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)
```
*Output will trace every line executed and every variable changed.*

---

## 3. Logging vs. Print

Never use `print()` for production code. Use the built-in `logging` module.

### Why Logging?
- Granular levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Output destinations: Console, files, remote logging servers (Datadog, Splunk).
- Metadata: Automatically include timestamps, file names, and line numbers.

**Example:**
```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.debug("Detailed diagnostic info")
logging.info("General operational events")
logging.warning("Something unexpected happened, but we recovered")
logging.error("Failed to process a transaction")
try:
    1 / 0
except ZeroDivisionError:
    logging.exception("Fatal error occurred") # Automatically includes the full traceback!
```

---

## 4. Profiling: Finding Bottlenecks

### 4.1 cProfile (CPU Profiling)
`cProfile` is a built-in C extension that measures where your program spends its time.

**Running from terminal:**
```bash
python -m cProfile -s time my_script.py
```
*(Sorts the output by the time spent in each function).*

### 4.2 line_profiler (Line-by-Line Time)
`cProfile` tells you *which function* is slow. `line_profiler` tells you *which line* inside the function is slow.

```python
# pip install line_profiler
# Usage: Add @profile decorator (no import needed if running via kernprof)

@profile
def slow_function():
    # ... code ...
```
Run with: `kernprof -l -v slow_function.py`

### 4.3 Memory Profiling
To find memory leaks, use the built-in `tracemalloc` library.

```python
import tracemalloc

tracemalloc.start()

# ... run your memory intensive code ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:5]:
    print(stat)
```

---

## 5. Security and Performance Considerations

- **Security**: Never leave `breakpoint()` or development debugging tools active in production. It pauses the thread and could lead to denial of service, or expose interactive shells to attackers.
- **Performance**: Profiling adds overhead. Do not run `cProfile` or `line_profiler` continuously in production. Use APM (Application Performance Monitoring) tools like New Relic or Datadog for production monitoring via sampling.
- **Logging**: Be careful not to log sensitive data (PII, passwords, API keys). Sanitize logs before emitting them.

---

## 6. Interview Questions & Exercises

### Interview Questions
1. **When would you use `logging` instead of `print()`?**
   *Answer*: Always in production. `print` is synchronous, unformatted, and cannot be easily filtered or redirected to files/monitoring systems. `logging` supports severity levels, rich formatting, thread-safety, and multiple output handlers.
2. **You have a Python script that uses too much memory and gets OOMKilled by Docker. How do you find the leak?**
   *Answer*: I would use the built-in `tracemalloc` module to take memory snapshots before and after the suspected operations, and compare the snapshots to see which line of code is allocating memory that isn't being freed.

### Practical Exercise
1. Write a script containing a function that calculates the Fibonacci sequence poorly (e.g., naive recursion).
2. Use `cProfile` to profile the script and observe the massive number of function calls.
3. Optimize the function using memoization (`functools.lru_cache`).
4. Profile it again and compare the performance difference.
5. Add a `breakpoint()` in the optimized code and step through it using `pdb` to watch the cache hits.
