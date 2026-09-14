"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (DATA SCIENCE PIPELINE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive CSV file containing 10,000,000 financial transactions is dropped on 
# a junior engineer's desk. They write a `for` loop, open the CSV, split the 
# strings, manually strip whitespace, cast strings to floats in a `try/except` 
# block, and calculate the sums. It takes 45 minutes to execute and crashes 
# on line 8,943,212 due to a missing comma.
#
# A senior Data Scientist understands the "ETL Pipeline" (Extract, Transform, Load). 
# They import `pandas`. They load the CSV directly into a vectorized C-level DataFrame. 
# They execute a mathematical `.dropna()`, physically vectorize the type-casting across 
# all 10,000,000 rows in a single SIMD instruction, and aggregate the sums using 
# `.groupby()`. The script executes in 4 seconds with mathematical perfection.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the ETL (Extract, Transform, Load) architectural pattern.
# - Master Vectorized Data Transformation using `pandas`.
# - Prove the performance disparity between standard Python iteration and Pandas.
#
# ==============================================================================
"""

import timeit
import csv
import io
import random
# Gracefully handle missing pandas dependency
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATING THE DIRTY DATASET (EXTRACT)
# ==============================================================================
def generate_dirty_csv(num_rows: int) -> str:
    """Generates a massive, corrupted CSV payload in memory."""
    print(f"  [INIT] Generating {num_rows:,} rows of dirty CSV data...")
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["transaction_id", "user_id", "amount", "status", "timestamp"])
    
    statuses = ["COMPLETED", "PENDING", "FAILED", " COMPLETED ", ""]
    
    for i in range(num_rows):
        # Inject intentional data corruption (Whitespace, nulls, wrong types)
        amt = random.uniform(10.0, 5000.0)
        status = random.choice(statuses)
        
        # 5% chance of a missing amount! (Corrupted Data)
        if random.random() < 0.05:
            amt = ""
            
        writer.writerow([f"TXN_{i}", random.randint(1, 100), amt, status, "2023-10-01 12:00:00"])
        
    return output.getvalue()


# ==============================================================================
# 4. THE NAIVE PYTHON PIPELINE (THE FOR LOOP)
# ==============================================================================
def naive_python_pipeline(csv_data: str) -> float:
    """
    Time Complexity: O(N)
    The CPU must dynamically type-check every single cell in Python Bytecode!
    """
    reader = csv.DictReader(io.StringIO(csv_data))
    
    total_revenue = 0.0
    
    for row in reader:
        # 1. Transform: Clean the status
        status = row["status"].strip().upper()
        
        # 2. Transform: Filter to COMPLETED only
        if status != "COMPLETED":
            continue
            
        # 3. Transform: Handle corrupted amounts
        amt_str = row["amount"]
        if amt_str == "":
            continue
            
        try:
            amt = float(amt_str)
        except ValueError:
            continue
            
        # 4. Load/Aggregate
        total_revenue += amt
        
    return total_revenue


# ==============================================================================
# 5. THE VECTORIZED PANDAS PIPELINE (THE C-LEVEL MATRIX)
# ==============================================================================
def pandas_vectorized_pipeline(csv_data: str) -> float:
    """
    Time Complexity: O(1) from the Python perspective! (Delegated to C/SIMD)
    """
    # 1. EXTRACT: Pandas builds the C-structs automatically!
    df = pd.read_csv(io.StringIO(csv_data))
    
    # 2. TRANSFORM: Vectorized String Operations!
    # Instead of a for loop, this single command applies `.strip().upper()` to 
    # the entire column in C.
    df["status"] = df["status"].str.strip().str.upper()
    
    # Transform: Drop any row where the amount is missing (NaN)!
    df = df.dropna(subset=["amount"])
    
    # Transform: Boolean Mask Filtering
    # This creates a binary array in C, instantly isolating the 'COMPLETED' rows!
    df = df[df["status"] == "COMPLETED"]
    
    # 3. LOAD / AGGREGATE
    # Sum the entire float64 array using C-level SIMD instructions!
    total_revenue = df["amount"].sum()
    
    return total_revenue


# ==============================================================================
# 6. MATHEMATICAL PROOF OF VECTORIZATION
# ==============================================================================
def demonstrate_etl_pipeline():
    section_header("Performance Proof: Naive Python vs Vectorized Pandas")
    
    if not HAS_PANDAS:
        print("  [ERROR] Pandas is not installed. Run `pip install pandas`.")
        return
        
    ROWS = 500_000 # Half a million rows!
    csv_payload = generate_dirty_csv(ROWS)
    
    print("\n  [SCENARIO A: PURE PYTHON `csv` MODULE]")
    start_py = timeit.default_timer()
    res_py = naive_python_pipeline(csv_payload)
    end_py = timeit.default_timer()
    time_py = end_py - start_py
    print(f"    -> Revenue Calculated: ${res_py:,.2f}")
    print(f"    -> Execution Time:     {time_py:.4f} seconds")
    
    print("\n  [SCENARIO B: VECTORIZED PANDAS]")
    start_pd = timeit.default_timer()
    res_pd = pandas_vectorized_pipeline(csv_payload)
    end_pd = timeit.default_timer()
    time_pd = end_pd - start_pd
    print(f"    -> Revenue Calculated: ${res_pd:,.2f}")
    print(f"    -> Execution Time:     {time_pd:.4f} seconds")
    
    # Notice: Pandas might actually be SLOWER on tiny datasets due to the C-API 
    # construction overhead, but on 500,000 rows, the SIMD acceleration takes over.
    if time_py > time_pd:
        speedup = time_py / time_pd
        print(f"\n  [CONCLUSION] Pandas outperformed Python Bytecode by {speedup:.1f}x!")
    else:
        print("\n  [CONCLUSION] Pandas lost! The C-API allocation overhead dwarfed the math.")
        print("  Increase the ROWS to 5,000,000 to see Pandas mathematically obliterate Python.")


def run_all_labs():
    demonstrate_etl_pipeline()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is an ETL Pipeline, and why is the 'Transform' step the most mathematically dangerous phase of Data Science?"
   Senior Answer: "ETL stands for Extract, Transform, Load. It is the architectural spine of Data Engineering. 'Extract' pulls raw data from databases, APIs, or massive CSV files. 'Transform' is where $90\\%$ of crashes occur: it requires scrubbing null values, coercing string dates into Unix timestamps, dropping corrupted rows, and normalizing strings. 'Load' pushes the clean data into a Data Warehouse (like Snowflake). Transform is dangerous because a single stray unicode character or `NaN` value mathematically destroys algorithms downstream. Attempting to execute a Machine Learning matrix multiplication on an array containing a single `NaN` value cascades the error, silently corrupting the entire neural network output."

2. Interviewer: "Explain the architecture of a Pandas DataFrame. Why does it consume so much RAM compared to reading a file line-by-line?"
   Senior Answer: "When you read a massive CSV line-by-line using standard Python, you only store $1$ row in RAM at a time ($O(1)$ memory). It is mathematically slow, but perfectly safe from OOM (Out-Of-Memory) crashes. A Pandas DataFrame is an In-Memory Columnar Datastore (backed by NumPy C-arrays). When you execute `pd.read_csv`, Pandas mathematically forces the *entire* CSV payload into RAM simultaneously, allocating massive, contiguous blocks of 64-bit floats and strings. A 1 GB CSV file can easily expand to 4 GB of RAM inside a DataFrame! You sacrifice memory safety to achieve lightning-fast, C-level SIMD vectorization across the entire dataset."

3. Interviewer: "In the Pandas pipeline, how does `df[df['status'] == 'COMPLETED']` mathematically filter the data without using a `for` loop?"
   Senior Answer: "This utilizes a concept called 'Boolean Masking'. The inner expression `df['status'] == 'COMPLETED'` does not execute a Python loop. It instructs the underlying C-code to evaluate the entire column against the string. The C-code generates a 'Boolean Array' of the exact same length (e.g., `[True, False, False, True...]`). When you pass this Boolean Array back into the DataFrame `df[...]`, the C-engine mathematically drops any row corresponding to `False`. The entire filter executes in a single vectorized sweep at bare-metal speeds, completely bypassing the Python interpreter's bytecode overhead."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Science (ETL Pipelines) Completed.")
