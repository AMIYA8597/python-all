import os

target_file = r"d:\work\python-all\12-Resources-References\03-Tools-Env\03-debug-tools.md"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

markdown_parts = []

part_1 = """# Advanced Python Debugging, Profiling, and Logging

## 1. Introduction & Overview

In the lifecycle of a software project, writing code is only the first phase. The true test of a developer's mettle, and indeed the robustness of a system, lies in maintaining, optimizing, and debugging the application when it meets the real world. Python, being a dynamic and interpreted language, presents unique challenges and opportunities in this space. Without the rigid compile-time checks of languages like C++ or Java, runtime behavior in Python can sometimes surprise even seasoned developers.

However, the Python ecosystem is rich with powerful, sophisticated tools designed to give you deep visibility into your application's state, performance, and memory consumption. This comprehensive guide serves as a textbook-depth reference to the advanced tools and techniques necessary for production-grade Python development. We will move beyond the ubiquitous `print()` statement and basic `logging` module to explore tools that provide granular control and insight.

The guide is divided into four main pillars:
1. **Advanced Debugging Tools**: Stepping through code interactively using `pdb`, its IPython-enhanced sibling `ipdb`, and the visual console debugger `pudb`.
2. **Memory Profilers**: Diagnosing memory leaks and understanding memory footprints using the built-in `tracemalloc`, the line-by-line `memory_profiler`, and the object-level `guppy3`.
3. **Performance Profilers**: Identifying bottlenecks with the deterministic `cProfile`, the granular `line_profiler`, and the low-overhead sampling profiler `py-spy`.
4. **Logging Strategies**: Transitioning from unstructured logs to structured, machine-readable logs with `structlog`, and integrating with centralized observability platforms like the ELK (Elasticsearch, Logstash, Kibana) stack.

By mastering these tools, you will transform from a developer who reacts to bugs into an engineer who proactively shapes performant, resilient, and observable systems. Let us delve into the depths of Python diagnostics.

---
"""
markdown_parts.append(part_1)

