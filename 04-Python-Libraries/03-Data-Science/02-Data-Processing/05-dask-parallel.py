"""
# ==============================================================================
# LABORATORY: OUT-OF-CORE PARALLELIZATION (DASK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Pandas is the undisputed king of Data Science, but it has a fatal, architectural 
# flaw: It is an "In-Memory, Eager" engine.
#
# If you try to execute `pd.read_csv("transactions.csv")` on a 50 Gigabyte CSV 
# file, Pandas will attempt to physically load all 50 GB into your laptop's RAM 
# at the exact same time. If you only have 16 GB of RAM, your Python process 
# will instantly crash with an `OutOfMemory` Exception.
#
# How do Data Scientists process terabytes of data? They use **Dask** (or PySpark).
# 
# Dask provides a `dask.dataframe` that looks and feels exactly like a Pandas 
# DataFrame, but operates radically differently:
# 1. Out-of-Core: It doesn't load the file. It chops the 50GB file into 500 tiny 
#    100MB chunks (partitions), streaming them one at a time from the hard drive.
# 2. Parallel: Because the data is chunked, Dask spins up 8 separate Python 
#    processes (bypassing the GIL) and processes 8 chunks simultaneously on all 
#    8 cores of your CPU.
# 3. Lazy Evaluation: It doesn't execute ANY math until you explicitly call `.compute()`.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Dask Partitions vs a single Pandas DataFrame.
# - Understand Task Graphs and Lazy Evaluation.
# - Execute massive aggregations using `.compute()`.
#
# ==============================================================================
"""

import pandas as pd
import numpy as np

# In a real environment: pip install dask[complete]
try:
    import dask.dataframe as dd
    HAS_DASK = True
except ImportError:
    HAS_DASK = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PANDAS VS DASK (PARTITIONS)
# ==============================================================================
def demonstrate_architecture():
    section_header("The Dask Partition Architecture")
    
    if not HAS_DASK:
        print("[WARNING] Dask is not installed. Skipping simulation.")
        print("Install using: pip install 'dask[complete]'")
        return
        
    print("Under the hood, a Dask DataFrame is physically just a list of tiny ")
    print("Pandas DataFrames (called Partitions) connected by an orchestrator.\n")
    
    # 1. CREATE A PANDAS DATAFRAME
    df_pandas = pd.DataFrame({
        "User": np.arange(1, 101),
        "Spend": np.random.uniform(10.0, 500.0, 100)
    })
    
    # 2. CONVERT IT TO DASK (Simulating reading a massive chunked file)
    # We explicitly tell Dask to physically cut the data into 4 chunks (partitions).
    df_dask = dd.from_pandas(df_pandas, npartitions=4)
    
    print("Pandas Type : ", type(df_pandas))
    print("Dask Type   : ", type(df_dask))
    print(f"Number of Dask Partitions: {df_dask.npartitions}")
    
    # We can literally extract and view one of the underlying Pandas partitions!
    first_partition = df_dask.partitions[0].compute()
    print("\nExtracting Partition #0 (A perfectly normal Pandas DataFrame!):")
    print(first_partition.head())


# ==============================================================================
# 4. LAZY EVALUATION & TASK GRAPHS
# ==============================================================================
def demonstrate_lazy_evaluation():
    section_header("Lazy Evaluation & Task Graphs")
    
    if not HAS_DASK:
        return
        
    df_pandas = pd.DataFrame({
        "User": np.arange(1, 100000),
        "Spend": np.random.uniform(10.0, 500.0, 99999)
    })
    df_dask = dd.from_pandas(df_pandas, npartitions=8)
    
    print("Let's ask Dask to calculate the Maximum Spend.")
    
    # PANDAS (Eager)
    # If we did this in Pandas, it would instantly loop through all 100k rows.
    
    # DASK (Lazy)
    max_spend = df_dask["Spend"].max()
    
    print("\nResult of df_dask['Spend'].max():")
    print(max_spend)
    print("Wait... it didn't print a number?!")
    
    print("\nExplanation:")
    print("Dask is LAZY. When you called `.max()`, it did absolutely ZERO math.")
    print("Instead, it instantly built a 'Task Graph' (a recipe):")
    print("1. Read Partition 1. Find the local max. Erase Partition 1 from RAM.")
    print("2. Read Partition 2. Find the local max. Erase Partition 2 from RAM.")
    print("3. Compare all 8 local maxes to find the Global Max.")
    
    # THE COMPUTE FUNCTION
    # Calling `.compute()` tells the orchestrator to execute the Task Graph 
    # using all 8 cores of your CPU in parallel!
    print("\nExecuting the Task Graph using .compute()...")
    actual_number = max_spend.compute()
    
    print(f"Final Global Max Spend: ${actual_number:.2f}")


# ==============================================================================
# 5. MASSIVE AGGREGATIONS
# ==============================================================================
def demonstrate_aggregations():
    section_header("Massive Out-Of-Core Aggregations")
    
    if not HAS_DASK:
        return
        
    # Simulating a massive clickstream dataset
    df_pandas = pd.DataFrame({
        "Country": np.random.choice(["USA", "UK", "Japan", "Brazil"], size=100_000),
        "Clicks": np.random.randint(1, 10, size=100_000)
    })
    df_dask = dd.from_pandas(df_pandas, npartitions=10)
    
    print("Objective: Group by Country and Sum the Clicks across 10 Partitions.")
    
    # 1. Build the recipe (Instant)
    lazy_groupby = df_dask.groupby("Country")["Clicks"].sum()
    
    # 2. Execute the recipe across all CPU cores (Compute)
    final_result = lazy_groupby.compute()
    
    print("\nAggregated Results:")
    print(final_result)


def run_all_labs():
    demonstrate_architecture()
    demonstrate_lazy_evaluation()
    demonstrate_aggregations()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Pandas crash when loading a 50GB file, but Dask does not?
   Answer: Pandas is an "In-Memory" engine. The `pd.read_csv()` function attempts to physically allocate a single contiguous 50GB block of RAM to hold the entire file simultaneously before returning control to the programmer. If the OS denies the memory request, it throws an OOM Exception. Dask is an "Out-Of-Core" engine. `dd.read_csv()` doesn't load the file at all. It scans the metadata and logically divides the file into 500 virtual chunks (e.g., 100MB each). When you execute a calculation, Dask streams exactly one 100MB chunk into RAM, calculates the local sub-total, and instantly deletes the 100MB chunk from RAM, never exceeding the hardware limits of the laptop.

2. What is Lazy Evaluation and a Task Graph?
   Answer: In Eager evaluation (Pandas), every line of code executes instantly and alters RAM. In Lazy evaluation (Dask), writing `df.max()` executes instantly in $0.0001$ seconds because it performs zero math. Instead, it generates a "Task Graph" (a mathematical blueprint or recipe of the required operations). This is brilliant because it allows the Dask compiler to mathematically optimize the entire script *before* running it. When you finally call `.compute()`, the orchestrator distributes the highly-optimized blueprint across the 8 physical cores of the CPU to execute in parallel.

3. If Dask is so much better, why don't we use it for everything?
   Answer: The Orchestration Overhead! Splitting data into 10 partitions, spinning up 10 independent Python multiprocessor threads, passing the data through the serialization bottlenecks (Pickle), and recombining the sub-totals takes roughly $1.0$ second of pure orchestrator overhead. If your dataset easily fits in RAM (e.g., a 10MB CSV), Pandas will execute the math natively in C in $0.01$ seconds. Dask would take 100x longer just spinning up the threads! You ONLY use Dask when Pandas physically fails due to OOM errors.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Dask Parallelization Completed.")
