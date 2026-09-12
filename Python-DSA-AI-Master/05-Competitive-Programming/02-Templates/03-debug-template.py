"""
=========================================================================================
Competitive Programming Debug Template: A Comprehensive Guide
=========================================================================================

## A. Concept Name
Advanced Competitive Programming Debugging and Profiling Framework

## B. Description
In the fast-paced world of Competitive Programming (CP), debugging effectively can be the
difference between a Gold medal and failing to qualify. Standard `print()` statements 
often lead to "Wrong Answer" (WA) or "Output Limit Exceeded" (OLE) verdicts because they 
pollute the standard output (`stdout`) which is checked by the Online Judge (OJ).

This module provides a robust, textbook-grade debugging template for Python. It offers:
1. Environment-aware debugging (automatically disables itself on the server).
2. Advanced introspection using the `inspect` and `ast` modules to automatically print
   variable names alongside their values, mimicking C++'s `#define debug(x)` macro.
3. Formatted data structure visualization (1D arrays, 2D matrices, Trees, and Graphs).
4. Time and space profiling decorators for bottleneck identification.
5. Zero-overhead execution when deployed on the Online Judge.

## C. Learning Objectives
By studying this module, you will learn:
1. Stream Redirection: How to separate program output (`stdout`) from debug info (`stderr`).
2. Metaprogramming & Introspection: Using Python's `inspect` and `ast` modules to 
   analyze the call stack and extract variable names at runtime.
3. ANSI Escape Codes: How to use terminal color codes for readable logging.
4. Performance Tuning: Implementing decorators to measure function execution time and 
   call frequency.
5. Defensive Programming: Ensuring that heavy debug operations do not execute or incur
   overhead when running in a production (or Online Judge) environment.

## D. Concept Explanation
In languages with a preprocessor (like C/C++), competitors use macros to conditionally 
compile debug statements. Python lacks a preprocessor, so we must rely on runtime 
evaluation. However, function calls and conditional checks (even `if False:`) take time. 
To mitigate this, we determine the environment (Local vs. OJ) at module load time.

### The Introspection Magic
A common pain point in Python is writing `print(f"x = {x}")`. We want a function `dbg(x, y)` 
that automatically outputs `x = 10, y = 20`. 
To achieve this:
1. `inspect.currentframe().f_back` gives us the caller's frame.
2. `inspect.getframeinfo` gives us the filename and line number.
3. We read the source code file at that line number.
4. We parse the source line using Python's Abstract Syntax Tree (`ast` module) to extract 
   the exact argument names passed to the `dbg()` function.

## E. Mathematical & Complexity Analysis
- Space Complexity (Introspection): O(L) where L is the length of the source line, as we 
  parse a small string into an AST.
- Time Complexity (Introspection): O(L + V) where V is the number of variables printed.
  AST parsing takes negligible time for a single line, but doing this inside a tight loop 
  (e.g., 10^5 iterations) will cause massive overhead.
- Overhead in OJ: O(1) (practically 0). We simply map our debug functions to `lambda *args, 
  **kwargs: None` or use short-circuit evaluation.

## F. Use Cases
- DP State Tracking: Tracing memoization tables.
- Graph Algorithms: Visualizing adjacency lists and shortest-path distances.
- Ad-Hoc Problems: Quickly checking loop invariants.
- Optimization: Profiling which recursive branch is taking too long.

## G. Project Connection
This template is the bedrock of a robust Python CP setup. It allows you to write complex 
logic with the confidence that you can inspect any state effortlessly.

=========================================================================================
"""

import sys
import os
import time
import inspect
import ast
import functools
import collections
from typing import Any, Iterable, List, Dict, Optional, Callable, Set, Tuple

# =========================================================================================
# 1. Environment Detection Setup
# =========================================================================================
# Typically, online judges do not have a specific file you can create locally,
# or they define specific environment variables (like "ONLINE_JUDGE").
# We define `LOCAL_RUN` as True if a custom flag is present or a local file exists.
LOCAL_RUN: bool = (
    os.path.exists("local.txt") or 
    os.environ.get("LOCAL_CP_DEBUG", "0") == "1" or
    "VSCODE_PID" in os.environ or 
    "TERM_PROGRAM" in os.environ
)

