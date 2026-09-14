"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (HIGH-PERFORMANCE DATA SCIENCE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist needs to calculate the Haversine distance (the 
# mathematical distance between two GPS coordinates on a sphere) for 5,000,000 
# taxi rides. They use a standard Pandas `.apply()` with a Python function. 
# Because `.apply()` is just a glorified `for` loop executing slow CPython 
# bytecode 5,000,000 times, the script takes 12 minutes to execute. The CEO 
# cancels the deployment because it cannot run in real-time.
#
# A senior performance engineer architects a "High-Performance Pipeline". 
# First, they try pure Vectorization (NumPy arrays). The execution time drops 
# to 0.5 seconds. Then, they inject the `@njit` decorator from `numba`. This 
# forces the Python code to be mathematically compiled directly into absolute 
# C-level Machine Code (LLVM) just before execution. The execution time violently 
# collapses to 0.02 seconds. The pipeline is deployed to production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Pandas Vectorization (bypassing `.apply()`).
# - Execute Just-In-Time (JIT) Compilation using `Numba`.
# - Architect high-performance mathematical pipelines for massive datasets.
#
# ==============================================================================
"""

import math
import timeit
import random

# Gracefully handle dependencies
try:
    import numpy as np
    import pandas as pd
    from numba import njit, prange
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MATHEMATICAL PRIMITIVE (THE HAVERSINE FORMULA)
# ==============================================================================
# The Haversine formula determines the great-circle distance between two points 
# on a sphere given their longitudes and latitudes.
# It requires heavy Trigonometry (sin, cos, atan2).

def haversine_slow_python(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """A standard, mathematically slow Python implementation."""
    R = 6371.0 # Earth radius in kilometers
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
        
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


# ==============================================================================
# 4. THE NUMBA COMPILATION ARCHITECTURE
# ==============================================================================
# The `@njit` decorator (No-Python JIT) is algorithmic magic.
# When Python sees this, it stops execution. It mathematically translates the 
# Python bytecode into pure C/LLVM Machine Code, compiles it, and caches it in RAM.
# The resulting function runs at the exact same speed as raw C or C++.

if HAS_LIBS:
    @njit(fastmath=True)
    def haversine_fast_numba(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """A mathematically compiled C-level implementation."""
        # Numba supports `math` functions, but they are compiled directly to C!
        R = 6371.0
        
        # We must use math (not np) inside basic Numba scalar functions for max speed
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2.0)**2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2.0)**2
            
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        
        return R * c
        
    # We can even parallelize the array execution mathematically in C!
    @njit(parallel=True, fastmath=True)
    def calculate_all_distances_numba(lat1_arr, lon1_arr, lat2_arr, lon2_arr):
        n = len(lat1_arr)
        result = np.zeros(n)
        # `prange` commands Numba to unlock all physical CPU Cores, bypassing the GIL!
        for i in prange(n):
            result[i] = haversine_fast_numba(lat1_arr[i], lon1_arr[i], lat2_arr[i], lon2_arr[i])
        return result


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_performance():
    section_header("Project: High-Performance Data Science")
    
    if not HAS_LIBS:
        print("  [ERROR] Pandas/Numba not installed. Run `pip install pandas numpy numba`.")
        return
        
    # We will simulate exactly 1,000,000 GPS coordinates!
    ROWS = 1_000_000
    print(f"  [INIT] Generating DataFrame with {ROWS:,} mathematical coordinates...")
    
    df = pd.DataFrame({
        'lat1': np.random.uniform(40.0, 41.0, ROWS),
        'lon1': np.random.uniform(-74.0, -73.0, ROWS),
        'lat2': np.random.uniform(40.0, 41.0, ROWS),
        'lon2': np.random.uniform(-74.0, -73.0, ROWS)
    })

    # --- SCENARIO A: THE JUNIOR APPROACH (Pandas .apply) ---
    print(f"\n  [SCENARIO A: PANDAS .APPLY() CATASTROPHE]")
    print("    -> Simulating .apply() on 1M rows (This would take ~10 seconds).")
    print("    -> [SKIPPED] To prevent the CI/CD pipeline from stalling.")
    
    # --- SCENARIO B: THE MID-LEVEL APPROACH (NumPy Vectorization) ---
    print(f"\n  [SCENARIO B: PURE NUMPY VECTORIZATION]")
    start_vec = timeit.default_timer()
    
    # We use NumPy's C-level arrays to execute math on the entire column simultaneously!
    R = 6371.0
    phi1 = np.radians(df['lat1'])
    phi2 = np.radians(df['lat2'])
    delta_phi = np.radians(df['lat2'] - df['lat1'])
    delta_lambda = np.radians(df['lon2'] - df['lon1'])
    
    a = np.sin(delta_phi / 2.0)**2 + \
        np.cos(phi1) * np.cos(phi2) * \
        np.sin(delta_lambda / 2.0)**2
        
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distances_vec = R * c
    
    end_vec = timeit.default_timer()
    time_vec = end_vec - start_vec
    print(f"    -> Execution Time: {time_vec:.4f} seconds (Blazing fast C-arrays!)")
    
    
    # --- SCENARIO C: THE SENIOR APPROACH (Numba JIT + Parallel CPU) ---
    print(f"\n  [SCENARIO C: NUMBA LLVM JIT COMPILATION]")
    print("    -> Booting LLVM Compiler...")
    
    # We extract the raw C-arrays from Pandas using `.values`
    lat1_arr = df['lat1'].values
    lon1_arr = df['lon1'].values
    lat2_arr = df['lat2'].values
    lon2_arr = df['lon2'].values
    
    # WARMUP: The first time Numba runs, it must physically compile the C-code.
    # We run a dummy array to force compilation so it doesn't taint our benchmark.
    _ = calculate_all_distances_numba(lat1_arr[:10], lon1_arr[:10], lat2_arr[:10], lon2_arr[:10])
    
    # THE ACTUAL BENCHMARK
    start_jit = timeit.default_timer()
    distances_jit = calculate_all_distances_numba(lat1_arr, lon1_arr, lat2_arr, lon2_arr)
    end_jit = timeit.default_timer()
    
    time_jit = end_jit - start_jit
    print(f"    -> Execution Time: {time_jit:.4f} seconds (Multi-core Machine Code!)")
    
    
    # --- CONCLUSION ---
    if time_jit > 0:
        speedup = time_vec / time_jit
        print(f"\n  [CONCLUSION] Numba was {speedup:.1f}x FASTER than pure NumPy vectorization!")
        print("  By architecting pure Machine Code, we mathematically conquered the 1M row dataset.")


def run_all_labs():
    demonstrate_performance()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is `pandas.apply()` mathematically catastrophic for mathematical operations on a $5$-Million row DataFrame?"
   Senior Answer: "The CPython Interpreter Overhead. `pandas.apply()` is not vectorized C-code; it is literally a glorified Python `for` loop under the hood. For every single one of the $5,000,000$ rows, Pandas must mathematically extract the row, convert the C-level `float64` into a heavy Python Object, pass it into the CPython Interpreter, evaluate the bytecode, convert the answer back to a C-level float, and insert it into a new array. This massive boxing/unboxing overhead consumes $99\\%$ of the CPU cycles. Native Vectorization (NumPy) bypasses the Python interpreter completely, executing a single C-loop over raw contiguous memory blocks."

2. Interviewer: "If NumPy is already written in raw C, how is it mathematically possible for Numba (`@njit`) to beat it by an additional $3\\times$ or $4\\times$ speedup?"
   Senior Answer: "Temporary Array Allocation (RAM Thrashing). When you execute a massive NumPy equation like `np.sin(A) + np.cos(B)`, NumPy cannot execute it in one pass. First, it calculates `np.sin(A)`, allocates a massive temporary array in RAM to hold the answer, then calculates `np.cos(B)`, allocates a second array in RAM, and finally loops through both to add them together. Allocating and reading giant blocks of RAM is violently slow. Numba mathematically fuses the entire equation into a single LLVM Machine Code Loop. It calculates the Sin, Cos, and Addition for Index $0$, stores the final answer, and moves to Index $1$, requiring absolutely zero temporary RAM arrays and ensuring perfect CPU L1 Cache locality."

3. Interviewer: "Why did we mathematically extract the raw arrays using `df['lat1'].values` before passing them into the Numba function?"
   Senior Answer: "Numba's 'No-Python' Mode architecture. The `@njit` decorator mathematically commands Numba to sever all ties with the CPython Interpreter and generate pure LLVM Machine Code. The Numba compiler natively understands exactly what a contiguous $1$D NumPy array (`.values`) is, and can map it directly to a C-pointer. However, it has absolutely no idea what a heavy, complex `pandas.Series` object is. If you pass a Pandas Series into a Numba function, Numba will violently crash because it mathematically cannot compile the Pandas internal object architecture into bare metal C-code."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (High-Performance Data Science) Completed.")
