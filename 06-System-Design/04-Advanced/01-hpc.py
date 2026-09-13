"""
High-Performance Computing (HPC) in Python

1. Module Description:
   This module explores High-Performance Computing (HPC) concepts in Python. It demonstrates
   how to bypass Python's Global Interpreter Lock (GIL) to fully utilize multi-core CPUs
   for computationally intensive tasks. HPC involves aggregating computing power to deliver 
   much higher performance than one could get out of a typical desktop computer or single 
   processor in order to solve large problems in science, engineering, or business.

2. Learning Objectives:
   - Understand the limitations of pure Python for CPU-bound tasks (e.g., the GIL).
   - Learn how to structure parallel tasks for multi-core execution.
   - Grasp the concepts of chunking and batching for optimal process pool utilization.
   - Analyze performance scaling and overheads associated with inter-process communication.

3. Concept Explanation:
   Python threads are subject to the Global Interpreter Lock (GIL), meaning only one thread
   can execute Python bytecode at a time. For I/O-bound tasks, threading is fine. However,
   for CPU-bound tasks, we must use multiple processes (each with its own Python interpreter
   and memory space). This brings in inter-process communication (IPC) overhead, so tasks
   must be coarse-grained enough that computation time heavily outweighs communication time.

4. Industry Use Cases:
   - Financial modeling and risk analysis (Monte Carlo simulations).
   - Bioinformatics (genome sequencing and folding).
   - Machine Learning data preprocessing.
   - Scientific simulations (fluid dynamics, particle physics).
"""

import time
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Tuple, List


# ---------------------------------------------------------------------------
# Basic Implementation: Single-Threaded CPU Bound Task
# ---------------------------------------------------------------------------
def calculate_pi_basic(num_samples: int) -> float:
    """
    Estimates the value of Pi using the Monte Carlo method.
    This is a basic, single-threaded implementation.
    
    Args:
        num_samples: Number of random points to generate.
        
    Returns:
        Estimated value of Pi.
    """
    points_inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            points_inside_circle += 1
            
    return 4.0 * points_inside_circle / num_samples


# ---------------------------------------------------------------------------
# Professional Implementation: High-Performance Multi-Processing Task
# ---------------------------------------------------------------------------
def _pi_worker(samples_chunk: int) -> int:
    """
    Worker function to be executed in a separate process.
    Must be defined at the top-level module scope for Windows compatibility.
    
    Args:
        samples_chunk: Number of samples this worker should process.
        
    Returns:
        Number of points that fell inside the unit circle.
    """
    points_inside = 0
    # Pre-fetching random speeds up the loop slightly
    rand = random.random
    for _ in range(samples_chunk):
        x = rand()
        y = rand()
        if x * x + y * y <= 1.0:
            points_inside += 1
    return points_inside


def calculate_pi_hpc(num_samples: int, num_workers: int = None) -> float:
    """
    Estimates the value of Pi using a parallelized Monte Carlo method.
    Distributes the workload across multiple CPU cores to bypass the GIL.
    
    Args:
        num_samples: Total number of random points to generate.
        num_workers: Number of parallel worker processes to use.
        
    Returns:
        Estimated value of Pi.
    """
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
        
    # Calculate chunk size per worker.
    # Chunking reduces inter-process communication overhead.
    samples_per_worker = num_samples // num_workers
    chunks = [samples_per_worker] * num_workers
    
    # Add remainder to the last chunk
    chunks[-1] += num_samples % num_workers
    
    total_inside = 0
    
    # ProcessPoolExecutor manages a pool of worker processes
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Map chunks to the worker function
        futures = [executor.submit(_pi_worker, chunk) for chunk in chunks]
        
        # Gather results as they complete
        for future in as_completed(futures):
            total_inside += future.result()
            
    return 4.0 * total_inside / num_samples


# ---------------------------------------------------------------------------
# Complexity Analysis & Interview Challenge
# ---------------------------------------------------------------------------
"""
Complexity Analysis:
- Time Complexity (Basic): O(N), where N is num_samples.
- Time Complexity (HPC): O(N / P) + O(P), where P is num_workers. The O(P) is IPC overhead.
- Space Complexity: O(1) beyond the Python process footprint, as we stream calculations.

Interview Challenge:
1. What happens if `num_samples` is extremely small (e.g., 1000) when using `calculate_pi_hpc`?
   Answer: The multiprocessing version will likely be slower than the basic version because 
   the overhead of spawning processes and IPC heavily outweighs the computation time.
   
2. Modify the `_pi_worker` to use NumPy arrays for vectorized computation to further 
   speed up single-core performance before parallelizing it.
"""


# ---------------------------------------------------------------------------
# Example Usage & Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- High-Performance Computing (HPC) ---")
    
    SAMPLES = 10_000_000
    
    print(f"Estimating Pi using {SAMPLES:,} samples...")
    
    # Basic Run
    start_time = time.time()
    pi_basic = calculate_pi_basic(SAMPLES)
    basic_duration = time.time() - start_time
    print(f"Basic Pi: {pi_basic} (Time: {basic_duration:.4f}s)")
    
    # HPC Run
    start_time = time.time()
    pi_hpc = calculate_pi_hpc(SAMPLES)
    hpc_duration = time.time() - start_time
    print(f"HPC Pi:   {pi_hpc} (Time: {hpc_duration:.4f}s)")
    
    speedup = basic_duration / hpc_duration if hpc_duration > 0 else 0
    print(f"Speedup multiplier: {speedup:.2f}x")
    
    # Simple assertions (Monte Carlo is stochastic, so we just check approximation bounds)
    assert 3.13 <= pi_basic <= 3.15, "Basic implementation failed accuracy check"
    assert 3.13 <= pi_hpc <= 3.15, "HPC implementation failed accuracy check"
    print("Tests passed successfully!")