# =========================================================================================
# 2. Terminal Colors & Formatting
# =========================================================================================
class TerminalColors:
    """
    ANSI escape sequences for terminal output styling.
    Ensures that debug output is visually distinct from normal output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# =========================================================================================
# 3. Core Introspection Debugging (The `dbg` function)
# =========================================================================================
def _get_caller_args_names(depth: int = 2) -> List[str]:
    """
    Analyzes the call stack to find the exact variable names passed to the debug function.
    
    Args:
        depth: The frame depth to look at. 2 means the caller of the function that called this.
               
    Returns:
        A list of strings representing the names of the arguments.
    """
    try:
        # Get the caller's frame
        frame = inspect.currentframe()
        for _ in range(depth):
            if frame is not None:
                frame = frame.f_back
        
        if frame is None:
            return []

        # Get the source code of the caller's frame
        frame_info = inspect.getframeinfo(frame)
        code_context = frame_info.code_context
        
        if not code_context:
            return []
            
        source_line = "".join(code_context).strip()
        
        # We need to extract the arguments from something like `dbg(x, y, z)`
        # Using AST to parse the function call
        # Wrapping in a dummy expression if it's incomplete or multi-line might be needed,
        # but for standard single-line `dbg(a, b)` this works perfectly.
        tree = ast.parse(source_line)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Check if the function being called is one of our debug functions
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                # We assume the first Call node matching our criteria is the right one
                # Extract argument representations
                arg_names = []
                for arg in node.args:
                    # Unparse reconstructs the string from the AST node (Python 3.9+)
                    if hasattr(ast, 'unparse'):
                        arg_names.append(ast.unparse(arg))
                    else:
                        # Fallback for older Pythons
                        if isinstance(arg, ast.Name):
                            arg_names.append(arg.id)
                        else:
                            arg_names.append(f"<expr:{type(arg).__name__}>")
                return arg_names
    except Exception as e:
        # Silently fail and return empty names if AST parsing fails 
        # (e.g., due to multiline function calls)
        pass
    
    return []

def debug_impl(*args: Any, **kwargs: Any) -> None:
    """
    The actual implementation of the advanced debug function.
    Prints the file name, line number, variable names, and their values.
    """
    # Get frame info for file and line number
    frame = inspect.currentframe()
    if frame is not None and frame.f_back is not None:
        back_frame = frame.f_back
        frame_info = inspect.getframeinfo(back_frame)
        filename = os.path.basename(frame_info.filename)
        lineno = frame_info.lineno
    else:
        filename = "unknown"
        lineno = 0

    arg_names = _get_caller_args_names(depth=2)
    
    # Pad arg_names if AST parsing failed
    while len(arg_names) < len(args):
        arg_names.append("?")
        
    # Format the output
    prefix = f"{TerminalColors.WARNING}[{filename}:{lineno}]{TerminalColors.ENDC}"
    
    output_parts = []
    for name, val in zip(arg_names, args):
        # Format the value nicely based on its type
        if isinstance(val, (list, tuple, set, dict)) and len(val) > 10:
            # Truncate large collections
            type_name = type(val).__name__
            val_str = str(val)
            if len(val_str) > 100:
                val_str = val_str[:97] + "..."
            formatted_val = f"{TerminalColors.OKCYAN}{type_name}(size={len(val)}){TerminalColors.ENDC} {val_str}"
        elif isinstance(val, str):
            formatted_val = f"'{val}'"
        else:
            formatted_val = str(val)
            
        output_parts.append(f"{TerminalColors.OKGREEN}{name}{TerminalColors.ENDC} = {formatted_val}")
        
    print(f"{prefix} {' | '.join(output_parts)}", file=sys.stderr)

# =========================================================================================
# 4. Specialized Data Structure Visualization
# =========================================================================================
def debug_matrix_impl(matrix: List[List[Any]], name: str = "Matrix") -> None:
    """
    Prints a 2D matrix in a neatly aligned grid.
    Crucial for DP tables and Grid/Maze graph problems.
    """
    frame = inspect.currentframe()
    lineno = frame.f_back.f_lineno if (frame and frame.f_back) else 0
    
    print(f"{TerminalColors.WARNING}[Line {lineno}] {name}:{TerminalColors.ENDC}", file=sys.stderr)
    
    if not matrix:
        print("  <Empty Matrix>", file=sys.stderr)
        return
        
    # Find the maximum string length of any element to align columns
    max_len = 0
    for row in matrix:
        for val in row:
            max_len = max(max_len, len(str(val)))
            
    # Print with alignment
    for i, row in enumerate(matrix):
        formatted_row = [str(val).rjust(max_len) for val in row]
        row_str = " ".join(formatted_row)
        print(f"  {TerminalColors.OKBLUE}R{i}:{TerminalColors.ENDC} [{row_str}]", file=sys.stderr)

def debug_tree_impl(adj: Dict[int, List[int]], root: int, name: str = "Tree") -> None:
    """
    Visualizes a tree given its adjacency list and a root node.
    Uses ASCII art branches.
    """
    print(f"{TerminalColors.WARNING}[Tree Visualization] {name}:{TerminalColors.ENDC}", file=sys.stderr)
    
    def dfs(node: int, parent: int, prefix: str, is_last: bool):
        # Print current node
        branch = "└── " if is_last else "├── "
        print(f"  {prefix}{branch}{node}", file=sys.stderr)
        
        # Prepare for children
        children = [child for child in adj.get(node, []) if child != parent]
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        for i, child in enumerate(children):
            dfs(child, node, new_prefix, i == len(children) - 1)
            
    if root not in adj and not adj:
        print("  <Empty Tree>", file=sys.stderr)
        return
        
    # Start the tree from a dummy visual root
    print(f"  {TerminalColors.OKCYAN}(Root){TerminalColors.ENDC}", file=sys.stderr)
    dfs(root, -1, "", True)

# =========================================================================================
# 5. Performance Profiling Decorators
# =========================================================================================
def timer_decorator_impl(func: Callable) -> Callable:
    """
    Decorator to measure and log the execution time of a function.
    Useful for checking if a specific function is the bottleneck.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = (end_time - start_time) * 1000 # milliseconds
        
        print(f"{TerminalColors.WARNING}[TIMER]{TerminalColors.ENDC} "
              f"Function {TerminalColors.OKGREEN}'{func.__name__}'{TerminalColors.ENDC} "
              f"took {TerminalColors.OKCYAN}{elapsed:.3f} ms{TerminalColors.ENDC}", 
              file=sys.stderr)
        return result
    return wrapper

