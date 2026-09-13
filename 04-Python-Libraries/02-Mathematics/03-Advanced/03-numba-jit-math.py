"""
# ==============================================================================
# LABORATORY: JUST-IN-TIME COMPILATION (NUMBA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python is interpreted. A massive `for` loop in Python executes 100x slower 
# than the exact same loop written in C.
#
# NumPy solved this by pre-compiling all of its array operations in C. 
# But what if your algorithm *cannot* be vectorized? What if you have a highly 
# complex custom simulation with nested `if/else` logic that forces you to write 
# raw Python `for` loops?
#
# Enter **Numba**.
# Numba is a Just-In-Time (JIT) compiler. You simply put `@njit` above your 
# standard Python function. 
# The very first time the function is called, Numba intercepts the Python 
# bytecode, passes it to the LLVM compiler, translates it into bare-metal 
# Machine Code, and replaces the Python function in RAM.
#
# From that point forward, calling the function literally executes raw Machine Code. 
# Your Python `for` loop will run at the exact speed of C++!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Interpreted Python and LLVM Machine Code.
# - Apply the `@njit` decorator to accelerate mathematical loops.
# - Utilize `prange` to instantly multithread your code across all CPU cores.
#
# ==============================================================================
"""

import math
import time
import numpy as np

# In a real environment, you must `pip install numba`
try:
    from numba import njit, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False
    # Fallback decorators so the script doesn't crash if Numba isn't installed
    def njit(*args, **kwargs):
        def decorator(func): return func
        if len(args) == 1 and callable(args[0]): return args[0]
        return decorator
    prange = range

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PURE PYTHON VS JIT COMPILATION
# ==============================================================================
# We will simulate a massive Monte Carlo calculation (e.g., calculating Pi 
# by throwing 10 million random darts at a dartboard).
# This requires a massive `for` loop that cannot be easily vectorized without 
# consuming massive amounts of RAM.

def monte_carlo_pi_pure_python(samples: int) -> float:
    """Standard, agonizingly slow Python execution."""
    inside_circle = 0
    for i in range(samples):
        # Native Python random module isn't supported inside Numba optimally, 
        # but Numba intercepts numpy's random perfectly!
        x = np.random.random()
        y = np.random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
    return (inside_circle / samples) * 4.0


# The `@njit` decorator is an alias for `@jit(nopython=True)`.
# `nopython=True` forces Numba to completely bypass the Python interpreter. 
# If it fails to compile the code into pure LLVM C, it will throw an error 
# rather than falling back to slow Python.
@njit
def monte_carlo_pi_numba(samples: int) -> float:
    """Compiled to bare-metal Machine Code at runtime!"""
    inside_circle = 0
    for i in range(samples):
        x = np.random.random()
        y = np.random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
    return (inside_circle / samples) * 4.0


def demonstrate_jit():
    section_header("JIT Compilation (LLVM Machine Code)")
    
    if not HAS_NUMBA:
        print("[WARNING] Numba is not installed. Both functions will run in Python.")
        print("Install it using: pip install numba")
    
    samples = 10_000_000 # 10 Million loops!
    print(f"Calculating Pi using {samples:,} Monte Carlo simulations...")
    
    # 1. RUNNING PURE PYTHON
    start = time.perf_counter()
    pi_py = monte_carlo_pi_pure_python(samples)
    end = time.perf_counter()
    py_time = end - start
    print(f"\nPure Python Result : {pi_py:.6f}")
    print(f"Pure Python Time   : {py_time:.4f} seconds (Slow...)")
    
    # 2. RUNNING NUMBA
    # CRITICAL NOTE: The first time a Numba function is called, it takes 
    # a fraction of a second to compile! We must do a "Warmup" run!
    if HAS_NUMBA:
        _ = monte_carlo_pi_numba(10) # Warmup compile
        
    start = time.perf_counter()
    pi_nb = monte_carlo_pi_numba(samples)
    end = time.perf_counter()
    nb_time = end - start
    print(f"\nNumba JIT Result   : {pi_nb:.6f}")
    print(f"Numba JIT Time     : {nb_time:.4f} seconds (Blazing Fast!)")
    
    if HAS_NUMBA:
        speedup = py_time / nb_time
        print(f"\nSPEEDUP FACTOR: {speedup:.1f}x Faster than Python!")


# ==============================================================================
# 4. INSTANT PARALLELIZATION (PRANGE)
# ==============================================================================
# Numba can also automatically multithread your code! 
# By adding `parallel=True` and changing `range` to `prange`, Numba will instruct 
# LLVM to distribute the loop chunks evenly across all physical cores on your CPU!

@njit(parallel=True)
def monte_carlo_pi_numba_parallel(samples: int) -> float:
    inside_circle = 0
    # prange instructs the compiler to multithread this loop!
    for i in prange(samples):
        x = np.random.random()
        y = np.random.random()
        if x**2 + y**2 <= 1.0:
            inside_circle += 1
    return (inside_circle / samples) * 4.0

def demonstrate_parallel():
    section_header("Instant Multithreading (prange)")
    
    if not HAS_NUMBA:
        return
        
    samples = 10_000_000
    
    _ = monte_carlo_pi_numba_parallel(10) # Warmup
    
    start = time.perf_counter()
    pi_par = monte_carlo_pi_numba_parallel(samples)
    end = time.perf_counter()
    par_time = end - start
    
    print(f"Numba Multithreaded Result : {pi_par:.6f}")
    print(f"Numba Multithreaded Time   : {par_time:.4f} seconds!")
    print("\nNumba completely bypassed Python's Global Interpreter Lock (GIL), ")
    print("allowing true, hardware-level CPU parallelism!")


def run_all_labs():
    demonstrate_jit()
    demonstrate_parallel()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does "Just-In-Time" (JIT) mean?
   Answer: Languages like C++ are "Ahead-Of-Time" (AOT) compiled. You run a compiler program, it creates an `.exe` file containing Machine Code, and you distribute the `.exe`. Python is interpreted; it reads code line-by-line. JIT is a hybrid. You ship Python code. When the user runs the script, the exact moment the CPU reaches the `@njit` decorator, the execution pauses. Numba compiles that specific function directly into LLVM Machine Code in RAM, replaces the Python function pointer, and executes the Machine Code. It compiles "Just In Time" for execution.

2. Why do we prefer `@njit` over `@jit`?
   Answer: `@njit` is an alias for `@jit(nopython=True)`. If you just use `@jit`, Numba will attempt to compile the code. If it encounters a Python object it doesn't understand (like a complex custom Class or an unsupported dictionary), it will silently fall back to "Object Mode", wrapping standard slow Python calls inside the C code. It gives you a false sense of security with zero performance gain! `@njit` forces Numba to compile in "No Python" mode. If it fails to understand something, it strictly crashes, forcing you to write mathematically pure, compilable code.

3. Why is `prange` able to bypass the Python GIL?
   Answer: The Global Interpreter Lock (GIL) is a Mutex that prevents multiple CPU threads from executing Python bytecodes simultaneously. It exists because Python's memory management (Reference Counting) is not thread-safe. However, when Numba compiles a function using `nopython=True`, the resulting Machine Code does not use Python objects! It uses raw $C$ floats and ints. Since there are no Python objects involved, Numba explicitly releases the GIL, allowing the raw Machine Code to multithread natively via OpenMP.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Numba JIT Compiler Completed.")
