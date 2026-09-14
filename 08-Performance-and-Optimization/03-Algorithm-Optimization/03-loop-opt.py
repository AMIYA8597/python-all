"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (LOOP OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A `for` loop executes its internal bytecode millions of times. A microscopic 
# architectural inefficiency inside the loop mathematically compounds into a 
# catastrophic performance bottleneck.
#
# A junior engineer places `math.sqrt()` inside a 5,000,000 iteration loop. 
# The Python interpreter must execute a dictionary lookup for the `math` module, 
# and another dictionary lookup for `sqrt`, exactly 5,000,000 times.
#
# A senior engineer "hoists" the function resolution OUTSIDE the loop 
# (`sqrt = math.sqrt`). The dictionary lookups are executed exactly once. The 
# inner loop uses a direct, localized pointer, instantly shaving seconds off 
# the execution time without changing any core logic.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Loop Invariant Code Hoisting.
# - Master Local Variable vs Global Variable pointer resolution.
# - Prove the CPU cost of the Python "Dot" operator.
#
# ==============================================================================
"""

import timeit
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE "DOT" OPERATOR PENALTY
# ==============================================================================
# Every time you use a '.' in Python, it triggers a `__getattribute__` execution!
# It mathematically searches Hash Tables to resolve the pointer.

def naive_loop_with_dots(n: int) -> float:
    """
    Time Complexity: O(N)
    The CPU must resolve the `math` module and the `sqrt` function on EVERY iteration.
    """
    total = 0.0
    for i in range(n):
        # DOT PENALTY: Two dictionary lookups per loop!
        total += math.sqrt(i)
    return total

def optimized_loop_hoisted(n: int) -> float:
    """
    Time Complexity: O(N)
    The dot operator is mathematically "Hoisted" outside the loop!
    """
    total = 0.0
    # HOISTING: The dictionary lookup happens exactly ONCE!
    # `local_sqrt` is now a highly-optimized Local Variable pointer!
    local_sqrt = math.sqrt
    for i in range(n):
        total += local_sqrt(i)
    return total

def demonstrate_dot_penalty():
    section_header("Performance Proof: Loop Hoisting & The Dot Penalty")
    
    N = 10_000_000 # 10 Million iterations!
    print(f"  Executing {N:,} iterations...")
    
    print("\n  [NAIVE LOOP (Millions of Dictionary Lookups)]")
    start_naive = timeit.default_timer()
    res_naive = naive_loop_with_dots(N)
    end_naive = timeit.default_timer()
    time_naive = end_naive - start_naive
    print(f"    -> Time:   {time_naive:.4f} seconds")
    
    print("\n  [OPTIMIZED LOOP (Hoisted Variables)]")
    start_opt = timeit.default_timer()
    res_opt = optimized_loop_hoisted(N)
    end_opt = timeit.default_timer()
    time_opt = end_opt - start_opt
    print(f"    -> Time:   {time_opt:.4f} seconds")
    
    speedup = ((time_naive - time_opt) / time_naive) * 100
    print(f"\n  [CONCLUSION] Hoisting the dot operator reduced execution time by {speedup:.2f}%!")


# ==============================================================================
# 4. BUILT-INS VS EXPLICIT LOOPS (THE C-LEVEL DELEGATION)
# ==============================================================================
# Python's built-in functions (`map`, `sum`, `filter`) are physically implemented 
# in C. When possible, delegating a loop to a built-in instantly pushes the 
# execution into optimized C-code.

def explicit_python_loop(n: int) -> int:
    """The interpreter mathematically drives the loop in Python Bytecode."""
    total = 0
    for i in range(n):
        total += i
    return total

def builtin_c_loop(n: int) -> int:
    """The interpreter yields execution to the C-level `sum()` function."""
    return sum(range(n))

def demonstrate_builtin_delegation():
    section_header("Performance Proof: Python Bytecode vs C-Level Built-ins")
    
    N = 10_000_000
    
    print("\n  [EXPLICIT PYTHON LOOP (Bytecode Execution)]")
    start_py = timeit.default_timer()
    res_py = explicit_python_loop(N)
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Time:   {time_py:.4f} seconds")
    
    print("\n  [C-LEVEL BUILT-IN (sum())]")
    start_c = timeit.default_timer()
    res_c = builtin_c_loop(N)
    end_c = timeit.default_timer()
    time_c = end_c - start_c
    print(f"    -> Time:   {time_c:.4f} seconds")
    
    speedup = ((time_py - time_c) / time_py) * 100
    print(f"\n  [CONCLUSION] Delegating to `sum()` reduced execution time by {speedup:.2f}%!")


def run_all_labs():
    demonstrate_dot_penalty()
    demonstrate_builtin_delegation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Explain the architectural cost of the 'dot operator' in Python, and why it matters inside a loop."
   Senior Answer: "Python is a dynamic language; it does not resolve object attributes at compile time. When the interpreter encounters `math.sqrt`, it mathematically fires the `__getattribute__` magic method. It must hash the string 'math', locate the module in the global namespace, hash the string 'sqrt', and locate the function pointer inside the module's `__dict__`. While dictionaries are $O(1)$, executing two C-level hash lookups millions of times inside a tight `for` loop generates catastrophic CPU overhead. By 'Hoisting' the lookup outside the loop (`sqrt = math.sqrt`), we pay the hash penalty exactly once, allowing the inner loop to use a direct local pointer."

2. Interviewer: "Why are Local Variables mathematically faster to access than Global Variables in Python?"
   Senior Answer: "Global variables are stored in a standard Dictionary (`globals()`). Accessing a global variable requires string hashing and dictionary traversal. Local variables, however, are architecturally optimized by the Python compiler. When a function is compiled, Python physically counts the local variables and assigns them to a statically-sized C-array (the 'Fast Locals' array). Accessing a local variable is executed using the `LOAD_FAST` bytecode, which is a direct $O(1)$ integer index lookup (`array[index]`), entirely bypassing the hashing engine. This makes Local Variable access up to $30-50\\%$ faster than Global access."

3. Interviewer: "If `map()` and `sum()` execute in optimized C-code, why are List Comprehensions usually considered 'faster' or 'more pythonic' than `map`?"
   Senior Answer: "Historically, `map(lambda x: x*2, data)` was slower than a list comprehension `[x*2 for x in data]` because the `map` function had to invoke the `lambda` function repeatedly. Python function calls incur massive bytecode stack overhead (creating frames, resolving variables). The C-level speed of `map` was completely annihilated by the Python-level function call overhead on every iteration! List comprehensions resolve this by executing the arithmetic inline, avoiding function frames entirely. However, if you are mapping a pre-existing built-in function (e.g., `map(str, data)`), `map` is vastly superior because it stays entirely within the C-layer, generating zero Python bytecode frames."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Algorithm Optimization (Loop Optimization) Completed.")