part_2 = """## 2. Advanced Debugging Tools

When a program behaves unexpectedly, the first instinct of many developers is to insert `print()` statements. While this can work for trivial scripts, it fails completely for complex systems, asynchronous code, or deeply nested logic. A proper debugger allows you to pause execution, inspect variables, evaluate expressions, and step through the code dynamically.

### 2.1. `pdb` (The Python Debugger)

`pdb` is the standard interactive debugger included in Python's standard library. It provides a command-line interface to pause execution and inspect the environment. Since Python 3.7, invoking the debugger has become as simple as inserting the `breakpoint()` built-in function.

#### Core Concepts and Commands
When execution hits `breakpoint()`, your terminal drops into the `(Pdb)` prompt. From here, a specialized command language is available:
*   **`l(ist)`**: Shows the source code around the current line. By default, it lists 11 lines.
*   **`ll` (long list)**: Lists the source code for the current function or frame entirely.
*   **`n(ext)`**: Executes the current line and steps to the next line in the current function. It steps *over* function calls.
*   **`s(tep)`**: Steps *into* the function called on the current line, allowing you to debug its internals.
*   **`c(ontinue)`**: Resumes execution until the next breakpoint is hit or the program finishes.
*   **`r(eturn)`**: Continues execution until the current function returns.
*   **`p(rint) <expression>`**: Evaluates and prints the value of a given expression in the current context.
*   **`pp <expression>`**: Pretty-prints the value (useful for large dictionaries or lists).
*   **`w(here)`**: Prints a stack trace, with the most recent frame at the bottom.
*   **`u(p)` / `d(own)`**: Move up and down the call stack, allowing you to inspect local variables in calling functions.
*   **`b(reak) [file:]lineno`**: Sets a new breakpoint dynamically.
*   **`q(uit)`**: Aborts the program and exits the debugger.

#### Advanced `pdb` Techniques
You can set conditional breakpoints dynamically. For example, `b 45, x > 10` sets a breakpoint at line 45 that only triggers if `x` is greater than 10. You can also run a script under `pdb` from the command line: `python -m pdb my_script.py`. This is extremely useful for post-mortem debugging when a script crashes; running it this way allows you to inspect the state at the exact moment of the crash.

### 2.2. `ipdb` (IPython Debugger)

While `pdb` is powerful, its interface is austere. `ipdb` integrates `pdb` with the rich interactive features of IPython. 

#### Why Choose `ipdb`?
1.  **Syntax Highlighting**: `ipdb` colorizes your source code, making it dramatically easier to read in the terminal.
2.  **Tab Completion**: Just like in IPython, you can press `<Tab>` to autocomplete variable names, attributes, and methods. This is an immense time-saver.
3.  **Better Tracebacks**: Stack traces are formatted more cleanly and provide more context.
4.  **Magic Commands**: You can use IPython "magic" commands within the debug session (e.g., `%timeit` to quickly profile a snippet).

#### Usage
Install via `pip install ipdb`. You can invoke it programmatically:
```python
import ipdb
ipdb.set_trace()
```
Or use it as an alternative to `pdb` from the command line: `python -m ipdb my_script.py`. Furthermore, setting the environment variable `PYTHONBREAKPOINT=ipdb.set_trace` will make the built-in `breakpoint()` function trigger `ipdb` instead of `pdb`.

### 2.3. `pudb` (Console-based Visual Debugger)

For developers who long for the graphical debuggers of IDEs (like PyCharm or VSCode) but are constrained to a terminal (e.g., SSHing into a remote server), `pudb` is a revelation. It is a full-screen, console-based visual debugger for Python.

#### Interface and Features
`pudb` divides the terminal into multiple panes:
*   **Code View**: The largest pane displays your source code with syntax highlighting and a clear marker indicating the current execution line. Breakpoints are visually marked.
*   **Variables View**: A dedicated pane showing all local and global variables. You can expand complex objects (like dictionaries, lists, or custom classes) to inspect their contents dynamically.
*   **Stack View**: Displays the current call stack. You can visually navigate up and down the stack to change the context.
*   **Breakpoints View**: A list of all active breakpoints, which can be toggled on and off.
*   **Command Line**: A prompt at the bottom where you can execute Python commands in the current context.

#### Workflow
Install via `pip install pudb`. You invoke it in your code using:
```python
import pudb
pudb.set_trace()
```
Or run your script with it: `pudb my_script.py`. Navigation is heavily keyboard-oriented (arrow keys, `n`, `s`, `c`, `b`), making it incredibly fast for developers who prefer staying on the keyboard. It bridges the gap between the power of an IDE and the accessibility of a terminal.

---
"""
markdown_parts.append(part_2)

