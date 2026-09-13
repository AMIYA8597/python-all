"""
# ==============================================================================
# LABORATORY: DISTRIBUTED ALGORITHMS (DASK & TASK GRAPHS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Python's `multiprocessing` library can bypass the GIL and 
# use all 16 cores on your computer.
#
# But what happens when your algorithm requires processing a 100 Gigabyte CSV 
# file? Your computer only has 16 GB of RAM. The Operating System will physically 
# crash with an Out-Of-Memory (OOM) error before you can even run the algorithm.
# 
# What if your algorithm requires 5,000 CPU cores to finish in time? You cannot 
# physically buy a CPU with 5,000 cores.
#
# The Solution: Distributed Computing (DASK / APACHE SPARK).
# Instead of scaling UP (buying a bigger CPU), we scale OUT (buying 1,000 cheap 
# computers and linking them over a network).
#
# Dask is the modern standard for distributed Python algorithms.
# How does it solve the 100GB RAM limit?
# LAZY EVALUATION and TASK GRAPHS (DAGs).
# 
# When you tell Dask to read a 100GB file and sort it, Dask actually does NOTHING. 
# It instantly returns a "Promise". It builds a Directed Acyclic Graph (DAG) in 
# memory representing the mathematical steps required to sort the data.
# 
# Only when you explicitly call `.compute()` does the engine execute! 
# It intelligently reads the 100GB file in tiny 100MB chunks, streams them 
# across the network to 50 different computers, sorts them individually, and 
# aggregates the answer back to your master script. Your laptop never exceeds 
# 1 GB of RAM usage!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Lazy Evaluation vs Eager Evaluation.
# - Understand Directed Acyclic Graphs (DAGs) for Task Scheduling.
# - Conceptually master Distributed Out-Of-Core algorithms.
#
# ==============================================================================
"""

import time
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MOCKING A DISTRIBUTED TASK GRAPH
# ==============================================================================
# Note: Since this repository cannot assume the user has a 50-node Dask cluster 
# or the `dask` library installed locally, we will physically build the 
# Architecture of a Task Graph to prove how Lazy Evaluation works under the hood!

class DelayedTask:
    """
    A mathematical 'Promise'. 
    It stores the function and arguments, but DOES NOT RUN them yet!
    """
    def __init__(self, func, *args):
        self.func = func
        self.args = args
        
    def compute(self) -> Any:
        """
        Recursively resolves all dependencies in the Task Graph (DAG) and 
        finally executes the physical code!
        """
        # If any of the arguments are ALSO DelayedTasks, we must compute them first!
        # This perfectly simulates traversing a Dependency Graph (Post-Order Traversal).
        resolved_args = []
        for arg in self.args:
            if isinstance(arg, DelayedTask):
                resolved_args.append(arg.compute())
            else:
                resolved_args.append(arg)
                
        # Now that all dependencies are resolved, run the actual math!
        return self.func(*resolved_args)


def delay(func):
    """
    A Decorator that converts Eager Python functions into Lazy Dask Promises.
    """
    def wrapper(*args):
        return DelayedTask(func, *args)
    return wrapper


# ==============================================================================
# 4. ALGORITHMIC FUNCTIONS (LAZY vs EAGER)
# ==============================================================================
def heavy_math(x: int) -> int:
    """Simulates a heavy algorithmic operation."""
    time.sleep(0.1) # 100ms processing delay
    return x * x

def heavy_aggregate(x: int, y: int) -> int:
    """Simulates a distributed merge (like combining chunks in parallel sort)."""
    time.sleep(0.1)
    return x + y

# Wrap them in our Dask architecture!
lazy_heavy_math = delay(heavy_math)
lazy_heavy_aggregate = delay(heavy_aggregate)