def call_counter_impl(func: Callable) -> Callable:
    """
    Decorator to count how many times a function is called.
    Crucial for checking if memoization is working or if a recursive
    function is blowing up exponentially.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    
    wrapper.calls = 0
    
    # We also want a way to print the total calls at the end
    def print_calls():
        print(f"{TerminalColors.WARNING}[COUNTER]{TerminalColors.ENDC} "
              f"Function {TerminalColors.OKGREEN}'{func.__name__}'{TerminalColors.ENDC} "
              f"called {TerminalColors.OKCYAN}{wrapper.calls} times{TerminalColors.ENDC}", 
              file=sys.stderr)
    
    wrapper.print_calls = print_calls
    return wrapper

# =========================================================================================
# 6. Zero-Overhead Environment Switch
# =========================================================================================
# This is the most critical part of the template.
# If we are NOT running locally (i.e., we are on Codeforces, LeetCode, etc.),
# we want our debug functions to do absolutely nothing and incur near zero overhead.

if LOCAL_RUN:
    dbg = debug_impl
    dbg_matrix = debug_matrix_impl
    dbg_tree = debug_tree_impl
    timer = timer_decorator_impl
    counter = call_counter_impl
else:
    # Dummy lambda functions that accept any arguments and do nothing instantly.
    dbg = lambda *args, **kwargs: None
    dbg_matrix = lambda *args, **kwargs: None
    dbg_tree = lambda *args, **kwargs: None
    
    # Dummy decorators that simply return the original function unmodified.
    def dummy_decorator(func: Callable) -> Callable:
        return func
        
    def dummy_counter(func: Callable) -> Callable:
        func.calls = 0
        func.print_calls = lambda: None
        return func
        
    timer = dummy_decorator
    counter = dummy_counter

# =========================================================================================
# 7. Real-World Applications and Tests
# =========================================================================================
def simulate_dp_problem() -> int:
    """
    Simulates solving a Dynamic Programming problem (e.g., Fibonacci or Knapsack).
    Demonstrates tracing recursive calls and memoization using our tools.
    """
    print("--- Simulating DP Problem ---")
    
    memo: Dict[int, int] = {}
    
    @counter
    def fib(n: int) -> int:
        # We can use dbg to trace the state
        dbg(n)
        if n <= 1:
            return n
        if n in memo:
            return memo[n]
        memo[n] = fib(n - 1) + fib(n - 2)
        return memo[n]
        
    result = fib(10)
    
    # Check how many times our function was called
    # If memoization works, calls should be roughly 2*n
    fib.print_calls()
    
    return result

def simulate_graph_problem() -> None:
    """
    Simulates a graph traversal problem.
    Demonstrates matrix printing (for grid mazes) and tree visualization.
    """
    print("\n--- Simulating Graph Problem ---")
    
    # 1. Grid / Matrix Visualization
    # E.g., representing a maze where 1 is a wall and 0 is a path
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1]
    ]
    dbg_matrix(maze, "Maze Grid")
    
    # 2. Tree Visualization
    # E.g., an adjacency list representation of a tree structure
    adj: Dict[int, List[int]] = {
        1: [2, 3],
        2: [1, 4, 5],
        3: [1, 6],
        4: [2],
        5: [2, 7, 8],
        6: [3],
        7: [5],
        8: [5]
    }
    dbg_tree(adj, root=1, name="Company Hierarchy Tree")

@timer
def simulate_heavy_computation() -> None:
    """
    Simulates a heavy computational task to demonstrate the timer decorator.
    """
    print("\n--- Simulating Heavy Computation ---")
    # Simulate work
    total = sum(i * i for i in range(10**6))
    dbg(total)

def test_variable_inspection() -> None:
    """
    Tests the advanced variable name extraction via AST.
    """
    print("\n--- Testing Variable Inspection ---")
    
    # Simple variables
    player_score = 42
    enemy_health = 100
    dbg(player_score, enemy_health)
    
    # Complex expressions
    points = [10, 20, 30]
    multiplier = 2.5
    dbg(points, multiplier, points[0] * multiplier)
    
    # Large collections
    massive_array = list(range(1000))
    dbg(massive_array)

if __name__ == "__main__":
    # Force local mode for demonstration purposes
    # In a real scenario, this is controlled by the LOCAL_RUN constant above.
    global LOCAL_RUN
    LOCAL_RUN = True
    
    # Re-bind functions to their active implementations for this test block
    dbg = debug_impl
    dbg_matrix = debug_matrix_impl
    dbg_tree = debug_tree_impl
    timer = timer_decorator_impl
    counter = call_counter_impl

    print("This output goes to stdout (Online Judge sees this)")
    print("=" * 60)
    
    test_variable_inspection()
    simulate_dp_problem()
    simulate_graph_problem()
    simulate_heavy_computation()
    
    print("=" * 60)
    print("All debug demonstrations completed successfully.")

"""
=========================================================================================
## H. Complexity Analysis & Best Practices
1. AST Overhead: `ast.parse` and stack introspection takes ~0.1ms to ~1ms per call. 
   Inside an O(N^2) loop where N=1000, calling `dbg()` 1,000,000 times will freeze 
   your program locally. 
   **Best Practice**: Only use `dbg()` inside loops when tracing a very small sample.
2. Short-Circuiting: Because of `if LOCAL_RUN`, the online judge sees `lambda: None`. 
   This is optimized out by the Python interpreter, ensuring 0ms overhead on the server.
3. String formatting: `sys.stderr` is used extensively. It is unbuffered by default in 
   some environments, which is great for instant feedback if the program crashes (e.g. 
   RecursionError).

## I. Interview Challenge
1. How would you modify the `_get_caller_args_names` function to correctly parse 
   multi-line function calls (e.g. `dbg(\n x,\n y\n)`) without failing? 
   (Hint: You would need to traverse the source lines upwards until you find matching 
   brackets, or use the `ast.parse` on the whole file and find the line node).
2. Discuss the difference between `time.time()`, `time.process_time()`, and 
   `time.perf_counter()`. Why is `perf_counter` used in the `timer` decorator for CP?
=========================================================================================
"""