part_3 = """## 3. Memory Profilers

Memory management in Python is abstracted away by reference counting and a cyclic garbage collector. While this simplifies development, it makes diagnosing memory issues—such as leaks or excessive memory footprints—notoriously difficult. A memory leak in a long-running process (like a web server or a background worker) can eventually exhaust system resources, leading to out-of-memory (OOM) kills.

### 3.1. `tracemalloc`

`tracemalloc` is a built-in module (since Python 3.4) that traces memory blocks allocated by Python. It provides the exact filename and line number where the memory was allocated. It is the most robust tool for answering the question: "Where is my memory going?"

#### Usage and Analysis
To use `tracemalloc`, you must start tracing early in your program's lifecycle.
```python
import tracemalloc

# Start tracing, storing 10 frames of traceback
tracemalloc.start(10)

def allocate_memory():
    # Simulate a memory leak
    return [x for x in range(1000000)]

data = allocate_memory()

# Take a snapshot of current memory allocations
snapshot = tracemalloc.take_snapshot()

# Display the top 5 memory-consuming lines
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:5]:
    print(stat)
```

The true power of `tracemalloc` comes from comparing snapshots over time. By taking a snapshot, running some code (like processing a web request), and taking another snapshot, you can calculate the difference. If memory grows persistently between snapshots without being garbage collected, you have found a leak.

### 3.2. `memory_profiler`

While `tracemalloc` is great for finding the source of allocations, `memory_profiler` provides a high-level, line-by-line breakdown of a function's memory consumption. It is ideal for understanding the memory profile of a specific algorithm or data processing pipeline.

#### Decorator-based Profiling
Install via `pip install memory_profiler`. You use it by decorating the function you want to profile with `@profile`.

```python
from memory_profiler import profile

@profile
def process_large_data():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    process_large_data()
```

Run the script normally (or via `mprof run script.py`). The output will be a table showing:
*   **Line #**: The line number.
*   **Mem usage**: The total memory usage of the Python interpreter after executing the line.
*   **Increment**: The amount of memory added (or released) by that specific line.
*   **Line Contents**: The source code of the line.

This increment column is invaluable. It quickly highlights statements that instantiate massive data structures. You can also use `mprof plot` to generate a graph of memory usage over time, visually correlating spikes with function executions.

### 3.3. `guppy3` (Heapy)

When you know you have a memory bloat but need to know *what* objects are consuming the memory, `guppy3` (specifically its `heapy` component) is the tool of choice. It analyzes the Python heap and categorizes objects by type, providing a statistical overview of the memory landscape.

#### Inspecting the Heap
Install via `pip install guppy3`. It is most often used interactively or by dropping a trace in the code.

```python
from guppy import hpy

def create_objects():
    hp = hpy()
    # Take a baseline heap snapshot
    hp.setrelheap() 
    
    # Create objects
    leaky_list = [dict(a=i, b=i*2) for i in range(100000)]
    
    # Check the heap relative to the baseline
    print(hp.heap())

create_objects()
```

The output of `hp.heap()` is a tabular summary showing the count and total size of objects, grouped by type (e.g., `dict`, `list`, `str`, `tuple`). If you notice that you have 5 million string objects consuming 80% of your heap, you can use `heapy`'s path-to-root tools to figure out which structures are holding references to those strings, preventing garbage collection.

---
"""
markdown_parts.append(part_3)


