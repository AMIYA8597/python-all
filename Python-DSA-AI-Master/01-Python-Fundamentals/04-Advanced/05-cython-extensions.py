"""
## A. Concept Name
Cython and C-Extensions (Pure Python Mode)

## B. One-Sentence Definition
Cython is an optimizing static compiler for Python that translates Python code—augmented with optional C-like static typing—into highly optimized C/C++ code.

## C. Why Does This Exist?
Python is dynamically typed and interpreted, which makes it highly productive but inherently slow for CPU-bound numerical loops and heavy computational tasks. Cython exists to bridge the gap between Python's rapid development speed and C's execution speed.

## D. Intuition
Imagine Python as a friendly manager who has to ask for every detail before doing a task (dynamic typing checks). C is like a specialized machine that blindly executes tasks at lightning speed because everything is strictly predefined (static typing). Cython allows the manager to give strict, predefined instructions to the machine ahead of time, eliminating the constant questioning.

## E. Real-Life Analogy
Think of writing Python as speaking to a human translator who translates your words into another language sentence by sentence in real-time (interpretation). It's flexible but slow. Cython is like giving the translator a written script beforehand so they can publish a fully translated book (compilation). When people want to read it, they just read the book directly, bypassing the real-time translation process.

## F. Mental Model
Python Code -> Add Cython Types (optional) -> Cython Compiler -> C/C++ Code -> C/C++ Compiler -> Compiled Python Extension Module (.so or .pyd) -> Imported in Python like a normal module.

## G. Visual Explanation
```
[Python World (Slow, Dynamic)]
       |
       | (Cython syntax / Pure Python annotations)
       v
[Cython Compiler] --> Generates standard C/C++ code
       |
       v
[C Compiler (gcc/clang)] --> Generates shared object (.so / .pyd)
       |
       v
[Back to Python World] <-- Can be 'import'ed natively (Fast, Static)
```

## H. Formal Explanation
Cython extends Python with static typing. Variables, class attributes, and function return types can be declared with C data types. When Cython compiles this code, it maps these variables directly to C variables, circumventing the Python C-API overhead (like PyObject reference counting and type checking) for operations involving only these static types. Pure Python mode uses decorators and type hints to allow Cython to compile the file while retaining standard Python interpretability.

## I. Mathematical Foundation (if applicable)
Not mathematically complex, but deeply rooted in compiler theory (Abstract Syntax Trees, static analysis, and code generation) and the C-Python API (PyObject structure).

## J. From-Scratch Implementation (if applicable)
Normally Cython is written in `.pyx` files. In this file, we use Cython's "Pure Python Mode" which uses the `cython` module to provide C-types and decorators to standard `.py` files.

## K. Library / Production Implementation (if applicable)
Libraries like NumPy, pandas, scikit-learn, and SciPy heavily rely on Cython (and C/C++) to achieve their high performance.

## L. Trace (walk through example)
1. Python executes `sum_cython_pure(100)`.
2. Uncompiled: Python sees the `@cython.locals` and type hints, ignores them (or mocks them), and interprets the loop normally.
3. Compiled: Cython translated this to a C function taking a `long n`. It uses a C `for` loop and C arithmetic. Python never gets involved in the loop. The final C `total` is converted back to a Python object (`PyLong_FromLong`) before returning.

## M. Complexity
- Time Complexity: O(N) for the loops below. However, the *constant factor* drops dramatically (often 100x-1000x) when compiled, as it avoids Python VM overhead per iteration.
- Space Complexity: O(1).

## N. Common Mistakes
- **Type Mismatch:** Mixing Python objects and C types unnecessarily within inner loops, causing Cython to generate slow C-API calls (Python interactions) instead of pure C operations.
- **Integer Overflow:** Python handles arbitrarily large integers automatically. C integers (`cython.int`) will silently overflow if they exceed `INT_MAX`.

## O. Common Confusions
- **Cython vs. CPython:** CPython is the standard Python interpreter (written in C). Cython is a separate compiler that translates Python-like code into C code to create extensions *for* CPython.
- **Uncompiled vs. Compiled:** Running a script with `python script.py` does not compile Cython code. It must be explicitly compiled via `cythonize` or a `setup.py` script to see performance gains.

## P. When To Use
- When you have CPU-bound loops with mathematical operations.
- When you need to wrap and interface with existing C or C++ libraries.
- When you want to release the Global Interpreter Lock (GIL) for true multithreading in Python.

## Q. When NOT To Use
- For I/O bound tasks (use `asyncio` or threading instead).
- When the code is already vectorized using NumPy.
- When you can achieve the same with simpler JIT compilers like Numba (for pure math).

## R. Trade-offs
- **Speed vs. Portability:** Cython makes code blazing fast but requires a C compiler and build step on every target platform (Windows, macOS, Linux).
- **Flexibility vs. Safety:** You gain C-speed but lose Python's automatic overflow protection and gain the possibility of segfaults.

## S. Debugging
Debugging compiled C-extensions is harder than Python. Cython provides a debugger (`cygdb`), but often, "Pure Python Mode" (used here) is preferred because you can debug the code with `pdb` or your IDE before compiling it for production.

## T. Memory Hook
Cython is the "Translator". It reads Python, writes C, and packages it up so Python can use it without knowing C was ever involved.

## U. Active Recall
1. What is the difference between Cython and CPython?
2. What overhead does Cython avoid by using static typing?
3. What is the danger of using `cython.int` instead of a standard Python integer?

## V. Practice
Write a pure Python Cythonized function to compute the Nth Fibonacci number iteratively, utilizing `cython.locals` to define C integers for the sequence state.

## W. Interview Question
"When would you choose Cython over multiprocessing, and when would you choose Cython over PyPy?"
*Answer:* 
- Cython over multiprocessing: When you need shared memory between workers without serialization (IPC) overhead, Cython with `nogil` allows threads to process shared arrays concurrently.
- Cython over PyPy: PyPy uses JIT to speed up Python generally. Choose Cython to wrap existing C/C++ libraries or when you need deterministic memory management and low-level control that a JIT cannot guarantee.

## X. Project Connection
In large data engineering or machine learning projects, custom metrics or complex aggregations that cannot be vectorized efficiently with Pandas/NumPy are often moved to Cython extensions to prevent them from becoming pipeline bottlenecks.
"""