def demonstrate_distributed_graphs():
    section_header("Algorithm: Eager Evaluation (Standard Python)")
    
    print("Executing 4 heavy math operations EAGERLY...")
    start = time.time()
    
    # Python physically stops and runs each line instantly!
    res1 = heavy_math(10)
    res2 = heavy_math(20)
    res3 = heavy_math(30)
    res4 = heavy_math(40)
    
    final_res = heavy_aggregate(heavy_aggregate(res1, res2), heavy_aggregate(res3, res4))
    
    eager_time = time.time() - start
    print(f"Final Result: {final_res}")
    print(f"Time Taken  : {eager_time:.2f} seconds (Blocked completely!)")
    
    
    section_header("Algorithm: Lazy Evaluation (Dask Task Graph)")
    
    print("Building the Distributed Task Graph LAZILY...")
    start = time.time()
    
    # Python does NOT run the math! It instantly creates 4 Promise objects!
    prom1 = lazy_heavy_math(10)
    prom2 = lazy_heavy_math(20)
    prom3 = lazy_heavy_math(30)
    prom4 = lazy_heavy_math(40)
    
    # We aggregate the Promises into a Master Promise!
    agg1 = lazy_heavy_aggregate(prom1, prom2)
    agg2 = lazy_heavy_aggregate(prom3, prom4)
    master_promise = lazy_heavy_aggregate(agg1, agg2)
    
    lazy_time = time.time() - start
    
    print(f"Graph Built in: {lazy_time:.5f} seconds! (Instantaneous)")
    print(f"Master Type   : {type(master_promise)}")
    
    print("\nSending the Task Graph to the Cluster (Calling `.compute()`)....")
    compute_start = time.time()
    
    # We trigger the mathematical resolution of the graph!
    final_res_lazy = master_promise.compute()
    compute_time = time.time() - compute_start
    
    print(f"Final Result  : {final_res_lazy}")
    print(f"Compute Time  : {compute_time:.2f} seconds")
    
    print("\nObservation:")
    print("Because we built a Task Graph first, a true Distributed Engine like ")
    print("Dask can look at the Graph and realize that `prom1`, `prom2`, `prom3`, ")
    print("and `prom4` have absolutely NO mathematical dependencies on each other!")
    print("The engine will instantly ship those 4 tasks to 4 different computers ")
    print("across the network, execute them in parallel, and ship the results back.")
    print("If you execute eagerly, Python forces a sequential 1-by-1 execution.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is an Out-Of-Core Algorithm?
   Answer: When dealing with massive datasets (e.g., 100 GB files) on a computer with only 16 GB of RAM, you cannot load the file into memory (Pandas will crash). An Out-Of-Core algorithm streams the data from the hard drive in tiny chunks (e.g., 100 MB), processes the chunk, updates an accumulator, and throws the chunk out of RAM before loading the next one. Dask fully automates this chunking mechanism.

2. Why is a Directed Acyclic Graph (DAG) required for Distributed Computing?
   Answer: To execute code across 50 different physical computers, the Master Node needs to know exactly which tasks can be run simultaneously without corrupting the data. By building a mathematical DAG (a flowchart of operations), the Master Node can instantly identify dependencies. If Node A and Node B do not have an arrow connecting them, they are 100% mathematically independent and can be safely assigned to different computers in the cluster!

3. Why do we wait to call `.compute()`?
   Answer: Optimization! If you eagerly execute `data.filter().sort().head(5)`, the engine might fully sort 1 Billion rows just to give you the top 5. By delaying execution and building the Task Graph first, the Dask Engine can analyze the ENTIRE sequence of requests before starting. It will mathematically rearrange the graph, pushing the `.head(5)` logic upstream, and only sorting the bare minimum data required to satisfy the final query, saving hours of distributed compute time!
"""

if __name__ == "__main__":
    demonstrate_distributed_graphs()
    print("\n[SUCCESS] Laboratory: Distributed Task Graphs Completed.")
    print("\n[CAPSTONE] THE PYTHON CURRICULUM IS FULLY COMPLETED.")