part_4 = """## 4. Performance Profilers

When a Python application is too slow, guessing the bottleneck is almost always wrong. Human intuition about execution time is poor, especially with complex libraries and frameworks. Performance profilers provide empirical data on where the CPU is spending its time.

### 4.1. `cProfile` & `pstats`

`cProfile` is the recommended built-in profiler. It is deterministic, meaning it tracks every single function call, return, and exception, calculating precise timings. Because it is implemented in C, its overhead is relatively low compared to the older `profile` module.

#### Standard Profiling Workflow
The easiest way to profile a script is from the command line:
`python -m cProfile -o output.prof my_script.py`

This generates a binary file `output.prof`. Reading this directly is impossible, which is where the `pstats` module comes in. You can write a small script or use the interactive `pstats` browser to analyze it:

```python
import pstats
from pstats import SortKey

p = pstats.Stats('output.prof')
# Sort by cumulative time spent in a function and its sub-functions
p.sort_stats(SortKey.CUMULATIVE).print_stats(20)
# Sort by total time spent strictly within the function itself
p.sort_stats(SortKey.TIME).print_stats(20)
```

**Key Metrics:**
*   **ncalls**: The number of times the function was called.
*   **tottime**: Total time spent in the function itself (excluding calls to sub-functions). High `tottime` means the function itself is computationally heavy.
*   **cumtime**: Cumulative time spent in the function *and* all sub-functions it called. High `cumtime` means the function is a major entry point for heavy work.

Tools like `snakeviz` or `tuna` can visualize `cProfile` outputs as interactive icicle graphs or sunburst charts, making it instantly obvious which call stacks dominate execution time.

### 4.2. `line_profiler`

`cProfile` is excellent for finding the *function* that is slow, but what if the function is 200 lines long? Knowing the function is slow doesn't help you fix it. `line_profiler` tells you exactly how much time was spent on each individual line of code.

#### Line-by-Line Analysis
Install via `pip install line_profiler`. Like `memory_profiler`, it uses a `@profile` decorator (which is injected into the built-ins by the `kernprof` script).

```python
# No import needed for @profile when running via kernprof
@profile
def slow_function():
    total = 0
    for i in range(10000):
        total += sum([j for j in range(100)]) # Inefficient line
    return total
```

Run it using the `kernprof` utility: `kernprof -l -v my_script.py`. 
The output will display:
*   **Line #**: Line number.
*   **Hits**: How many times the line was executed.
*   **Time**: Total time spent executing that line across all hits.
*   **Per Hit**: Average time per execution.
*   **% Time**: Percentage of the function's total time spent on this line.

This granular view is crucial for micro-optimizations, such as noticing that a list comprehension is slower than a generator, or that a database query inside a loop is consuming 90% of the function's execution time.

### 4.3. `py-spy`

Deterministic profilers like `cProfile` and `line_profiler` add overhead. For highly performance-sensitive applications, this overhead might skew the results or be unacceptable for profiling in a production environment. `py-spy` is a sampling profiler for Python programs. It reads the memory of the Python process from the outside (like a system debugger) without modifying the code or running inside the interpreter.

#### Low-Overhead Production Profiling
Install via `pip install py-spy`. Because it runs out-of-process, it requires elevated privileges (e.g., `sudo` on Linux).

You can attach it to a running process using its PID:
`sudo py-spy top --pid 12345`

This opens a `top`-like interface showing the most active functions in real-time. It doesn't pause the program, making it safe for production use.

`py-spy` can also generate flame graphs directly:
`sudo py-spy record -o profile.svg --pid 12345`

A flame graph is a powerful visualization where the x-axis represents the population of the profile (time spent), and the y-axis represents the call stack. Wide blocks indicate functions where a lot of time is spent. It is the ultimate tool for quickly identifying bottlenecks in live, production systems without deploying new profiling code.

---
"""
markdown_parts.append(part_4)


