"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (BIG DATA & DISTRIBUTED COMPUTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer is tasked with analyzing 500 Gigabytes of server logs. They 
# confidently import `pandas`. When they execute `pd.read_csv`, the Pandas engine 
# attempts to load all 500 GB into their laptop's 16 GB of RAM. The Operating 
# System violently terminates the Python process with an OOM (Out Of Memory) crash.
#
# A senior Big Data Engineer understands "Distributed Computing". They import 
# `pyspark`. Instead of executing on a single laptop, the Spark framework 
# mathematically partitions the 500 GB dataset into 10,000 microscopic chunks. 
# It orchestrates 50 separate physical AWS servers (a Cluster) to process the 
# chunks in parallel. The entire 500 GB dataset is analyzed, aggregated, and 
# reduced to a 1 KB result in 45 seconds, mathematically immune to RAM limits.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architectural difference between Single-Node (Pandas) and 
#   Distributed Multi-Node (PySpark).
# - Understand the Resilient Distributed Dataset (RDD) and DataFrame API.
# - Master Lazy Evaluation in Big Data pipelines.
#
# ==============================================================================
"""

import timeit
import os

# Gracefully handle missing pyspark dependency
try:
    from pyspark.sql import SparkSession
    import pyspark.sql.functions as F
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False
    
def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DISTRIBUTED ARCHITECTURE (PYSPARK SIMULATION)
# ==============================================================================
def demonstrate_big_data_pipeline():
    section_header("The Distributed Pipeline (PySpark DataFrame API)")
    
    if not HAS_PYSPARK:
        print("  [ERROR] PySpark is not installed.")
        print("  Run `pip install pyspark` to execute this lab locally (Single-Node Mode).")
        return
        
    print("  [INIT] Booting the Spark JVM (Java Virtual Machine) Engine...")
    print("  (In production, this connects to a massive Cluster of 50 servers!)")
    
    # We must suppress the massive Java logging output for the lab
    os.environ['SPARK_HOME'] = "" 
    os.environ['PYSPARK_PYTHON'] = "python"
    
    start_boot = timeit.default_timer()
    spark = SparkSession.builder \
        .appName("Laboratory_BigData") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.ui.showConsoleProgress", "false") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("ERROR")
    end_boot = timeit.default_timer()
    print(f"    -> Spark Cluster (Local Mode) Online in {end_boot - start_boot:.2f} seconds.")


    # --- 1. EXTRACT (Lazy Data Loading) ---
    print("\n  [PHASE 1: EXTRACTION (Lazy Loading)]")
    # We will dynamically generate a massive list of records in memory to simulate 
    # a giant Parquet/CSV file. (1,000,000 records)
    records = [{"server_id": f"srv-{i%10}", "error_code": 500 if i % 7 == 0 else 200, "bytes": i % 1024} for i in range(1_000_000)]
    
    print("    -> Distributing 1,000,000 records across the Cluster nodes...")
    # This mathematically fragments the data across the CPU cores (Partitions)
    df = spark.createDataFrame(records)
    print(f"    -> Partitions generated: {df.rdd.getNumPartitions()} (Chunks of data)")


    # --- 2. TRANSFORM (Lazy Evaluation) ---
    print("\n  [PHASE 2: TRANSFORMATION (Building the DAG)]")
    # Unlike Pandas, executing these commands does absolutely NOTHING!
    # Spark is mathematically constructing a DAG (Directed Acyclic Graph) of operations.
    
    # We want to find the total bytes transferred by servers that threw 500 errors.
    transformed_df = df.filter(F.col("error_code") == 500) \
                       .groupBy("server_id") \
                       .agg(F.sum("bytes").alias("total_failed_bytes")) \
                       .orderBy(F.desc("total_failed_bytes"))
                       
    print("    -> AST (Abstract Syntax Tree) constructed. Zero data processed.")


    # --- 3. LOAD (The Physical Execution Action) ---
    print("\n  [PHASE 3: ACTION (Executing the DAG)]")
    # When we call `.show()` or `.collect()`, Spark compiles the DAG into Java bytecode,
    # broadcasts it to all 50 physical servers, executes the math in parallel,
    # and aggregates the final answer!
    
    start_action = timeit.default_timer()
    
    # We trigger the execution!
    results = transformed_df.limit(5).collect()
    
    end_action = timeit.default_timer()
    
    print(f"    -> Execution Time: {end_action - start_action:.2f} seconds")
    print("\n  [FINAL AGGREGATED RESULTS (Top 5 Failed Servers)]")
    for row in results:
        print(f"    -> {row['server_id']}: {row['total_failed_bytes']:,} bytes")
        
    
    # Shut down the JVM cluster
    spark.stop()
    print("\n  [SHUTDOWN] Spark Cluster terminated.")


def run_all_labs():
    demonstrate_big_data_pipeline()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Pandas is highly optimized using C-level SIMD instructions, why is it mathematically impossible to use Pandas on a $500$ GB dataset?"
   Senior Answer: "Pandas was architected strictly for 'Single-Node' execution. It fundamentally requires the entire dataset to reside in a single, contiguous block of RAM on a single physical machine. If the dataset exceeds the hardware's physical RAM limit (e.g., trying to load $500$ GB into $16$ GB of RAM), the OS will resort to 'Swapping' (thrashing the hard drive) and violently crash with an OOM error. PySpark solves this using 'Distributed Processing'. It mathematically slices the $500$ GB file into $5,000$ microscopic $100$ MB chunks. It streams these chunks through the CPU (or distributes them across $50$ physical servers). Because it only loads a microscopic fragment of the data into RAM at any given millisecond, PySpark is mathematically immune to memory limits, capable of processing Petabytes of data with only $4$ GB of RAM."

2. Interviewer: "What is a DAG (Directed Acyclic Graph), and why does PySpark utilize 'Lazy Evaluation'?"
   Senior Answer: "If you tell PySpark to `.filter()` a dataset, and then `.select()` two columns, and then `.limit(10)`, it physically does absolutely nothing. Instead, it mathematically records your intent into a DAG (a flowchart of operations). It waits until you invoke an 'Action' (like `.collect()` or `.write()`). At that exact millisecond, PySpark's Catalyst Optimizer analyzes the entire DAG. It realizes, 'Wait, if the user only wants $10$ rows at the end, I don't need to filter all $10$ billion rows! I only need to scan until I find $10$ matches, and then stop instantly!' If Spark executed eagerly like Pandas, it would have processed $10$ billion rows sequentially. Lazy evaluation allows the engine to mathematically re-write and optimize your code into the most efficient execution path before touching a single byte of data."

3. Interviewer: "Why does Python (PySpark) require a JVM (Java Virtual Machine) to execute Big Data workloads?"
   Senior Answer: "PySpark is simply a lightweight Python 'Wrapper' (API). The actual underlying framework, Apache Spark, is written in Scala (which runs on the JVM). When you write `df.filter(F.col('age') > 30)` in Python, you are not executing Python bytecode. The Py4J library instantly translates your Python command into Java bytecode and sends it to the Spark JVM via a local socket. The JVM handles all the heavy lifting: RAM allocation, Thread management, Network clustering, and Disk I/O. The Python process essentially sits idle, acting as a remote control, while the Java engines execute the raw mathematics."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Science (Big Data / PySpark) Completed.")
