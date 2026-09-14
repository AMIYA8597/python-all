"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (NUMBA & JIT COMPILATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# NumPy is incredibly fast for vectorized operations, but it fails if your algorithm 
# fundamentally *requires* a custom `for` loop that cannot be broadcasted (e.g., 
# complex iterative Monte Carlo simulations, custom Cryptography hashes).
#
# A junior engineer abandons Python completely and spends 3 weeks rewriting the 
# algorithm in C++, manually compiling and linking a shared library to Python.
#
# A senior engineer installs `numba` and adds a single `@jit` decorator above 
# their standard Python `for` loop. At runtime, the Numba LLVM compiler mathematically 
# translates the Python bytecode into pure, optimized Machine Code, bypassing the 
# GIL and executing at exact C-level speeds, taking exactly 3 seconds to implement.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Just-In-Time (JIT) compilation in Python.
# - Master `nopython=True` mode (bypassing the CPython API entirely).
# - Prove the performance parity of Numba vs C++.
#
# ==============================================================================
"""

import timeit
import math
import random
try:
    from numba import jit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE COMPLEX CUSTOM LOOP (IMPOSSIBLE TO VECTORIZE)
# ==============================================================================
# A Monte Carlo simulation to estimate Pi. 
# It fundamentally requires an iterative loop with internal conditional logic!

def python_monte_carlo_pi(n: int) -> float:
    """
    Time Complexity: O(N)
    A pure Python implementation. The Interpreter executes every single 
    multiplication, addition, and conditional check in slow Bytecode.
    """
    acc = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        # The CPU must dynamically type-check every float and execute the math!
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / n


# ==============================================================================
# 4. THE NUMBA JIT COMPILATION (LLVM MACHINE CODE)
# ==============================================================================
# The `@jit(nopython=True)` decorator (or `@njit`) mathematically forbids the compiled 
# machine code from ever calling back into the CPython Interpreter. 
# It executes entirely on bare metal!

if HAS_NUMBA:
    @jit(nopython=True)
    def numba_monte_carlo_pi(n: int) -> float:
        """
        At runtime, Numba inspects this code, identifies that `n` is an integer, 
        and physically compiles this exact function into raw LLVM Machine Code.
        """
        acc = 0
        for i in range(n):
            x = random.random()
            y = random.random()
            if (x**2 + y**2) < 1.0:
                acc += 1
        return 4.0 * acc / n


# ==============================================================================
# 5. MATHEMATICAL JIT COMPILATION PROOF
# ==============================================================================
def demonstrate_jit_compilation():
    section_header("Performance Proof: CPython Bytecode vs LLVM Machine Code")
    
    if not HAS_NUMBA:
        print("  [ERROR] Numba is not installed. Run `pip install numba`.")
        return
        
    N = 10_000_000 # 10 Million Iterations!
    
    print("\n  [PURE CPYTHON INTERPRETER]")
    start_py = timeit.default_timer()
    res_py = python_monte_carlo_pi(N)
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Estimated Pi: {res_py:.6f}")
    print(f"    -> Time:   {time_py:.4f} seconds")
    
    # --------------------------------------------------------------------------
    # CRITICAL NUMBA ARCHITECTURE: THE FIRST RUN PENALTY
    # --------------------------------------------------------------------------
    print("\n  [NUMBA COMPILATION PHASE]")
    print("    (Numba is currently translating the Python Bytecode to C/LLVM...)")
    
    # The First Run incurs a massive time penalty because the compiler is actively 
    # writing the Machine Code binary!
    start_compile = timeit.default_timer()
    numba_monte_carlo_pi(1) # We compile it on a tiny N!
    end_compile = timeit.default_timer()
    print(f"    -> Compilation Time: {end_compile - start_compile:.4f} seconds")
    
    print("\n  [NUMBA EXECUTING PURE MACHINE CODE]")
    start_nb = timeit.default_timer()
    res_nb = numba_monte_carlo_pi(N)
    end_nb = timeit.default_timer()
    time_nb = end_nb - start_nb
    print(f"    -> Estimated Pi: {res_nb:.6f}")
    print(f"    -> Time:   {time_nb:.4f} seconds")
    
    speedup = time_py / time_nb
    print(f"\n  [CONCLUSION] Numba compiled the code to bare metal, achieving a {speedup:.1f}x speedup!")


def run_all_labs():
    demonstrate_jit_compilation()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is Just-In-Time (JIT) compilation, and how does Numba execute it mathematically?"
   Senior Answer: "Python is an Interpreted language (AOT/Ahead-Of-Time compilation does not happen). When Numba's `@jit` decorator intercepts a function call, it pauses execution. It mathematically analyzes the Type Signatures of the provided arguments (e.g., detecting that `n` is a 64-bit integer). It then utilizes the LLVM Compiler Infrastructure to dynamically generate highly optimized, native Machine Code for that exact type signature in real-time (Just-In-Time). It caches this binary executable in RAM. All subsequent calls to the function entirely bypass the Python interpreter and execute the raw Machine Code directly on the CPU, achieving C++ parity speeds."

2. Interviewer: "Why is `nopython=True` strictly required to achieve maximum performance in Numba?"
   Senior Answer: "If you simply use `@jit` without `nopython=True`, Numba operates in 'Object Mode'. It attempts to compile the code, but if it encounters a dynamic Python object (like a massive Dictionary or a custom Class) that it cannot map to a strict C-type, it will silently fall back to calling the CPython C-API to handle it. This context-switching between Machine Code and the Python Interpreter completely annihilates performance. By enforcing `nopython=True`, we mathematically guarantee that Numba will exclusively generate bare-metal Machine Code. If it encounters Python objects it cannot compile, it violently crashes with a `TypingError`, forcing the developer to rewrite the logic into strict C-compatible arrays and loops."

3. Interviewer: "If Numba can compile Python into C-level Machine Code, why don't we just put `@jit` on every single function in a Django Web Backend?"
   Senior Answer: "Numba is strictly a mathematical array-processing compiler. It exclusively understands contiguous memory (NumPy arrays) and primitive scalars (floats, ints). It physically does not understand Python ORMs, SQLAlchemy models, WebSockets, or dynamic HTTP JSON Request dictionaries. If you attempt to `@jit` a web endpoint, Numba will crash instantly because it cannot translate dynamic web classes into static C-structs. Numba should only be deployed on isolated mathematical bottlenecks (e.g., a function calculating encryption hashes or simulating physical physics)."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Algorithm Optimization (Numba & JIT) Completed.")
