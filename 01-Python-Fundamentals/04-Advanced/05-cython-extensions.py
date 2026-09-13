"""
# ==============================================================================
# LABORATORY: CYTHON AND C-EXTENSIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When pure Python is too slow (even with multiprocessing) and you are performing
# massive mathematical loops (e.g., in pandas or scikit-learn), you must write 
# C-extensions. Cython is a superset of Python that compiles directly to C, 
# offering 100x to 1000x speedups by avoiding Python's dynamic type overhead 
# and explicitly releasing the GIL.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between `def`, `cdef`, and `cpdef`.
# - Understand static typing in Cython (`cdef int x = 0`).
# - Understand how to release the Global Interpreter Lock (`with nogil`).
# - Note: This file is a Python mock demonstrating Cython syntax and concepts. 
#   In a real project, this would be a `.pyx` file compiled via `setup.py`.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PYTHON BOTTLENECK (DYNAMIC TYPING)
# ==============================================================================
def integrate_f_python(a: float, b: float, N: int) -> float:
    """
    Pure Python execution.
    In Python, every time the loop runs, it must:
    1. Check if `i` is an integer.
    2. Check if `dx` is a float.
    3. Allocate a new float object for the result of `i * dx`.
    This dynamic overhead in a tight loop is what makes Python slow.
    """
    s = 0.0
    dx = (b - a) / N
    for i in range(N):
        # f(x) = x^2
        x = a + i * dx
        s += x ** 2
    return s * dx

def demonstrate_python_overhead():
    section_header("The Python Bottleneck")
    print("In pure Python, an integration loop of 10 million iterations")
    print("must perform 10 million type checks and object allocations.")
    print("Cython fixes this by compiling to statically typed C.")


# ==============================================================================
# 4. CYTHON SYNTAX EXPLAINED (MOCK .PYX)
# ==============================================================================

CYTHON_CODE_EXAMPLE = """
# This code belongs in a .pyx file, not a .py file!

# 1. cdef: Pure C function. Fastest. Cannot be called from Python!
cdef double f_c(double x):
    return x ** 2

# 2. cpdef: Creates both a C function and a Python wrapper. Fast, and callable from Python.
cpdef double integrate_f_cython(double a, double b, int N):
    
    # Static Typing: We declare the C types of variables before using them.
    # No more Python objects, no more type checking overhead!
    cdef int i
    cdef double s = 0.0
    cdef double dx = (b - a) / N
    cdef double x
    
    for i in range(N):
        x = a + i * dx
        s += f_c(x)  # Calling a pure C function!
        
    return s * dx
"""

def demonstrate_cython_syntax():
    section_header("Cython Syntax (cdef, cpdef)")
    print("To get a 100x speedup, we statically type variables using 'cdef':")
    print(CYTHON_CODE_EXAMPLE)
    print("By declaring `cdef double s = 0.0`, Cython creates a raw C double.")
    print("It no longer creates expensive Python float objects in the loop.")


# ==============================================================================
# 5. RELEASING THE GIL (`WITH NOGIL`)
# ==============================================================================

CYTHON_NOGIL_EXAMPLE = """
from cython.parallel import prange

# We mark the C function as 'nogil', meaning it doesn't interact with Python objects
cdef double heavy_c_computation(double x) nogil:
    return x ** 2.5

cpdef double parallel_compute(double[:] data):
    cdef int i
    cdef int n = data.shape[0]
    cdef double total = 0.0
    
    # We explicitly release the GIL!
    # Because we are using raw C types and pure C functions, we don't need it.
    with nogil:
        # prange is Cython's parallel range (OpenMP under the hood)
        # This will now utilize ALL CPU CORES automatically!
        for i in prange(n, num_threads=8):
            total += heavy_c_computation(data[i])
            
    return total
"""

def demonstrate_nogil():
    section_header("Bypassing the GIL with Cython")
    print("If you only use C types (no Python objects, lists, or dicts),")
    print("you can explicitly release the Global Interpreter Lock using `with nogil:`.")
    print("\nThis allows true multi-core parallel execution (via OpenMP) inside a single Python process.")
    print("\nExample Syntax:")
    print(CYTHON_NOGIL_EXAMPLE)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between `def`, `cdef`, and `cpdef` in Cython?
   Answer: 
   - `def`: Standard Python function (slow, takes Python objects).
   - `cdef`: Pure C function (extremely fast, takes C types, but CANNOT be called from Python).
   - `cpdef`: Hybrid function (Cython generates a fast C function AND a Python wrapper so it can be called from standard Python scripts).

2. Why is a pure Python `for` loop so much slower than a C `for` loop?
   Answer: Python is dynamically typed. Every iteration, it must check the type of the variables, ensure the `+` operator is valid for those types, and allocate brand new objects in memory for the results. C knows the types at compile-time and simply executes raw CPU instructions.

3. How do you release the GIL in Cython?
   Answer: Use the `with nogil:` block. This tells the interpreter that the code inside the block does not interact with any Python objects, so the lock is not needed. This enables true multi-core parallelism using `prange`.
"""

if __name__ == "__main__":
    demonstrate_python_overhead()
    demonstrate_cython_syntax()
    demonstrate_nogil()
    print("\n[SUCCESS] Laboratory: Cython Concepts Completed.")