part_5 = """## 5. Logging Strategies

Logging is the bedrock of observability. While debugging tools are interactive and profilers are diagnostic, logs are the historical record of your application's behavior. A robust logging strategy is non-negotiable for distributed systems, microservices, or any application deployed to production.

### 5.1. Standard Logging vs. Structured Logging

The standard Python `logging` module outputs unstructured text. A log line might look like this:
`2023-10-27 10:00:01 - WARNING - user_service - User login failed for user john_doe from IP 192.168.1.5`

While readable by humans, this is a nightmare for machines. If you want to search your logs for all failed logins from a specific IP subnet, you must write complex Regular Expressions to parse the text. 

**Structured Logging** solves this by emitting logs as machine-readable data structures, typically JSON. The equivalent structured log would be:
```json
{
  "timestamp": "2023-10-27T10:00:01Z",
  "level": "warning",
  "logger": "user_service",
  "event": "user_login_failed",
  "username": "john_doe",
  "ip_address": "192.168.1.5"
}
```
Now, querying is trivial. You can filter by `level="warning"` and `event="user_login_failed"`.

### 5.2. `structlog`

`structlog` is the premier library for structured logging in Python. It acts as a wrapper around the standard library or other logging frameworks, providing a powerful pipeline for enriching logs with context.

#### Building Contextual Logs
Install via `pip install structlog`. Instead of formatting strings, you pass key-value pairs to the logger.

```python
import structlog

# Basic configuration to output JSON
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()

def process_checkout(user_id, cart_id):
    # Bind context to the logger for this specific execution path
    bound_log = log.bind(user_id=user_id, cart_id=cart_id)
    
    bound_log.info("checkout_started")
    try:
        # Simulate processing
        if not charge_card():
            raise PaymentError("Insufficient funds")
        bound_log.info("checkout_completed", status="success")
    except Exception as e:
        # Context (user_id, cart_id) is automatically included in the error log
        bound_log.error("checkout_failed", error=str(e))
```

The power of `bind()` is immense. If an error occurs deep in the call stack, the log will contain the `user_id` and `cart_id` bound at the top level, providing critical context without needing to pass those variables through every function signature.

### 5.3. ELK Stack Integration Basics

Structured logs are only useful if they are collected and indexed. The ELK stack (Elasticsearch, Logstash, Kibana) is a standard architecture for log aggregation.

1.  **Elasticsearch**: A distributed search and analytics engine. It stores your JSON logs and indexes every field, allowing for lightning-fast queries (e.g., "Find all errors where `user_id` is 42").
2.  **Logstash** (or Filebeat/Fluentd): The data processing pipeline. It tails your log files or receives logs over a network, parses them (if necessary), and ships them to Elasticsearch. When using `structlog` to emit JSON, Logstash's job is trivial as the data is already structured.
3.  **Kibana**: The visualization dashboard. It sits on top of Elasticsearch and allows you to create charts, dashboards, and complex queries. 

#### Python Integration Strategy
In a production deployment, it is an anti-pattern for your Python application to send logs directly to Elasticsearch via HTTP. This couples your application performance to the logging infrastructure's latency and availability.

Instead, the standard pattern is:
1.  Python application uses `structlog` to write JSON logs to standard output (stdout) or a local file.
2.  A lightweight agent like Filebeat (part of the Elastic ecosystem) or Fluent Bit runs on the same server/container.
3.  The agent tails the local log file, batches the logs, and asynchronously ships them to Logstash or directly to Elasticsearch.

This decoupled architecture ensures that if the ELK stack goes down, your Python application continues running, and logs are buffered locally until the connection is restored. Once in Kibana, developers can build dashboards tracking API latency (parsed from logs), error rates per endpoint, and user activity flows, turning logs from a debugging tool into a business intelligence asset.

---
"""
markdown_parts.append(part_5)


part_6 = """## 6. Conclusion & Best Practices

Mastering these advanced tools separates novice developers from senior engineers capable of maintaining critical infrastructure. As a final synthesis, consider these best practices:

1.  **Shift Left with Profiling**: Do not wait for production users to complain about latency. Integrate `cProfile` and `memory_profiler` into your CI/CD pipeline or run them periodically during development. Performance regressions should be caught like unit test failures.
2.  **Log with Intent**: Every log message should have a purpose. Ask yourself: "If this log fires at 3 AM, will it help me solve the problem?" Avoid verbose, context-less logging. Embrace `structlog` and bind context (Trace IDs, User IDs) as early as possible in a request's lifecycle.
3.  **Know Your Tools' Limits**: `tracemalloc` will find your leak, but it will slow down your program significantly. `py-spy` is fast, but it's a sampler, not a deterministic profiler. Choose the tool that matches the environment (development vs. production) and the specific diagnostic need.
4.  **Embrace the Debugger**: When faced with a complex logic error, resist the urge to litter the code with `print()`. Drop an `ipdb.set_trace()` or use `pudb` to explore the state interactively. The time invested in learning debugger commands pays exponential dividends in debugging speed.

Python's dynamic nature is its greatest strength, enabling rapid development. By integrating advanced debugging, memory profiling, performance tracing, and structured logging into your workflow, you build a safety net that ensures that rapid development does not come at the cost of stability or performance.
"""
markdown_parts.append(part_6)


# Write everything to the file
with open(target_file, "w", encoding="utf-8") as f:
    for part in markdown_parts:
        f.write(part)

print(f"Successfully generated 03-debug-tools.md at {target_file}")
