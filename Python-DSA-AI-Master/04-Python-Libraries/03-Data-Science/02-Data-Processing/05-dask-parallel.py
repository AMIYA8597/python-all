"""
Module: 05-dask-parallel
Description: Comprehensive textbook-grade interactive lesson on Parallel Data Processing with Dask.

Learning Objectives:
1. Understand the core concepts of parallel and distributed computing in Python.
2. Master Dask Delayed, Dask Array, and Dask DataFrame.
3. Learn how Dask creates and executes task graphs (DAGs).
4. Analyze mathematical principles of parallelism (Amdahl's Law, Gustafson's Law).
5. Apply Dask to real-world large-scale data processing scenarios.

-------------------------------------------------------------------------------
Mathematical Background: The Laws of Parallelism
-------------------------------------------------------------------------------
When designing parallel data processing systems, two critical laws govern the
theoretical speedup you can achieve.

1. Amdahl's Law:
   Amdahl's Law focuses on fixed workloads and predicts the theoretical maximum
   speedup using multiple processors.
   
   S(s) = 1 / ((1 - p) + (p / s))
   
   Where:
   - S(s) is the theoretical speedup.
   - p is the proportion of the execution time that can be parallelized.
   - 1 - p is the proportion of the execution time that is strictly serial.
   - s is the speedup of the parallelized part (typically the number of cores).

   Implication: No matter how many cores you add, the maximum speedup is bottlenecked
   by the serial portion of the code.

2. Gustafson's Law:
   Gustafson's Law shifts the perspective to scaled workloads, assuming that as you
   gain more computing power, you will process larger datasets, keeping the execution
   time constant.

   S(s) = (1 - p) + s * p

   Where:
   - p is the proportion of parallel time.
   - s is the number of processors.

-------------------------------------------------------------------------------
Big-O Analysis & Computational Complexity
-------------------------------------------------------------------------------
In parallel computing, we analyze Work (W) and Span (Depth, D).

- Work, W(n): Total number of operations required by all processors.
  Example (Matrix Multiplication): O(n^3)
- Span, D(n): The longest path of dependent operations in the task graph (critical path).
  Example (Matrix Multiplication using parallel divide & conquer): O(log^2 n)
  
Speedup on P processors is bounded by:
T_P = O(W/P + D)

With Dask, constructing the task graph introduces an overhead of O(E + V), where E is the
number of dependencies and V is the number of tasks. For performance, tasks should be
granulated such that the execution time of each task vastly outweighs the graph building cost (usually > 100ms per task).

-------------------------------------------------------------------------------
Modern Type Hints & Real-World Context
-------------------------------------------------------------------------------
This module makes extensive use of Python's `typing` module to ensure robustness.
We simulate massive datasets using normal data structures, applying Dask's lazy 
evaluation to realize theoretical principles in actionable Python code.
"""

import time
import math
import random
from typing import List, Dict, Any, Callable, Tuple, Optional

# Attempt to import dask, gracefully failing if it's not installed,
# as this is an educational script meant to run anywhere.
try:
    import dask
    import dask.delayed as delayed
    import dask.array as da
    import dask.dataframe as dd
    import pandas as pd
    import numpy as np
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    print("Warning: Dask, Pandas, or Numpy is not installed. Some features will be mocked.")


