"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (STARTUPS - PERFORMANCE & GENERATORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Startups frequently process massive datasets (e.g., millions of database rows 
# or massive CSV files) using highly constrained cloud servers (e.g., 512MB RAM 
# AWS Lambda instances). 
#
# A junior engineer loads the entire 5GB dataset into a Python List. The 
# Lambda function instantly hits its memory ceiling and terminates with a 
# OOM (Out of Memory) crash. 
#
# A senior engineer uses Python Generators (`yield`) to build a Lazy Evaluation 
# Pipeline. Instead of loading 5GB into RAM, the Generator mathematically 
# streams the data exactly 1 element at a time, processing it, and instantly 
# garbage-collecting the previous element. The memory footprint drops from 5GB 
# down to exactly 50 bytes (O(1) space).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Generator Functions (`yield`) for infinite streams.
# - Master Generator Expressions for O(1) data transformations.
# - Understand how to chunk massive datasets dynamically.
#
# ==============================================================================
"""

import sys
import time
from typing import Generator, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERATORS (O(1) MEMORY STREAMING)
# ==============================================================================
def massive_data_stream(limit: int) -> Generator[int, None, None]:
    """
    Simulates a massive database fetch. 
    Instead of returning a giant List, it YIELDS one item at a time!
    """
    for i in range(limit):
        # YIELD pauses the function, returns the value, and perfectly preserves 
        # the local state until the caller requests the next value!
        yield i * 2

def demonstrate_generators():
    section_header("Startup: Generators vs Lists (Memory Profiles)")
    
    LIMIT = 10_000_000
    
    print(f"Task: Generate {LIMIT:,} even numbers.")
    
    # 1. THE BAD WAY: A List Comprehension
    # This executes completely, allocating a massive 10M item array in RAM.
    print("\n  [BAD] Using a List Comprehension...")
    start_time = time.perf_counter()
    bad_list = [i * 2 for i in range(LIMIT)]
    end_time = time.perf_counter()
    
    list_memory_mb = sys.getsizeof(bad_list) / (1024 * 1024)
    print(f"    -> Time to build: {(end_time - start_time):.2f} seconds")
    print(f"    -> RAM Consumed : {list_memory_mb:.2f} MB")
    
    # Clean up to prevent our lab from crashing!
    del bad_list
    
    # 2. THE GOOD WAY: A Generator Expression
    # Notice the parentheses `()` instead of brackets `[]`!
    print("\n  [GOOD] Using a Generator Expression `(...)`...")
    start_time = time.perf_counter()
    good_gen = (i * 2 for i in range(LIMIT))
    end_time = time.perf_counter()
    
    gen_memory_bytes = sys.getsizeof(good_gen)
    print(f"    -> Time to build: {(end_time - start_time):.6f} seconds (Instant!)")
    print(f"    -> RAM Consumed : {gen_memory_bytes} BYTES (Basically Zero!)")
    
    # To prove it works, let's extract the first 3 items!
    print("    -> Extracting data dynamically on-demand:")
    print(f"       next() -> {next(good_gen)}")
    print(f"       next() -> {next(good_gen)}")
    print(f"       next() -> {next(good_gen)}")


# ==============================================================================
# 4. CHUNKING (BATCH PROCESSING PIPELINES)
# ==============================================================================
def chunk_data(data: List[int], chunk_size: int) -> Generator[List[int], None, None]:
    """
    Time: O(N) | Space: O(Chunk Size)
    Splits a massive list into small, digestible chunks for database batch-inserts 
    or parallel processing.
    """
    for i in range(0, len(data), chunk_size):
        # We YIELD a slice of the list!
        yield data[i:i + chunk_size]

def demonstrate_chunking():
    section_header("Startup: Batch Chunking Pipeline")
    
    raw_data = list(range(1, 22)) # 1 to 21
    batch_size = 5
    
    print(f"Total Records: {len(raw_data)}")
    print(f"Batch Size: {batch_size}\n")
    
    # Initialize the generator
    pipeline = chunk_data(raw_data, batch_size)
    
    # Consume the chunks dynamically!
    batch_num = 1
    for chunk in pipeline:
        print(f"  [PROCESSING BATCH {batch_num}] -> DB Insert: {chunk}")
        batch_num += 1


def run_all_labs():
    demonstrate_generators()
    demonstrate_chunking()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the physical memory difference between `[x for x in data]` and `(x for x in data)`?"
   Senior Answer: "The first is a List Comprehension. The Python interpreter physically executes the entire loop, allocating memory for every single element simultaneously, and constructs a massive, contiguous Array in RAM. If the dataset is 10GB, the process will consume 10GB of RAM and likely crash the server. The second is a Generator Expression. It does not execute the loop. It creates a lightweight State Machine object in RAM (usually around 100 bytes). It only mathematically computes and returns a single element when the `next()` function is explicitly called, achieving perfect $O(1)$ constant memory utilization."

2. Interviewer: "What happens if you try to iterate over a Generator twice? (e.g., `for x in gen: print(x)`, and then immediately running that same loop again)?"
   Senior Answer: "The second loop will output absolutely nothing. Generators are strictly Single-Pass state machines. When a generator yields a value, it physically moves its internal state pointer forward. Once it hits the end of the data and raises the `StopIteration` exception, the state machine is mathematically exhausted and permanently dead. It does not cache or store the data it produced. If you need to iterate over the data multiple times, you must either instantiate a brand new generator, or cache the generator's output into a List (if RAM permits)."

3. Interviewer: "In a production microservice, why is Chunking (Batch Processing) superior to inserting records into a database one by one?"
   Senior Answer: "Inserting records one by one forces the application to establish a network connection, open a database transaction, execute an SQL statement, wait for disk I/O confirmation, and close the transaction for every single record. This introduces horrific network latency and I/O bottlenecking, limiting throughput to perhaps 50 inserts per second. By chunking the data (e.g., into arrays of 1,000 records) and using a Batch Insert (`executemany`), we amortize the network and transaction overhead across 1,000 records simultaneously. The database engine can heavily optimize the disk writes, increasing throughput to 50,000+ inserts per second."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Startup Prep (Performance & Generators) Completed.")