# Try to import the cython module; if not available, we define dummy decorators/functions
# so the script remains executable in standard Python.
try:
    import cython
except ImportError:
    # Dummy cython module for environments without Cython installed
    class _CythonDummy:
        def cclass(self, cls): return cls
        def cfunc(self, func): return func
        def ccov(self, func): return func
        def declare(self, *args, **kwargs): pass
        def locals(self, **kwargs):
            def decorator(func): return func
            return decorator
        int = int
        double = float
        p_double = float
    cython = _CythonDummy()  # type: ignore

import time
from typing import List


# --- Basic Implementation: Pure Python vs Cythonized ---
def sum_pure_python(n: int) -> int:
    """Standard Python implementation of a simple loop."""
    total = 0
    for i in range(n):
        total += i
    return total

@cython.cfunc
@cython.locals(n=cython.int, total=cython.int, i=cython.int)
def sum_cython_pure(n: int) -> int:
    """
    Cython pure Python implementation.
    If compiled, Cython will use C integers for `n`, `total`, and `i`,
    making the loop execute at C speed. Uncompiled, it runs as normal Python.
    """
    total: cython.int = 0  # type: ignore
    i: cython.int  # type: ignore
    for i in range(n):
        total += i
    return total


# --- Intermediate Implementation: Cython Classes (Extension Types) ---
@cython.cclass
class Particle:
    """
    Using @cython.cclass creates a C-extension type (like a built-in type).
    Attributes must be explicitly declared for C-level access.
    """
    x: cython.double  # type: ignore
    y: cython.double  # type: ignore
    velocity: cython.double  # type: ignore

    def __init__(self, x: float, y: float, velocity: float):
        self.x = x
        self.y = y
        self.velocity = velocity

    @cython.cfunc
    def get_momentum(self, mass: float) -> float:
        return self.velocity * mass


# --- Advanced Implementation: Releasing the GIL ---
"""
In true Cython (.pyx files), you can use `with nogil:` block to release 
the Global Interpreter Lock, allowing true multi-threading for CPU bound tasks.

Example (Pure Python Syntax equivalent):

@cython.cfunc
@cython.nogil
def heavy_computation(data_ptr: cython.p_double, size: cython.int) -> cython.double:
    ...
"""

# --- Tests ---
def run_tests() -> None:
    print("Testing Cython Concepts (in Pure Python Mode)...")

    n = 1000000

    # Test pure Python sum
    start = time.time()
    res1 = sum_pure_python(n)
    time_py = time.time() - start

    # Test Cython pure Python sum
    start = time.time()
    res2 = sum_cython_pure(n)
    time_cy = time.time() - start

    assert res1 == res2

    print(f"Pure Python Time: {time_py:.4f}s")
    print(f"Cython Syntax Time: {time_cy:.4f}s")
    print("(Note: They are similar because this script is being interpreted, not compiled.)")

    # Test Class
    p = Particle(0.0, 0.0, 10.5)
    assert p.get_momentum(2.0) == 21.0

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