# =============================================================================
# 1. Theoretical Analysis: Amdahl's and Gustafson's Laws
# =============================================================================
def calculate_amdahls_law(parallel_fraction: float, num_processors: int) -> float:
    """
    Calculates theoretical speedup based on Amdahl's Law.
    
    Args:
        parallel_fraction (float): The portion of the program that can be parallelized (0.0 to 1.0).
        num_processors (int): The number of processors/cores available.
        
    Returns:
        float: The theoretical maximum speedup.
        
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    if not (0.0 <= parallel_fraction <= 1.0):
        raise ValueError("Parallel fraction must be between 0.0 and 1.0")
    if num_processors < 1:
        raise ValueError("Number of processors must be at least 1")
        
    serial_fraction = 1.0 - parallel_fraction
    speedup = 1.0 / (serial_fraction + (parallel_fraction / num_processors))
    return speedup


# =============================================================================
# 2. Dask Delayed: Lazy Evaluation and Task Graphs
# =============================================================================
def simulate_cpu_bound_task(data: int, cost_ms: int = 100) -> int:
    """
    A simulated CPU-bound task that takes `cost_ms` milliseconds to run.
    """
    time.sleep(cost_ms / 1000.0)
    # Arbitrary math operation to simulate work
    return int(math.factorial(data % 10) + data)

def demonstrate_dask_delayed(data_list: List[int]) -> Tuple[float, float, Any]:
    """
    Demonstrates lazy evaluation and parallel execution using dask.delayed.
    
    Instead of executing functions immediately, dask.delayed wraps them to construct
    a Directed Acyclic Graph (DAG) of tasks. The DAG is evaluated only when 
    `.compute()` is called.
    
    Args:
        data_list (List[int]): Input integers to process.
        
    Returns:
        Tuple[float, float, Any]: Serial execution time, Parallel execution time, and results.
    """
    print("\n--- Demonstrating Dask Delayed (Lazy Evaluation) ---")
    
    if not DASK_AVAILABLE:
        print("Dask not available. Skipping Dask Delayed demo.")
        return 0.0, 0.0, []

    # 1. Serial Execution (Synchronous)
    start_serial = time.time()
    serial_results = []
    for item in data_list:
        # Each item takes ~100ms
        res = simulate_cpu_bound_task(item, cost_ms=100)
        serial_results.append(res)
    end_serial = time.time()
    serial_duration = end_serial - start_serial

    # 2. Parallel Execution (Dask Delayed)
    start_parallel = time.time()
    lazy_results = []
    for item in data_list:
        # dask.delayed builds the computation graph without executing it
        lazy_res = delayed(simulate_cpu_bound_task)(item, cost_ms=100)
        lazy_results.append(lazy_res)
    
    # Execute the graph in parallel using Dask's default thread pool
    parallel_results = dask.compute(*lazy_results)
    end_parallel = time.time()
    parallel_duration = end_parallel - start_parallel

    print(f"Serial Execution Time:   {serial_duration:.4f}s")
    print(f"Parallel Execution Time: {parallel_duration:.4f}s")
    print(f"Speedup Factor:          {serial_duration / parallel_duration:.2f}x")
    
    return serial_duration, parallel_duration, parallel_results


# =============================================================================
# 3. Dask Arrays: Scalable Multi-dimensional Arrays
# =============================================================================
def demonstrate_dask_array() -> None:
    """
    Demonstrates Dask Arrays, which coordinate many Numpy arrays arranged into a grid.
    They support out-of-core computing, meaning they can process datasets larger
    than available RAM by loading chunks iteratively.
    """
    print("\n--- Demonstrating Dask Arrays (Parallel Numpy) ---")
    if not DASK_AVAILABLE:
        print("Dask not available. Skipping Dask Array demo.")
        return

    # Create a massive simulated array of 10,000 x 10,000 random numbers (~800MB in RAM)
    # Using chunks (1000, 1000), Dask breaks this into 100 independent numpy arrays.
    print("Initializing a 10,000 x 10,000 Dask Array with chunk size (1000, 1000)...")
    darr = da.random.random((10000, 10000), chunks=(1000, 1000))
    
    print(f"Dask Array Object: {darr}")
    print(f"Total Array Size (Bytes): {darr.nbytes}")
    print(f"Chunk Size (Bytes): {darr.chunks[0][0] * darr.chunks[1][0] * 8}") # 8 bytes per float64
    
    # Chain computations (Lazy)
    # O(N) operations where N is the total number of elements.
    print("Constructing computation graph (Mean, Std Dev, and Matrix Transformation)...")
    transformed = (darr * 2) - darr.mean(axis=0)
    final_result_lazy = transformed.std()

    # Trigger computation
    print("Computing task graph (out-of-core, parallelized across cores)...")
    start_time = time.time()
    result = final_result_lazy.compute()
    end_time = time.time()
    
    print(f"Computed Standard Deviation: {result:.4f}")
    print(f"Computation Time: {end_time - start_time:.4f}s")


# =============================================================================
# 4. Real-world Application: Big Data Log Processing Simulation
# =============================================================================
def process_log_files() -> None:
    """
    Simulates processing large log files using Dask Dataframes.
    Dask Dataframes parallelize Pandas operations across cores or clusters.
    """
    print("\n--- Real-World Application: Log Processing Pipeline ---")
    if not DASK_AVAILABLE:
        print("Dask/Pandas not available. Skipping Dask DataFrame demo.")
        return
        
    # Simulate generating a large CSV locally using Pandas
    print("Generating simulated log data (100,000 rows)...")
    num_rows = 100000
    df = pd.DataFrame({
        'timestamp': pd.date_range('2026-01-01', periods=num_rows, freq='S'),
        'user_id': np.random.randint(1, 1000, num_rows),
        'endpoint': np.random.choice(['/home', '/api/data', '/login', '/logout', '/settings'], num_rows),
        'response_time_ms': np.random.exponential(50, num_rows)
    })
    
    # In a real scenario, this would be `dd.read_csv('logs_*.csv')`
    # We partition the Pandas DataFrame into a Dask DataFrame with 4 partitions
    ddf = dd.from_pandas(df, npartitions=4)
    
    print(f"Dask DataFrame Partitions: {ddf.npartitions}")
    
    # Analytics task: Find the 95th percentile response time for each endpoint
    # This involves GroupBy and Quantile operations which require complex shuffling in distributed systems
    print("Constructing Map-Reduce analytics query...")
    
    # Task Graph Definition (Lazy)
    grouped = ddf.groupby('endpoint')['response_time_ms']
    # .quantile is an expensive operation that Dask optimizes using approximate algorithms
    p95_lazy = grouped.quantile(0.95)
    
    print("Executing query across partitions...")
    start = time.time()
    p95_result = p95_lazy.compute()
    end = time.time()
    
    print(f"Query Execution Time: {end - start:.4f}s")
    print("\n95th Percentile Response Time per Endpoint (ms):")
    for endpoint, val in p95_result.items():
        print(f"  {endpoint}: {val:.2f} ms")


# =============================================================================
# 5. Interview Challenge: Task Graph Dependency Traversal
# =============================================================================
class SimulatedDaskTask:
    """
    Represents a task node in a Directed Acyclic Graph (DAG) typical of Dask.
    """
    def __init__(self, name: str, func: Callable, args: List['SimulatedDaskTask'] = None):
        self.name = name
        self.func = func
        self.args = args or []
        self._cached_result = None
        self._computed = False

    def compute(self) -> Any:
        """
        Recursively computes the dependencies (DFS on the task graph) 
        and evaluates this task. Memorization ensures each node computes once.
        
        Time Complexity: O(V + E) where V is vertices, E is edges.
        Space Complexity: O(V) for the recursion stack and caching.
        """
        if self._computed:
            return self._cached_result
            
        print(f"  [Task Engine] Executing {self.name}...")
        
        # Recursively evaluate dependencies
        resolved_args = [arg.compute() for arg in self.args]
        
        # Execute this node's logic
        self._cached_result = self.func(*resolved_args)
        self._computed = True
        return self._cached_result

def interview_challenge_task_graph() -> None:
    """
    Common systems design/algorithms interview challenge:
    Implement a miniature version of Dask's task scheduler that traverses
    and executes a DAG (Directed Acyclic Graph) of operations.
    """
    print("\n--- Interview Challenge: Build a Miniature DAG Scheduler ---")
    
    # Define atomic operations
    def add(x, y): return x + y
    def mul(x, y): return x * y
    def load_data(): return 10
    def get_coefficient(): return 5
    
    # Build the task graph (DAG)
    # Formula: Result = (Data * Coefficient) + Data
    
    # Leaf nodes (Dependencies)
    node_data = SimulatedDaskTask("LoadData", load_data)
    node_coeff = SimulatedDaskTask("LoadCoefficient", get_coefficient)
    
    # Intermediate nodes
    node_mul = SimulatedDaskTask("Multiply", mul, [node_data, node_coeff])
    
    # Root node
    node_add = SimulatedDaskTask("Add", add, [node_mul, node_data])
    
    print("Task graph constructed. Triggering compute on Root Node (Add)...")
    final_result = node_add.compute()
    
    print(f"Graph Computation Result: {final_result}")
    assert final_result == (10 * 5) + 10, "DAG Scheduler failed!"
    print("DAG Scheduler test passed.")


# =============================================================================
# 6. Test Suite and Executions
# =============================================================================
def run_tests() -> None:
    """
    Validates mathematical models and theoretical frameworks.
    """
    print("\n--- Running Tests ---")
    
    # Test Amdahl's Law calculations
    # If 50% is parallelizable and we have 2 cores
    # Speedup = 1 / ((1-0.5) + (0.5/2)) = 1 / (0.5 + 0.25) = 1 / 0.75 = 1.333...
    speedup = calculate_amdahls_law(0.5, 2)
    assert math.isclose(speedup, 1.3333333333333333), f"Amdahl calculation failed: {speedup}"
    
    # If 100% is parallelizable, speedup should equal number of processors
    assert math.isclose(calculate_amdahls_law(1.0, 4), 4.0), "Amdahl perfect parallel failed"
    
    print("Mathematical assertion tests passed successfully.")


if __name__ == "__main__":
    print("=======================================================================")
    print("  PYTHON DSA & AI MASTER: PARALLEL DATA PROCESSING WITH DASK")
    print("=======================================================================\n")
    
    print("Dask extends standard Python APIs (NumPy, Pandas, Lists) to scale")
    print("from single-core local execution to thousand-node distributed clusters.")
    
    # 1. Theoretical Foundations
    print("\n[Section 1: Theoretical Parallelism (Amdahl's Law)]")
    s = calculate_amdahls_law(0.9, 10)
    print(f"With 90% parallelizable code and 10 cores, theoretical speedup is {s:.2f}x")
    
    # 2. Dask Delayed (Lazy Evaluation)
    print("\n[Section 2: Dask Delayed - Task Graphs]")
    demonstrate_dask_delayed([1, 2, 3, 4, 5, 6, 7, 8])
    
    # 3. Dask Array
    print("\n[Section 3: Dask Array - Scalable Matrices]")
    demonstrate_dask_array()
    
    # 4. Dask DataFrame
    print("\n[Section 4: Dask DataFrame - Out-of-core Analytics]")
    process_log_files()
    
    # 5. Interview Challenge (Mini Scheduler)
    print("\n[Section 5: Systems Design Challenge]")
    interview_challenge_task_graph()
    
    # 6. Unit Tests
    run_tests()
    
    print("\n=======================================================================")
    print("  END OF LESSON: 05-DASK-PARALLEL")
    print("=======================================================================\n")
