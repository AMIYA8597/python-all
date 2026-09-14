"""
# ==============================================================================
# LABORATORY: PERFORMANCE AND OPTIMIZATION (PARALLEL ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have a list of 100,000,000 numbers and you need to compute the sum, find 
# the maximum, or execute a Map-Reduce operation. 
#
# A junior engineer runs a single `for` loop, maxing out Core 0 while Cores 
# 1 through 15 sit at 0% utilization. The script takes 60 seconds.
#
# A senior engineer understands "Divide and Conquer" mathematics. They shatter 
# the 100,000,000 elements into 16 perfectly equal chunks. They deploy 16 
# isolated OS processes. The 16 cores independently process their chunks in 
# parallel, returning 16 sub-answers. The senior engineer combines the sub-answers 
# into the final result, collapsing the execution time from 60 seconds to 4 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Divide and Conquer (Map-Reduce) parallel architecture.
# - Prove the CPU limits of multi-core processing.
# - Analyze the overhead of Data Sharding.
#
# ==============================================================================
"""

import math
import timeit
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE HEAVY MAP-REDUCE PAYLOAD
# ==============================================================================
def heavy_computation_chunk(chunk: list) -> float:
    """
    Simulates a mathematically brutal operation on a massive chunk of data.
    e.g., Applying a complex pricing algorithm to historical stock data.
    """
    sub_total = 0.0
    for num in chunk:
        # We artificially inflate the math to guarantee CPU bound execution
        sub_total += math.sqrt(num) * math.sin(num)
    return sub_total


# ==============================================================================
# 4. MATHEMATICAL DATA SHARDING (DIVIDE AND CONQUER)
# ==============================================================================
def execute_parallel_algorithm():
    section_header("Performance Proof: Parallel Map-Reduce")
    
    # 20 Million Data Points!
    TOTAL_DATA = 20_000_000
    print(f"  [INIT] Generating {TOTAL_DATA:,} data points...")
    
    # In reality, this would be a massive array, but we will use a range to save RAM
    # during generation. We convert it to a list to simulate a physical dataset.
    dataset = list(range(TOTAL_DATA))
    
    # --- SCENARIO A: SEQUENTIAL (1 CORE) ---
    print("\n  [SCENARIO A: SEQUENTIAL PROCESSING (1 Core)]")
    start_seq = timeit.default_timer()
    
    # The single core takes the entire dataset!
    result_seq = heavy_computation_chunk(dataset)
    
    end_seq = timeit.default_timer()
    time_seq = end_seq - start_seq
    print(f"    -> Final Result: {result_seq:.4f}")
    print(f"    -> Time Taken:   {time_seq:.4f} seconds")
    
    # --- SCENARIO B: PARALLEL MAP-REDUCE (8 CORES) ---
    print("\n  [SCENARIO B: PARALLEL MAP-REDUCE (N Cores)]")
    start_par = timeit.default_timer()
    
    # Step 1: Divide (Sharding)
    # We dynamically read the CPU hardware to determine the perfect shard count!
    CORES = min(8, multiprocessing.cpu_count()) 
    print(f"    -> Sharding data across {CORES} CPU Cores...")
    
    chunk_size = math.ceil(TOTAL_DATA / CORES)
    chunks = []
    
    # We mathematically slice the massive dataset into perfect chunks!
    for i in range(CORES):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, TOTAL_DATA)
        chunks.append(dataset[start_idx:end_idx])
    
    # Step 2: Map (Parallel Processing)
    # We broadcast the chunks to the independent isolated Python processes!
    with ProcessPoolExecutor(max_workers=CORES) as executor:
        # `executor.map` guarantees the sub-answers return in the exact order!
        sub_answers = list(executor.map(heavy_computation_chunk, chunks))
        
    # Step 3: Reduce (Aggregation)
    # We combine the sub-answers on the Master Process!
    final_result_par = sum(sub_answers)
    
    end_par = timeit.default_timer()
    time_par = end_par - start_par
    
    print(f"    -> Final Result: {final_result_par:.4f}")
    print(f"    -> Time Taken:   {time_par:.4f} seconds")
    
    speedup = time_seq / time_par
    print(f"\n  [CONCLUSION] The Parallel Map-Reduce achieved a {speedup:.1f}x hardware speedup!")
    
    # Validate mathematical integrity!
    if math.isclose(result_seq, final_result_par, rel_tol=1e-9):
        print("  [INTEGRITY CHECK] PASS: The parallel math perfectly matches the sequential math.")
    else:
        print("  [INTEGRITY CHECK] FAIL: Precision mismatch.")


def run_all_labs():
    if __name__ == '__main__':
        pass

# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the 'Map-Reduce' architecture, and why is it mandatory for scaling CPU workloads across multi-core systems?"
   Senior Answer: "Map-Reduce is a paradigm consisting of three mathematical phases: Divide, Map, and Reduce. First, you 'Divide' a massive dataset (e.g., $10$ GB of logs) into isolated shards ($1$ GB each). Second, you 'Map' (broadcast) those shards to independent worker processes (or distributed physical servers). The workers compute their sub-answers in $100\\%$ parallel isolation without any shared memory locking or GIL contention. Finally, the Master node 'Reduces' (aggregates) the sub-answers (e.g., summing $10$ sub-totals into the final total). It is mandatory because it is the only architecture that mathematically guarantees linear horizontal scaling (adding more cores directly equates to faster processing) without triggering synchronization bottlenecks."

2. Interviewer: "Why did we use `math.ceil` when slicing the dataset into chunks?"
   Senior Answer: "When sharding data, the total length is rarely perfectly divisible by the number of CPU cores. If you have $105$ elements and $4$ cores, integer division (`105 // 4`) yields chunks of $26$. $26 \\times 4 = 104$. The $105^{th}$ element is mathematically orphaned and excluded from the computation, destroying the integrity of the data! By using `math.ceil(105 / 4)`, we guarantee chunks of $27$. Cores $1, 2,$ and $3$ process $27$ elements, and Core $4$ processes the remaining $24$, ensuring $100\\%$ data coverage."

3. Interviewer: "In the Parallel test, why did an $8$-core system achieve a $6x$ speedup instead of a perfect $8.0x$ speedup?"
   Senior Answer: "A perfect $1:1$ linear speedup is a theoretical mathematical myth due to 'Amdahl's Law' and IPC overhead. While the heavy 'Map' computation happens in pure parallel, the 'Divide' (slicing the massive array) and the 'Reduce' (summing the final answers) are strictly sequential operations executed on a single core. Furthermore, streaming Gigabit-sized data chunks across the OS memory boundaries to child processes requires Serialization (Pickling). The time spent sequentially slicing, pickling, and unpickling permanently degrades the theoretical maximum speedup. This is why Map-Reduce is only utilized on datasets massive enough to mathematically dwarf the IPC serialization tax."
"""

if __name__ == "__main__":
    multiprocessing.freeze_support()
    execute_parallel_algorithm()
    print("\n[SUCCESS] Laboratory: Concurrency (Parallel Algorithms) Completed.")
