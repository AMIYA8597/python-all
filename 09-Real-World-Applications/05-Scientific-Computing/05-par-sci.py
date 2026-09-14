"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (PARALLEL SCIENTIFIC COMPUTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# An astrophysicist needs to run a highly complex black-hole simulation against 
# 1,000 different star masses. A junior developer writes a Python `for` loop, 
# sequentially passing each of the 1,000 masses into the simulation function. 
# It takes 40 hours to execute. They notice their $5,000 64-Core Threadripper 
# workstation is at 1.5% CPU utilization because Python's GIL forced the entire 
# workload onto a single physical CPU core.
#
# A senior Scientific Computing engineer understands "Embarrassingly Parallel" 
# architecture. They import `joblib`. In two lines of code, they mathematically 
# shatter the `for` loop, cloning the Python interpreter across all 64 physical 
# hardware cores. The 1,000 simulations are distributed symmetrically. The 
# 40-hour execution finishes in exactly 38 minutes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Multi-Processing architecture to bypass the Python GIL.
# - Execute Embarrassingly Parallel workloads using `joblib`.
# - Understand mathematical overhead and IPC (Inter-Process Communication).
#
# ==============================================================================
"""

import time
import timeit
import math
import multiprocessing

# Gracefully handle missing dependencies
try:
    from joblib import Parallel, delayed
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE HEAVY SCIENTIFIC SIMULATION (CPU BOUND)
# ==============================================================================
# This function is mathematically "CPU Bound". It does not wait for the network,
# it does not wait for the hard drive. It just aggressively burns CPU clock cycles
# doing raw, heavy floating-point mathematics.

def simulate_black_hole_physics(mass: float) -> float:
    """A mathematically heavy, arbitrary calculation simulating deep physics."""
    # We do a massive amount of useless math to simulate 0.1 seconds of heavy CPU load!
    result = mass
    for _ in range(3_000_000):
        # Taking the square root and multiplying burns massive CPU cycles
        result = math.sqrt(result * 1.0001)
    return result


# ==============================================================================
# 4. ARCHITECTURAL EXECUTION (SEQUENTIAL VS PARALLEL)
# ==============================================================================
def demonstrate_parallel_computing():
    section_header("Bypassing the GIL: Parallel Processing (Joblib)")
    
    if not HAS_JOBLIB:
        print("  [ERROR] Joblib is not installed. Run `pip install joblib`.")
        return
        
    print("  [SCENARIO] Executing heavy CPU-Bound physics simulation on 24 parameters.")
    
    # We define 24 parameters to simulate
    parameters = [float(i * 100) for i in range(1, 25)]
    
    # --- SCENARIO A: THE SEQUENTIAL CPYTHON LOOP ---
    print("\n  [SCENARIO A: THE SINGLE-CORE BOTTLENECK (Sequential)]")
    print("    -> Python is legally forced by the GIL to use exactly 1 CPU Core.")
    
    start_seq = timeit.default_timer()
    
    results_seq = []
    for mass in parameters:
        res = simulate_black_hole_physics(mass)
        results_seq.append(res)
        
    end_seq = timeit.default_timer()
    time_seq = end_seq - start_seq
    
    print(f"    -> Execution Time: {time_seq:.2f} seconds")


    # --- SCENARIO B: THE JOBLIB MULTI-PROCESSING INJECTION ---
    print("\n  [SCENARIO B: MULTI-CORE HARDWARE TAKEOVER (joblib)]")
    
    # We query the OS to find out how many physical hardware cores exist!
    physical_cores = multiprocessing.cpu_count()
    print(f"    -> Hardware detected: {physical_cores} CPU Cores available.")
    
    start_par = timeit.default_timer()
    
    # `Parallel` mathematically clones the Python Interpreter into X separate OS Processes.
    # Because they are separate OS Processes, the GIL is completely bypassed!
    # `delayed` is a decorator that prevents the function from executing instantly, 
    # allowing Joblib to carefully distribute the pointers across the CPUs!
    
    results_par = Parallel(n_jobs=-1)(
        delayed(simulate_black_hole_physics)(mass) for mass in parameters
    )
    
    end_par = timeit.default_timer()
    time_par = end_par - start_par
    
    print(f"    -> Execution Time: {time_par:.2f} seconds")
    
    
    # --- CONCLUSION ---
    if time_par > 0:
        speedup = time_seq / time_par
        print(f"\n  [CONCLUSION] Mathematical Speedup: {speedup:.1f}x faster!")
        print("  By changing exactly two words (`Parallel` and `delayed`), we achieved")
        print("  a massive architectural hardware victory.")


def run_all_labs():
    demonstrate_parallel_computing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why didn't we use Python's built-in `threading` module to execute the 24 physics simulations? Threads are much lighter than full OS Processes."
   Senior Answer: "The Python GIL (Global Interpreter Lock). The GIL is a C-level Mutex (Mutual Exclusion lock) that mathematically guarantees that only ONE Thread can execute Python bytecode at any given millisecond. If we spin up $24$ Python Threads to do heavy math, the OS will put all $24$ threads on a single CPU core, and they will violently fight each other for the GIL. The execution time will actually be *slower* than the sequential `for` loop due to Thread Context Switching overhead. To achieve true hardware parallelism for CPU-Bound math, we must use OS-level 'Multi-Processing' (`joblib` with `n_jobs=-1`). This spins up $24$ completely independent Python executables in RAM, each with their own isolated GIL, allowing the OS to physically map them to all $24$ hardware cores."

2. Interviewer: "What is an 'Embarrassingly Parallel' workload, and why was the physics simulation the perfect candidate for it?"
   Senior Answer: "An Embarrassingly Parallel workload is an algorithm where the individual tasks mathematically share absolutely zero state with each other. In our scenario, simulating Star Mass #1 has absolutely zero mathematical dependency on the outcome of Star Mass #2. Because they don't need to communicate, we can flawlessly distribute them across 64 cores without worrying about Race Conditions, Deadlocks, or expensive Inter-Process Communication (IPC). If Star #2's math required the answer from Star #1, it would be a sequential dependency, breaking the parallel architecture."

3. Interviewer: "If `joblib` is so fast, why don't we wrap every single `for` loop in our web server with `Parallel(n_jobs=-1)`?"
   Senior Answer: "Architectural Overhead (The IPC Penalty). Spinning up a new Python OS Process is violently expensive. The Operating System must allocate a brand new block of RAM, boot a fresh CPython Interpreter, and serialize (Pickle) the target function and arguments across an Inter-Process socket. If the `for` loop only takes $0.05$ seconds to execute sequentially, `joblib` will take $1.5$ seconds just to boot the worker processes and transmit the data. You mathematically LOSE performance. Parallel Multi-Processing is strictly reserved for massive, heavy mathematical functions where the execution time (e.g., $5$ minutes per loop) vastly eclipses the $1.5$-second architectural setup penalty."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scientific Computing (Parallel Processing) Completed.")
